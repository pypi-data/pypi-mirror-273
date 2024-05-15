# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.datasets.instance import Instance
from deepview.validator.datasets.core import Dataset
from deepview.validator.datasets.utils import (
    classify_dataset, 
    validate_dataset_source, 
    read_image
)
from deepview.validator.datasets.utils import (
    get_image_files, 
    get_annotation_files
)
from deepview.validator.writers import logger
from typing import List, Tuple
from PIL import ImageFile
import numpy as np
import warnings
import json
import os

class DarkNetDataset(Dataset):
    """
    Reads Darknet format datasets.
    Dataset format should be the same as coco128 at 
    `https://www.kaggle.com/datasets/ultralytics/coco128`.
    Optionally, the images and text annotations can be in the same directory.

    Parameters
    ----------
        source: str
            The path to the source dataset.

        info_dataset: dict
            Contains information such as:

                .. code-block:: python

                    {
                        "classes": [list of unique labels],
                        "validation":
                        {
                            "images: 'path to the images',
                            "annotations": 'path to the annotations'
                        }
                    }

            *Note: the classes are optional and the path to the images
            and annotations can be the same.*

        gformat: str
            The annotation format that can be either 'yolo', 'pascalvoc',
            or 'coco'. By default darknet datasets have annotations in
            'yolo' format.

        absolute: bool
            Specify as True if the annotations are not normalized to the
            image dimensions. By default they are normalized.

        validate_type: str
            The type of validation to perform that can be 'detection',
            'segmentation', or 'pose'.

        validate_3d: bool
            Specify for 3D bounding box annotations.

        show_missing_annotations: bool
            If this is True, then print on the terminal all
            missing annotations. Else, it will only
            print the number of missing annotations.

        label_offset: int
            This is the offset of the ground truths indices to be mapped
            into string labels.

    Raises
    ------
        InvalidDatasetSourceException
            Raised if the path to the images or annotations is None.

        DatasetNotFoundException
            Raised if the provided path to the images or 
            annotations does not exist.

        ValueError
            Raised if the provided path to the images or 
            annotations is not a string.

        EmptyDatasetException
            Raised if the provided path to the images or 
            text files does not contain any image files or 
            text files respectively.
    """
    def __init__(
        self,
        source: str,
        info_dataset: dict=None,
        gformat: str="yolo",
        absolute: bool=False,
        validate_type: str="detection",
        validate_3d: bool=False,
        show_missing_annotations: bool=False,
        label_offset: int=0,
    ):
        ImageFile.LOAD_TRUNCATED_IMAGES = True

        super(DarkNetDataset, self).__init__(
            source=source,
            gformat=gformat,
            absolute=absolute,
            validate_type=validate_type,
        )
        self.show_missing_annotations = show_missing_annotations
        self.label_offset = label_offset
        self.validate_3d = validate_3d

        if info_dataset is None:
            info_dataset = classify_dataset(source)

        self.validate_type = validate_type.lower()

        try:
            images_path = info_dataset.get("dataset").get('validation').get('images')
            annotations_path = info_dataset.get("dataset").get('validation').get('annotations')
        except AttributeError:
            images_path = info_dataset.get('validation').get('images')
            annotations_path = info_dataset.get('validation').get('annotations')
        
        self.image_source = validate_dataset_source(images_path)
        self.annotation_source = validate_dataset_source(annotations_path)
        
        labels = info_dataset.get('classes', None)
        if labels is not None:
            self.labels = [str(label) for label in labels]
   
        self.images = get_image_files(self.image_source)
        self.annotations = get_annotation_files(self.annotation_source)

        # This is used to map the image name to the annotation file.
        self.annotation_extension = os.path.splitext(self.annotations[0])[1]

    def build_dataset(self) -> List[tuple]:
        """
        Builds the instances to allow iteration in the dataset.

        Returns
        -------
            instances: list of tuples
                One instance contains the
                (path to the image, path to the annotation).
        """
        missing_annotations = 0
        instances = list()
        for image_path in self.images:
            annotation_path = os.path.join(
                self.annotation_source,
                os.path.splitext(os.path.basename(image_path))[0] + 
                self.annotation_extension)
            
            if os.path.exists(annotation_path):
                instances.append((image_path, annotation_path))
            else:
                instances.append((image_path, None))
                if self.show_missing_annotations:
                    logger(
                        "Could not find the annotation " +
                        "for this image: {}. ".format(
                            os.path.basename(image_path)) +
                        "Looking for {}".format(
                            os.path.splitext(
                                os.path.basename(image_path))[0] +
                            self.annotation_extension),
                        code="WARNING")
                missing_annotations += 1
          
        if not self.show_missing_annotations and missing_annotations > 0:
            logger(
                "There were {} images without annotations. ".format(
                    missing_annotations) + "To see the names of the images, " +
                "enable --show_missing_annotations in the command line.",
                code="WARNING")
        return instances

    def read_sample(self, sample: Tuple[str, str]) -> Instance:
        """
        Reads one sample from the dataset.
        
        Parameters
        ----------
            sample: Tuple
                This contains (image path, annotation path).

        Returns
        -------
            ground truth instance: Instance
                The ground truth instance objects contains the bounding boxes
                and the labels representing the ground truth of the image.
        """
        image_path, annotation_path = sample
        image = read_image(image_path)
        height, width, _ = image.shape

        instance = Instance(image_path)
        instance.height = height
        instance.width = width
        instance.image = image
    
        if self.validate_type == 'detection':
            if self.validate_3d:
                annotations = self.read_3d_detection_json_file(annotation_path)
                instance.boxes = annotations.get("boxes")
                instance.centers = annotations.get("centers")
                instance.sizes = annotations.get("sizes")
                instance.box_angles = annotations.get("angles")
                instance.calibration = annotations.get("view")
                instance.labels = annotations.get("labels")
            else:
                annotations = self.read_text_files(annotation_path)
                instance.boxes = annotations.get("boxes")
                instance.labels = annotations.get("labels")
        elif self.validate_type == "segmentation":
            annotations = self.read_segmentation_json_file(
                annotation_path, height, width)
            instance.polygons = annotations.get("segments")
            instance.labels = annotations.get("labels")
        elif self.validate_type == "pose":
            annotations = self.read_pose_json_file(annotation_path)
            instance.boxes = annotations.get("boxes")
            instance.pose_angles = annotations.get("angles")
            instance.labels = annotations.get("labels")
        else:
            raise ValueError(
                "Invalid validation type: {}".format(self.validate_type))
        return instance

    def read_text_files(self, annotation_path: str) -> dict:
        """
        Reads the text file annotation to get the ground truth 
        bounding boxes and the labels.

        Parameters
        ----------
            annotation_path: str
                This is the path to the text file annotation.

        Returns
        -------
            annotation info: dict
                This contains information such as:

                    .. code-block:: python

                        {
                            'boxes': list of bounding boxes,
                            'labels': list of labels
                        }
        """
        annotations = {
            "boxes": np.array([]),
            "labels": np.array([]).astype(np.int32)
        }

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                annotation = np.genfromtxt(annotation_path)
        except TypeError:
            return annotations

        if len(annotation) > 0:
            annotation = annotation.reshape(-1, 5)
            boxes = annotation[:, 1:5]
            boxes = self.normalizer(boxes) if self.normalizer else boxes
            boxes = self.transformer(boxes) if self.transformer else boxes
            annotations["boxes"] = boxes
        else:
            return annotations

        labels = annotation[:, 0:1].flatten().astype(np.int32)
        # If there are string labels, 
        # then convert ground truth labels to strings.
        if self.labels is not None and len(self.labels) > 0:
            labels = self.convert_labels(
                self.labels, labels, self.label_offset)
        annotations["labels"] = labels   
        return annotations

    def read_detection_json_file(self, annotation_path: str) -> dict:
        """
        Reads from the JSON annotation to retrieve detection bounding boxes
        and labels.

        Parameters
        ----------
            annotation_path: str
                This is the path to the JSON annotation.

        Returns
        -------
            annotation info: dict
                This contains information such as:

                    .. code-block:: python

                        {
                            'boxes': list of bounding boxes,
                            'labels': list of labels
                        }
        """
        annotations = {
                "boxes": np.array([]),
                "labels": np.array([]).astype(np.int32)
            }

        try:
            with open(annotation_path) as file:
                data: dict = json.load(file)

            annotation = np.array(data.get("boxes"))
            annotation = self.normalizer(annotation) if self.normalizer else annotation
            boxes = self.transformer(annotation[:, 0:5]) if self.transformer else annotation[:, 0:5]
            
            labels = data.get("labels")
            # If there are string labels, 
            # then convert ground truth labels to strings.
            if len(self.labels):
                labels = self.convert_labels(
                    self.labels, labels, self.label_offset)

        # TypeError is due to the annotation path being None.
        except (FileNotFoundError, TypeError, KeyError):
            return annotations

        annotations["boxes"] = boxes
        annotations["labels"] = labels
        return annotations
    
    def read_3d_detection_json_file(self, annotation_path: str) -> dict:
        """
        Reads from the JSON annotation to retrieve 3D
        detection bounding boxes, angles, calibration, and labels.

        Parameters
        ----------
            annotation_path: str
                This is the path to the JSON annotation.

        Returns
        -------
            annotation info: dict
                This contains information such as:

                    .. code-block:: python

                        {
                            'boxes': list of 2D bounding boxes,
                            'centers': 3D bounding box centers (x,y,z),
                            'sizes': 3D bounding box sizes (w,h,l),
                            'angles': 3D bounding box heading angles (yaw heading in radians),
                            'view': (3x4) np.array calibration matrix,
                            'labels': list of labels
                        }
        """
        annotations = {
                "boxes": np.array([]),
                "centers": np.array([]),
                "sizes": np.array([]),
                "angles": np.array([]),
                "view": np.array([]),
                "labels": np.array([]).astype(np.int32)
            }
        
        try:
            with open(annotation_path) as file:
                data: dict = json.load(file)

            boxes_3d = np.array(data.get("3d-boxes"))
            angles = np.array(data.get("angles")).flatten()

            if len(boxes_3d) > 0 and len(angles) > 0:
                centers = boxes_3d[:, 0:3]
                sizes = boxes_3d[:, 3:6]
                view = np.array(data.get("calibration"))
        
                boxes = np.array(data.get("boxes"))
                labels = boxes[:, 4:5].flatten().astype(np.int32)
                # If there are string labels, 
                # then convert ground truth labels to strings.
                if len(self.labels):
                    labels = self.convert_labels(
                        self.labels, labels, self.label_offset)
                boxes = boxes[:0:4] # Exclude the labels.
            else:
                return annotations
        
        except UnicodeDecodeError:
            logger(f"Encountered UnicodeDecodeError for {annotation_path}" +
                   "Returning an empty ground truth schema for this image.",
                   code="WARNING")
            return annotations
        # TypeError is due to the annotation path being None.
        except (FileNotFoundError, TypeError, KeyError):
            return annotations
        
        annotations["boxes"] = boxes
        annotations["centers"] = centers
        annotations["sizes"] = sizes
        annotations["angles"] = angles
        annotations["view"] = view
        annotations["labels"] = labels
        return annotations
    
    def read_segmentation_json_file(
            self, annotation_path: str, height: int, width: int) -> dict:
        """
        Reads from a JSON annotation file to retrieve segmentation polygons
        such as multiple (x,y) coordinates around an object to be segmented.

        Parameters
        ----------
            annotation_path: str
                This is the path to the JSON annotation.

            height: int
                This is the image height.
            
            width: int
                This is the image width.

        Returns
        -------
            annotation info: dict
                This contains information such as:

                    .. code-block:: python

                        {
                            'segments': list of polygon segments 
                                        [[[x,y], [x,y], ...]...],
                            'labels': list of labels
                        }
        """
        annotations = {
            "segments": np.array([]),
            "labels": np.array([]).astype(np.int32)
        }

        try:
            with open(annotation_path) as file:
                data = json.load(file)
    
            segments, labels = list(), list()
            for segment in data["segment"]:
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

        except UnicodeDecodeError:
            logger(f"Encountered UnicodeDecodeError for {annotation_path}" +
                   "Returning an empty ground truth schema for this image.",
                   code="WARNING")
            return annotations
        # TypeError is due to the annotation path being None.
        except (FileNotFoundError, TypeError, KeyError):
            return annotations

        annotations["segments"] = segments
        annotations["labels"] = labels
        return annotations

    def read_pose_json_file(self, annotation_path: str) -> dict:
        """
        Reads from a JSON annotation file to retrieve headpose angles.

        Parameters
        ----------
            annotation_path: str
                The path to the annotation file.

        Returns
        -------
            load: dict
                This contains the angles and the labels.

                    .. code-block:: python

                        {
                            "boxes": list of bounding boxes,
                            "angles": [roll, pitch, yaw],
                            "labels": [helmet]
                        }
        """
        annotations = {
            "boxes": np.array([[]]),
            "angles": np.array([[]]),
            "labels": np.array([]).astype(np.int32)
        }

        try:
            with open(annotation_path) as file:
                data: dict = json.load(file)
          
            angles = data.get("angles")
            if data.get("boxes") is None:
                raise TypeError(
                    "There are no boxes for this file {}".format(
                        os.path.basename(annotation_path)))
            
            labels, boxes = list(), list()
            if len(data.get("boxes")):
                labels = np.array(data.get("boxes"))[:, 4:5].astype(np.int32)
                # If there are string labels, 
                # then convert integer labels to strings.
                if len(self.labels):
                    labels = self.convert_labels(self.labels, labels)  
                boxes = np.array(data.get("boxes"))
                boxes = boxes[:, 0:4]
                boxes = self.normalizer(boxes) if self.normalizer else boxes
                boxes = self.transformer(boxes) if self.transformer else boxes

        except UnicodeDecodeError:
            logger(f"Encountered UnicodeDecodeError for {annotation_path}" +
                   "Returning an empty ground truth schema for this image.",
                   code="WARNING")
            return annotations
        # TypeError is due to the annotation path being None.
        except (FileNotFoundError, TypeError, KeyError):
            return annotations
        
        annotations["angles"] = angles
        annotations["labels"] = labels
        annotations["boxes"] = boxes
        return annotations