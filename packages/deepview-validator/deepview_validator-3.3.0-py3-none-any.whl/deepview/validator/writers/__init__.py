# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from deepview.validator.writers.tensorboard import TensorBoardWriter
from deepview.validator.writers.console import ConsoleWriter
from deepview.validator.writers.core import Writer

include_symbols = True

def set_symbol_condition(include: bool):
    """
    This set the include_symbols to specify which logger to use throughout
    the validation process.

    Parameters
    ----------
        include: bool
            This is the condition to set include_symbols.
    """
    global include_symbols
    include_symbols = include

def logger(message: str, code: str=''):
    """
    Logs information to the terminal of the following types:
    
        1) Error
        2) Warning
        3) Info
        3) Success

    Parameters
    ----------
        message: str
            The message to print to the terminal.

        code: str
            The type of the message (error, warning, info, success).
    """
    if include_symbols:
        logger_with_symbols(message, code)
    else:
        logger_no_symbols(message, code)

def logger_with_symbols(message: str, code: str=''):
    """
    Logs information to the terminal of the following types:
    
        1) Error
        2) Warning
        3) Info
        3) Success

    Parameters
    ----------
        message: str
            The message to print to the terminal.

        code: str
            The type of the message (error, warning, info, success).
    """
    if code.upper() == 'ERROR':
        print(f'\t - ❌ [ERROR]: {message}')
        exit(1)
    elif code.upper() == 'WARNING':
        print(f'\t - ⚠️ [WARNING]: {message}')
    elif code.upper() == 'INFO':
        print(f'\t - ℹ️ [INFO]: {message}')
    elif code.upper() == 'SUCCESS':
        print(f'\t - ✅ [SUCCESS]: {message}')
    else:
        print(f'\t - {message}')

def logger_no_symbols(message: str, code: str=''):
    """
    Logs information to the terminal of the following types:
    
        1) Error
        2) Warning
        3) Info
        3) Success

    Parameters
    ----------
        message: str
            The message to print to the terminal.

        code: str
            The type of the message (error, warning, info, success).
    """
    if code.upper() == 'ERROR':
        print(f'\t - [ERROR]: {message}')
        exit(1)
    elif code.upper() == 'WARNING':
        print(f'\t - [WARNING]: {message}')
    elif code.upper() == 'INFO':
        print(f'\t - [INFO]: {message}')
    elif code.upper() == 'SUCCESS':
        print(f'\t - [SUCCESS]: {message}')
    else:
        print(f'\t - {message}')