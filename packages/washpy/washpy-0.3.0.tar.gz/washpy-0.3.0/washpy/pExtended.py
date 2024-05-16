from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class pExtendedPWM507(BaseModel):
    """
    This is my best effort attempt at capturing the pExtended field in a python struct,
    tailored to the PWM 507 machine.

    Some of these fields are completely missing from the official Miele documentation,
    some are spelled a little differently, some have a slightly different type.
    """

    DoorOpen: bool
    DeviceLocked: bool
    SpinningSpeed: Optional[int]
    TargetSpinningSpeed: int
    CurrentSpinningSpeed: int
    SISetTemperature: List[int]
    SIBlockTargetTemperature: int
    WaitingForPayment: bool
    pProgramphase: int
    Extras: Dict[str, bool]
    AutoDosing: Optional[Dict[str, Any]]
    ProgramID: Optional[int]
    ProgramName: Optional[str]
    StepID: Optional[int]
    StepName: Optional[str]
    CurrentLoadWeight: int
    SINominalLoad: int
    SISetLoad: int
    SICurrentLoad: int

    # undocumented
    SICurrentTemperature: List[int]
    # undocumented
    BlockID: int
    # undocumented
    BlockName: str

    # deprecated
    Temperature: List[int]
    # deprecated
    TargetTemperature: List[int]
    # deprecated
    CurrentTemperature: List[int]
