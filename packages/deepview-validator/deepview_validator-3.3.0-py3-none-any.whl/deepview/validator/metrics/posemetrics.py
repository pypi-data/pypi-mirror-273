# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from deepview.validator.metrics import PoseDataCollection
    from deepview.validator.metrics import MetricSummary

from deepview.validator.metrics.core import Metrics
import numpy as np

class PoseMetrics(Metrics):
    """
    Computes the mean squared error between angles for 
    detection and ground truth for pose angles.

    Parameters
    ----------
        data_collection: PoseDataCollection
            This is a container for the prediction and 
            the ground truth angles.
        
        metric_summary: MetricSummary
            Contains the metrics calculated.
    """
    def __init__(
            self, 
            data_collection: PoseDataCollection,
            metric_summary: MetricSummary
        ):
        super(PoseMetrics, self).__init__()
        self.data_collection = data_collection
        self.metric_summary = metric_summary

    def compute_overall_metrics(self) -> np.ndarray:
        """
        Calculates the pose metrics with mean squared error for each angle. 

        Returns
        -------
            overall_metrics: np.ndarray
                This contains the mean squared error for each angle.
        """
        pose_label_data_list = self.data_collection.pose_data_list
        overall_metrics = np.zeros(len(pose_label_data_list))
        for i, pose_data in enumerate(pose_label_data_list):
            overall_metrics[i] = self.mean_absolute_error(
                pose_data.y_true, pose_data.y_pred)
        return overall_metrics
    
    def run_metrics(self):
        """
        Method process for gathering all metrics used for the pose
        validation.
        """
        self.metric_summary.angles_mae = self.compute_overall_metrics()