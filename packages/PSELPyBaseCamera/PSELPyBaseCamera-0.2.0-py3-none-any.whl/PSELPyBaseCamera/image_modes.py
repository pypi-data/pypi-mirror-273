#  Copyright (c) 2023. Photonic Science and Engineering Ltd.
from __future__ import annotations

import logging
from enum import auto
from enum import Enum
from typing import Type
from typing import Union

import numpy as np

from .logging_tools import *

_logger = logging.getLogger(__name__)


class ImageMode(Enum):
    """Image modes supported by PSELViewer."""

    L = auto()
    P = auto()
    RGB = auto()
    RGBA = auto()
    I16 = auto()
    I = auto()
    F = auto()


INTEGER_MODES = [
    ImageMode.L,
    ImageMode.P,
    ImageMode.RGB,
    ImageMode.RGBA,
    ImageMode.I16,
    ImageMode.I,
]
FLOATING_POINT_MODES = [
    ImageMode.F,
]


def image_mode_to_string(mode: ImageMode) -> str:
    """Convert an image mode to its string representation.

    Args:
        mode: Image mode.
    Returns:
        Image mode's string representation.
    """
    image_modes_string = {
        ImageMode.L: "L",
        ImageMode.P: "P",
        ImageMode.RGB: "RGB",
        ImageMode.RGBA: "RGBA",
        ImageMode.I16: "I;16",
        ImageMode.I: "I",
        ImageMode.F: "F",
    }
    return image_modes_string[mode]


def string_to_image_mode(string: str) -> ImageMode:
    """Convert an image mode string to its ImageMode value.

    Args:
        string: String representation of image mode
    Returns:
        Image mode value represetned by the string.
    """
    string_image_modes = {
        "L": ImageMode.L,
        "P": ImageMode.P,
        "RGB": ImageMode.RGB,
        "RGBA": ImageMode.RGBA,
        "I;16": ImageMode.I16,
        "I": ImageMode.I,
        "F": ImageMode.F,
    }
    return string_image_modes[string]


def image_mode_to_np_number(mode: ImageMode):
    """Convert an image mode to its numpy dtype.

    NOTE: This is a surjective function.

    Args:
        mode: Image mode.
    Returns:
        Image mode's numpy dtype.
    """
    image_modes = {
        ImageMode.L: np.uint8,
        ImageMode.P: np.uint8,
        ImageMode.RGB: np.uint8,
        ImageMode.RGBA: np.uint8,
        ImageMode.I16: np.uint16,
        ImageMode.I: np.int32,
        ImageMode.F: np.float32,
    }
    return image_modes[mode]


def image_mode_to_range(mode: ImageMode) -> tuple[int, int]:
    """Return the range of an image mode.
    Args:
        mode: The image mode to get the range of.
    Returns:
        Range of the given mode.
    """
    image_modes_to_range = {
        ImageMode.L: (0, 255),
        ImageMode.P: (0, 255),
        ImageMode.RGB: (0, 255),
        ImageMode.RGBA: (0, 255),
        ImageMode.I16: (0, 65535),
        ImageMode.I: (0, 2 ** 30 - 1),
        ImageMode.F: (0, 2 ** 30 - 1),
    }
    return image_modes_to_range[mode]
