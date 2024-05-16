from typing import Final, List
from pydantic import BaseModel


class User(BaseModel):
    """
    Represents a User as defined in section 17.4.1
    of the Miele Professional IP Profile - Services document.
    """

    ID: Final[int]
    """
    16bit integer, values 0..100, 65535 are reserved.

    Cannot be changed.
    """

    LoginName: Final[str]
    """
    max. 64 characters long

    Cannot be changed.
    """

    Password: str
    """
    Will be `'***'`, if the `User` is retrieved from a device.
    A device never returns the actual password.

    Password requirements, the password must contain:
      - min. 8 characters
      - uppercase characters
      - lowercase characters
      - special characters
      - numbers
    """

    Type: int = 1
    """
    | value    | user type |
    |----------|-----------|
    | 1        | HTTP user |
    | all else | reserved  |
    """

    Description: str
    """max. 64 characters long"""

    Roles: List[int]
    """
    List of all Role IDs the user is part of.

    Max. 32 `Role`s per `User`.
    """
