# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from __future__ import annotations
from typing import TYPE_CHECKING, Union, List, Tuple
if TYPE_CHECKING:
    from deepview.validator.metrics import DetectionLabelData

from deepview.validator.metrics.detectionutils import clamp
import numpy as np

class DetectionLabelData:
    """
    Acts a container that stores the total number of true positives, 
    false positives, false negatives per label.

    Parameters
    ----------
        label: str or int
            The unique string or integer index label to base the container.
    """
    def __init__(self, label: Union[str, int, np.integer]):
        # The label being represented in this class.
        self._label = label
        # Total number of ground truths of the label.
        self._ground_truths = 0
        # Contains (IoU, score) values for predictions
        # marked as true positives.
        self._tps = list()
        # Contains (IoU, score) values for predictions marked as 
        # classification false positives.
        self._class_fps = list()
        # Contains score values for predictions captured as 
        # localization false positives.
        self._local_fps = list()

        # The number of true positives that became localization false positives
        # due to the IoU less than the set threshold.
        self._tp2fp = 0

    @property
    def label(self) -> Union[str, int, np.integer]:
        """
        Attribute to access the label stored.
        Can only be set to :py:class:`str` or :py:class:`int`

        Returns
        -------
            :py:class:`str` or :py:class:`int`: The label stored.
        """
        return self._label

    @label.setter
    def label(self, this_label: Union[str, int, np.integer]):
        """
        Sets the label.

        Parameters
        ----------
            this_label: str or int
                The label being represented in this container.
        """
        self._label = this_label

    @property
    def ground_truths(self) -> int:
        """
        Attribute to access the number of ground truths.
        Can only be set to :py:class:`int`

        Returns
        -------
            :py:class:`int`: The number of ground truths for this label.
        """
        return self._ground_truths

    @ground_truths.setter
    def ground_truths(self, gts: int):
        """
        Sets the number of ground truths for this label.

        Parameters
        ----------
            gts: int
                This is the number of ground truths for this label.
        """
        self._ground_truths = gts

    def add_ground_truths(self, gts: int = 1):
        """
        Adds the number of existing ground truths.

        Parameters
        ----------
            gts: int
                The number of ground truths to add.
        """
        self._ground_truths += gts

    @property
    def tps(self) -> List[Tuple[float, float]]:
        """
        Attribute to access the true positives data.
        Can only be set to :py:class:`list`

        Returns
        -------
            :py:class:`list`
                This contains the (IoU, score) of each 
                true positive for this label.
        """
        return self._tps

    @tps.setter
    def tps(self, this_tps: List[Tuple[float, float]]):
        """
        Sets the true positives data to a new value.

        Parameters
        ----------
            this_tps: :py:class:`list`
                These are true positives data to set.
        """
        self._tps = this_tps

    def add_tp(self, iou: float, score: float):
        """
        Adds the true positive prediction IoU and confidence score. 
        A true positive is when the prediction and the ground truth 
        label matches and the IoU is greater than the set IoU threshold.

        Parameters
        ----------
            iou: float
                The IoU of the true positive prediction.

            score: float
                The confidence score of the true positive prediction.
        """
        self._tps.append((clamp(iou), clamp(score)))

    def get_tp_scores(self) -> np.ndarray:
        """
        Grabs the prediction scores marked as true positives.

        Returns
        -------
            scores: np.ndarray
                The true positive scores.
        """
        if len(self.tps):
            return np.array(self.tps)[:, 1]
        return np.array([])

    def get_tp_iou(self) -> np.ndarray:
        """
        Grabs the prediction IoUs marked as true positives.

        Returns
        -------
            IoUs: np.ndarray
                The true positive IoU values.
        """
        if len(self.tps):
            return np.array(self.tps)[:, 0]
        return np.array([])

    def get_tp_count(self, iou_threshold: float, score_threshold: float) -> int:
        """
        Grabs the number of true positives at the 
        specified IoU threshold and score threshold.

        Parameters
        ----------
            iou_threshold: float
                The IoU threshold to consider the true positives.

            score_threshold: float
                The score threshold to consider the predictions.

        Returns
        -------
            count: int
                The number of true positives at the specified
                IoU and score threshold.
        """
        if len(self.tps):
            tp_iou = np.array(self.tps)[:, 0] >= iou_threshold
            tp_score = np.array(self.tps)[:, 1] >= score_threshold
            return np.count_nonzero(tp_iou * tp_score)
        return 0

    @property
    def class_fps(self) -> List[Tuple[float, float]]:
        """
        Attribute to access the classification false positives data.
        Can only be set to :py:class:`list`

        Returns
        -------
            :py:class:`list`
                This contains the (IoU, score) of each classification
                false positive for this label.
        """
        return self._class_fps

    @class_fps.setter
    def class_fps(self, this_class_fps: List[Tuple[float, float]]):
        """
        Sets the classification false positives data to a new value.

        Parameters
        ----------
            this_class_fps: :py:class:`list`
                These are classification false positives data to set.
        """
        self._class_fps = this_class_fps

    def add_class_fp(self, iou: float, score: float):
        """
        Adds the false positive (classification) prediction IoU 
        and confidence score. A false positive (classification) is when 
        the prediction and the ground truth labels don't match and the 
        IoU is greater than the set IoU threshold.

        Parameters
        ----------
            iou: float
                The IoU of the classification false positive prediction.

            score: float
                The confidence score of the classification false
                positive prediction.
        """
        self.class_fps.append((clamp(iou), clamp(score)))

    def get_class_fp_scores(self) -> np.ndarray:
        """
        Grabs the prediction scores marked as classification false positives.

        Returns
        -------
            scores: np.ndarray
                The classification false positive scores.
        """
        if len(self.class_fps):
            return np.array(self.class_fps)[:, 1]
        return np.array([])

    def get_class_fp_iou(self) -> np.ndarray:
        """
        Grabs the prediction IoUs marked as classification false positives.

        Returns
        -------
            IoUs: np.ndarray
                The classification false positive IoUs.
        """
        if len(self.class_fps):
            return np.array(self.class_fps)[:, 0]
        return np.array([])

    def get_class_fp_count(self, iou_threshold: float, score_threshold: float) -> int:
        """
        Grabs the number of classification false positives at 
        the specified IoU and score threshold.

        Parameters
        ----------
            iou_threshold: float
                The IoU threshold to consider classification false positives.

            score_threshold: float
                The score threshold to consider predictions.

        Returns
        -------
            count: int
                The number of classification false positives at the
                specified IoU and score threshold.
        """
        if len(self.class_fps):
            fp_iou = np.array(self.class_fps)[:, 0] >= iou_threshold
            fp_score = np.array(self.class_fps)[:, 1] >= score_threshold
            return np.count_nonzero(fp_iou * fp_score)
        return 0

    @property
    def local_fps(self) -> List[float]:
        """
        Attribute to access the localization false positives data.
        Can only be set to :py:class:`list`

        Returns
        -------
            :py:class:`list`
                This contains the score of each localization
                false positive for this label.
        """
        return self._local_fps

    @local_fps.setter
    def local_fps(self, this_local_fps: List[float]):
        """
        Sets the localization false positives data to a new value.

        Parameters
        ----------
            this_local_fps: :py:class:`list`
                These are localization false positives data to set.
        """
        self._local_fps = this_local_fps

    def add_local_fp(self, score: float):
        """
        Adds the number of false positive (localization) captured.
        A false positive (localization) is when there is a 
        prediction but no ground truth.

        Parameters
        ----------
            score: float
                The confidence score of the localization
                false positive prediction.

        Raises
        ------
            ValueError
                Raised if the provided score is not a floating 
                point type and is out bounds meaning it is
                greater than 1 or less than 0.
        """
        self.local_fps.append(clamp(score))

    def get_local_fp_scores(self) -> np.ndarray:
        """
        Grabs the prediction scores marked as localization false positives.

        Returns
        -------
            scores: np.ndarray
                The localization false positive scores.
        """
        if len(self.local_fps):
            return np.array(self.local_fps)
        return np.array([])

    def get_local_fp_count(self, iou_threshold: float, score_threshold: float) -> int:
        """
        Grabs the number of localization false positives at the specified IoU 
        and score threshold. The IoU threshold is needed because true positives 
        that have an IoU less than the set IoU threshold will be considered as 
        localization false positives.

        Parameters
        ----------
            iou_threshold: float
                The IoU threshold to consider true positives as local
                false positives.

            score_threshold: float
                The score threshold to consider predictions.

        Returns
        -------
            count: int
                The number of localization false positives at the
                specified IoU and score threshold.
        """
        local_fp = 0
        if len(self.tps):
            # Any predictions that are below the IoU thresholds are
            # localization false positives.
            fp_iou = np.array(self.tps)[:, 0] < iou_threshold
            tp_score = np.array(self.tps)[:, 1] >= score_threshold
            local_fp += np.count_nonzero(fp_iou * tp_score)

        if len(self.class_fps):
            class_fp_iou = np.array(self.class_fps)[:, 0] < iou_threshold
            class_fp_score = np.array(self.class_fps)[:, 1] >= score_threshold
            local_fp += np.count_nonzero(class_fp_iou * class_fp_score)

        local_fp += np.count_nonzero(np.array(self.local_fps)
                                     >= score_threshold)
        return local_fp

    @property
    def tp2fp(self) -> int:
        """
        Attribute to access the number of true positives that turned to
        localization false positives.
        Can only be set to :py:class:`int`

        Returns
        -------
            :py:class:`int`
                The number of true positives that turned to localization 
                false positives.
        """
        return self._tp2fp

    @tp2fp.setter
    def tp2fp(self, this_tp2fp: int):
        """
        Sets the number of true positives that turned to
        localization false positives.

        Parameters
        ----------
            this_tp2fp: :py:class:`int`
                These are the number of true positives that turned to
                localization false positives to set.
        """
        self._tp2fp = this_tp2fp

    def add_tp2fp(self, iou_threshold: float, score_threshold: float):
        """
        Adds the number of potential true positives that became localization 
        false positives due to their IoU being less than the defined 
        IoU threshold. 

        Parameters
        ----------
            iou_threshold: float
                The IoU threshold set.

            score_threshold: float
                The score threshold set. 
        """
        if len(self.tps):
            fp_iou = np.array(self.tps)[:, 0] < iou_threshold
            tp_score = np.array(self.tps)[:, 1] >= score_threshold
            # These are the IoUs for those TP that are less than threshold.
            # loc_iou = np.array(self.tps)[:, 0] * tp_score.astype(int)
            self.tp2fp += np.count_nonzero(fp_iou * tp_score)

    def get_fn_count(self, iou_threshold: float, score_threshold: float) -> int:
        """
        Grabs the number of false negatives at the specified IoU threshold 
        and score threshold. Score threshold is needed because by principle 
        fp = gt - tp, and score and IoU threshold is required to find the 
        number of true positives.

        Parameters
        ----------
            iou_threshold: float
                The IoU threshold to consider true positives.

            score_threshold: float
                The score threshold to consider predictions.

        Returns
        -------
            count: int
                The number of false negatives at the specified
                IoU and score threshold.
        """
        return self._ground_truths - self.get_tp_count(
            iou_threshold, score_threshold)

class DetectionDataCollection:
    """
    Acts as a container for DetectionLabelData objects 
    for each label and provides methods to capture the 
    total number of true positives, false positives, 
    and false negatives in the dataset.
    """
    def __init__(self):
        # A list containing the DetectionLabelData objects for each label.
        self._label_data_list = list()
        # A list containing the strings or integers of unique labels.
        self._labels = list()
        # A list containing the strings or integers of unfiltered labels.
        self._unfiltered_labels = list()

        """yolov5 properties for mAP"""
        self.tp = []
        self.conf = []
        self.pred_cls = []  # classes of detections
        self.target_cls = []  # classes of ground truths\
        self.ious = [0.5, 0.55, 0.60, 0.65, 0.70, 0.75, 0.8, 0.85, 0.9, 0.95]

    @property
    def label_data_list(self) -> List[DetectionLabelData]:
        """
        Attribute to access the list containing DetectionLabelData objects
        Can only be set to :py:class:`list`

        Returns
        -------
            :py:class:`list`
                This contains the DetectionLabelData objects.
        """
        return self._label_data_list

    @label_data_list.setter
    def label_data_list(self, label_datas: List[DetectionLabelData]):
        """
        Sets the list of DetectionLabelData objects.

        Parameters
        ----------
            label_datas: :py:class:`list`
                This is the list of DetectionLabelData objects to set.
        """
        self._label_data_list = label_datas

    def add_label_data(self, label: Union[str, int, np.integer]):
        """
        Adds DetectionLabelData object per label.

        Parameters
        ----------
            label: str or int
                The string label or the integer index to place as a data container.
        """
        self._label_data_list.append(DetectionLabelData(label))

    def get_label_data(
            self,
            label: Union[str, int, np.integer]) -> DetectionLabelData | None:
        """
        Grabs the DetectionLabelData object by label.

        Parameters
        ----------
            label: str or int
                A unique string label or integer index from the dataset.

        Returns
        -------
            None if the object does not exist.

            label_data: DetectionLabelData
                The data container of the label specified.
        """
        label_data: DetectionLabelData
        for label_data in self._label_data_list:
            if label_data.label == label:
                return label_data
        return None

    @property
    def labels(self) -> list:
        """
        Attribute to access the list of unique labels gathered.
        Can only be set to :py:class:`list`

        Returns
        -------
            :py:class:`list`
                This contains unique labels gathered during validation.
        """
        return self._labels

    @labels.setter
    def labels(self, new_labels: list):
        """
        Sets the list of unique labels gathered during validation.

        Parameters
        ----------
            new_labels: :py:class:`list`
                This is the list of unique labels gathered during validation.
        """
        self._labels = new_labels

    @property
    def unfiltered_labels(self) -> list:
        """
        Attribute to access the list of unique unfiltered labels gathered.
        Can only be set to :py:class:`list`

        Returns
        -------
            :py:class:`list`
                This contains unique unfiltered labels gathered 
                during validation.
        """
        return self._unfiltered_labels

    @unfiltered_labels.setter
    def unfiltered_labels(self, new_labels: list):
        """
        Sets the list of unique unfiltered labels gathered during validation.

        Parameters
        ----------
            new_labels: :py:class:`list`
                This is the list of unique unfiltered labels gathered 
                during validation.
        """
        self._unfiltered_labels = new_labels

    def store_unfiltered_labels(self, new_labels: Union[list, np.ndarray]):
        """
        Gathers and stores the unfiltered unique labels currently found.

        Parameters
        ----------
            new_labels: list, np.ndarray
                These are the new unfiltered labels found.
        """
        self._unfiltered_labels = np.unique(
            np.concatenate((self._unfiltered_labels, new_labels)))

    def reset_containers(self):
        """
        Resets the label_data_list container to an empty list 
        and resets the labels captured to an empty list.
        """
        self._label_data_list = list()
        self._labels = list()
        self._unfiltered_labels = list()

        """yolov5 properties for mAP"""
        self.tp = []
        self.conf = []
        self.pred_cls = []  # classes of detections
        self.target_cls = []  # classes of ground truths\

    def capture_class(self, labels: Union[list, np.ndarray]):
        """
        Records the unique labels encountered from the prediction and 
        ground truth and creates a container (DetectionLabelData) 
        for each unique label found.

        Parameters
        ----------
            labels: list or np.ndarray
                This list contains labels for one image from either the 
                ground truth or the predictions.
        """
        for label in labels:
            if isinstance(label, str):
                if label.lower() in ["background", " ", ""]:
                    continue
            if label not in self.labels:
                self.add_label_data(label)
                self.labels.append(label)