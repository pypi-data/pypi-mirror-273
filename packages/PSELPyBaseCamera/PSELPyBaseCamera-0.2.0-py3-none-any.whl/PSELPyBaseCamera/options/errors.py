#  Copyright (c) 2023. Photonic Science and Engineering Ltd.
from __future__ import annotations

from .types import OptionType


class SettingCameraOptionValueError(ValueError):
    def __init__(
        self, option_name: str, option_value: OptionType, camera_name: str, *args
    ):
        """Error class for when an option fails to be set in a camera.

        Args:
            option_name: Name of the option that failed to be set.
            option_value: Value that caused error.
            camera_name: Camera that the option was being set on.
        """
        super().__init__(*args)
        self.option_name: str = option_name
        self.option_value: OptionType = option_value
        self.camera_name: str = camera_name
