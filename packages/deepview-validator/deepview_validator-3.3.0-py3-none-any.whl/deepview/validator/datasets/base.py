# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.datasets.generators.detection import BaseObjectDetectionGenerator
from deepview.validator.datasets.instance import Instance
from deepview.validator.datasets.core import Dataset
from PIL import Image
import numpy as np
import io
import os

class BaseDataset(Dataset):
    """
    This class utilizes deepview-datasets methods for iterating through
    the images and annotations.

    Parameters
    ----------
        source: str
            The path to the dataset passed in validator.

        iterator: Iterator
            Object in deepview-datasets for iterating through
            the images or annotations. This can either be a generator if
            a YAML file was passed, or a Reader if a directory was passed. 
    """
    def __init__(self, source: str, iterator):
        super(BaseDataset, self).__init__(source)
        self.iterator = iterator

        if isinstance(self.iterator, BaseObjectDetectionGenerator):
            self.storage = self.iterator.reader.storage
            self.labels = self.iterator.reader.classes
        else:
            self.storage = self.iterator.storage
            self.labels = self.iterator.classes

    def build_dataset(self):
        """
        Returns the iterator object which already contains all the images
        and annotations read in the dataset.
        """
        return self.iterator
    
    def read_sample(self, sample: tuple) -> Instance:
        """
        Returns the ground truth instance object which is needed to be read
        by validator.

        Parameters
        ----------
            sample: tuple
                This contains the (image, boxes) in one sample.

        Returns
        -------
            instance: Instance
                An object that contains the image, boxes, labels, etc.
        """
        image, boxes = sample
        if len(image.shape) < 2:
            image = Image.open(io.BytesIO(image)).convert('RGB')
            image = np.asarray(image, dtype=np.uint8)
        height, width, _ = image.shape

        if isinstance(self.iterator, BaseObjectDetectionGenerator):
            image_path = self.iterator.reader.get_instance_id()
        else:
            image_path = self.iterator.get_instance_id()

        # Add file extension to allow image saving in disk.
        if os.path.splitext(image_path)[-1] == "":
            image_path += ".png"
        
        instance = Instance(image_path)
        instance.height = height
        instance.width = width
        instance.image = image

        boxes = boxes[np.sum(boxes, axis=-1) != 0]
        instance.boxes = self.yolo2xyxy(boxes[..., 0:4])

        if len(self.labels) > 0:
            string_labels = []
            for label in boxes[..., 4:5]:
                string_labels.append(self.labels[int(label)])
            labels = np.array(string_labels)
        else:
            labels = boxes[..., 4:5]
        instance.labels = labels
        return instance