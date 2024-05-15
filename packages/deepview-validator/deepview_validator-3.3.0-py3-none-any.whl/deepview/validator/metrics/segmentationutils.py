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
    from deepview.validator.datasets import Instance

from PIL import Image, ImageDraw
import numpy as np

def create_mask_image(
        height: int, width: int, instance: Instance) -> np.ndarray:
    """
    Creates a numpy array of masks from a given list of polygons.
    
    Parameters
    ----------
        height: int
            The height of the image.

        width: int
            The width of the image.

        instance: Instance
            This is a container of the segmentation polygons and 
            segmentation masks.

    Returns
    -------
        Masked image: (height, width) np.ndarray
    """
    polygons = instance.polygons
    labels = instance.labels

    mask = Image.new('L', (width, height), 0)
    for c, polygon in zip(labels, polygons):
        ImageDraw.Draw(mask).polygon(polygon, outline=int(c), fill=int(c))
    # This array contains a mask of the image where the objects are
    # outlined by class number
    return np.array(mask)

def create_binary_mask(mask: np.ndarray) -> np.ndarray:
    """
    Creates a binary numpy array of 1's and 0's encapsulating 
    every object (regardless of class) in the image as a 1 and 
    background as 0.
    
    Parameters
    ----------
        mask: (height, width) np.ndarray
            Mask of class labels unique to each object.

    Returns
    -------
        mask: (height, width) np.ndarray
            Binary mask of 1's and 0's.
    """
    return np.where(mask > 0, 1, mask)

def create_mask_class(mask: np.ndarray, cls: int) -> np.ndarray:
    """
    Separates a mask with more than one classes into an individual 
    mask of 1's and 0's where 1 represents the specified class and 
    0 represents other classes.
    
    Parameters
    ----------
        mask: (height, width) np.ndarray
            Mask of class labels unique to each object.

        cls: int
            The integer representing the class in the mask
            to keep as a value of 1. The other classes will be treated as
            0's.

    Returns
    -------
        temp_mask: (height, width) np.ndarray
            Binary mask of 1's and 0's.
    """
    temp_mask = np.where(mask != cls, 0, mask)
    temp_mask[temp_mask == cls] = 1
    return temp_mask

def create_mask_classes(
        new_mask: np.ndarray, 
        cls: int, 
        current_mask: np.ndarray=None
    ) -> np.ndarray:
    """
    Appends a current mask with another mask of different class 
    i.e converting a binary mask (new mask) into a mask with its 
    class and then appending the original mask to include 
    the new mask with its class.
  
    Parameters
    ----------
        new_mask: (height, width) np.ndarray
            The current binary mask.

        cls: int
            Class representing the 1's in the new mask. This is the class
            to append to the current mask.

        current_mask: (height, width) np.ndarray
            Current multiclass mask.

    Returns
    -------
        multiclass mask: (height, width) np.ndarray
            Mask with an additional class added.
    """
    new_mask = np.where(new_mask == 1, cls, new_mask)
    if current_mask is not None:
        return np.add(current_mask, new_mask)
    else:
        return new_mask

def create_mask_background(mask: np.ndarray) -> np.ndarray:
    """
    Creates a binary mask for the background class with 1's in the 
    image and the rest of the objects will have values of 0's.
    
    Parameters
    ----------
        mask: (height, width) np.ndarray
            Matrix array of classes representing the image pixels.

    Returns
    -------
        mask: (height, width) np.ndarray
            Binary mask of 1's and 0's, where 1's is background and
            objects are 0's
    """
    # 2 is a temporary class
    temp_mask = np.where(mask != 0, 2, mask)
    temp_mask[temp_mask == 0] = 1
    temp_mask[temp_mask == 2] = 0
    return temp_mask

def classify_mask(
        gt_class_mask: np.ndarray, 
        dt_class_mask: np.ndarray, 
        exclude_background: np.ndarray = True
    ) -> Tuple[int, int, int]:
    """
    Classifies if the pixels are either true predictions or false predictions.
    Note the masks provided can also be multiclass, however this function
    is used primarily to find the true predictions and false predictions
    per class.
   
    Parameters
    ----------
        gt_class_mask: (height, width) np.ndarray
            2D binary array representing pixels forming the image ground truth.
            1 represents the class being classified and 0 are the rest of 
            the classes.

        dt_class_mask: (height, width) np.ndarray
            2D binary array representing pixels forming the image prediction.
            1 represents the class being classified and 0 are the rest of 
            the classes.

        exclude_background: bool
            Specify to avoid background to background
            predictions and ground truths as true predictions.

    Returns
    -------
        true_predictions: int
            The number of true predictions pixels in the image.

        false_predictions: int
            The number of false predictions pixels in the image.

        union: int
            The union between ground truths and model predictions occurs
            when both arrays are non-zero. The union is the sum of 
            true predictions and false predictions. 
    """
    gt_mask_flat = gt_class_mask.flatten()
    dt_mask_flat = dt_class_mask.flatten()

    if exclude_background:
        # Do not consider 0 against 0 as true predictions. 0 means another class 
        # not just background. True predictions are 1 against 1 which means this 
        # current class.
        true_predictions = np.sum(
            (gt_mask_flat == dt_mask_flat) & (gt_mask_flat > 0) & (dt_mask_flat > 0))
        
        # The union between ground truths and predictions where both are non-zero.
        union = np.sum((gt_mask_flat != 0) | (dt_mask_flat != 0))
    else:
        true_predictions = np.sum(gt_mask_flat == dt_mask_flat)   
        union = len(gt_mask_flat) 

    false_predictions = np.sum(gt_mask_flat != dt_mask_flat)
    return true_predictions, false_predictions, union