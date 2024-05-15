# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.runners.deepviewrt import (
    SegmentationDeepViewRTRunner,
    DeepViewRTRunner
)
from deepview.validator.runners.tensorrt import TensorRTRunner
from deepview.validator.runners.offline import OfflineRunner
from deepview.validator.runners.tflite import TFliteRunner
from deepview.validator.runners.hailo import HailoRunner
from deepview.validator.runners.keras import (
    SegmentationKerasRunner, 
    DetectionKerasRunner, 
    PoseKerasRunner
)
from deepview.validator.runners.onnx import ONNXRunner
from deepview.validator.runners.core import Runner