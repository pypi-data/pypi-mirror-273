# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from __future__ import annotations
from typing import TYPE_CHECKING, Tuple
if TYPE_CHECKING:
    from deepview.validator.evaluators import Parameters

from deepview.validator.exceptions import NonMatchingIndexException
from deepview.validator.exceptions import MissingLibraryException
from deepview.validator.metrics.detectionutils import batch_iou
from deepview.validator.datasets.core import Dataset
import numpy as np
import os

class Runner:
    """
    Abstract Class that provides a template for the other runner classes.

    Parameters
    ----------
        model: str
            This is the path to the model file, 
            directory of prediction text files (offline), or a loaded model.

        model: str 
            The path to the model.

        parameters: Parameters
            These are the model parameters set from the command line.

        labels: list
            Unique string labels.

    Raises
    ------
        FileNotFoundError
            Raised if the path to the model does not exist.
    """
    def __init__(self, model, parameters: Parameters=None, labels: list=None):
        
        self.model = model
        self.parameters = parameters
        
        if labels is None:
            self.labels = []
        else:
            self.labels = labels

        self.input_shape = None

        self.box_timings = list()
        self.inference_timings = list()
        self.loading_input_timings = list()

    @staticmethod
    def validate_model_path(source):
        """
        Validates the existance of the model path.
        
        Parameters
        ----------
            source: str
                This is the path to the model file.

        Returns
        -------
            source: str
                The validated path to the model.

        Raises
        ------
            FileNotFoundError
                Raised if the path to the model does not exist.
        """
        if not os.path.exists(source):
            raise FileNotFoundError(
                "Model file is expected to be at: {}".format(source))
        return source
    
    def update_engine(self):
        """
        Updates the engine using TensorFlow or PyTorch.
        """
        try:
            import torch
            cuda = torch.cuda.is_available() and self.parameters.engine != "cpu"
            if cuda:
                self.parameters.engine = "cuda"
                return
        except ImportError:
            pass

        try:
            import tensorflow as tf
            if len(tf.config.list_physical_devices('GPU')):
                self.parameters.engine = "gpu"
            elif len(tf.config.list_physical_devices('CPU')):
                self.parameters.engine = "cpu"
        except ImportError:
            pass

    def update_nms(self):
        """
        Updates the NMS used based on the model output shape.
        """
        output_shape = self.get_output_shape()
        # For COCO, yolo generates models with classes + 4 (boxes) + 1 (confidence).
        if (output_shape[0] is None or output_shape[-1] != 85) and len(output_shape) == 3:
            self.parameters.nms = "tensorflow"
        elif output_shape[0] == 1 and len(output_shape) == 3:
            self.parameters.nms = "torch"

    def load_model(self):
        """Abstract Method"""
        pass

    def run_single_instance(self, image):
        """Abstract Method"""
        pass

    def postprocessing(self, outputs):
        """Abstract Method"""
        pass

    def get_input_type(self):
        """Abstract Method"""
        pass

    def get_input_shape(self):
        """Abstract Method"""
        pass

    def get_output_type(self):
        """Abstract Method"""
        pass

    def get_output_shape(self):
        """Abstract Method"""
        pass

    @staticmethod
    def apply_normalization(
        image: np.ndarray, normalization: str, input_type: str="float32"):
        """
        Performs images normalizations (signed, unsigned, raw).

        Parameters
        ----------
            image: np.ndarray
                The image to perform normalization.

            normalization: str
                This is the type of normalization to perform [signed, unsigned, raw].

            input_type: str
                This is the numpy datatype to convert. Ex. "uint8"

        Returns
        -------
            image: np.ndarray
                Depending on the normalization, the image will be returned.
        """
        if normalization.lower() == 'signed':
            return np.expand_dims((image / 127.5) - 1.0, 0).astype(np.dtype(input_type))
        elif normalization.lower() == 'unsigned':
            return np.expand_dims(image / 255.0, 0).astype(np.dtype(input_type))
        else:
            return np.expand_dims(image, 0).astype(np.dtype(input_type))
        
    def from_numpy(self, x: np.ndarray):
        """
        Convert numpy array to torch tensor.

        Parameters
        ----------
            x: np.ndarray
                The numpy array to convert to pytorch tensor.

        Returns
        -------
            x: torch.Tensor
                This is the numpy array as a torch.Tensor type.
        """
        try:
            import torch
        except ImportError:
            raise MissingLibraryException(
                "torchvision~=0.15.2 is needed to convert from NumPy.")
        return torch.from_numpy(x).to("cpu") if isinstance(x, np.ndarray) else x

    def multiclass_nms(
            self, 
            boxes: np.ndarray, 
            scores: np.ndarray, 
            nms_thr: float, 
            score_thr: float, 
            class_agnostic: bool=True
        ) -> np.ndarray:
        """
        Multiclass NMS implemented in Numpy
        
        Parameters
        ----------
            boxes: np.ndarray
                Input boxes to the NMS (number of boxes, 4) in xyxy f
                non-normalized ormat.

            scores: np.ndarray
                Input scores to the NMS (number of boxes, number of classes).

            nms_thr: float
                This is the IoU threshold for the NMS.

            score_thr: float
                This contains the score threshold input for the NMS.

            class_agnostic: bool
                This is to determine which type of NMS to perform.

        Returns
        -------
            dets: np.ndarray
                Post-NMS detections (number of detections, 6) which contains
                (xyxy, score, class) a total of 6 columns.
        """
        if class_agnostic:
            nms_method = self.multiclass_nms_class_agnostic
        else:
            nms_method = self.multiclass_nms_class_aware
        return nms_method(boxes, scores, nms_thr, score_thr)
    
    def multiclass_nms_class_aware(
            self, 
            boxes: np.ndarray, 
            scores: np.ndarray, 
            nms_thr: float, 
            score_thr: float,
        ) -> np.ndarray:
        """
        Multiclass NMS implemented in Numpy. Class-aware version.
        Method taken from: https://github.com/Megvii-BaseDetection/YOLOX/blob/main/yolox/utils/demo_utils.py#L96

        Parameters
        ----------
            boxes: np.ndarray
                Input boxes to the NMS (number of boxes, 4) in xyxy f
                non-normalized ormat.

            scores: np.ndarray
                Input scores to the NMS (number of boxes, number of classes).

            nms_thr: float
                This is the IoU threshold for the NMS.

            score_thr: float
                This contains the score threshold input for the NMS.

        Returns
        -------
            dets: np.ndarray
                Post-NMS detections (number of detections, 6) which contains
                (xyxy, score, class) a total of 6 columns.
        """
        final_dets = []
        num_classes = scores.shape[1]
        for cls_ind in range(num_classes):
            cls_scores = scores[:, cls_ind]
            valid_score_mask = cls_scores > score_thr
            if valid_score_mask.sum() == 0:
                continue
            else:
                valid_scores = cls_scores[valid_score_mask]
                valid_boxes = boxes[valid_score_mask]
                keep = self.nms(valid_boxes, valid_scores, nms_thr)
                if len(keep) > 0:
                    cls_inds = np.ones((len(keep), 1)) * cls_ind
                    dets = np.concatenate(
                        [valid_boxes[keep], valid_scores[keep, None], cls_inds], 1
                    )
                    final_dets.append(dets)
        if len(final_dets) == 0:
            return None
        return np.concatenate(final_dets, 0)

    def multiclass_nms_class_agnostic(
            self, 
            boxes: np.ndarray, 
            scores: np.ndarray, 
            nms_thr: float, 
            score_thr: float,
        ) -> np.ndarray:
        """
        Multiclass NMS implemented in Numpy. Class-agnostic version.
        Method taken from https://github.com/Megvii-BaseDetection/YOLOX/blob/main/yolox/utils/demo_utils.py#L120.
        
        Parameters
        ----------
            boxes: np.ndarray
                Input boxes to the NMS (number of boxes, 4) in xyxy f
                non-normalized ormat.

            scores: np.ndarray
                Input scores to the NMS (number of boxes, number of classes).

            nms_thr: float
                This is the IoU threshold for the NMS.

            score_thr: float
                This contains the score threshold input for the NMS.

        Returns
        -------
            dets: np.ndarray
                Post-NMS detections (number of detections, 6) which contains
                (xyxy, score, class) a total of 6 columns.
        """
        cls_inds = scores.argmax(1)
        cls_scores = scores[np.arange(len(cls_inds)), cls_inds]

        valid_score_mask = cls_scores > score_thr
        if valid_score_mask.sum() == 0:
            return None
        valid_scores = cls_scores[valid_score_mask]
        valid_boxes = boxes[valid_score_mask]
        valid_cls_inds = cls_inds[valid_score_mask]
        keep = self.nms(valid_boxes, valid_scores, nms_thr)
        if keep:
            dets = np.concatenate(
                [valid_boxes[keep], valid_scores[keep, None], valid_cls_inds[keep, None]], 1
            )
        return dets

    @staticmethod
    def nms(boxes: np.ndarray, scores: np.ndarray, nms_thr: float) -> list:
        """
        Single class NMS implemented in Numpy.
        Method taken from: https://github.com/Megvii-BaseDetection/YOLOX/blob/main/yolox/utils/demo_utils.py#L57

        Parameters
        ----------
            boxes: np.ndarray
                Input boxes to the NMS (number of boxes, 4) in xyxy f
                non-normalized ormat.

            scores: np.ndarray
                Input scores to the NMS (number of boxes, number of classes).

            nms_thr: float
                This is the IoU threshold for the NMS.

        Returns
        -------
            keep: list
                This contains the indices of the boxes to keep.
        """
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]

        areas = (x2 - x1 + 1) * (y2 - y1 + 1)
        order = scores.argsort()[::-1]

        keep = []
        while order.size > 0:
            i = order[0]
            keep.append(i)
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])

            w = np.maximum(0.0, xx2 - xx1 + 1)
            h = np.maximum(0.0, yy2 - yy1 + 1)
            inter = w * h
            ovr = inter / (areas[i] + areas[order[1:]] - inter)

            inds = np.nonzero(ovr <= nms_thr)[0]
            order = order[inds + 1]
        return keep
    
    def torch_nms( # NOSONAR
            self, 
            prediction,
            agnostic: bool=False,
            multi_label: bool=True,
            nm: int=0,
            max_wh: int=7680,
            max_nms: int= 30000,
            redundant: bool=True,
            merge: bool=False
        ):
        """
        This is the YoloV5 NMS found here:: \
        https://github.com/ultralytics/yolov5/blob/master/utils/general.py#L955

        Reproducing the same parameters as YoloV5 requires:: \
        1) detection score threshold = 0.001
        2) detection iou threshold = 0.60
        3) max detections = 300

        Parameters
        ----------
            prediction: torch.Tensor
                Raw predictions from the model (inference_out, loss_out).
                This contains shape (batch size, number of boxes, number of classes).

            agnostic: bool

            multi_label: bool
                If validation has more than 1 labels.

            nm: int

            max_wh: int
                The maximum box width and height (pixels).

            max_nms: int
                The maximum number of boxes into torchvision.ops.nms().

            redundant: bool
                Require redundant detections.

            merge: bool
                Use merge NMS.

        Returns
        -------
            output: list
                Length 1 which is formatted in the following way which 
                has a shape of (1, number of boxes, 6).
                [[[xmin, ymin, xmax, ymax, confidence, label], [...], ...]]. 
        """
        try:
            import torchvision
            import torch
        except ImportError:
            raise MissingLibraryException(
                "torchvision~=0.15.2 is required to use torch NMS.")
        
        if self.parameters.max_detections is None:
            self.parameters.max_detections = 100

        # YOLOv5 model in validation model.
        if isinstance(prediction, (list, tuple)):  
            # Select only inference output.
            prediction = prediction[0] 

        bs = prediction.shape[0]  # Batch size.
        # Offset of -5 is explained in https://medium.com/@KrashKart/i-wish-i-knew-this-about-yolov5-2fbab3584906
        nc = prediction.shape[2] - nm - 5  # The number of classes.
        xc = prediction[..., 4] > self.parameters.detection_score # Candidates.

        multi_label &= nc > 1  # Multiple labels per box (adds 0.5ms/img).
        mi = 5 + nc  # Mask start index.
        output = [torch.zeros((0, 6 + nm), device="cpu")] * bs

        for xi, x in enumerate(prediction):  # Image index, image inference.
            x = x[xc[xi]]  # Confidence.
            if not x.shape[0]:
                continue
            
            # Compute conf
            x[:, 5:] *= x[:, 4:5]  # conf = obj_conf * cls_conf.
            
            # (center_x, center_y, width, height) to (x1, y1, x2, y2).
            box = Dataset.yolo2xyxy(x[:, :4])  
            mask = x[:, mi:]  # zero columns if no masks

            # Detections matrix nx6 (xyxy, conf, cls).
            if multi_label:
                i, j = (
                    x[:, 5:mi] > self.parameters.detection_score
                ).nonzero(as_tuple=False).T
                x = torch.cat(
                    (box[i], x[i, 5 + j, None], j[:, None].float(), mask[i]), 
                    1)
            else:  # Best class only.
                conf, j = x[:, 5:mi].max(1, keepdim=True)
                x = torch.cat(
                    (box, conf, j.float(), mask), 
                    1)[conf.view(-1) > self.parameters.detection_score]

            # Check shape.
            n = x.shape[0]  # Number of boxes.
            if not n:  # No boxes.
                continue
            # Sort by confidence and remove excess boxes.
            x = x[x[:, 4].argsort(descending=True)[:max_nms]]  

            # Batched NMS.
            c = x[:, 5:6] * (0 if agnostic else max_wh)  # The classes.
            # boxes (offset by class), scores.
            boxes, scores = x[:, :4] + c, x[:, 4]  
        
            # Torchvision NMS.
            i = torchvision.ops.nms(
                boxes, scores, self.parameters.detection_iou)  
            i = i[:self.parameters.max_detections]  # This limits detections.
            # Merge NMS (boxes merged using weighted mean).
            if merge and (1 < n < 3e3):  
                # Update boxes as boxes(i,4) = weights(i,n) * boxes(n,4).
                # IoU matrix.
                iou = batch_iou(boxes[i], boxes) > self.parameters.detection_iou
                weights = iou * scores[None]  # Box weights.
                # Merged boxes.
                x[i, :4] = torch.mm(
                    weights, x[:, :4]).float() / weights.sum(1, keepdim=True) 
                if redundant:
                    i = i[iou.sum(1) > 1]  # Require redundancy.
            output[xi] = x[i]
        return output
    
    def tensorflow_nms(
            self, 
            boxes: np.ndarray, 
            scores: np.ndarray, 
            clip_boxes: bool=False
        ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Performs NMS using Tensorflow.

        Parameters
        ----------
            boxes: np.ndarray
                The bounding boxes from the model inference.

            scores: np.ndarray
                The detection scores from the model inference.

            clip_boxes: False
                If set to True, the boxes will be clamped within [0, 1).

        Returns
        -------
            nms_predicted_boxes: np.ndarray
                The detection bounding boxes after NMS.

            nms_predicted_classes: np.ndarray
                The detection labels after NMS.

            nms_predicted_scores: np.ndarray
                The detection scores after NMS.
        """
        try:
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
            import tensorflow as tf
        except ImportError:
            raise MissingLibraryException(
                "tensorflow>=2.8.0,<2.16.0 is needed to perform NMS.")
        
        if self.parameters.max_detections is None:
            self.parameters.max_detections = 100
        
        nmsed_boxes, nmsed_scores, nmsed_classes, valid_boxes = \
            tf.image.combined_non_max_suppression(
                boxes,
                scores,
                self.parameters.max_detections,
                self.parameters.max_detections,
                iou_threshold=self.parameters.detection_iou,
                score_threshold=self.parameters.detection_score,
                clip_boxes=clip_boxes)
        nmsed_classes = tf.cast(nmsed_classes, tf.int32)

        return self.tensorflow_nms_filter(
            nmsed_boxes, nmsed_scores, nmsed_classes, valid_boxes)
    
    def tensorflow_nms_filter(
            self, nmsed_boxes, nmsed_scores, nmsed_classes, valid_boxes
        ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        This method performs NMS filter operations.
        
        Parameters
        ----------
            nmsed_boxes: torch.Tensor
                This is the output of TensorFlow NMS bounding boxes.

            nmsed_scores: torch.Tensor
                This is the output of TensorFlow NMS scores.

            nmsed_classes: torch.Tensor
                This is the output of TensorFlow NMS classes.

            valid_boxes: torch.Tensor
                This contains indices for valid detections.

        Returns
        -------
            nms_predicted_boxes: np.ndarray
                This contains only the valid bounding boxes.
            
            nms_predicted_classes: np.ndarray
                This contains only the valid bounding boxes.
            
            nms_predicted_scores: np.ndarray
                This contains only the valid bounding boxes.
        """
        nms_predicted_boxes = [nmsed_boxes.numpy()[i, :valid_boxes[i], :]
                               for i in range(nmsed_boxes.shape[0])][0]
        nms_predicted_classes = [nmsed_classes.numpy()[i, :valid_boxes[i]]
                                 for i in range(nmsed_classes.shape[0])][0]
        nms_predicted_scores = [nmsed_scores.numpy()[i, :valid_boxes[i]]
                                for i in range(nmsed_scores.shape[0])][0]
        return nms_predicted_boxes, nms_predicted_classes, nms_predicted_scores

    def index2string(self, classes: np.ndarray) -> np.ndarray:
        """
        This method converts the model label indices into their string
        representations.

        Parameters
        ----------
            classes: np.ndarray
                This contains the model label indices.

        Returns
        -------
            string_classes: np.ndarray
                This contains labels as strings. 
        """
        if len(self.labels) > 0:
            string_classes = list()
            for cls in classes:
                try:
                    string_classes.append(self.labels[int(cls)])
                except IndexError:
                    raise NonMatchingIndexException(cls)
            return np.array(string_classes)
        return classes
    
    def class_filter(
            self, 
            boxes: np.ndarray, 
            classes: np.ndarray, 
            scores: np.ndarray
        ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        For dataset to model label mismatches. Filter only the 
        bounding boxes and scores with classes that are in common between
        the ground truth and the detections.

        Parameters
        ----------
            boxes: np.ndarray
                These contains boxes in any format.

            classes: np.ndarray
                These contains an array of integer indices.

            scores: np.ndarray
                These contains an array of model confidence scores. 
        
        Returns
        -------
            boxes: np.ndarray
                These are the filtered boxes.

            classes: np.ndarray
                These are the filtered classes.

            scores: np.ndarray
                These are the filtered scores. 
        """
        if len(self.labels) > 0:
            labels = np.arange(0, len(self.labels), 1)
            # Take only the labels that are common to the ground truth labels.
            indices = np.nonzero(np.in1d(classes, labels))[0]
            boxes = boxes[indices]
            scores = scores[indices]
            classes = classes[indices]
            # The classes may not contain indices that are larger still. 
            # For example classes may contain [11, 9, 7]. The ground truth
            # contains [0, 1, 2]. The classes should be mapped as [2, 1, 0].
            if issubclass(classes.dtype.type, np.integer):
                sorted_indices = np.argsort(classes)
                classes = np.argsort(sorted_indices)  
        return boxes, classes, scores

    def summarize(self):
        """
        Returns a summary of all the timings: 
        (mean, avg, max) of (load, inference, box).

        Returns
        -------
            timings in ms: dict

            .. code-block:: python

                {
                 'min_inference_time': minimum time to produce bounding boxes,
                 'max_inference_time': maximum time to produce bounding boxes,
                 'min_input_time': minimum time to load an image,
                 'max_input_time': maximum time to load an image,
                 'min_decoding_time': minimum time to process model
                                    predictions,
                 'max_decoding_time': maximum time to process model
                                    predictions,
                 'avg_decoding': average time to process model predictions,
                 'avg_input': average time to load an image,
                 'avg_inference': average time to produce bounding boxes,
                }
        """
        try:
            return {
                'min_inference_time': np.min(self.inference_timings),
                'max_inference_time': np.max(self.inference_timings),
                'min_input_time': np.min(self.loading_input_timings),
                'max_input_time': np.max(self.loading_input_timings),
                'min_decoding_time': np.min(self.box_timings),
                'max_decoding_time': np.max(self.box_timings),
                'avg_decoding': np.mean(self.box_timings),
                'avg_input': np.mean(self.loading_input_timings),
                'avg_inference': np.mean(self.inference_timings),
            }
        except ValueError:
            return None