# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.metrics.detectionutils import minkowski_distance
from typing import Union, List
import numpy as np

class ImageSummary:
    """
    The validation summary per image.

    Parameters
    ----------
        image_path: str
            The path or name of the image.

    Raises
    ------
        ValueError
            This error is raised if a dictionary argument to set
            does not contain the expected keys.
    """
    def __init__(
            self,
            image_path: str
    ) -> None:

        self._image_path = image_path
        self._ground_truths = 0
        self._predictions = 0

        """Detection Summary"""
        self._index_matches = list()
        self._index_extra_dt = list()
        self._index_missed_gt = list()
        self._iou_list = list()

        # A container for the matched centers
        self._centers = {
            "gt_centers": [],
            "dt_centers": [],
            "center_distances": []
        }

        """
        The following summary will have the format below:
        [
			[(gt_box), (dt_box), (iou,)], # A Classification FP or a TP
			[(gt_box),  None, 	  None],  # A False Negative
			[None, (dt_box), None], 	  # A Localizaiton False Positive
		]
        """
        self._summary = list()
        self._index_summary = list()

        """Segmentation Summary"""
        self._true_predictions = 0
        self._false_predictions = 0
        self._union = 0

        """Pose Summary"""

    @property
    def image_path(self) -> str:
        """
        Attribute to access the image path/name.
        Can only be set to :py:class:`str`

        Returns
        -------
            :py:class:`str`: The image path/name
        """
        return self._image_path

    @image_path.setter
    def image_path(self, image_path: str):
        """
        Sets the image path/name.

        Parameters
        ----------
            image_path: str
                The image path/name
        """
        self._image_path = image_path

    @property
    def ground_truths(self) -> int:
        """
        Attribute to access the number of ground truths.
        Can only be set to :py:class:`int`

        Returns
        -------
            :py:class:`int`: The number of ground truths in the image.
        """
        return self._ground_truths

    @ground_truths.setter
    def ground_truths(self, gts: int):
        """
        Sets the number of ground truths in the image.

        Parameters
        ----------
            gts: int
                This is the number of ground truths in the image.
        """
        self._ground_truths = gts

    @property
    def predictions(self) -> int:
        """
        Attribute to access the number of predictions.
        Can only be set to :py:class:`int`

        Returns
        -------
            :py:class:`int`: The number of predictions in the image.
        """
        return self._predictions

    @predictions.setter
    def predictions(self, dts: int):
        """
        Sets the number of predictions in the image.

        Parameters
        ----------
            dts: int
                This is the number of predictions in the image.
        """
        self._predictions = dts

    @property
    def index_matches(self) -> List[list]:
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
    def index_matches(self, this_index_matches: List[list]):
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
        Can be set to :py:class:`list`

        Returns
        -------
            :py:class:`list` 
                The IoU of the matched predictions to ground truths.
        """
        return self._iou_list

    @iou_list.setter
    def iou_list(self, this_iou_list: Union[list, np.ndarray]):
        """
        Sets the iou_list.

        Parameters
        ----------
            this_iou_list: :py:class:`list` 
                The IoUs of matched predictions to ground truths.
        """
        self._iou_list = this_iou_list

    @property
    def centers(self) -> dict:
        """
        Attribute to access the matched center points of the bounding boxes.
        Can only be set to :py:class:dict.

        Returns
        -------
            :py:class:dict.: The matched center points of the bounding boxes.
        """
        return self._centers

    @centers.setter
    def centers(self, this_centers: dict):
        """
        Sets the matched center points to another dictionary.

        Parameters
        ----------
            this_centers: dict
                The matched center points to set.

        Raises
        ------
            ValueError
                This error is raised if the dictionary does not contain
                the expected keys.
        """
        if not all(key in this_centers.keys()
                   for key in ["gt_centers", "dt_centers", "center_distances"]):
            raise ValueError(
                f"The following keys are expected: {this_centers.keys()}")
        self._centers = this_centers

    def append_centers(
        self,
        gt_center: Union[list, np.ndarray],
        dt_center: Union[list, np.ndarray]
    ):
        """
        Appends the center points of the bounding boxes assuming gt_center
        and dt_center are matched.

        Parameters
        ----------
            gt_center: list or np.ndarray
                This contains the (x,y,z) center of the ground truth bounding box.

            dt_center: list or np.ndarray
                This contains the (x,y,z) center of the prediction bounding box.
        """
        self._centers["gt_centers"].append(gt_center)
        self._centers["dt_centers"].append(dt_center)
        self._centers["center_distances"].append(minkowski_distance(dt_center, gt_center))

    @property
    def summary(self) -> list:
        """
        Attribute to access the summary. 
        The following summary will have the format below:: 

            .. code-block:: python

                [[(gt_box), (dt_box), (iou,)], # A Classification FP or a TP
                 [(gt_box),  None, 	  None],  # A False Negative
                 [None, (dt_box), None], 	  # A Localizaiton False Positive]

        Returns
        -------
            :py:class:list: The summary of the image 
            predictions and ground truths.
        """
        return self._summary

    @summary.setter
    def summary(self, this_summary: list):
        """
        Sets the summary.

        Parameters
        ----------
            this_summary: :py:class:list.
                The summary of the image predictions and ground truths.
        """
        self._summary = this_summary

    @property
    def index_summary(self) -> list:
        """
        Attribute to access the summary. 
        The following summary will have the format below:: 

            .. code-block:: python

                [[(gt_box), (dt_box), (iou,)], # A Classification FP or a TP
                 [(gt_box),  None, 	  None],  # A False Negative
                 [None, (dt_box), None], 	  # A Localizaiton False Positive]

        Returns
        -------
            :py:class:list: The summary of the image 
            predictions and ground truths.
        """
        return self._index_summary

    @index_summary.setter
    def index_summary(self, this_summary: list):
        """
        Sets the summary.

        Parameters
        ----------
            this_summary: :py:class:list.
                The summary of the image predictions and ground truths.
        """
        self._index_summary = this_summary

    def append_summary(self, summary_instance: list):
        """
        Summary instance has one of the following forms that is indicative
        of its nature as either a true positive, classification or localiation 
        false positive, or false negative:: 

            .. code-block:: python
                [
                    [(gt_box), (dt_box), (iou,)], # A Classification FP or a TP
                    [(gt_box),  None, 	  None],  # A False Negative
                    [None, (dt_box), None], 	  # A Localizaiton False Positive
                ]

        Parameters
        ----------
            summary_instance: list
                An information about the image summary.
        """
        self._summary.append(summary_instance)

    def append_index_summary(self, summary_instance: list):
        """
        Summary instance has one of the following forms that is indicative
        of its nature as either a true positive, classification or localiation 
        false positive, or false negative:: 

            .. code-block:: python
                [
                    [(gt_box), (dt_box), (iou,)], # A Classification FP or a TP
                    [(gt_box),  None, 	  None],  # A False Negative
                    [None, (dt_box), None], 	  # A Localizaiton False Positive
                ]

        Parameters
        ----------
            summary_instance: list
                An information about the image summary.
        """
        self._index_summary.append(summary_instance)

    @property
    def true_predictions(self) -> int:
        """
        Attribute to access the number of true_predictions.
        Can only be set to :py:class:`int`

        Returns
        -------
            :py:class:`int`: The number of true_predictions for the image.
        """
        return self._true_predictions

    @true_predictions.setter
    def true_predictions(self, tps: int):
        """
        Sets the number of true_predictions for the image.

        Parameters
        ----------
            tps: int
                This is the number of true_predictions for the image.
        """
        self._true_predictions = tps

    @property
    def false_predictions(self) -> int:
        """
        Attribute to access the number of false_predictions.
        Can only be set to :py:class:`int`

        Returns
        -------
            :py:class:`int`: The number of false_predictions for this image.
        """
        return self._false_predictions

    @false_predictions.setter
    def false_predictions(self, fps: int):
        """
        Sets the number of false_predictions for this image.

        Parameters
        ----------
            fps: int
                This is the number of false_predictions for this image.
        """
        self._false_predictions = fps

    @property
    def union(self) -> int:
        """
        Attribute to access the number of union pixels.
        Can only be set to :py:class:`int`

        Returns
        -------
            :py:class:`int`: The number of ground truths and prediction pixels
            for the image
        """
        return self._union

    @union.setter
    def union(self, uni: int):
        """
        Sets the number of ground truths and prediction pixels
        for the image.

        Parameters
        ----------
            uni: int
                This is the number of union for this image.
        """
        self._union = uni

    def add_union(self, uni: int = 1):
        """
        Adds the number of existing union pixels.

        Parameters
        ----------
            uni: int
                The number of union pixels to add.
        """
        self._union += uni

class MetricSummary:
    """
    Validation summary used to store the validation metrics
    of the model using the validation dataset provided.

    Parameters
    ----------
        model: str
            The path or name of the model.

        dataset: str
            The path or name of the validation dataset.

    Raises
    ------
        ValueError
            This error is raised if the dictionary does not contain
            the expected keys.
    """
    def __init__(
            self,
            model: str = "Training Model",
            dataset: str = "Validation Dataset",
    ) -> None:

        self._model = model
        self._dataset = dataset
        self._save_path = None
        # This list becomes too resource intensive.
        # self._image_summaries = list() # NOSONAR
        self._ground_truths = 0
        # This is used for segmentation total number of prediction pixels.
        self._predictions = 0

        """Detection Summaries"""
        # A container for the matched centers
        self._centers = {
            "gt_centers": [],
            "dt_centers": [],
            "center_distances": []
        }

        self._true_positives = 0
        self._false_negatives = 0
        self._classification_false_positives = 0
        self._localization_false_positives = 0
        self._overall_precision = np.nan
        self._overall_recall = np.nan
        self._overall_accuracy = np.nan

        self._map = {
            "0.50": np.nan,
            "0.75": np.nan,
            "0.50:0.95": np.nan,
        }

        self._mar = {
            "0.50": np.nan,
            "0.75": np.nan,
            "0.50:0.95": np.nan,
        }

        self._macc = {
            "0.50": np.nan,
            "0.75": np.nan,
            "0.50:0.95": np.nan,
        }

        self._classification_fp_error = {
            "0.50": np.nan,
            "0.75": np.nan,
            "0.50:0.95": np.nan,
        }

        self._localization_fp_error = {
            "0.50": np.nan,
            "0.75": np.nan,
            "0.50:0.95": np.nan,
        }

        self._append_centers = False
        self._mae_centers = {
            "x-center-mae": np.nan,
            "y-center-mae": np.nan,
            "z-center-mae": np.nan,
            "distance-mae": np.nan,
        }

        """Segmentation Summaries"""
        self._true_predictions = 0
        self._false_predictions = 0
        self._union = 0
        self._average_precision = np.nan
        self._average_recall = np.nan
        self._average_accuracy = np.nan

        """Pose Summaries"""
        self._angles_mae = list()

        self._timings = {
            "min_inference_time": None,
            "max_inference_time": None,
            "min_input_time": None,
            "max_input_time": None,
            "min_decoding_time": None,
            "max_decoding_time": None,
            "avg_inference": None,
            "avg_input": None,
            "avg_decoding": None,
        }

    @property
    def model(self) -> str:
        """
        Attribute to access the model path/name.
        Can only be set to :py:class:`str`

        Returns
        -------
            :py:class:`str`: The model path/name
        """
        return self._model

    @model.setter
    def model(self, model_path: str):
        """
        Sets the model path/name.

        Parameters
        ----------
            model_path: str
                The model path/name
        """
        self._model = model_path

    @property
    def dataset(self) -> str:
        """
        Attribute to access the dataset path/name.
        Can only be set to :py:class:`str`

        Returns
        -------
            :py:class:`str`: The dataset path/name
        """
        return self._dataset

    @dataset.setter
    def dataset(self, dataset_path: str):
        """
        Sets the dataset path/name.

        Parameters
        ----------
            dataset_path: str
                The dataset path/name
        """
        self._dataset = dataset_path

    @property
    def save_path(self) -> str:
        """
        Attribute to access the path to save the results.
        Can only be set to :py:class:`str`

        Returns
        -------
            :py:class:`str`: The path to save the results.
        """
        return self._save_path

    @save_path.setter
    def save_path(self, this_save_path: str):
        """
        Sets the path to save the results.

        Parameters
        ----------
            this_save_path: str
                The path to save the results
        """
        self._save_path = this_save_path

    @property
    def image_summaries(self) -> List[ImageSummary]:
        """
        Attribute to access the image summaries.
        Can be set to :py:class:`list` of ImageSummary

        Returns
        -------
            :py:class:`list` of ImageSummary
                This contains summary of each image.
        """
        return self._image_summaries

    @image_summaries.setter
    def image_summaries(self, this_summaries: List[ImageSummary]):
        """
        Sets the image summaries to a new value.

        Parameters
        ----------
            this_summaries: :py:class:`list` of ImageSummary
                These are the summary objects per image
        """
        self._image_summaries = this_summaries

    def append_image_summary(self, summary: ImageSummary):
        """
        Appends the image summary list with an ImageSummary object.
        This also adds the current number of ground truths for the dataset
        based on the number of ground truths from image summary being appended.

        Parameters
        ----------
            summary: ImageSummary
                An object containing the summary per image.
        """
        self.add_ground_truths(summary.ground_truths)
        self._image_summaries.append(summary)

    @property
    def ground_truths(self) -> int:
        """
        Attribute to access the number of ground truths.
        Can only be set to :py:class:`int`

        Returns
        -------
            :py:class:`int`: The number of ground truths in the dataset.
        """
        return self._ground_truths

    @ground_truths.setter
    def ground_truths(self, gts: int):
        """
        Sets the number of ground truths in the dataset.

        Parameters
        ----------
            gts: int
                This is the number of ground truths in the dataset.
        """
        self._ground_truths = gts

    def add_ground_truths(self, gts: int):
        """
        Adds the number of existing ground truths.

        Parameters
        ----------
            gts: int
                The number of ground truths to add.
        """
        self._ground_truths += gts

    @property
    def predictions(self) -> int:
        """
        Attribute to access the number of predictions.
        Can only be set to :py:class:`int`

        Returns
        -------
            :py:class:`int`: The number of predictions in the dataset.
        """
        return self._predictions

    @predictions.setter
    def predictions(self, prd: int):
        """
        Sets the number of predictions in the dataset.

        Parameters
        ----------
            prd: int
                This is the number of predictions in the dataset.
        """
        self._predictions = prd

    def add_predictions(self, prd: int):
        """
        Adds the number of existing predictions.

        Parameters
        ----------
            prd: int
                The number of predictions to add.
        """
        self._predictions += prd

    @property
    def centers(self) -> dict:
        """
        Attribute to access the matched center points of the bounding boxes.
        Can only be set to :py:class:dict.

        Returns
        -------
            :py:class:dict.: The matched center points of the bounding boxes.
        """
        return self._centers

    @centers.setter
    def centers(self, this_centers: dict):
        """
        Sets the matched center points to another dictionary.

        Parameters
        ----------
            this_centers: dict
                The matched center points to set.

        Raises
        ------
            ValueError
                This error is raised if the dictionary does not contain
                the expected keys.
        """
        if not all(key in this_centers.keys()
                   for key in ["gt_centers", "dt_centers", "center_distances"]):
            raise ValueError(
                f"The following keys are expected: {this_centers.keys()}")
        self._centers = this_centers

    def store_centers(
        self,
        gt_centers: Union[list, np.ndarray],
        dt_centers: Union[list, np.ndarray],
        center_distances: Union[list, np.ndarray]
    ):
        """
        Appends the center points of the bounding boxes assuming gt_center
        and dt_center are matched. Furthermore, the distance between the
        centers is also stored.

        Parameters
        ----------
            gt_centers: list or np.ndarray
                This contains the [[x,y,z], ...] center of the ground truth 
                bounding box.

            dt_centers: list or np.ndarray
                This contains the [[x,y,z], ...] center of the prediction 
                bounding box.
            
            center_distances: list or np.ndarray
                This contains the center distances between matched 
                ground truth and prediction.
        """
        self._centers["gt_centers"] += gt_centers
        self._centers["dt_centers"] += dt_centers
        self._centers["center_distances"] += center_distances

    @property
    def true_positives(self) -> int:
        """
        Attribute to access the number of true positives.
        Can only be set to :py:class:`int`

        Returns
        -------
            :py:class:`int`: The number of true positives in the dataset.
        """
        return self._true_positives

    @true_positives.setter
    def true_positives(self, tps: int):
        """
        Sets the number of true positives in the dataset.

        Parameters
        ----------
            tps: int
                This is the number of true positives in the dataset.
        """
        self._true_positives = tps

    @property
    def false_negatives(self) -> int:
        """
        Attribute to access the number of false negatives.
        Can only be set to :py:class:`int`

        Returns
        -------
            :py:class:`int`: The number of false negatives in the dataset.
        """
        self._false_negatives = self.ground_truths - (
            self.true_positives + self.classification_false_positives)
        return self._false_negatives

    @false_negatives.setter
    def false_negatives(self, fns: int):
        """
        Sets the number of false negatives in the dataset.

        Parameters
        ----------
            fns: int
                This is the number of false negatives in the dataset.
        """
        self._false_negatives = fns

    @property
    def classification_false_positives(self) -> int:
        """
        Attribute to access the number of classification false positives.
        Can only be set to :py:class:`int`

        Returns
        -------
            :py:class:`int`: The number of 
                classification false positives in the dataset.
        """
        return self._classification_false_positives

    @classification_false_positives.setter
    def classification_false_positives(self, cfps: int):
        """
        Sets the number of classification false positives in the dataset.

        Parameters
        ----------
            cfps: int
                This is the number of classification 
                false positives in the dataset.
        """
        self._classification_false_positives = cfps

    @property
    def localization_false_positives(self) -> int:
        """
        Attribute to access the number of localization false positives.
        Can only be set to :py:class:`int`

        Returns
        -------
            :py:class:`int`: The number of 
                localization false positives in the dataset.
        """
        return self._localization_false_positives

    @localization_false_positives.setter
    def localization_false_positives(self, lfps: int):
        """
        Sets the number of localization false positives in the dataset.

        Parameters
        ----------
            lfps: int
                This is the number of localization 
                false positives in the dataset.
        """
        self._localization_false_positives = lfps

    @property
    def overall_precision(self) -> float:
        """
        Attribute to access the overall precision score. 
        Can only be set to :py:class:float.

        Returns
        -------
            :py:class:float: The overall precision score.
        """
        return self._overall_precision

    @overall_precision.setter
    def overall_precision(self, precision: float):
        """
        Sets the overall precision score.

        Parameters
        ----------
            op: float
                The overall precision to set.
        """
        self._overall_precision = precision

    @property
    def overall_recall(self) -> float:
        """
        Attribute to access the overall recall score. 
        Can only be set to :py:class:float.

        Returns
        -------
            :py:class:float: The overall recall score.
        """
        return self._overall_recall

    @overall_recall.setter
    def overall_recall(self, recall: float):
        """
        Sets the overall recall score.

        Parameters
        ----------
            recall: float
                The overall recall to set.
        """
        self._overall_recall = recall

    @property
    def overall_accuracy(self) -> float:
        """
        Attribute to access the overall accuracy score. 
        Can only be set to :py:class:float

        Returns
        -------
            :py:class:float: The overall accuracy score.
        """
        return self._overall_accuracy

    @overall_accuracy.setter
    def overall_accuracy(self, accuracy: float):
        """
        Sets the overall accuracy score.

        Parameters
        ----------
            accuracy: float
                The overall accuracy to set.
        """
        self._overall_accuracy = accuracy

    @property
    def map(self) -> dict:
        """
        Attribute to access the mAP at IoU thresholds 0.50, 0.75, 0.50:0.95. 
        Can only be set to :py:class:dict.

        Returns
        -------
            :py:class:dict: The mAP scores at various IoU thresholds.
        """
        return self._map

    @map.setter
    def map(self, this_map: dict):
        """
        Sets the mAP scores at IoU thresholds 0.50, 0.75, 0.50:0.95.

        Parameters
        ----------
            this_map: dict
                The mAP scores to set.

        Raises
        ------
            ValueError
                This error is raised if the dictionary does not contain
                the expected keys.
        """
        if not all(key in this_map.keys()
                   for key in ["0.50", "0.75", "0.50:0.95"]):
            raise ValueError(
                f"The following keys are expected: {this_map.keys()}")
        self._map = this_map

    @property
    def mar(self) -> dict:
        """
        Attribute to access the mAR at IoU thresholds 0.50, 0.75, 0.50:0.95. 
        Can only be set to :py:class:dict.

        Returns
        -------
            :py:class:dict: The mAR scores at various IoU thresholds.
        """
        return self._mar

    @mar.setter
    def mar(self, this_mar: dict):
        """
        Sets the mAR scores at IoU thresholds 0.50, 0.75, 0.50:0.95.

        Parameters
        ----------
            this_mar: dict
                The mAR scores to set.

        Raises
        ------
            ValueError
                This error is raised if the dictionary does not contain
                the expected keys.
        """
        if not all(key in this_mar.keys()
                   for key in ["0.50", "0.75", "0.50:0.95"]):
            raise ValueError(
                f"The following keys are expected: {this_mar.keys()}")
        self._mar = this_mar

    @property
    def macc(self) -> dict:
        """
        Attribute to access the mACC at IoU thresholds 0.50, 0.75, 0.50:0.95. 
        Can only be set to :py:class:dict.

        Returns
        -------
            :py:class:dict: The mACC scores at various IoU thresholds.
        """
        return self._macc

    @macc.setter
    def macc(self, this_macc: dict):
        """
        Sets the mACC scores at IoU thresholds 0.50, 0.75, 0.50:0.95.

        Parameters
        ----------
            this_macc: dict
                The mACC scores to set.

        Raises
        ------
            ValueError
                This error is raised if the dictionary does not contain
                the expected keys.
        """
        if not all(key in this_macc.keys()
                   for key in ["0.50", "0.75", "0.50:0.95"]):
            raise ValueError(
                f"The following keys are expected: {this_macc.keys()}")
        self._macc = this_macc

    @property
    def classification_fp_error(self) -> dict:
        """
        Attribute to access the classification false positive error rate 
        at IoU thresholds 0.50, 0.75, 0.50:0.95. 
        Can only be set to :py:class:dict.

        Returns
        -------
            :py:class:dict: The classification FP error 
            at various IoU thresholds.
        """
        return self._classification_fp_error

    @classification_fp_error.setter
    def classification_fp_error(self, cfp_error: dict):
        """
        Sets the classification FP error rate
        at IoU thresholds 0.50, 0.75, 0.50:0.95.

        Parameters
        ----------
            cfp_error: dict
                The classification FP error to set.

        Raises
        ------
            ValueError
                This error is raised if the dictionary does not contain
                the expected keys.
        """
        if not all(key in cfp_error.keys()
                   for key in ["0.50", "0.75", "0.50:0.95"]):
            raise ValueError(
                f"The following keys are expected: {cfp_error.keys()}")
        self._classification_fp_error = cfp_error

    @property
    def localization_fp_error(self) -> dict:
        """
        Attribute to access the localization false positive error rate 
        at IoU thresholds 0.50, 0.75, 0.50:0.95. 
        Can only be set to :py:class:dict.

        Returns
        -------
            :py:class:dict: The localization FP error 
            at various IoU thresholds.
        """
        return self._localization_fp_error

    @localization_fp_error.setter
    def localization_fp_error(self, lfp_error: dict):
        """
        Sets the localization FP error rate
        at IoU thresholds 0.50, 0.75, 0.50:0.95.

        Parameters
        ----------
            lfp_error: dict
                The localization FP error to set.

        Raises
        ------
            ValueError
                This error is raised if the dictionary does not contain
                the expected keys.
        """
        if not all(key in lfp_error.keys()
                   for key in ["0.50", "0.75", "0.50:0.95"]):
            raise ValueError(
                f"The following keys are expected: {lfp_error.keys()}")
        self._localization_fp_error = lfp_error

    @property
    def append_centers(self) -> bool:
        """
        Attribute to access append_centers. 
        Specify whether to include centers metric in the table of summaries.
        Can only be set to :py:class:bool.

        Returns
        -------
            :py:class:bool: Condition to include center metrics.
        """
        return self._append_centers

    @append_centers.setter
    def append_centers(self, this_append_centers: bool):
        """
        Specify whether to include centers metric in the table of summaries.

        Parameters
        ----------
            this_append_centers: bool
                The condition to set.
        """
        self._append_centers = this_append_centers

    @property
    def mae_centers(self) -> dict:
        """
        Attribute to access the mean average error of the 
        bounding box centers.
        Can only be set to :py:class:dict.

        Returns
        -------
            :py:class:dict: The MAE of the bounding box centers.
        """
        return self._mae_centers

    @mae_centers.setter
    def mae_centers(self, this_mae_centers: dict):
        """
        Sets the mean average error of the bounding box centers.

        Parameters
        ----------
            this_mae_centers: dict
                The MAE of the centers.

        Raises
        ------
            ValueError
                This error is raised if the dictionary does not contain
                the expected keys.
        """
        if not all(key in this_mae_centers.keys()
                   for key in ["x-center-mae",
                               "y-center-mae",
                               "z-center-mae",
                               "distance-mae"]):
            raise ValueError(
                f"The following keys are expected: {this_mae_centers.keys()}")
        self._mae_centers = this_mae_centers

    @property
    def true_predictions(self) -> int:
        """
        Attribute to access the number of true_predictions.
        Can only be set to :py:class:int.

        Returns
        -------
            :py:class:`int`: The number of true_predictions for this dataset.
        """
        return self._true_predictions

    @true_predictions.setter
    def true_predictions(self, tps: int):
        """
        Sets the number of true_predictions for this dataset.

        Parameters
        ----------
            tps: int
                This is the number of true_predictions for this dataset.
        """
        self._true_predictions = tps

    def add_true_predictions(self, tps: int = 1):
        """
        Adds the number of existing true_predictions.

        Parameters
        ----------
            tps: int
                The number of true_predictions to add.
        """
        self._true_predictions += tps

    @property
    def false_predictions(self) -> int:
        """
        Attribute to access the number of false_predictions.
        Can only be set to :py:class:`int`

        Returns
        -------
            :py:class:`int`: The number of false_predictions for this dataset.
        """
        return self._false_predictions

    @false_predictions.setter
    def false_predictions(self, fps: int):
        """
        Sets the number of false_predictions for this dataset.

        Parameters
        ----------
            fps: int
                This is the number of false_predictions for this dataset.
        """
        self._false_predictions = fps

    def add_false_predictions(self, fps: int = 1):
        """
        Adds the number of existing false_predictions.

        Parameters
        ----------
            fps: int
                The number of false_predictions to add.
        """
        self._false_predictions += fps

    @property
    def union(self) -> int:
        """
        Attribute to access the number of union pixels.
        Can only be set to :py:class:`int`

        Returns
        -------
            :py:class:`int`: The number of ground truths and prediction pixels
            for the dataset
        """
        return self._union

    @union.setter
    def union(self, uni: int):
        """
        Sets the number of ground truths and prediction pixels
        for the dataset

        Parameters
        ----------
            uni: int
                This is the number of union for this dataset.
        """
        self._union = uni

    def add_union(self, uni: int = 1):
        """
        Adds the number of existing union pixels.

        Parameters
        ----------
            uni: int
                The number of union pixels to add.
        """
        self._union += uni

    @property
    def average_precision(self) -> float:
        """
        Attribute to access the average precision score. 
        Can only be set to :py:class:float.

        Returns
        -------
            :py:class:float: The average precision score.
        """
        return self._average_precision

    @average_precision.setter
    def average_precision(self, precision: float):
        """
        Sets the average precision score.

        Parameters
        ----------
            op: float
                The average precision to set.
        """
        self._average_precision = precision

    @property
    def average_recall(self) -> float:
        """
        Attribute to access the average recall score. 
        Can only be set to :py:class:float.

        Returns
        -------
            :py:class:float: The average recall score.
        """
        return self._average_recall

    @average_recall.setter
    def average_recall(self, recall: float):
        """
        Sets the average recall score.

        Parameters
        ----------
            recall: float
                The average recall to set.
        """
        self._average_recall = recall

    @property
    def average_accuracy(self) -> float:
        """
        Attribute to access the average accuracy score. 
        Can only be set to :py:class:float.

        Returns
        -------
            :py:class:float: The average accuracy score.
        """
        return self._average_accuracy

    @average_accuracy.setter
    def average_accuracy(self, accuracy: float):
        """
        Sets the average accuracy score.

        Parameters
        ----------
            accuracy: float
                The average accuracy to set.
        """
        self._average_accuracy = accuracy

    @property
    def angles_mae(self) -> list:
        """
        Attribute to access the mean absolute error of the pose angles.
        Can only be set to :py:class:`list`

        Returns
        -------
            :py:class:`list`
                This contains the mean absolute error of the pose angles.
        """
        return self._angles_mae

    @angles_mae.setter
    def angles_mae(self, data: list):
        """
        Sets the data for the mean absolute error of the pose angles.

        Parameters
        ----------
            data: :py:class:`list`
                These are the mean absolute error of the pose angles to set.
        """
        self._angles_mae = data

    @property
    def timings(self) -> dict:
        """
        Attribute to access the model timings.
        Can only be set to :py:class:dict.

        Returns
        -------
            :py:class:dict: The model timings.
        """
        return self._timings

    @timings.setter
    def timings(self, this_timings: Union[dict, None]):
        """
        Sets the timings of the model.

        Parameters
        ----------
            this_timings: dict
                The model timings.

        Raises
        ------
            ValueError
                This error is raised if the dictionary does not contain
                the expected keys.
        """
        if isinstance(this_timings, dict) and not all(key in this_timings.keys()
                                                      for key in ["min_inference_time",
                                                                  "max_inference_time",
                                                                  "min_input_time",
                                                                  "max_input_time",
                                                                  "min_decoding_time",
                                                                  "max_decoding_time",
                                                                  "avg_inference",
                                                                  "avg_input",
                                                                  "avg_decoding",]):
            raise ValueError(
                f"The following keys are expected: {this_timings.keys()}")
        self._timings = this_timings

    def reset(self):
        self._save_path = None
        self._image_summaries = list()
        self._ground_truths = 0
        # This is used for segmentation total number of prediction pixels.
        self._predictions = 0

        """Detection Summaries"""
        self._true_positives = 0
        self._false_negatives = 0
        self._classification_false_positives = 0
        self._localization_false_positives = 0
        self._overall_precision = np.nan
        self._overall_recall = np.nan
        self._overall_accuracy = np.nan

        self._map = {
            "0.50": np.nan,
            "0.75": np.nan,
            "0.50:0.95": np.nan,
        }

        self._mar = {
            "0.50": np.nan,
            "0.75": np.nan,
            "0.50:0.95": np.nan,
        }

        self._macc = {
            "0.50": np.nan,
            "0.75": np.nan,
            "0.50:0.95": np.nan,
        }

        self._classification_fp_error = {
            "0.50": np.nan,
            "0.75": np.nan,
            "0.50:0.95": np.nan,
        }

        self._localization_fp_error = {
            "0.50": np.nan,
            "0.75": np.nan,
            "0.50:0.95": np.nan,
        }

        self._append_centers = False
        self._mae_centers = {
            "x-center-mae": np.nan,
            "y-center-mae": np.nan,
            "z-center-mae": np.nan,
            "distance-mae": np.nan,
        }

        """Segmentation Summaries"""
        self._true_predictions = 0
        self._false_predictions = 0
        self._union = 0
        self._average_precision = np.nan
        self._average_recall = np.nan
        self._average_accuracy = np.nan

        """Pose Summaries"""
        self._angles_mae = list()

        self._timings = {
            "min_inference_time": None,
            "max_inference_time": None,
            "min_input_time": None,
            "max_input_time": None,
            "min_decoding_time": None,
            "max_decoding_time": None,
            "avg_inference": None,
            "avg_input": None,
            "avg_decoding": None,
        }


class PlotSummary:
    """
    This is a class to store the data for the plots.
    """

    def __init__(self) -> None:
        self._class_histogram_data = dict()

        """Confusion Matrix Data"""
        self._confusion_matrix_data = list()
        self._confusion_labels = list()
        self._confusion_matrix = np.array(list())

        """Precision Recall Curve"""
        self._precision = np.array(list())
        self._recall = np.array(list())
        self._average_precision = np.array(list())
        self._curve_labels = list()

    @property
    def class_histogram_data(self) -> dict:
        """
        Attribute to access the class histogram data.
        Can only be set to :py:class:`dict`

        Returns
        -------
            :py:class:`dict`
                This contains the data for the class histogram.
        """
        return self._class_histogram_data

    @class_histogram_data.setter
    def class_histogram_data(self, data: dict):
        """
        Sets the data for the class histogram to a new value.

        Parameters
        ----------
            data: :py:class:`dict`
                These are the class histogram data to set. This should
                be a dictionary with the following keys:

                {
                    "precision": precision,
                    "recall": recall,
                    "accuracy": accuracy,
                    "tp": tp,
                    "fn": fn,
                    "fp": fp,
                    "gt": gt
                }
        """
        self._class_histogram_data = data

    def append_class_histogram_data(self, label: str, data: dict):
        """
        This adds another key to the class histogram data indicated as the
        class label and data contains the metrics of that label.

        Parameters
        ----------
            label: str
                This is the key of the dictionary that is the class label.

            data: dict
                This contains the metrics of the label. This should
                be a dictionary with the following keys::

                    .. code-block:: python

                        {
                            "precision": precision,
                            "recall": recall,
                            "accuracy": accuracy,
                            "tp": tp,
                            "fn": fn,
                            "fp": fp,
                            "gt": gt
                        }
        """
        self._class_histogram_data[label] = data

    @property
    def confusion_matrix_data(self) -> List[tuple]:
        """
        Attribute to access the confusion matrix data.
        Can only be set to :py:class:`list`

        Returns
        -------
            :py:class:`list`
                This contains the data for the confusion matrix.
        """
        return self._confusion_matrix_data

    @confusion_matrix_data.setter
    def confusion_matrix_data(self, data: List[tuple]):
        """
        Sets the data for the confusion matrix to a new value.

        Parameters
        ----------
            data: :py:class:`list`
                These are the confusion matrix data to set.

                This data should be formatted as the following:
                [(gt_label, dt_label), (gt_label, dt_label), ...]
        """
        self._confusion_matrix_data = data

    @property
    def confusion_labels(self) -> list:
        """
        Attribute to access the confusion matrix unique labels.
        Can only be set to :py:class:`list`

        Returns
        -------
            :py:class:`list`
                This contains the labels for the confusion matrix.
        """
        return self._confusion_labels

    @confusion_labels.setter
    def confusion_labels(self, labels: list):
        """
        Sets the labels for the confusion matrix to a new value.

        Parameters
        ----------
            labels: :py:class:`list`
                These are the confusion matrix labels to set.
        """
        self._confusion_labels = labels

    @property
    def confusion_matrix(self) -> np.ndarray:
        """
        Attribute to access the confusion matrix.
        Can only be set to :py:class:`np.ndarray`

        Returns
        -------
            :py:class:`np.ndarray`
                This contains the confusion matrix.
        """
        return self._confusion_matrix

    @confusion_matrix.setter
    def confusion_matrix(self, labels: np.ndarray):
        """
        Sets the confusion matrix to a new value.

        Parameters
        ----------
            labels: :py:class:`np.ndarray`
                These are the confusion matrix to set.
        """
        self._confusion_matrix = labels

    def append_confusion_matrix_data(self, datum: tuple):
        """
        This appends the (gt_label, dt_label) datum for the confusion matrix.

        Parameters
        ----------
            datum: tuple
                One data point for the confusion matrix (gt_label, dt_label)
                where gt_label is the ground truth class and dt_label is 
                the prediction class. The tuple represents the matched 
                detection to ground truth. 
        """
        self.confusion_matrix_data.append(datum)

    def tabularize_confusion_matrix(self):
        """
        This converts the confusion matrix data in a numpy table where the
        rows will contain the prediction labels and the columns contain the
        ground truth labels.

        Returns
        -------
            confusion_matrix: (nxn) np.ndarray
                The confusion matrix as a table.
        """
        # Unique items in the data.
        chain = list(sum(self.confusion_matrix_data, ()))
        # This should always contain background to describe
        # false negatives and localization false positives.
        self.confusion_labels = list(set(chain))
        # Move background class to the beginning of the list.
        if "background" in self.confusion_labels:
            self.confusion_labels.remove("background")
        self.confusion_labels.insert(0, "background")

        # The confusion matrix will have rows as the
        # predictions and columns as the ground truth.
        self.confusion_matrix = np.zeros(
            (len(self.confusion_labels), len(self.confusion_labels)))
        for datum in self.confusion_matrix_data:
            gt_index = self.confusion_labels.index(datum[0])
            dt_index = self.confusion_labels.index(datum[1])
            self.confusion_matrix[dt_index][gt_index] += 1

    @property
    def precision(self) -> np.ndarray:
        """
        Attribute to access the array of precision values. 
        Can only be set to :py:class:`np.ndarray`

        Returns
        -------
            :py:class:`np.ndarray`
                This contains the data for the precision recall curve.
        """
        return self._precision

    @precision.setter
    def precision(self, data: np.ndarray):
        """
        Sets the data for the precision values.

        Parameters
        ----------
            data: :py:class:`np.ndarray`
                These are the precision values to set.

                This data should be formatted as the following:
                (nc x thresholds) so each row are for a unique class and 
                each column is the precision value for each score threshold.
        """
        self._precision = data

    @property
    def recall(self) -> np.ndarray:
        """
        Attribute to access the array of recall values. 
        Can only be set to :py:class:`np.ndarray`

        Returns
        -------
            :py:class:`np.ndarray`
                This contains the data for the precision recall curve.
        """
        return self._recall

    @recall.setter
    def recall(self, data: np.ndarray):
        """
        Sets the data for the recall values.

        Parameters
        ----------
            data: :py:class:`np.ndarray`
                These are the recall values to set.

                This data should be formatted as the following:
                (nc x thresholds) so each row are for a unique class and 
                each column is the recall value for each score threshold.
        """
        self._recall = data

    @property
    def average_precision(self) -> np.ndarray:
        """
        Attribute to access the array of average_precision values. 
        Can only be set to :py:class:`np.ndarray`

        Returns
        -------
            :py:class:`np.ndarray`
                This contains the data for the precision recall curve.
        """
        return self._average_precision

    @average_precision.setter
    def average_precision(self, data: np.ndarray):
        """
        Sets the data for the average_precision values.

        Parameters
        ----------
            data: :py:class:`np.ndarray`
                These are the average_precision values to set.

                This data should be formatted as the following:
                (nc x 10) so each row are for a unique class and 
                each column is the precision at 10 different IoU threshold from
                0.50 to 0.95 in 0.05 intervals with a static score threshold
                set from the command line.
        """
        self._average_precision = data

    @property
    def curve_labels(self) -> list:
        """
        Attribute to access the precision recall curve unique labels.
        Can only be set to :py:class:`list`

        Returns
        -------
            :py:class:`list`
                This contains the labels for the precision recall curve.
        """
        return self._curve_labels

    @curve_labels.setter
    def curve_labels(self, labels: list):
        """
        Sets the labels for the precision recall curve to a new value.

        Parameters
        ----------
            labels: :py:class:`list`
                These are the precision recall curve labels to set.
        """
        self._curve_labels = labels

    def reset(self):
        """
        Resets the containers for the data use to plot.
        """
        self._class_histogram_data = dict()
        self._confusion_matrix_data = list()

        self._precision = np.array(list())
        self._recall = np.array(list())
        self._average_precision = np.array(list())