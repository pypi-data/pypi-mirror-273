"""
This module provides functionality around `Status`, according to section 4.3.4.2
of the Miele Professional IP Profile - Core document.
"""

from enum import Enum


class Status(Enum):
    """
    represents the <object:DeviceState>.Status

    Codes and descriptions are retrieved directly from the Miele IPprofileCore document.

    use the `status_from_code` method to convert from integer to Status

    """

    RESERVED = 0
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 0, 18..30, 36..63  | Reserved No use |
    """

    OFF = 1
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 1 | Appliance in off state |
    """

    STAND_BY = 2
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 2 | Appliance in stand-by|
    """

    PROGRAMMED = 3
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 3 | Appliance already programmed |
    """

    PROGRAMMED_WAITING_TO_START = 4
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 4 | Appliance already programmed and ready to start |
    """

    RUNNING = 5
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 5 | Appliance is running |
    """

    PAUSE = 6
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 6 | Appliance is in pause |
    """

    END_PROGRAMMED = 7
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 7 | Appliance end programmed task |
    """

    FAILURE = 8
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 8             | FAILURE     | 
    """

    PROGRAMME_INTERRUPTED = 9
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 9 | The appliance programmed tasks have been interrupted |
    """

    IDLE = 10
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 10 | Appliance is in idle state |
    """

    RINSE_HOLD = 11
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 11 | Appliance rinse hold |
    """

    SERVICE = 12
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 12 | Appliance in service state |
    """

    SUPERFREEZING = 13
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 13 | Appliance in superfreezing state |
    """

    SUPERCOOLING = 14
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 14 | Appliance in supercooling state |
    """

    SUPERHEATING = 15
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 15 | Appliance in superheating state |
    """

    MANUALCONTROL = 16
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 16 |Appliance is in manual program control state (e.g. manual external control on Benchmark machines) |
    """

    WATERDRAIN = 17
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 17 | Appliance in water drain state |
    """

    BOOT = 31
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 31 | Appliance is in booting state |
    """

    SAFE_STATE = 32
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 32 | Appliance is in safe state |
    """

    SHUTDOWN = 33
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 33 | Appliance is shutting down |
    """

    UPDATE = 34
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 34 | Appliance is in update state |
    """

    SYSTEST = 35
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 35 | Appliance is in systest state |
    """

    NON_STANDARDIZED = 64
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 64..127 | Non standardized |
    """

    DEFAULT = 144
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 144 | Default – proprietary |
    """

    LOCKED = 145
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 145 | Locked – proprietary |
    """

    SUPERCOOLING_SUPERFREEZING = 146
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 146 | Supercooling_Superfreezing - proprietary |
    """

    NOT_CONNECTED = 255
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 255 | No connection to this appliance |
    """

    PROPRIETARY = 128
    """
       | Integer Range | Description |
       |---------------|-------------|
       | 128..255 | Proprietary |
    """


def status_from_code(status_code: int) -> Status:
    """
    Converts integer status codes to Status enum objects,
    according to section 4.3.4.2.1 of the Miele IPprofileCore document.
    """
    # the code ranges 18...30 and 36...63 belong to the reserved value 0
    if (
        status_code >= 18
        and status_code <= 30
        or status_code >= 36
        and status_code <= 63
    ):
        return Status.RESERVED

    # the code range 64...127 is all NON_STANDARDIZED
    if status_code >= 64 and status_code <= 127:
        return Status.NON_STANDARDIZED

    # the code range 128..255 is PROPRIETARY, except for some codes in that range
    if (
        status_code >= 128
        and status_code <= 255
        and status_code not in {144, 145, 146, 255}
    ):
        return Status.PROPRIETARY

    return Status(status_code)


class StatusException(Exception):
    """
    This exception is raised, if the status of the machine
    is incompatible to the requested action.
    """
