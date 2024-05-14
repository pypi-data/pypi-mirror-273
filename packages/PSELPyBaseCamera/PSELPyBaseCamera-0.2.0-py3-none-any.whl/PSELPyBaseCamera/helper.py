#  Copyright (c) 2023. Photonic Science and Engineering Ltd.
"""File of helper functions for cameras."""
from __future__ import annotations

import ctypes as ct
import logging
from pathlib import Path
from typing import Any
from typing import Union

import numpy as np

from .image_modes import image_mode_to_np_number
from PSELPyBaseCamera.options import OptionSetterResult

_logger = logging.getLogger(__name__)

__all__ = [
    "_map_result_to_enum",
    "c_int_p",
    "c_ulong_p",
    "c_char_p",
    "c_ushort_p",
    "get_dll_path",
    "has_binning",
    "has_high_performance_mapping",
    "has_high_performance_mapping",
    "has_intensifier",
    "has_rotate",
    "image_pointer_to_numpy_array",
]


c_ushort_p = ct.POINTER(ct.c_ushort)
c_int_p = ct.POINTER(ct.c_int)
c_ulong_p = ct.POINTER(ct.c_ulong)
c_char_p = ct.POINTER(ct.c_char)


def get_dll_path(path: Path) -> tuple[bool, Union[int, Path]]:
    """Function that searches path for camera dll. There must be exactly 1 .dll file.

    Args:
        Path to camera folder
    Returns:
        Tuple where the first element indicates success or failure. The second is the
            dll path on success, and the number of .dll files found on failure
    """
    count = 0
    dll_path = Path()
    _logger.debug(f"Looking for dll in {path}")
    for file in path.iterdir():
        if file.suffix == ".dll":
            dll_path = file
            count += 1

    if count != 1:
        _logger.error(
            f"Too many {count} dll's found, please check that you only have 1 dll file"
            f" present in {path}"
        )
        return False, count
    else:
        _logger.debug(f"Found dll at {dll_path}")
        return True, dll_path


def _read_ps_setup(cwd: Path, name: str) -> list[str]:
    path = Path(cwd / name / "PSL_camera_files" / "ps_setup.dat").resolve()
    if not path.exists():
        _logger.info(f"Unable to find ps_setup.dat, does it not exist at {path}?")
        return []

    _logger.debug(f"Reading ps_setup.dat: {path}")
    with path.open(mode="r") as file:
        lines = file.readlines()
    return lines


def _map_result_to_enum(result: Any) -> OptionSetterResult:
    """Helper function to map any truthy/falsy result from driver to
    `OptionSetterResult.COMPLETED` or `OptionSetterResult.FAILED`.

    This function is not suitable for option setters where the driver may return
    truthy, but has changed the options value to do so. This requires
    OptionSetterResult.CHECK which must be handled separately.

    Args:
        Boolean-like value to be mapped to OptionSetterResult enum
    Returns:
        OptionSetterResult enum value based on result
    """
    if result:
        return OptionSetterResult.COMPLETED
    else:
        return OptionSetterResult.FAILED


# TODO: The 4 has_xxx functions can be refactored into one function that takes sequence of options to search for.


def has_high_performance_mapping(cwd: Path, name: str) -> bool:
    """Function that searches ps_setup.dat to find if the camera has high performance
    mapping.

    Args:
        cwd: path to current working directory
        name: camera name
    Returns:
        boolean indicating if the camera has high performance mapping
    """
    lines = _read_ps_setup(cwd, name)

    for line in lines:
        (option, _, value) = line.strip().partition("=")
        if option == "viewer_use_hp_mapping":
            res = bool(int(value))
            _logger.debug(f"high performance mapping option found with value={res}")
            return res
    _logger.info("high performance mapping option not found, defaulting to False")
    return False


def has_binning(cwd: Path, name: str) -> bool:
    """Function that searches ps_setup.dat to find if the camera has harware binning.

    Args:
        cwd: path to current working directory
        name: camera name
    Returns:
        boolean indicating if the camera has harware binning
    """
    lines = _read_ps_setup(cwd, name)

    for line in lines:
        (option, _, value) = line.strip().partition("=")
        if option == "binning_supported":
            res = bool(int(value))
            _logger.debug(f"binning option found with value={res}")
            return res
    _logger.info("has binning option not found, defaulting to False")
    return False


def has_intensifier(cwd: Path, name: str) -> bool:
    """Function that searches ps_setup.dat to find if the camera has an intensifier.

    Args:
        cwd: path to current working directory
        name: camera name
    Returns:
        boolean indicating if the camera has an intensifier
    """
    lines = _read_ps_setup(cwd, name)

    for line in lines:
        (option, _, value) = line.strip().partition("=")
        if option in (
            "intensifiergaincanbeset",
            "IntensifierGainCanBeSet",
            "HasIntensifier",
            "hasintensifier",
        ):
            res = bool(int(value))
            _logger.debug(f"has intensifier option found with value={res}")
            return res
    _logger.info("has intensifier option not found, defaulting to True")
    return True


def has_rotate(cwd: Path, name: str) -> bool:
    """Function that searches ps_setup.dat to find if the camera has a rotation option.

    Args:
        cwd: path to current working directory
        name: camera name
    Returns:
        boolean indicating if the camera has a rotation option
    """
    lines = _read_ps_setup(cwd, name)

    for line in lines:
        (option, _, value) = line.strip().partition("=")
        if option == "use_rotation":
            res = bool(int(value))
            _logger.debug(f"has rotate option found with value={res}")
            return res
    _logger.info("has rotate option not found, defaulting to False")
    return False


def image_pointer_to_numpy_array(image_pointer, size, mode, depth=1):
    nx, ny = size
    return np.frombuffer(
        image_pointer[0 : depth * nx * ny], image_mode_to_np_number(mode)
    ).reshape((ny, nx))
    # return np.array(image_pointer[0 : nx * ny], image_mode_to_np_number(mode)).reshape(
    #     (ny, nx)
    # )
    # return np.ndarray((ny, nx), image_mode_to_np_number(mode), image_pointer[0:nx*ny])
