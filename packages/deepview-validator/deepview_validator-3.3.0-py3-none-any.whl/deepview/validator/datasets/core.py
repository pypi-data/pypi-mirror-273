# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.exceptions import UnsupportedAnnotationFormatException
from typing import Union, List
import numpy as np

class Dataset:
    """
    Contains transformation methods for both images and annotations.
    Images can be resized and annotations can be normalized or denormalized. 
    Annotations can be converted to specific formats (yolo, coco, pascalvoc). 
    More information can be found on the annotation formats: 
    https://support.deepviewml.com/hc/en-us/articles/10869801702029-Darknet-Ground-Truth-Annotations-Schema

    Parameters
    ----------
        source: str
            The path to the source dataset.

        gformat: str
            The annotation format (yolo, pascalvoc, coco).

        absolute: bool
            If true, then the annotations are not normalized.

        validate_type: str
            Can be either 'detection', 'segmentation' or 'pose'.

    Raises
    ------
        UnsupportedAnnotationFormatException
            Raised if the provided annotation format is not identified.

        ValueError
            Raises are caused if the provided parameters
            in certain methods does not conform to the specified data type.
    """

    def __init__(
        self,
        source: str,
        gformat: str = "yolo",
        absolute: bool = False,
        validate_type: str = "detection",
    ):
        self.source = source
        self.format = gformat.lower()
        self.absolute = absolute
        self.validate_type = validate_type.lower()
        self._labels = list()

        if self.format not in ['yolo', 'pascalvoc', 'coco']:
            raise UnsupportedAnnotationFormatException(self.format)
        
        self.transformer = None
        if self.format == 'yolo':
            self.transformer = self.yolo2xyxy
        elif self.format == 'coco':
            self.transformer = self.xywh2xyxy
        else:
            self.transformer = None

        self.normalizer = None
        self.denormalizer = None
        if absolute:
            if validate_type.lower() == 'detection':
                self.normalizer = self.normalize
        else:
            if validate_type.lower() == 'segmentation':
                self.denormalizer = self.denormalize_polygon

    @property
    def labels(self) -> List[str]:
        """
        Attribute to access the unique string labels.
        Can be set to :py:class:`list`.

        Returns
        -------
            :py:class:`list` of strings
                This contains the unique string labels.
        """
        return self._labels

    @labels.setter
    def labels(self, new_labels: List[str]):
        """
        Sets the labels to a new value.

        Parameters
        ----------
            new_labels: :py:class:`list`.
                These are the unique string labels in the dataset to set.
        """
        self._labels = new_labels

    @staticmethod
    def convert_labels(
        labels: List[str],
        labels_to_convert: Union[list, np.ndarray],
        label_offset: int = 0
    ) -> list:
        """
        Converts integer lables in string labels.

        Parameters
        ----------
            labels: list or np.ndarray
                This contains the string labels that will be used to map
                integer labels to string.

            labels_to_convert: list or np.ndarray
                This is the labels for the ground truth annotation on a single
                image presumed to be integers.

        Returns
        -------
            labels: list
                A list on containing string representations.
        """
        if all(isinstance(label, str) for label in labels_to_convert):
            return labels_to_convert
        return [labels[int(label)+label_offset].lower() for
                label in labels_to_convert]

    @staticmethod
    def bgr2rgb(image: np.ndarray) -> np.ndarray:
        """
        Converts BGR image to RGB image.

        Parameters
        ----------
            image: (height, width, 3) np.ndarray
                The image as a BGR numpy array.

        Returns
        -------
            image: (height, width, 3) np.ndarray
                The image as a RGB image.
        """
        return image[:, :, ::-1]

    @staticmethod
    def rgb2bgr(image: np.ndarray) -> np.ndarray:
        """
        This method converts RGB image to BGR image.

        Parameters
        ----------
            image: (height, width, 3) np.ndarray
                The image as a RGB numpy array.

        Returns
        -------
            image: (height, width, 3) np.ndarray
                The image as a BGR image.
        """
        return image[:, :, ::-1]

    @staticmethod
    def normalize(boxes: np.ndarray, height: int, width: int) -> np.ndarray:
        """
        Normalizes the boxes to the width and height of the 
        image or model input resolution.

        Parameters
        ----------
            boxes: np.ndarray
                List of lists of floats [[boxes1], [boxes2]].
                Contains boxes to normalize.

            height: int
                The dimension to normalize the y-coordinates.

            width: int
                The dimension to normalize the x-coordinates.

        Returns
        -------
            Normalized boxes: np.ndarray
                new x-coordinate = old x-coordinate/width
                new y-coordinate = old y-coordinate/height
        """
        if isinstance(boxes, list):
            boxes = np.array(boxes)
        boxes[..., 0:1] /= width
        boxes[..., 1:2] /= height
        boxes[..., 2:3] /= width
        boxes[..., 3:4] /= height
        return boxes

    @staticmethod
    def denormalize(boxes: np.ndarray, height: int, width: int) -> np.ndarray:
        """
        Denormalizes the boxes by the width and height of the image 
        or model input resolution to get the pixel values of the boxes.

        Parameters
        ----------
            boxes: np.ndarray
                List of lists of floats [[boxes1], [boxes2]].
                Contains boxes to denormalize.

            height: int
                The dimension to denormalize the y-coordinates.

            width: int
                The dimension to denormalize the x-coordinates.

        Returns
        -------
            Denormalized boxes: np.ndarray
                new x-coordinate = old x-coordinate*width
                new y-coordinate = old y-coordinate*height
        """
        if isinstance(boxes, list):
            boxes = np.array(boxes)
        boxes[..., 0:1] *= width
        boxes[..., 1:2] *= height
        boxes[..., 2:3] *= width
        boxes[..., 3:4] *= height
        return boxes.astype(np.int32)

    @staticmethod
    def normalize_polygon(
            vertex: Union[list, np.ndarray], height: int, width: int):
        """
        Normalizes the vertex coordinate of a polygon.

        Parameters
        ----------
            vertex: list or Vector<2>
                This contains [x, y] coordinate.

            height: int
                The dimension to normalize the y-coordinates.

            width: int
                The dimension to normalize the x-coordinates.

        Returns
        -------
            normalized coordinates: list
                This contains [x, y].
        """
        return [float(vertex[0]) / width, float(vertex[1]) / height]

    @staticmethod
    def denormalize_polygon(
            vertex: Union[list, np.ndarray], height: int, width: int):
        """
        Denormalizes the vertex coordinate of a polygon.

        Parameters
        ----------
            vertex: list or Vector<2>
                This contains [x, y] coordinate.

            height: int
                The dimension to denormalize the y-coordinates.

            width: int
                The dimension to denormalize the x-coordinates.

        Returns
        -------
            Denormalized coordinates: list
                This contains [x, y].
        """
        return [int(float(vertex[0])*width), int(float(vertex[1])*height)]

    @staticmethod
    def yolo2xyxy(boxes: np.ndarray) -> np.ndarray:
        """
        Converts yolo format into pascalvoc format.

        Parameters
        ----------
            boxes: np.ndarray
                Contains lists for each boxes in
                yolo format [[boxes1], [boxes2]].

        Returns
        -------
            boxes: np.ndarray
                Contains list for each boxes in
                pascalvoc format.
        """
        w_c = boxes[..., 2:3]
        h_c = boxes[..., 3:4]
        boxes[..., 0:1] = boxes[..., 0:1] - w_c / 2
        boxes[..., 1:2] = boxes[..., 1:2] - h_c / 2
        boxes[..., 2:3] = boxes[..., 0:1] + w_c
        boxes[..., 3:4] = boxes[..., 1:2] + h_c
        return boxes

    @staticmethod
    def xywh2xyxy(boxes: np.ndarray) -> np.ndarray:
        """
        Converts coco format to pascalvoc format.

        Parameters
        ----------
            boxes: np.ndarray
                Contains lists for each boxes in
                coco format [[boxes1], [boxes2]].

        Returns
        -------
            boxes: np.ndarray
                Contains list for each boxes in
                pascalvoc format.
        """
        boxes[..., 2:3] = boxes[..., 2:3] + boxes[..., 0:1]
        boxes[..., 3:4] = boxes[..., 3:4] + boxes[..., 1:2]
        return boxes

    def build_dataset(self):
        """Abstract Method"""
        raise NotImplementedError("This is an abstract method.")

    def read_sample(self, instance):
        """Abstract Method"""
        raise NotImplementedError("This is an abstract method.")

    def read_all_samples(
            self, 
            info: str = "Validation Progress", 
            silent: bool=False
        ):
        """
        Reads all the samples in either Darknet or TFRecord datasets.

        Parameters
        ----------
            info: str
                The description of why image instances are being read.
                By default it is to run validation, 
                hence "Validation Progress".

            silent: bool
                If set to true, prevent validation logging.

        Returns
        -------
            ground truth instance: Instance
                Yeilds one sample of the ground truth
                instance which contains information on the image
                as a numpy array, boxes, labels, and image path.
        """
        if silent:
            samples = self.build_dataset()
            for sample in samples:
                yield self.read_sample(sample)
        else:
            try:
                from tqdm import tqdm
            except ImportError:
                pass

            try:
                samples = tqdm(self.build_dataset(), colour="green")
                samples.set_description(info)
                for sample in samples:
                    yield self.read_sample(sample)
            except NameError:
                samples = self.build_dataset()
                num_samples = len(samples)
                for index in range(num_samples):
                    print("\t - [INFO]: Computing metrics for image: " +
                          "%i of %i [%2.f %s]" %
                          (index + 1,
                           num_samples,
                           100 * ((index + 1) / float(num_samples)),
                           '%'), end='\r')
                    yield self.read_sample(samples[index])