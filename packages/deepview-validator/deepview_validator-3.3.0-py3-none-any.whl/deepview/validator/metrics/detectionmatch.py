# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from __future__ import annotations
from typing import TYPE_CHECKING, Union, List
if TYPE_CHECKING:
    from deepview.validator.metrics import ImageSummary, PlotSummary
    from deepview.validator.metrics import DetectionDataCollection
    from deepview.validator.evaluators import Parameters
    from deepview.validator.datasets import Instance

from deepview.validator.exceptions import MatchingAlgorithmException
from deepview.validator.metrics.detectionutils import (
    minkowski_distance,
    localize_distance,
    get_center_point,
    iou_2d,
    iou_3d,
)
import numpy as np

class MatchDetections:
    """
    The purpose of this class is to match the model detections
    to the ground truth based on congruent labels and the highest
    IoU. This class also provides methods to classify that matches into
    true positives, false positives, and false negatives.

    Parameters
    ----------
        gt_instance: Instance
            This is the ground truth instance containing the ground truth 
            bounding boxes, labels, etc.

        dt_instance: Instance
            This is the prediction instance containing the prediction
            bounding boxes, scores, labels, etc.

        parameters:
            This contains the parameters set from the command line.

        data_collection: DetectionDataCollection
            This stores the number of true positives, false positives, and
            false negatives per label found throughout validation.

        image_summary: ImageSummary
            A summary per image containing information for which detections
            were matched to ground truths and which detections or 
            ground truths were not matched.

        plot_summary: PlotSummary
            This is a container for the data to draw the plots.

        verbose_store: bool
            If this is set to true, this means a verbose store information 
            for which detections were matched to ground truths and which 
            detections or ground truths were not matched in image summary.

    Raises
    ------
        MatchingAlgorithmException
            Raised if duplicate matches were found in the final results or
            an invalid metric is passed. 
    """
    def __init__(
        self,
        gt_instance: Instance,
        dt_instance: Instance,
        parameters: Parameters,
        data_collection: DetectionDataCollection,
        image_summary: ImageSummary,
        plot_summary: PlotSummary,
        verbose_store: bool = True
    ) -> None:

        self.gt_instance = gt_instance
        self.dt_instance = dt_instance
        self.parameters = parameters
        self.data_collection = data_collection
        self.image_summary = image_summary
        self.plot_summary = plot_summary
        self.verbose_store = verbose_store

        """Properties"""
        if self.parameters.validate_3d:
            self._ground_truths = gt_instance.corners
            self._predictions = dt_instance.corners
        else:
            self._ground_truths = gt_instance.boxes
            self._predictions = dt_instance.boxes

        # This contains the IoUs of each detection to ground truth match.
        self._iou_list = np.zeros(len(self._predictions))
        # An IoU map where rows are the ground truths and 
        # the predictions are the columns.
        self._iou_grid = np.zeros(
            (len(self._ground_truths), len(self._predictions)))
        # The matches containing ground truth and detection indices: 
        # [[gti, dti], [gti, dti], ..].
        self._index_matches = list()
        # The prediction indices that were not matched.
        self._index_unmatched_dt = list(range(0, len(self._predictions)))
        # The ground truth indices that were not matched.
        self._index_unmatched_gt = list(range(0, len(self._ground_truths)))

        # Assign shallow copy to these properties toward 
        # the properties in image_summary
        self.image_summary.index_matches = self.index_matches
        self.image_summary.index_unmatched_dt = self.index_unmatched_dt
        self.image_summary.index_unmatched_gt = self.index_unmatched_gt
        self.image_summary.iou_list = self.iou_list

    @property
    def ground_truths(self) -> Union[list, np.ndarray]:
        """
        Attribute to access the ground truths being matched.
        Can be set to :py:class:`list` or :py:class:`np.ndarray`

        Returns
        -------
            :py:class:`list` or :py:class:`np.ndarray`
                This is the ground truth list. This either contains
                bounding boxes if 2D validation or 3D box corners if
                3D validation. 
        """
        return self._ground_truths

    @ground_truths.setter
    def ground_truths(self, this_ground_truths: Union[list, np.ndarray]):
        """
        Sets the ground truth instance to matched.

        Parameters
        ----------
            this_ground_truths: :py:class:`list` or :py:class:`np.ndarray`
                These is the ground truth object. This either contains
                bounding boxes if 2D validation or 3D box corners if
                3D validation. 
        """
        self._ground_truths = this_ground_truths

    @property
    def predictions(self) -> Union[list, np.ndarray]:
        """
        Attribute to access the predictions being matched.
        Can be set to :py:class:`list` or :py:class:`np.ndarray`

        Returns
        -------
            :py:class:`list` or :py:class:`np.ndarray`
                This is the predictions list. This either contains
                bounding boxes if 2D validation or 3D box corners if
                3D validation. 
        """
        return self._predictions

    @predictions.setter
    def predictions(self, this_predictions: Union[list, np.ndarray]):
        """
        Sets the predictions list to matched.

        Parameters
        ----------
            this_predictions: :py:class:`list` or :py:class:`np.ndarray`
                These is the predictions list. This either contains
                bounding boxes if 2D validation or 3D box corners if
                3D validation. 
        """
        self._predictions = this_predictions

    @property
    def index_matches(self) -> List[List[int, int]]:
        """
        Attribute to access the index_matches. This contains the indices
        of the ground truth and the predictions that are matched in the format
        [[gti, dti], [gti, dti], ...].
        Can be set to :py:class:`list`

        Returns
        -------
            :py:class:`list` 
                The indices of the matched ground truth and the predictions.
        """
        return self._index_matches

    @index_matches.setter
    def index_matches(self, this_index_matches: List[List[int, int]]):
        """
        Sets the index_matches.

        Parameters
        ----------
            this_index_matches: :py:class:`list` 
                These is the index_matches.
        """
        self._index_matches = this_index_matches

    @property
    def index_unmatched_dt(self) -> List[int]:
        """
        Attribute to access the index_unmatched_dt. This contains the indices
        of the predictions that were unmatched.
        Can be set to :py:class:`list`

        Returns
        -------
            :py:class:`list` 
                The indices of the unmatched predictions.
        """
        return self._index_unmatched_dt

    @index_unmatched_dt.setter
    def index_unmatched_dt(self, this_index_unmatched_dt: List[int]):
        """
        Sets the index_unmatched_dt.

        Parameters
        ----------
            this_index_unmatched_dt: :py:class:`list` 
                The indices of the unmatched predictions.
        """
        self._index_unmatched_dt = this_index_unmatched_dt

    @property
    def index_unmatched_gt(self) -> List[int]:
        """
        Attribute to access the index_unmatched_gt. This contains the indices
        of the ground truths that were unmatched.
        Can be set to :py:class:`list`

        Returns
        -------
            :py:class:`list` 
                The indices of the unmatched ground truths.
        """
        return self._index_unmatched_gt

    @index_unmatched_gt.setter
    def index_unmatched_gt(self, this_index_unmatched_gt: List[int]):
        """
        Sets the index_unmatched_gt.

        Parameters
        ----------
            this_index_unmatched_gt: :py:class:`list` 
                The indices of the unmatched ground truths.
        """
        self._index_unmatched_gt = this_index_unmatched_gt

    @property
    def iou_list(self) -> Union[list, np.ndarray]:
        """
        Attribute to access the iou_list. This contains the IoUs of the 
        matched predictions to ground truths.
        Can be set to :py:class:`list` or :py:class:`np.ndarray`

        Returns
        -------
            :py:class:`list` or :py:class:`np.ndarray`
                The IoU of the matched predictions to ground truths.
        """
        return self._iou_list

    @iou_list.setter
    def iou_list(self, this_iou_list: Union[list, np.ndarray]):
        """
        Sets the iou_list.

        Parameters
        ----------
            this_iou_list: :py:class:`list` or :py:class:`np.ndarray`
                The IoUs of matched predictions to ground truths.
        """
        self._iou_list = this_iou_list

    @property
    def iou_grid(self) -> Union[list, np.ndarray]:
        """
        Attribute to access the iou_grid. This contains all the IoU 
        computations where the rows are the ground truths and the columns
        are the predictions.
        Can be set to :py:class:`list` or :py:class:`np.ndarray`

        Returns
        -------
            :py:class:`list` or :py:class:`np.ndarray`
                The IoU combinations rows->ground truths, columns->predictions.
        """
        return self._iou_grid

    @iou_grid.setter
    def iou_grid(self, this_iou_grid: Union[list, np.ndarray]):
        """
        Sets the iou_grid.

        Parameters
        ----------
            this_iou_grid: :py:class:`list`  or :py:class:`np.ndarray`
                The IoU matrix.
        """
        self._iou_grid = this_iou_grid

    def match(self): #NOSONAR
        """
        The matching algorithm which matches the predictions to ground truth
        based on matching labels first and then by highest IoU or lowest 
        centerpoint distance between boxes.

        This algorithm also incorporates recursive calls to 
        perform rematching of ground truth that were unmatched due to 
        duplicative matches, but the rematching is based on the next best IoU.

        Raises
        ------
            MatchingAlgorithmException
                Raised if duplicate matches were found in the final results or
                an invalid metric is passed. 
        """
        if 0 in [len(self.ground_truths), len(self.predictions)]:
            return
        if not self.parameters.rematching:
            # Just match each box to highest GT. Unmatch any duplicates
            for dti, dt in enumerate(self.predictions):
                for gti, gt in enumerate(self.ground_truths):
                    self.store_metric(gt, dt, gti, dti)

            idx = np.argsort(self.iou_grid, axis=None)[::-1]
            for i in idx:
                dti = i // self.iou_grid.shape[0]
                gti = i % self.iou_grid.shape[0]
                match_iou = self.iou_grid[gti, dti]
                if (match_iou > 0 and 
                    dti in self.index_unmatched_dt and
                    gti in self.index_unmatched_gt):
                    self.index_matches.append((dti, gti))
                    self.iou_list[dti] = match_iou
                    self.index_unmatched_dt.remove(dti)
                    self.index_unmatched_gt.remove(gti)
            return
        for gti, gt in enumerate(self.ground_truths):
            # A list of prediction indices with 
            # matching labels as the ground truth.
            dti_reflective, iou_reflective = list(), list()
            gt_label = self.gt_instance.labels[gti]

            for dti, dt in enumerate(self.predictions):
                self.store_metric(gt, dt, gti, dti)
                
                dt_label = self.dt_instance.labels[dti]
                if dt_label == gt_label:
                    dti_reflective.append(dti)
                    iou_reflective.append(self.iou_grid[gti][dti])
            
            # A potential match is the detection that produced the highest IoU.
            dti = np.argmax(self.iou_grid[gti])
            iou = max(self.iou_grid[gti])
            # If there is no intersection, it cannot be a match.
            if iou < 0:
                continue
            # Only match if the IoU between matching ground truth and detection labels > 0.
            if len(dti_reflective) and max(iou_reflective) >= self.parameters.validation_iou:
                # The IoU of the detections with the same labels
                # as the ground truth. A potential match is the
                # detection with the same label as the ground truth.
                dti = dti_reflective[np.argmax(iou_reflective)]
                iou = max(iou_reflective)
            self.compare_matches(dti, gti, iou)

        # Find the unmatched predictions
        for match in self.index_matches:
            self.index_unmatched_dt.remove(match[0])
            self.index_unmatched_gt.remove(match[1])

    def compare_matches(self, dti: int, gti: int, iou: float): #NOSONAR
        """
        Checks if duplicate matches exists. A duplicate match is when the 
        same detection is being matched to more than one ground truth. 
        The IoUs are compared and the better IoU is the true match and the 
        ground truth of the other match is then rematch to the next best IoU, 
        but it performs a recursive call to check if the next best IoU 
        also generates a duplicate match.

        Parameters
        ----------
            dti: int
                The detection index being matched to the current ground truth.

            gti: int
                The current ground truth matched to the detection.

            iou: float
                The current best IoU that was computed for the current ground
                truth against all detections.

        Raises
        ------
            MatchingAlgorithmException:
                Raised if a duplicate match was left unchecked 
                and was not rematched. 
        """
        twice_matched = [(d, g) for d, g in self.index_matches if d == dti]
        if len(twice_matched) == 1:
            # Compare the IoUs between duplicate matches.
            dti, pre_gti = twice_matched[0]
            if iou > self.iou_list[dti]:
                self.index_matches.remove((dti, pre_gti))
                self.iou_list[dti] = iou
                self.index_matches.append((dti, gti))

                # Rematch pre_gti
                self.iou_grid[pre_gti][dti] = 0.
                dti = np.argmax(self.iou_grid[pre_gti])
                iou = max(self.iou_grid[pre_gti])
                if iou > 0 and self.parameters.rematching:
                    self.compare_matches(dti, pre_gti, iou)
            else:
                # Rematch gti
                self.iou_grid[gti][dti] = 0.
                dti = np.argmax(self.iou_grid[gti])
                iou = max(self.iou_grid[gti])
                if iou > 0 and self.parameters.rematching:
                    self.compare_matches(dti, gti, iou)

        elif len(twice_matched) == 0:
            if iou > 0:
                self.iou_list[dti] = iou
                self.index_matches.append((dti, gti))
        else:
            raise MatchingAlgorithmException(
                "Duplicate matches were unchecked.")

    def store_metric_all(self, eps: float=1e-7): #NOSONAR
        """
        Attempt to store metrics in one call - Currently method is unused.
        Computes either the 3D or 2D IoU or centerpoint distances 
        and stores the values in the IoU grid.

        When the iou_first flag is False, IoU is considered 0 if the 
        classes don't match

        Parameters
        ----------
            eps: float
                Minimal threshold to avoid 0/0 divisions.

        Raises
        ------
            MatchingAlgorithmException
                Raised if an invalid metric is passed. 
        """
        if self.parameters.metric == "iou":
            if self.parameters.validate_3d:
                a1 = np.expand_dims(self.ground_truths[:, 0:3], 1)
                a2 = np.expand_dims(self.ground_truths[:, 3:6], 1)
                b1 = np.expand_dims(self.predictions[:, 0:3], 0)
                b2 = np.expand_dims(self.predictions[:, 3:6], 0)
                inter = (np.minimum(a2, b2) -
                         np.maximum(a1, b1)).clip(0).prod(2)
                if not self.parameters.iou_first:
                    classes_incorrect = self.dt_instance.labels != np.expand_dims(
                        self.gt_instance.labels, 1)
                    inter[classes_incorrect] = 0.

                self.iou_grid = inter / ((a2 - a1).prod(2) +
                                         (b2 - b1).prod(2) - inter + eps)
            else:
                a1 = np.expand_dims(self.ground_truths[:, 0:2], 1)
                a2 = np.expand_dims(self.ground_truths[:, 2:4], 1)
                b1 = np.expand_dims(self.predictions[:, 0:2], 0)
                b2 = np.expand_dims(self.predictions[:, 2:4], 0)
                inter = (np.minimum(a2, b2) -
                         np.maximum(a1, b1)).clip(0).prod(2)
                if not self.parameters.iou_first:
                    classes_incorrect = self.dt_instance.labels != np.expand_dims(
                        self.gt_instance.labels, 1)
                    inter[classes_incorrect] = 0.

                self.iou_grid = inter / ((a2 - a1).prod(2) +
                                         (b2 - b1).prod(2) - inter + eps)
        elif self.parameters.metric == "centerpoint":
            if self.parameters.validate_3d:
                for gti, gt in enumerate(self.ground_truths):
                    for dti, dt in enumerate(self.predictions):
                        if (not self.parameters.iou_first and 
                            self.dt_instance.labels[dti] != self.gt_instance.labels[gti]):
                            self.iou_grid[gti][dti] = 0
                            continue
                        self.iou_grid[gti][dti] = \
                            1 - minkowski_distance(
                                self.dt_instance.centers[dti],
                                self.gt_instance.centers[gti])
            else:
                for gti, gt in enumerate(self.ground_truths):
                    for dti, dt in enumerate(self.predictions):
                        if (not self.parameters.iou_first and 
                            self.dt_instance.labels[dti] != self.gt_instance.labels[gti]):
                            self.iou_grid[gti][dti] = 0
                            continue
                        dt_center = get_center_point(dt.astype(float))
                        gt_center = get_center_point(gt.astype(float))
                        self.iou_grid[gti][dti] = \
                            1 - minkowski_distance(dt_center, gt_center)
        else:
            raise MatchingAlgorithmException(
                "Unknown matching matching metric specified.")

    def store_metric(
        self,
        gt: Union[list, np.ndarray],
        dt: Union[list, np.ndarray],
        gti: int,
        dti: int
    ):
        """
        Computes either the 3D or 2D IoU or centerpoint distances 
        and stores the values in the IoU grid.

        When the iou_first flag is False, IoU is 
        considered 0 if the classes don't match.

        Parameters
        ----------
            gt: list or np.ndarray
                This either contains ground truth bounding boxes 
                if 2D validation or 3D box corners if 3D validation. 

            dt: list or np.ndarray
                This either contains prediction bounding boxes 
                if 2D validation or 3D box corners if 3D validation. 

            gti: int
                This is the index of the ground truth 
                bounding boxes or corners.

            dti: int 
                This is the index of the prediction 
                bounding boxes or corners.

        Raises
        ------
            MatchingAlgorithmException
                Raised if an invalid metric is passed. 
        """
        if (not self.parameters.iou_first and 
            self.dt_instance.labels[dti] != self.gt_instance.labels[gti]):
            self.iou_grid[gti][dti] = 0
            return
        if self.parameters.metric == "iou":
            if self.parameters.validate_3d:
                self.iou_grid[gti][dti] = \
                    iou_3d(np.transpose(dt.astype(float)),
                           np.transpose(gt.astype(float)))
            else:
                self.iou_grid[gti][dti] = \
                    iou_2d(dt.astype(float),
                           gt.astype(float))

        elif self.parameters.metric == "centerpoint":
            if self.parameters.validate_3d:
                self.iou_grid[gti][dti] = \
                    1 - minkowski_distance(
                        self.dt_instance.centers[dti],
                        self.gt_instance.centers[gti])
            else:
                self.iou_grid[gti][dti] = 1 - localize_distance(
                    dt.astype(float),
                    gt.astype(float),
                    leniency_factor=self.parameters.leniency_factor
                )
        else:
            raise MatchingAlgorithmException(
                "Unknown matching matching metric specified.")

    def classify_detections(self):
        """
        Classifies the matched, missed, and extra detections 
        into true positives, localization and classification false positives, 
        and false negatives.
        """
        self.classify_matches()
        self.classify_extras()
        self.classify_misses()
        self.setup_yolo_map()
        self.image_summary.ground_truths = len(self.gt_instance.labels)
        self.image_summary.predictions = len(self.dt_instance.labels)

    def setup_yolo_map(self): 
        """
        Formulates the variables needed to utilize the functionality of 
        calculating the average percision per class in YoloV5.
        https://github.com/ultralytics/yolov5/blob/master/utils/metrics.py#L29

        The following parameters are followed:: \
        
            tp: (nx10) np.ndarray
                This contains the True and False for each detection (rows) for 
                each IoU at 0.50-0.95 (columns).

            conf: (nx1) np.ndarray
                The confidence scores of each detections.

            pred_cls: (nx1) np.ndarray
                The prediction classes.

            target_cls: (nx1) np.ndarray
                The ground truth classes.
        """
        for match in self.index_matches:
            dt_label = self.dt_instance.labels[match[0]]
            gt_label = self.gt_instance.labels[match[1]]
            score = self.dt_instance.scores[match[0]]
            iou = self.iou_list[match[0]]

            if dt_label != gt_label:
                tp = [False for _ in self.data_collection.ious]
            else:
                tp = [iou >= x for x in self.data_collection.ious]

            self.data_collection.tp.append(tp)
            self.data_collection.conf.append(score)
            self.data_collection.pred_cls.append(dt_label)
            self.data_collection.target_cls.append(gt_label)

        for extra in self.index_unmatched_dt:
            dt_label = self.dt_instance.labels[extra]
            score = self.dt_instance.scores[extra]

            tp = [False for _ in self.data_collection.ious]
            self.data_collection.tp.append(tp)
            self.data_collection.conf.append(score)
            self.data_collection.pred_cls.append(dt_label)

        for miss in self.index_unmatched_gt:
            gt_label = self.gt_instance.labels[miss]
            self.data_collection.target_cls.append(gt_label)

    def classify_matches(self):  # NOSONAR
        """
        Classifies the matched detections as either 
        true positives or classification false positives.
        """
        for match in self.index_matches:
            dt_label = self.dt_instance.labels[match[0]]
            gt_label = self.gt_instance.labels[match[1]]
            score = self.dt_instance.scores[match[0]]
            iou = self.iou_list[match[0]]

            if dt_label != gt_label:
                label_data = self.data_collection.get_label_data(dt_label)
                if label_data is not None:
                    label_data.add_class_fp(iou, score)

            label_data = self.data_collection.get_label_data(gt_label)
            if label_data is not None:
                label_data.add_ground_truths()
                if dt_label == gt_label:
                    label_data.add_tp(iou, score)

            self.store_matched_centers(match)
            if self.verbose_store:
                self.store_matches(match)
                if score >= self.parameters.validation_score:
                    if iou >= self.parameters.validation_iou:
                        self.store_confusion_data(gt_label, dt_label)
                    # This would become either a localization false positive or
                    # false negative.
                    else:
                        self.store_confusion_data("background", dt_label)
                        self.store_confusion_data(gt_label, "background")

    def store_matches(self, match: List[int, int]):
        """
        Stores a verbose information about the matches in the image summary.
        This includes the bounding box, iou, score of the matches.

        Parameters
        ----------
            match: list
                This includes the index of the match 
                [detection index, ground truth index].
        """
        score = self.dt_instance.scores[match[0]]
        iou = self.iou_list[match[0]]

        # Stores the bounding box matches in the image summary.
        if len(self.dt_instance.boxes) > 0 or len(self.gt_instance.boxes) > 0:
            dt_label = self.dt_instance.labels[match[0]]
            gt_label = self.gt_instance.labels[match[1]]

            gt_box = list(self.gt_instance.boxes[match[1]])
            gt_box.insert(4, gt_label)
            dt_box = list(self.dt_instance.boxes[match[0]])
            dt_box.insert(4, dt_label)

            if score >= self.parameters.validation_score:
                self.image_summary.append_summary(
                    [
                        tuple([x if isinstance(x, str) else float(x)
                              for x in gt_box]),
                        tuple([x if isinstance(x, str) else float(x)
                              for x in dt_box]),
                        (float(iou),)
                    ]  # If it is a classification FP or TP.
                )
                self.image_summary.append_index_summary(
                    [
                        match[1],
                        match[0],
                        (float(iou),)
                    ]  # If it is a classification FP or TP.
                )
            else:
                self.image_summary.append_summary(
                    [
                        tuple([x if isinstance(x, str) else float(x)
                              for x in gt_box]),
                        None,
                        None
                    ]  # If it is a False Negative.
                )
                self.image_summary.append_index_summary(
                    [
                        match[1],
                        None,
                        None
                    ]  # If it is a False Negative.
                )

    def store_matched_centers(self, match: list):
        """
        Stores the matched centers in the image summary object. 
        These are the centers of the ground truth and detection bounding box.

        Parameters
        ----------
            match: list
                This includes the index of the match 
                [detection index, ground truth index].
        """
        score = self.dt_instance.scores[match[0]]
        iou = self.iou_list[match[0]]
        dt_center, gt_center = None, None

        # Stores the centerpoint coordinates in the image summary
        if (len(self.dt_instance.centers) > 0 and 
            len(self.gt_instance.centers) > 0):
            dt_center = self.dt_instance.centers[match[0]]
            gt_center = self.gt_instance.centers[match[1]]

            if (score >= self.parameters.validation_score and 
                iou >= self.parameters.validation_iou):
                self.image_summary.append_centers(gt_center, dt_center)      
        else:
            if self.parameters.metric == "centerpoint":
                dt_center = get_center_point(self.dt_instance.boxes[match[0]])
                gt_center = get_center_point(self.gt_instance.boxes[match[1]])

                if (score >= self.parameters.validation_score and 
                    iou >= self.parameters.validation_iou):
                    self.image_summary.append_centers(gt_center, dt_center)

    def classify_extras(self):
        """
        Classifies the extra predictions into localization false positives. 
        """
        for extra in self.index_unmatched_dt:
            dt_label = self.dt_instance.labels[extra]
            score = self.dt_instance.scores[extra]

            label_data = self.data_collection.get_label_data(dt_label)
            if label_data is not None:
                label_data.add_local_fp(score)

            if self.verbose_store:
                self.store_extras(extra)
                if score >= self.parameters.validation_score:
                    self.store_confusion_data("background", dt_label)

    def store_extras(self, extra: int):
        """
        Stores a verbose information about the extra predictions inside
        the image summary object such as the bounding box, score, and label 
        of this extra prediction.

        Parameters
        ---------
            extra: int
                This is the index of the extra prediction. 
        """
        dt_label = self.dt_instance.labels[extra]
        score = self.dt_instance.scores[extra]
        # Stores the unmatched predictions in the image summary
        if len(self.dt_instance.boxes) > 0:
            if score >= self.parameters.validation_score:
                dt_box = list(self.dt_instance.boxes[extra])
                dt_box.insert(4, dt_label)
                self.image_summary.append_summary(
                    [
                        None,
                        tuple([x if isinstance(x, str) else float(x)
                              for x in dt_box]),
                        None
                    ]  # If it is a localization FP.
                )
                self.image_summary.append_index_summary(
                    [
                        None,
                        extra,
                        None
                    ]  # If it is a localization FP.
                )

    def classify_misses(self):
        """
        Classifies the missed predictions into false negatives.
        """
        for miss in self.index_unmatched_gt:
            gt_label = self.gt_instance.labels[miss]

            label_data = self.data_collection.get_label_data(gt_label)
            if label_data is not None:
                label_data.add_ground_truths()

            if self.verbose_store:
                self.store_misses(miss)
                self.store_confusion_data(gt_label, "background")

    def store_misses(self, miss: int):
        """
        Stores a verbose information on the missed predictions such as the 
        bounding box and the label. 

        Parameters
        ----------
            miss: int
                This is the index of the missed prediction. 
        """
        gt_label = self.gt_instance.labels[miss]
        # Store the unmatched ground truths inside the image summary.
        if len(self.gt_instance.boxes) > 0:
            gt_box = list(self.gt_instance.boxes[miss])
            gt_box.insert(4, gt_label)
            self.image_summary.append_summary(
                [
                    tuple([x if isinstance(x, str) else float(x)
                          for x in gt_box]),
                    None,
                    None
                ]  # If it is a False Negative.
            )
            self.image_summary.append_index_summary(
                [
                    miss,
                    None,
                    None
                ]  # If it is a False Negative.
            )

    def store_confusion_data(
        self,
        gt_label: Union[str, int, np.integer],
        dt_label: Union[str, int, np.integer]
    ):
        """
        Collects data to plot the confusion matrix.

        Parameters
        ----------
            gt_label: str or int
                This is the ground truth label.

            dt_label: str, int
                This is the detection label.
        """
        if isinstance(gt_label, np.ndarray):
            gt_label = gt_label[0]
        if isinstance(dt_label, np.ndarray):
            dt_label = dt_label[0]
        self.plot_summary.append_confusion_matrix_data((gt_label, dt_label))