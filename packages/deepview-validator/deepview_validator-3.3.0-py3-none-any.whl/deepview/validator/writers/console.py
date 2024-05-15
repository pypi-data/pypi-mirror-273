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
    from deepview.validator.evaluators import Parameters
    from deepview.validator.metrics import MetricSummary

from deepview.validator.writers.core import Writer


class ConsoleWriter(Writer):
    """
    Used to print the metrics on the terminal.
    """

    def __init__(self):
        super(ConsoleWriter, self).__init__()

    def __call__(
        self,
        summary: MetricSummary,
        parameters: Parameters = None,
        validation_type: str = "detection",
    ) -> Tuple[str, str, str]:
        """
        When this is called, it prints the metrics on the console.

        Parameters
        ----------
            summary: Summary
                This summary object contains information 
                regarding the final metrics.

            parameters: Parameters
                This parameters object contains information 
                regarding the model and validation parameters.

            validation_type: str
                This is the type of validation performed.
                Either 'detection', 'segmentation' or 'pose'.

        Returns
        -------
            header: str
                The validation header message.

            summary: str
                The string representation of the summary 
                object formatted as a table.

            timings: str
                The model timings formatted as a table.
        """
        if validation_type.lower() == "detection":
            header, summary, timings = self.format_detection_summary(
                summary, parameters)
        elif validation_type.lower() == "segmentation":
            header, summary, timings = self.format_segmentation_summary(
                summary, parameters)
        elif validation_type.lower() == "pose":
            header, summary, timings = self.format_pose_summary(
                summary, parameters)
        if not parameters.silent:
            print(header)
            print(summary)
            if timings is not None:
                print(timings)
        return header, summary, timings
