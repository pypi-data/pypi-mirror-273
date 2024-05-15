# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.exceptions import UnsupportedNormalizationException
from deepview.validator.exceptions import UnsupportedBoxFormatException
from deepview.validator.exceptions import UnsupportedEngineException
from deepview.validator.exceptions import UnsupportedNMSException
from deepview.validator.metrics.detectionutils import clamp
from typing import Union
import os

class Parameters:
    """
    Default initialization parameters provided are based on the model
    parameters. Other parameters included are for validation specifications.

    Parameters
    ----------
        validation_iou: float
            This is the threshold for the validation IoU which specifies which
            of the matched detections should be regarded as localization
            false positives should they have an IoU below this threshold.

        detection_iou: float
            This is for NMS purposes when running the model.

        validation_score: float
            This is the threshold for the validation score which specifies 
            which detections should not be regarded during validation should
            they have scores below this threshold.

        detection_score: float
            This is for NMS purposes when running the model.

        engine: str
            This is the type of processor to use to run the model. Options 
            include "cpu", "npu", "gpu".

        nms: str
            This is the type of NMS to use when running the model. Options
            include "standard", "fast", "matrix", "tensorflow".

        normalization: str
            This is the type of image normalization to perform. Options 
            include "raw", "signed", "unsigned", "imagenet", "whitening".

        box_format: str
            This is the box format to set to output from the model. Options
            include "xyxy", "xywh", "yxyx".

        warmup: int
            This is the number of warmup iterations to perform prior to 
            running the model for validation. 

        label_offset: int
            This is the offset to map the integer labels to string labels.

        max_detections: int
            The maximum number of detections to output per image. 
    """

    def __init__(
        self,
        validation_iou: float = 0.50,
        detection_iou: float = 0.50,
        validation_score: float = 0.00,
        detection_score: float = 0.50,
        engine: str = "npu",
        nms: str = "fast",
        normalization: str = "raw",
        box_format: str = "xyxy",
        warmup: int = 0,
        label_offset: int = 0,
        max_detections: int = 100,
    ) -> None:
        self._validation_iou = clamp(validation_iou)
        self._detection_iou = clamp(detection_iou)
        self._validation_score = clamp(validation_score)
        self._detection_score = clamp(detection_score)
        self._engine = engine
        self._nms = nms
        self._normalization = normalization
        self._box_format = box_format
        self._warmup = warmup
        self._label_offset = label_offset
        self._max_detections = max_detections
        self._metric = "iou"
        self._clamp_boxes = None
        self._ignore_boxes = None
        self._display = -1
        self._plots = True
        self._validate_3d = False
        self._include_background = False
        self._visualize = None
        self._tensorboard = None
        self._json_out = None
        self._rematching = True
        self._iou_first = True
        self._silent = False
        self._leniency_factor=2
        self._letterbox = False
        self._auto_offset = True
        self._class_filter = False

    @property
    def validation_iou(self) -> float:
        """
        Attribute to access the validation iou. 
        This metric is used to classify if matched predictions will
        be considered as localization FPs if IoUs are below this threshold.
        Can only be set to :py:class:float.

        Returns
        -------
            :py:class:float: The validation iou.
        """
        return self._validation_iou

    @validation_iou.setter
    def validation_iou(self, iou: float):
        """
        Sets the validation IoU.

        Parameters
        ----------
            iou: float
                The validation IoU to set.
        """
        self._validation_iou = clamp(iou)

    @property
    def detection_iou(self) -> float:
        """
        Attribute to access the detection iou. 
        This metric is used for the NMS detection. 
        Can only be set to :py:class:float.

        Returns
        -------
            :py:class:float: The detection iou.
        """
        return self._detection_iou

    @detection_iou.setter
    def detection_iou(self, iou: float):
        """
        Sets the detection IoU.

        Parameters
        ----------
            iou: float
                The detection IoU to set.
        """
        self._detection_iou = clamp(iou)

    @property
    def validation_score(self) -> float:
        """
        Attribute to access the validation score threshold. 
        This metric is used which prediction to validate if scores
        are higher than this threshold. 
        Can only be set to :py:class:float.

        Returns
        -------
            :py:class:float: The validation score.
        """
        return self._validation_score

    @validation_score.setter
    def validation_score(self, score: float):
        """
        Sets the validation score.

        Parameters
        ----------
            score: float
                The validation score to set.
        """
        self._validation_score = clamp(score)

    @property
    def detection_score(self) -> float:
        """
        Attribute to access the detection score threshold. 
        This metric is used for the NMS detection. 
        Can only be set to :py:class:float.

        Returns
        -------
            :py:class:float: The detection score.
        """
        return self._detection_score

    @detection_score.setter
    def detection_score(self, score: float):
        """
        Sets the detection score.

        Parameters
        ----------
            score: float
                The detection score to set.
        """
        self._detection_score = clamp(score)

    @property
    def engine(self) -> str:
        """
        Attribute to access the type of engine to run. 
        This is the processor used to run the model: "npu", "gpu", "cpu".
        Can only be set to :py:class:str.

        Returns
        -------
            :py:class:str: The engine type.
        """
        return self._engine

    @engine.setter
    def engine(self, this_engine: Union[str, None]):
        """
        Sets the engine type.

        Parameters
        ----------
            this_engine: str
                The engine to set.

        Raises
        ------
            UnsupportedEngineException
                Raised if the passed engine is not recognized.
        """
        if this_engine is not None:
            this_engine = this_engine.lower()
            if this_engine not in ['npu', 'cpu', 'gpu', 'cuda', 'deepviewrt', 'hailo']:
                raise UnsupportedEngineException(this_engine)
        self._engine = this_engine

    @property
    def nms(self) -> str:
        """
        Attribute to access the NMS type. 
        This metric is used for the NMS detection. 
        Can only be set to :py:class:str.

        Returns
        -------
            :py:class:str: The NMS type.
        """
        return self._nms

    @nms.setter
    def nms(self, this_nms: Union[str, None]):
        """
        Sets the NMS type.

        Parameters
        ----------
            this_nms: str
                The NMS to set.

        Raises
        ------
            UnsupportedNMSException
                Raised if the NMS provided is not recognized.
        """
        if this_nms is not None:
            this_nms = this_nms.lower()
            if this_nms not in ['standard', 'fast', 'matrix', 'tensorflow', 'torch']:
                raise UnsupportedNMSException(this_nms)
        self._nms = this_nms

    @property
    def normalization(self) -> str:
        """
        Attribute to access the image normalization type. 
        Usually: Quantized models use "raw" and floating point models
        use "unsigned" or "signed".
        Can only be set to :py:class:str.

        Returns
        -------
            :py:class:str: The normalization type.
        """
        return self._normalization

    @normalization.setter
    def normalization(self, norm: Union[str, None]):
        """
        Sets the normalization type.

        Parameters
        ----------
            norm: str
                The normalization to set.

        Raises
        ------
            UnsupportedNormalizationException
                Raised if the passed image normalization is not recognized.
        """
        if norm is not None:
            norm = norm.lower()
            if norm not in ["raw", "signed", "unsigned", "whitening", "imagenet"]:
                raise UnsupportedNormalizationException(norm)
        self._normalization = norm

    @property
    def box_format(self) -> str:
        """
        Attribute to access the box format. 
        The box format can either be: "xyxy", "xywh", "yxyx"
        Can only be set to :py:class:'str'

        Returns
        -------
            :py:class:str: The box format type.
        """
        return self._box_format

    @box_format.setter
    def box_format(self, this_box_format: Union[str, None]):
        """
        Sets the box format type.

        Parameters
        ----------
            this_box_format: str
                The box format to set.

        Raises
        ------
            UnsupportedBoxFormatException
                Raised if the box format provided is not supported.
        """
        if this_box_format is not None:
            this_box_format = this_box_format.lower()
            if this_box_format not in ["xyxy", "xywh", "yxyx"]:
                raise UnsupportedBoxFormatException(this_box_format)
        self._box_format = this_box_format

    @property
    def warmup(self) -> int:
        """
        Attribute to access the model warmup iterations. 
        Can only be set to :py:class:int

        Returns
        -------
            :py:class:int: The number of warmup iterations to perform.
        """
        return self._warmup

    @warmup.setter
    def warmup(self, this_warmup: int):
        """
        Sets the number of model warmup iterations to perform.

        Parameters
        ----------
            this_warmup: int
                The warmup to set.
        """
        self._warmup = this_warmup

    @property
    def label_offset(self) -> int:
        """
        Attribute to access the label offset for the predictions. 
        This is used for mapping the prediction integer labels to strings. 
        Can only be set to :py:class:int

        Returns
        -------
            :py:class:int: The offset to perform.
        """
        return self._label_offset

    @label_offset.setter
    def label_offset(self, this_label_offset: int):
        """
        Sets the label offset for the predictions.

        Parameters
        ----------
            this_label_offset: int
                The label_offset to set.
        """
        self._label_offset = this_label_offset

    @property
    def max_detections(self) -> int:
        """
        Attribute to access the max detections for the predictions. 
        This is used to set the maximum detections per image. 
        Can only be set to :py:class:int.

        Returns
        -------
            :py:class:int: The maximum detections.
        """
        return self._max_detections

    @max_detections.setter
    def max_detections(self, this_max_detections: int):
        """
        Sets the maximum detections for the predictions.

        Parameters
        ----------
            this_max_detections: int
                The max_detections to set.
        """
        self._max_detections = this_max_detections

    @property
    def metric(self) -> str:
        """
        Attribute to access the metric type. 
        This parameter is used to define which metric ("iou", "centerpoint") 
        to use to match the predictions to ground truth.
        Can only be set to :py:class:str.

        Returns
        -------
            :py:class:str: The metric type.
        """
        return self._metric

    @metric.setter
    def metric(self, this_metric: str):
        """
        Sets the metric type.

        Parameters
        ----------
            this_metric: str
                The metric to set.
        """
        self._metric = this_metric

    @property
    def clamp_boxes(self) -> int:
        """
        Attribute to access clamp boxes. 
        This is used to specify the lowest limit for the 
        box dimensions in pixels. Any box dimensions (height or width) 
        lower than this setting will be resized to this setting.
        Can only be set to :py:class:int.

        Returns
        -------
            :py:class:int: The pixel dimension to clamp.
        """
        return self._clamp_boxes

    @clamp_boxes.setter
    def clamp_boxes(self, this_clamp_boxes: int):
        """
        Sets the clamp boxes.

        Parameters
        ----------
            this_clamp_boxes: int
                The clamp_boxes to set.
        """
        self._clamp_boxes = this_clamp_boxes

    @property
    def ignore_boxes(self) -> int:
        """
        Attribute to access ignore boxes. 
        Any box dimension (width or height) lower than this limit
        will be ignored from validation. 
        Can only be set to :py:class:int.

        Returns
        -------
            :py:class:int: The pixel dimension to ignore.
        """
        return self._ignore_boxes

    @ignore_boxes.setter
    def ignore_boxes(self, this_ignore_boxes: int):
        """
        Sets the ignore boxes.

        Parameters
        ----------
            this_ignore_boxes: int
                The ignore_boxes to set.
        """
        self._ignore_boxes = this_ignore_boxes

    @property
    def display(self) -> int:
        """
        Attribute to access display. 
        Set the number of images to display showing results
        for validation. 
        Can only be set to :py:class:int.

        Returns
        -------
            :py:class:int: The number of images to display.
        """
        return self._display

    @display.setter
    def display(self, this_display: int):
        """
        Sets the number of images to display.

        Parameters
        ----------
            this_display: int
                The display to set.
        """
        self._display = this_display

    @property
    def plots(self) -> bool:
        """
        Attribute to access plots. 
        Specify whether to draw validation plots or not. 
        Validation plots include: Confusion Matrix, PR-curve, and 
        classification histogram.
        Can only be set to :py:class:bool.

        Returns
        -------
            :py:class:bool: Condition to include plots.
        """
        return self._plots

    @plots.setter
    def plots(self, this_plots: bool):
        """
        Specify to include validation plots.

        Parameters
        ----------
            this_plots: bool
                The plots to set.
        """
        self._plots = this_plots

    @property
    def validate_3d(self) -> bool:
        """
        Attribute to access validate_3d. 
        Specify whether to perform 3D bounding box validation.
        Can only be set to :py:class:bool.

        Returns
        -------
            :py:class:bool: Condition to perform 3D detection validation.
        """
        return self._validate_3d

    @validate_3d.setter
    def validate_3d(self, this_validate_3d: bool):
        """
        Specify to perform 3D detection validation.

        Parameters
        ----------
            this_validate_3d: bool
                The validate_3d to set.
        """
        self._validate_3d = this_validate_3d

    @property
    def include_background(self) -> bool:
        """
        Attribute to access include_background. 
        Specify whether to include background as part of 
        segmentation validation.
        Can only be set to :py:class:bool.

        Returns
        -------
            :py:class:bool: Condition to include background for segmentation
            validation.
        """
        return self._include_background

    @include_background.setter
    def include_background(self, this_include_background: bool):
        """
        Specify to include background class for segmentation validation.

        Parameters
        ----------
            this_include_background: bool
                The include_background to set.
        """
        self._include_background = this_include_background

    @property
    def visualize(self) -> str:
        """
        Attribute to access the visualize.
        This is the path to store the validation results which
        includes images.
        Can only be set to :py:class:str.

        Returns
        -------
            :py:class:str: The path to save validation results.
        """
        return self._visualize

    @visualize.setter
    def visualize(self, this_visualize: str):
        """
        Sets the path to save the validation results in disk.

        Parameters
        ----------
            this_visualize: str
                The visualize to set.
        """
        if not os.path.exists(this_visualize):
            os.makedirs(this_visualize)
        self._visualize = this_visualize

    @property
    def tensorboard(self) -> str:
        """
        Attribute to access the tensorboard.
        This is the path to store the validation results which includes
        tfevent files to be loaded using tensorboard.
        Can only be set to :py:class:str.

        Returns
        -------
            :py:class:str: The path to save validation results.
        """
        return self._tensorboard

    @tensorboard.setter
    def tensorboard(self, this_tensorboard: str):
        """
        Sets the path to save the validation results in disk.

        Parameters
        ----------
            this_tensorboard: str
                The tensorboard to set.
        """
        if not os.path.exists(this_tensorboard):
            os.makedirs(this_tensorboard)
        self._tensorboard = this_tensorboard

    @property
    def json_out(self) -> str:
        """
        Attribute to access the json_out.
        This is the path to save the json file containing 
        validation metrics and raw data to draw the plots.
        Can only be set to :py:class:str.

        Returns
        -------
            :py:class:str: The path to save json file.
        """
        return self._json_out

    @json_out.setter
    def json_out(self, this_json_out: str):
        """
        Sets the path to save the json file in disk.

        Parameters
        ----------
            this_json_out: str
                The path to the json file to set.

        Raises
        ------
            ValueError
                Raised if the parameter --json_out recieved an 
                extension that is not a json file.
        """
        if this_json_out:
            if os.path.splitext(this_json_out)[1].lower() == ".json":
                # Create directory that stores the file if it doesn't exist.
                if not os.path.exists(os.path.dirname(this_json_out)):
                    os.makedirs(os.path.dirname(this_json_out))
                self._json_out = this_json_out
            elif os.path.splitext(this_json_out)[1].lower() == "":
                if not os.path.exists(os.path.normpath(this_json_out)):
                    os.makedirs(os.path.normpath(this_json_out))
                self._json_out = os.path.join(this_json_out, "results.json")
            else:
                raise ValueError(
                    "--json_out parameter can only create " +
                    "json files, but received {}".format(this_json_out))

    @property
    def rematching(self) -> bool:
        """
        Attribute to access the recursive flag.
        This is a flag to determine whether bboxes are 
        rematched after being replaced due to another bbox 
        having a better IoU.

        Returns
        -------
            :py:class:bool: The condition whether to perform bbox rematching.
        """
        return self._rematching

    @rematching.setter
    def rematching(self, rematching: bool):
        """
        Sets a flag to determine whether bboxes are 
        rematched after being replaced due to another bbox 
        having a better IoU.

        Parameters
        ----------
            rematching: bool
                Set the rematching condition.
        """
        self._rematching = rematching

    @property
    def iou_first(self) -> bool:
        """
        Attribute to access the iou_first flag.
        This is a flag to determine whether iou are 
        matched first or classes are matched first during validation.

        Returns
        -------
            :py:class:bool: The condition to prioritize higher IoU matching
            over the same class matching.
        """
        return self._iou_first

    @iou_first.setter
    def iou_first(self, iou_first: bool):
        """
        Sets a flag to determine whether iou are matched first or classes are matched first during validation

        Parameters
        ----------
            iou_first: bool
                Condition to perform higher IoU matching prioritization
                over the same class matching.
        """
        self._iou_first = iou_first

    @property
    def silent(self) -> bool:
        """
        Attribute to access the display flag.
        This is a flag to determine whether messages 
        are printed to console. Does not print when silent is true.

        Returns
        -------
            py:class:bool: Condition to disable validation logging.
        """
        return self._silent

    @silent.setter
    def silent(self, silent: bool):
        """
        Sets a flag to determine whether messages are printed to console. 
        Does not print when silent is true

        Parameters
        ----------
            silent: bool
                This is the condition to disable validation logging.
        """
        self._silent = silent

    @property
    def leniency_factor(self) -> int:
        """
        Attribute to access the leniency factor for center distance calculations. 
        Can only be set to :py:class:int

        Returns
        -------
            :py:class:int: The leniency factor. This is a criteria to consider
            center distances if the number of times the diagonal 
            (center to corner) of the smallest bounding box fits within the 
            box to box center distance does not exceed the leniency factor.

        """
        return self._leniency_factor

    @leniency_factor.setter
    def leniency_factor(self, this_leniency_factor: int):
        """
        Sets the leniency factor. This is a criteria to consider
        center distances if the number of times the diagonal 
        (center to corner) of the smallest bounding box fits within the 
        box to box center distance does not exceed the leniency factor.

        Parameters
        ----------
            this_leniency_factor: int
                The leniency_factor to set.
        """
        self._leniency_factor = this_leniency_factor

    @property
    def letterbox(self) -> bool:
        """
        Attribute to access letterbox condition. 
        Specify whether to preprocess images using letterbox transformations
        rather than image resizing.
        Can only be set to :py:class:bool.

        Returns
        -------
            :py:class:bool: Condition to specify letterbox image preprocessing.
        """
        return self._letterbox

    @letterbox.setter
    def letterbox(self, this_letterbox: bool):
        """
        Specify whether to preprocess images using letterbox transformations
        rather than image resizing.

        Parameters
        ----------
            this_letterbox: bool
                Condition to specify letterbox image preprocessing.
        """
        self._letterbox = this_letterbox

    @property
    def auto_offset(self) -> bool:
        """
        Attribute to access auto offset condition. 
        Specify whether to enable auto offset of the model
        indices based on the model output shape and the ground truth labels.
        Can only be set to :py:class:bool.

        Returns
        -------
            :py:class:bool: Condition to specify the auto offset property.
        """
        return self._auto_offset

    @auto_offset.setter
    def auto_offset(self, this_auto_offset: bool):
        """
        Specify whether to enable auto offset of the model
        indices based on the model output shape and the ground truth labels.

        Parameters
        ----------
            this_auto_offset: bool
                Condition to specify auto offset property
        """
        self._auto_offset = this_auto_offset

    @property
    def class_filter(self) -> bool:
        """
        Attribute to access the class filter condition. 
        Specify to filter the classes from the model detections to allow
        only the classes present in the ground truth dataset.
        Requires that the model detections has more classes than the 
        ground truth dataset.
        Can only be set to :py:class:bool.

        Returns
        -------
            :py:class:bool: Condition to specify the class filter property.
        """
        return self._class_filter

    @class_filter.setter
    def class_filter(self, this_class_filter: bool):
        """
        Specify to filter the classes from the model detections to allow
        only the classes present in the ground truth dataset.
        Requires that the model detections has more classes than the 
        ground truth dataset.

        Parameters
        ----------
            this_class_filter: bool
                Condition to specify class_filter property
        """
        self._class_filter = this_class_filter