"""
Module to handle HTTP requests to API
"""

import httpx
from skylock_cli.config import API_URL
from skylock_cli.model.user import User


def send_register_request(user: User) -> httpx.Response:
    """
    Send a register request to the SkyLock backend API
    """
    url = f"{API_URL}/v1/auth/register"
    data = user.to_json()
    headers = {"Content-Type": "application/json"}
    return httpx.post(url=url, data=data, headers=headers).raise_for_status()
