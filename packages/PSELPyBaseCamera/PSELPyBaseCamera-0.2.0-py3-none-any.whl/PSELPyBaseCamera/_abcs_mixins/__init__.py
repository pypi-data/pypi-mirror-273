#  Copyright (c) 2023. Photonic Science and Engineering Ltd.
from __future__ import annotations

from ._abcs_mixins import AcquisitionABC
from ._abcs_mixins import BackgroundCorrection
from ._abcs_mixins import BrightCornerCorrectionABC
from ._abcs_mixins import BrightPixelCorrectionABC
from ._abcs_mixins import BrightSpotCorrectionABC
from ._abcs_mixins import CameraNameMixin
from ._abcs_mixins import CameraOptionsMixin
from ._abcs_mixins import CameraTypeMixin
from ._abcs_mixins import ClockSpeedABC
from ._abcs_mixins import ConnectionABC
from ._abcs_mixins import CoolingModeABC
from ._abcs_mixins import CyclopsBin2ModeABC
from ._abcs_mixins import DLLABC
from ._abcs_mixins import ExposureABC
from ._abcs_mixins import FlatFieldCorrectionABC
from ._abcs_mixins import FusionABC
from ._abcs_mixins import FusionLowNoiseABC
from ._abcs_mixins import FusionNoiseReductionFactorABC
from ._abcs_mixins import GainModeABC
from ._abcs_mixins import HardwareBinningABC
from ._abcs_mixins import HighPrecisionRemapping
from ._abcs_mixins import ImageModeABC
from ._abcs_mixins import IntensifierGainABC
from ._abcs_mixins import IPortABC
from ._abcs_mixins import Is14BitCameraABC
from ._abcs_mixins import IsCyclopsCameraABC
from ._abcs_mixins import OffsetSubtractionABC
from ._abcs_mixins import ReadCCDTemperatureABC
from ._abcs_mixins import RemapABC
from ._abcs_mixins import RemapClipMixin
from ._abcs_mixins import RemapSmoothMixin
from ._abcs_mixins import SequenceAcquisitionABC
from ._abcs_mixins import SharpeningABC
from ._abcs_mixins import SizeABC
from ._abcs_mixins import SoftwareBinningABC
from ._abcs_mixins import StreamingABC
from ._abcs_mixins import SubAreaABC
from ._abcs_mixins import SubAreaBinningABC
from ._abcs_mixins import TriggerModeABC
from ._abcs_mixins import UpdateSizesMixin
from ._abcs_mixins import VideoGainABC

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
    "CoreCamera",
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


class CoreCamera:
    CORE_CLASSES = [
        ConnectionABC,
        CameraTypeMixin,
        CameraNameMixin,
        ImageModeABC,
        CameraOptionsMixin,
    ]

    def __init_subclass__(cls, **kwargs):
        for required_cls in CoreCamera.CORE_CLASSES:
            if not issubclass(cls, required_cls):
                raise TypeError(f"{required_cls} is a required camera dependency")
        super().__init_subclass__(**kwargs)
