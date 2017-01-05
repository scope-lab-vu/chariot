__author__ = "Subhav Pradhan"

import os
import logging

# Helper to create and return python logger. This uses environment variable CHARIOT_LOG_LEVEL to determine base log level.
def get_logger(name):
    logger = logging.getLogger(name)
    
    # Get base log level from environment variable.
    try:
        logLevel = os.environ["CHARIOT_LOG_LEVEL"]
    except KeyError:
        # If environment variable not set, use INFO as base.
        logLevel = "INFO" 
    
    if (logLevel == "DEBUG"):
        logger.setLevel(logging.DEBUG)
    elif (logLevel == "WARNING"):
        logger.setLevel(logging.WARNING)
    elif (logLevel == "ERROR"):
        logger.setLevel(logging.ERROR)
    elif (logLevel == "CRITICAL"):
        logger.setLevel(logging.CRITICAL)
    else:
        # If none of the above four is used as base log level,
        # then assume INFO.
        logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)

    return logger
