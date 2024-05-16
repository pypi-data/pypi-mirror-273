from typing import Tuple
import datetime
import json
import requests


class WrongCredentialsException(Exception):
    """
    Indicates, that a wrong user name or password has been given.
    """


class NoUserException(Exception):
    """
    Indicates, that no user exists on a given device.
    """


class LoginTimeoutException(Exception):
    """
    Indicates, that the login currently is in timeout state,
    and the user has to wait until any further login attempt.
    """


def authenticate(
    device_url: str, user: str, password: str
) -> Tuple[str, datetime.timedelta]:
    """
    `device_url`: e.g. `'https://192.168.1.251/Devices/000116343328'`

    `user`: e.g. `'MYUSER'`

    `password`: e.g. `'verySecurePassword!'`

    **returns**: a string, containing a bearer token, and a time duration for which the token is valid.
    If the token is used again within the valid time period, the valid time period is refreshed.

    **raises**:
      - `NoUserException`, if HTTP response code 401
      - `WrongCredentialsException`, if HTTP response code 403
      - `LoginTimeoutException`, if HTTP response code 429
      - `ValueError`, else, and not HTTP code 200
    """
    url = device_url + "/profSession"

    payload = json.dumps({"LoginName": user, "Password": password})
    headers = {"Content-Type": "application/json"}

    response = requests.request(
        "POST", url, verify=False, headers=headers, data=payload
    )

    match response.status_code:
        case 200:
            # the happy case
            return (
                response.json()["SessionId"],
                datetime.timedelta(seconds=response.json()["Timeout"]),
            )
        case 401:
            raise NoUserException("No user has been created on this device")
        case 403:
            raise WrongCredentialsException(
                f"For the user {user}, the password {password} is wrong."
            )
        case 429:
            raise LoginTimeoutException(
                f"Too many bad login attempts have been made. Please wait."
            )
        case _:
            raise ValueError(f"Unable to authenticate: got HTTP response {response}")
