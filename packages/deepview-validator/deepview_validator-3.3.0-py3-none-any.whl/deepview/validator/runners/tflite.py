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
from deepview.validator.datasets.utils import resize
from deepview.validator.runners.core import Runner
from deepview.validator.writers import logger
from time import monotonic_ns as clock_now
from timeit import timeit
import numpy as np

class TFliteRunner(Runner):
    """
    Runs TensorFlow Lite models.
    
    Parameters
    ----------
        model: str or tflite interpreter.
            The path to the model or the loaded tflite model.

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
        super(TFliteRunner, self).__init__(model, parameters, labels)
        try:  # https://coral.ai/docs/edgetpu/tflite-python/#update-existing-tf-lite-code-for-the-edge-tpu
            from tflite_runtime.interpreter import (  # type: ignore
                Interpreter, 
                load_delegate
            ) 
        except ImportError:
            try:
                import tensorflow as tf
                Interpreter, load_delegate = ( # NOSONAR
                    tf.lite.Interpreter,
                    tf.lite.experimental.load_delegate,
                )
            except ImportError:
                raise MissingLibraryException(
                    "tensorflow>=2.8.0,<2.16.0 or tflite_runtime is needed to load the model. ")

        if isinstance(model, str):
            model = self.validate_model_path(model)
            self.interpreter = Interpreter(model_path=model)  # load TFLite model
        else:
            self.interpreter = model
            self.model = "Training Model"

        self.interpreter.allocate_tensors()  # allocate
        self.update_nms()
        self.update_engine()
    
        if self.parameters.warmup > 0:
            logger("Loading model and warmup...", code="INFO")
            t = timeit(self.interpreter.invoke, number=self.parameters.warmup)
            logger("model warmup took %f seconds (%f ms avg)" %
                           (t, t * 1000 / self.parameters.warmup), code="INFO")

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
        [    1, 25200,    85]
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
        Produce tflite predictions on one image and records the timings. 
        This method does not pad the images to match the input shape of the 
        model. This is different to yolov5 implementation where images are 
        padded: https://github.com/ultralytics/yolov5/blob/master/val.py#L197

        Tflite runner functionality was taken from:: \
        https://github.com/ultralytics/yolov5/blob/master/models/common.py#L579

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
        # Take only the (height, width).
        image = resize(image, self.get_input_shape()[1:3]) 
        tensor = self.apply_normalization(
            image, self.parameters.normalization, self.get_input_type())
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()
        self.interpreter.set_tensor(input_details[0]['index'], tensor)
        load_ns = clock_now() - start
        self.loading_input_timings.append(load_ns * 1e-6)
        
        """Inference"""
        start = clock_now()
        self.interpreter.invoke()
        infer_ns = clock_now() - start
        self.inference_timings.append(infer_ns * 1e-6)

        """Postprocessing"""
        start = clock_now()
        outputs = []
        for output in output_details:
            # is TFLite quantized uint8 model.
            int8 = input_details[0]["dtype"] == np.uint8  
            x = self.interpreter.get_tensor(output["index"])
            if int8:
                scale, zero_point = output["quantization"]
                x = (x.astype(np.float32) - zero_point) * scale  # re-scale
            outputs.append(x)
            
        nmsed_boxes, nmsed_classes, nmsed_scores = self.postprocessing(outputs)
        decoder_ns = clock_now() - start
        self.box_timings.append(decoder_ns * 1e-6)
        return nmsed_boxes, nmsed_classes, nmsed_scores

    def postprocessing(
            self, 
            outputs: list
        ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Retrieves the boxes, scores and labels.

        Parameters
        ----------
            output: list
                This is the raw detections of the model with the following shape
                (batch size, number of boxes, number of classes).

                After NMS, it will be transformed into a list of length 1 with
                a shape of (1, number of boxes, 6).
                [[[xmin, ymin, xmax, ymax, confidence, label], [...], ...]]. 

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
        outputs = [x if isinstance(x, np.ndarray) else x.numpy() for x in outputs]
        if len(outputs) == 2:
            nmsed_boxes, nmsed_classes, nmsed_scores = self.process_internal(outputs)
        else:
            nmsed_boxes, nmsed_classes, nmsed_scores = self.process_yolov(outputs)

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
            outputs: list
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
        for output in outputs:
            if output.shape[-1] == 4:
                boxes = output
            else:
                scores = output
        return self.tensorflow_nms(
                    boxes.reshape([1,-1,1,4]),
                    scores, 
                    clip_boxes=True)
    
    def process_yolov( # NOSONAR
            self, 
            outputs: list
        ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Process YOLOv5 exported models.

        Parameters
        ----------
            output: list or np.ndarray
                Models converted in YoloV5 requires torch NMS which has the 
                following shape (batch size, number of boxes, number of classes).
                The output is a torch.Tensor.

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
        if len(outputs) == 1:
            h, w = self.get_input_shape()[1:3]
            # NMS requires non-normalized coordinates.
            outputs[0][..., :4] *= [w, h, w, h]  # xywh normalized to pixels.
            if isinstance(outputs, (list, tuple)):
                output = self.from_numpy(outputs[0]) if len(outputs) == 1 else [
                    self.from_numpy(x) for x in outputs]
            else:
                output = self.from_numpy(outputs)

            output = self.torch_nms(output)
            outputs = output[0].numpy()
            outputs[..., :4] /= [w, h, w, h]
            
            nmsed_boxes = outputs[..., :4]
            # Single dimensional arrays gets converted to the element. 
            # Specify the axis into 1 to prevent that.
            nmsed_scores = np.squeeze(outputs[..., 4:5], axis=1)
            nmsed_classes = np.squeeze(outputs[...,5:6], axis=1)
        elif len(outputs) == 4:
            # For YOLOv5 converted models with NMS embedded.
            # boxes = (1, 100, 4), batch_size = (1,), classes = (1, 100), scores = (1, 100).
            nmsed_scores, nmsed_classes = None, None
            for output in outputs:
                if output.shape[-1] == 4:
                    nmsed_boxes = output[0]
                elif len(output.shape) == 2:
                    # If all values are 0 or 1, then this could be classes.
                    unique = np.unique(output[0])
                    if len(unique) == 1 and (unique[0] == 0 or unique[0] == 1):
                        nmsed_classes = output[0]
                    # If all values are in between 0 and 1, then this could be scores.
                    elif np.all(np.logical_and(output[0] >= 0, output[0] <= 1)):
                        nmsed_scores = output[0]
                    # Other combinations should just be classes.
                    else:
                        nmsed_classes = output[0]
            if nmsed_scores is None or nmsed_classes is None:
                return np.array([]), np.array([]), np.array([])
        else:
            logger(
                "Postprocessing for this model output is not yet supported.", 
                code="ERROR")
        return nmsed_boxes, nmsed_classes, nmsed_scores
    
    def get_input_type(self) -> str:
        """
        This returns the input type of the model.

        Returns
        -------
            type: str
                The input type of the model.
        """
        return self.interpreter.get_input_details()[0]["dtype"].__name__

    def get_input_shape(self) -> np.ndarray:
        """
        Grabs the model input shape.

        Returns
        -------
            shape: np.ndarray
                The model input shape.
                (batch size, height, width, channels).
        """
        return self.interpreter.get_input_details()[0]["shape"]
    
    def get_output_type(self) -> str:
        """
        This returns the output type of the model.

        Returns
        -------
            type: str
                The output type of the model.
        """
        return self.interpreter.get_output_details()[-1]["dtype"].__name__
    
    def get_output_shape(self) -> np.ndarray:
        """
        Grabs the model output shape.

        Returns
        --------
            shape: np.ndarray
                The model output shape.
                (batch size, boxes, classes).
        """
        return self.interpreter.get_output_details()[-1]["shape"]