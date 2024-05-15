# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.runners.modelclient.core import ModelClientRunner
from deepview.validator.runners.modelclient.segmentation import ( 
    SegmentationModelPack, 
    SegmentationDeepLab,
    SegmentationRunner
)
from deepview.validator.runners.modelclient.detection import (
    BoxesModelPack,
    BoxesYolo
)
