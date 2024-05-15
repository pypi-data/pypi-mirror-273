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

from deepview.validator.exceptions import MissingLibraryException
from deepview.validator.writers.core import Writer
import numpy as np
import os

class TensorBoardWriter(Writer):
    """
    Used to publish the images and the metrics onto TensorBoard.
    
    Parameters
    ----------
        logdir: str
            This is the path to save the tfevents file.

        writer: TensorboardWriter
            If this is provided, then this object will be used to write
            onto Tensorboard.
    """
    def __init__(
        self,
        logdir: str=None,
        writer: TensorBoardWriter=None
        ):
        super(TensorBoardWriter, self).__init__()

        self.error_message = ("TensorFlow library is needed to " + 
                              "allow tensorboard functionalities")
        try:
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
            import tensorflow as tf
        except ImportError:
            raise MissingLibraryException(self.error_message)

        self.logdir = logdir
        self.writer = writer
        if logdir:
            self.writer = tf.summary.create_file_writer(self.logdir)

    def __call__(self, image: np.ndarray, image_path: str, step: int=0):
        """
        When it is called, it publishes the images onto tensorboard.
        
        Parameters
        ----------
            image: (height, width, 3) np.ndarray
                The image array to display to tensorboard.

            image_path: str
                The path to the image.

            step: int
                This represents the number of the current 
                epoch when training a model. For standalone validation, 
                set as 0.
        """
        try:
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
            import tensorflow as tf
        except ImportError:
            raise MissingLibraryException(self.error_message)

        with self.writer.as_default():
            nimage = np.expand_dims(image, 0)
            tf.summary.image(os.path.basename(image_path), nimage, step=step)
            self.writer.flush()

    def publish_metrics(
            self,
            summary: MetricSummary,
            parameters: Parameters=None,
            validation_type: str="detection",
            step: int=0
        ) -> Tuple[str, str, str]:
        """
        Publishes the validation metrics onto tensorboard.
       
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
                Either 'detection', 'segmentation' or 'pose'

            step: int
                This is the iteration number which represents the
                epoch number when training a model.
        
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
        try:
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
            import tensorflow as tf
        except ImportError:
            raise MissingLibraryException(self.error_message)

        with self.writer.as_default():
            if validation_type.lower() == 'detection':
                header, summary, timings = self.format_detection_summary(
                    summary, parameters)
            elif validation_type.lower() == 'segmentation':
                header, summary, timings = self.format_segmentation_summary(
                    summary, parameters)
            elif validation_type.lower() == 'pose':
                header, summary, timings = self.format_pose_summary(
                    summary, parameters)

            tf.summary.text(
                header,
                summary,
                step=step)
            
            if timings is not None:
                tf.summary.text(
                    "Timing Results",
                    timings,
                    step=step)
                
            self.writer.flush()
        return header, summary, timings