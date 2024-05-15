# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from typing import Union
import numpy as np

def crop_frame_bbxarea(
        image: np.ndarray, gt_box: Union[list, np.ndarray]) -> np.ndarray:
    """
    Crops the frame to include only the bounding box that surrounds 
    the object of interest for pose validation.
    
    Parameters
    ----------
        image: np.ndarray
            The frame to crop before feeding to the model.

        gt_box: list or np.ndarray
            This contains non-normalized [xmin, ymin, xmax, ymax].

    Returns
    -------
        box_area: np.ndarray
            The frame cropped to the area of the bounding box. 
    """
    x1, y1, x2, y2  = gt_box
    box_area = image[y1:y2, x1:x2, ...]
    return box_area