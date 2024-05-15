# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from __future__ import annotations
from typing import TYPE_CHECKING, Tuple
if TYPE_CHECKING:
    from deepview.validator.metrics import SegmentationDataCollection
    from deepview.validator.metrics import MetricSummary, PlotSummary
    from deepview.validator.metrics import SegmentationLabelData

from deepview.validator.metrics.core import Metrics
import numpy as np

class SegmentationMetrics(Metrics):
    """
    Provides methods to calculate:: \

        1. precision = true predictions / all predictions.
        2. recall = true predictions / all ground truths.
        3. accuracy = true predictions / all ground truths and all predictions.

    Parameters
    ----------
        segmentationdatacollection: SegmentationDataCollection
            This contains the number of true predictions and false predictions
            per class.
    """
    def __init__(
        self,
        data_collection: SegmentationDataCollection,
        plot_summary: PlotSummary,
        metric_summary: MetricSummary
    ):
        super(SegmentationMetrics, self).__init__()
        self.data_collection = data_collection
        self.plot_summary = plot_summary
        self.metric_summary = metric_summary

    def get_overall_metrics(self) -> Tuple[float, float, float]:
        """
        Computes the overall segmentation accuracy.
        Overall segmentation accuracy  = true predictions pixels / union pixels.

        Returns
        -------
            overall segmentation precision: float
                This is the true prediction pixels / total predictions.

            overall segmentation recall: float
                This is the true prediction pixels / total ground truths. 

            overall segmentation accuracy: float
                This is the true prediction pixels / union pixels. The union
                pixels is the number of ground truths | predictions.
        """
        precision, recall, accuracy = 0.,0.,0.
        precision = self.metric_summary.true_predictions / self.metric_summary.predictions
        recall = self.metric_summary.true_predictions / self.metric_summary.ground_truths
        accuracy = self.metric_summary.true_predictions / self.metric_summary.union
        return precision, recall, accuracy
    
    def get_class_metrics(
            self, 
            label_data: SegmentationLabelData) -> Tuple[float, float, float]:
        """
        Returns the precision, recall, and accuracy metrics of a specific 
        class.

        Parameters
        ----------
            label_data: SegmentationLabelData
                This object contains the true predictions and false predictions
                of a specific class.

        Returns
        -------
            precision: float
                This is the true predictions / all predictions for this
                class.
            
            recall: float
                This is the true predictions / all ground truths for this
                class.

            accuracy: float
                This is the true predictions / all ground truths and predictions
                for this class.
        """
        precision, recall, accuracy = 0.,0.,0.
        if label_data.true_predictions > 0:
            precision = label_data.true_predictions / label_data.predictions
            recall = label_data.true_predictions / label_data.ground_truths
            accuracy = label_data.true_predictions / label_data.union
        return precision, recall, accuracy
    
    def run_metrics(self):
        """
        Method process for gathering all metrics used for the segmentation
        validation.
        """
        nc = len(self.data_collection.label_data_list)
        ap, ar, aacc = 0.,0.,0.
        
        if nc > 0:
            for label_data in self.data_collection.label_data_list:
                precision, recall, accuracy = self.get_class_metrics(label_data)
                ap += precision
                ar += recall
                aacc += accuracy

                data = {'precision': precision,
                        'recall': recall,
                        'accuracy': accuracy,
                        'true_predictions': label_data.true_predictions,
                        'false_predictions': label_data.false_predictions,
                        'gt': label_data.ground_truths}
                
                self.plot_summary.append_class_histogram_data(
                    label_data.label, data)

            self.metric_summary.average_precision = ap/nc
            self.metric_summary.average_recall = ar/nc
            self.metric_summary.average_accuracy = aacc/nc

            precision, recall, accuracy = self.get_overall_metrics()
            self.metric_summary.overall_precision = precision
            self.metric_summary.overall_recall = recall
            self.metric_summary.overall_accuracy = accuracy

        else:
            data = {'precision': np.nan,
                    'recall'   : np.nan,
                    'accuracy' : np.nan,
                    'true_predictions': 0,
                    'false_predictions': 0,
                    'gt': 0}
            self.plot_summary.append_class_histogram_data("No label", data)