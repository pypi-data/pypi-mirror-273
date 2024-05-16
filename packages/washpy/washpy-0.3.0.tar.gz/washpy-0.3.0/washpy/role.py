from washpy.permission import Permission

from typing import Final, List

from pydantic import BaseModel


class Role(BaseModel):
    """
    Represents a Role as defined in section 17.3.1
    of the Miele Professional IP Profile - Services document.
    """

    ID: Final[int]
    """
    16bit integer, values 0..100 and 65535 are reserved.

    Cannot be changed.
    """

    Description: str
    """max. 64 characters long"""

    Permissions: List[int]
    """max. 32 entries long. each entry is a Permission ID, see `washpy.permission.Permission`."""

    def __str__(self) -> str:
        """
        Nice human-readable representation. Permission IDs are parsed to Permissions.
        """
        s = f"Role ID={self.ID}\nDescription='{self.Description}'\n"
        for perm in self.Permissions:
            s += f"\n{Permission(perm)}"
        return s
