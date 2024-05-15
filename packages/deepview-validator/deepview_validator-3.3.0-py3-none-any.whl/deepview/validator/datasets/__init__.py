# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from __future__ import annotations
from typing import Type

from deepview.validator.datasets.instance import InstanceCollection
from deepview.validator.datasets.tfrecord import TFRecordDataset
from deepview.validator.datasets.darknet import DarkNetDataset
from deepview.validator.datasets.arrow import ArrowDataset
from deepview.validator.datasets.instance import Instance
from deepview.validator.datasets.base import BaseDataset
from deepview.validator.datasets.core import Dataset
from deepview.validator.writers import logger

def instantiate_dataset(
        info_dataset,
        source: str=None,
        gformat: str='yolo',
        absolute: bool=False,
        validate_type: str='detection',
        validate_3d: bool=False,
        show_missing_annotations: bool=False,
        label_offset: int=0,
        local: bool=False
    ) -> Type[Dataset]:
    """
    This function instantiates either darknet or tfrecord
    format dataset objects.

    Parameters
    ----------
        info_dataset: dict
            If the dataset is darknet, this 
            contains information such as:

            .. code-block:: python

                {
                    "classes": [list of unique labels],
                    "type": "darknet",
                    "validation":
                    {
                        "images: 'path to the images',
                        "annotations": 'path to the annotations'
                    },
                }

            *Note: the classes are optional and the path to the images
            and annotations can be the same.*

            If the dataset is tfrecord, this
            contains information such as:

            .. code-block:: python

                {
                    "classes": [list of unique labels],
                    "validation": {
                        "path": path to the *.tfrecord files.
                    }
                }

        source: str
            The path to the dataset.

        gformat: str
            The annotation format that can be either 'yolo', 'pascalvoc',
            or 'coco'. By default darknet datasets have annotations in
            'yolo' format.

        absolute: bool
            Specify as True if the annotations are not normalized to the
            image dimensions. By default they are normalized.

        validate_type: str
            The type of validation to perform that can be 'detection' or
            'segmentation'.

        validate_3d: bool
            Specify for 3D bounding box annotations.

        show_missing_annotations: bool
            If this is True, then print on the terminal all
            missing annotations. Else, it will only
            print the number of missing annotations.

        label_offset: int
            The offset to use for the mapping of integer labels to 
            string labels. 

        local: bool
            Specify whether to use local validator methods for reading datasets.
            Otherwise, by default use deepview-datasets.

    Returns
    -------
        Dataset object: DarknetDataset or TFRecordDataset
            This object is returned depending on the type of dataset
            provided.

    Raises
    ------
        InvalidDatasetSourceException
            This exception will be raised if the path
            to the images or annotations is None.

        DatasetNotFoundException
            This exception will be raised if the provided path
            to the images or annotations does not exist.

        ValueError
            This exception will be raised if the provided
            path to the images or annotations is not a string.

        EmptyDatasetException
            This exception will be raised if the provided
            path to the images or text files does not contain
            any image files or text files respectively.
    """
    if isinstance(info_dataset, dict):
        try:
            ds_format = info_dataset.get('type')
            if ds_format is None:
                ds_format = info_dataset.get("dataset").get("format")
        except AttributeError:
            logger("Dataset was not properly read. Ensure the dataset " +
                "structure follows images/validate and labels/validate.",
                code="ERROR")
        if ds_format in [None, "tfrecord"]:
            return TFRecordDataset(
                info_dataset=info_dataset,
                source=source,
                gformat=gformat,
                absolute=absolute,
                validate_type=validate_type,
                label_offset=label_offset
                )
        elif ds_format == "darknet":
            return DarkNetDataset(
                info_dataset=info_dataset,
                source=source,
                gformat=gformat,
                absolute=absolute,
                validate_type=validate_type,
                show_missing_annotations=show_missing_annotations,
                validate_3d=validate_3d,
                label_offset=label_offset,
                )
        elif ds_format == "arrow":
            return ArrowDataset(
                info_dataset=info_dataset,
                source=source,
                gformat=gformat,
                absolute=absolute,
                validate_type=validate_type,
                label_offset=label_offset,
            )
    else:
        return BaseDataset(
            source=source,
            iterator=info_dataset
        )