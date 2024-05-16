from typing import Any, Dict, Final, List, Optional, Union
import requests

import datetime

from washpy.authenticate import authenticate
from washpy.post_new_password import post_new_password
from washpy.state import State
from washpy.status import *
from washpy.role import Role
from washpy.user import User


class DeviceUser:
    """
    Represents a user on a device.

    This class is used to interface with the actual machine,
    most of the methods of this class perform HTTP requests.
    """

    device_url: Final[str]
    """e.g. `'https://192.168.1.251/Devices/000116343328'`"""

    user: Final[str]
    """username"""

    password: str

    token: str
    """a bearer-token, used for authenticating a user with a device at every other XKM API endpoint"""

    timeout: datetime.timedelta
    """
    timedelta. From the date when the `token` was last used,
    the `token` stays valid for the duration of `timeout`
    """

    last_used: datetime.datetime
    """date when the `token` was last used"""

    def __init__(self, device_url: str, user: str, password: str) -> None:
        """
        `device_url`: e.g. `'https://192.168.1.251/Devices/000116343328'`

        `user`: a username

        `password`: the password of user

        Authenticates the user at the specified machine

        **raises**: see `washpy.authenticate`
        """
        self.user = user
        self.password = password
        self.device_url = device_url
        self.last_used = datetime.datetime.now()
        (self.token, self.timeout) = authenticate(
            self.device_url, self.user, self.password
        )

    def __repr__(self) -> str:
        return (
            f"DeviceUser(device_url='{self.device_url}', "
            f"user='{self.user}', "
            f"password='~~ HIDDEN ~~', "
            f"token='{self.token}', "
            f"timeout={self.timeout.__repr__()}, "
            f"last_used={self.last_used.__repr__()}) "
        )

    # ~~~ private HTTP request section ~~~

    def _do_get_request(self, api_endpoint: str) -> Dict[str, Any]:
        """
        queries the api_endpoint, e.g. the `/State` endpoint, of the machine.

        **returns**: the body of the response as an unpacked json object

        **raises**: ValueError, if the GET request was unsuccessfull
        """
        url = self.device_url + api_endpoint

        payload = {}
        headers = {"Authorization": f"Bearer {self.token}"}

        now = self.refresh_authentication()
        response = requests.request(
            "GET", url, headers=headers, data=payload, verify=False
        )

        if response.status_code != 200:
            raise ValueError(f"Unable to GET: got HTTP response {response}")
        self.last_used = now
        return response.json()

    def _do_post_request(self, api_endpoint: str, payload: str) -> None:
        """
        Does a POST request to the specified API endpoint.

        **raises**: ValueError, if the POST request was unsuccessfull
        """
        url = self.device_url + api_endpoint

        headers = {"Authorization": f"Bearer {self.token}"}

        now = self.refresh_authentication()
        response = requests.request(
            "POST", url, headers=headers, data=payload, verify=False
        )

        if response.status_code != 201:
            raise ValueError(f"Unable to POST: got HTTP response {response}")
        self.last_used = now

    def _do_put_request(self, api_endpoint: str, payload: str) -> None:
        """
        Does a PUT request to the specified API endpoint.

        **raises**: ValueError, if the PUT request was unsuccessfull
        """
        url = self.device_url + api_endpoint

        headers = {"Authorization": f"Bearer {self.token}"}

        now = self.refresh_authentication()
        response = requests.request(
            "PUT", url, headers=headers, data=payload, verify=False
        )

        if response.status_code != 200:
            raise ValueError(f"Unable to PUT: got HTTP response {response}")
        self.last_used = now

    def _do_delete_request(self, api_endpoint: str) -> None:
        """
        Does a DELETE request to the specified API endpoint.

        **raises**: ValueError, if the DELETE request was unsuccessfull
        """
        url = self.device_url + api_endpoint

        headers = {"Authorization": f"Bearer {self.token}"}

        payload = {}
        now = self.refresh_authentication()
        response = requests.request(
            "DELETE", url, headers=headers, data=payload, verify=False
        )

        if response.status_code != 204:
            raise ValueError(f"Unable to DELETE: got HTTP response {response}")
        self.last_used = now

    # ~~~ basic management section ~~~

    def refresh_authentication(self) -> datetime.datetime:
        """
        if self.token is only valid for less then 10 seconds
        or if it is invalid,
        refresh it.

        **returns**: the point in time at which the check has happened

        **raises**: see `washpy.authenticate`
        """
        now = datetime.datetime.now()
        token_valid_date = self.last_used + self.timeout
        if now > token_valid_date - datetime.timedelta(seconds=10):
            (self.token, self.timeout) = authenticate(
                self.device_url, self.user, self.password
            )
            self.last_used = now
        return now

    def post_new_password(self, new_password):
        """
        a wrapper around `washpy.post_new_password`.

        Changes the password and refreshes authentication.
        """
        post_new_password(self.device_url, self.user, self.password, new_password)
        self.password = new_password
        self.refresh_authentication()

    # ~~~ State section ~~~

    def get_state(self) -> State:
        """
        queries the `/State` endpoint.

        **returns**: a complete state of the machine

        **raises**: ValueError, if the GET request was unsuccessfull
        """
        return State(**self._do_get_request("/State"))

    # ~~~ profUser section ~~~

    def get_all_roles(self) -> List[int]:
        """
        queries the `/profUser/roles` endpoint.

        **returns**: a list of all Role IDs.

        **raises**: ValueError, if the GET request was unsuccessfull
        """
        return [int(id) for id in self._do_get_request("/profUser/roles").keys()]

    def get_role(self, role_id: int) -> Role:
        """
        queries the `/profUser/roles/{role_id}` endpoint.

        **returns**: the `Role` corresponding to the `role_id`

        **raises**: ValueError, if the GET request was unsuccessfull
        """
        return Role(**self._do_get_request(f"/profUser/roles/{role_id}"))

    def post_new_role(self, role: Role) -> None:
        """
        POSTs a new `Role` to the `/profUser/roles` endpoint.

        **raises**: ValueError, if the POST request was unsuccessfull
        """
        self._do_post_request("/profUser/roles", role.model_dump_json())

    def put_modify_role(self, role: Role) -> None:
        """
        PUTs a modified `Role` to the `/profUser/roles/{role.ID}` endpoint.

        **raises**: ValueError, if the PUT request was unsuccessfull
        """
        # per documentation, the role.ID field should not be sent
        # in the PUT payload string.
        # But in practice, it just gets ignored
        self._do_put_request(f"/profUser/roles/{role.ID}", role.model_dump_json())

    def delete_role(self, role: Role | int) -> None:
        """
        DELETEs a `Role` from the `/profUser/roles/{role.ID}` endpoint.
        If an `int` is passed to `role`, it is treated as `role.ID`.

        **raises**: ValueError, if the PUT request was unsuccessfull
        """
        role_id: int
        if isinstance(role, Role):
            role_id = role.ID
        else:
            role_id = role

        self._do_delete_request(f"/profUser/roles/{role_id}")

    def get_all_users(self) -> List[int]:
        """
        queries the `/profUser/users` endpoint.

        **returns**: a list of all User IDs.

        **raises**: ValueError, if the GET request was unsuccessfull
        """
        return [int(id) for id in self._do_get_request("/profUser/users").keys()]

    def get_user(self, user_id: int) -> User:
        """
        queries the `/profUser/users/{user_id}` endpoint.

        **returns**: the `User` corresponding to the `user_id`

        **raises**: ValueError, if the GET request was unsuccessfull
        """
        return User(**self._do_get_request(f"/profUser/users/{user_id}"))

    def post_new_user(self, user: User) -> None:
        """
        POSTs a new `User` to the `/profUser/users` endpoint.

        **raises**: ValueError, if the POST request was unsuccessfull
        """
        self._do_post_request("/profUser/users", user.model_dump_json())

    def put_modify_user(self, user: User) -> None:
        """
        PUTs a modified `User` to the `/profUser/users/{user.ID}` endpoint.

        **raises**: ValueError, if the PUT request was unsuccessfull
        """
        self._do_put_request(f"/profUser/users/{user.ID}", user.model_dump_json())

    def delete_user(self, user: User | int) -> None:
        """
        DELETEs a `User` from the `/profUser/users/{user.ID}` endpoint.
        If an `int` is passed to `user`, it is treated as `user.ID`.

        **raises**: ValueError, if the PUT request was unsuccessfull
        """
        user_id: int
        if isinstance(user, User):
            user_id = user.ID
        else:
            user_id = user

        self._do_delete_request(f"/profUser/users/{user_id}")
