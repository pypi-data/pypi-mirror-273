from typing import Any, List
import numpy.typing as npt
import logging

NDArray = npt.NDArray[Any]
NDArrays = List[NDArray]

# Create logger
LOGGER_NAME = "armisticeai"
ARMISTICEAI_LOGGER = logging.getLogger(LOGGER_NAME)
ARMISTICEAI_LOGGER.setLevel(logging.DEBUG)

DEFAULT_FORMATTER = logging.Formatter(
    "%(levelname)s %(name)s %(asctime)s | %(filename)s:%(lineno)d | %(message)s"
)

# Configure console logger
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(DEFAULT_FORMATTER)
ARMISTICEAI_LOGGER.addHandler(console_handler)

logger = logging.getLogger(LOGGER_NAME)  # pylint: disable=invalid-name
log = logger.log  # pylint: disable=invalid-name
