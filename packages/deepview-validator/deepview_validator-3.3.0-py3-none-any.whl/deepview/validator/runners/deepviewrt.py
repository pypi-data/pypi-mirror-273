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

from deepview.validator.exceptions import NonMatchingIndexException
from deepview.validator.exceptions import MissingLibraryException
from deepview.validator.runners.core import Runner
from deepview.validator.writers import logger
from time import monotonic_ns as clock_now
from timeit import timeit
import numpy as np
import os

class DeepViewRTRunner(Runner):
    """
    Runs DeepViewRT models using the VAAL API.
    
    Parameters
    ----------
        model: str 
            The path to the model.

        parameters: Parameters
            These are the model parameters set from the command line.

        labels: list
            Unique string labels.

    Raises
    ------
        NonMatchingIndexException
            Raised if the model outputs an index
            that is out of bounds to the labels list passed
            or the labels contained within the model itself.

        MissingLibraryException
            Raised if the deepview.vaal library is not found.

        NotImplementedError
            Some methods have not been implemented yet.

        ValueError
            Raised if the provided image is neither a string
            nor a np.ndarray.
    """
    def __init__(
        self,
        model: str,
        parameters: Parameters,
        labels: list=None
    ):
        super(DeepViewRTRunner, self).__init__(model, parameters, labels)
        
        try:
            import deepview.vaal as vaal # type: ignore
        except ImportError:
            raise MissingLibraryException(
                "vaal library is needed to run DeepViewRT models.")
        
        try:
            self.ctx = vaal.Context(self.parameters.engine)
        except AttributeError:
            raise EnvironmentError(
                'Did not find Vaal Context. Try setting the environment \
                    variable VAAL_LIBRARY to the VAAL library.')
        # Change because VAAL automatically uses CPU if NPU is unavailable.
        self.parameters.engine = self.ctx.device

        if self.parameters.max_detections is not None:
            self.ctx['max_detection'] = self.parameters.max_detections

        self.ctx['score_threshold'] = self.parameters.detection_score
        self.ctx['iou_threshold'] = self.parameters.detection_iou
        self.ctx['box_format'] = self.parameters.box_format

        if (self.parameters.nms is not None and 
            self.parameters.nms in ['standard', 'fast', 'matrix']):
            self.ctx['nms_type'] = self.parameters.nms
        else:
            # Fast is the default usage in VAAL.
            self.parameters.nms = "fast"

        if self.parameters.normalization == 'raw':
            self.ctx['proc'] = vaal.ImageProc.RAW
        elif self.parameters.normalization == 'signed':
            self.ctx['proc'] = vaal.ImageProc.SIGNED_NORM
        elif self.parameters.normalization == 'unsigned':
            self.ctx['proc'] = vaal.ImageProc.UNSIGNED_NORM
        elif self.parameters.normalization == 'whitening':
            self.ctx['proc'] = vaal.ImageProc.WHITENING
        elif self.parameters.normalization == 'imagenet':
            self.ctx['proc'] = vaal.ImageProc.IMAGENET
        else:
            logger(f"Unsupported normalization method: {self.parameters.normalization}", 
                   code="ERROR")

        model = self.validate_model_path(model)
        self.ctx.load_model(model)
        if int(self.parameters.warmup) > 0:
            logger("Loading model and warmup...", code="INFO")
            t = timeit(self.ctx.run_model, number=self.parameters.warmup)
            logger("model warmup took %f seconds (%f ms avg)\n" %
                    (t, t * 1000 / self.parameters.warmup), code="INFO")

        if self.parameters.label_offset == 0 and self.parameters.auto_offset:
            self.parameters.label_offset = self.auto_offset()
            
    def auto_offset(self) -> int:
        """
        Initialize an auto offset parameter to reduce complexity for the
        manually setting the offset of the model indices due to 
        integer to string mapping mismatches.

        This is done by comparing the number of labels in the ground truth
        and the model outputs. Common patterns are for a playing cards model.

        Properly converted.
        ```
        out.shape=(1, 1500, 13)   <-- number of labels
        out.shape=(1, 1500, 1, 4)
        ```

        Improperly converted.
        ```
        out.shape=(1, 20, 20, 57)
        out.shape=(1, 1500, 1, 4)
        out.shape=(1, 1500, 14)    <-- number of labels
        out.shape=(1, 10, 10, 57)
        ```

        Returns
        -------
            offset: int
                The offset to apply towards the model indices.
        """
        label_count = 0
        shape = self.get_output_shape()
        if shape is not None:
            label_count = shape[-1]
        
        if len(self.labels) == 0 or label_count == 0:
            return 0
        return len(self.labels) - label_count
    
    def apply_offset(self, label: int) -> int:
        """
        Apply label offset to the model output. The offset set in the command
        line is applied if it is set. Otherwise, the auto offset feature
        will be used. 

        Parameters
        ----------
            label: int
                This is the current label output of the model.

        Parameters
        ----------
            label: int
                This is the index with the applied offset.
        """
        if self.parameters.label_offset != 0:
            label = label + self.parameters.label_offset

        if label < 0:
            raise ValueError(
                f"The model label resulted in a negative integer: {label}")
        return label

    def run_single_instance(
            self, 
            image: Union[str, np.ndarray]
        ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Runs deepviewrt models and parses the prediction 
        bounding boxes, scores, and labels and records timings 
        (load, inference, box).
        
        Parameters
        ----------
            image: str or np.ndarray
                This can be a path to the image file or a numpy array
                image.

        Returns
        -------
            boxes: np.ndarray
                The prediction bounding boxes.. [[box1], [box2], ...].

            classes: np.ndarray
                The prediction labels.. [cl1, cl2, ...].

            scores: np.ndarray
                The prediction confidence scores.. [score, score, ...]
                normalized between 0 and 1.

        Raises
        ------
            ValueError
                Raised if the provided image is neither a string
                nor a numpy.ndarray.
        """
        if isinstance(image, str):
            start = clock_now()
            self.ctx.load_image(image)
            load_ns = clock_now() - start
        elif isinstance(image, np.ndarray):
            start = clock_now()
            rgba_image = np.concatenate(
                (image, np.zeros((image.shape[0], image.shape[1], 1))), axis=2)
            self.ctx.load_image(rgba_image.astype(np.uint8))
            load_ns = clock_now() - start
        else:
            raise ValueError(
                "The provided image is neither a path nor a np.ndarray. " +
                "Provided with type: {}".format(type(image)))
        self.loading_input_timings.append(load_ns * 1e-6)

        start = clock_now()
        self.ctx.run_model()
        infer_ns = clock_now() - start
        self.inference_timings.append(infer_ns * 1e-6)

        start = clock_now()
        if self.parameters.nms == "tensorflow": 
            outputs = list()
            for i in range(4):
                out = self.ctx.output(index=i)
                if out is not None:
                    outputs.append(out.dequantize().array())
        else:
            outputs = self.ctx.boxes()
        boxes_ns = clock_now() - start
        self.box_timings.append(boxes_ns * 1e-6)
        return self.postprocessing(outputs)

    def postprocessing(
            self, 
            outputs: list
        ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Collects the bounding boxes, scores and labels for the image.
       
        Parameters
        ----------
            outputs: list
                This contains bounding boxes, scores, labels.

        Returns
        -------
            boxes: np.ndarray
                The prediction bounding boxes.. [[box1], [box2], ...].

            classes: np.ndarray
                The prediction labels.. [cl1, cl2, ...].

            scores: np.ndarray
                The prediction confidence scores.. [score, score, ...]
                normalized between 0 and 1.
        """
        if self.parameters.nms == "tensorflow":
            boxes, scores = self.decode_outputs(outputs)
            boxes, classes, scores = self.process_tensorflow_nms(boxes, scores)
        else:
            boxes, classes, scores = list(), list(), list()
            for box in outputs:
                output = self.process_vaal_nms(box)
                if output is not None:
                    label, box, score = output
                    classes.append(label)
                    boxes.append(box)
                    scores.append(score)
                else:
                    return output
        return np.array(boxes), np.array(classes), np.array(scores)
    
    @staticmethod
    def decode_outputs(outputs: list) -> Tuple[np.ndarray, np.ndarray]:
        """
        Outputs from the context is decoded into boxes and scores based
        on its shape.

        Parameters
        ----------
            outputs: list
                This contains bounding boxes, scores, labels.

        Returns
        ----------
            boxes: np.ndarray
                This array contains the bounding boxes for one image.
            
            scores: np.ndarray
                This array contains the model score per bounding box.
        """
        boxes, scores = None, None
        for output in outputs:
            if len(output.shape) == 3:
                scores = output
                continue
            if output.shape[-1] == 4 and output.shape[-2] == 1:
                boxes = output
        return boxes, scores
    
    def process_vaal_nms(self, box):
        """
        Processes model detections using the VAAL NMS.

        Parameters
        ----------
            box: deepview.vaal.library.VAALBox
                This contains the label, box, and score from the model.

        Returns
        -------
            The NMS processed label, box, and score.

        Raises
        ------
            NonMatchingIndexException
                Raised if the label index 
                returned by the model does not match any index position in
                either context labels or the provided labels from the dataset.
        """
        if len(self.ctx.labels) > 0:
            if self.ctx.label(box.label) == "VisionPack Trial Expired":
                return None
            else:
                dt_class = self.ctx.label(box.label).lower().rstrip(
                    '\"').lstrip('\"')
        elif len(self.labels) > 0:
            label = self.apply_offset(box.label)
            try:
                dt_class = self.labels[label].lower().rstrip(
                    '\"').lstrip('\"')
            except IndexError:
                raise NonMatchingIndexException(label)
        else:
            label = self.apply_offset(box.label)
            dt_class = label
        dt_box = [box.xmin, box.ymin, box.xmax, box.ymax]
        dt_score = box.score
        return dt_class, dt_box, dt_score
       
    def process_tensorflow_nms(
            self, 
            boxes: np.ndarray, 
            scores: np.ndarray
        ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Processes model detections using TensorFlow NMS.
       
        Parameters
        ----------
            boxes: np.ndarray
                This array contains the bounding boxes for one image.
            
            scores: np.ndarray
                This array contains the model score per bounding box.

        Returns
        -------
            labels, bounding boxes, scores: np.ndarray
                These are the model detections after being processed using
                TensorFlow NMS.
        
        Raises
        ------
            NonMatchingIndexException
                Raised if the model label index does
                not match any index position in the provided labels from
                the dataset. 
        """
        try:
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
            import tensorflow as tf
        except ImportError:
            raise MissingLibraryException(
                "tensorflow>=2.8.0,<2.16.0 is needed to perform NMS operations.")

        # Negative offsets could mean that the model contains the background class,
        # but the dataset does not.
        if self.parameters.label_offset < 0:
            scores = scores[..., abs(self.parameters.label_offset):]
        # Positive offsets could mean that the dataset contains the background class,
        # but the dataset does not.
        # TODO: Consider cases where the offset might be positive.

        nms_predicted_boxes, nms_predicted_classes, nms_predicted_scores =\
            self.tensorflow_nms(
                boxes.astype(np.float32), 
                scores.astype(np.float32),
            )
        nms_predicted_classes = self.index2string(nms_predicted_classes)
        return nms_predicted_boxes, nms_predicted_classes, nms_predicted_scores

    def get_input_type(self):
        """
        Returns the model input type.

        Returns
        -------
            type: str
                The model input type.

        Raises
        ------
            NotImplementedError
                raise because it has not been implemented yet.
        """
        raise NotImplementedError("has not been implemented.")

    def get_input_shape(self):
        """
        Grabs the model input shape.
        
        Returns
        -------
            type: tuple or list
                The model input shape.
        """
        return self.ctx.tensor('serving_default_input_1:0').shape
    
    def get_output_type(self):
        """
        Returns the model output type.

        Returns
        -------
            type: str
                The model output type.

        Raises
        ------
            NotImplementedError
                raise because it has not been implemented yet.
        """
        raise NotImplementedError("has not been implemented.")

    def get_output_shape(self) -> Union[tuple, None]:
        """
        Grabs the model output shape. Only returns shapes with lengths of 3.

        Properly converted.
        ```
        out.shape=(1, 1500, 13)   <-- number of labels
        out.shape=(1, 1500, 1, 4)
        ```

        Improperly converted.
        ```
        out.shape=(1, 20, 20, 57)
        out.shape=(1, 1500, 1, 4)
        out.shape=(1, 1500, 14)    <-- number of labels
        out.shape=(1, 10, 10, 57)
        ```

        Returns
        -------
            shape: tuple (1x3)
                The output shape (batch size, number of boxes, number of labels).
        """
        for i in range(4):
            out = self.ctx.output(index=i)
            if out is None:
                continue
            shape = out.array().shape
            if len(shape) == 3:
                return shape
        return None
    
class SegmentationDeepViewRTRunner(Runner):
    """
    Runs DeepViewRT Segmentationmodels using the VAAL API.
    
    Parameters
    ----------
        model: str 
            The path to the model.

        parameters: Parameters
            These are the model parameters set from the command line.

    Raises
    ------
        MissingLibraryException
            Raised if the deepview.vaal library is not found.

        ValueError
            Raised if the provided image_path
            does not exist and the provided image is not a numpy.ndarray.
    """
    def __init__(
        self,
        model: str,
        parameters: Parameters
    ):
        super(SegmentationDeepViewRTRunner, self).__init__(model, parameters)
        
        try:
            import deepview.vaal as vaal # type: ignore
        except ImportError:
            raise MissingLibraryException(
                "vaal library is needed to run DeepViewRT models.")

        try:
            self.ctx = vaal.Context(self.parameters.engine)
        except AttributeError:
            raise EnvironmentError(
                'Did not find Vaal Context. Try setting the environment \
                    variable VAAL_LIBRARY to the VAAL library.')
        
        # Change because VAAL automatically uses CPU if NPU is unavailable.
        self.parameters.engine = self.ctx.device

        if self.parameters.normalization == 'raw':
            self.ctx['proc'] = vaal.ImageProc.RAW
        elif self.parameters.normalization == 'signed':
            self.ctx['proc'] = vaal.ImageProc.SIGNED_NORM
        elif self.parameters.normalization == 'unsigned':
            self.ctx['proc'] = vaal.ImageProc.UNSIGNED_NORM
        elif self.parameters.normalization == 'whitening':
            self.ctx['proc'] = vaal.ImageProc.WHITENING
        elif self.parameters.normalization == 'imagenet':
            self.ctx['proc'] = vaal.ImageProc.IMAGENET
        else:
            logger(f"Unsupported normalization method: {self.parameters.normalization}", 
                   code="ERROR")

        model = self.validate_model_path(model)
        self.ctx.load_model(model)
        if int(self.parameters.warmup) > 0:
            logger("Loading model and warmup...", code="INFO")
            t = timeit(self.ctx.run_model, number=self.parameters.warmup)
            logger("model warmup took %f seconds (%f ms avg)\n" %
                          (t, t * 1000 / self.parameters.warmup), code="INFO")
            
    def run_single_instance(self, image: Tuple[str, np.ndarray]) -> np.ndarray:
        """
        Runs deepviewrt models to produce prediction masks 
        on the provided image and records timings (load, inference, box).
        
        Parameters
        ----------
            image: str or np.ndarray
                This can be a path to the image file or a numpy array.    
            
        Returns
        -------
            mask: np.ndarray
                This is the segmentation mask of the image 
                where each pixel is represented by a class in
                the image.

        Raises
        ------
            ValueError
                Raised if the provided image is neither a string nor
                a numpy.ndarray.
        """
        if isinstance(image, str):
            start = clock_now()
            self.ctx.load_image(image)
            load_ns = clock_now() - start
        elif isinstance(image, np.ndarray):
            start = clock_now()
            rgba_image = np.concatenate(
                (image, np.zeros((image.shape[0], image.shape[1], 1))), axis=2)
            self.ctx.load_image(rgba_image.astype(np.uint8))
            load_ns = clock_now() - start
        else:
            raise ValueError(
                "The provided image is neither a path nor a np.ndarray. " +
                "Provided with type: {}".format(type(image)))
        self.loading_input_timings.append(load_ns * 1e-6)

        start = clock_now()
        self.ctx.run_model()
        infer_ns = clock_now() - start
        self.inference_timings.append(infer_ns * 1e-6)

        start = clock_now()
        outputs = self.ctx.output(index=0).array()[0]
        mask = np.argmax(outputs, axis=-1).astype(np.uint8)
        boxes_ns = clock_now() - start
        self.box_timings.append(boxes_ns * 1e-6)
        return mask

    def get_input_type(self):
        """
        Returns the model input type.

        Returns
        -------
            type: str
                The model input type.

        Raises
        ------
            NotImplementedError
                raise because it has not been implemented yet.
        """
        raise NotImplementedError("has not been implemented.")

    def get_input_shape(self):
        """
        Grabs the model input shape.
        
        Returns
        -------
            type: tuple or list
                The model input shape.
        """
        return self.ctx.tensor('serving_default_input_1:0').shape
    
    def get_output_type(self):
        """
        Returns the model output type.

        Returns
        -------
            type: str
                The model output type.

        Raises
        ------
            NotImplementedError
                raise because it has not been implemented yet.
        """
        raise NotImplementedError("has not been implemented.")

    def get_output_shape(self) -> Union[tuple, None]:
        """
        Returns the model output type.
       
        Returns
        -------
            type: str
                The model output type

        Raises
        ------
            NotImplementedError
                raise because it has not been implemented yet.
        """
        raise NotImplementedError("has not been implemented.")