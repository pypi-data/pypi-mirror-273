"""
washpy implements parts of the Miele Professional IP Profile API.

Start by setting up the admin user, see `washpy.post_new_password`.

Then, create a `washpy.device_user.DeviceUser`, representing an user on a device.
Most of the functionality is derived from that class.
"""

import requests

# disables warnings from the unverified HTTPS requests
requests.packages.urllib3.disable_warnings()

from washpy.device_user import DeviceUser
from washpy.authenticate import authenticate
from washpy.post_new_password import post_new_password


if __name__ == "__main__":
    print("Hello World!")
