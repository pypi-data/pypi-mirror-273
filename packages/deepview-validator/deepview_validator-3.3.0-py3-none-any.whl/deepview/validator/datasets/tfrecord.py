# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.exceptions import MissingLibraryException
from deepview.validator.exceptions import EmptyDatasetException
from deepview.validator.datasets.instance import Instance
from deepview.validator.datasets.core import Dataset
from deepview.validator.datasets.utils import (
    validate_dataset_source,
    classify_dataset
)
import numpy as np
import glob
import os

class TFRecordDataset(Dataset):
    """
    Reads TFRecord Datasets.
    
    Parameters
    ----------
        source: str
            The path to the source dataset.

        info_dataset: dict
            Formatted as:

                .. code-block:: python

                    {
                        "classes": [list of unique labels],
                        "validation": {
                            "path": path to the *.tfrecord files.
                        }
                    }

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
            The offset to use for the mapping of integer labels to 
            string labels.

    Raises
    ------
        MissingLibraryException
            Raised if tensorflow library is not installed. 

        EmptyDatasetException
            Raised if the provided path to the tfrecord files 
            does not contain any tfrecord files.
    """
    def __init__(
        self,
        source: str,
        info_dataset: dict=None,
        gformat: str="yolo",
        absolute: bool=False,
        validate_type: str="detection",
        label_offset: int=0
    ):
        super(TFRecordDataset, self).__init__(
            source=source,
            gformat=gformat,
            absolute=absolute,
            validate_type=validate_type
        )

        self.label_offset = label_offset

        if info_dataset is None:
            info_dataset = classify_dataset(source)

        self.source = validate_dataset_source(
            info_dataset.get('validation').get('path'))
        
        labels = info_dataset.get('classes', None)
        if labels is not None:
            self.labels = [str(label) for label in labels]

        self.tfrecords = glob.glob(os.path.join(self.source, '*.tfrecord'))
        if len(self.tfrecords) == 0:
            raise EmptyDatasetException(f"There are no TFRecord files in {self.source}")

    def py_read_data(self, example):
        """
        This method reads the from the file to extract information.
        
        Parameters
        ----------
            example:

        Returns
        -------

        Raises
        ------
            MissingLibraryException
                Raised if tensorflow is not installed in the system.
        """
        try:
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
            import tensorflow as tf
        except ImportError:
            raise MissingLibraryException("Tensorflow library is needed to " +
                                          "read tfrecord datasets.")
        feature_description = {
            "image": tf.io.FixedLenFeature([], tf.string),
            "image_name": tf.io.FixedLenFeature([], tf.string),
            "width": tf.io.FixedLenFeature([], tf.int64),
            "height": tf.io.FixedLenFeature([], tf.int64),
            "objects": tf.io.VarLenFeature(tf.int64),
            "bboxes": tf.io.VarLenFeature(tf.float32),
        }
        sample = tf.io.parse_single_example(
            example,
            feature_description)

        img = tf.io.decode_jpeg(sample['image']).numpy()
        height, width, _ = img.shape

        labels = tf.sparse.to_dense(sample['objects']).numpy().astype(np.int32)
        boxes = np.array([], dtype=np.float32)

        if len(labels):
            boxes = tf.sparse.to_dense(
                sample['bboxes']).numpy().reshape(-1, 4).astype(np.float32)
            boxes = self.normalizer(boxes) if self.normalizer else boxes
            boxes = self.transformer(boxes) if self.transformer else boxes
            boxes[boxes < 0] = 0.0
        return img, boxes, labels, height, width, sample.get('image_name')

    def read_data(self, path):
        """
        This method reads the tfrecord data.

        Parameters
        ----------
            path:

        Returns
        -------

        Raises
        ------
            MissingLibraryException
                Raised if tensorflow is not installed in the system.
        """
        try:
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
            import tensorflow as tf
        except ImportError:
            raise MissingLibraryException("Tensorflow library is needed to " +
                                          "read tfrecord datasets.")
        return tf.py_function(
            self.py_read_data,
            [path],
            Tout=[tf.uint8, tf.float32, tf.int32,
                  tf.int32, tf.int32, tf.string])

    def build_dataset(self):
        """
        Builds the dataset. Records contain information for each image.

        Returns
        -------
            records:

        Raises
        ------
            MissingLibraryException
                Raised if tensorflow library is not installed in the system.
        """
        try:
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
            import tensorflow as tf
        except ImportError:
            raise MissingLibraryException("Tensorflow library is needed to " +
                                          "read tfrecord datasets.")
        iteration = tf.data.TFRecordDataset(
            self.tfrecords,
            num_parallel_reads=tf.data.AUTOTUNE
        ).map(
            self.read_data,
            num_parallel_calls=tf.data.AUTOTUNE
        ).batch(
            batch_size=1
        ).prefetch(tf.data.AUTOTUNE)

        records = [record for record in iteration]
        return records

    def read_sample(self, this_instance) -> Instance:
        """
        Reads one sample from the dataset (one annotation file).

        Parameters
        ----------
            this_instance

        Returns
        -------
            ground truth instance: Instance
                The ground truth instance objects contains the bounding boxes
                and the labels representing the ground truth of the image.
        """
        img, boxes, labels, height, width, file_path = this_instance

        instance = Instance(file_path.numpy()[0].decode())

        labels = labels.numpy()[0]
        if len(self.labels):
            labels = self.convert_labels(
                self.labels, labels, self.label_offset)
    
        instance.height = height.numpy()[0]
        instance.width = width.numpy()[0],
        instance.image = img.numpy()[0]
        instance.boxes = boxes.numpy()[0]
        instance.labels = labels
        return instance