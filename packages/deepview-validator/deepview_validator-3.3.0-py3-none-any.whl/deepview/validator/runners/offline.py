# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.exceptions import UnsupportedAnnotationFormatException
from deepview.validator.exceptions import UnsupportedValidationTypeException
from deepview.validator.metrics.segmentationutils import create_mask_image
from deepview.validator.datasets.core import Dataset
from deepview.validator.runners.core import Runner
from deepview.validator.datasets import Instance
from typing import Tuple, Union
import numpy as np
import warnings
import json
import os

class OfflineRunner(Runner):
    """
    Reads model detection annotations stored that are in YOLO format. 
    For more information on the Yolo format visit:: \
        https://support.deepviewml.com/hc/en-us/articles/10869801702029
    Also reads model pose annotations in JSON files.
    For more information on the JSON pose annotations visit:: \
        https://support.deepviewml.com/hc/en-us/articles\
            /15626078040973-Headpose-dataset-format-for-ModelPack

    *Note: These text files should also include the model prediction scores \
        which adds to the Yolo format: [cls score xc yc width height].*

    Use Case: PT models are ran using https://github.com/ultralytics/yolov5 
    repository. These model predictions will be stored in TXT files that 
    are in Yolo format. will read the text files to be validated.

    Parameters
    ----------
        annotation_source: str
            This is the path to the model prediction annotations
            stored in text files with yolo format annotations.
            [cls score xc yc width height].

        labels: list
            This contains the unique string labels in the dataset.

        validate_type: str
            This is the validation type being performed: detection, 
            segmentation or pose. 

        validate_3d: bool
            This is to specify whether or not to perform 3D detection
            validation.

        format: str
            Specify the format of the annotations (yolo, coco, pascalvoc).

        label_offset: int
            The index offset to match label index to the ground truth index.

    Raises
    ------
        UnsupportedAnnotationFormatException
            Raised if the annotation format passed
            is not recognized.

        NonMatchingIndexException
            Raised if the model outputs an index
            that is out of bounds to the labels list passed.

        UnsupportedValidationTypeException
            Raised if the provided validation type is not 
            recognized.
    """
    def __init__(
        self,
        annotation_source: str,
        labels: list=None,
        validate_type: str="detection",
        validate_3d: bool=False,
        format: str='yolo',
        label_offset: int=0
    ):
        super(OfflineRunner, self).__init__(annotation_source, labels=labels)

        self.loaded_model = None
        self.label_offset = label_offset
        self.validate_3d = validate_3d

        self.define_denormalizer(validate_type)
        self.define_transformer(format)
        self.define_annotation_extension()

    def define_denormalizer(self, validate_type: str):
        """
        This defines a denormalizer if the validation type is segmentation
        which requires denormalizing polygon coordinates to be translated into
        segmentation masks.

        Parameters
        ----------
            validate_type: str
                This is the validation type of either "detection", 
                "segmentation", or "pose".

        Raises
        ------
            UnsupportedValidationTypeException
                Raised if the provided validation type is not 
                recognized.
        """
        self.validate_type = validate_type.lower()
        if self.validate_type not in ["detection", "segmentation", "pose"]:
            raise UnsupportedValidationTypeException(self.validate_type)
        
        self.denormalizer = None
        if validate_type == 'segmentation':
            self.denormalizer = Dataset.denormalize_polygon

    def define_transformer(self, format: str):
        """
        This defines the annotation transformer from yolo to pascalvoc or
        coco to pascalvoc as validator processes annotations in pascalvoc
        by default.

        Parameters
        ---------- 
            format: str
                The annotation format either in "yolo", "pascalvoc", or "coco".

        Raises
        ------  
            UnsupportedAnnotationFormatException
                Raised if the annotation format passed
                is not recognized.
        """
        self.format = format.lower()
        if self.format not in ['yolo', 'pascalvoc', 'coco']:
            raise UnsupportedAnnotationFormatException(self.format)
        
        if self.format == 'yolo':
            self.transformer = Dataset.yolo2xyxy
        elif self.format == 'coco':
            self.transformer = Dataset.xywh2xyxy
        else:
            self.transformer = None

    def define_annotation_extension(self):
        """
        Depending on the validation type, annotation extensions varies
        where detection is in text files for 2D validation and json files
        for 3D validation. Similarly, for pose and segmentation, the 
        annotations are stored in json files.
        """
        if self.validate_type == "detection":
            if self.validate_3d:
                self.annotation_extension = "json"
            else:
                self.annotation_extension = "txt"
        else:
            self.annotation_extension = "json"

    def run_single_instance(self, image: str):
        """
        Reads one prediction annotation file based on the 
        image name and returns the bounding boxes and 
        labels for detection, or the angles for pose, 
        or the mask for segmentation.

        Parameters
        ----------
            image: str
                The path to the image. This is used to match the
                annotation to be read.

        Returns
        -------
            * 2D Detection \
                boxes: np.ndarray
                    The prediction bounding boxes.. [[box1], [box2], ...].

                classes: np.ndarray
                    The prediction labels.. [cl1, cl2, ...].

                scores: np.ndarray
                    The prediction confidence scores.. [score, score, ...]
                    normalized between 0 and 1.

            * 3D Detection \
                centers: np.ndarray
                    This contains the [x,y,z] bounding box centers.

                sizes: np.ndarray
                    This contains the [width, height, length] 
                    of the bounding box sizes.

                angles: np.ndarray
                    This contains the bounding box heading angles 
                    (yaw heading in radians).

                view: np.ndarray
                    (3x4) np.array calibration matrix for the bounding box.

                labels: np.ndarray
                    This contains the detection labels of each bounding box.

                scores: np.ndarray
                    This contains the detection scores of each bounding box.

            * Pose: \
                angles: list
                    [roll, pitch, yaw].

            * segmentation: \
                    dt_mask: np.ndarray
                        This is the same resolution as the image with 
                        container integers per element depending 
                        on the label to represent each pixel. 

        Raises
        ------
            NonMatchingIndexException
                Raised if the model outputs an index
                that is out of bounds to the labels list passed.

            ValueError
                Raised if the provided image is not a
                string path pointing to the image.

            UnsupportedValidationTypeException
                Raised if the provided validation type is not 
                recognized.
        """
        if isinstance(image, str):
            annotation_path = os.path.join(self.model, "{}.{}".format(
                os.path.splitext(os.path.basename(image))[0], 
                self.annotation_extension))
        else:
            raise ValueError(
                "The provided image needs to be a string path pointing " +
                "to the image. Provided with type: {}".format(type(image)))

        annotation = self.get_annotation(annotation_path)
        if self.validate_type == "detection":
            if self.validate_3d:
                return self.process_3d_detection(annotation)
            else:
                return self.process_detection(annotation)
        elif self.validate_type == "pose":
            return self.process_pose(annotation)
        
        elif self.validate_type == "segmentation":
            return self.process_segmentation(annotation)
        else:
            raise UnsupportedValidationTypeException(self.validate_type)
    
    def get_annotation(
            self, annotation_path: str) -> Union[Union[np.ndarray, dict], None]:
        """
        Reads the annotatation path provided to get 
        the information stored in the file.

        Parameters
        ----------
            annotation_path: str
                This is the path to the annotation file.

        Returns
        -------
            annotation: np.ndarray
                For detection in the following format:
                [[cls, score, xc, yc, width, height], [...], [...], ...].

            annotation: dict
                For 3D detection.

                    .. code-block:: python

                        {
                            "boxes": 2D bounding boxes with labels,
                            "3d-boxes": Contains size and centers for 3D bounding boxes,
                            "calibration": (3x4) np.array calibration matrix,
                            "angles": 3D bounding box heading angles (yaw heading in radians),
                        }       
                
                For segmentation.
                
                    .. code-block:: python
                        
                        {
                            "dimension": [height, width],
                            "segment": [[[x, y], [x,y], ...], [...]] 
                            "labels": [int, int, int ...] 
                        }
                
                For pose.
                
                    .. code-block:: python

                        {
                            "angles": [[roll, pitch, yaw]]
                        }                         
        """
        try:
            if self.validate_type == "detection" and not self.validate_3d:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    return np.genfromtxt(annotation_path)
            # 3D detection, segmentation, pose
            with open(annotation_path, "r") as fp:
                return json.load(fp)
        except FileNotFoundError:
            return None

    def process_detection(
            self, 
            annotation: Union[np.ndarray, None]
        ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Parses the annotation to grab the detection bounding 
        boxes, scores, and labels.

        Parameters
        ----------
            annotation: np.ndarray
                [[cls, score, xc, yc, width, height], [...], [...], ...].

        Returns
        ------- 
            boxes: np.ndarray
                [[xmin, ymin, xmax, ymax], [...], ...]
            
            labels: np.ndarray
                [label, label, label, ...]

            scores: np.ndarray
                [score, score, score, ...]
        
        Raises
        ------
            NonMatchingIndexException
                Raised if the model outputs an index
                that is out of bounds to the labels list passed.
        """
        if annotation is None:
            return np.array([]), np.array([]), np.array([])
        
        if len(annotation):
            annotation = annotation.reshape(-1, 6)
            boxes = annotation[:, 1:5]
            boxes = self.transformer(boxes) if self.transformer else boxes
        else:
            return np.array([]), np.array([]), np.array([])

        scores = annotation[:, 5:6].flatten().astype(np.float32)
        labels = annotation[:, 0:1].flatten().astype(np.int32) + self.label_offset
        labels = self.index2string(labels)
        return boxes, labels, scores
    
    def process_3d_detection(
            self, 
            annotation: Union[dict, None]
        ) -> Tuple[
            np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Parses the annotation to retrieve 3D bounding box information for
        the detections.

        Parameters
        ----------
            annotation: dict

                .. code-block:: python

                    {
                        "boxes": 2D bounding boxes with labels,
                        "3d-boxes": Contains size and centers for 3D bounding boxes,
                        "calibration": (3x4) np.array calibration matrix,
                        "angles": 3D bounding box heading angles (yaw heading in radians),
                    }          
        
        Returns
        -------
            centers: np.ndarray
                This contains the [x,y,z] bounding box centers.

            sizes: np.ndarray
                This contains the [width, height, length] 
                of the bounding box sizes.

            angles: np.ndarray
                This contains the bounding box heading angles 
                (yaw heading in radians).

            view: np.ndarray
                (3x4) np.array calibration matrix for the bounding box.

            labels: np.ndarray
                This contains the detection labels of each bounding box.

            scores: np.ndarray
                This contains the detection scores of each bounding box.
        """
        if annotation is None:
            return np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([])

        angles = np.array(annotation.get("angles")).flatten()
        boxes_3d = np.array(annotation.get("3d-boxes"))
        if len(boxes_3d) == 0 and len(angles) == 0:
            return np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([])
        
        centers = boxes_3d[:, 0:3]
        sizes = boxes_3d[:, 3:6]
        view = np.array(annotation.get("calibration"))
        boxes = np.array(annotation.get("boxes"))
        labels = boxes[:, 4:5].flatten().astype(np.int32) + self.label_offset
        labels = self.index2string(labels)
        
        # This needs to be refactored to actual model scores in the future.
        scores = np.ones(len(labels))
        return centers, sizes, angles, view, labels, scores
    
    def process_pose(
            self, annotation: Union[dict, None]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Parses the annotation to get the euler angles.

        Parameters
        ----------
            annotation: dict

                .. code-block:: python

                    {
                        "angles": [[roll, pitch, yaw]]
                    }                         

        Returns
        -------
            angles: np.ndarray
                [roll, pitch, yaw]
            
            labels: np.ndarray
                The label representing each set of angles.
        """
        if annotation is None:
            return np.array([]), np.array([])
        return np.ndarray(annotation.get("angles")[0]), self.labels
    
    def process_segmentation(self, annotation: Union[dict, None]) -> np.ndarray:
        """
        Parses the annotations to get the segments and 
        create the detection mask.

        Parameters
        ----------
            annotation: dict

                .. code-block:: python
                        
                        {
                            "dimension": [width, height],
                            "segment": [[[x, y], [x,y], ...], [...]] 
                            "labels": [int, int, int ...] 
                        }
        
        Returns
        -------
            dt_mask: np.ndarray
                This is the same resolution as the image with 
                container integers per element depending on the label to
                represent each pixel. 
        """
        if annotation is None:
            return annotation
        
        width, height = annotation.get("dimension")
        dt_mask = np.zeros((height, width))
        try:
            segments, labels = list(), list()
            for segment in annotation.get("segment"):
                for polygon in segment:
                    cls = polygon["class"]
                    poly = polygon["polygon"]
                    # label_offset should be 1 if there is a background class.
                    labels.append(cls+self.label_offset)
                    # a list of vertices
                    x_y = []
                    for vertex in poly:
                        vertex = self.denormalizer(
                            vertex, height, width) if \
                            self.denormalizer else vertex
                        x_y.append(float(vertex[0]))
                        x_y.append(float(vertex[1]))
                    segments.append(x_y)
        except KeyError:
            return dt_mask
        
        dt_instance = Instance("Sample")
        dt_instance.polygons = segments
        dt_instance.labels = labels
        return create_mask_image(height, width, dt_instance)