# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from typing import Union, List
import numpy as np

class Instance:
    """
    This is the instance object of an image that is used to store the image
    properties such as the dimensions and the path and also stores either
    the ground truth or the prediction bounding boxes (2D/3D), segmentation 
    polygons/masks, or pose angles.

    Parameters
    ----------
        image_path: str
            The path to the image for Darknet datasets. Otherwise this is the 
            image name for TFRecord datasets.
    """

    def __init__(
        self,
        image_path: str
    ) -> None:

        self._image_path = image_path
        # This is the numpy array image.
        self._image = None
        self._height = 0
        self._width = 0

        """Detection Properties"""
        # These are the 2D bounding boxes in either Yolo, Coco, or PascalVoc.
        self._boxes = list()
        # These contain either string or integer labels per bounding box.
        # These could also be the unique integer labels in the segmentation mask.
        self._labels = list()
        # These contain the prediction scores per bounding box. Empty if gt.
        self._scores = list()

        """Unfiltered properties are the original properties"""
        # These are the 2D bounding boxes in either Yolo, Coco, or PascalVoc.
        self._unfiltered_boxes = list()
        # These contain either string or integer labels per bounding box.
        self._unfiltered_labels = list()
        # These contain the prediction scores per bounding box. Empty if gt.
        self._unfiltered_scores = list()

        # These contain the 3D bounding box centers (x,y,z)
        self._centers = list()
        # These contain the 3D bounding box size (width, height, length)
        self._sizes = list()
        # These contain the angles to rotate the 3D bounding box in the y-axis.
        self._box_angles = list()
        # These contain the view calibration matrix for 
        # 3D bounding box conversion to corners.
        self._calibration = list()
        # These contain the 3D bounding box corners (3,8)
        self._corners = list()

        """Segmentation Properties"""
        # These contain the segmentation points to form the 
        # polygon shaped around the object.
        self._polygons = list()
        # This is the segmentation mask for the image.
        self._mask = None

        """Pose Properties"""
        # These contain the pose angles
        self._pose_angles = list()

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
    def image_path(self, path: str):
        """
        Sets the image path/name.

        Parameters
        ----------
            path: str
                The image path/name
        """
        self._image_path = path

    @property
    def image(self) -> np.ndarray:
        """
        Attribute to access the image.
        Can only be set to :py:class:`ndarray`

        Returns
        -------
            :py:class:`ndarray`: The image as a numpy array
        """
        return self._image

    @image.setter
    def image(self, this_image: np.ndarray):
        """
        Sets the image array.

        Parameters
        ----------
            image: np.ndarray
                The image array
        """
        self._image = this_image

    @property
    def height(self) -> int:
        """
        Attribute to access the image height in pixels.
        Can only be set to :py:class:`int`

        Returns
        -------
            :py:class:`int`: The image height in pixels. 0 means uninitialized.
        """
        return self._height

    @height.setter
    def height(self, image_height: int):
        """
        Sets the image height dimension to a new value.

        Parameters
        ----------
            image_height: int
                This is the new image height to set.
        """
        self._height = image_height

    @property
    def width(self) -> int:
        """
        Attribute to access the image width in pixels.
        Can only be set to :py:class:`int`

        Returns
        -------
            :py:class:`int`: The image width in pixels. 0 means uninitialized.
        """
        return self._width

    @width.setter
    def width(self, image_width: int):
        """
        Sets the image width dimension to a new value.

        Parameters
        ----------
            image_width: int
                This is the new image width to set.
        """
        self._width = image_width

    @property
    def boxes(self) -> Union[list, np.ndarray]:
        """
        Attribute to access the 2D bounding boxes for detection.
        Can be set to :py:class:`list` or :py:class:`ndarray` of float.

        Returns
        -------
            :py:class:`list` or :py:class:`ndarray` of float
                This contains the 2D normalized bounding boxes 
        """
        return self._boxes

    @boxes.setter
    def boxes(self, boxes_2d: Union[list, np.ndarray]):
        """
        Sets the 2D bounding boxes to a new value.

        Parameters
        ----------
            boxes_2d: :py:class:`list` or :py:class:`ndarray`
                These are the 2D bounding boxes to set.
        """
        self._boxes = boxes_2d

    def append_boxes(self, box: Union[list, np.ndarray]):
        """
        Appends list or stacks numpy array 2D bounding boxes.

        Parameters
        ----------
            box: list or np.ndarray
                This is the 2D normalized bounding box in either Yolo, Coco,
                or PascalVoc.
        """
        if isinstance(self._boxes, np.ndarray):
            self._boxes = np.vstack([self._boxes, box])
        else:
            self._boxes.append(box)

    @property
    def unfiltered_boxes(self) -> Union[list, np.ndarray]:
        """
        Attribute to access the unfiltered 2D bounding boxes for detection.
        Can be set to :py:class:`list` or :py:class:`ndarray` of float.

        Returns
        -------
            :py:class:`list` or :py:class:`ndarray` of float
                This contains the unfiltered 2D normalized bounding boxes 
        """
        return self._unfiltered_boxes

    @unfiltered_boxes.setter
    def unfiltered_boxes(self, boxes_2d: Union[list, np.ndarray]):
        """
        Sets the unfiltered 2D bounding boxes to a new value.

        Parameters
        ----------
            boxes_2d: :py:class:`list` or :py:class:`ndarray`
                These are the unfiltered 2D bounding boxes to set.
        """
        self._unfiltered_boxes = boxes_2d

    @property
    def labels(self) -> Union[list, np.ndarray]:
        """
        Attribute to access the labels per bounding box.
        Can be set to :py:class:`list` or 
        :py:class:`ndarray` of strings or integers.

        Returns
        -------
            :py:class:`list` or :py:class:`ndarray` of strings or integers
                This contains the labels per bounding box.
        """
        return self._labels

    @labels.setter
    def labels(self, new_labels: Union[list, np.ndarray]):
        """
        Sets the labels to a new value.

        Parameters
        ----------
            new_labels: :py:class:`list` or :py:class:`ndarray`
                These are the labels to set.
        """
        self._labels = new_labels

    @property
    def unfiltered_labels(self) -> Union[list, np.ndarray]:
        """
        Attribute to access the unfiltered labels per bounding box.
        Can be set to :py:class:`list` or 
        :py:class:`ndarray` of strings or integers.

        Returns
        -------
            :py:class:`list` or :py:class:`ndarray` of strings or integers
                This contains the unfiltered labels per bounding box.
        """
        return self._unfiltered_labels

    @unfiltered_labels.setter
    def unfiltered_labels(self, new_labels: Union[list, np.ndarray]):
        """
        Sets the unfiltered labels to a new value.

        Parameters
        ----------
            new_labels: :py:class:`list` or :py:class:`ndarray`
                These are the unfiltered labels to set.
        """
        self._unfiltered_labels = new_labels

    def append_labels(self, label: Union[str, int, np.integer]):
        """
        Appends list or appends numpy array label.

        Parameters
        ----------
            label: str or integer
                This is the label to append to the list.
        """
        if isinstance(self._labels, np.ndarray):
            self._boxes = np.append(self._boxes, label)
        else:
            self._boxes.append(label)

    @property
    def scores(self) -> Union[list, np.ndarray]:
        """
        Attribute to access the scores per bounding box.
        Can be set to :py:class:`list` or :py:class:`ndarray` of float.

        Returns
        -------
            :py:class:`list` or :py:class:`ndarray` of float
                This contains the scores per bounding box.
        """
        return self._scores

    @scores.setter
    def scores(self, new_scores: Union[list, np.ndarray]):
        """
        Sets the scores to a new value.

        Parameters
        ----------
            new_scores: :py:class:`list` or :py:class:`ndarray`
                These are the scores to set.
        """
        self._scores = new_scores

    @property
    def unfiltered_scores(self) -> Union[list, np.ndarray]:
        """
        Attribute to access the unfiltered scores per bounding box.
        Can be set to :py:class:`list` or :py:class:`ndarray` of float.

        Returns
        -------
            :py:class:`list` or :py:class:`ndarray` of float
                This contains the unfiltered scores per bounding box.
        """
        return self._unfiltered_scores

    @unfiltered_scores.setter
    def unfiltered_scores(self, new_scores: Union[list, np.ndarray]):
        """
        Sets the unfiltered scores to a new value.

        Parameters
        ----------
            new_scores: :py:class:`list` or :py:class:`ndarray`
                These are the unfiltered scores to set.
        """
        self._unfiltered_scores = new_scores

    def append_scores(self, score: float):
        """
        Appends list or appends numpy array scores.

        Parameters
        ----------
            score: float
                This is the score to append to the list.
        """
        if isinstance(self._scores, np.ndarray):
            self._scores = np.append(self._scores, score)
        else:
            self._scores.append(score)

    @property
    def centers(self) -> Union[list, np.ndarray]:
        """
        Attribute to access the centers per 3D bounding box.
        Can be set to :py:class:`list` or :py:class:`ndarray` of float.

        Returns
        -------
            :py:class:`list` or :py:class:`ndarray` of float
                This contains the centers per 3D bounding box in (x,y,z).
        """
        return self._centers

    @centers.setter
    def centers(self, new_centers: Union[list, np.ndarray]):
        """
        Sets the centers to a new value.

        Parameters
        ----------
            new_centers: :py:class:`list` or :py:class:`ndarray`
                These are the centers to set.
        """
        self._centers = new_centers

    @property
    def sizes(self) -> Union[list, np.ndarray]:
        """
        Attribute to access the sizes per 3D bounding box.
        Can be set to :py:class:`list` or :py:class:`ndarray` of float.

        Returns
        -------
            :py:class:`list` or :py:class:`ndarray` of float
                This contains the size per 
                3D bounding box in [width, height, length].
        """
        return self._sizes

    @sizes.setter
    def sizes(self, new_sizes: Union[list, np.ndarray]):
        """
        Sets the sizes to a new value.

        Parameters
        ----------
            new_size: :py:class:`list` or :py:class:`ndarray`
                These are the size to set.
        """
        self._sizes = new_sizes

    @property
    def box_angles(self) -> Union[list, np.ndarray]:
        """
        Attribute to access the angles per 3D bounding box.
        Can be set to :py:class:`list` or :py:class:`ndarray` of float.

        Returns
        -------
            :py:class:`list` or :py:class:`ndarray` of float
                This contains the angles per 3D bounding box in radians to 
                perform rotation around the y-axis. The y-axis would be 
                pointing upwards, the x-axis is either left/right, and the 
                z-axis is in/out of the page.
        """
        return self._box_angles

    @box_angles.setter
    def box_angles(self, new_box_angles: Union[list, np.ndarray]):
        """
        Sets the box_angles to a new value.

        Parameters
        ----------
            new_box_angles: :py:class:`list` or :py:class:`ndarray`
                These are the box_angles to set.
        """
        self._box_angles = new_box_angles

    @property
    def calibration(self) -> Union[list, np.ndarray]:
        """
        Attribute to access the calibration per 3D bounding box.
        Can be set to :py:class:`list` or :py:class:`ndarray` of float.

        Returns
        -------
            :py:class:`list` or :py:class:`ndarray` of float
                This contains the view matrix to transform 
                the 3D bounding box centers into respective 
                corners that can be drawn on the image.
        """
        return self._calibration

    @calibration.setter
    def calibration(self, new_calibration: Union[list, np.ndarray]):
        """
        Sets the calibration to a new value.

        Parameters
        ----------
            new_calibration: :py:class:`list` or :py:class:`ndarray`
                This is the calibration to set.
        """
        self._calibration = new_calibration

    @property
    def corners(self) -> Union[list, np.ndarray]:
        """
        Attribute to access the corners per 3D bounding box.
        Can be set to :py:class:`list` or :py:class:`ndarray` of float.

        Returns
        -------
            :py:class:`list` or :py:class:`ndarray` of float
                This contains the corners of the 3D bounding box with shape
                (3,8) representing the (x,y,z) 8 corners of a 3D box.

                The following points are:
                    P1: top, left, front corner
                    P2: top, right, front corner
                    P3: top, right, back corner
                    P4: top, left, back corner
                    P5: bottom, left, front corner
                    P6: bottom, right, front corner
                    P7: bottom, right, back corner
                    P8: bottom, left, back corner                
        """
        return self._corners

    @corners.setter
    def corners(self, new_corners):
        """
        Sets the corners to a new value.

        Parameters
        ----------
            new_corners: :py:class:`list` or :py:class:`ndarray`
                This is the corners to set.
        """
        self._corners = new_corners

    @property
    def polygons(self) -> Union[list, np.ndarray]:
        """
        Attribute to access the 2D points that form the polygon to shape
        around the object to form segmentation masks.
        Can be set to :py:class:`list` or :py:class:`ndarray` of float.

        Returns
        -------
            :py:class:`list` or :py:class:`ndarray` of float
                This contains the polygon points. Ex.
                [[[x1,y1], [x2,y2], ... ,[xn,yn]], [...], ...]           
        """
        return self._polygons

    @polygons.setter
    def polygons(self, new_polygons: Union[list, np.ndarray]):
        """
        Sets the polygons to a new value.

        Parameters
        ----------
            new_polygons: :py:class:`list` or :py:class:`ndarray`
                This is the polygons to set.
        """
        self._polygons = new_polygons

    @property
    def mask(self) -> np.ndarray:
        """
        Attribute to access the segmentation mask of the image.
        :py:class:`ndarray` of integers.

        Returns
        -------
            :py:class:`ndarray` of integers
                This contains the mask with the same dimensions as the image
                providing an integer label per pixel to represent the mask.         
        """
        return self._mask

    @mask.setter
    def mask(self, new_mask: np.ndarray):
        """
        Sets the mask to a new value.

        Parameters
        ----------
            new_mask: py:class:`ndarray`
                This is the mask to set.
        """
        self._mask = new_mask

    @property
    def pose_angles(self) -> Union[list, np.ndarray]:
        """
        Attribute to access the pose angles.
        Can be set to :py:class:`list` or :py:class:`ndarray` of float.

        Returns
        -------
            :py:class:`list` or :py:class:`ndarray` of float
                This contains the angles for pose in radians which is the
                [yaw, pitch, roll].
        """
        return self._pose_angles

    @pose_angles.setter
    def pose_angles(self, new_pose_angles: Union[list, np.ndarray]):
        """
        Sets the pose_angles to a new value.

        Parameters
        ----------
            new_pose_angles: :py:class:`list` or :py:class:`ndarray`
                These are the pose_angles to set.
        """
        self._pose_angles = new_pose_angles


class InstanceCollection:
    """
    This class is intended to contain the ground truth 
    and prediction instances. Furthermore, it will also contain 
    the gathered per image such as the 
    """

    def __init__(self) -> None:
        self._gt_instances = list()
        self._dt_instances = list()

    @property
    def gt_instances(self) -> List[Instance]:
        """
        Attribute to access the ground truth instance objects.
        Can only be set to :py:class:`list`

        Returns
        -------
            :py:class:`list`: Contains ground truth instance objects.
        """
        return self._gt_instances

    def append_gt_instance(self, instance: Instance):
        """
        Appends the ground truth instance in the gt_instances list.

        Parameters
        ----------
            instance: Instance
                The ground truth instance object.
        """
        self._gt_instances.append(instance)

    @property
    def dt_instances(self) -> List[Instance]:
        """
        Attribute to access the prediction instance objects.
        Can only be set to :py:class:`list`

        Returns
        -------
            :py:class:`list`: Contains prediction instance objects.
        """
        return self._dt_instances

    def append_dt_instance(self, instance: Instance):
        """
        Appends the prediction instance in the dt_instances list.

        Parameters
        ----------
            instance: Instance
                The prediction instance object.
        """
        self._dt_instances.append(instance)

    def reset(self):
        """
        Resets the collected instances to an empty list
        """
        self._gt_instances = list()
        self._dt_instances = list()