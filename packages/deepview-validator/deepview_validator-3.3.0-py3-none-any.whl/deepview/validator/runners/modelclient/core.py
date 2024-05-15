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
    from deepview.validator.evaluators import Parameters

from deepview.validator.exceptions import ModelRunnerFailedConnectionException
from deepview.validator.exceptions import MissingLibraryException
from deepview.validator.runners.core import Runner

class ModelClientRunner(Runner):
    """
    Uses the modelclient API to run DeepViewRT models.

    Parameters
    ----------
        model: str
            The path to the model.

        target: str
            The modelrunner target in the EVK. Ex. 10.10.40.205:10817.

        parameters: Parameters
            These are the model parameters set from the command line.

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
        parameters: Parameters=None
    ):
        super(ModelClientRunner, self).__init__(model, parameters)
        self.target = target
        self.load_model()

    def load_model(self):
        """
        Loads the model to the modelrunner target.
      
        Raises
        ------
            ModelRunnerFailedConnectionException
                Raised if connecting to modelrunner is unsuccessful.

            MissingLibraryException
                Raised if the library requests is not installed.
        """
        try:
            import requests as req
        except ImportError:
            raise MissingLibraryException(
                "requests is needed to communicate " +
                "with the modelclient server.")

        try:
            from deepview.rt.modelclient import ModelClient # type: ignore
            self.client = ModelClient(uri=self.target, rtm=self.model)
        except req.exceptions.ConnectionError:
            raise ModelRunnerFailedConnectionException(self.target)
        
        self.parameters.engine = req.get(self.target).json()['engine']

        response = req.get("{}/model".format(self.target))
        self.modelclient_parameters = {}
        if response.status_code == 200:
            body = response.json()
            inputs = body['inputs']
            outputs = body['outputs']
            self.modelclient_parameters['input_name'] = inputs[0]['name']
            self.modelclient_parameters['input_type'] = inputs[0]['datatype']
            self.modelclient_parameters['input_scale'] = inputs[0]['scale']
            self.modelclient_parameters['input_zp'] = inputs[0]['zero_point']
            self.modelclient_parameters['input_shape'] = inputs[0]['shape'][1:]
            
            output_parameters = dict()
            for key in outputs:
                output_parameters[key['name']] = {
                    "scale": key['scale'],
                    "zero_point": key['zero_point'],
                    "index": key['index'],
                    "datatype": key['datatype'],
                    "shape": key['shape']
                }
            self.modelclient_parameters['outputs'] = output_parameters

        else:
            raise ValueError(
                "Bad url was provided and the model is not " +
                "running in specified target !")