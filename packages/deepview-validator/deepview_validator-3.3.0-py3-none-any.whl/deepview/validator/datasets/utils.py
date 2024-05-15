# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.exceptions import UnsupportedDatasetTypeException
from deepview.validator.exceptions import DatasetNotFoundException
from deepview.validator.exceptions import MissingLibraryException
from deepview.validator.exceptions import EmptyDatasetException
from deepview.validator.datasets.core import Dataset
from deepview.validator.writers import logger
from typing import Union, Tuple
from PIL import Image
import numpy as np
import glob
import os

coco_label_sync = {
    "motorbike": "motorcycle",
    "aeroplane": "airplane",
    "sofa": "couch",
    "pottedplant": "potted plant",
    "diningtable": "dining table",
    "tvmonitor": "tv"
}

def read_image(image_path: str) -> np.ndarray:
    """
    Opens the image using pillow.Image and if the image is neither in the 
    format: [RGB, RGBA, CMYK, YCVCr] then the image will be converted to RGB.

    Parameters
    ----------
        image_path: str
            The path to the image to read.
    
    Returns
    -------
        image: np.ndarray
            The image represented as a numpy array.
    """
    image = Image.open(image_path)
    if image.mode in ["RGB", "RGBA", "CMYK", "YCbCr"]:
        image = np.asarray(image)
    else:
        image.convert("RGB")
        image = np.asarray(image, dtype=np.uint8)
        image = np.stack((image,)*3, axis=-1)
    return image

def letterbox_yolox(
        image: np.ndarray, input_size: np.ndarray):
    """
    This function performs image letterbox using the implementation provided
    in YOLOx: https://github.com/Megvii-BaseDetection/YOLOX/blob/main/yolox/data/data_augment.py#L142

    Parameters
    ----------
        image: np.ndarray
            This is the input image for letterbox transformation.

        input_size: np.ndarray
            This is the model input size (generally) or the output image 
            resolution after letterbox transformation.

    Returns
    -------
        image: np.ndarray
            The image after letterbox transformation.

        r: float
            Ratio to adjust model bounding boxes due to the letterbox
            transformations.
    """
    if len(image.shape) == 3:
        padded_image = np.ones((input_size[0], input_size[1], 3), dtype=np.uint8) * 114
    else:
        padded_image = np.ones(input_size, dtype=np.uint8) * 114

    r = min(input_size[0] / image.shape[0], input_size[1] / image.shape[1])
    resized_image = resize(image, (int(image.shape[0] * r), int(image.shape[1] * r)), Image.BILINEAR)
    padded_image[: int(image.shape[0] * r), : int(image.shape[1] * r)] = resized_image
    padded_image = Dataset.rgb2bgr(padded_image) # RGB2BGR 
    padded_image = np.ascontiguousarray(padded_image, dtype=np.float32)
    return padded_image, r

def resize(
        image: Union[str, np.ndarray], 
        size: tuple=None, 
        resample: int=None
    ) -> np.ndarray:
    """
    Resizes the images depending on the size passed.

    Parameters
    ----------
        image: (height, width, 3) np.ndarray or str
            The image represented as a numpy array.
            The path to the image that can be opened using pillow.

        size: (height, width) tuple
            Specify the size to resize.

        resample: int
            This is the type of resampling method in PIllow by default it 
            is Image.NEAREST set to 0. However, other forms are Image.BILINEAR
            set to 2.

    Returns
    -------
        image: (height, width, 3) np.ndarray
            Resized image.

    Raises
    ------
        ValueError
            Raised if the provided image is not a 
            np.ndarray or the given string image path does not exist.
    """
    if size is None:
        return image

    # Resize method requires (width, height)
    size = (size[1], size[0])
    if isinstance(image, str):
        if os.path.exists(image):
            img = Image.open(image)
            if resample is not None:
                img = img.resize(size, resample)
            else:
                img = img.resize(size)
            return np.asarray(img)
        else:
            raise ValueError(
                "The given image path does not exist at {}".format(image))
    elif isinstance(image, np.ndarray):
        img = Image.fromarray(np.uint8(image))
        if resample is not None:
            img = img.resize(size, resample)
        else:
            img = img.resize(size)
        return np.asarray(img)
    else:
        raise ValueError(
            "The image provided is neither a " +
            "numpy array or a pillow image object. " +
            "Recieved type: {}".format(type(image)))

def get_image_files(directory_path: str, check_empty: bool=True) -> list:
    """
    Gets all the path of the image files within the specified directory.

    Parameters
    ----------
        directory_path: str
            The path to the directory containing the images.
        
        check_empty: bool
            If this is true, it will raise an error if there are no images
            found at the path provided.

    Returns
    -------
        images: list
            The list of all image paths found with various extensions.

    Raises
    ------
        EmptyDatasetException
            This exception is raised if no images were found in the 
            directory.
    """
    images = list()
    for ext in ['*.[pP][nN][gG]', '*.[jJ][pP][gG]', '*.[jJ][pP][eE][gG]']:
        partial = glob.glob(os.path.join(directory_path, ext))
        images += partial

    if check_empty and len(images) == 0:
        raise EmptyDatasetException(
            f"There are no images found in {directory_path}"
        )
    return sorted(images)

def get_arrow_files(directory_path: str, check_empty: bool=True) -> Tuple[list, list]:
    """
    Gets all the path of the arrow boxes and images files 
    within the specified directory.

    Parameters
    ----------
        directory_path: str
            The path to the directory containing the arrow files.
        
        check_empty: bool
            If this is true, it will raise an error if there are no arrow 
            files found at the path provided.

    Returns
    -------
        images: list
            The list of all arrow image paths found.

        boxes: list
            The list of all arrow boxes paths found.

    Raises
    ------
        EmptyDatasetException
            This exception is raised if no images were found in the 
            directory.
    """
    images = glob.glob(os.path.join(directory_path, "images_*.arrow"))
    boxes = glob.glob(os.path.join(directory_path, "boxes_*.arrow"))

    if check_empty and (len(images) == 0 and len(boxes) == 0):
        raise EmptyDatasetException(
            f"There are no arrow files found in {directory_path}"
        )
    return images, boxes
    
def contains_annotations(annotations: list) -> bool:
    """
    Checks if the detected annotation files are actual darknet annotations.

    Parameters
    ----------
        annnotations: list
            This contains paths of annotations files.

    Returns
    -------
        :py:class:`bool`: This is true if the annotations are indeed image
        annotations, else it is returned as False.
    """
    non_annotation_files = ["readme.txt", "labels.txt"] #NOSONAR

    if len(annotations) == 0:
        return False
    if len(annotations) == 1:
        # For additional, extranneous non annotation files, add it here.
        for non_annotation in non_annotation_files:
            if non_annotation in [os.path.basename(annotations[0]).lower()]:
                return False
        return True
    elif len(annotations) == 2:
        detected_files = sorted([os.path.basename(annotation).lower() for annotation in annotations])
        non_annotation_files = sorted(non_annotation_files)
        # For additional, extranneous non annotation files, add it here.
        return non_annotation_files != detected_files
    else:
        return True

def get_annotation_files(
        directory_path: str, 
        check_empty: bool=True
        ) -> list:
    """
    Gets all the path of the image files within the specified directory.

    Parameters
    ----------
        directory_path: str
            The path to the directory containing the images.

        check_empty: bool
            If this is true, it will raise an error if there 
            are no annotations found at the path provided.

    Returns
    -------
        annotations: list
            The list of annotation paths found as either text or json files.

    Raises
    ------
        EmptyDatasetException
            This exception is raised if no images were found in the 
            directory.
    """
    annotations = list()
    for ext in ['*.txt', '*.json']:
        annotations = glob.glob(os.path.join(directory_path, ext))
        if contains_annotations(annotations):
            break
        else:
            continue
    
    if check_empty and len(annotations) == 0:
        raise EmptyDatasetException(
            f"There are no text or JSON files found in {directory_path}"
        )
    return annotations

def validate_dataset_source(source: str) -> str:
    """
    Validates the existance of the source path.

    Parameters
    ----------
        source: str
            The path to the dataset.

    Returns
    -------
        source: str
            The validated path to the dataset.

    Raises
    ------
        DatasetNotFoundException
            Raised if the provided source to the dataset does not exist.

        ValueError
            Raised if the provided source to the dataset is not a string.
    """
    if not (isinstance(source, str)):
        raise ValueError(
            "The provided path to the dataset is not a string. " +
            "Recieved type: {}".format(
                type(source)))
    
    if not os.path.exists(source):
        raise DatasetNotFoundException(source)
    return source
        
def read_yaml_file(file_path: str, local: bool):
    """
    Reads yaml files internal to AuZone for collecting
    dataset information.

    Parameters
    ----------
        file_path: str
            The path to the yaml file.
        
        local: bool
            Specify if True to use local dataset readers. Otherwise,
            use deepview-datasets by default.

    Returns
    -------
        info_dataset: dict
            This contains the yaml file contents.
            
    Raises
    ------
        MissingLibraryException
            Raised if the yaml library is not installed in the system.
            
        FileNotFoundError
            Raised if the provided path to the file does not exist.
    """
    if local:
        try:
            import yaml
        except ImportError:
            raise MissingLibraryException(
                "The yaml library is needed to read yaml files.")
        if not os.path.exists(file_path):
            raise FileNotFoundError("The yaml file is not found at: {}".format(
                file_path))
        with open(file_path) as file:
            return yaml.full_load(file)
    else:
        from deepview.datasets.generators import ObjectDetectionGenerator
        handler = ObjectDetectionGenerator(
            from_config=file_path # config is the path to the yaml file
        )
        ds_iterator = handler.get_val_generator()
        return ds_iterator

def find_yaml_file(source: str):
    """
    Finds yaml files inside a directory. Returns the path to the yaml file
    if it exists, otherwise it returns None.

    Parameters
    ----------
        source: str
            The path to the directory to start to looking.
    
    Returns
    -------
        The path to the yaml file if it exists. Otherwise it returns None.
    """
    for root, _, files in os.walk(source):
        for file in files:
            if os.path.splitext(file)[1] == ".yaml":
                return os.path.join(root, file)
    return None

def find_labels_file(
        source: str, 
        labels_path: str=None, 
        labels_file: str="labels.txt") -> list:
    """
    Finds the labels file inside the directory if the source is given. 
    Otherwise if the labels_path is given, it will check if the file exists. 

    Parameters
    ----------
        source: str
            The path to the directory to search for labels.txt

        labels_path: str
            The path to the labels.txt file if known.

        labels_file: str
            The name of the labels file to search.

    Returns
    -------
        labels: list
            This is the list of labels that are the 
            contents of the labels file. If the label file is not found, 
            it will return an empty list.
    """
    labels = []
    # Check if labels.txt is under /dataset_path (source)/labels.txt.
    if os.path.exists(os.path.join(source, labels_file)):
        labels_path = os.path.join(source, labels_file)
    # Check if labels.txt path is explicitly provided.
    elif labels_path is not None:
        labels_path = validate_dataset_source(labels_path)
    # If labels.txt is not found, then search through the dataset.
    else:
        for root, _, files in os.walk(source):
            if labels_file in files:
                labels_path = os.path.join(root, labels_file)
        # Continue validation without the label file.
        if labels_path is None:  
            logger("The file labels.txt could not be found.", 
                    code="WARNING")
        
    if labels_path is not None:
        with open(labels_path) as file:
            labels = [line.rstrip().lower() 
                      for line in file.readlines() 
                      if line not in ["\n", "", "\t"]]
    return labels

def create_info(
    image_source: str,
    annotation_source: str,
    type: str=None,
    labels: list=[],
) -> dict:
    """
    This creates info dataset which is a dictionary
    containing the dataset information. This dictionary is formatted
    based on contents of standard dataset yaml files.

    Parameters
    ----------
        image_source: str
            This is the path to the images.

        annotation_source: str
            This is the path to the annotation files.

        type: str
            This is the type of the dataset ["darknet", "arrow"].

        labels: list
            This contains unique string labels.

    Returns
    -------
        info_dataset: dict
            Contains dataset information.
    """
    info_dataset = dict()
    info_dataset["type"] = type
    info_dataset["classes"] = labels
    info_dataset["validation"] = {
        "images": image_source,
        "annotations": annotation_source
    }
    return info_dataset

def create_polar_info(
    image_source: str,
    annotation_source: str,
    type: str=None,
    labels: list=[],
):
    """
    This creates info dataset which is a dictionary
    containing the dataset information. This dictionary is formatted
    based on contents of polar dataset yaml files.

    Parameters
    ----------
        image_source: str
            This is the path to the images.

        annotation_source: str
            This is the path to the annotation files.

        type: str
            This is the type of the dataset ["darknet", "arrow"].

        labels: list
            This contains unique string labels.

    Returns
    -------
        info_dataset: dict
            Contains dataset information.
    """
    info_dataset = {
        "dataset": dict()
    }
    info_dataset["dataset"]["format"] = type
    info_dataset["dataset"]["classes"] = labels
    info_dataset["dataset"]["validation"] = {
        "images": image_source,
        "annotations": annotation_source
    }
    return info_dataset

def collect_tfrecord_files(source: str, labels: list=[]):
    """
    Searches the source directory provided to gather tfrecord files.

    Parameters
    ----------
        source: str
            The path to the directory to search for tfrecord files.

        labels: list
            The list of string labels to include in the dataset information.

    Returns
    -------
        info_dataset: dict
            This includes the path found for the tfrecord files and the labels.
            If no tfecord files were found, then None is returned. 
    """
    tfrecord_files = glob.glob(os.path.join(source, "*.tfrecord"))
    if len(tfrecord_files) > 0:
        # There are no polar yaml representations defined yet.
        info_dataset = dict()
        info_dataset["classes"] = labels
        info_dataset["validation"] = { "path": source }
        return info_dataset
    return None

def collect_darknet_files(source: str, labels: list=[], local: bool=False):
    """
    Searches the source directory provided to gather images and text or json
    files for darknet datasets.

    Parameters
    ----------
        source: str
            The path to the directory to search for 
            images and annotation files.

        labels: list
            The list of string labels to include in the dataset information.

        local: bool
            Specify to use local dataset readers in validator. Otherwise
            by default, use deepview-datasets.

    Returns
    -------
        info_dataset: dict
            This includes the paths found for the images and the annotation 
            files and the labels. If no images were found, 
            then None is returned. 
    """
    for location in ["", "images/validate"]:
        image_source = os.path.join(source, location)
        images = get_image_files(image_source, False)
        if len(images) > 0:
            break
    
    for location in ["", "labels/validate"]:
        annotation_source = os.path.join(source, location)
        annotations = get_annotation_files(annotation_source, False)
        if len(annotations) > 0:
            break
    
    if len(images) == 0:
        return None
    
    if local:
        return create_info(
            image_source, 
            annotation_source, 
            "darknet",
            labels
        )
    else:
        from deepview.datasets.readers.darknet import DarknetDetectionReader
        return DarknetDetectionReader(
            images=image_source,
            annotations=annotation_source,
            classes=labels,
            silent=True
        )
    
def collect_arrow_files(source: str, labels: list=[], local: bool=False):
    """
    Searches the source directory provided to gather images and text or json
    files for darknet datasets.

    Parameters
    ----------
        source: str
            The path to the directory to search for arrow files.

        labels: list
            The list of string labels to include in the dataset information.

        local: bool
            Specify to use local dataset readers in validator. Otherwise
            by default, use deepview-datasets.

    Returns
    -------
        info_dataset: dict
            This includes the paths found for the images and the boxes arrow
            files and the labels. If no arrow files were found, 
            then None is returned. 
    """
    for location in ["", "validate"]:
        source = os.path.join(source, location)
        images, boxes = get_arrow_files(source, False)
        if len(images) > 0 and len(boxes):
            break
    
    if len(images) == 0 and len(boxes) == 0:
        return None
    
    image_source = os.path.join(source, "images_*.arrow")
    boxes_source = os.path.join(source, "boxes_*.arrow")

    if local:
        return create_info(
            image_source, 
            boxes_source, 
            "arrow",
            labels
        )
    else:
        from deepview.datasets.readers.arrow import PolarsDetectionReader
        return PolarsDetectionReader(
            inputs=image_source,
            annotations=boxes_source,
            classes=labels,
            silent=True
        )
    
def classify_dataset( #NOSONAR
        source: str, 
        labels_path: str=None, 
        local: bool=False
    ) -> dict: 
    """
    Inspects the \*.yaml file contents if it exists.
    Otherwise it will search for either images with text
    annotations (Darknet) or tfrecord files (TFRecord Dataset).

    Parameters
    ----------
        source: str
            The validated path to the dataset.
            This can point to a yaml file or a directory containing
            tfrecords or images and text annotations.

        labels_path: str
            The path to the labels.txt (if provided).

        local: bool
            Specify to use the local validator reader instead of 
            deepview-datasets.

    Returns
    -------
        info_dataset: dict, Iterator
            This dictionary contains the paths of the dataset files
            either the tfrecords or the images and the annotation files.
            This dictionary also contains the string labels if it exists.

            This is an object from deepview-datasets that iterates through
            the dataset, if not specifying the local reader. 

    Raises
    ------
        UnsupportedDatasetTypeException
            Raised if the yaml file specifies a dataset type that 
            is not recognized. Can only recognize (darknet or tfrecord).

        EmptyDatasetException
            Raised if the path provided does not contain 
            any tfrecords, images, or text annotations.

        NotImplementedError
            Certain dataset formats is currently not implemented.
    """
    source = validate_dataset_source(source)

    if os.path.isdir(source):
        """Handle AuZoneNet and AuZoneTFRecords format."""
        # Check if a dataset yaml file is inside the directory.
        yaml_file = find_yaml_file(source)
        if yaml_file:
            return read_yaml_file(yaml_file, local)

        # Find and read the contents of the labels file.
        labels = find_labels_file(source, labels_path)
                
        """Handle standard TFRecord datasets."""
        info_dataset = collect_tfrecord_files(source, labels)
        if info_dataset: return info_dataset

        """Handle standard Darknet datasets."""
        info_dataset = collect_darknet_files(source, labels, local)
        if info_dataset: return info_dataset

        """Handle Arrow datasets."""
        info_dataset = collect_arrow_files(source, labels, local)
        if info_dataset: 
            return info_dataset
        else:
            raise EmptyDatasetException(
                "info_dataset returned None. " + 
                f"Check if the path provided ({source}) contains " + 
                "either tfrecord files or images and annotations files."
            )
    elif os.path.isfile(source):
        if os.path.splitext(os.path.basename(source))[1] == ".yaml":
            return read_yaml_file(source, local)
        
        elif os.path.splitext(os.path.basename(source))[1] == ".txt":
            raise NotImplementedError(
                "Single text file is not currently supported.")
        elif os.path.splitext(source)[1] == ".deepview":
            raise NotImplementedError(
                "Deepview files are not currently supported.")
        else:
            UnsupportedDatasetTypeException(source)
    else:
        UnsupportedDatasetTypeException(source)

def standardize_coco_labels(labels: Union[list, np.ndarray]) -> list:
    """
    This converts synonyms of coco labels to standard coco labels using the
    provided labels mapping "coco_label_sync". This requires that the labels 
    provided to contain strings.

    Parameters
    ----------
        labels: list or np.ndarray
            This contains a list of string labels to map to 
            standard coco labels.
    
    Returns
    -------
        synced_labels: list
            This returns converted string labels to standard coco labels based
            from its synonym.
    """
    synced_labels = list()
    for label in labels:
        for key in coco_label_sync.keys():
            if label == key:
                label = coco_label_sync[key]
        synced_labels.append(label)
    return synced_labels