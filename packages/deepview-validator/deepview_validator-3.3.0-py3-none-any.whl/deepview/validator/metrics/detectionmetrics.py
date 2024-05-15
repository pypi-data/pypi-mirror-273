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
    from deepview.validator.metrics import PlotSummary, MetricSummary
    from deepview.validator.datasets import InstanceCollection
    from deepview.validator.evaluators import Parameters
    from deepview.validator.metrics import (
        DetectionDataCollection,
        DetectionLabelData
    )
    
from deepview.validator.metrics.detectionutils import nan_to_last_num
from deepview.validator.evaluators.utils import detection_evaluate
from deepview.validator.metrics.core import Metrics
import numpy as np

class DetectionMetrics(Metrics):
    """
    Provides methods to calculate::

        1. precision.
                -> overall precision.

                -> mAP 0.5, 0.75, 0.5-0.95.
        2. recall.
                -> overall recall.

                -> mAR 0.5, 0.75, 0.5-0.95.
        3. accuracy.
                -> overall accuracy.

                -> mACC 0.5, 0.75, 0.5-0.95.

    Other calculations such as false positive ratios, 
    precision vs recall data are also handled in this class.

    Parameters
    ----------
        data_collection: DetectionDataCollection
            This contains the number of ground truths in
            the dataset and tp, fp, and fn per class.

        collected_instances: InstanceCollection
            This contains the instance objects for both ground truth and 
            detections.

        plot_summary: PlotSummary
            This contains data to be used to generate the plots.

        metric_summary: MetricSummary
            This will be used to store the validation metrics.

        parameters: Parameters
            This contains the model and validation parameters set 
            from the command line.
    """
    def __init__(
        self,
        data_collection: DetectionDataCollection,
        collected_instances: InstanceCollection,
        plot_summary: PlotSummary,
        metric_summary: MetricSummary,
        parameters: Parameters,
    ):
        super(DetectionMetrics, self).__init__()

        self.data_collection = data_collection
        self.collected_instances = collected_instances
        self.plot_summary = plot_summary
        self.metric_summary = metric_summary
        self.parameters = parameters

    def append_classifications(self, label_data: DetectionLabelData):
        """
        Adds the total number of true positives stored in the metric summary
        based on the DetectionLabelData object which is an object that
        represents a particular class label.

        Parameters
        ----------  
            label_data: DetectionLabelData
                This object contains the number of true positives, 
                false positives, and false negatives for a particular class.
        """
        self.metric_summary.true_positives += label_data.get_tp_count(
            self.parameters.validation_iou, self.parameters.validation_score)

        self.metric_summary.classification_false_positives += label_data.get_class_fp_count(
            self.parameters.validation_iou, self.parameters.validation_score)

        self.metric_summary.localization_false_positives += label_data.get_local_fp_count(
            self.parameters.validation_iou, self.parameters.validation_score)

    def get_center_metrics(self) -> dict:
        """
        Calculates the mean absolute error between the center coordinates
        between the ground truth and the prediction bounding boxes. 

        Returns
        -------
            distance_metrics dict
                This is formatted as follows: \

                    .. code-block:: python

                        {
                            "x-center-mae": "mean absolute error of the x-coordinate",
                            "y-center-mae": "mean absolute error of the y-coordinate",
                            "z-center-mae": "mean absolute error of the z-coordinate",
                            "distance-mae": "mean absolute error of the center distances"
                        }  
        """
        distance_metrics = {
            "x-center-mae": np.nan,
            "y-center-mae": np.nan,
            "z-center-mae": np.nan,
            "distance-mae": np.nan,
        }
        center_distances = self.metric_summary.centers.get("center_distances")
        gt_centers = np.array(self.metric_summary.centers.get("gt_centers"))
        dt_centers = np.array(self.metric_summary.centers.get("dt_centers"))

        if len(gt_centers) + len(dt_centers) > 0:
            self.metric_summary.append_centers = True
            x_mae = self.mean_absolute_error(
                gt_centers[:, 0:1], dt_centers[:, 0:1])
            y_mae = self.mean_absolute_error(
                gt_centers[:, 1:2], dt_centers[:, 1:2])
            if (gt_centers.shape[1] > 2 or dt_centers.shape[1] > 2):
                z_mae = self.mean_absolute_error(
                    gt_centers[:, 2:3], dt_centers[:, 2:3])
            else:
                z_mae = np.nan
            distance_mae = sum(center_distances)/len(gt_centers)

            distance_metrics = {
                "x-center-mae": x_mae,
                "y-center-mae": y_mae,
                "z-center-mae": z_mae,
                "distance-mae": distance_mae
            }
        return distance_metrics

    def get_overall_metrics(self) -> Tuple[float, float, float]:
        """
        Returns the overall precision, recall, and accuracy.

            1. overall precision = sum tp / \
                (sum tp + sum fp (localization + classification)).
            2. overall recall = sum tp / \
                (sum tp + sum fn + sum fp (localization)).
            3. overall accuracy  = sum tp / \
                (sum tp + sum fn + sum fp (localization + classification)).
        """
        precision, recall, accuracy = 0., 0., 0.
        if self.metric_summary.true_positives == 0:
            if (self.metric_summary.classification_false_positives +
                    self.metric_summary.localization_false_positives == 0):
                precision = np.nan
            if self.metric_summary.false_negatives == 0:
                recall = np.nan
            if (self.metric_summary.classification_false_positives +
                self.metric_summary.localization_false_positives +
                    self.metric_summary.false_negatives == 0):
                accuracy = np.nan
        else:
            precision = self.compute_precision(
                self.metric_summary.true_positives,
                self.metric_summary.classification_false_positives +
                self.metric_summary.localization_false_positives
            )
            recall = self.compute_recall(
                self.metric_summary.true_positives,
                self.metric_summary.false_negatives +
                self.metric_summary.classification_false_positives
            )
            accuracy = self.compute_accuracy(
                self.metric_summary.true_positives,
                self.metric_summary.classification_false_positives +
                self.metric_summary.localization_false_positives,
                self.metric_summary.false_negatives
            )
        return precision, recall, accuracy

    def get_mean_average_metrics(
        self,
        maps: np.ndarray,
        mars: np.ndarray,
        maccs: np.ndarray,
        nc: int
    ) -> Tuple[list, list, list]:
        """
        Given an array of precision, recall, and accuracy at 0.50 to 0.95 IoU
        thresholds, this will return values only at IoU thresholds, 
        0.50, 0.75, and 0.50-0.95 averages.

        Parameters
        ----------
            maps: np.ndarray (1,20)
                precision values from different IoU thresholds.

            mars: np.ndarray (1,20)
                recall values from different IoU thresholds.

            maccs: np.ndarray (1,20)
                accuracy values from different IoU thresholds.

            nc: int
                The number of classes.

        Returns
        -------
            metric_map: list
                This contains the precision values at IoU thresholds
                0.50, 0.75, 0.50-0.95

            metric_mar: list
                This contains the recall values at IoU thresholds
                0.50, 0.75, 0.50-0.95

            metric_maccs: list
                This contains the accuracy values at IoU thresholds
                0.50, 0.75, 0.50-0.95
        """
        # These arrays are essentially the mAP, mAR, and mACC across the
        # IoU thresholds 0.00 to 1.00 in 0.05 intervals with shape (1, 20).
        if np.isnan(maps).all():
            maps = np.empty(20) * np.nan
        else:
            maps = np.nansum(maps, axis=0) / nc

        if np.isnan(mars).all():
            mars = np.empty(20) * np.nan
        else:
            mars = np.nansum(mars, axis=0) / nc

        if np.isnan(maccs).all():
            maccs = np.empty(20) * np.nan
        else:
            maccs = np.nansum(maccs, axis=0) / nc

        # These are the mAP, mAR, and mACC 0.5-0.95 IoU thresholds.
        map_5095 = np.sum(maps[10:])/10
        mar_5095 = np.sum(mars[10:])/10
        macc_5095 = np.sum(maccs[10:])/10
        # This list contains mAP, mAR, mACC 0.50, 0.75, and 0.5-0.95.
        metric_map = [maps[10], maps[15], map_5095]
        metric_mar = [mars[10], mars[15], mar_5095]
        metric_maccuracy = [maccs[10], maccs[15], macc_5095]
        return metric_map, metric_mar, metric_maccuracy

    def get_class_metrics(
        self,
        label_data: DetectionLabelData,
        validation_score: float,
        validation_iou: float
    ) -> Tuple[np.ndarray, list]:
        """
        Returns the precision, recall, and accuracy metrics and the truth 
        values of a specific class at the set IoU and score thresholds.

        Parameters
        ----------
            label_data: DetectionLabelData
                This is a container of the truth values of a specific class.

            validation_iou: float
                The validation IoU threshold to consider true positives.

            score_threshold: float
                The validation score threshold to consider for predictions.

        Returns
        -------
            class_metrics: np.ndarray (1, 3)
                This contains the values for precision, recall, and accuracy
                of the class representing the label data container.

            class_truth_values: np.ndarray (1, 4)
                This contains the values for true positives, classification
                false positives, localization false positives, and
                false negatives for the class representing the label data
                container. 
        """
        # These are the truth values just for the specified class in the
        # data container: true positives, false positives, and false negatives.
        tp = label_data.get_tp_count(validation_iou, validation_score)
        cfp = label_data.get_class_fp_count(validation_iou, validation_score)
        lfp = label_data.get_local_fp_count(validation_iou, validation_score)
        fn = label_data.get_fn_count(validation_iou, validation_score)

        class_metrics = np.zeros(3)
        class_truth_values = [tp, cfp, lfp, fn]
        if tp == 0:
            if cfp + lfp == 0:
                class_metrics[0] = np.nan
            if fn == 0:
                class_metrics[1] = np.nan
            if cfp + lfp + fn == 0:
                class_metrics[2] = np.nan
        else:
            class_metrics[0] = self.compute_precision(tp, cfp + lfp)
            class_metrics[1] = self.compute_recall(tp, fn)
            class_metrics[2] = self.compute_accuracy(tp, cfp + lfp, fn)
        return class_metrics, class_truth_values

    def get_fp_error(self) -> list:
        """
        Calculates the false positive error ratios:: \

            1. Localization FP Error = Localization FP / \
                                (Classification FP + Localization FP).
            2. Classification FP Error = Classification FP / \
                                (Classification FP + Localization FP).

        *Note: localization false positives are predictions 
        that do no correlate to a ground truth. Classification 
        false positives are predictions with non matching labels.*

        Returns
        -------
            Error Ratios: list
                This contains false positive ratios for
                IoU thresholds (0.5, 0.75, 0.5-0.95).
        """
        local_fp_error, class_fp_error = np.zeros(10), np.zeros(10)
        for it, iou_threshold in enumerate(np.arange(0.5, 1, 0.05)):
            class_fp, local_fp = 0, 0

            label_data: DetectionLabelData
            for label_data in self.data_collection.label_data_list:
                class_fp += label_data.get_class_fp_count(
                    iou_threshold, self.parameters.validation_score)
                local_fp += label_data.get_local_fp_count(
                    iou_threshold, self.parameters.validation_score)

            if local_fp + class_fp == 0:
                local_fp_error[it] = np.nan
                class_fp_error[it] = np.nan
            else:
                local_fp_error[it] = local_fp / (local_fp + class_fp)
                class_fp_error[it] = class_fp / (local_fp + class_fp)

        return [local_fp_error[0], class_fp_error[0],
                local_fp_error[5], class_fp_error[5],
                np.sum(local_fp_error) / 10, np.sum(class_fp_error) / 10]

    def group_evaluation(self):
        """
        This is used for the precision-recall curve which will 
        run through each score threshold and performs the validator 
        evaluation based on the filtered detections. 

        *Note: This method behaves the same as the one in DetectionEvaluator, 
        but redefined here to resolve circular imports. However, 
        both methods call the same function "detection_evaluate" which 
        should avoid any differences in the changes between both methods.*
        """
        # Reset the data.
        self.data_collection.reset_containers()
        gt_instances = self.collected_instances.gt_instances
        dt_instances = self.collected_instances.dt_instances

        for gt_instance, dt_instance in zip(gt_instances, dt_instances):
            detection_evaluate(gt_instance,
                               dt_instance,
                               self.parameters,
                               self.data_collection,
                               verbose_store=False,
                               restore=True)

    def get_pr_data(self, eps: float = 1e-16, interval: float = 0.01): #NOSONAR
        """
        This performs a loop through different thresholds which runs
        validation at each threshold. This process is timely because 
        many score thresholds will need to be evaluated.

        Parameters
        ----------  
            eps: float
                The smallest acceptable value for the score threshold.

            interval: float
                This is the interval between score thresholds.

        Returns
        -------
            precision_recall_data: dict
                The following container is formatted as follows: \

                    .. code-block:: python

                        {
                            "precision": precision # (nc, score thresholds),
                            "recall": recall # (nc, score thresholds),
                            "average precision": average precision # (nc, iou thresholds)
                            "names": unique labels 
                        }
        """
        # For the score thresholds to include 1, the max score should be 1+interval.
        score_min, score_max = eps, 1. + interval
        score_thresholds = np.arange(score_min, score_max, interval)

        original_score_threshold = self.parameters.validation_score
        # The labels captured based on the validation iterations.
        if len(self.data_collection.unfiltered_labels) == 0:
            self.plot_summary.precision = np.zeros((0, len(score_thresholds)+2))
            self.plot_summary.recall = np.zeros((0, len(score_thresholds)+2))
            self.plot_summary.average_precision = np.zeros((0, 10))
            return 
     
        if (isinstance(self.data_collection.unfiltered_labels, list)
                and "background" in self.data_collection.unfiltered_labels):
            self.data_collection.unfiltered_labels.remove("background")

        elif (self.data_collection.unfiltered_labels.dtype.type is np.str_
                and "background" in self.data_collection.unfiltered_labels):
            labels = self.data_collection.unfiltered_labels
            self.data_collection.unfiltered_labels = np.delete(
                labels, np.nonzero(labels == "background"))

        nc = len(self.data_collection.unfiltered_labels)
        names = self.data_collection.unfiltered_labels

        # Precision and recall, rows = classes, columns = range of thresholds.
        # The extra two lengths are for the assertion of values of 1.
        self.plot_summary.precision = np.zeros((nc, len(score_thresholds)+2))
        self.plot_summary.recall = np.zeros((nc, len(score_thresholds)+2))
        # Assert the last value for precision is 1 and the first value for recall is 1.
        self.plot_summary.precision[:, -1], self.plot_summary.recall[:, 0] = 1, 1
        # Average Precision, rows = classes, columns = range of IoUs (0.5-0.95).
        self.plot_summary.average_precision = np.zeros((nc, 10))

        if self.parameters.silent:
            for ti, score_t in enumerate(score_thresholds):
                self.build_pr_data(original_score_threshold,
                                score_t, ti, nc, names)
        else: 
            try:
                from tqdm import tqdm
                thresholds = tqdm(score_thresholds, colour="blue")
                thresholds.set_description("Building PR Curve")
                # Iterate the range of thresholds.
                for ti, score_t in enumerate(thresholds):
                    self.build_pr_data(original_score_threshold,
                                    score_t, ti, nc, names)
            except ImportError:
                num = len(score_thresholds)
                # Iterate the range of thresholds.
                for index in range(num):
                    print("\t - [INFO]: Computing metrics for image: " +
                        "%i of %i [%2.f %s]" %
                        (index + 1,
                        num,
                        100 * ((index + 1) / float(num)),
                        '%'), end='\r')
                    self.build_pr_data(original_score_threshold,
                                    score_t, ti, nc, names)

        # This portion replaces NaN values with the last acceptable values.
        # This is necessary so that the lengths are the same for both
        # precision and recall.
        for ci in range(nc):
            self.plot_summary.precision[ci] = nan_to_last_num(
                self.plot_summary.precision[ci])
            self.plot_summary.recall[ci] = nan_to_last_num(
                self.plot_summary.recall[ci])

        self.parameters.validation_score = original_score_threshold
        self.plot_summary.curve_labels = names

    def build_pr_data(
        self,
        original_score_threshold: float,
        score_threshold: float,
        ti: int,
        nc: int,
        names: list
    ):
        """
        Computes the precision and recall based on varying score thresholds.

        Parameters
        ----------
            original_score_threshold: float
                The validation score threshold set from the command line
                which is used to consider displaying the average precision 
                values on the plot. 

            score_threshold: float
                The score threshold to evaluate the instances as part
                of the array of score thresholds.

            ti: int
                The index of the score threshold.

            nc: int
                The number of classes captured during validation.

            names: list
                These contain the unique string labels.
        """
        self.parameters.validation_score = score_threshold
        self.group_evaluation()

        # Precision and recall for each class at this threshold.
        class_precision, class_recall = np.zeros(nc), np.zeros(nc)

        # Iterate through each data and grab precision and recall.
        for label_data in self.data_collection.label_data_list:
            class_metrics, _ = self.get_class_metrics(
                label_data, score_threshold, self.parameters.validation_iou)

            # The index to store the precision and recall based on class.
            current_label = label_data.label

            # Grab the index of the current label in the list.
            ci = np.argwhere(names == current_label)
            class_precision[ci] = class_metrics[0]
            class_recall[ci] = class_metrics[1]

            if round(score_threshold, 2) == round(original_score_threshold, 2):
                # AP from precision-recall curve based on the validation score threshold set.
                self.plot_summary.average_precision[ci, :] = self.compute_ap_iou(
                    label_data, original_score_threshold)

        # Due to the assertion of the values of 1 for precision and recall,
        # the actual threshold starts at the offset of 1.
        self.plot_summary.precision[:, ti+1] = class_precision
        self.plot_summary.recall[:, ti+1] = class_recall

    def compute_ap_iou(self, label_data: DetectionLabelData, score_threshold: float):
        """
        Computes the precision for a specific class 
        at 10 different iou thresholds.

        Parameters
        ----------
            label_data: DetectionLabelData
                A container for the number of tp, fp, and fn for the label.

            score_threshold: float
                The score threshold to consider for predictions.

        Returns
        -------
            precision: np.ndarray
                precision values for each IoU threshold (0.5-0.95).
        """
        # Precision values for the IoU thresholds 0.5 to 1.0 at 0.05 intervals.
        precision = np.zeros(10)
        for i, iou_threshold in enumerate(np.arange(0.5, 1, 0.05)):
            tp = label_data.get_tp_count(iou_threshold, score_threshold)
            class_fp = label_data.get_class_fp_count(
                iou_threshold, score_threshold)
            local_fp = label_data.get_local_fp_count(
                iou_threshold, score_threshold)
            if tp != 0:
                precision[i] = self.compute_precision(
                    tp, class_fp + local_fp)
        return precision

    def run_metrics(self):
        """
        Method process for gathering all metrics used for the detection
        validation.
        """
        self.metric_summary.mae_centers = self.get_center_metrics()
        nc = len(self.data_collection.label_data_list)

        # These arrays contain the metrics for each class where the rows
        # represent the class and the columns represent the IoU thresholds:
        # 0.00 to 1.00 in 0.05 intervals.

        px, py, ap, unique_classes = DetectionMetrics.ap_per_class(
            np.array(self.data_collection.tp),
            np.array(self.data_collection.conf),
            np.array(self.data_collection.pred_cls),
            np.array(self.data_collection.target_cls)
        )
        # Used for plotting precision recall curve.
        self.plot_summary.precision = py
        self.plot_summary.recall = px
        self.plot_summary.average_precision = ap
        self.plot_summary.curve_labels = unique_classes

        ap50, ap75, ap = ap[:, 0], ap[:, 5], ap.mean(1)  # AP@0.5, AP@0.5:0.95
        maps, mars, maccs = np.zeros((nc, 20)), np.zeros((nc, 20)), np.zeros((nc, 20))

        if nc > 0:
            for ic, label_data in enumerate(self.data_collection.label_data_list):
                self.append_classifications(label_data)

                class_metrics, class_truth_values = self.get_class_metrics(
                    label_data,
                    self.parameters.validation_score,
                    self.parameters.validation_iou)
                data = {'precision': class_metrics[0],
                        'recall': class_metrics[1],
                        'accuracy': class_metrics[2],
                        'tp': class_truth_values[0],
                        'fn': class_truth_values[3],
                        'fp': class_truth_values[1] + class_truth_values[2],
                        'gt': label_data.ground_truths
                        }
                self.plot_summary.append_class_histogram_data(
                    str(label_data.label), data)

                for it, iou_threshold in enumerate(np.arange(0.00, 1, 0.05)):
                    class_metrics, _ = self.get_class_metrics(
                        label_data,
                        self.parameters.validation_score,
                        iou_threshold)
                    # The index of the class ic and the index of the IoU
                    # threshold it will contain the metric: precision, recall,
                    # and accuracy of the class.
                    mars[ic][it] = class_metrics[1]
                    maccs[ic][it] = class_metrics[2]
                    # This mAP computation is the average of the precision 
                    # of each class.
                    # maps[ic][it] = class_metrics[0] #NOSONAR

            mean_metrics = self.get_mean_average_metrics(maps, mars, maccs, nc)
            self.metric_summary.map = {"0.50": 0.0 if np.isnan(ap50.mean()) else ap50.mean(),
                                       "0.75": 0.0 if np.isnan(ap75.mean()) else ap75.mean(),
                                       "0.50:0.95": 0.0 if np.isnan(ap.mean()) else ap.mean()}
            self.metric_summary.mar = {"0.50": mean_metrics[1][0],
                                       "0.75": mean_metrics[1][1],
                                       "0.50:0.95": mean_metrics[1][2]}
            self.metric_summary.macc = {"0.50": mean_metrics[2][0],
                                        "0.75": mean_metrics[2][1],
                                        "0.50:0.95": mean_metrics[2][2]}

            overall_metrics = self.get_overall_metrics()
            self.metric_summary.overall_precision = overall_metrics[0]
            self.metric_summary.overall_recall = overall_metrics[1]
            self.metric_summary.overall_accuracy = overall_metrics[2]

            false_positive_ratios = self.get_fp_error()
            self.metric_summary.classification_fp_error = {
                "0.50": false_positive_ratios[1],
                "0.75": false_positive_ratios[3],
                "0.50:0.95": false_positive_ratios[5]}

            self.metric_summary.localization_fp_error = {
                "0.50": false_positive_ratios[0],
                "0.75": false_positive_ratios[2],
                "0.50:0.95": false_positive_ratios[4]}
        else:
            data = {'precision': np.nan,
                    'recall': np.nan,
                    'accuracy': np.nan,
                    'tp': 0,
                    'fn': 0,
                    'fp': 0,
                    'gt': 0
                    }
            self.plot_summary.append_class_histogram_data("No label", data)

    """The following methods were taken from YoloV5 to match the mAP metric
    which is the area under the curve.
    https://github.com/ultralytics/yolov5/blob/master/utils/metrics.py#L29
    """
    @staticmethod
    def ap_per_class(
        tp: np.ndarray, 
        conf: np.ndarray, 
        pred_cls: np.ndarray, 
        target_cls: np.ndarray, 
        eps: float=1e-16
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Compute the average precision, given the recall and precision curves.
        Source:: https://github.com/rafaelpadilla/Object-Detection-Metrics.

        Parameters
        ----------
            tp: np.ndarray 
                True positives (nparray, nx1 or nx10).

            conf:  np.ndarray 
                Objectness value from 0-1 (nparray).

            pred_cls: np.ndarray
                Predicted object classes (nparray).

            target_cls: np.ndarray 
                True object classes (nparray).

            eps: float
                Prevents 0/0 division.

        Returns
        -------
            px: np.ndarray
                Recall for the curve.

            py: np.ndarray
                Precision for the curve.

            ap: np.ndarray
                The average precision as computed in py-faster-rcnn.

            unique_classes: np.ndarray
                Labels for the curve.
        """
        i = np.argsort(-conf)
        tp, conf, pred_cls = tp[i], conf[i], pred_cls[i]
        # Find unique classes
        unique_classes, nt = np.unique(target_cls, return_counts=True)
        nc = unique_classes.shape[0]  # number of classes, number of detections

        # Create Precision-Recall curve and compute AP for each class
        px, py = np.linspace(0, 1, 1000), []  # for plotting
        ap, p, r = np.zeros((nc, 10)), np.zeros(
            (nc, 1000)), np.zeros((nc, 1000))
        for ci, c in enumerate(unique_classes):
            i = np.nonzero(pred_cls == c)[0]
            n_l = nt[ci]  # number of labels
            n_p = i.sum()  # number of predictions
            if n_p == 0 or n_l == 0:
                continue

            # Accumulate FPs and TPs
            fpc = (1 - tp[i]).cumsum(0)
            tpc = tp[i].cumsum(0)
            # Recall
            recall = tpc / (n_l + eps)  # recall curve
            # negative x, xp because xp decreases
            r[ci] = np.interp(-px, -conf[i], recall[:, 0], left=0)

            # Precision
            precision = tpc / (tpc + fpc)  # precision curve
            p[ci] = np.interp(-px, -conf[i], precision[:, 0],
                              left=1)  # p at pr_score

            # AP from recall-precision curve
            for j in range(tp.shape[1]):
                ap[ci, j], mpre, mrec = DetectionMetrics.compute_ap(
                    recall[:, j], precision[:, j])
                if j == 0:
                    py.append(np.interp(px, mrec, mpre))  # precision at mAP@0.5
        return px, py, ap, unique_classes

    @staticmethod
    def smooth(y, f=0.05):
        # Box filter of fraction f
        # number of filter elements (must be odd)
        nf = round(len(y) * f * 2) // 2 + 1
        p = np.ones(nf // 2)  # ones padding
        yp = np.concatenate((p * y[0], y, p * y[-1]), 0)  # y padded
        return np.convolve(yp, np.ones(nf) / nf, mode="valid")  # y-smoothed

    @staticmethod
    def compute_ap(recall: np.ndarray, precision: np.ndarray):
        """
        Compute the average precision, given the recall and precision curves.

        Parameters
        ----------
            recall: np.ndarray   
                The recall curve (list).

            precision: np.ndarray
                The precision curve (list).

        Returns
        ------- 
            ap: np.ndarray
                The average precision as the area under the curve.

            mpre: np.ndarray
                mean precision.

            mrec: np.ndarray
                mean recall.
        """
        # Append sentinel values to beginning and end
        mrec = np.concatenate(([0.0], recall, [1.0]))
        mpre = np.concatenate(([1.0], precision, [0.0]))

        # Precision curve
        mpre = np.maximum.accumulate(mpre[::-1])[::-1]

        x = np.linspace(0, 1, 101)
        ap = np.trapz(np.interp(x, mrec, mpre), x)
        return ap, mpre, mrec