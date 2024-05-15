# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from typing import Union, List
import numpy as np

class PoseLabelData:
    """
    This is a container of angles for one specific angle 
    for both prediction and ground truth. An angle could be either yaw, 
    pitch, or roll.

    Parameters
    ----------
        label: str
            This is the angle name (Ex. roll, pitch, or yaw).
    """
    def __init__(self, label: Union[str, int, np.integer]):
        # The angle for this container.
        self._label = label
        # The true or ground truth angles.
        self._y_true = list()
        # The predicted angles.
        self._y_pred = list()

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
    def y_true(self) -> List[float]:
        """
        Attribute to access the ground truth angles.
        Can only be set to :py:class:`list`

        Returns
        -------
            :py:class:`list`
                This contains the ground truth angles.
        """
        return self._y_true
    
    @y_true.setter
    def y_true(self, this_y_true: List[float]):
        """
        Sets the ground truth angles to a new value.

        Parameters
        ----------
            this_y_true: :py:class:`list`
                These are ground truth angles to set.
        """
        self._y_true = this_y_true
    
    def add_y_true(self, angle: float):
        """
        Adds a ground truth angle to the ground truth list.

        Parameters
        ----------
            angle: float
                The ground truth angle.
        """
        self._y_true.append(angle)

    @property
    def y_pred(self) -> List[float]:
        """
        Attribute to access the prediction angles.
        Can only be set to :py:class:`list`

        Returns
        -------
            :py:class:`list`
                This contains the prediction angles.
        """
        return self._y_pred
    
    @y_pred.setter
    def y_pred(self, this_y_pred: List[float]):
        """
        Sets the prediction angles to a new value.

        Parameters
        ----------
            this_y_pred: :py:class:`list`
                These are prediction angles to set.
        """
        self._y_pred = this_y_pred

    def add_y_pred(self, angle: float):
        """
        Adds a predicted angle to the predicted list.

        Parameters
        ----------
            angle: float
                The model prediction angle.
        """
        self._y_pred.append(angle)

class PoseDataCollection:
    """
    This is a container for PoseLabelData objects which 
    contains angles for either roll, pitch, yaw.

    Raises
    ------
        ValueError
            Raised if the detected angle name was never stored as a
            container. Also if the lengths of ground truth and 
            prediction angles are not matching.   
    """
    def __init__(self) -> None:
        
        self._pose_data_list = list()
        self._angle_names = list()

    @property
    def pose_data_list(self) -> List[PoseLabelData]:
        """
        Attribute to access the list containing PoseLabelData objects
        Can only be set to :py:class:`list`

        Returns
        -------
            :py:class:`list`
                This contains the PoseLabelData objects.
        """
        return self._pose_data_list
    
    @pose_data_list.setter
    def pose_data_list(self, pose_datas: List[PoseLabelData]):
        """
        Sets the list of PoseLabelData objects.

        Parameters
        ----------
            pose_datas: :py:class:`list`
                This is the list of PoseLabelData objects to set.
        """
        self._pose_data_list = pose_datas

    def add_pose_data(self, label: Union[str, int, np.integer]):
        """
        Adds PoseLabelData object per label.
        
        Parameters
        ----------
            label: str or int
                The angle label to place as a data container. 
                Can be either 'roll', 'pitch', or 'yaw'.
        """
        self._pose_data_list.append(PoseLabelData(label))

    def get_pose_data(
            self, label: Union[str, int, np.integer]) -> Union[PoseLabelData, None]:
        """
        Grabs the PoseLabelData object by label.
        
        Parameters
        ----------
            label: str or int
                The name of the angle.

        Returns
        -------
            None if the object does not exist.

            pose_data: PoseLabelData
                The data container of the angle name specified.
        """
        for pose_data in self._pose_data_list:
            if pose_data.label == label:
                return pose_data
        return None
    
    @property
    def angle_names(self) -> list:
        """
        Attribute to access the list of unique angle names gathered.
        Can only be set to :py:class:`list`

        Returns
        -------
            :py:class:`list`
                This contains unique angle names gathered during validation.
        """
        return self._angle_names
    
    @angle_names.setter
    def angle_names(self, new_angle_names: list):
        """
        Sets the list of unique angle names gathered during validation.

        Parameters
        ----------
            new_angle_names: :py:class:`list`
                This is the list of unique angle names 
                gathered during validation.
        """
        self._angle_names = new_angle_names
    
    def reset_containers(self):
        """
        Resets the pose_data_list and the angle names captured
        into an empty list. 
        """
        self._pose_data_list, self._angle_names = list(), list()

    def capture_angle_names(self, name: Union[str, int, np.integer]):
        """
        Creates a PoseLabelData object based on the 
        provided angle name if it does not exist yet.
        
        Parameters
        ----------
            name: str or int
                The name of the angle.
        """
        if name not in self._angle_names:
            self.add_pose_data(name)
            self._angle_names.append(name)

    def store_angle(
            self, 
            name: Union[str, int, np.integer], 
            gt_angle: float,
            dt_angle: float 
        ):
        """
        Stores the angle in the object with the specified name.

        Parameters
        ----------
            name: str or int
                The name of the angle.

            gt_angle: float
                The ground truth angle. 

            dt_angle: float
                The prediction angle.

        Raises
        ------
            ValueError
                Raised if the detected angle name was never stored as a
                container.
        """
        pose_data = self.get_pose_data(name)
        if pose_data is None:
            raise ValueError(f"No PoseDataLabel container is associated with this angle: {name}")
        pose_data.add_y_pred(dt_angle)
        pose_data.add_y_true(gt_angle)

    def store_angles(
            self, 
            dt_angles: Union[list, np.ndarray], 
            gt_angles: Union[list, np.ndarray]):
        """
        Evaluates the lengths of the provided angles. 
        If it is three it assumes the angles are roll, pitch, and yaw. 
        If it is four, it assumes the angles are quaternion. 
        Also provides flexibility for other angle lengths, but names 
        them as angle_1, angle_2, etc..

        Parameters
        ----------
            dt_angles: list or np.ndarray
                An array that contains the detection angles.

            gt_angles: list or np.ndarray
                An array that contains the ground truth angles.

        Raises
        ------
            ValueError
                The lengths of ground truth and prediction angles are 
                not matching.       
        """
        if len(gt_angles) != len(dt_angles):
            raise ValueError("The lengths of the provided angles for " + 
                             "prediction and ground truth are not the same.")

        # Euler angles.
        if len(gt_angles) == 3:
            for name, dt_angle, gt_angle in zip(
                ["roll", "pitch", "yaw"], dt_angles, gt_angles):
                self.capture_angle_names(name)
                self.store_angle(name, gt_angle, dt_angle)

        # No angles were captured for both prediction and ground truth.
        elif len(gt_angles) == 0:
            for name in ["roll", "pitch", "yaw"]:
                self.capture_angle_names(name)
                self.store_angle(name, np.nan, np.nan)

        # Quaternion angles.
        elif len(gt_angles) == 4:
            for name, dt_angle, gt_angle in zip(
                ["real", "i", "j", "k"], dt_angles, gt_angles):
                self.capture_angle_names(name)
                self.store_angle(name, gt_angle, dt_angle)
        else:
            for i, (dt_angle, gt_angle) in enumerate(zip(dt_angles, gt_angles)):
                self.capture_angle_names("angle_{}".format(i))
                self.store_angle("angle_{}".format(i), gt_angle, dt_angle)