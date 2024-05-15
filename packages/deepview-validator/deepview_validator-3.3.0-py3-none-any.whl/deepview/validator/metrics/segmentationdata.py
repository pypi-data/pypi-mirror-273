# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from typing import Union, List
import numpy as np

class SegmentationLabelData:
    """
    Acts a container that stores the total number of true predictions and
    false predictions for a specific label.

    Parameters
    ----------
        label: str or int
            The unique string or integer index label to base the container.
    """
    def __init__(self, label: Union[str, int, np.integer]):
        # The label being represented in this class.
        self._label = label
        # Total number of ground truth pixels of this label.
        self._ground_truths = 0
        # Total number of prediction pixels of this label.
        self._predictions = 0
        # Total number of both ground truths and predictions of this label.
        self._union = 0
        # Total number of true prediction pixels.
        self._true_predictions = 0
        # Total number of false prediction pixels.
        self._false_predictions = 0

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
    def predictions(self) -> int:
        """
        Attribute to access the number of predictions.
        Can only be set to :py:class:`int`

        Returns
        -------
            :py:class:`int`: The number of predictions for this label.
        """
        return self._predictions

    @predictions.setter
    def predictions(self, prd: int):
        """
        Sets the number of predictions for this label.

        Parameters
        ----------
            prd: int
                This is the number of predictions for this label.
        """
        self._predictions = prd

    def add_predictions(self, prd: int = 1):
        """
        Adds the number of existing predictions.

        Parameters
        ----------
            prd: int
                The number of predictions to add.
        """
        self._predictions += prd

    @property
    def union(self) -> int:
        """
        Attribute to access the number of union pixels.
        Can only be set to :py:class:`int`

        Returns
        -------
            :py:class:`int`: The number of union pixels for this label.
        """
        return self._union

    @union.setter
    def union(self, uni: int):
        """
        Sets the number of union pixels for this label.
        Union pixels is the sum total of both ground truths and predictions
        for this label.

        Parameters
        ----------
            uni: int
                This is the number of union pixels for this label.
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
    def true_predictions(self) -> int:
        """
        Attribute to access the number of true_predictions.
        Can only be set to :py:class:`int`

        Returns
        -------
            :py:class:`int`: The number of true_predictions for this label.
        """
        return self._true_predictions

    @true_predictions.setter
    def true_predictions(self, tps: int):
        """
        Sets the number of true_predictions for this label.

        Parameters
        ----------
            tps: int
                This is the number of true_predictions for this label.
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
            :py:class:`int`: The number of false_predictions for this label.
        """
        return self._false_predictions

    @false_predictions.setter
    def false_predictions(self, fps: int):
        """
        Sets the number of false_predictions for this label.

        Parameters
        ----------
            fps: int
                This is the number of false_predictions for this label.
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

class SegmentationDataCollection:
    """
    Acts as a container of SegmentationLabelData objects for each label 
    and provides methods to capture the total number of true predictions
    and false predictions pixels. 
    """
    def __init__(self):
        # A list containing the SegmentationDataLabel objects for each label.
        self._label_data_list = list()
        # A list containing the strings of unique labels.
        self.labels = list()

    @property
    def label_data_list(self) -> List[SegmentationLabelData]:
        """
        Attribute to access the list containing SegmentationLabelData objects
        Can only be set to :py:class:`list`

        Returns
        -------
            :py:class:`list`
                This contains the SegmentationLabelData objects.
        """
        return self._label_data_list

    @label_data_list.setter
    def label_data_list(self, label_datas: List[SegmentationLabelData]):
        """
        Sets the list of SegmentationLabelData objects.

        Parameters
        ----------
            label_datas: :py:class:`list`
                This is the list of SegmentationLabelData objects to set.
        """
        self._label_data_list = label_datas

    def add_label_data(self, label: Union[str, int, np.integer]):
        """
        Adds a SegmentationLabelData object for the label.

        Parameters
        ----------
            label: str or int
                The string label or the integer index to place as a data container.
        """
        self.label_data_list.append(SegmentationLabelData(label))

    def get_label_data(
        self,
        label: Union[str, int, np.integer]
    ) -> Union[SegmentationLabelData, None]:
        """
        Grabs the SegmentationLabelData object by label.

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
        label_data: SegmentationLabelData
        for label_data in self.label_data_list:
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

    def reset_containers(self):
        """
        Resets the label_data_list container to an empty list 
        and resets the labels captured to an empty list.
        """
        self._label_data_list, self._labels = list(), list()
        self._ground_truths = 0
        self._predictions = 0
        self._union = 0
        self._true_predictions = 0
        self._false_predictions = 0

    def capture_class(
        self,
        class_labels: Union[list, np.ndarray],
        labels: List[str] = None
    ):
        """
        Records the unique labels encountered in the prediction and 
        ground truth and creates a container (SegmentationLabelData) 
        for the label found in the model predictions and ground truth.

        Parameters
        ----------
            class_labels: list of int.
                All unique indices for the classes found from the ground
                truth and the model prediction masks.

            labels: list
                This list contains unique string labels for the classes found.
                This is optional to convert the integer labels into string
                labels.
        """
        for label in class_labels:
            if labels is not None:
                label: str = labels[label]
                if label.lower() in [" ", ""]:
                    continue
            if label not in self.labels:
                self.add_label_data(label)
                self.labels.append(label)