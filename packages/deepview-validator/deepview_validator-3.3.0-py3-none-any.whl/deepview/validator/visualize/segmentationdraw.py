# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from deepview.validator.datasets import Instance

from PIL import Image, ImageDraw, ImageFont
import numpy as np

colors = np.array(
    [[180, 0, 0],
    [178, 179, 0],
    [142, 206, 70],
    [127, 96, 166],
    [2, 1, 181],
    [3, 152, 133],
    [121, 121, 121],
    [76, 0, 0],
    [240, 0, 0],
    [107, 123, 61],
    [245, 185, 0],
    [94, 78, 127],
    [202, 2, 202],
    [105, 153, 199],
    [252, 155, 209],
    [53, 76, 32],
    [146, 76, 17],
    [0, 166, 76],
    [0, 219, 99],
    [2, 71, 128]], np.uint8)

font = ImageFont.load_default()

def polygon2masktransform(nimage: np.ndarray, polygons: list) -> Image.Image:
    """
    Given a set of polygons, the provided image will be masked with these 
    polygons. 

    Parameters
    ----------
        nimage: np.ndarray
            This is the image as a numpy array.

        polygons: list
            This is the list of polgons 
            [ [cls, x1, y1, x2, y2, x3, y3, ...] ...].

    Returns
    -------
        image_mask: Image
            This is the image with masks overlaid.
    """
    image = Image.fromarray(np.uint8(nimage))
    image = image.convert("RGBA")
    mask = Image.new('RGBA', image.size, (255, 255, 255, 0))
    mask_draw = ImageDraw.Draw(mask)

    for polygon in polygons:
        mask_draw.polygon(polygon, fill=(0, 0, 255, 125))
        image_mask = Image.alpha_composite(image, mask)

    image_mask = image_mask.convert("RGB")
    return image_mask

def duo_image_mask(
        nimage: np.ndarray, 
        dt_polygons: list, 
        gt_polygons: list) -> Image.Image:
    """
    Masks the original image and returns the masked image 
    with mask predictions on the left and ground truth 
    masks on the right. 

    Parameters
    ----------
        nimage: np.ndarray
            The original image as a numpy array.

        dt_polygons: list
            A list of predictions with polygon vertices
            [ [cls, x1, y1, x2, y2, x3, y3, ...] ...].

        gt_polygons: list
            A list of ground truth with polygon vertices
            [ [cls, x1, y1, x2, y2, x3, y3, ...] ...].

    Returns
    -------
        image: Image
            The image with drawn mask where the left
            pane shows the ground truth mask and the right pane shows the
            prediction mask.
    """
    dt_mask = polygon2masktransform(nimage, dt_polygons)
    gt_mask = polygon2masktransform(nimage, gt_polygons)
    dst = Image.new('RGB', (dt_mask.width + gt_mask.width, dt_mask.height))
    dst.paste(dt_mask, (0, 0))
    dst.paste(gt_mask, (dt_mask.width, 0))
    return dst

def mask2imagetransform(
        mask: np.ndarray, 
        labels: list, 
        union: bool=False) -> Image.Image:
    """
    Transform a numpy array of mask into an RGBA image.
    
    Parameter
    ---------
        mask: (height, width, 3) np.ndarray
            Array representing the mask.

        labels: list
            The list of prediction integer labels in the mask.

        union: bool
            Specify to mask all objects with one color (True). Otherwise
            each label in the mask have distinct colors.

    Returns
    -------
        image: PIL Image object
            The masked image.
    """
    # Transform dimension of masks from a 2D numpy array to 4D with RGBA channels.
    mask_4_channels = np.stack((mask,) * 4, axis=-1)

    if union:
        # Assign all classes with color white.
        mask_4_channels[mask_4_channels == 1] = 255
        # Temporarily unpack the bands for readability.
        red, green, blue, _ = mask_4_channels.T
        # Areas of all classes.
        u_areas = (red == 255) & (blue == 255) & (green == 255)
        # Color all classes with blue.
        mask_4_channels[..., :][u_areas.T] = (0, 0, 255, 130)
    else:
        labels = np.sort(np.unique(labels))
        for label in labels:
            if label != 0:
                # Designate a color for each class.
                mask_4_channels[mask_4_channels == label] = \
                    colors[label][0]
        
        # Temporarily unpack the bands for readability.
        red, green, blue, _ = mask_4_channels.T
        for label in labels:
            if label != 0:
                # Find object areas ... (leaves alpha values alone...).
                object_areas = (red == colors[label][0]) &\
                (blue == colors[label][0]) & (green == colors[label][0])
                # Transpose back needed.
                mask_4_channels[..., :][object_areas.T] = \
                    np.append(colors[label], 130)
        
    # Convert array to image object for image processing.
    return Image.fromarray(mask_4_channels.astype(np.uint8))

def maskimage(nimage: np.ndarray, instance: Instance):
    """
    Masks the original image and returns the original image 
    with mask prediction on the left and mask ground truth on the right.
    
    Parameters
    ----------
        nimage: np.ndarray
            This is the image to draw masks on as a numpy array.

        instance: Instance
            An object container of the masks. This can either be a ground truth
            or a prediction instance. Only one of the either masks are being
            drawn. 

    Returns
    -------
        image: PIL Image object
            The image with drawn masks.
    """
    image = Image.fromarray(np.uint8(nimage))
    # Convert array to image object for image processing.
    mask = mask2imagetransform(instance.mask, instance.labels)
    # convert img to RGBA mode.
    image = image.convert("RGBA")     
    mask_image = Image.alpha_composite(image, mask)
    mask_image = mask_image.convert("RGB")
    dst = Image.new('RGB', (mask_image.width, mask_image.height))
    dst.paste(mask_image, (0, 0))
    return dst

def mask2maskimage(
        gt_instance: Instance, 
        dt_instance: Instance, 
        image: Image.Image=None) -> Image.Image:
    """
    Masks the original image and returns the original image 
    with mask prediction on the left and mask ground truth on the right.
    
    Parameters
    ----------
        gt_instance: Instance
            This object contains the ground truth mask.

        dt_instance: Instance
            This object contains the predictions mask.

        image: Image.Image
            This is optional to draw on this image instead of the image
            stored in the ground truth instance.

    Returns
    -------
        image: Image.Image
            The image with drawn masks where on the right pane
            shows the ground truth mask and on the left pane shows
            the prediction mask.
    """
    if image is None:
        image = gt_instance.image
        image = Image.fromarray(np.uint8(image))

    # Create image from numpy masks.
    mask_gt = mask2imagetransform(gt_instance.mask, gt_instance.labels)
    mask_dt = mask2imagetransform(dt_instance.mask, dt_instance.labels)

    image_gt = image.convert("RGBA")
    image_dt = image.convert("RGBA")
    mask_image_gt = Image.alpha_composite(image_gt, mask_gt).convert("RGB")
    mask_image_dt = Image.alpha_composite(image_dt, mask_dt).convert("RGB")
    
    dst = Image.new(
        'RGB', 
        (mask_image_dt.width+mask_image_gt.width, mask_image_dt.height))
    dst.paste(mask_image_gt, (0, 0))
    dst.paste(mask_image_dt, (mask_image_dt.width, 0))

    draw_text = ImageDraw.Draw(dst)
    draw_text.text(
        (0, 0), "GROUND TRUTH", font=font, align='left', fill=(0, 0, 0))
    draw_text.text(
        (mask_image_dt.width, 0), 
        "MODEL PREDICTION", 
        font=font, align='left', fill=(0, 0, 0))
    return dst