# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, Union
if TYPE_CHECKING:
    from deepview.validator.evaluators import Parameters

from deepview.validator.exceptions import MissingLibraryException
from deepview.validator.datasets.utils import (
    letterbox_yolox,
    resize, 
)
from deepview.validator.runners.core import Runner
from deepview.validator.writers import logger
from time import monotonic_ns as clock_now
from timeit import timeit
import numpy as np

class ONNXRunner(Runner):
    """
    Runs ONNX models.
    
    Parameters
    ----------
        model: str
            The path to the model or the loaded ONNX model.

        parameters: Parameters
            These are the model parameters set from the command line.

        labels: list
            Unique string labels.

    Raises
    ------
        MissingLibraryException
            Raised if tflite_runtime library is not intalled.

        ValueError
                Raised if the provided image is
                neither a string path that points to the image nor is it a
                numpy.ndarray. Furthermore it raise if the
                provided image path does not exist.
    """
    def __init__(
        self,
        model,
        parameters: Parameters,
        labels: list=None
    ):
        super(ONNXRunner, self).__init__(model, parameters, labels)

        try:
            import onnxruntime
        except ImportError:
            raise MissingLibraryException(
                "onnxruntime~=1.16.3 or onnxruntime-gpu~=1.16.3 is needed to run ONNX models.")
        try:
            import torch
        except ImportError:
            raise MissingLibraryException(
                "torchvision~=0.15.2 is needed to check for cuda.")
        
        if isinstance(model, str):
            model = self.validate_model_path(model)
            cuda = torch.cuda.is_available() and parameters.engine != "cpu"  # use CUDA
            providers = ["CUDAExecutionProvider", "CPUExecutionProvider"] if cuda else ["CPUExecutionProvider"]
            self.session = onnxruntime.InferenceSession(model, providers=providers)
            self.output_names = [x.name for x in self.session.get_outputs()]
            self.graph_name = self.session.get_modelmeta().graph_name
        else:
            self.session = model
            self.model = "Training Model"

        self.update_nms()
        self.update_engine()

        if self.parameters.warmup > 0:
            # Produce a sample image of zeros.
            input_type = "float32" if "float" in self.get_input_type() else "uint32"
            height, width = self.get_input_shape()[2:4]
            image = np.expand_dims(np.zeros((height, width, 3)), 0).astype(np.dtype(input_type))
            image = np.transpose(image, axes=[0,3,1,2])
            logger("Loading model and warmup...", code="INFO")
            t = timeit(lambda: self.session.run(
                self.output_names, 
                {self.session.get_inputs()[0].name: image}), 
                number=self.parameters.warmup)
            logger("model warmup took %f seconds (%f ms avg)" %
                    (t, t * 1000 / self.parameters.warmup), code="INFO")
        
        # When filtering the model detection classes against the ground truth,
        # don't perform the auto offset.
        if (self.parameters.label_offset == 0 and 
            self.parameters.auto_offset and 
            not self.parameters.class_filter):
            self.parameters.label_offset = self.auto_offset()
            
    def auto_offset(self) -> int:
        """
        Initialize an auto offset parameter to reduce complexity for the
        manually setting the offset of the model indices due to 
        integer to string mapping mismatches.

        This is done by comparing the number of labels in the ground truth
        and the model outputs. Common patterns are for a coco128 model.

        ```
        shape=[1, 25200, 85]
        ```

        From this article https://medium.com/@KrashKart/i-wish-i-knew-this-about-yolov5-2fbab3584906,
        the first 5 rows (index 0 to 4) indicate, the probability of bounding 
        box coordinates (xmin, ymin, xmax, ymax) as well as the objectness per 
        grid cell for all grid cells.

        The next rows (5 to 85 in this case) are the probability of class 
        i existing at all grid cells.

        Returns
        -------
            offset: int
                The offset to apply towards the model indices.
        """
        shape = self.get_output_shape()
        if len(shape) == 3:
            yolo_converted = shape[-1] - 5
            label_count = yolo_converted if yolo_converted == len(self.labels) else shape[-1]
        else:
            label_count = 0

        if len(self.labels) == 0 or label_count == 0:
            return 0
        return len(self.labels) - label_count

    def run_single_instance(
        self, 
        image: Union[str, np.ndarray]
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Produce ONNX inference on one image and records the timings. 
        This method does not pad the images to match the input shape of the 
        model. This is different to yolov5 implementation where images are 
        padded: https://github.com/ultralytics/yolov5/blob/master/val.py#L197

        ONNX runner functionality was taken from:: \
        https://github.com/ultralytics/yolov5/blob/master/models/common.py#L487

        Parameters
        ----------
            image: str or np.ndarray
                The path to the image or numpy array image

        Returns
        -------
            nmsed_boxes: np.ndarray
                The prediction bounding boxes.. [[box1], [box2], ...].

            nmsed_classes: np.ndarray
                The prediction labels.. [cl1, cl2, ...].

            nmsed_scores: np.ndarray
                The prediction confidence scores.. [score, score, ...]
                normalized between 0 and 1.
        """

        """Input Preprocessing"""
        start = clock_now()
        height, width, _ = image.shape
        if self.parameters.letterbox:
            image, ratio = letterbox_yolox(image, self.get_input_shape()[2:4])
        else:
            # Take only the (height, width).
            image = resize(image, self.get_input_shape()[2:4]) 
            ratio = 1.0
        input_type = "float32" if "float" in self.get_input_type() else "uint32"
        image = self.apply_normalization(
            image, self.parameters.normalization, input_type)
        # Expects batch size, channel, height, width.
        image = np.transpose(image, axes=[0,3,1,2])
        load_ns = clock_now() - start
        self.loading_input_timings.append(load_ns * 1e-6)

        """Inference"""
        start = clock_now()
        outputs = self.session.run(self.output_names, {self.session.get_inputs()[0].name: image})
        infer_ns = clock_now() - start
        self.inference_timings.append(infer_ns * 1e-6)

        """Postprocessing"""
        start = clock_now()
        # An output with 7 columns refers to batch_id, xmin, ymin, xmax, ymax, cls, score.
        # Otherwise it is batch_size, number of boxes, number of classes which needs external NMS.
        nmsed_boxes, nmsed_classes, nmsed_scores = self.postprocessing(outputs, ratio, (height, width))
        decoder_ns = clock_now() - start
        self.box_timings.append(decoder_ns * 1e-6)
        return nmsed_boxes, nmsed_classes, nmsed_scores

    def postprocessing(
            self, 
            output: Union[list, np.ndarray],
            ratio: float,
            image_shape: tuple,
        ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Retrieves the boxes, scores and labels. This method will perform NMS
        operations where the outputs will be transformed into the following format.

        Models converted internally will directly return the nms
        bounding boxes, scores, and labels as described below.

        Models converted in YoloV5 will be a list of length 1 which 
        is formatted in the following way which has a shape of (1, number of boxes, 6).
        [[[xmin, ymin, xmax, ymax, confidence, label], [...], ...]]. 

        Models converted in YoloV7 will extract the bounding boxes, scores,
        and labels from the output and directly return.

        Parameters
        ----------
            output: list or np.ndarray

                Pre NMS
                -------
                Models converted internally will be a list with length of 2
                containing the bounding boxes as the first element and the scores
                for the second element which needs to be passed to NMS.

                Models converted in YoloV5 requires torch NMS which has the 
                following shape (batch size, number of boxes, number of classes).
                The output is a torch.Tensor.

                Models converted in YoloV7 will already have NMS embedded. The
                output will be a torch.Tensor in the following format which 
                has a shape of (number of boxes, 7).
                [[batch_id, xmin, ymin, xmax, ymax, cls, score], ...]

            ratio: float
                This is the ratio value from the letterbox transformation
                to adjust the bounding boxes.

            image_shape: tuple
                This is the original resolution of the image to normalize
                coordinates.

        Returns
        -------
            nmsed_boxes: np.ndarray
                The prediction bounding boxes.. [[box1], [box2], ...].

            nmsed_classes: np.ndarray
                The prediction labels.. [cl1, cl2, ...].

            nmsed_scores: np.ndarray
                The prediction confidence scores.. [score, score, ...]
                normalized between 0 and 1.
        """
        # Indicates YOLOv5, YOLOv7 exported models.
        if self.graph_name == "main_graph":
            # Convert to NumPy.
            if isinstance(output, (list, tuple)):
                output = self.from_numpy(output[0]) if len(output) == 1 else [
                    self.from_numpy(x) for x in output]
            else:
                output = self.from_numpy(output)

        if isinstance(output, list):
            if self.graph_name != "main_graph":
                nmsed_boxes, nmsed_classes, nmsed_scores = self.process_yolox(output, ratio, image_shape)
            else:
                nmsed_boxes, nmsed_classes, nmsed_scores = self.process_internal(output)
        else:
            nmsed_boxes, nmsed_classes, nmsed_scores = self.process_yolov(output)

        if self.parameters.class_filter:
            nmsed_boxes, nmsed_classes, nmsed_scores = self.class_filter(
                nmsed_boxes, nmsed_classes, nmsed_scores
            )
        if self.parameters.label_offset != 0:
            nmsed_classes += self.parameters.label_offset
        nmsed_classes = self.index2string(nmsed_classes)
        return nmsed_boxes, nmsed_classes, nmsed_scores
    
    def process_internal(
            self, 
            output: Union[list, np.ndarray]
        ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Process internal exported models.

        Parameters
        ----------
            output: list, np.ndarray
                Models converted internally will be a list with length of 2
                containing the bounding boxes as the first element and the scores
                for the second element which needs to be passed to NMS.

        Returns
        -------
            nmsed_boxes: np.ndarray
                The prediction bounding boxes.. [[box1], [box2], ...].

            nmsed_classes: np.ndarray
                The prediction labels.. [cl1, cl2, ...].

            nmsed_scores: np.ndarray
                The prediction confidence scores.. [score, score, ...]
                normalized between 0 and 1.
        """
        if len(output) == 2: # Internal converted model.
            return self.tensorflow_nms(
                    output[0].reshape([1,-1,1,4]) / self.get_input_shape()[2],
                    output[1], 
                    clip_boxes=True)
        else:
            logger("Postprocessing for this model output is not yet supported.", code="ERROR")
    
    def process_yolov(
            self, 
            output: Union[list, np.ndarray]
        ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Process YOLOv5 and YOLOv7 exported models.

        Parameters
        ----------
            output: list or np.ndarray
                Models converted in YoloV5 requires torch NMS which has the 
                following shape (batch size, number of boxes, number of classes).
                The output is a torch.Tensor.

                Models converted in YoloV7 will already have NMS embedded. The
                output will be a torch.Tensor in the following format which 
                has a shape of (number of boxes, 7).
                [[batch_id, xmin, ymin, xmax, ymax, cls, score], ...]

        Returns
        -------
            nmsed_boxes: np.ndarray
                The prediction bounding boxes.. [[box1], [box2], ...].

            nmsed_classes: np.ndarray
                The prediction labels.. [cl1, cl2, ...].

            nmsed_scores: np.ndarray
                The prediction confidence scores.. [score, score, ...]
                normalized between 0 and 1.
        """
        h, w = self.get_input_shape()[2:4]
        # YoloV5 converted model.
        if output.shape[1] != 7:
            output = self.torch_nms(output)
            outputs = output[0].numpy()
            outputs[..., :4] /= [w, h, w, h]

            nmsed_boxes = outputs[..., :4]
            # Single dimensional arrays gets converted to the element. 
            # Specify the axis into 1 to prevent that.
            nmsed_scores = np.squeeze(outputs[..., 4:5], axis=1)
        # YoloV7 converted model.
        else: 
            outputs = output.numpy()
            outputs[..., 1:5] /= [w, h, w, h]
            nmsed_boxes = outputs[..., 1:5]
            # Single dimensional arrays gets converted to the element. 
            # Specify the axis into 1 to prevent that.
            nmsed_scores = np.squeeze(outputs[..., 6:7], axis=1)
        nmsed_classes = np.squeeze(outputs[...,5:6], axis=1)
        return nmsed_boxes, nmsed_classes, nmsed_scores

    def process_yolox(
            self, 
            outputs: Union[list, np.ndarray], 
            ratio: float,
            image_shape: tuple,
            p6: bool=False
        ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        This performs postprocessing of YOLOx models.
        Method taken from https://github.com/Megvii-BaseDetection/YOLOX/blob/main/yolox/utils/demo_utils.py#L139

        Parameters
        ----------
            output: list or np.ndarray
                This is the output of the model to postprocess into
                bounding boxes, classes, scores after NMS.

            ratio: float
                This is the ratio value from the letterbox transformation
                to adjust the bounding boxes.

            image_shape: tuple
                This is the original resolution of the image to normalize
                coordinates.

            p6: bool

        Returns
        -------
            nmsed_boxes: np.ndarray
                The prediction bounding boxes.. [[box1], [box2], ...].

            nmsed_classes: np.ndarray
                The prediction labels.. [cl1, cl2, ...].

            nmsed_scores: np.ndarray
                The prediction confidence scores.. [score, score, ...]
                normalized between 0 and 1.
        """
        height, width = self.get_input_shape()[2:4]

        grids = []
        expanded_strides = []
        strides = [8, 16, 32] if not p6 else [8, 16, 32, 64]

        hsizes = [height // stride for stride in strides]
        wsizes = [width // stride for stride in strides]
        output = outputs[0]
        for hsize, wsize, stride in zip(hsizes, wsizes, strides):
            xv, yv = np.meshgrid(np.arange(wsize), np.arange(hsize))
            grid = np.stack((xv, yv), 2).reshape(1, -1, 2)
            grids.append(grid)
            shape = grid.shape[:2]
            expanded_strides.append(np.full((*shape, 1), stride))

        grids = np.concatenate(grids, 1)
        expanded_strides = np.concatenate(expanded_strides, 1)
        output[..., :2] = (output[..., :2] + grids) * expanded_strides
        output[..., 2:4] = np.exp(output[..., 2:4]) * expanded_strides
        predictions = output[0]
        boxes = predictions[:, :4]
        scores = predictions[:, 4:5] * predictions[:, 5:]

        boxes_xyxy = np.ones_like(boxes)
        boxes_xyxy[:, 0] = boxes[:, 0] - boxes[:, 2]/2.
        boxes_xyxy[:, 1] = boxes[:, 1] - boxes[:, 3]/2.
        boxes_xyxy[:, 2] = boxes[:, 0] + boxes[:, 2]/2.
        boxes_xyxy[:, 3] = boxes[:, 1] + boxes[:, 3]/2.
        boxes_xyxy /= ratio

        # Typical: nms_thr=0.45, score_thr=0.1
        dets = self.multiclass_nms(
            boxes_xyxy, 
            scores, 
            nms_thr=self.parameters.detection_iou, 
            score_thr=self.parameters.detection_score
        )
        if dets is None:
            return np.array([]), np.array([]), np.array([])
        nmsed_boxes = dets[:, :4]
        nmsed_scores = dets[:, 4]
        nmsed_classes = dets[:, 5]
        nmsed_boxes /= [image_shape[1], image_shape[0], image_shape[1], image_shape[0]]
        return nmsed_boxes, nmsed_classes, nmsed_scores

    def get_input_type(self) -> str:
        """
        This returns the input type of the model.

        Returns
        -------
            type: str
                The input type of the model.
        """
        return self.session.get_inputs()[0].type

    def get_input_shape(self) -> np.ndarray:
        """
        Grabs the model input shape.

        Returns
        -------
            shape: np.ndarray
                The model input shape.
                (batch size, channels, height, width).
        """
        return self.session.get_inputs()[0].shape
    
    def get_output_type(self) -> str:
        """
        This returns the output type of the model.

        Returns
        -------
            type: str
                The output type of the model.
        """
        return self.session.get_outputs()[-1].type
    
    def get_output_shape(self) -> np.ndarray:
        """
        Grabs the model output shape.

        Returns
        --------
            shape: np.ndarray
                The model output shape.
                (batch size, boxes, classes).
        """
        return self.session.get_outputs()[-1].shape
    
    def get_metadata(self) -> dict:
        """
        This returns the model metadata containing stride and label names
        mapping.

        Returns
        -------
            meta: dict
                Contains the model stride and the label mappings.
        """
        return self.session.get_modelmeta().custom_metadata_map  # metadata