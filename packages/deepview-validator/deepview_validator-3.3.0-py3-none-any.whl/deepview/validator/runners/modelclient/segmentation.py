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
    from deepview.validator.evaluators.parameters import Parameters

from deepview.validator.runners.modelclient.core import ModelClientRunner
from deepview.validator.exceptions import MissingLibraryException
from deepview.validator.datasets.utils import resize
from time import monotonic_ns as clock_now
from typing import Tuple
import numpy as np
import os

class SegmentationRunner(ModelClientRunner):
    """
    Uploads the model to the target and runs the model per image.

    Parameters
    ----------
        model: str
            The path to the model.

        target: str
            The modelrunner target in the EVK. Ex. 10.10.40.205:10817.

        parameters: Parameters
            This object contains the model parameters set from the command line.

        segmentation_model_type: str
            This is the type of segmentation model. Can either
            be "modelpack" or "deeplab".

    Raises
    ------
        ModelRunnerFailedConnectionException
            Raised if connecting to modelrunner is unsuccessful.

        MissingLibraryException
            Raised if certain libraries are not installed.

        ValueError
                Raised if the provided image_path
                does not exist and the provided image is not a numpy.ndarray.
    """
    def __init__(
        self,
        model: str,
        target: str,
        parameters: Parameters,
        segmentation_model_type: str="modelpack"
    ):
        try:
            import requests as re
        except ImportError:
            raise MissingLibraryException(
                "requests is needed to communicate " +
                "with the modelclient server.")

        super(SegmentationRunner,self).__init__(
            model=model,
            target=target,
            parameters=parameters
        )
        self.segmentation_model_type = segmentation_model_type.lower()
        self.outputs = list()

        r = re.get(self.target +
                   str('model' if self.target.endswith('/') else '/model'))
        if r.status_code == 200:
            r = r.json()
            self.shape = np.array(r['inputs'][0].get('shape'))[1:]
            self.input_name = r['inputs'][0].get('name')
            self.outputs = r['outputs']
        else:
            raise RuntimeError(
                "Error connecting to modelrunner url: {}".format(
                    self.target))

    def preprocess_input(self, image):
        """Abstract method."""
        raise NotImplementedError("This is an abstract method.")

    def decode(self, outputs):
        """Abstract method."""
        raise NotImplementedError("This is an abstract method.")

    def run_single_instance(self, image: Tuple[str, np.ndarray]):
        """
        Reads the image and grabs the segmentation mask output.

        Parameters
        ----------
            image: str or np.ndarray
                This is either the path to the image or
                a numpy array image.

        Returns
        -------
            dt_mask: np.ndarray
                The model prediction mask of the image.

        Raises
        ------
            MissingLibraryException
                Raised if opencv is not installed.
        """
        try:
            import cv2 # type: ignore
        except ImportError:
            raise MissingLibraryException(
                "opencv is needed to perform mask operations.")
        
        start = clock_now()
        image = resize(image, self.get_input_shape())
        inp = self.preprocess_input(image)
        load_ns = clock_now() - start
        self.loading_input_timings.append(load_ns * 1e-6)

        start = clock_now()
        outputs = self.client.run(
            {
                self.input_name: inp
            },
            outputs=[key['name'] for key in self.outputs],
            params={'run': 1}
        )
        infer_ns = clock_now() - start
        self.inference_timings.append(infer_ns * 1e-6)

        start = clock_now()
        seg_mask, _ = self.decode(outputs)

        dt_mask = cv2.resize(
            seg_mask[0],
            self.get_input_shape(),
            interpolation=cv2.INTER_NEAREST)
        if self.segmentation_model_type == "modelpack":
            dt_mask = cv2.warpAffine(dt_mask.astype(np.uint8), np.float32(
                [[1, 0, 15], [0, 1, 15]]), self.get_input_shape())

        boxes_ns = clock_now() - start
        self.box_timings.append(boxes_ns * 1e-6)
        return dt_mask
    
    def get_input_shape(self) -> tuple:
        """
        Grabs the ModelPack input shape.

        Returns
        -------
            shape: tuple
                The model input shape.
        """
        return self.modelclient_parameters['input_shape'][0:2]

class SegmentationModelPack(SegmentationRunner):
    """
    Inherits SegmentationRunner and preprocesses the input type of the MPK 
    models and decodes the output to generate the segmentation mask.
   
    Parameters
    ----------
        model: str
            The path to the model.

        target: str
            The modelrunner target in the EVK. Ex. 10.10.40.205:10817.

        parameters: Parameters
            This object contains the model parameters set from the command line.

        segmentation_model_type: str
            This is "modelpack" type.

    Raises
    ------
        ModelRunnerFailedConnectionException
            Raised if connecting to modelrunner is unsuccessful.

        MissingLibraryException
            Raised if certain libraries are not installed.
    """

    def __init__(
        self,
        model: str,
        target: str,
        parameters: Parameters,
        segmentation_model_type: str="modelpack",
    ):
        super(SegmentationModelPack, self).__init__(
            model=model,
            target=target,
            parameters=parameters,
            segmentation_model_type=segmentation_model_type,
        )

    def decode(self, outputs: dict):
        """
        Decodes the output, x and returns the numpy array segmentation 
        mask with elements containing the values of the objects ids.

        Parameters
        ----------
            outputs: dict
                This is the output of the model which
                contains the detection mask.

        Returns
        -------
            TODO: Add Description.
        """
        for _, out in outputs.items():
            return np.argmax(out, axis=-1), out

    def preprocess_input(self, image: np.ndarray) -> np.ndarray:
        """
        Expands the dimension of the array by one.
       
        Parameters
        ----------
            img: np.ndarray
                This is the image to feed the model.

        Returns
        -------
            img: np.ndarray
                Expanded image with extra dimension 1.
        """
        return np.expand_dims(image, 0).astype(np.uint8)

class SegmentationDeepLab(SegmentationRunner):
    """
    Inherits SegmentationRunner and preprocesses the input 
    type of the Deeplab models and decodes the output to 
    generate the segmentation mask.

    Parameters
    ----------
        model: str
            The path to the model.

        target: str
            The modelrunner target in the EVK. Ex. 10.10.40.205:10817.

        parameters: Parameters
            This object contains the model parameters set from the command line.

        segmentation_model_type: str
            This is the type of the model. e.g. "deeplab".

    Raises
    ------
        ModelRunnerFailedConnectionException
            Raised if connecting to modelrunner is unsuccessful.

        MissingLibraryException
            Raised if certain libraries are not installed.
    """

    def __init__(
        self,
        model: str,
        target: str,
        parameters: Parameters,
        segmentation_model_type: str="deeplab"
    ):
        super(SegmentationDeepLab, self).__init__(
            model=model,
            target=target,
            parameters=parameters,
            segmentation_model_type=segmentation_model_type    
        )

    def decode(self, outputs: dict):
        """
        Decodes the output, x and returns the numpy array \
            segmentation mask with elements containing the values of \
                the objects ids.
       
        Parameters
        ----------
            outputs: dict
                This is the output of the model which
                contains the detection mask.

        Returns
        -------
            TODO: Add description.

        Raises
        ------
            MissingLibraryException
                Raised if the tensorflow library is not installed.
        """
        try:
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
            import tensorflow as tf
        except ImportError:
            raise MissingLibraryException(
                "tensorflow is needed for deeplab prediction decoding.")

        for _, out in outputs.items():
            z = np.argmax(out, axis=-1)
            z[z <= 2] = 0
            z[z == 15] = 1
            z[z == 7] = 2
            z[z > 2] = 0
            r = tf.one_hot(z, 2)
            return z, r

    def preprocess_input(self, image: np.ndarray) -> np.ndarray:
        """
        Expands the dimension of the array by one.
       
        Parameters
        ----------
            img: np.ndarray
                This is the image to feed the model.

        Returns
        -------
            img: np.ndarray
                Expanded image with extra dimension 1.
        """
        return np.expand_dims(image.copy(), 0).astype(np.uint8)
