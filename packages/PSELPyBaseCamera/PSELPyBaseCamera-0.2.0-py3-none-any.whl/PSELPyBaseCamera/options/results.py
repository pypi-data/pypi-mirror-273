#  Copyright (c) 2023. Photonic Science and Engineering Ltd.
from __future__ import annotations

from enum import IntEnum


class OptionSetterResult(IntEnum):
    """Enumeration of possible results from setting an option within the camera.

    COMPLETED and CHECK will evaluate to True in a boolean expression, FAILED will
    evaluate to False in a boolean expression.

    COMPLETED -> Option was set successfully

    FAILED -> Option setting failed

    CHECK -> Option was set but driver may have altered value, the value of this
    setting should be read out to ensure the correct value is being stored.
    """

    FAILED = 0
    COMPLETED = 1
    CHECK = 2
