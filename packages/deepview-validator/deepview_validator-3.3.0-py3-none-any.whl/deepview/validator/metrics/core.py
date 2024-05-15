# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from typing import Union
import numpy as np

class Metrics:
    """
    Abstract class that provides a template 
    for basic metric computations.
    """
    @staticmethod
    def compute_precision(tp: int, fp: int) -> float:
        """
        Calculates the precision = tp/(tp+fp).

        Parameters
        ----------
            tp: int
                The number of true positives.

            fp: int
                The number of false positives.

        Returns
        -------
            Precision score: float
                Resulting value is the result of tp/(tp+fp).
        """
        if tp + fp == 0:
            return 0.0
        return tp / (tp + fp)

    @staticmethod
    def compute_recall(tp: int, fn: int) -> float:
        """
        Calculates recall = tp/(tp+fn).

        Parameters
        ----------
            tp: int
                The number of true positives.

            fn: int
                The number of false negatives.

        Returns
        -------
            Recall score: float
                Resulting value is the result of tp/(tp+fn).
        """
        if tp + fn == 0:
            return 0.0
        return tp / (tp + fn)

    @staticmethod
    def compute_accuracy(tp: int, fp: int, fn: int) -> float:
        """
        Calculates the accuracy = tp/(tp+fp+fn).

        Parameters
        ----------
            tp: int
                The number of true positives.

            fp: int
                The number of false positives.

            fn: int
                The number of false negatives.

        Returns
        -------
            Accuracy score: float
                Resulting value is the result of tp/(tp+fp+fn).
        """
        if tp + fp + fn == 0:
            return 0.0
        return tp / (tp + fp + fn)

    @staticmethod
    def mean_squared_error(
            y_true: Union[list, np.ndarray],
            y_pred: Union[list, np.ndarray]) -> float:
        """
        Calculates the mean squared error defined in this source: 
        https://www.geeksforgeeks.org/python-mean-squared-error/

        Parameters
        ----------
            y_true: list or np.ndarray
                The true values.

            y_pred: list or np.ndarray
                The predicted values.

        Returns
        -------
            mean squared error: float
                The mean squared error of the values
                comparing y_pred to y_true.
        """
        return np.square(np.subtract(y_true, y_pred)).mean()

    @staticmethod
    def mean_absolute_error(
            y_true: Union[list, np.ndarray],
            y_pred: Union[list, np.ndarray]) -> float:
        """
        Calculates the mean absolute error defined in this source: 
        https://datagy.io/mae-python/

        Parameters
        ----------
            y_true: list
                The true values.

            y_pred: list
                The predicted values.

        Returns
        -------
            mean absolute error: float
                The mean absolute error of the values
                comparing y_pred to y_true.
        """
        return np.abs(np.subtract(y_true, y_pred)).mean()