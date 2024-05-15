# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.visualize.detectiondraw import draw_2d_bounding_box
from PIL import Image, ImageDraw
from typing import Tuple
import numpy as np

def establish_axis_points(
        angles: list,
        starting_position: tuple,
        size: int=150
    ) -> tuple:
    """
    Provides the (x,y) end positions of the lines forming 
    the 3 axis for the pose.

    Parameters
    ----------
        angles: list
            This contains the [roll, pitch, yaw] angles in radians.

        starting_position: tuple
            This is the starting positions for 
            which to start drawing the lines in (x,y).
        
        size: int
            This is the pixel length of the lines.

    Returns
    -------
        end_positions: tuple
            The ((x,y), (x,y), (x,y)) end positions of the lines.
    """
    roll, pitch, yaw = angles
    tdx, tdy = starting_position
    # X-Axis (out of the screen) drawn in red.
    x1 = int(size * (np.sin(yaw)) + tdx)
    y1 = int(size * (-np.cos(yaw) * np.sin(pitch)) + tdy)
    # Y-Axis pointing to right. drawn in green.
    x2 = int(size * (np.cos(yaw) * np.cos(roll)) + tdx)
    y2 = int(size * (np.cos(pitch) * np.sin(roll) + np.cos(roll) * np.sin(pitch) * np.sin(yaw)) + tdy)
    # Z-Axis | drawn in blue.
    x3 = int(size * (-np.cos(yaw) * np.sin(roll)) + tdx)
    y3 = int(size * (np.cos(pitch) * np.cos(roll) - np.sin(pitch) * np.sin(yaw) * np.sin(roll)) + tdy)
    return((x1,y1), (x2,y2), (x3,y3))

def establish_axis_order(
        yaw: float, 
        end_positions: tuple, 
        colors: tuple
    ) -> Tuple[str, str, tuple, tuple]:
    """
    This establish the order of which the axis should be drawn and
    their colors per frame to avoid illusions of rotations going back and forth
    and maintain rotations moving in a single direction. 

    Parameters
    ----------
        yaw: float
            The yaw angle in radians.

        end_positions: tuple
            This is the ((x,y), (x,y), (x,y)) end points of the axes.

        colors: tuple
            The three distinct colors of each axis. 

    Returns
    -------
        color_infront: str
            This is the color of the axis that is drawn last or the front axis.

        color_behind: str
            This is the color of the axis that is drawn first or the axis
            behind.

        axis_infront: tuple
            This is the end position of the axis (x,y) that is to be drawn
            last to appear in front.

        axis_behind: tuple
            This is the end position of the axis (x,y) that is to be drawn
            first to appear behind.
    """
    if yaw >= (-80*np.pi/180) and yaw <= (170*np.pi/180):
        axis_behind = end_positions[1]
        axis_infront = end_positions[0]
        color_behind = colors[1]
        color_infront = colors[2]
    else:
        axis_behind = end_positions[0]
        axis_infront = end_positions[1]
        color_behind = colors[2]
        color_infront = colors[1]
    return color_infront, color_behind, axis_infront, axis_behind

def draw_axis(
        image_draw: ImageDraw.ImageDraw,
        start_position: tuple,
        end_positions: tuple,
        colors: tuple,
        width: int=5
    ):
    """
    This draws the pose axis/compass on a 2D image. 

    Parameters
    ----------
        image_draw: ImageDraw.ImageDraw
            This is the object that loaded the image to draw the
            axis on.

        start_position: tuple
            This is the (x,y) starting position of the three lines.
            Ensure the values are integers.

        end_position: tuple
            This is the ((x,y), (x,y), (x,y)) end positions of the lines.
            Ensure the first point is the axis drawn behind, the second
            point is the axis drawn in the middle, and the third point is
            the axis drawn on the front.

        color: tuple
            This is color of each line ("blue", "green", "red")  
            or any other combination for the three axis. 

        width: int
            This is the width of the lines. 
    """
    image_draw.line(
        (start_position, end_positions[0]), 
        fill=colors[0], 
        width=width)
    image_draw.line(
        (start_position, end_positions[1]), 
        fill=colors[1], 
        width=width)
    image_draw.line(
        (start_position, end_positions[2]), 
        fill=colors[2], 
        width=width)
    
def draw_axes(
        nimage: np.ndarray,
        dt_euler: list,
        gt_euler: list,
        starting_position: tuple=None,
        gt_box: list=None
    ) -> Image.Image:
    """
    This function draws both the ground truth and the prediction axes.

    Parameters
    ----------
        nimage: np.ndarray
            This is the image as an numpy array.

        dt_euler: list
            This is the prediction angles containing [roll, pitch, yaw]
            in radians.

        gt_euler: list
            This is the ground truth angles containing [roll, pitch, yaw]
            in radians.

        starting_position: tuple
            This is the point to start drawing the axis in (x,y).

        gt_box: list
            This is an optional bounding box around the object that is being
            rotated in [xmin, ymin, xmax, ymax].

    Returns
    -------
        image: np.ndarray
            The image with overlaid ground truth and prediction axes and 
            a bounding box around the object being analyzed. 
    """
    image = Image.fromarray(nimage)
    image_draw = ImageDraw.Draw(image)

    if starting_position is None:
        if gt_box is None:
            height, width = nimage.shape[:2]
            starting_position = (width/2, height/2)
        else:
            x1, y1, x2, y2 = gt_box
            starting_position = (int((x1+x2)* 0.5), int((y1+y2)* 0.5))
            draw_2d_bounding_box(image_draw, ((x1, y1),(x2,y2)), "green")

    if len(dt_euler):
        end_positions = establish_axis_points(dt_euler, starting_position)
        color_infront, color_behind, axis_infront, axis_behind = establish_axis_order(
            dt_euler[2],
            end_positions,
            ("lightblue", "lightgreen", "tomato")
        )
        draw_axis(
            image_draw, 
            starting_position,
            (axis_behind, end_positions[2], axis_infront),
            (color_behind, "lightblue", color_infront)
        )
    
    if len(gt_euler):
        end_positions = establish_axis_points(gt_euler, starting_position)
        color_infront, color_behind, axis_infront, axis_behind = establish_axis_order(
            gt_euler[2],
            end_positions,
            ("blue", "green", "red")
        )
        draw_axis(
            image_draw, 
            starting_position,
            (axis_behind, end_positions[2], axis_infront),
            (color_behind, "blue", color_infront)
        )
    return image