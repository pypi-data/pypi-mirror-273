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
    from deepview.validator.datasets import Dataset
    from deepview.validator.runners import Runner

from deepview.validator.exceptions import UnsupportedModelExtensionException
from deepview.validator.exceptions import UnsupportedValidationTypeException
from deepview.validator.exceptions import UnsupportedApplicationException
from deepview.validator.exceptions import UnsupportedModelTypeException
from deepview.validator.writers import logger, set_symbol_condition
from deepview.validator.datasets.utils import classify_dataset
from deepview.validator.datasets import instantiate_dataset
from deepview.validator.evaluators import Parameters
from deepview.validator import version
import argparse
import datetime
import os


def select_score_threshold(args):
    """
    Two parameters are provided for controlling detection score threshold and
    validation score threshold.

    For detection, there is "detection_score" and "detection_threshold".
    For validation, there is "validation_score" and "validation_threshold".

    This function ensures both parameters are read.

    Parameters
    ----------
        args: argparse.Namespace
            This contains the arguments set in the commandline.

    Returns
    -------
        validation_score: float
            The validation score threshold set in the command line.

        detection_score: float
            The detection score threshold set in the command line.

    Raises
    ------
        ReferenceError
            This is raised if both types of thresholds 
            are set in the commandline.
    """
    if args.validation_score > 0.0 and args.validation_threshold > 0.0:
        raise RuntimeError(
            "Only one of the validation score thresholds should be set.")
    validation_score = (args.validation_score 
                        if args.validation_score > 0.0 
                        else args.validation_threshold)

    detection_score = 0.50
    if args.detection_score is not None and args.detection_threshold is not None:
        raise RuntimeError(
            "Only one of the detection score thresholds should be set.")
    detection_score = (args.detection_score 
                       if args.detection_score is not None 
                       else args.detection_threshold 
                       if args.detection_threshold is not None 
                       else detection_score)
    return validation_score, detection_score


def build_parameters(
        args, validation_score: float, detection_score: float) -> Parameters:
    """
    Store command line arguments inside the Parameters object 
    and the save paths of the validation results.

    Parameters
    ----------
        args: argsparse.NameSpace
            The command line arguments set.

        validation_score: float
            This is the validation score threshold set.

        detection_score: float
            This is the detection score threshold set.

    Returns
    -------
        parameters: Parameters
            The model and validation parameters set that is stored inside 
            the parameters object.
    """
    parameters = Parameters(
        validation_iou=args.validation_iou,
        detection_iou=args.detection_iou,
        validation_score=validation_score,
        detection_score=detection_score,
        engine=args.engine,
        nms=args.nms_type,
        normalization=args.norm,
        box_format=args.box_format,
        warmup=args.warmup,
        label_offset=args.label_offset,
        max_detections=args.max_detection
    )
    parameters.metric = args.metric
    parameters.clamp_boxes = args.clamp_box
    parameters.ignore_boxes = args.ignore_box
    parameters.display = args.display
    parameters.plots = args.exclude_plots
    parameters.validate_3d = args.validate_3d
    parameters.include_background = args.include_background
    parameters.leniency_factor = args.leniency_factor
    parameters.letterbox = args.letterbox
    parameters.auto_offset = args.disable_auto_offset
    parameters.class_filter = args.class_filter

    # Time of validation
    today = datetime.datetime.now().strftime(
        '%Y-%m-%d--%H:%M:%S').replace(":", "_")
    if args.tensorboard:
        parameters.tensorboard = os.path.join(
            args.tensorboard,
            f"{os.path.basename(os.path.normpath(args.model))}_{today}")
    elif args.visualize:
        parameters.visualize = os.path.join(
            args.visualize,
            f"{os.path.basename(os.path.normpath(args.model))}_{today}")
    parameters.json_out = args.json_out

    if args.yolov5:
        parameters.rematching = False
        parameters.iou_first = False
        
    return parameters


def build_dataset(args) -> Type[Dataset]:
    """
    Instantiate the dataset that was passed.

    Parameters
    ----------
        args: argsparse.NameSpace
            The command line arguments set.

    Returns
    -------
        dataset: Dataset
            This is either a DarkNetDataset or TFRecordDataset depending
            on the dataset format that was passed in the command line. 
    """

    # Determine the type of the dataset either as Darknet or TFRecord.
    info_dataset = classify_dataset(
        source=args.dataset,
        labels_path=args.labels_file,
        local=args.local_reader)
    # Build the dataset class depending on the type.
    return instantiate_dataset(
        info_dataset=info_dataset,
        source=args.dataset,
        gformat=args.annotation_format,
        absolute=args.absolute_annotations,
        validate_type=args.validate,
        validate_3d=args.validate_3d,
        show_missing_annotations=args.show_missing_annotations,
        label_offset=args.gt_label_offset,
        local=args.local_reader
        )


def deepviewrt_detection_runner(
        args, labels: list, parameters: Parameters) -> Type[Runner]:
    """
    Instantiate DeepViewRT detection 
    runners based on the different validation types.

    Parameters
    ----------
        args: argsparse.NameSpace
            The command line arguments set.

        dataset: Type[Dataset]
            This is the dataset object that was instantiated. This is used
            to replace the shape based on the model shape returned.

        parameters: Parameters
            These are the model parameters loaded by the command line.

    Returns
    -------
        runner: Type[Runner]
            This is the runner object that is used to run the model. 
    """
    if args.application.lower() == "vaal":
        from deepview.validator.runners import DeepViewRTRunner
        return DeepViewRTRunner(args.model, parameters, labels)

    elif args.application.lower() == "modelclient":
        if args.model_box_type.lower() == 'modelpack':
            from deepview.validator.runners.modelclient import BoxesModelPack
            return BoxesModelPack(args.model,
                                  f"http://{args.target}/v1",
                                  parameters,
                                  labels,
                                  args.decoder)

        elif args.model_box_type.lower() == 'yolo':
            from deepview.validator.runners.modelclient import BoxesYolo
            return BoxesYolo(args.model,
                             f"http://{args.target}/v1",
                             parameters,
                             labels,
                             args.decoder)
        else:
            raise UnsupportedModelTypeException(args.model_box_type)
    else:
        raise UnsupportedApplicationException(args.application)


def deepviewrt_segmentation_runner(
        args, parameters: Parameters) -> Type[Runner]:
    """
    Instantiate DeepViewRT segmentation runners 
    based on the different validation types.

    Parameters
    ----------
        args: argsparse.NameSpace
            The command line arguments set.

        dataset: Type[Dataset]
            This is the dataset object that was instantiated. This is used
            to replace the shape based on the model shape returned.

        parameters: Parameters
            These are the model parameters loaded by the command line.

    Returns
    -------
        runner: Type[Runner]
            This is the runner object that is used to run the model. 
    """
    if args.target is None:
        from deepview.validator.runners import SegmentationDeepViewRTRunner
        return SegmentationDeepViewRTRunner(args.model, parameters)
    else:
        if args.model_segmentation_type.lower() == 'modelpack':
            from deepview.validator.runners.modelclient import SegmentationModelPack
            runner = SegmentationModelPack(
                model=args.model,
                target=f'http://{args.target}/v1',
                parameters=parameters)
            return runner

        elif args.model_segmentation_type.lower() == 'deeplab':
            from deepview.validator.runners.modelclient import SegmentationDeepLab
            runner = SegmentationDeepLab(
                model=args.model,
                target=f'http://{args.target}/v1',
                parameters=parameters)
            return runner


def build_deepviewrt_runner(
        args, labels: list, parameters: Parameters) -> Type[Runner]:
    """
    Instantiate DeepViewRT runners based on the different validation types.

    Parameters
    ----------
        args: argsparse.NameSpace
            The command line arguments set.

        dataset: Type[Dataset]
            This is the dataset object that was instantiated. This is used
            to replace the shape based on the model shape returned.

        parameters: Parameters
            These are the model parameters loaded by the command line.

    Returns
    -------
        runner: Type[Runner]
            This is the runner object that is used to run the model. 
    """
    if args.validate.lower() == "detection":
        return deepviewrt_detection_runner(args, labels, parameters)
    elif args.validate.lower() == "segmentation":
        return deepviewrt_segmentation_runner(args, parameters)
    elif args.validate.lower() == "pose":
        raise NotImplementedError(
            "Pose RTM models is currently not supported.")
    else:
        raise UnsupportedValidationTypeException(args.validate)


def build_keras_runner(
        model: str, validate: str, labels: list, parameters: Parameters) -> Type[Runner]:
    """
    Instantiate Keras runners based on the different validation types.

    Parameters
    ----------
        model: str
            This is the path to the keras model.

        validate: str
            This is the validation type: detection, segmentation, pose

        labels: list
            This is the list of string labels from the dataset.

        parameters: Parameters
            These are the model parameters loaded by the command line.

    Returns
    -------
        runner: Type[Runner]
            This is the runner object that is used to run the model. 
    """
    if validate.lower() == "detection":
        from deepview.validator.runners import DetectionKerasRunner
        return DetectionKerasRunner(model, parameters, labels)

    elif validate.lower() == "segmentation":
        from deepview.validator.runners import SegmentationKerasRunner
        return SegmentationKerasRunner(model, parameters)

    elif validate.lower() == "pose":
        from deepview.validator.runners import PoseKerasRunner
        return PoseKerasRunner(model, parameters)
    else:
        raise UnsupportedValidationTypeException(validate)


def build_tflite_runner(
        args, labels: list, parameters: Parameters) -> Type[Runner]:
    """
    Instantiate TfLite detection runner.

    Parameters
    ----------
        args: argsparse.NameSpace
            The command line arguments set.

        labels: list
            This is the list of string labels from the dataset.

        parameters: Parameters
            These are the model parameters loaded by the command line.

    Returns
    -------
        runner: Type[Runner]
            This is the runner object that is used to run the model. 
    """
    if args.validate.lower() == "detection":
        from deepview.validator.runners import TFliteRunner
        return TFliteRunner(args.model, parameters, labels)
    else:
        raise UnsupportedValidationTypeException(args.validate)


def build_tensorrt_runner(
        args, labels: list, parameters: Parameters) -> Type[Runner]:
    """
    Instantiate TensorRT runners.

    Parameters
    ----------
        args: argsparse.NameSpace
            The command line arguments set.

        labels: list
            This is the list of string labels from the dataset.

        parameters: Parameters
            These are the model parameters set from the command line.

    Returns
    -------
        runner: Type[Runner]
            This is the runner object that is used to run the model. 
    """
    from deepview.validator.runners import TensorRTRunner
    return TensorRTRunner(args.model, parameters, labels)


def build_onnx_runner(args, labels: list, parameters: Parameters) -> Type[Runner]:
    """
    Instantiate PyTorch runners.

    Parameters
    ----------
        args: argsparse.NameSpace
            The command line arguments set.

        labels: list
            This is the list of string labels from the dataset.

        parameters: Parameters
            These are the model parameters set from the command line.

    Returns
    -------
        runner: Type[Runner]
            This is the runner object that is used to run the model. 
    """
    if args.validate.lower() == "detection":
        from deepview.validator.runners import ONNXRunner
        return ONNXRunner(args.model, parameters, labels)
    else:
        raise UnsupportedValidationTypeException(args.validate)
    

def build_hailo_runner(args, labels: list, parameters: Parameters) -> Type[Runner]:
    """
    Instantiate Hailo runners.

    Parameters
    ----------
        args: argsparse.NameSpace
            The command line arguments set.

        labels: list
            This is the list of string labels from the dataset.

        parameters: Parameters
            These are the model parameters set from the command line.

    Returns
    -------
        runner: Type[Runner]
            This is the runner object that is used to run the model. 
    """
    if args.validate.lower() == "detection":
        from deepview.validator.runners import HailoRunner
        return HailoRunner(args.model, parameters, labels)
    else:
        raise UnsupportedValidationTypeException(args.validate)
    

def build_offline_runner(args, labels: list) -> Type[Runner]:
    """
    Instantiate Offline runners.

    Parameters
    ----------
        args: argsparse.NameSpace
            The command line arguments set.

        labels: list
            This is the list of string labels from the dataset.

        detection_score: float
            The detection score threshold set.

    Returns
    -------
        runner: Type[Runner]
            This is the runner object that is used to run the model. 
    """
    from deepview.validator.runners import OfflineRunner
    return OfflineRunner(
        annotation_source=args.model,
        labels=labels,
        validate_type=args.validate,
        validate_3d=args.validate_3d,
        format=args.offline_annotation_format,
        label_offset=args.label_offset)

def find_keras_pb_model(
        model: str, validate: str, labels: list, parameters: Parameters):
    """
    Instantiate Keras runners based on pb model extension.

    Parameters
    ----------
        model: str
            This is the path to the directory to search.

        validate: str
            This is the validation type: detection, segmentation, pose

        labels: list
            This is the list of string labels from the dataset.

        parameters: Parameters
            These are the model parameters loaded by the command line.

    Returns
    -------
        runner: Type[Runner]
            This is the runner object that is used to run the model. 
    """
    runner = None
    for root, _, files in os.walk(model):
        for file in files:
            if os.path.basename(file) == "keras_metadata.pb" or \
                os.path.basename(file) == "saved_model.pb":
                runner = build_keras_runner(
                    root, 
                    validate, 
                    labels, 
                    parameters
                )
                break
    return runner


def main():
    parser = argparse.ArgumentParser(
        description=('Standalone DeepView Validator.'),
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-V', '--version',
                        help="Print the package version.",
                        action='version',
                        version=version()
                        )
    parser.add_argument('--validate',
                        help=("Type of validation to perform: "
                              "'detection', 'segmentation', or 'pose'"),
                        choices=['detection', 'segmentation', 'pose'],
                        default='detection',
                        type=str
                        )
    parser.add_argument('--validate_3d',
                        help="Specify to perform 3D detection validation",
                        action="store_true"
                        )
    parser.add_argument('--application',
                        help=("Type of application to use: "
                              "'vaal' or 'modelclient'."),
                        choices=['vaal', 'modelclient'],
                        default='vaal',
                        type=str
                        )
    parser.add_argument('-d', '--dataset',
                        help=("absolute or relative path "
                              "to the dataset folder or yaml file."),
                        required=True,
                        type=str
                        )
    parser.add_argument('--local_reader',
                        help=('Specify whether to use local validator methods '
                              'for reading datasets. '
                              'Otherwise, by default use deepview-datasets.'),
                        action='store_true')
    parser.add_argument('--letterbox',
                        help='Perform letterbox image preprocessing.',
                        action='store_true')
    parser.add_argument('--labels_file',
                        help=("absolute or relative path "
                              "to the labels.txt file."),
                        type=str
                        )
    parser.add_argument('--gt_label_offset',
                        help=("The label offset to use for the ground truth "
                              "mapping integer labels to string labels. "
                              "This is typically set to 1 for segmentation "
                              "as datasets include the background class."),
                        default=0,
                        type=int
                        )
    parser.add_argument('--include_background',
                        help=("This is primarily used for segmentation. "
                              "This allows evaluation of the "
                              "background class as part of validation."),
                        action="store_true"
                        )
    parser.add_argument('--annotation_format',
                        help=("Specify the format of the annotations: "
                              "'yolo', 'coco', 'pascalvoc'"),
                        choices=['yolo', 'coco', 'pascalvoc'],
                        default='yolo',
                        type=str
                        )
    parser.add_argument('--offline_annotation_format',
                        help=("Specify the format of "
                              "the Offline Runner annotations: "
                              "'yolo', 'coco', 'pascalvoc'"),
                        choices=['yolo', 'coco', 'pascalvoc'],
                        default='yolo',
                        type=str
                        )
    parser.add_argument('--absolute_annotations',
                        help=("This specifies that the annotations "
                              "are not normalized to the image dimensions."),
                        action='store_true'
                        )
    parser.add_argument('--show_missing_annotations',
                        help=("This shows the image names without "
                              "annotations on the terminal"),
                        action='store_true'
                        )
    parser.add_argument('--clamp_box',
                        help=("The value to clamp the minimum width or height "
                              "of the bounding boxes for ground truth and "
                              "predictions in pixels."),
                        type=int
                        )
    parser.add_argument('--ignore_box',
                        help=("Ignore bounding boxes "
                              "for detections and ground truth with height "
                              "or width less than this value in pixels."),
                        type=int
                        )
    parser.add_argument('--metric',
                        help=("Specify the metric to use when "
                              "matching model predictions to ground truth."),
                        choices=['iou', 'centerpoint'],
                        default='iou',
                        type=str
                        )
    parser.add_argument('--leniency_factor',
                        help=("Specify the criteria to consider center "
                              "distances. This is the number of times the "
                              "smallest bounding box diagonal (center to corner) "
                              "should fit in the box-box center distance."),
                        default=2,
                        type=int
                        )
    parser.add_argument('--disable_auto_offset',
                        help=("Disable auto offset of the model indices "
                              "based on its output shape and "
                              "the ground truth labels."),
                        action="store_false")
    parser.add_argument('--class_filter',
                        help=("Filter the model detection classes to match "
                              "the ground truth classes. This should only "
                              "be specified if the model has more classes than "
                              "the dataset."),
                        action='store_true')
    parser.add_argument('-e', '--engine',
                        help=("Compute engine for inference."
                              "'npu', 'gpu', 'cpu'"),
                        choices=['cpu', 'npu', 'gpu'],
                        default='npu',
                        type=str
                        )
    parser.add_argument('--detection_threshold',
                        help=("NMS threshold for valid scores. This parameter "
                              "will overwrite --detection_score"),
                        type=float,
                        )
    parser.add_argument('--detection_score',
                        help=('NMS threshold for valid scores. This parameter '
                              "will overwrite --detection_threshold."),
                        type=float,
                        )
    parser.add_argument('--validation_threshold',
                        help=("Validation score threshold "
                              "to filter predictions. This parameter will "
                              "overwrite --validation_score."),
                        type=float,
                        default=0.0
                        )
    parser.add_argument('--validation_score',
                        help=("Validation score threshold "
                              "to filter predictions. This parameter will "
                              "overwrite --validation_threshold"),
                        type=float,
                        default=0.0
                        )
    parser.add_argument('--detection_iou',
                        help='IoU threshold for NMS.',
                        default=0.50,
                        type=float
                        )
    parser.add_argument('--validation_iou',
                        help=("Validation IoU threshold "
                              "to consider true positives."),
                        default=0.50,
                        type=float
                        )
    parser.add_argument('-l', '--label_offset',
                        help=("Label offset when matching index to label name "
                              "for the predictions."),
                        default=0,
                        type=int
                        )
    parser.add_argument('-b', '--box_format',
                        help=("box format to reorient the prediction "
                              "coordinates: 'xywh', 'xyxy', 'yxyx', etc).\n"),
                        choices=['xywh', 'xyxy', 'yxyx'],
                        default='xyxy',
                        type=str
                        )
    parser.add_argument(
        '-n', '--norm',
        help=(
            'Normalization method applied to input images.'
            '- raw (default, no processing)\n'
            '- unsigned (0...1)\n'
            '- signed (-1...1)\n'
            '- whitening (per-image standardization/whitening)\n'
            '- imagenet (standardization using imagenet)\n'),
        choices=['raw', 'unsigned', 'signed', 'whitening', 'imagenet'],
        default='raw',
        type=str
    )
    parser.add_argument('-m', '--max_detection',
                        help='Number of maximum predictions (bounding boxes).',
                        type=int
                        )
    parser.add_argument('-w', '--warmup',
                        help='The warmup iterations before processing images.',
                        default=0,
                        type=int
                        )
    parser.add_argument('-s', '--nms_type',
                        help=("NMS type to perform validation: "
                              "'standard', 'fast', 'matrix', 'tensorflow'. "
                              "For Keras models, only tensorflow is allowed."),
                        choices=['standard', 'fast', 'matrix', 'tensorflow'],
                        type=str
                        )
    parser.add_argument('--decoder',
                        help=("If the model does not have embedded decoder, "
                              "then apply this parameter in the command line."),
                        action='store_true'
                        )
    parser.add_argument('--model_box_type',
                        help="Type of the box model: 'modelpack', 'yolo'.",
                        choices=['modelpack', 'yolo'],
                        default='modelpack',
                        type=str
                        )
    parser.add_argument('--model_segmentation_type',
                        help=("Type of the Segmentation model: "
                              "'modelpack', 'deeplab'"),
                        choices=['modelpack', 'deeplab'],
                        default='modelpack',
                        type=str
                        )
    parser.add_argument('--target',
                        help=('Provide the modelrunner target.\n'
                              'Ex. 10.10.40.205:10817'),
                        default=None,
                        type=str
                        )
    parser.add_argument('--display',
                        help=("How many images to display into tensorboard. "
                              "By default it is (-1) all the images, "
                              "but an integer can be passed."),
                        default=-1,
                        type=int
                        )
    parser.add_argument('--visualize',
                        help=("Path to store visualizations "
                              "(images with bounding boxes "
                              "or segmentation masks)."),
                        default=None,
                        type=str
                        )
    parser.add_argument('--tensorboard',
                        help=("Path to store *.tfevents files "
                              "needed for tensorboard."),
                        default=None,
                        type=str
                        )
    parser.add_argument('--json_out',
                        help=("Path to save the validation summary "
                              "as a json file on disk."),
                        default=None,
                        type=str
                        )
    parser.add_argument('--exclude_plots',
                        help=("Specify to exclude the plots data in the "
                              "summary and/or save the plots as images if "
                              "visualize or tensorboard parameter is set."),
                        action="store_false"
                        )
    parser.add_argument('--exclude_symbols',
                        help=("Specify whether to exclude symbols when "
                              "logging messages on the terminal."),
                        action="store_false")
    parser.add_argument('--yolov5',
                        help='Run validator with YOLOv5 matching',
                        action='store_true')
    parser.add_argument('model',
                        help=("Model path to the DeepViewRT (rtm), "
                              "Keras (H5), TFlite, TensorRT (trt) "
                              "model to load."),
                        metavar='model.rtm',
                        type=str
                        )
    args = parser.parse_args()

    set_symbol_condition(args.exclude_symbols)
    validation_score, detection_score = select_score_threshold(args)
    parameters = build_parameters(args, validation_score, detection_score)
    dataset = build_dataset(args)

    # DEEPVIEWRT EVALUATION
    if os.path.splitext(args.model)[1].lower() == ".rtm":
        runner = build_deepviewrt_runner(args, dataset.labels, parameters)
    # KERAS EVALUATION
    elif os.path.splitext(args.model)[1].lower() == ".h5":
        runner = build_keras_runner(
            args.model, args.validate, dataset.labels, parameters)
    # TFLITE EVALUATION
    elif os.path.splitext(args.model)[1].lower() == ".tflite":
        runner = build_tflite_runner(args, dataset.labels, parameters)
    # TensorRT Engine Evaluation
    elif os.path.splitext(args.model)[1].lower() == ".trt":
        runner = build_tensorrt_runner(args, dataset.labels, parameters)
    # ONNX EVALUATION
    elif os.path.splitext(args.model)[1].lower() == ".onnx":
        runner = build_onnx_runner(args, dataset.labels, parameters)
    elif os.path.splitext(args.model)[1].lower() == ".hef":
        runner = build_hailo_runner(args, dataset.labels, parameters)
    # Offline EVALUATION (TEXT FILES)
    elif os.path.splitext(args.model)[1].lower() == "":
        runner = find_keras_pb_model(
            args.model, args.validate, dataset.labels, parameters)

        if runner is None:
            logger("Model extension does not exist, reading text files",
                code='INFO')
            parameters.detection_iou = None
            parameters.detection_score = None
            parameters.warmup = None
            parameters.nms = None
            parameters.max_detections = None
            parameters.normalization = None
            parameters.engine = "cpu"
            runner = build_offline_runner(args, dataset.labels)
    else:
        raise UnsupportedModelExtensionException(
            os.path.splitext(args.model)[1].lower())

    """
    Instantiate evaluators. 
    """
    # Detection Evaluation
    if args.validate.lower() == 'detection':
        from deepview.validator.evaluators import DetectionEval
        evaluator = DetectionEval(
            parameters=parameters,
            runner=runner,
            dataset=dataset)
        evaluator.group_evaluation()
        evaluator.conclude()

    # Segmentation Evaluation
    elif args.validate.lower() == 'segmentation':
        from deepview.validator.evaluators import SegmentationEval
        evaluator = SegmentationEval(
            parameters=parameters,
            runner=runner,
            dataset=dataset)
        evaluator.group_evaluation()
        evaluator.conclude()

    # Pose Evaluation
    elif args.validate.lower() == "pose":
        from deepview.validator.evaluators import PoseEval
        evaluator = PoseEval(
            parameters=parameters,
            runner=runner,
            dataset=dataset)
        evaluator.group_evaluation()
        evaluator.conclude()

    else:
        raise UnsupportedValidationTypeException(args.validate)


if __name__ == '__main__':
    """
    Functionalities
        1. Validation of DeepViewRT (RTM).
        2. Validation of Keras (H5) models.
        3. Validation of TFLITE models.
        4. Validation of TensorRT engines (trt).
        5. Validation of two datasets (OfflineRunner).
        6. Compatibility with TFRecord and DarkNet format datasets.
    """
    main()
    