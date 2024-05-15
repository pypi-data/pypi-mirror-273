# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from __future__ import annotations
from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
    from deepview.validator.evaluators import Parameters
    from deepview.validator.metrics import PlotSummary
    from deepview.validator.datasets import Instance
    from deepview.validator.metrics import (
        SegmentationDataCollection,
        DetectionDataCollection, 
    )

from deepview.validator.metrics.detectionmatch import MatchDetections
from deepview.validator.metrics.summary import ImageSummary
from deepview.validator.metrics.segmentationutils import (
    create_mask_background, 
    create_mask_class, 
    classify_mask
)
from deepview.validator.metrics.detectionutils import (
    ignore_boxes, 
    clamp_boxes, 
    get_corners,
    filter_dt
)
from deepview.validator.datasets.utils import resize
from copy import deepcopy
import numpy as np
import os

def detection_evaluate(
        gt_instance: Instance, 
        dt_instance: Instance,
        parameters: Parameters,
        data_collection: DetectionDataCollection,
        plot_summary: PlotSummary=None,
        verbose_store: bool=True,
        restore: bool = False
    ) -> ImageSummary:
    """
    This is the base detection evaluation function.

    Parameters
    ----------
        gt_instance: Instance
            This contains the ground truth instance for the image such as
            the bounding boxes, labels, etc.

        dt_instance: Instance
            This contains the ground truth instance for the image such as
            the bounding boxes, labels, scores, etc.
        
        parameters: Parameters
            This contains the model and validation parameters 
            set from the command line.

        data_collection: DetectionDataCollection
            Contains a list of DetectionLabelData which are 
            class representation of ground truth or prediction labels that
            act as containers for their number of true positives,
            false positives, or false negatives.

        plot_summary: PlotSummary
            This contains the data used to generate the validation plots.

        verbose_store: bool
            If this is set to true, this specifies to store the confusion
            matrix data and aswell as the information on the matches in
            the image summaries. 

        restore: bool
            This is used for building the PR curve, since it iterates through
            the same detections and ground truths per threshold, it is important
            to start with data that is untampered. So restore, restores the 
            data to be processed with the original set of detections and ground
            truths that were not filtered, clamped, or ignored. 

    Returns
    -------
        image_summary: ImageSummary
            This is the image summary object which contains the matches
            and unmatches per image.
    """
    image_summary = ImageSummary(os.path.basename(gt_instance.image_path))

    # Restore is set to true for building the PR curve.
    if restore:
        # Restore detection bounding boxes to its original condition.
        dt_instance.boxes = deepcopy(dt_instance.unfiltered_boxes)
        dt_instance.labels = deepcopy(dt_instance.unfiltered_labels)
        dt_instance.scores = deepcopy(dt_instance.unfiltered_scores)
    else:
        # Save untampered/unfiltered detection bounding boxes. This will be
        # used for building the PR curve. 
        dt_instance.unfiltered_boxes = deepcopy(dt_instance.boxes)
        dt_instance.unfiltered_labels = deepcopy(dt_instance.labels)
        dt_instance.unfiltered_scores = deepcopy(dt_instance.scores)
        data_collection.store_unfiltered_labels(dt_instance.unfiltered_labels)

    # Filter detections only for valid scores.
    if len(dt_instance.boxes):
        dt_boxes, dt_labels, scores = filter_dt(
            np.array(dt_instance.boxes), 
            np.array(dt_instance.labels), 
            np.array(dt_instance.scores), 
            parameters.validation_score
        )
        dt_instance.boxes = dt_boxes
        dt_instance.labels = dt_labels
        dt_instance.scores = scores

    if parameters.clamp_boxes:
        clamp_boxes(gt_instance, dt_instance, parameters.clamp_boxes)
    if parameters.ignore_boxes:
        ignore_boxes(gt_instance, dt_instance, parameters.ignore_boxes)

    data_collection.capture_class(dt_instance.labels)
    data_collection.capture_class(gt_instance.labels)

    # corner formats should be [[[x,y,z], [x,y,z], ... x6]]
    if parameters.validate_3d:
        gt_instance.corners = get_corners(
            gt_instance.sizes, gt_instance.box_angles, gt_instance.centers)
        dt_instance.corners = get_corners(
            dt_instance.sizes, dt_instance.box_angles, dt_instance.centers)

    matcher = MatchDetections(
        gt_instance, 
        dt_instance,
        parameters,
        data_collection,
        image_summary,
        plot_summary,
        verbose_store
    )
    matcher.match()
    matcher.classify_detections()
    return image_summary

def segmentation_evaluate(
    gt_instance: Instance, 
    dt_instance: Instance,
    parameters: Parameters,
    data_collection: SegmentationDataCollection,
    labels: Union[list, np.ndarray]=None,
) -> ImageSummary:
    """
    This is the base segmentation evaluation function.

    Parameters
    ----------
        gt_instance: Instance
            This contains the ground truth instance for the image such as
            the polygons, masks, labels, etc.

        dt_instance: Instance
            This contains the ground truth instance for the image such as
            the polygons, masks, etc.
        
        parameters: Parameters
            This contains the model and validation parameters 
            set from the command line.

        data_collection: SegmentationDataCollection
            Contains a list of SegmentationLabelData which are 
            class representation of ground truth or prediction labels that
            act as containers for their number of true predictions and 
            false predictions per label.

        labels: list or np.ndarray
            This contains a list of string labels to optionally convert
            integer labels to strings.

    Returns
    -------
        image_summary: ImageSummary
            This is the image summary object which contains the number of
            predictions and ground truth pixels per image and as well as
            the number of true predictions and false predictions per image.
    """
    image_summary = ImageSummary(os.path.basename(gt_instance.image_path))
    
    class_labels = np.unique(
        np.append(gt_instance.labels, dt_instance.labels))
    
    gt_mask = gt_instance.mask
    dt_mask = resize(dt_instance.mask, (gt_instance.height, gt_instance.width))
    dt_instance.mask = dt_mask
    
    predictions = dt_mask.flatten()
    ground_truths = gt_mask.flatten()
    if not parameters.include_background:
        class_labels = class_labels[class_labels != 0]
        predictions = predictions[predictions != 0]
        ground_truths = ground_truths[ground_truths !=0]
        true_predictions, false_predictions, union_gt_dt = classify_mask(
            gt_mask, dt_mask)
    else:
        true_predictions, false_predictions, union_gt_dt = classify_mask(
            gt_mask, dt_mask, False)

    data_collection.capture_class(class_labels, labels)

    image_summary.ground_truths = len(ground_truths)
    image_summary.predictions = len(predictions)
    image_summary.true_predictions = true_predictions
    image_summary.false_predictions = false_predictions
    image_summary.union = union_gt_dt
        
    for cl in class_labels:
        gt_class_mask = create_mask_class(gt_mask, cl)
        dt_class_mask = create_mask_class(dt_mask, cl)

        # Evaluate background class
        if cl == 0:
            gt_class_mask = create_mask_background(gt_mask)
            dt_class_mask = create_mask_background(dt_mask)

        class_ground_truths = np.sum(gt_mask == cl)
        class_predictions = np.sum(dt_mask == cl)

        # Under classify_mask always exclude background because we are
        # only concerned with this class. 
        class_true_predictions, class_false_predictions, union_gt_dt = \
            classify_mask(gt_class_mask, dt_class_mask)

        if labels is not None:
            datalabel = data_collection.get_label_data(labels[cl])
        else:
            datalabel = data_collection.get_label_data(cl)
        
        datalabel.add_true_predictions(class_true_predictions)
        datalabel.add_false_predictions(class_false_predictions)
        datalabel.add_ground_truths(class_ground_truths)
        datalabel.add_predictions(class_predictions)
        datalabel.add_union(union_gt_dt)
    return image_summary