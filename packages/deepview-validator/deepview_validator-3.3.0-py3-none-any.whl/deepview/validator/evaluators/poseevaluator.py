# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from __future__ import annotations
from typing import TYPE_CHECKING, Type
if TYPE_CHECKING:
    from deepview.validator.writers import TensorBoardWriter
    from deepview.validator.metrics import MetricSummary
    from deepview.validator.evaluators import Parameters
    from deepview.validator.runners import Runner

from deepview.validator.metrics.poseutils import crop_frame_bbxarea
from deepview.validator.metrics.posedata import PoseDataCollection
from deepview.validator.metrics.posemetrics import PoseMetrics
from deepview.validator.visualize.posedraw import draw_axes
from deepview.validator.evaluators.core import Evaluator
from deepview.validator.datasets.core import Dataset
from deepview.validator.datasets import Instance
from deepview.validator.writers import logger
from copy import deepcopy
import numpy as np
import os

class PoseEval(Evaluator):
    """
    Performs pose evaluation for headpose models.

    Parameters
    ----------
        runner: Type[Runner]
            This object provides methods to run the pose model.

        dataset: Type[Dataset]
            This object provides methods to read and parse the dataset.

        parameters: Parameters
            This contains the validation parameters set from the command line.
    """
    def __init__(
        self,
        parameters: Parameters,
        runner: Type[Runner] = None,
        dataset: Type[Dataset] = None,
    ):
        super(PoseEval, self).__init__(
            runner=runner,
            dataset=dataset,
            parameters=parameters
        )
        self.data_collection = PoseDataCollection()

    def __call__(self, val_messenger: TensorBoardWriter = None):
        """
        Usually for ModelPack purposes of allowing ModelPack 
        tensorboard writer object to operate here. 

        Parameters
        ----------
            val_messenger: TensorBoardWriter
                This object handles publishing of validation 
                results to tensorboard.
        """
        if val_messenger is not None:
            self.tensorboard_writer = val_messenger

    def instance_collector(self):
        """
        Collects the ground truth and the prediction pose 
        instances for one image.

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
            gt_instance.boxes = Dataset.denormalize(
                gt_instance.boxes, height, width)
            gt_instance.pose_angles = np.squeeze(gt_instance.pose_angles)
            dt_instance = None
            if len(gt_instance.boxes) > 0:
                gt_box = gt_instance.boxes[0]
                gt_instance.boxes = gt_box
                # This is for non-offline runners.
                if os.path.splitext(self.runner.model)[1].lower() != "":
                    image = gt_instance.image
                    image = crop_frame_bbxarea(image, gt_box)
                else:
                    image = gt_instance.image_path
                angles, labels = self.runner.run_single_instance(image)

                dt_instance = Instance(gt_instance.image_path)
                dt_instance.pose_angles = angles
                dt_instance.labels = labels

            yield {
                'gt_instance': gt_instance,
                'dt_instance': dt_instance
            }

    def single_evaluation(
            self,
            instances: dict,
            epoch: int = 0,
            add_image: bool = False
        ):
        """
        This method runs pose validation a single image evaluation.

        Parameters
        ----------
            instances: dict
                The ground truth and the prediction instances.

            epoch: int
                Used for training a model the epoch number.

            add_image: bool
                If this is set to true it means to save the image or 
                display the image into tensorboard.
        """
        gt_instance: Instance = instances.get("gt_instance")
        dt_instance: Instance = instances.get("dt_instance")

        if None in [gt_instance, dt_instance]:
            logger(
                "Ground truth and detection instances returned None. " +
                "Contact support@au-zone.com for more information.",
                code="WARNING")
            return

        dt_angles = dt_instance.pose_angles
        # Currently inside a list of lists
        gt_angles = gt_instance.pose_angles
        self.data_collection.store_angles(dt_angles, gt_angles)

        if add_image:
            if self.parameters.visualize or self.tensorboard_writer:
                image = draw_axes(
                    gt_instance.image,
                    dt_angles,
                    gt_angles,
                    gt_box=gt_instance.boxes)

            if self.parameters.visualize:
                image.save(os.path.join(
                    self.parameters.visualize,
                    os.path.basename(gt_instance.image_path)))
            elif self.tensorboard_writer:
                self.tensorboard_writer(
                    np.asarray(image), gt_instance.image_path, step=epoch)

    def group_evaluation(self, add_image: bool = True):
        """
        Performs pose evaluation on all images.

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
                add_image=add_image
            )

    def conclude(self, epoch: int = 0) -> MetricSummary:
        """
        Computes the final metrics for pose models and saves
        the results either to tensorboard or to the local machine.

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

        metrics = PoseMetrics(
            self.data_collection,
            self.metric_summary
        )
        metrics.run_metrics()

        if self.parameters.json_out:
            self.save_json_summary()

        if self.tensorboard_writer:
            self.publish_metrics(epoch, validation_type="pose")
        else:
            header, format_summary, format_timings = self.console_writer(
                summary=self.metric_summary,
                parameters=self.parameters,
                validation_type="pose")

            if self.parameters.visualize:
                self.save_metrics_disk(header, format_summary, format_timings)
    
        metric_summary_copy = deepcopy(self.metric_summary)
        self.reset()
        return metric_summary_copy