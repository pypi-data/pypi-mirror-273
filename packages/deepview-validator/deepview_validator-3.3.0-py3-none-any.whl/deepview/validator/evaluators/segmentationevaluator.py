# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from __future__ import annotations
from typing import TYPE_CHECKING, Type, Union
if TYPE_CHECKING:
    from deepview.validator.writers import TensorBoardWriter
    from deepview.validator.metrics import MetricSummary
    from deepview.validator.evaluators import Parameters
    from deepview.validator.datasets import Dataset
    from deepview.validator.runners import Runner

from deepview.validator.metrics.segmentationutils import create_mask_image
from deepview.validator.visualize.segmentationdraw import mask2maskimage
from deepview.validator.evaluators.utils import segmentation_evaluate
from deepview.validator.evaluators.core import Evaluator
from deepview.validator.datasets import Instance
from deepview.validator.visualize.utils import (
    plot_classification_segmentation,
    figure2numpy,
    close_figures
)
from deepview.validator.metrics import (
    SegmentationDataCollection,
    SegmentationMetrics
)
from copy import deepcopy
import numpy as np
import os

class SegmentationEval(Evaluator):
    """
    Provides methods to perform segmentation validation.
    The common process of running validation::

        1. Grab the ground truth and the model prediction instances per image.
        2. Create masks for both ground truth and model prediction.
        3. Classify the mask pixels as either true predictions or false predictions.
        4. Overlay the ground truth and predictions masks on the image.
        5. Calculate the metrics.

    Parameters
    ----------
        runner: Type[Runner]
            This object provides methods to run the detection model.

        dataset: Type[Dataset]
            This object provides methods to read and parse the dataset.

        parameters: Parameters
            This contains validation parameters set from the command line.
    """
    def __init__(
        self,
        parameters: Parameters,
        runner: Type[Runner] = None,
        dataset: Type[Dataset] = None
    ):
        super(SegmentationEval, self).__init__(
            runner=runner,
            dataset=dataset,
            parameters=parameters
        )
        self.data_collection = SegmentationDataCollection()

    def __call__(self, val_messenger: TensorBoardWriter = None):
        """
        Usually for ModelPack purposes of allowing ModelPack 
        tensorboard writer object to operate here 

        Parameters
        ----------
            val_messenger: TrainingTensorBoardWriter
                This object is internal for modelpack that was instantiated
                specifically for training a model.
        """
        if val_messenger is not None:
            self.tensorboard_writer = val_messenger

    def instance_collector(self):
        """
        Collects the instances from the ground truth
        and the model segmentations.

        Yields
        -------
            instances: dict
                This yields one image instance from the ground
                truth and the model predictions.
        """
        gt_instance: Instance
        for gt_instance in self.dataset.read_all_samples(
            silent=self.parameters.silent):
            height = gt_instance.height
            width = gt_instance.width
            gt_instance.mask = create_mask_image(height, width, gt_instance)
            gt_instance.labels = np.unique(gt_instance.mask)

            if os.path.splitext(self.runner.model)[1].lower() != "":
                image = gt_instance.image
            # For offline runners, only the path to the image is needed.
            else:
                image = gt_instance.image_path

            dt_instance = Instance(gt_instance.image_path)
            dt_instance.mask = self.runner.run_single_instance(image)
            dt_instance.labels = np.unique(dt_instance.mask)

            yield {
                'gt_instance': gt_instance,
                'dt_instance': dt_instance
            }

    def single_evaluation(
        self,
        instances: dict,
        labels: Union[list, np.ndarray] = None,
        epoch: int = 0,
        add_image: bool = False
    ):
        """
        This method runs segmentation validation on a single instance.

        Parameters
        ----------
            instances: dict
                The ground truth and the prediction instances.

            labels: list or np.ndarray
                This contains a list of string labels to optionally convert
                integer labels to strings.

            epoch: int
                This is the training epoch number. This
                parameter is internal for modelpack usage.
                Standalone validation has no use of this parameter.

            add_image: bool
                If set to True, this will save the image with drawn 
                segmentation masks from both ground truth and predictions.
        """
        gt_instance: Instance = instances.get("gt_instance")
        dt_instance: Instance = instances.get("dt_instance")

        # Store the ground truth and prediction instances per image.
        # Too resource intensive for the EVK.
        # self.collected_instances.append_gt_instance(gt_instance)
        # self.collected_instances.append_dt_instance(dt_instance)

        image_summary = segmentation_evaluate(
            gt_instance,
            dt_instance,
            self.parameters,
            self.data_collection,
            labels)
        self.metric_summary.add_ground_truths(image_summary.ground_truths)
        self.metric_summary.add_predictions(image_summary.predictions)
        self.metric_summary.add_true_predictions(
            image_summary.true_predictions)
        self.metric_summary.add_false_predictions(
            image_summary.false_predictions)
        self.metric_summary.add_union(image_summary.union)

        # Too resource intensive for the EVK, add_ground_truths is also inside the method below.
        # self.metric_summary.append_image_summary(image_summary)

        # Execute this code for four pane image results
        if add_image:
            if self.parameters.visualize or self.tensorboard_writer:
                image = mask2maskimage(gt_instance, dt_instance)
            if self.parameters.visualize:
                image.save(
                    os.path.join(self.parameters.visualize,
                                 os.path.basename(gt_instance.image_path)))
            elif self.tensorboard_writer:
                self.tensorboard_writer(
                    np.asarray(image), gt_instance.image_path, step=epoch)
        return image_summary

    def group_evaluation(self, add_image: bool = True):
        """
        Performs the segmentation evaluation on all images.

        Parameters
        ----------
            add_image: bool
                If this is set to true, images will be saved, otherwise
                images will not be saved. Note that either visualize or
                tensorboard parameters need to be set in the command line
                in order for this parameter to have an effect.
        """
        for instances in self.instance_collector():
            if self.parameters.display >= 0:
                if self.counter < self.parameters.display:
                    add_image = True
                    self.counter += 1
                else:
                    add_image = False

            self.single_evaluation(
                instances,
                labels=self.dataset.labels,
                add_image=add_image)

    def conclude(self, epoch=0) -> MetricSummary:
        """
        Computes the final metrics, draws the class histogram, and
        saves the results either to tensorboard or to the local machine.

        Parameters
        ----------
            epoch: int
                This is the training epoch number. This
                parameter is internal for modelpack usage.
                Standalone validation has no use of this parameter.

        Returns
        -------
            metric_summary: MetricSummary
                This contains the validation metrics of the model. The data
                stored in this object is used to report onto Tensorboard or
                into the terminal. 
        """
        if self.runner is not None:
            timings = self.runner.summarize()
            self.metric_summary.timings = timings

        metrics = SegmentationMetrics(self.data_collection,
                                      self.plot_summary,
                                      self.metric_summary)
        metrics.run_metrics()

        """Plot Operations"""
        if self.parameters.visualize or self.tensorboard_writer:
            fig_class_metrics = plot_classification_segmentation(
                self.plot_summary.class_histogram_data,
                self.metric_summary.model)

        if self.parameters.visualize:
            fig_class_metrics.savefig(
                f'{self.parameters.visualize}/class_scores.png',
                bbox_inches="tight")
            close_figures([fig_class_metrics])
        elif self.tensorboard_writer:
            nimage_class = figure2numpy(fig_class_metrics)
            self.tensorboard_writer(nimage_class,
                                    f"{self.metric_summary.model}_scores.png",
                                    step=epoch)
            close_figures([fig_class_metrics])

        if self.parameters.json_out:
            self.save_json_summary()

        if self.tensorboard_writer:
            self.publish_metrics(epoch=epoch, validation_type="segmentation")
        else:
            header, format_summary, format_timings = self.console_writer(
                summary=self.metric_summary,
                parameters=self.parameters,
                validation_type="segmentation")

            if self.parameters.visualize:
                self.save_metrics_disk(
                    header,
                    format_summary,
                    format_timings)

        metric_summary_copy = deepcopy(self.metric_summary)
        self.reset()
        return metric_summary_copy