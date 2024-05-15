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
    validate_dataset_source
)
from deepview.validator.writers import logger
import numpy as np

class ArrowDataset(Dataset):
    """
    Reads Arrow datasets.

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
                            "images: 'path to the images arrow files',
                            "annotations": 'path to the annotations arrow files'
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
        label_offset: int=0,
    ):
        super(ArrowDataset, self).__init__(
            source=source,
            gformat=gformat,
            absolute=absolute,
            validate_type=validate_type,
        )
        self.label_offset = label_offset

        if info_dataset is None:
            info_dataset = classify_dataset(source)

        self.validate_type = validate_type.lower()
        
        try:
            self.image_source = info_dataset.get("dataset").get('validation').get('images')
            self.annotation_source = info_dataset.get("dataset").get('validation').get('annotations')
        except AttributeError:
            self.image_source = validate_dataset_source(info_dataset.get('validation').get('images'))
            self.annotation_source = validate_dataset_source(info_dataset.get('validation').get('annotations'))
            
        try:
            from deepview.datasets.readers import PolarsDetectionReader
        except ImportError:
            logger(
                "Dependency missing: deepview-datasets is needed for polar datasets.", 
                code="ERROR")
        self.reader = PolarsDetectionReader(
            inputs = self.image_source,
            annotations = self.annotation_source,
        )

        labels = info_dataset.get('classes', None)
        if labels is not None:
            self.labels = [str(label) for label in labels]
        else:
            self.labels = self.reader.classes

    def build_dataset(self):
        """
        Allows iteration in the dataset.

        Returns
        -------
            reader: Iterable
                Contains the images and boxes.
        """
        return self.reader
    
    def read_sample(self, sample: tuple) -> Instance:
        """
        Reads one sample from the dataset.

        Parameters
        ----------
            sample: tuple
                This contains (image, boxes).
        
        Returns
        -------
            ground truth instance: Instance
                The ground truth instance objects contains the bounding boxes
                and the labels representing the ground truth of the image.
        """
        image = sample[0].astype(np.uint8)
        height, width, _ = image.shape
        boxes = sample[1]

        instance = Instance(f"image_{self.reader.__current__ - 1}.jpg") # Index starts at 1.
        instance.height = height
        instance.width = width
        instance.image = image

        labels = np.squeeze(boxes[..., 4:5].astype(np.int32), axis=1)
        boxes = boxes[..., 0:4]

        if len(boxes) > 0:
            boxes = self.normalizer(boxes) if self.normalizer else boxes
            boxes = self.transformer(boxes) if self.transformer else boxes

        # If there are string labels, 
        # then convert ground truth labels to strings.
        if self.labels is not None and len(self.labels) > 0:
            labels = self.convert_labels(
                self.labels, labels, self.label_offset)

        instance.boxes = boxes
        instance.labels = labels
        return instance