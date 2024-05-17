import logging
import os
import typing
import requests

from typing import Dict
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception,
)

from syntrac.sdk.version import __version__

MAX_RETRIES = os.getenv("SYNTRAC_PROMPT_MANAGER_MAX_RETRIES") or 3
POLLING_INTERVAL = os.getenv("SYNTRAC_PROMPT_MANAGER_POLLING_INTERVAL") or 5


class Fetcher:
    def __init__(self, base_url: str, api_key: str):
        self._base_url = base_url
        self._api_key = api_key

    def post(self, api: str, body: Dict[str, str]):
        post_url(f"{self._base_url}/v1/syntrac/{api}", self._api_key, body)

    def patch(self, api: str, body: Dict[str, str]):
        patch_url(f"{self._base_url}/v1/syntrac/{api}", self._api_key, body)


class RetryIfServerError(retry_if_exception):
    def __init__(
        self,
        exception_types: typing.Union[
            typing.Type[BaseException],
            typing.Tuple[typing.Type[BaseException], ...],
        ] = Exception,
    ) -> None:
        self.exception_types = exception_types
        super().__init__(lambda e: check_http_error(e))


def check_http_error(e):
    return isinstance(e, requests.exceptions.HTTPError) and (
        500 <= e.response.status_code < 600
    )


@retry(
    wait=wait_exponential(multiplier=1, min=4),
    stop=stop_after_attempt(MAX_RETRIES),
    retry=RetryIfServerError(),
)
def fetch_url(url: str, api_key: str):
    response = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "X-Syntrac-SDK-Version": __version__,
        },
    )

    if response.status_code != 200:
        if response.status_code == 401 or response.status_code == 403:
            logging.error("Authorization error: Invalid API key.")
        raise requests.exceptions.HTTPError(response=response)
    else:
        return response.json()


def post_url(url: str, api_key: str, body: Dict[str, str]):
    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "X-Syntrac-SDK-Version": __version__,
        },
        json=body,
    )

    if response.status_code != 200 or response.status_code != 201:
        raise requests.exceptions.HTTPError(response=response)


def patch_url(url: str, api_key: str, body: Dict[str, str]):
    response = requests.patch(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "X-Syntrac-SDK-Version": __version__,
        },
        json=body,
    )

    if response.status_code != 200:
        raise requests.exceptions.HTTPError(response=response)
