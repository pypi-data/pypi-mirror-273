# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from __future__ import annotations
from typing import TYPE_CHECKING, Type, List
if TYPE_CHECKING:
    from deepview.validator.metrics import ImageSummary, MetricSummary
    from deepview.validator.metrics import DetectionDataCollection
    from deepview.validator.writers import TensorBoardWriter
    from deepview.validator.evaluators import Parameters
    from deepview.validator.datasets import Instance
    from deepview.validator.datasets import Dataset
    from deepview.validator.runners import Runner
    import matplotlib.figure

from deepview.validator.metrics.detectionmetrics import DetectionMetrics
from deepview.validator.evaluators.utils import detection_evaluate
from deepview.validator.metrics import DetectionDataCollection
from deepview.validator.evaluators.core import Evaluator
from deepview.validator.visualize.detectiondraw import (
    draw_2d_bounding_boxes,
    draw_3d_bounding_boxes
)
from deepview.validator.datasets import Instance
from deepview.validator.visualize.utils import (
    plot_classification_detection,
    plot_confusion_matrix,
    plot_pr_curve,
    figure2numpy,
    close_figures
)
from deepview.validator.writers import logger
from copy import deepcopy
import numpy as np
import os

class DetectionEval(Evaluator):
    """
    Provides methods to perform detection validation.
    The common process of running validation::

        1. Grab the ground truth and the model prediction instances per image.
        2. Match the  model predictions to the ground truth.
        3. Categorize the model predictions into tp, fp or fn.
        4. Draw the bounding boxes.
        5. Calculate the metrics.

    Parameters
    ----------
        runner: Type[Runner]
            This object provides methods to run the detection model.

        dataset: Type[Dataset]
            This object provides methods to read and parse the dataset.

        parameters: Parameters
            This contains the validation parameters set from the command line.
    """
    def __init__(
        self,
        parameters: Parameters,
        runner: Type[Runner] = None,
        dataset: Type[Dataset] = None
    ):
        super(DetectionEval, self).__init__(
            runner=runner,
            dataset=dataset,
            parameters=parameters
        )
        self.data_collection = DetectionDataCollection()
        if self.parameters.validate_3d:
            self.drawer = draw_3d_bounding_boxes
        else:
            self.drawer = draw_2d_bounding_boxes

    def __call__(self, val_messenger: TensorBoardWriter = None):
        """
        Usually for ModelPack purposes of allowing ModelPack 
        tensorboard writer object to operate here. 

        Parameters
        ----------
            val_messenger: TensorBoardWriter
                This object handles publishing of validation 
                results into tensorboard.
        """
        if val_messenger is not None:
            self.tensorboard_writer = val_messenger

    def instance_collector(self, labels: List[str] = []):
        """
        Collects the instances from the ground truth and the model predictions.

        Parameters
        ----------
            labels: list
                This is the unique string labels that can be optionally
                set if validating coco datasets where labels had synonyms for
                representing the same object. A method is provided to map any
                synyonyms back to the standard coco labels. 

        Yields
        -------
            instances: dict
                This yields one image instance from the ground
                truth and the model predictions.
        """
        gt_instance: Instance
        for gt_instance in self.dataset.read_all_samples(
            silent=self.parameters.silent):

            if (os.path.splitext(self.runner.model)[1].lower() != "" or 
                self.runner.loaded_model is not None):
                image = gt_instance.image
            # For offline runners, only the path to the image is needed.
            else:
                image = gt_instance.image_path

            detections = self.runner.run_single_instance(image)

            if detections is None:
                yield {
                    'gt_instance': gt_instance,
                    'dt_instance': None
                }
            dt_instance = Instance(gt_instance.image_path)

            if self.parameters.validate_3d:
                # Note: This may change depending on the outputs of the trained model.
                dt_centers, dt_sizes, dt_angles, dt_view, dt_classes, dt_scores = detections
                dt_instance.centers = dt_centers
                dt_instance.sizes = dt_sizes
                dt_instance.box_angles = dt_angles
                dt_instance.calibration = dt_view
                dt_instance.scores = dt_scores
            else:
                dt_boxes, dt_classes, dt_scores = detections
                dt_instance.boxes = dt_boxes
                dt_instance.scores = dt_scores

            # Convert any synonym of the predicted label
            # into the standard coco label.
            if labels is not None and "clock" in labels:
                from deepview.validator.datasets.utils import standardize_coco_labels
                dt_classes = standardize_coco_labels(dt_classes)
            dt_instance.labels = dt_classes

            yield {
                'gt_instance': gt_instance,
                'dt_instance': dt_instance
            }

    def single_evaluation(
            self, 
            instances: dict, 
            epoch: int = 0, 
            add_image: bool = False
        ) -> ImageSummary:
        """
        This method runs detection validation on a single instance.

        Parameters
        ----------
            instances: dict
                The ground truth and the prediction instances.

            epoch: int
                This is the training epoch number. This
                parameter is internal for modelpack usage.
                Standalone validation has no use of this parameter.

            add_image: bool
                If set to True, this will save the image 
                with drawn bounding boxes.

        Returns
        -------
            image_summary: ImageSummary
                This object contains the detection metrics for 
                this particular image.
        """
        gt_instance: Instance = instances.get("gt_instance")
        dt_instance: Instance = instances.get("dt_instance")

        # Store the ground truth and prediction instances per image.
        # Too resource intensive for the EVK.
        # self.collected_instances.append_gt_instance(gt_instance)
        # self.collected_instances.append_dt_instance(dt_instance)

        image_summary = detection_evaluate(
            gt_instance,
            dt_instance,
            self.parameters,
            self.data_collection,
            self.plot_summary
        )
        self.metric_summary.add_ground_truths(image_summary.ground_truths)
        self.metric_summary.store_centers(
            gt_centers=image_summary.centers.get("gt_centers"),
            dt_centers=image_summary.centers.get("dt_centers"),
            center_distances=image_summary.centers.get("center_distances")
        )
        # Too resource intensive for the EVK, add_ground_truths is also inside the method below.
        # self.metric_summary.append_image_summary(image_summary)

        if add_image:
            if self.parameters.visualize or self.tensorboard_writer:
                image = self.drawer(
                    gt_instance,
                    dt_instance,
                    image_summary,
                    self.parameters.validation_iou,
                    self.parameters.validation_score)

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
        Performs the bounding box evaluation on all images.

        Parameters
        ----------
            add_image: bool
                If this is set to true, images will be saved, otherwise
                images will not be saved. Note that either visualize or
                tensorboard parameters need to be set in the command line
                in order for this parameter to have an effect.
        """
        for instances in self.instance_collector(self.dataset.labels):
            if self.parameters.display >= 0:
                if self.counter < self.parameters.display:
                    add_image = True
                    self.counter += 1
                else:
                    add_image = False

            if instances.get("dt_instance") is None:
                logger(
                    "VisionPack Trial Expired. Please use a licensed version" +
                    " for complete validation. Contact support@au-zone.com" +
                    " for more information.", code="WARNING")
                break
            self.single_evaluation(instances, add_image=add_image)

    def conclude(self, epoch: int = 0) -> MetricSummary:
        """
        Computes the final metrics, draws the final plots, and
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

        metrics = DetectionMetrics(
            self.data_collection,
            self.collected_instances,
            self.plot_summary,
            self.metric_summary,
            self.parameters
        )
        metrics.run_metrics()

        """Plot Operations"""
        if self.parameters.plots:
            self.plot_summary.tabularize_confusion_matrix()
            # Using YoloV5 implementation of the precision recall curve.
            # The code below will use deepview-validator implementation
            # of the precision recall curve.
            # metrics.get_pr_data()

            if self.parameters.visualize or self.tensorboard_writer:
                plots = self.get_plots()

                if self.parameters.visualize:
                    self.save_plots_disk(plots)
                elif self.tensorboard_writer:
                    self.publish_plots(plots, epoch)
                close_figures(plots)
        
        """Metric Operations"""
        if self.parameters.json_out:
            self.save_json_summary()
        if self.tensorboard_writer:
            self.publish_metrics(epoch)
        else:
            header, format_summary, format_timings = self.console_writer(
                summary=self.metric_summary,
                parameters=self.parameters,
                validation_type="detection")

            if self.parameters.visualize:
                self.save_metrics_disk(header, format_summary, format_timings)
        
        metric_summary_copy = deepcopy(self.metric_summary)
        self.reset()
        return metric_summary_copy

    def get_plots(self) -> List[matplotlib.figure.Figure]:
        """
        Creates Matplotlib figures based on the plot data gathered
        during validation.

        Returns
        -------
            plots: list
                This contains matplotlib figures of the plots. 
        """
        fig_class_metrics = plot_classification_detection(
            self.plot_summary.class_histogram_data, self.metric_summary.model)

        fig_confusion_matrix = plot_confusion_matrix(
            self.plot_summary.confusion_matrix, 
            self.plot_summary.confusion_labels, 
            self.metric_summary.model)
        # Using YoloV5 implementation of the precision recall curve.
        fig_prec_rec_curve = plot_pr_curve(
            self.plot_summary.precision,
            self.plot_summary.recall,
            self.plot_summary.average_precision,
            self.plot_summary.curve_labels,
            self.metric_summary.model)
        return [fig_class_metrics, fig_confusion_matrix, fig_prec_rec_curve]

    def save_plots_disk(self, plots: List[matplotlib.figure.Figure]):
        """
        Saves the validation plots as an image in the local machine.

        Parameters
        ----------
            plots: list
                    This contains matplotlib figures of the plots. 
        """
        plots[0].savefig(
            f"{self.parameters.visualize}/class_scores.png",
            bbox_inches="tight")

        plots[1].savefig(
            f"{self.parameters.visualize}/confusion_matrix.png",
            bbox_inches="tight")

        plots[2].savefig(
            f"{self.parameters.visualize}/prec_rec_curve.png",
            bbox_inches="tight")

    def publish_plots(self, plots: List[matplotlib.figure.Figure], epoch: int = 0):
        """
        Publishes the plots onto tensorboard.

        Parameters
        ----------
            plots: list
                This contains matplotlib figures of the plots. 

            epoch: int
                The epoch number if it is a training model. 
        """
        nimage_class = figure2numpy(plots[0])
        nimage_confusion_matrix = figure2numpy(plots[1])
        nimage_precision_recall = figure2numpy(plots[2])

        self.tensorboard_writer(
            nimage_class,
            f"{self.metric_summary.model}_scores.png",
            step=epoch)
        self.tensorboard_writer(
            nimage_confusion_matrix,
            f"{self.metric_summary.model}_confusion_matrix.png",
            step=epoch)
        self.tensorboard_writer(
            nimage_precision_recall,
            f"{self.metric_summary.model}_precision_recall.png",
            step=epoch)