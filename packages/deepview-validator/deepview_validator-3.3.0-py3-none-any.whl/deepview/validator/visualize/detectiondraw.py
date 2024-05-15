# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, Union
if TYPE_CHECKING:
    from deepview.validator.metrics import ImageSummary
    from deepview.validator.datasets import Instance

from PIL import Image, ImageDraw, ImageFont
import numpy as np

messages = {
            "Match": "%s %.2f%% %.2f",  # Format (label, score, iou)
            "Match Loc": "LOC: %s %.2f%% %.2f", # Format (label, score, iou)
            "Loc": "LOC: %s %.2f%%", # Format (label, score)
            "Clf": "CLF: %s %.2f%% %.2f", # Format (label, score, iou)
        }
font = ImageFont.load_default()

def draw_rect(
        image_draw: ImageDraw.ImageDraw, 
        selected_corners: np.ndarray, 
        color: str, 
        width: int=2
    ):
    """
    This is primarily used for drawing 3D bounding boxes which consists of 
    2 rectangles and 4 lines particularly speaking.

    Parameters
    ----------
        image_draw: ImageDraw.ImageDraw
            The object that loaded the image to draw rectangles on.

        selected_corners: np.ndarray
            This contains the corners of the 3D bounding box with shape
                (3,8) representing the (x,y,z) 8 corners of a 3D box.

        color: str
            The color to use for the line.

        width: int
            This is the width of the line forming the rectangle. 
    """
    prev = selected_corners[-1]
    for corner in selected_corners:
        image_draw.line(
            ((int(prev[0]), int(prev[1])), (int(corner[0]), int(corner[1]))),
            fill=color,
            width=width
        )
        prev = corner

def draw_3d_bounding_box(
        image_draw: ImageDraw.ImageDraw, 
        corners: np.ndarray, 
        color: str="RoyalBlue", 
        width: int=2
    ):
    """
    Draw 3D bounding boxes which consists of 2 rectangles and 4 lines 
    particularly speaking.

    Parameters
    ----------
        image_draw: ImageDraw.ImageDraw
            The object that loaded the image to draw rectangles on.

        corners: np.ndarray
            This contains the corners of the 3D bounding box with shape
                (3,8) representing the (x,y,z) 8 corners of a 3D box.

        color: str
            The color to use for the line.

        width: int
            This is the width of the line forming the rectangle. 
    """
    for i in range(4):
        image_draw.line(
            ((int(corners.T[i][0]), int(corners.T[i][1])),  
            (int(corners.T[i + 4][0]), int(corners.T[i + 4][1]))),
            fill=color,
            width=2)
    draw_rect(image_draw, corners.T[:4], color, width)
    draw_rect(image_draw, corners.T[4:], color, width)

def draw_2d_bounding_box(
        image_draw: ImageDraw.ImageDraw, 
        box_position: tuple, 
        color: str="RoyalBlue", 
        width: int=3
    ):
    """
    Draws a 2D bounding box on the image loaded.

    Parameters
    ----------
        image_draw: ImageDraw.ImageDraw
            The object that loaded the image to draw bounding box on.

        box_position: tuple
            ((x1, y1), (x2, y2)) position of the box.

        color: str
            The color of the bounding box. Typically, 
            ground truth/false negatives is set to "RoyalBlue", 
            false positives is set to "OrangeRed",
            true positives is set to "LimeGreen".

        width: int
            The width of the line to draw the bounding boxes.
    """
    image_draw.rectangle(
        box_position,
        outline=color,
        width=width)
    
def draw_text(
        image_draw: ImageDraw.ImageDraw, 
        text: str,
        text_position: tuple,
        font: ImageFont,
        color: str="black", 
        align: str="left",
        background_position: tuple=None, 
        background_color: str="RoyalBlue"
    ):
    """
    This function will write the text on the image and will also optionally
    draw a 2D box overlay as the background of the text 
    to make it more visible.

    Parameters
    ----------
        image_draw: ImageDraw.ImageDraw
            The object that loaded the image to write text on.

        text: str
            The text to write on the image.

        text_position: tuple
            This is the (x, y) position on the image to write the text.

        font: ImageFont
            This is the font of the text.

        color: str
            This is the color of the text.

        align: str
            This is the text alignment. 

        background_position: tuple
            This is the ((x1, y1), (x2, y2)) position to draw the background
            box of the text.

        background_color: str
            This is the color of the background. it is recommended to align the 
            colors with the bounding boxes to make it clear which text 
            corresponds to which.
    """
    if background_position:
        image_draw.rectangle(
            background_position,
            fill=background_color)
    image_draw.text(
        text_position,
        text,
        font=font,
        align=align,
        fill=color
        )

def position_2d_text_background(
        text: str, 
        font: ImageFont,
        text_position: tuple, 
        box_position: tuple
    ) -> Tuple[tuple, tuple]:
    """
    This positions the background of the text to make it aligned with the 
    2d bounding box.

    Parameters
    ----------
        text: str
            The text that will be drawn on the image.

        font: ImageFont
            The type of font to use.

        text_position: tuple
            This contains the (x, y) position of the text.

        box_position: tuple
            This contain the ((x1, y1), (x2, y2)) position 
            of the 2D bounding box.

    Returns
    -------
        background_position: tuple
            This is the ((x1, y1), (x2, y2)) position of the text background.

        text_position: tuple
            This is the (x,y) position of the text aligned to the background.
    """
    if hasattr(font, 'getsize'): # works on older Pillow versions < 10.
        text_width, text_height = font.getsize(text)
    else:
        (text_width, text_height), _ = font.font.getsize(text) # newer Pillow versions >= 10.

    box_text_x1 = box_position[0][0]
    box_text_x2 = box_text_x1 + text_width

    # This suggests a ground truth text is being drawn where the label is 
    # located in the bottom left of the bounding box.
    if text_position[1] > box_position[0][1]:
        box_text_y1 = box_position[1][1] - text_height
    # A prediction text is being drawn where the labels is located 
    # in the top left of the bounding box.
    else:
        box_text_y1 = box_position[0][1] 
        # The +10 keeps the text within the bounding box.
        text_position = (text_position[0], text_position[1] + 10) 

    box_text_y2 = box_text_y1 + text_height
    return ((box_text_x1, box_text_y1), (box_text_x2, box_text_y2)), text_position

def position_3d_text_background(
        text: str, 
        font: ImageFont,
        text_position: tuple, 
        color: str = "RoyalBlue"
    ) -> Tuple[tuple, tuple]:
    """
    This positions the background of the text to make it aligned to the 
    3d bounding box.

    Parameters
    ----------
        text: str
            The text that will be drawn on the image.

        font: ImageFont
            The type of font to use.

        text_position: tuple
            This contains the (x, y) position of the text.

        color: str
            The color is used to determine if the box being drawn 
            is the ground truth or the prediction.
    
    Returns
    -------
        background_position: tuple
            This is the ((x1, y1), (x2, y2)) position of the text background.

        text_position: tuple
            This is the (x,y) position of the text aligned to the background.
    """
    if hasattr(font, 'getsize'): # works on older Pillow versions < 10.
        text_width, text_height = font.getsize(text)
    else:
        (text_width, text_height), _ = font.font.getsize(text) # newer Pillow versions >= 10.

    corner1, corner2, = text_position
    box_text_x1 = corner1[0] # Front, left, top corner.
    box_text_x2 = box_text_x1 + text_width

    if color == "RoyalBlue":
        box_text_y1 = corner2[1]
        box_text_y2 = box_text_y1 + text_height
        text_position = (corner1[0], corner2[1])
    else:
        box_text_y1 = corner1[1] - text_height
        box_text_y2 = corner1[1]
        text_position = (corner1[0], corner1[1] - text_height)
    return ((box_text_x1, box_text_y1), (box_text_x2, box_text_y2)), text_position

def draw_center_point_mae(
        image_draw: ImageDraw.ImageDraw, 
        gt_center: Union[list, np.ndarray], 
        dt_center: Union[list, np.ndarray], 
        box_position: tuple,
        font: ImageFont
    ):
    """
    In the center of the bounding box, the mean absolute error of the center
    coordinates between the ground truth and the prediction 
    bounding boxes is shown.

    Parameters
    ----------
        image_draw: ImageDraw.ImageDraw
            The object that loaded the image to write text on.

        gt_center: list, np.ndarray, or tuple 
            This is the (x,y,z) center of the ground truth bounding box.

        dt_center: list, np.ndarray, or tuple
            This is the (x,y,z) center of the prediction bounding box.

        box_position: tuple
            ((x1, y1), (x2, y2)) position of the prediction bounding box.

        font: ImageFont
            The type of font to use.
    """
    x_mae = round(abs(dt_center[0] - gt_center[0]), 2)
    y_mae = round(abs(dt_center[1] - gt_center[1]), 2)
    z_mae = round(abs(dt_center[2] - gt_center[2]), 2)
    # Find the average to write the text in the middle of the bbx.
    y_pos = (box_position[0][1] + box_position[1][1])/2
    
    draw_text(
        image_draw,
        f"error(x)={x_mae}",
        (box_position[0][0]+2, y_pos-9),
        font,
        color="white",
        background_position=(box_position[0][0]+2, y_pos-9, 
                             box_position[0][0]+80, y_pos+20),
        background_color="dimgray")

    draw_text(
        image_draw,
        f"error(y)={y_mae}",
        (box_position[0][0]+2, y_pos),
        font,
        color="white",
    )

    draw_text(
        image_draw,
        f"error(z)={z_mae}",
        (box_position[0][0]+2, y_pos+9),
        font,
        color="white",
    )

def classify_text(
        gt_label: str, 
        dt_label: str, 
        score: float, 
        iou: float, 
        validation_iou: float
    ) -> Tuple[str, str]:
    """
    Determine the appropriate text to display and the color 
    to use based on the parameters provided.

    Parameters
    ----------
        gt_label: str
            This is the ground truth label.

        dt_label: str
            This is the prediction label.

        score: float
            This is the prediction score.

        iou: float
            This is the IoU between the ground truth and the prediction.

        validation_iou: float
            This IoU is the threshold of classifying predictions as either
            true positives or localization false positives. 

    Returns
    -------
        text: str
            This is the chosen formatted text to display.

        color: str
            This is the chosen color to use for the bounding box.
    """
    # True Positives.
    if dt_label == gt_label:
        text = messages["Match"] % (dt_label, score, iou)
        color = "LimeGreen"
    # Classification False Positives.
    else:
        text = messages["Clf"] % (dt_label, score, iou)
        color = "OrangeRed"

    # Localization False Positives.
    if iou <= validation_iou:
        text = messages["Match Loc"] % (dt_label, score, iou)
        color = "OrangeRed"

    # Any unmatched or sole ground truths are false negatives.
    return text, color

def format_box_position(box_position, width: int, height: int) -> tuple:
    """
    This denormalizes the bounding box coordinates and formats it into a
    tuple.

    Parameters
    ----------
        box_position: list or np.ndarray
            This is a normalized bounding box [xmin, ymin, xmax, ymax].

        width: int
            This is the width of the image.

        height: int
            This is the height of the image.

    Returns
    -------
        box_position: tuple
            Non normalized (pixels) ((xmin, ymin), (xmax, ymax)).
    """
    p1 = (box_position[0] * width, box_position[1] * height)
    p2 = (box_position[2] * width, box_position[3] * height)
    return (p1,p2)

def format_corner_position(corners: np.ndarray, angle: float) -> tuple:
    """
    Determines which corners should the text start from based on the
    3D rotation of the box around the pitch.

    Parameters
    -----------
        corners: np.ndarray
            This contains the corners of the 3D bounding box with shape
                (3,8) representing the (x,y,z) 8 corners of a 3D box.

        angle: float
            This is the angle of rotation in radians.

    Returns
    -------
        corner_position: tuple
            This is ((x,y), (x,y)) two corners to base the text location. For 
            ground truths, the text is based on corner 2 and for the 
            predictions, the text is based on corner 1.
    """
    if angle < 0: angle += 2*np.pi

    if angle >= np.pi/2 and angle < np.pi:
        corner1 = (corners[0,2], corners[1,2])
        corner2 = (corners[0,7], corners[1,7])
    elif angle >= np.pi and angle < 3*np.pi/2:
        corner1 = (corners[0,3], corners[1,3])
        corner2 = (corners[0,4], corners[1,4])
    elif angle >= 3*np.pi/2 and angle < 2*np.pi:
        corner1 = (corners[0,0], corners[1,0])
        corner2 = (corners[0,5], corners[1,5])
    else:
        corner1 = (corners[0,1], corners[1,1])
        corner2 = (corners[0,6], corners[1,6])
    return (corner1,corner2)

def establish_view_calibration(view: np.ndarray) -> np.ndarray:
    """
    This is for 3D bounding box purposes which provides a 3D view matrix
    to calibrates existing corners coordinates to image coordinates. 

    Parameters
    ----------
        view: np.ndarray
            This is 3x4 calibration matrix.

    Returns
    -------
        viewpad: np.ndarray
            This contains the view matrix to transform the 3D 
            bounding box centers into respective corners that 
            can be drawn on the image.
    """
    viewpad = np.eye(4)
    if len(view) > 0:
        viewpad[:view.shape[0], :view.shape[1]] = view
    return viewpad

def draw_2d_bounding_boxes(
        gt_instance: Instance,
        dt_instance: Instance,
        image_summary: ImageSummary,
        validation_iou: float,
        validation_score: float
) -> Image.Image:
    """
    This is the process for drawing all the 2d bounding box in an image. This
    includes the ground truth and the prediction bounding boxes with 
    respective colors based on their classifications as true positives,
    false positives, or false negatives. 

    Parameters
    ----------
        gt_instance: Instance
            This is the ground truth instance containing the bounding boxes 
            and their labels.

        dt_instance: Instance
            This is the prediction instance containing the bounding boxes
            and their scores and labels.

        image_summary: ImageSummary
            This is the summary of the image from the evaluation process which
            includes which bounding boxes were matched and which were not
            matched.

        validation_iou: float
            This is the validation iou threshold which determines the point
            between classifying a prediction bounding box as either a
            true positive or a localization false positive.

        validation_score: float
            This is the validation score threshold which determines which 
            prediction bounding boxes to draw if their scores are greater than
            or equal to this threshold.

    Returns
    -------
        image: np.ndarray
            The image overlaid with 2d prediction and ground truth boxes. 
    """
    image = Image.fromarray(gt_instance.image)
    image_draw = ImageDraw.Draw(image)
   
    # Draw ground truths
    for label, bounding_box in zip(gt_instance.labels, gt_instance.boxes): 
        box_position = format_box_position(
            bounding_box, gt_instance.width, gt_instance.height)
        draw_2d_bounding_box(image_draw, box_position)
        
        text = str(label)
        background_position, text_position = position_2d_text_background(
            text,
            font,
            (box_position[0][0], box_position[1][1] - 12),
            box_position
        )
        draw_text(
            image_draw, 
            text, 
            text_position, 
            font, 
            background_position=background_position)
        
    # Draw extra predictions
    for extra in image_summary.index_unmatched_dt:
        dt_label = dt_instance.labels[extra]
        score = dt_instance.scores[extra]*100
        text = messages["Loc"] % (dt_label, score)

        if score >= validation_score*100:
            bounding_box = dt_instance.boxes[extra]
            box_position = format_box_position(
                bounding_box, gt_instance.width, gt_instance.height)
            draw_2d_bounding_box(image_draw, box_position, "OrangeRed")
            
            background_position, text_position = position_2d_text_background(
                text,
                font,
                (box_position[0][0], box_position[0][1] - 10),
                box_position)
            draw_text(
                image_draw,
                text,
                text_position,
                font,
                background_position=background_position,
                background_color="OrangeRed")

    # Draw matches
    for match in image_summary.index_matches:
        dt_label = dt_instance.labels[match[0]]
        gt_label = gt_instance.labels[match[1]]
        iou = image_summary.iou_list[match[0]]
        score = dt_instance.scores[match[0]]*100

        dt_center, gt_center = None, None
        if len(gt_instance.centers) > 0 and len(dt_instance.centers) > 0:
            dt_center = dt_instance.centers[match[0]]
            gt_center = gt_instance.centers[match[1]]

        text, color = classify_text(
            gt_label, dt_label, score, iou, validation_iou)

        if score >= validation_score*100:
            bounding_box = dt_instance.boxes[match[0]]
            box_position = format_box_position(
                bounding_box, gt_instance.width, gt_instance.height)
            draw_2d_bounding_box(image_draw, box_position, color)

            background_position, text_position = position_2d_text_background(
                text,
                font,
                (box_position[0][0], box_position[0][1] - 10),
                box_position)
            draw_text(
                image_draw,
                text,
                text_position,
                font,
                background_position=background_position,
                background_color=color)

            if None not in [dt_center, gt_center]:
                draw_center_point_mae(
                    image_draw, gt_center, dt_center, box_position, font)
    return image
   
def draw_3d_bounding_boxes(
        gt_instance: Instance,
        dt_instance: Instance,
        image_summary: ImageSummary,
        validation_iou: float,
        validation_score: float,
        image: Image.Image=None
    ) -> Image.Image:
    """
    This is the process for drawing all the 3d bounding box in an image. This
    includes the ground truth and the prediction bounding boxes with 
    respective colors based on their classifications as true positives,
    false positives, or false negatives. 

    Parameters
    ----------
        gt_instance: Instance
            This is the ground truth instance containing the 3d corners
            and their labels.

        dt_instance: Instance
            This is the prediction instance containing the 3d corners
            and their scores and labels.

        image_summary: ImageSummary
            This is the summary of the image from the evaluation process which
            includes which 3d boxes were matched and which were not
            matched.

        validation_iou: float
            This is the validation iou threshold which determines the point
            between classifying a prediction bounding box as either a
            true positive or a localization false positive.

        validation_score: float
            This is the validation score threshold which determines which 
            prediction bounding boxes to draw if their scores are greater than
            or equal to this threshold.
        
        image: Image.Image
            This is optional to draw on this image instead of the image
            stored in the ground truth instance.

    Returns
    -------
        image: np.ndarray
            The image overlaid with 3d prediction and ground truth boxes. 
    """
    if image is None:
        image = Image.fromarray(gt_instance.image)
    image_draw = ImageDraw.Draw(image)
    
    # Draw ground truths
    viewpad = establish_view_calibration(gt_instance.calibration)
    for label, angle, corners in zip(
        gt_instance.labels, gt_instance.box_angles, gt_instance.corners): 
        nbr_points = corners.shape[1]
        # Do operation in homogenous coordinates.
        corners = np.concatenate((corners, np.ones((1, nbr_points))))
        corners = np.dot(viewpad, corners)
        corners = corners[:3, :]
        # Normalize.
        corners = corners / corners[2:3, :].repeat(3, 0).reshape(3, nbr_points)

        corner_position = format_corner_position(corners, angle)
        draw_3d_bounding_box(image_draw, corners)

        text = str(label)
        background_position, text_position = position_3d_text_background(
            text,
            font,
            corner_position
        )
        draw_text(
            image_draw,
            text,
            text_position,
            font,
            background_position=background_position
        )

    # Draw extra predictions
    viewpad = establish_view_calibration(dt_instance.calibration)
    for extra in image_summary.index_unmatched_dt:
        dt_label = dt_instance.labels[extra]
        score = dt_instance.scores[extra]*100
        text = messages["Loc"] % (dt_label, score)

        if score >= validation_score*100:
            corners = dt_instance.corners[extra]
            angle = dt_instance.box_angles[extra]
            nbr_points = corners.shape[1]
            # Do operation in homogenous coordinates.
            corners = np.concatenate((corners, np.ones((1, nbr_points))))
            corners = np.dot(viewpad, corners)
            corners = corners[:3, :]
            # Normalize.
            corners = corners / corners[2:3, :].repeat(3, 0).reshape(3, nbr_points)
            
            corner_position = format_corner_position(corners, angle)
            draw_3d_bounding_box(image_draw, corners, "OrangeRed")

            background_position, text_position = position_3d_text_background(
                text,
                font,
                corner_position,
                "OrangeRed"
            )
            draw_text(
                image_draw,
                text,
                text_position,
                font,
                background_position=background_position,
                background_color="OrangeRed"
            )   

    # Draw matches
    for match in image_summary.index_matches:
        dt_label = dt_instance.labels[match[0]]
        gt_label = gt_instance.labels[match[1]]
        iou = image_summary.iou_list[match[0]]
        score = dt_instance.scores[match[0]]*100

        dt_center, gt_center = None, None
        if len(gt_instance.centers) > 0 and len(dt_instance.centers) > 0:
            dt_center = dt_instance.centers[match[0]]
            gt_center = gt_instance.centers[match[1]]

        text, color = classify_text(
            gt_label, dt_label, score, iou, validation_iou)

        if score >= validation_score*100:
            corners = dt_instance.corners[match[0]]
            angle = dt_instance.box_angles[match[0]]

            nbr_points = corners.shape[1]
            # Do operation in homogenous coordinates.
            corners = np.concatenate((corners, np.ones((1, nbr_points))))
            corners = np.dot(viewpad, corners)
            corners = corners[:3, :]
            # Normalize.
            corners = corners / corners[2:3, :].repeat(3, 0).reshape(3, nbr_points)

            corner_position = format_corner_position(corners, angle)
            draw_3d_bounding_box(image_draw, corners, color)

            background_position, text_position = position_3d_text_background(
                text,
                font,
                corner_position,
                color
            )
            draw_text(
                image_draw,
                text,
                text_position,
                font,
                background_position=background_position,
                background_color=color
            )

            if dt_center is not None and gt_center is not None:
                draw_center_point_mae(
                    image_draw, gt_center, dt_center, corner_position, font)
    return image