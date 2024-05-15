# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from __future__ import annotations
from typing import TYPE_CHECKING, Union, Tuple
if TYPE_CHECKING:
    from deepview.validator.datasets import Instance

from deepview.validator.exceptions import MissingLibraryException
from deepview.validator.exceptions import InvalidIoUException
import numpy as np

def clamp(
    value: Union[float, int] | None, 
    min: Union[float, int]=0, 
    max: Union[float, int]=1
) -> Union[float, int]:
    """
    Clamps a given value between 0 and 1 by default. 
    If the value is in between the set min and max, then it is returned.
    Otherwise it returns either min or max depending on which is the closest.

    Parameters
    ----------
        value: float or int
            Value to clamp between 0 and 1 (defaults).

        min: int or float
            Minimum acceptable value.

        max: int or float
            Maximum acceptable value.

    Returns
    -------
        None if value is None
        
        value: int or float
            This is the clamped value.
    """
    if value is None:
        return value
    return min if value < min else max if value > max else value # /NOSONAR

def restrict_distance(distance: float, leniency_factor: float) -> float:
    """
    Distances within the range [leniency factor, 1] are accepted. The distance
    is then scaled within this range. 

    Parameters
    ----------
        distance: float
            This is the distance to restrict.

        leniency_factor: float
            This is 1-distance minimum threshold allowable.

    Returns
    -------
        distance: float
            The restricted distance between two points.
    """
    if distance < leniency_factor:
        return 0.
    return (distance - leniency_factor)/(1. - leniency_factor)

def localize_distance(
    box_a: Union[list, np.ndarray], 
    box_b: Union[list, np.ndarray], 
    leniency_factor: int=2
):
    """
    Given the diagonal of the smaller bounding box, the center distance 
    between the bounding boxes will only be considered if the diagonal length 
    does not exceed the number of times as the leniency factor when compared
    against the center distance calculated.

    Parameters
    ----------
        box_a: list or np.ndarray
            This is a bounding box [xmin, ymin, xmax, ymax].
        
        box_b: list or np.ndarray
            This is a bounding box [xmin, ymin, xmax, ymax].

        leniency_factor: int
            This is the maximum times the diagonal of the smaller bounding
            box should fit inside the center distances.

    Returns
    -------
        distance: float
            The restricted distance between the centers of bounding boxes. If
            it does not meet the leniency criteria, it will return the maximum
            distance of 1.
    """
    diagonal = min(
        minkowski_distance(box_a[0:2], box_a[2:4]), 
        minkowski_distance(box_b[0:2], box_b[2:4]))
    center_distance = minkowski_distance(box_a, box_b)
    if int(center_distance/diagonal) <= leniency_factor:
        return center_distance
    # Validation takes 1-center_distance, so returning 1. would indicate far apart.
    return 1. 

def minkowski_distance(
    center_a: Union[list, np.ndarray], 
    center_b: Union[list, np.ndarray],
    p: int=2
) -> float:
    """
    Calculates the Minkowski distance between two points. 
    If p is 1, then this would be the Hamming distance.
    If p is 2, then this would be the Euclidean distance.
    https://www.analyticsvidhya.com/blog/2020/02/4-types-of-distance-metrics-in-machine-learning/

    Parameters
    ----------
        center_a: list or np.ndarray
            The 2D [x,y] or 3D [x,y,z] coordinates 
            for the first point.

        center_b: list or np.ndarray
            The 2D [x,y] or 3D [x,y,z] coordinates 
            for the second point.

        p: int
            The order in the minkowski distance computation.

    Returns
    -------
        distance: float
            The distance between two points.
    """
    return np.power(np.sum(np.power(np.absolute(center_a-center_b), p)), 1/p)

def cosine_similarity(
    center_a: Union[list, np.ndarray], 
    center_b: Union[list, np.ndarray],
    normalize: bool=False
) -> float:
    """
    The cosine similarity between two vectors is the dot product of the vectors
    over the product of the magnitudes of the vectors.
    https://en.wikipedia.org/wiki/Cosine_similarity

    Parameters
    ----------
        center_a: list or np.ndarray
            The 2D [x,y] or 3D [x,y,z] coordinates 
            for the first point.

        center_b: list or np.ndarray
            The 2D [x,y] or 3D [x,y,z] coordinates 
            for the second point.

        normalize: bool
            If this is set to true, this normalizes the metric to be within
            the range of 0 and 1. This is used such that the metric behaves 
            similar to an IoU for object detection. Otherwise, by default
            it is -1 for perpendicular vectors and 1 for orthogonal. 

    Returns
    -------
        cosine: float
            The distance between two points.
    """
    cosine = np.dot(center_a,center_b)/(np.linalg.norm(center_a)*np.linalg.norm(center_b))
    # normalize ranges -1 to 1 into 0 to 1.
    if normalize:
        cosine = (cosine + 1)/2
    return cosine

def get_center_point(box: Union[list, np.ndarray]) -> np.ndarray:
    """
    If given the [xmin, ymin, xmax, ymax] of the bounding box,
    this function finds the centerpoint of the bounding box in [x,y].

    Parameters
    ----------
        box: list or np.ndarray
            The [xmin, ymin, xmax, ymax] of the bounding box.

    Returns
    -------
        The centerpoint coordinate [x,y].
    """
    width = box[2] - box[0]
    height = box[3] - box[1]
    return np.array([box[0] + width/2, box[1] + height/2])

def iou_2d(
    box_a: Union[list, np.ndarray], 
    box_b: Union[list, np.ndarray], 
    eps: float=1e-10
) -> float:
    """
    Computes the IoU between ground truth and detection 
    bounding boxes. IoU computation method retrieved from:: 
    https://gist.github.com/meyerjo/dd3533edc97c81258898f60d8978eddc
    
    Parameters
    ----------
        box_a: list or np.ndarray
            This is a bounding box [xmin, ymin, xmax, ymax].
        
        box_b: list or np.ndarray
            This is a bounding box [xmin, ymin, xmax, ymax].

        eps: float
            Avoids division by zero errors.

    Returns
    -------
        IoU: float
            The IoU score between boxes.

    Exceptions
    ----------
        InvalidIoUException
            Raised if the calculated IoU is invalid. 
            i.e. less than 0 or greater than 1.

        ValueError
            Raised if the provided boxes for ground truth 
            and detection does not have a length of four.
    """
    if len(box_a) != 4 or len(box_b) != 4:
        raise ValueError("The provided bounding boxes does not meet " \
                            "expected lengths [xmin, ymin, xmax, ymax]")
    
    # Determine the (x, y)-coordinates of the intersection rectangle.
    x_a = max(box_a[0], box_b[0])
    y_a = max(box_a[1], box_b[1])
    x_b = min(box_a[2], box_b[2])
    y_b = min(box_a[3], box_b[3])

    # Compute the area of intersection rectangle.
    inter_area = max((x_b - x_a, 0)) * max((y_b - y_a), 0)
    if inter_area == 0:
        return 0.
    # Compute the area of both the prediction and ground-truth rectangles.
    box_a_area = abs((box_a[2] - box_a[0]) * (box_a[3] - box_a[1]))
    box_b_area = abs((box_b[2] - box_b[0]) * (box_b[3] - box_b[1]))

    # Compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = inter_area / float(box_a_area + box_b_area - inter_area)

    if iou > 1. + eps or iou < 0.:
        raise InvalidIoUException(iou)
    # Return the intersection over union value.
    return iou  

def iou_3d(
    corners1: Union[list, np.ndarray], 
    corners2: Union[list, np.ndarray]
) -> float:
    """
    Computes the 3D IoU between ground truth and detection bounding boxes.
    Source: https://github.com/varunagrawal/bbox/blob/master/bbox/metrics.py#L139

    Parameters
    ----------
        corners1: list or np.ndarray (8,3)
            This is a list of 8 corners for 3D one bounding box where rows
            represents one point and columns represents the [x,y,z] coordinate.

        corners2: list or np.ndarray (8,3)
            This is a list of 8 corners for 3D one bounding box where rows
            represents one point and columns represents the [x,y,z] coordinate.

    Returns
    -------
        iou: float
            This is the 3D IoU between ground truth and prediction
            bounding boxes.
    """
    # Check if the two boxes don't overlap.
    if not polygon_collision(corners1[0:4,[0,2]], corners2[0:4,[0,2]]):
        return 0.0
    
    # Intersection of the x,z plane.
    intersection_points = polygon_intersection(
        corners1[0:4,[0,2]], corners2[0:4,[0,2]])
    # If intersection_points is empty, means the boxes don't intersect
    if len(intersection_points) == 0:
        return 0.0
    inter_area = polygon_area(intersection_points)

    ymax = np.minimum(corners1[4,1], corners2[4,1])
    ymin = np.maximum(corners1[0,1], corners2[0,1])
    inter_vol = inter_area * np.maximum(0, ymax - ymin)

    vol1 = box3d_vol(corners1)
    vol2 = box3d_vol(corners2)
    union_vol = (vol1 + vol2 - inter_vol)

    iou = inter_vol / union_vol
    # set nan and +/- inf to 0
    if np.isinf(iou) or np.isnan(iou):
        iou = 0
    return iou

def batch_iou(box1, box2, eps: float=1e-7):
    """
    Return intersection-over-union (Jaccard index) of boxes.
    This is a YoloV5 implementation taken here:: \
    https://github.com/ultralytics/yolov5/blob/master/utils/metrics.py#L266

    Both sets of boxes are expected to be in (x1, y1, x2, y2) format.
    
    Parameters
    ----------
        box1: (Tensor[N, 4])
            Bounding boxes array.

        box2: (Tensor[M, 4])
            Bounding boxes array.

        eps: float
            Avoids division by zero errors.

    Returns
    --------
        iou: (Tensor[N, M]) 
            The NxM matrix containing the pairwise IoU values for every 
            element in boxes1 and boxes2.
    """
    # https://github.com/pytorch/vision/blob/master/torchvision/ops/boxes.py
    try:
        import torch
    except ImportError:
        raise MissingLibraryException(
            "Torchvision is needed to perform batch IoU.")

    (a1, a2), (b1, b2) = box1.unsqueeze(1).chunk(2, 2), box2.unsqueeze(0).chunk(2, 2)
    inter = (torch.min(a2, b2) - torch.max(a1, b1)).clamp(0).prod(2)
    return inter / ((a2 - a1).prod(2) + (b2 - b1).prod(2) - inter + eps)

def filter_dt(
    boxes: np.ndarray, 
    classes: np.ndarray, 
    scores: np.ndarray, 
    threshold: float
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Filters the detections to include only scores 
    greater than or equal to the validation threshold set.
    
    Parameters
    ----------
        boxes: np.ndarray
            The prediction bounding boxes.. [[box1], [box2], ...].

        classes: np.ndarray
            The prediction labels.. [cl1, cl2, ...].

        scores: np.ndarray
            The prediction confidence scores.. [score, score, ...]
            normalized between 0 and 1.

        threshold: float
            This is the validation score threshold to filter
            the detections.

    Returns
    ------- 
        boxes, classes, scores: np.ndarray
            These contain only the detections whose scores are 
            larger than or greater than the validation threshold set.
    """
    filter_indices = np.argwhere(scores>=threshold).flatten()
    if classes.dtype.type is np.str_:
        filter_indices = np.argwhere(
            (scores>=threshold) & (classes != "background")).flatten()
    boxes = np.take(boxes, filter_indices, axis=0)
    scores = np.take(scores, filter_indices, axis=0)
    classes = np.take(classes, filter_indices, axis=0)
    return boxes, classes, scores

def clamp_boxes(gt_instance: Instance, dt_instance: Instance, clamp: int):
    """
    Clamps bounding box less than the provided clamp value to 
    the clamp value in pixels. The minimum width and height 
    of the bounding is the clamp value in pixels. 
    
    Parameters
    ----------
        gt_instance: Instance
            This contains the ground truth bounding boxes, labels, etc.

        dt_instance: Instance
            This contains the detection bounding boxes, labels, etc.

        clamp: int
            The minimum acceptable dimensions of the bounding boxes for 
            detections and ground truth. 
    """
    height = gt_instance.height
    width = gt_instance.width
    gt_boxes = gt_instance.boxes
    dt_boxes = dt_instance.boxes

    gt_widths = ((gt_boxes[..., 2:3] - gt_boxes[..., 0:1])*width).flatten()
    gt_heights = ((gt_boxes[..., 3:4] - gt_boxes[..., 1:2])*height).flatten()
    dt_widths = ((dt_boxes[..., 2:3] - dt_boxes[..., 0:1])*width).flatten()
    dt_heights = ((dt_boxes[..., 3:4] - dt_boxes[..., 1:2])*height).flatten()

    gt_modify = np.transpose(
        np.nonzero(((gt_widths<clamp)+(gt_heights<clamp)))).flatten()
    dt_modify = np.transpose(
        np.nonzero(((dt_widths<clamp)+(dt_heights<clamp)))).flatten()
    if len(gt_boxes):
        gt_boxes[gt_modify, 2:3] = gt_boxes[gt_modify, 0:1] + clamp/width
        gt_boxes[gt_modify, 3:4] = gt_boxes[gt_modify, 1:2] + clamp/height
        gt_instance.boxes = gt_boxes
    if len(dt_boxes):
        dt_boxes[dt_modify, 2:3] = dt_boxes[dt_modify, 0:1] + clamp/width
        dt_boxes[dt_modify, 3:4] = dt_boxes[dt_modify, 1:2] + clamp/height
        dt_instance.boxes = dt_boxes

def ignore_boxes(gt_instance: Instance, dt_instance: Instance, ignore: int):
    """
    Ignores the boxes with dimensions less than the ignore parameter provided. 
    
    Parameters
    ----------
        gt_instance: Instance
            This contains the ground truth bounding boxes, labels, etc.

        dt_instance: Instance
            This contains the detection bounding boxes, labels, etc.

        ignore: int
            The dimension pixels threshold to ignore. Any boxes with width 
            and height less than this value will be ignored and filtered out.
    """
    height = gt_instance.height
    width = gt_instance.width
    gt_boxes = gt_instance.boxes
    gt_labels = gt_instance.labels
    dt_boxes = dt_instance.boxes
    dt_labels = dt_instance.labels
    scores = dt_instance.scores

    gt_widths = ((gt_boxes[..., 2:3] - gt_boxes[..., 0:1])*width).flatten()
    gt_heights = ((gt_boxes[..., 3:4] - gt_boxes[..., 1:2])*height).flatten()
    dt_widths = ((dt_boxes[..., 2:3] - dt_boxes[..., 0:1])*width).flatten()
    dt_heights = ((dt_boxes[..., 3:4] - dt_boxes[..., 1:2])*height).flatten()

    gt_keep = np.transpose(
        np.nonzero(((gt_widths>=ignore)*(gt_heights>=ignore)))).flatten()
    dt_keep = np.transpose(
        np.nonzero(((dt_widths>=ignore)*(dt_heights>=ignore)))).flatten()
    
    gt_instance.boxes = np.take(gt_boxes, gt_keep, axis=0)
    gt_instance.labels =  np.take(gt_labels, gt_keep, axis=0)
    dt_instance.boxes = np.take(dt_boxes, dt_keep, axis=0)
    dt_instance.labels = np.take(dt_labels, dt_keep, axis=0)
    dt_instance.scores = np.take(scores, dt_keep, axis=0)

def nan_to_last_num(process_array: np.ndarray) -> np.ndarray:
    """
    Replaces all NAN values with the last valid number. If all 
    values are NaN, then all elements are replaced with zeros.
    
    Parameters
    ----------
        process_array: np.ndarray
            This is the array to replace NaN values with the last 
            acceptable value.

    Returns
    -------
        process_array: np.ndarray
            The same array but with NaN replaced with last acceptable values.
            Otherwise, all elements are replaced with zeros if all elements are
            NaN.
    """
    try:
        # Find the maximum index where the value is not a NaN.
        precision_repeat_id = np.max(
            np.argwhere(
                np.logical_not(
                    np.isnan(process_array))).flatten())
        # NaN values should be replace with the last acceptable value.
        process_array = np.nan_to_num(
            process_array,
            nan=process_array[int(precision_repeat_id)])
    except ValueError:
        # The whole array are nans just convert back to zero.
        process_array[np.isnan(process_array)] = 0.
    return process_array

def x_rotation(angle: float) -> np.ndarray:
    """
    Rotation around the x-axis.
    Source: https://en.wikipedia.org/wiki/Rotation_matrix

    Parameters
    ----------
        angle: float
            The angle of rotation in radians.

    Returns
    ------- 
        Rotation matrix around the x-axis.
    """    
    c = np.cos(angle)
    s = np.sin(angle)
    return np.array([[ 1, 0,  0],
                     [ 0, c, -s],
                     [ 0, s,  c]])

def y_rotation(angle: float) -> np.ndarray:
    """
    Rotation around the y-axis.
    Source: https://en.wikipedia.org/wiki/Rotation_matrix
    
    Parameters
    ----------
        angle: float
            The angle of rotation in radians.

    Returns
    ------- 
        Rotation matrix around the y-axis.
    """
    c = np.cos(angle)
    s = np.sin(angle)
    return np.array([[ c, 0, s],
                     [ 0, 1, 0],
                     [-s, 0, c]])

def z_rotation(angle: float) -> np.ndarray:
    """
    Rotation around the z-axis.
    Source: https://en.wikipedia.org/wiki/Rotation_matrix

    Parameters
    ----------
        angle: float
            The angle of rotation in radians.

    Returns
    ------- 
        Rotation matrix around the z-axis.
    """
    c = np.cos(angle)
    s = np.sin(angle)
    return np.array([[c, -s,  0],
                     [s,  c,  0],
                     [0,  0,  1]])

def transform(
    box_size: Union[list, np.ndarray, tuple], 
    heading_angle: float, 
    center: Union[list, np.ndarray, tuple]
) -> np.ndarray:
    """
    Provides rotations and formation of the 3D box corners.

    Parameters
    ----------
        box_size: np.ndarray, list, or tuple
            Can be unpacked to width, height, length respectively.
        
        heading_angle: float
            The angle in radians to rotate around the y-axis.

        center: np.ndarray, list, or tuple
            In the order of the x-center, y-center, and z-center coordinates. 

    Returns
    -------
        corners_3d: np.ndarray (3,8)
            The 3D bounding box corners where rows are the [x,y,z] coordinates
            and columns are the 8 corner points. 
    """
    R = y_rotation(heading_angle)
    w,h,l = box_size
    x_corners = [-l/2, l/2, l/2,-l/2,-l/2, l/2,l/2,-l/2];
    y_corners = [-h/2,-h/2,-h/2,-h/2, h/2, h/2,h/2, h/2];
    z_corners = [-w/2,-w/2, w/2, w/2,-w/2,-w/2,w/2, w/2];

    corners_3d = np.dot(R, np.vstack([x_corners,y_corners,z_corners]))
    corners_3d[0,:] = corners_3d[0,:] + center[0];
    corners_3d[1,:] = corners_3d[1,:] + center[1];
    corners_3d[2,:] = corners_3d[2,:] + center[2];
    return corners_3d

def box3d_vol(corners: np.ndarray) -> float:
    """
    Computes the volume of the 3D bounding box based on the corners provided.

    Parameters
    ----------
        corners: np.ndarray (8,3)
            no assumption on axis direction

    Returns
    ------- 
        volume: float
            The volume of the bounding box.
    """
    a = np.sqrt(np.sum((corners[0,:] - corners[1,:])**2))
    b = np.sqrt(np.sum((corners[1,:] - corners[2,:])**2))
    c = np.sqrt(np.sum((corners[0,:] - corners[4,:])**2))
    return a*b*c

def get_corners(sizes: list, box_angles: list, centers: list) -> list:
    """
    Transforms a list of sizes, angles, and centers into 3D box corners.

    Parameters
    ----------
        sizes: list
            Contains lists that can be unpacked 
            to width, height, length respectively.
        
        box_angles: list
            Contains the angles in radians to rotate around the y-axis.

        centers: list
            Contains lists in the order of 
            the x-center, y-center, and z-center coordinates. 

    Returns
    -------
        corners: list
            A list of (8,3) corners.
    """
    # corner formats should be [[[x,y,z], [x,y,z], ... x6]]
    corners = list()
    if 0 not in [len(sizes), len(box_angles), len(centers)]:
        for size, angle, center in zip(sizes, box_angles, centers):
            corners.append(transform(size,angle,center))
    return corners

"""
Useful functions to deal with 3D geometry.
Source: https://github.com/varunagrawal/bbox/blob/master/bbox/geometry.py
"""

def get_plane(a, b, c):
    """
    Get plane equation from 3 points.
    Returns the coefficients of `ax + by + cz + d = 0`
    """
    ab = b - a
    ac = c - a

    x = np.cross(ab, ac)
    d = -np.dot(x, a)
    pl = np.hstack((x, d))
    return pl

def point_plane_dist(pt, plane, signed: bool=False):
    """
    Get the signed distance from a point `pt` to a plane `plane`.
    Reference: http://mathworld.wolfram.com/Point-PlaneDistance.html

    Plane is of the format [A, B, C, D], where the plane equation is Ax+By+Cz+D=0
    Point is of the form [x, y, z]
    `signed` flag indicates whether to return signed distance.
    """
    v = plane[0:3]
    dist = (np.dot(v, pt) + plane[3]) / np.linalg.norm(v)

    if signed:
        return dist
    else:
        return np.abs(dist)

def edges_of(vertices):
    """
    Return the vectors for the edges of the polygon defined by `vertices`.

    Args:
        vertices: list of vertices of the polygon.
    """
    edges = []
    N = len(vertices)

    for i in range(N):
        edge = vertices[(i + 1) % N] - vertices[i]
        edges.append(edge)

    return edges

def orthogonal(v):
    """
    Return a 90 degree clockwise rotation of the vector `v`.

    Args:
        v: 2D array representing a vector.
    """
    return np.array([-v[1], v[0]])

def is_separating_axis(o, p1, p2):
    """
    Return True and the push vector if `o` is a separating axis 
    of `p1` and `p2`. Otherwise, return False and None.

    Args:
        o: 2D array representing a vector.
        p1: 2D array of points representing a polygon.
        p2: 2D array of points representing a polygon.
    """
    min1, max1 = float('+inf'), float('-inf')
    min2, max2 = float('+inf'), float('-inf')

    for v in p1:
        projection = np.dot(v, o)

        min1 = min(min1, projection)
        max1 = max(max1, projection)

    for v in p2:
        projection = np.dot(v, o)

        min2 = min(min2, projection)
        max2 = max(max2, projection)

    if max1 >= min2 and max2 >= min1:
        d = min(max2 - min1, max1 - min2)
        # push a bit more than needed so the shapes do not overlap in future
        # tests due to float precision
        d_over_o_squared = d / np.dot(o, o) + 1e-10
        pv = d_over_o_squared * o
        return False, pv
    else:
        return True, None

def polygon_collision(p1, p2):
    """
    Return True if the shapes collide. Otherwise, return False.

    p1 and p2 are np.arrays, the vertices of the polygons in the
    counterclockwise direction.

    Source: https://hackmd.io/s/ryFmIZrsl

    Args:
        p1: 2D array of points representing a polygon.
        p2: 2D array of points representing a polygon.
    """
    edges = edges_of(p1)
    edges += edges_of(p2)
    orthogonals = [orthogonal(e) for e in edges]

    push_vectors = []
    for o in orthogonals:
        separates, pv = is_separating_axis(o, p1, p2)

        if separates:
            # they do not collide and there is no push vector
            return False
        else:
            push_vectors.append(pv)

    return True

def polygon_area(polygon):
    """
    Get the area of a polygon which is represented by a 2D array of points.
    Area is computed using the Shoelace Algorithm.

    Args:
        polygon: 2D array of points.
    """
    x = polygon[:, 0]
    y = polygon[:, 1]
    area = (np.dot(x, np.roll(y, -1)) - np.dot(np.roll(x, -1), y))
    return np.abs(area) / 2

def polygon_intersection(poly1, poly2):
    """
    Use the Sutherland-Hodgman algorithm to 
    compute the intersection of 2 convex polygons.
    """
    def line_intersection(e1, e2, s, e):
        dc = e1 - e2
        dp = s - e
        n1 = np.cross(e1, e2)
        n2 = np.cross(s, e)
        n3 = 1.0 / (np.cross(dc, dp))
        return np.array([(n1 * dp[0] - n2 * dc[0]) * n3,
                         (n1 * dp[1] - n2 * dc[1]) * n3])

    def is_inside_edge(p, e1, e2):
        """Return True if e is inside edge (e1, e2)"""
        return np.cross(e2 - e1, p - e1) >= 0

    output_list = poly1
    # e1 and e2 are the edge vertices for each edge in the clipping polygon
    e1 = poly2[-1]

    for e2 in poly2:
        # If there is no point of intersection
        if len(output_list) == 0:
            break

        input_list = output_list
        output_list = []
        s = input_list[-1]

        for e in input_list:
            if is_inside_edge(e, e1, e2):
                # if s in not inside edge (e1, e2)
                if not is_inside_edge(s, e1, e2):
                    # line intersects edge hence we compute intersection point
                    output_list.append(line_intersection(e1, e2, s, e))
                output_list.append(e)
            # is s inside edge (e1, e2)
            elif is_inside_edge(s, e1, e2):
                output_list.append(line_intersection(e1, e2, s, e))

            s = e
        e1 = e2
    return np.array(output_list)