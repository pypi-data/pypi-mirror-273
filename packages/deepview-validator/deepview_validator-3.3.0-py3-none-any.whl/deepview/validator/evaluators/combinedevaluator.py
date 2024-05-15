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
    from deepview.validator.evaluators import SegmentationEval
    from deepview.validator.writers import TensorBoardWriter
    from deepview.validator.evaluators import DetectionEval
    from deepview.validator.evaluators import PoseEval

from deepview.validator.visualize.segmentationdraw import mask2maskimage
from deepview.validator.visualize.detectiondraw import (
    draw_2d_bounding_boxes, 
    draw_3d_bounding_boxes
)
import numpy as np

class CombinedEvaluator:
    """
    This is allows multiple validation combinations to run on the same image.

    Parameters
    ----------
        detection_evaluator: DetectionEval
            This provides methods for detection validation.

        segmentation_evaluator: SegmentationEval
            This provides methods for segmentation validation.

        pose_evaluator: PoseEval
            This provides methods for pose validation.
    """
    def __init__(
        self,
        detection_evaluator: DetectionEval=None,
        segmentation_evaluator: SegmentationEval=None,
        pose_evaluator: PoseEval=None
    ):
        self.detection_evaluator = detection_evaluator
        self.segmentation_evaluator = segmentation_evaluator
        self.pose_evaluator = pose_evaluator

        if self.detection_evaluator.parameters.validate_3d:
            self.drawer = draw_3d_bounding_boxes
        else:
            self.drawer = draw_2d_bounding_boxes

    def __call__(self, val_messenger: TensorBoardWriter=None):
        """
        Usually for ModelPack purposes of allowing ModelPack 
        tensorboard writer object to operate here. 
        
        Parameters
        ----------
            val_messenger: TensorBoardWriter
                This object handles publishing of validation 
                results into tensorboard.
        """
        self.detection_evaluator(val_messenger)
        self.segmentation_evaluator(val_messenger)
        self.pose_evaluator(val_messenger)
        self.tensorboard_writer = val_messenger

    def single_detection_evaluation(self, instances: dict, epoch: int=0):
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
        """
        self.detection_evaluator.single_evaluation(instances, epoch, False)

    def single_segmentation_evaluation(
        self, 
        instances: dict,
        labels: Union[list, np.ndarray]=None,
        epoch: int=0
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
        """
        self.segmentation_evaluator.single_evaluation(
            instances, labels, epoch, False)

    def single_pose_evaluation(self, instances: dict, epoch: int=0):
        """
        This method runs pose validation a single image evaluation.
        
        Parameters
        ----------
            instances: dict
                The ground truth and the prediction instances.
                
            epoch: int
                Used for training a model the epoch number.
        """
        self.pose_evaluator.single_evaluation(instances, epoch, False)

    def single_evaluation(
        self, 
        detection_instances: dict, 
        segmentation_instances: dict,
        labels: Union[list, np.ndarray]=None,
        epoch: int=0
    ):
        """
        Currently supports segmentation and detection validation combinations.
        Runs detection and segmentation validation operations on the same
        image.

        Parameters
        ----------
            detection_instances: dict
                The ground truth and the prediction detection instances.

            segmentation_instances: dict
                The ground truth and the prediction segmentation instances.

            labels: list or np.ndarray
                    This contains a list of string labels to optionally 
                    convert integer labels to strings.

            epoch: int
                This is the training epoch number. This
                parameter is internal for modelpack usage.
                Standalone validation has no use of this parameter.
        """
        self.detection_evaluator.single_evaluation(
            detection_instances, epoch, False)
        self.segmentation_evaluator.single_evaluation(
            segmentation_instances, labels, epoch, False)

    def publish_image(
            self, 
            detection_instances: dict, 
            segmentation_instances: dict,
            epoch: int=0
    ):
        """
        Currently supports segmentation and detection validation combinations.
        This draws both detection bounding boxes and segmentation masks on 
        the same image.

        Parameters
        ----------
            detection_instances: dict
                The ground truth and the prediction detection instances.

            segmentation_instances: dict
                The ground truth and the prediction segmentation instances.

            epoch: int
                This is the training epoch number. This
                parameter is internal for modelpack usage.
                Standalone validation has no use of this parameter.
        """
        if self.tensorboard_writer:
            image = self.drawer(
                detection_instances.get("gt_instance"),
                detection_instances.get("dt_instance"),
                self.detection_evaluator.metric_summary.image_summaries[-1],
                self.detection_evaluator.parameters.validation_iou,
                self.detection_evaluator.parameters.validation_score
            )
            image = mask2maskimage(
                segmentation_instances.get("gt_instance"),
                segmentation_instances.get("dt_instance"),
                image
            )
            self.tensorboard_writer(
                np.asarray(image), 
                detection_instances.get("gt_instance").image_path, 
                step=epoch)

    def conclude(self, epoch: int=0):
        """
        Currently supports segmentation and detection validation combinations.
        This runs the metrics for detection and segmentation.

        Parameters
        ----------
            epoch: int
                This is the training epoch number. This
                parameter is internal for modelpack usage.
                Standalone validation has no use of this parameter.
        """
        self.segmentation_evaluator.conclude(epoch)
        self.detection_evaluator.conclude(epoch)