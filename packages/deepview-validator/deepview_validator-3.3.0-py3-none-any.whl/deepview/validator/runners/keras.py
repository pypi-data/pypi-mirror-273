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
import os

class DetectionKerasRunner(Runner):
    """
    Runs the Keras (h5) models using the TensorFlow library.
    
    Parameters
    ----------
        model: str or tf.keras.Model
            The path to the model or the loaded keras model.

        parameters: Parameters
            These are the model parameters set from the command line.

        labels: list
            Unique string labels.

    Raises
    ------
        NonMatchingIndexException
            Raised if the model outputs an index
            that is out of bounds to the labels list passed or the labels
            contained within the model itself.

        MissingLibraryException
            Raised if the TensorFlow library is not installed.
    """
    def __init__(
        self,
        model,
        parameters: Parameters,
        labels: list=None
    ):
        super(DetectionKerasRunner, self).__init__(model, parameters, labels)

        try:
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
            import tensorflow as tf
        except ImportError:
            raise MissingLibraryException(
                "tensorflow>=2.8.0,<2.16.0 is needed to load the model.")
        
        if isinstance(model, str):
            model = self.validate_model_path(model)
            if os.path.exists(os.path.join(model, "saved_model.pb")):
                self.loaded_model = tf.saved_model.load(model)
                self.inputs = self.loaded_model.signatures["serving_default"].inputs
                self.outputs = self.loaded_model.signatures["serving_default"].outputs
            else:
                self.loaded_model = tf.keras.models.load_model(model, compile=False)
        else:
            self.loaded_model = model
            self.model = "Training Model"
        
        self.update_nms()
        self.update_engine()

        if self.parameters.warmup > 0:
            logger("Loading model and warmup...", code="INFO")
            # Produce a sample image of zeros.
            input_type = self.get_input_type()
            height, width = self.get_input_shape()[1:3]
            image = np.expand_dims(np.zeros((height, width, 3)), 0).astype(np.dtype(input_type))

            if isinstance(self.loaded_model, tf.keras.Model):
                t = timeit(lambda: self.loaded_model.predict(image, verbose=0), number=self.parameters.warmup)
            else:
                t = timeit(lambda: self.loaded_model(image), number=self.parameters.warmup)
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
        and the model outputs. Typical shapes seen include.

        ```
        (None, None, 4)
        (None, 6000, 3)
        ```

        Common patterns are for a coco128 YoloV5 model.

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
        Runs the model to produce bounding box predictions on a 
        single image and records the timing information of the model.

        Parameters
        ----------
            image: str or np.ndarray
                This can either be the path to an image or a numpy array
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
        """
        """Input Preprocessing"""
        start = clock_now()
        # Take only the (height, width).
        image = resize(image, self.get_input_shape()[1:3])
        tensor = self.apply_normalization(
            image, self.parameters.normalization, self.get_input_type())
        # Convert shapes (1,64,64) to (1,64,64,3)
        if len(tensor.shape) < 4:
            tensor = np.expand_dims(tensor, axis=3)
            tensor = np.repeat(tensor, repeats=3, axis=3)
        load_ns = clock_now() - start
        self.loading_input_timings.append(load_ns * 1e-6)

        """Inference"""
        try: # This is for a Keras saved model or H5 file.
            start = clock_now()
            outputs = self.loaded_model.predict(tensor, verbose=0)
            infer_ns = clock_now() - start
            self.inference_timings.append(infer_ns * 1e-6)
        except AttributeError: # This is for a Tensorflow saved model.
            start = clock_now()
            outputs = self.loaded_model(tensor)
            infer_ns = clock_now() - start
            self.inference_timings.append(infer_ns * 1e-6)

        """Postprocessing"""
        start = clock_now()
        boxes, classes, scores = self.postprocessing(outputs)
        boxes_ns = clock_now() - start
        self.box_timings.append(boxes_ns * 1e-6)
        return boxes, classes, scores

    def postprocessing(
            self, 
            outputs: tuple
        ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Extracts the boxes, labels, and scores using TensorFlow NMS.

        Parameters
        ----------
            outputs: tuple
                Internally converted models have lengths of 2 where
                boxes = outputs[-2] and scores = outputs[-1].

                YoloV5 converted models have lengths of 1 where the element
                has the shape (1, 25200, 85) for coco models.

                YoloV7 currently supports ONNX and TensorRT conversion.

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
            MissingLibraryException
                Raised if the TensorFlow library is not installed.

            NonMatchingIndexException
                Raised if the model label index is
                out of bounds to the input labels list.
        """
        try:
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
            import tensorflow as tf
        except ImportError:
            raise MissingLibraryException(
                "tensorflow>=2.8.0,<2.16.0 is needed to perform NMS operations.")
    
        if len(outputs) < 2:
            if tf.is_tensor(outputs[0]): # YoloV5 keras converted model.
                nmsed_boxes, nmsed_classes, nmsed_scores = self.process_yolo_standard(outputs)
            else: # YoloV5 keras converted model with NMS.
                nmsed_boxes, nmsed_classes, nmsed_scores = self.process_yolo_nms(outputs[0])
        else: 
            # The outputs here is either a list or a tuple. Either of length 2 or 4.
            # The elements are either numpy array or tf.Tensor.
            # The difference is relied upon the shape at the last 2 element.
            # For YoloV5 models, the shape is [1, 100] or similar for classes.
            # Internally, the shape is [1, 6000, 1, 4], (1, 1935, 1, 4), or similar for boxes.
            if len(outputs[-2].shape) == 4: # Internal converted model.
                nmsed_boxes, nmsed_classes, nmsed_scores = self.process_internal(outputs)    
            else: # YoloV5 tensorflow converted model with NMS.
                nmsed_boxes, nmsed_classes, nmsed_scores = self.process_yolo_nms(outputs)

        if self.parameters.class_filter:
            nmsed_boxes, nmsed_classes, nmsed_scores = self.class_filter(
                nmsed_boxes, nmsed_classes, nmsed_scores
            )
        nmsed_classes = self.index2string(nmsed_classes)
        return nmsed_boxes, nmsed_classes, nmsed_scores
    
    def process_internal(self, outputs: tuple) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        This methods process model outputs that were trained internally.

        Parameters
        ----------
            outputs: tuple
                This has a length of either 2 or 4 which contains 
                boxes = outputs[-2] and scores = outputs[-1] at the last indices.

        Returns
        -------
            nmsed_boxes: np.ndarray
                Model bounding boxes after NMS.
            
            nmsed_classes: np.ndarray
                Model classes after NMS.
            
            nmsed_scores: np.ndarray
                Model scores after NMS.
        """
        boxes = outputs[-2]
        # Negative offsets could mean that the model contains the background class,
        # but the dataset does not.
        if self.parameters.label_offset < 0:
            scores = outputs[-1][..., abs(self.parameters.label_offset):]
        # Positive offsets could mean that the dataset contains the background class,
        # but the dataset does not.
        # TODO: Consider cases where the offset might be positive.
        else:
            scores = outputs[-1]

        return self.tensorflow_nms(boxes, scores)
    
    def process_yolo_standard(self, outputs: tuple) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        This method processes the outputs of the model that was converted in 
        YoloV5.

        Parameters
        ----------
            outputs: tuple
                This has a length of 1 which contains a torch.Tensor of shape
                (batch_size, number of boxes, number of classes).

        Returns
        -------
            nmsed_boxes: np.ndarray
                Model bounding boxes after NMS.
            
            nmsed_classes: np.ndarray
                Model classes after NMS.
            
            nmsed_scores: np.ndarray
                Model scores after NMS.
        """
        h, w = self.get_input_shape()[1:3]
        outputs = [x if isinstance(x, np.ndarray) else x.numpy() for x in outputs]
        # NMS requires non-normalized coordinates.
        outputs[0][..., :4] *= [w, h, w, h]  # xywh normalized to pixels.
        
        if isinstance(outputs, (list, tuple)):
            output = self.from_numpy(outputs[0]) if len(outputs) == 1 else [
                self.from_numpy(x) for x in outputs]
        else:
            output = self.from_numpy(outputs)

        # Currently it is a tuple with length of 1 (YoloV5) or 2 (Internal)
        #output = self.from_numpy(outputs[0])
        output = self.torch_nms(output)

        outputs = output[0].numpy()
        outputs[..., :4] /= [w, h, w, h]
        nmsed_boxes = outputs[..., :4]
        # Single dimensional arrays gets converted to the element. 
        # Specify the axis into 1 to prevent that.
        nmsed_scores = np.squeeze(outputs[..., 4:5], axis=1)
        nmsed_classes = np.squeeze(outputs[...,5:6], axis=1)

        if self.parameters.label_offset != 0:
            nmsed_classes += self.parameters.label_offset
        return nmsed_boxes, nmsed_classes, nmsed_scores
    
    def process_yolo_nms(self, outputs: list) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        This method processes the outputs of the model that was converted in
        YoloV5 which embeds the NMS.

        Parameters
        ----------
            outputs: list or CombinedNonMaxSuppression
                This can be unpacked into boxes, scores, classes, and valid boxes.
                The output of tf.image.combined_non_max_suppression method.

        Returns
        -------
            nms_predicted_boxes: np.ndarray
                This contains only the valid bounding boxes.
            
            nms_predicted_classes: np.ndarray
                This contains only the valid bounding boxes.
            
            nms_predicted_scores: np.ndarray
                This contains only the valid bounding boxes.
        """
        try:
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
            import tensorflow as tf
        except ImportError:
            raise MissingLibraryException(
                "tensorflow>=2.8.0,<2.16.0 is needed for Keras models.")
        
        nmsed_boxes, nmsed_scores, nmsed_classes, valid_boxes = outputs
                
        nmsed_classes = tf.cast(nmsed_classes, tf.int32)
        return self.tensorflow_nms_filter(
            nmsed_boxes, nmsed_scores, nmsed_classes, valid_boxes
        )

    def get_input_type(self) -> str:
        """
        Returns the model input type.
        
        Returns
        -------
            type: str
                The model input type.
        """
        try:
            return self.loaded_model.input.dtype.as_numpy_dtype
        except AttributeError:
            return self.inputs[0].dtype.as_numpy_dtype
        
    def get_input_shape(self):
        """
        Grabs the model input shape.

        Returns
        -------
            type: tuple or list
                The model input shape.
        """
        try:
            return self.loaded_model.input.shape
        except AttributeError:
            return self.inputs[0].shape
        
    def get_output_type(self):
        """
        Returns the model output type of the first output.

        Returns
        -------
            type: tf.float32
                The model output type.
        """
        try:
            return self.loaded_model.output[-1].dtype.as_numpy_dtype
        except AttributeError:
            return self.outputs[-1].dtype.as_numpy_dtype
    
    def get_output_shape(self):
        """
        Grabs the model output shape of the first output.

        Returns
        -------
            type: tuple or list
                The model output shape.
        """
        try:
            return self.loaded_model.output[-1].shape
        except AttributeError:
            return self.outputs[-1].shape


class SegmentationKerasRunner(Runner):
    """
    Runs Keras models to produce segmentation masks.
  
    Parameters
    -----------
        model: str, tf.keras.Model
            The path to the Keras model or the loaded keras model object.

        parameters: Parameters
            This object contains the model parameters configured from the
            command line.

    Raises
    ------
        MissingLibraryException:
            Raised if the the TensorFlow library
            which is used to load and run a keras model is not installed.
    """
    def __init__(
            self, 
            model,
            parameters: Parameters
        ):
        super(SegmentationKerasRunner, self).__init__(model, parameters)

        try:
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
            import tensorflow as tf
        except ImportError:
            raise MissingLibraryException(
                "tensorflow>=2.8.0,<2.16.0 is needed to load Keras models.")
        
        if isinstance(model, str):
            model = self.validate_model_path(model)
            if os.path.exists(os.path.join(model, "saved_model.pb")):
                self.loaded_model = tf.saved_model.load(model)
                self.inputs = self.loaded_model.signatures["serving_default"].inputs
                self.outputs = self.loaded_model.signatures["serving_default"].outputs
            else:
                self.loaded_model = tf.keras.models.load_model(model, compile=False)
        else:
            self.loaded_model = model
            self.model = "Training Model"

        self.parameters = parameters

        if len(tf.config.list_physical_devices('GPU')):
            self.parameters.engine = "gpu"
        elif len(tf.config.list_physical_devices('CPU')):
            self.parameters.engine = "cpu"
        else:
            self.parameters.engine = "unknown"

    def run_single_instance(self, image: Tuple[str, np.ndarray]):
        """
        Runs the loaded Keras model on a single image 
        to produce a mask for the image.

        Parameters
        ----------
            image: str or np.ndarray
                This can either be the path to an image or a numpy array
                image.

        Returns
        -------
            mask: np.ndarray
                This is the segmentation mask of the image 
                where each pixel is represented by a class in
                the image.

        Raises
        ------
            MissingLibraryException
                Raised if the TensorFlow library 
                is not installed which is needed
                to run a Keras model.
        """
        try:
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
            import tensorflow as tf
        except ImportError:
            raise MissingLibraryException(
                "tensorflow>=2.8.0,<2.16.0 is needed to load Keras models.")

        start = clock_now()
        image = resize(image, self.get_input_shape()[1:3])
        tensor = self.apply_normalization(
            image, self.parameters.normalization, self.get_input_type())
        load_ns = clock_now() - start
        self.loading_input_timings.append(load_ns * 1e-6)
    
        start = clock_now()
        try: # This is for a Keras saved model or H5 file.
            outputs = self.loaded_model.predict(tensor, verbose=0)
        except AttributeError: # This is for a Tensorflow saved model.
            outputs = self.loaded_model(tensor)
        infer_ns = clock_now() - start
        self.inference_timings.append(infer_ns * 1e-6)

        start = clock_now()
        mask = tf.argmax(outputs, axis=-1)[0].numpy().astype(np.uint8)
        boxes_ns = clock_now() - start
        self.box_timings.append(boxes_ns * 1e-6)
        return mask

    def get_input_type(self) -> str:
        """
        Returns the model input type.
        
        Returns
        -------
            type: str
                The model input type.
        """
        try:
            return self.loaded_model.input.dtype.as_numpy_dtype
        except AttributeError:
            return self.inputs[0].dtype.as_numpy_dtype

    def get_input_shape(self):
        """
        Returns the input shape of the Keras model.
        
        Returns
        -------
            input shape: tuple or list
                This is the model input shape.
        """
        try:
            return self.loaded_model.input.shape
        except AttributeError:
            return self.inputs[0].shape
        
    def get_output_type(self):
        """
        Returns the model output type of the first output.

        Returns
        -------
            type: tf.float32
                The model output type.
        """
        try:
            return self.loaded_model.output[-1].dtype.as_numpy_dtype
        except AttributeError:
            return self.outputs[-1].dtype.as_numpy_dtype
    
    def get_output_shape(self):
        """
        Grabs the model output shape of the first output.

        Returns
        -------
            type: tuple or list
                The model output shape.
        """
        try:
            return self.loaded_model.output[-1].shape
        except AttributeError:
            return self.outputs[-1].shape
        

class PoseKerasRunner(Runner):
    """
    Runs Keras pose models.

    Parameters
    ----------
        model: str
            The path to the Keras model or the loaded keras model object.

        parameters: Parameters
            This object contains the model parameters configured from the
            command line.

    Raises
    -------
        MissingLibraryException
            Raised if the TensorFlow library is not installed.
    """
    def __init__(
            self, 
            model, 
            parameters: Parameters
        ):
        super(PoseKerasRunner, self).__init__(model, parameters)

        try:
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
            import tensorflow as tf
        except ImportError:
            raise MissingLibraryException(
                "tensorflow>=2.8.0,<2.16.0 is needed to load the model.")
        
        if isinstance(model, str):
            model = self.validate_model_path(model)
            if os.path.exists(os.path.join(model, "saved_model.pb")):
                self.loaded_model = tf.saved_model.load(model)
                self.inputs = self.loaded_model.signatures["serving_default"].inputs
                self.outputs = self.loaded_model.signatures["serving_default"].outputs
            else:
                self.loaded_model = tf.keras.models.load_model(model, compile=False)
        else:
            self.loaded_model = model
            self.model = "Training Model"

        self.parameters = parameters
        
        if len(tf.config.list_physical_devices('GPU')):
            self.parameters.engine = "gpu"
        elif len(tf.config.list_physical_devices('CPU')):
            self.parameters.engine = "cpu"
        else:
            self.parameters.engine = "unknown"

    def run_single_instance(self, image: Tuple[str, np.ndarray]):
        """
        Runs the model to produce angle predictions on a single image and 
        records the timing information of the model.

        Parameters
        ----------
            image: str or np.ndarray
                This can either be the path to an image or a numpy array
                image.

        Returns
        -------
            angles: list
                The Euler angles roll, pitch, yaw.

            None
                Place for supposed labels. TODO Replace None with actual labels.
        """
        start = clock_now()
        image = resize(image, self.get_input_shape()[1:3])
        tensor = self.apply_normalization(
            image, self.parameters.normalization, self.get_input_type())
        load_ns = clock_now() - start
        self.loading_input_timings.append(load_ns * 1e-6)

        start = clock_now()
        outputs = self.loaded_model.predict(tensor, verbose=0)
        infer_ns = clock_now() - start
        self.inference_timings.append(infer_ns * 1e-6)

        start = clock_now()
        boxes_ns = clock_now() - start
        self.box_timings.append(boxes_ns * 1e-6)
        return outputs[0], None

    def get_input_type(self) -> str:
        """
        Returns the model input type.
        
        Returns
        -------
            type: str
                The model input type.
        """
        try:
            return self.loaded_model.input.dtype.as_numpy_dtype
        except AttributeError:
            return self.inputs[0].dtype.as_numpy_dtype

    def get_input_shape(self):
        """
        Returns the model input shape.
       
        Returns
        -------
            type: tuple or list
                The model input shape.
        """
        try:
            return self.loaded_model.input.shape
        except AttributeError:
            return self.inputs[0].shape
        
    def get_output_type(self):
        """
        Returns the model output type of the first output.

        Returns
        -------
            type: tf.float32
                The model output type.
        """
        try:
            return self.loaded_model.output[-1].dtype.as_numpy_dtype
        except AttributeError:
            return self.outputs[-1].dtype.as_numpy_dtype
    
    def get_output_shape(self):
        """
        Grabs the model output shape of the first output.

        Returns
        -------
            type: tuple or list
                The model output shape.
        """
        try:
            return self.loaded_model.output[-1].shape
        except AttributeError:
            return self.outputs[-1].shape