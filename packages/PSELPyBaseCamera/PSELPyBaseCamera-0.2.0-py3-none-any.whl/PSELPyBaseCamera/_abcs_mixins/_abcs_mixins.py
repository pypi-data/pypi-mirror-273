#  Copyright (c) 2023. Photonic Science and Engineering Ltd.
from __future__ import annotations

import ctypes as ct
import logging
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Callable
from typing import Optional

import numpy as np

from PSELPyBaseCamera.options import OptionSetterResult
from PSELPyBaseCamera.options import OptionType
from PSELPyBaseCamera.options import SettingCameraOptionValueError

PointerType = Any
_logger = logging.getLogger(__name__)

__all__ = [
    "AcquisitionABC",
    "BackgroundCorrection",
    "BrightCornerCorrectionABC",
    "BrightPixelCorrectionABC",
    "BrightSpotCorrectionABC",
    "CameraNameMixin",
    "CameraOptionsMixin",
    "CameraTypeMixin",
    "ClockSpeedABC",
    "ConnectionABC",
    "CoolingModeABC",
    "CyclopsBin2ModeABC",
    "DLLABC",
    "ExposureABC",
    "FlatFieldCorrectionABC",
    "FusionABC",
    "FusionLowNoiseABC",
    "FusionNoiseReductionFactorABC",
    "GainModeABC",
    "HardwareBinningABC",
    "HighPrecisionRemapping",
    "ImageModeABC",
    "IntensifierGainABC",
    "IPortABC",
    "Is14BitCameraABC",
    "IsCyclopsCameraABC",
    "OffsetSubtractionABC",
    "ReadCCDTemperatureABC",
    "RemapABC",
    "RemapClipMixin",
    "RemapSmoothMixin",
    "SequenceAcquisitionABC",
    "SharpeningABC",
    "SizeABC",
    "SoftwareBinningABC",
    "StreamingABC",
    "SubAreaABC",
    "SubAreaBinningABC",
    "TriggerModeABC",
    "UpdateSizesMixin",
    "VideoGainABC",
]

# Connection


class ConnectionABC(ABC):
    @abstractmethod
    def open(self):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError


class DLLABC(ABC):
    @abstractmethod
    def load_cam_dll(self):
        raise NotImplementedError

    @abstractmethod
    def unload_cam_dll(self):
        raise NotImplementedError

    @abstractmethod
    def init_functions(self):
        raise NotImplementedError


# Camera properties
class CameraTypeMixin:
    @property
    def camera_type(self) -> str:
        return self.__class__.__name__


class CameraNameMixin:
    _name = ""

    @property
    def name(self) -> str:
        """Name of the camera.

        Returns:
            name of the camera
        """
        return self._name


class IPortABC(ABC):
    @property
    @abstractmethod
    def is_iport(self):
        raise NotImplementedError

    def select_iport_device(self):
        raise NotImplementedError


class Is14BitCameraABC(ABC):
    @property
    @abstractmethod
    def is_14_bit_camera(self):
        raise NotImplementedError


class IsCyclopsCameraABC(ABC):
    @property
    @abstractmethod
    def is_cyclops_camera(self):
        raise NotImplementedError


class ImageModeABC(ABC):
    @property
    @abstractmethod
    def image_mode(self):
        raise NotImplementedError


# Camera Options
class CameraOptionsMixin:
    _camera_options = []
    _set_camera_option_routing_dict: dict[str, Callable[..., OptionSetterResult]] = {}
    _get_camera_option_routing_dict: dict[str, Callable[..., OptionType]] = {}

    def __init_subclass__(cls, **kwargs):
        # This mixin requires the CameraNameMixin to be present
        if not issubclass(cls, CameraNameMixin):
            raise TypeError(
                f"{__class__.__name__} requires CameraNameMixin to be inherited."
            )
        super().__init_subclass__(**kwargs)

    def get_camera_options(self):
        return self._camera_options

    def get_camera_option_names(self) -> list[str]:
        """Get a list of all settable camera option names that can be used in
        conjunction with :py:meth:`PyFDS.FDS.set_camera_option_value`.

        Returns:
            list of settable camera option names
        """
        return list(self._set_camera_option_routing_dict.keys())

    def get_camera_option_value(self, name: str) -> OptionType:
        if name in self._get_camera_option_routing_dict:
            return self._get_camera_option_routing_dict[name]()
        else:
            _logger.error(f"Option does not have a get method: {name}")
            raise ValueError(f"Option does not have a get method: {name}")

    def set_camera_option_value(
        self,
        option_name: str,
        option_value: OptionType,
        update_value_callback: Callable[[OptionType], bool],
    ) -> bool:
        """Set the value of a camera option.

        Args:
            option_name: Name of the option.
            option_value: Value to set this option to.
            update_value_callback: Function callback to set the named options value at
                the source of this call.
        Returns:
            Boolean indicating success or failure in setting option in the camera
            driver.
        Raises:
            SettingCameraOptionValueError: if setting the option in the camera fails.
        """
        if option_name not in self._set_camera_option_routing_dict:
            raise KeyError(f"{option_name} not in dict. Setting with {option_value}")

        _logger.info(f"Setting option {option_name} with value {option_value}")

        setter = self._set_camera_option_routing_dict[option_name]

        if isinstance(option_value, tuple):
            result = setter(*option_value)
        else:
            result = setter(option_value)

        _logger.info(f"Setting option {option_name} result={result}")

        if result is OptionSetterResult.COMPLETED:
            # if result:
            return True
        elif result is OptionSetterResult.FAILED:
            # if not result:
            _logger.log(
                logging.ERROR,
                f"set_camera_option_value for {self.name} failed to set"
                f" {option_name} to {option_value}",
            )
            # TODO: This should try and read the value the driver has back out so that
            #  it can be reflected in the GUI
            raise SettingCameraOptionValueError(option_name, option_value, self.name)
        elif result is OptionSetterResult.CHECK:
            new_value = self.get_camera_option_value(option_name)
            _logger.log(
                logging.INFO,
                f"The driver returned a different value ({new_value}) to the one"
                f" requested by the user ({option_value}). Callback triggered to"
                " reflect this change",
            )
            _logger.info(update_value_callback)
            _logger.info(type(update_value_callback))
            res = update_value_callback(new_value)
            _logger.info(f"Callback result {res}")
            return res
        else:
            raise ValueError(
                f"Invalid result when setting option {option_name} to {option_value},"
                f" recieved {result}."
            )

    @staticmethod
    def _disable_camera_option(options: list, *names) -> list:
        """Certain settings can require a camera to have options made unavailable.
        This function can be used to disable the option within the camera's option
        list.

        Names should provide the full path excliuding the '<camera name> settings'
        group.

        Note: This will *only* have an effect to the local variable, any other systems
        that use the camera options should read them again and rebuild their data
        structure.

        Args:
            options: options list to edit.
            names: Series of parameter names, path to parameter to delete, final one and
                all its children are deleted.
        Raises:
            ValueError: If the target cannot be found due to invalid path or missing
                item.
        """

        def _disable_camera_option_worker(children: list, wnames: tuple) -> list:
            for i in range(len(children)):
                if children[i]["name"] == wnames[0]:
                    if len(wnames) == 1:
                        children[i]["readonly"] = True
                        children[i]["visible"] = False
                        children[i]["enabled"] = False
                        _logger.info(f"disabled option {children[i]['name']}")
                    else:
                        if "children" not in children[i]:
                            raise ValueError(
                                "Option path invalid: option has no children"
                            )
                        res = _disable_camera_option_worker(
                            children[i]["children"], wnames[1:]
                        )
                        children[i]["children"] = res
                    return children
            raise ValueError("Option path invalid: option not found")

        options[0]["children"] = _disable_camera_option_worker(
            options[0]["children"], names
        )
        return options

    @staticmethod
    def create_camera_option(current_options: list, option: dict, *names) -> list:
        def _create_camera_option_worker(children: list, wnames: tuple) -> list:
            for i in range(len(children)):
                print(f"(i) -- {children[i]['name']}")
                if children[i]["name"] == wnames[0]:
                    if len(wnames) == 1:
                        if "children" in children[i]:
                            children[i]["children"].append(option)
                        else:
                            children[i]["children"] = [option]
                    else:
                        if "children" not in children[i]:
                            raise ValueError(
                                "Option path invalid: option has no children"
                            )
                        res = _create_camera_option_worker(
                            children[i]["children"], wnames[1:]
                        )
                        children[i]["children"] = res
                    return children
            raise ValueError("Option path invalid: option not found")

        current_options[0]["children"] = _create_camera_option_worker(
            current_options[0]["children"], names
        )
        return current_options


# Acquisition


class AcquisitionABC(ABC):
    @abstractmethod
    def snap(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def snap_and_return(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def abort_snap(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_image_pointer(self):
        raise NotImplementedError

    @abstractmethod
    def get_image(
        self, image_pointer=None, tsize=None
    ) -> tuple[tuple[int, int], np.ndarray]:
        raise NotImplementedError

    @abstractmethod
    def get_raw_image(
        self, image_pointer: Optional[PointerType] = None
    ) -> tuple[tuple[int, int], np.ndarray]:
        raise NotImplementedError


class SequenceAcquisitionABC(ABC):
    @abstractmethod
    def allocate_sequence_buffer(self):
        raise NotImplementedError

    @abstractmethod
    def transfer_image_pointer(self):
        raise NotImplementedError

    @abstractmethod
    def free_sequence_buffer(self):
        raise NotImplementedError


class StreamingABC(ABC):
    @abstractmethod
    def enable_streaming(self, enable: bool):
        raise NotImplementedError


class FusionABC(ABC):
    def __init_subclass__(cls, **kwargs):
        # This ABC requires AcquisitionABC to be present
        if not issubclass(cls, AcquisitionABC):
            raise TypeError(
                f"{__class__.__name__} requires AcquisitionABC to be inherited."
            )

        # This ABC requires Is14BitCameraABC to be present
        if not issubclass(cls, Is14BitCameraABC):
            raise TypeError(
                f"{__class__.__name__} requires Is14BitCameraABC to be inherited."
            )
        super().__init_subclass__(**kwargs)

    def enable_fusion(self, enable: bool):
        raise NotImplementedError


class FusionNoiseReductionFactorABC(ABC):
    def __init_subclass__(cls, **kwargs):
        # This ABC requires FusionABC to be present
        if not issubclass(cls, FusionABC):
            raise TypeError(f"{__class__.__name__} requires FusionABC to be inherited.")

    def set_fusion_noise_reduction_factor(self, value: int):
        raise NotImplementedError


class FusionLowNoiseABC(ABC):
    def __init_subclass__(cls, **kwargs):
        # This ABC requires FusionABC to be present
        if not issubclass(cls, FusionABC):
            raise TypeError(f"{__class__.__name__} requires FusionABC to be inherited.")

    def enable_fusion_low_noise(self, enable: bool):
        raise NotImplementedError


class CyclopsBin2ModeABC(ABC):
    def enable_bin2_mode(self, enable: bool):
        raise NotImplementedError


# Corrections


class OffsetSubtractionABC(ABC):
    @abstractmethod
    def enable_offset_subtraction(self, enable: bool):
        raise NotImplementedError


class BrightPixelCorrectionABC(ABC):
    @abstractmethod
    def enable_bright_pixel_correction(self, enable: bool):
        raise NotImplementedError


class BrightCornerCorrectionABC(ABC):
    @abstractmethod
    def enable_bright_corner_correction(self, enable: bool):
        raise NotImplementedError


class BrightSpotCorrectionABC(ABC):
    @abstractmethod
    def enable_bright_spot_correction(self, enable: bool):
        raise NotImplementedError


class FlatFieldCorrectionABC(ABC):
    @abstractmethod
    def enable_flat_field_correction(self, enable: bool):
        raise NotImplementedError


class SharpeningABC(ABC):
    @abstractmethod
    def enable_sharpening(self, enable: bool):
        raise NotImplementedError


class BackgroundCorrection(ABC):
    @abstractmethod
    def enable_background_correction(self, enable: bool):
        raise NotImplementedError


class RemapSmoothMixin:
    _smooth = False

    def enable_smooth(self, enable: bool):
        self._smooth = enable


class RemapClipMixin:
    _clip = False

    def enable_clip(self, enable: bool):
        self._clip = enable


class RemapABC(ABC):
    _remapping = False

    @abstractmethod
    def open_map(self, file_name: str = "distortion.map"):
        raise NotImplementedError

    def enable_remapping(self, enable: bool):
        self._remapping = enable

    @abstractmethod
    def remap(self, image_pointer: PointerType, Nx: int, Ny: int):
        raise NotImplementedError


class HighPrecisionRemapping(ABC):
    @abstractmethod
    def set_remap_parameters(self):
        raise NotImplementedError

    @abstractmethod
    def set_HPM_x(self, value: int):
        raise NotImplementedError

    @abstractmethod
    def set_HPM_y(self, value: int):
        raise NotImplementedError

    @abstractmethod
    def set_HPM_rotation(self, value: int):
        raise NotImplementedError

    @abstractmethod
    def set_HPM_sub_width(self, value: int):
        raise NotImplementedError

    @abstractmethod
    def set_HPM_sub_height(self, value: int):
        raise NotImplementedError

    @abstractmethod
    def set_HPM_angular(self, enable: bool):
        raise NotImplementedError

    @abstractmethod
    def generate_HPM_working_map(self):
        raise NotImplementedError

    @abstractmethod
    def get_HPM_remap_size(self):
        raise NotImplementedError

    @abstractmethod
    def high_precision_remap(self, image_pointer: PointerType):
        raise NotImplementedError


# Binning
class HardwareBinningABC(ABC):
    @abstractmethod
    def set_hardware_binning(self, xbin: int, ybin: int):
        raise NotImplementedError


class SoftwareBinningABC(ABC):
    @abstractmethod
    def set_software_binning(self, xbin: int, ybin: int):
        raise NotImplementedError

    @abstractmethod
    def software_bin_image(self, image_pointer: PointerType, nx: int, ny: int):
        raise NotImplementedError


# Sub Area
class SubAreaABC(ABC):
    @abstractmethod
    def set_sub_area(self, left: int, right: int, top: int, bottom: int):
        raise NotImplementedError


class SubAreaBinningABC(ABC):
    @abstractmethod
    def set_sub_area_and_binning(
        self, left: int, right: int, top: int, bottom: int, xbin: int, ybin: int
    ):
        raise NotImplementedError


# Size
class SizeABC(ABC):
    @property
    @abstractmethod
    def size(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def size_max(self):
        raise NotImplementedError


class UpdateSizesMixin:
    safe_buffer = None
    _size_max = None

    def __init_subclass__(cls, **kwargs):
        print("init subclass")
        # This mixin requires the SizeABC to be present
        if not issubclass(cls, SizeABC):
            raise TypeError(f"{__class__.__name__} requires SizeABC to be inherited.")
        super().__init_subclass__(**kwargs)

    def update_size(self):
        """Update the size property and reallocate the safe buffer to the appropriate
        size

        Returns:
            new size of images
        """
        Nx, Ny = self.size
        if Nx != 0 and Ny != 0:
            buff = ct.c_char * (Nx * (Ny + 1) * self._byte_depth)
            self.safe_buffer = buff()
            return Nx, Ny
        return None

    def update_size_max(self):
        """Query the driver to update the maximum allowed image size.

        Returns:
            maximum image size
        """
        Nx, Ny = self.size_max
        self._size_max = (Nx, Ny)
        return self._size_max


# Exposure
class ExposureABC(ABC):
    @abstractmethod
    def set_exposure(self, expo: int, unit: str):
        raise NotImplementedError


# Trigger mode
class TriggerModeABC(ABC):
    @abstractmethod
    def set_trigger_mode(self, mode):
        raise NotImplementedError


# Gain Mode
class GainModeABC(ABC):
    @abstractmethod
    def set_gain_mode(self, mode):
        raise NotImplementedError


# Intensifier Gain
class IntensifierGainABC(ABC):
    @abstractmethod
    def set_intensifier_gain(self, gain: int):
        raise NotImplementedError


# Video Gain
class VideoGainABC(ABC):
    @abstractmethod
    def set_video_gain(self, gain: int):
        raise NotImplementedError


# Clock Speed
class ClockSpeedABC(ABC):
    @abstractmethod
    def set_clock_speed(self, speed):
        raise NotImplementedError


# Cooling Mode
class CoolingModeABC(ABC):
    @abstractmethod
    def set_cooling_mode(self, mode):
        raise NotImplementedError


# Read CCD Temperature
class ReadCCDTemperatureABC(ABC):
    @abstractmethod
    def read_CCD_temperature(self):
        raise NotImplementedError
