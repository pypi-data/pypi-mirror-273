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
    from deepview.validator.metrics import SegmentationDataCollection
    from deepview.validator.metrics import DetectionDataCollection
    from deepview.validator.metrics import PoseDataCollection
    from deepview.validator.evaluators import Parameters
    from deepview.validator.datasets import Dataset
    from deepview.validator.runners import Runner

from deepview.validator.metrics import MetricSummary, PlotSummary, ImageSummary
from deepview.validator.writers import ConsoleWriter, TensorBoardWriter
from deepview.validator.datasets import InstanceCollection
import numpy as np
import json
import os

class Evaluator:
    """
    Abstract class that provides a template for the
    validation evaluations (detection or segmentation).
    
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
        runner: Type[Runner],
        dataset: Type[Dataset],
        parameters: Parameters,
    ):
        self._runner = runner
        self._dataset = dataset
        self._parameters = parameters
        self._data_collection = None

        self._console_writer = ConsoleWriter()
        self._tensorboard_writer = None
        if self._parameters.tensorboard:
            self._tensorboard_writer = TensorBoardWriter(
                self._parameters.tensorboard)

        if self._runner is not None:
            model_name = os.path.basename(os.path.normpath(self.runner.model))
        else:
            model_name = "Training Model"

        if self._dataset is not None:
            dataset_name = os.path.basename(os.path.normpath(self.dataset.source))
        else:
            dataset_name = "Validation Dataset"

        if self._parameters.tensorboard:
            save_path = self._parameters.tensorboard
        elif self._tensorboard_writer:
            save_path = self._tensorboard_writer.logdir
        elif self._parameters.visualize:
            save_path = self._parameters.visualize
        else:
            save_path = None

        self._collected_instances = InstanceCollection()
        self._metric_summary = MetricSummary(
            model=model_name,
            dataset=dataset_name,
        )
        self._plot_summary = PlotSummary()
        self._metric_summary.save_path = save_path

        # This counter is used to determine the number of images saved.
        self._counter = 0

    @property
    def runner(self) -> Type[Runner]:
        """
        Attribute to access the runner object. 
        The runner object provides methods to run the model.
        Can only be set to :py:class:Type[Runner]

        Returns
        -------
            :py:class:Type[Runner]: The runner object.
        """
        return self._runner
    
    @runner.setter
    def runner(self, this_runner: Type[Runner]):
        """
        Sets the runner object.

        Parameters
        ----------
            this_runner: Type[Runner]
                The runner object to set.
        """
        self._runner = this_runner

    @property
    def dataset(self) -> Type[Dataset]:
        """
        Attribute to access the dataset object. 
        The dataset object provides methods to read the dataset.
        Can only be set to :py:class:Type[Dataset]

        Returns
        -------
            :py:class:Type[Dataset]: The dataset object.
        """
        return self._dataset
    
    @dataset.setter
    def dataset(self, this_dataset: Type[Dataset]):
        """
        Sets the dataset object.

        Parameters
        ----------
            this_dataset: Type[Dataset]
                The dataset object to set.
        """
        self._dataset = this_dataset

    @property
    def parameters(self) -> Parameters:
        """
        Attribute to access the parameters object. 
        The parameters object stores model and validation parameters.
        Can only be set to :py:class:Parameters

        Returns
        -------
            :py:class:Parameters: The parameters object.
        """
        return self._parameters
    
    @parameters.setter
    def parameters(self, this_parameters: Parameters):
        """
        Sets the parameters object.

        Parameters
        ----------
            this_parameters: Parameters
                The parameters object to set.
        """
        self._parameters = this_parameters

    @property
    def data_collection(self) -> Union[
        DetectionDataCollection, SegmentationDataCollection, PoseDataCollection]:
        """
        Attribute to access the data collection object. 
        The data collection object stores base metric values for each validation
        type such as total true positives, false positives, or false negatives.
        Can be set to 
        :py:class:DetectionDataCollection
        :py:class:SegmentationDataCollection
        :py:class:PoseDataCollection

        Returns
        -------
            The data collection object.
                :py:class:DetectionDataCollection
                :py:class:SegmentationDataCollection
                :py:class:PoseDataCollection
        """
        return self._data_collection
    
    @data_collection.setter
    def data_collection(self, this_data_collection: Union[
        DetectionDataCollection, SegmentationDataCollection, PoseDataCollection]):
        """
        Sets the data collection object.

        Parameters
        ----------
            this_data_collection: Union[DetectionDataCollection, 
                                        SegmentationDataCollection, 
                                        PoseDataCollection]
                The data collection object to set. 
        """
        self._data_collection = this_data_collection

    @property
    def collected_instances(self) -> InstanceCollection:
        """
        Attribute to access the collected_instances object. 
        The InstanceCollection object stores the validation ground truth
        and prediction instances.
        Can only be set to :py:class:InstanceCollection

        Returns
        -------
            :py:class:InstanceCollection: The collected_instances object.
        """
        return self._collected_instances
    
    @collected_instances.setter
    def collected_instances(self, this_collected_instances: InstanceCollection):
        """
        Sets the collected_instances object.

        Parameters
        ----------
            this_collected_instances: InstanceCollection
                The collected_instances object to set.
        """
        self._collected_instances = this_collected_instances

    @property
    def metric_summary(self) -> MetricSummary:
        """
        Attribute to access the metric summary object. 
        The metric summary object stores the 
        validation summary containing the metrics.
        Can only be set to :py:class:MetricSummary

        Returns
        -------
            :py:class:MetricSummary: The metric summary object.
        """
        return self._metric_summary
    
    @metric_summary.setter
    def metric_summary(self, this_summary: MetricSummary):
        """
        Sets the metric summary object.

        Parameters
        ----------
            this_summary: MetricSummary
                The metric summary object to set.
        """
        self._metric_summary = this_summary

    @property
    def plot_summary(self) -> PlotSummary:
        """
        Attribute to access the plot summary object. 
        The plot summary object stores the 
        data used for plotting validation metrics.
        Can only be set to :py:class:PlotSummary

        Returns
        -------
            :py:class:PlotSummary: The plot summary object.
        """
        return self._plot_summary
    
    @plot_summary.setter
    def plot_summary(self, this_summary: PlotSummary):
        """
        Sets the plot summary object.

        Parameters
        ----------
            this_summary: PlotSummary
                The plot summary object to set.
        """
        self._plot_summary = this_summary

    @property
    def console_writer(self) -> ConsoleWriter:
        """
        Attribute to access the console writer object. 
        The console writer object provides methods to write the 
        validation summary on the terminal. 
        Can only be set to :py:class:ConsoleWriter

        Returns
        -------
            :py:class:ConsoleWriter: The console writer object.
        """
        return self._console_writer
    
    @console_writer.setter
    def console_writer(self, this_console_writer: ConsoleWriter):
        """
        Sets the console writer object.

        Parameters
        ----------
            this_console_writer: ConsoleWriter
                The console writer object to set.
        """
        self._console_writer = this_console_writer

    @property
    def tensorboard_writer(self) -> TensorBoardWriter:
        """
        Attribute to access the tensorboard writer object. 
        The tensorboard writer object provides methods to write the 
        validation summary onto tensorboard.
        Can only be set to :py:class:TensorBoardWriter

        Returns
        -------
            :py:class:TensorBoardWriter: The tensorboard writer object.
        """
        return self._tensorboard_writer
    
    @tensorboard_writer.setter
    def tensorboard_writer(self, this_tensorboard_writer: TensorBoardWriter):
        """
        Sets the tensorboard writer object.

        Parameters
        ----------
            this_tensorboard_writer: TensorBoardWriter
                The tensorboard writer object to set.
        """
        self._tensorboard_writer = this_tensorboard_writer

    @property
    def counter(self) -> int:
        """
        Attribute to access the image count saved so far.
        Can only be set to :py:class:`int`

        Returns
        -------
            :py:class:`int`: The number of images saved so far.
        """
        return self._counter

    @counter.setter
    def counter(self, count: int):
        """
        Sets the counter to a new value.

        Parameters
        ----------
            count: int
                This is the count of the image saved thus far.
        """
        self._counter = count

    def reset(self):
        """
        Resets the metric containers.
        """
        self._collected_instances.reset()
        self._metric_summary.reset()
        self._plot_summary.reset()
        self.data_collection.reset_containers()

    def instance_collector(self):
        """Abstract Method"""
        raise NotImplementedError("This is an abstract method")

    def single_evaluation(self, instance, epoch, add_image):
        """Abstract Method"""
        raise NotImplementedError("This is an abstract method")

    def group_evaluation(self):
        """Abstract Method"""
        raise NotImplementedError("This is an abstract method")

    def conclude(self):
        """Abstract Method"""
        raise NotImplementedError("This is an abstract method")

    def print_types(self, d: Union[dict, list], tabs: int=0):
        """
        Debugs the typing of a data structure that the application 
        is trying to serialize into a JSON file.

        Parameters
        ----------
            d: dict or list
                This is the datastructure to debug for the types.

            tabs: int
                The number of tabs which allows for better formatting 
                showing the nested structures.
        """
        if type(d) == type(dict()):
            for key, value in d.items():
                t = '\t'*tabs
                print(f"{t} {key=}: type: {type(value)}")
                if type(value) == type(dict()) or type(value) == type(list()):
                    self.print_types(value, tabs+1)
        elif type(d) == type(list()):
            for index in range(min(len(d), 4)):
                t = '\t'*tabs
                print(f"{t} {index=}: type: {type(d[index])}")
                if type(d[index]) == type(dict()) or \
                            type(d[index]) == type(list()):
                    self.print_types(d[index], tabs+1)

    def save_metrics_disk(
        self, 
        header: str, 
        format_summary: str, 
        format_timings: str=None
    ):
        """
        Saves the validation metrics onto a text file on disk.

        Parameters
        ----------
            header: str
                The title of the validation metrics.

            format_summary: str
                The formatted validation summary as a 
                table showing the metrics.

            format_timings: str
                The formatted timings summary as a table.
        """
        with open(
            os.path.join(self.parameters.visualize, 'metrics.txt'), 'w') as fp:
            fp.write(header + '\n')
            fp.write(format_summary + '\n')
            if format_timings is not None:
                fp.write(format_timings)
            fp.close()

    def publish_metrics(self, 
                        epoch: int=0, 
                        validation_type: str="detection"
                    ):
        """
        Publishes the metrics onto tensorboard.

        Parameters
        ----------
            epoch: int
                The epoch number when training a model.

            validation_type: str
                The type of validation that is being performed:
                "detection", "segmentation", "pose".
        """
        header, summary, timings = self.tensorboard_writer.publish_metrics(
                        summary=self.metric_summary,
                        parameters=self.parameters,
                        step=epoch,
                        validation_type=validation_type)
        return header, summary, timings
    
    def save_json_summary(self):
        """
        Saves the validation metric summary as a JSON file.

        Parameters
        -------
            confusion_matrix: (nxn) np.ndarray
                The confusion matrix as a table  where the
                rows will contain the prediction labels and the 
                columns contain the ground truth labels.

            unique_labels: list
                This contains the labels that is used to label the confusion
                matrix. This will contains the background class.

            precision_recall_data: dict

                .. code-block:: python

                    {
                        "precision": precision # (nc, score thresholds),
                        "recall": recall # (nc, score thresholds),
                        "average precision": average precision # (nc, iou thresholds)
                        "names": unique labels for each precision and recall array.
                    }
        """
        import json

        summary_dictionary = {key.lstrip('_'): value for key, value in 
            self.metric_summary.__dict__.items() if key != "_image_summaries"}
        summary_dictionary["confusion_labels"] = self.plot_summary.confusion_labels
        summary_dictionary["confusion_matrix"] = self.plot_summary.confusion_matrix
        summary_dictionary["precision"] = self.plot_summary.precision
        summary_dictionary["recall"] = self.plot_summary.recall
        summary_dictionary["ap"] = self.plot_summary.average_precision
        summary_dictionary["curve_labels"] = self.plot_summary.curve_labels

        with open(self.parameters.json_out, 'w', encoding='utf-8') as fp:
            json.dump(
                summary_dictionary,
                fp, 
                cls=NpEncoder, 
                indent=4
            )
            fp.close()
        
class NpEncoder(json.JSONEncoder):
    """
    Encodes numpy arrays in the summary to be JSON serializable.
    The source for this class was retrieved from:: \
    
    https://stackoverflow.com/questions/50916422/python-typeerror-object-of-type-int64-is-not-json-serializable
    """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, ImageSummary):
            return None
        return super(NpEncoder, self).default(obj)