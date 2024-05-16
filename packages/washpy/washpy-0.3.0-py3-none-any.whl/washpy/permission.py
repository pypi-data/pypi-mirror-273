"""
This module provides permissions, according to section 17.2.4.1 
of the Miele Professional IP Profile - Services document.
"""

from enum import Enum


class Service(Enum):
    """
    Enumeration of all services, that a permission might be assigned to.

    The integer codes are defined in hexadecimal.
    """

    IdentOrState: int = 0x01
    profUser_users: int = 0x11
    profUser_roles: int = 0x12
    WLAN: int = 0x21
    Security_Cloud: int = 0x22
    Settings: int = 0x31
    FileTransfer: int = 0x32
    profProgram: int = 0x41
    profService: int = 0x51
    profSensor: int = 0x52
    profPayment: int = 0x61
    profDosing: int = 0x71
    profLock: int = 0x91
    DOP2: int = 0x81


class Permission:
    """
    Captures the permisstion 16bit integer value into a python class.
    """

    service: Service
    """Allowed `Service`"""

    GET: bool
    """Allows HTTP GET request"""

    PUT: bool
    """Allows HTTP PUT request"""

    POST: bool
    """Allows HTTP PUT request"""

    DELETE: bool
    """Allwos HTTP DELETE request"""

    def __init__(self, permission_id: int = 0x0100) -> None:
        """
        `permission_id`: 16bit unsigned integer, with the following layout:

         | 8 bit      | 4 bit | 4 bit     |
         |------------|-------|-----------|
         | Service ID |  0000 | http mask |

        The http mask has 4 bits `abcd`. Each bit represents the capability to do one type of HTTP request:
          - `a`: HTTP GET
          - `b`: HTTP PUT
          - `c`: HTTP POST
          - `d`: HTTP DELETE

        Default value: `0x0100`: `Service.IdentOrState` service with no HTTP request permissions.

        **raises**: `ValueError`, if the permission id is invalid
        """
        self.service = Service(permission_id >> 8)

        self.GET = permission_id & 0b1000 == 0b1000
        self.PUT = permission_id & 0b100 == 0b100
        self.POST = permission_id & 0b10 == 0b10
        self.DELETE = permission_id & 0b1 == 0b1

    def __int__(self) -> int:
        """
        Turns the permission class back into the 16bit integer permission id.
        """
        id = self.service.value << 8
        if self.GET:
            id |= 0b1000
        if self.PUT:
            id |= 0b100
        if self.POST:
            id |= 0b10
        if self.DELETE:
            id |= 0b1
        return id

    def __repr__(self) -> str:
        return f"Permission({hex(int(self))})"

    def __str__(self) -> str:
        return f"Permission: {self.service}, GET={self.GET}, PUT={self.PUT}, POST={self.POST}, DELETE={self.DELETE}"
