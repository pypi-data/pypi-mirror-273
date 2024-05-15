"""Class to connect to the DFI server."""

import logging
from enum import Enum
from http import HTTPStatus
from json import dumps
from typing import Any

import requests
from requests.exceptions import HTTPError
from requests.models import Response

from dfi.errors import DFIResponseError

_logger = logging.getLogger(__name__)


# this class exists in python >=3.11 so we reimplement for 3.10 support
class HTTPMethod(str, Enum):
    """Defines a set of HTTP methods and descriptions."""

    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    CONNECT = "CONNECT"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"
    PATCH = "PATCH"


class Connect:
    """Class instantiating the connectors to the DFI API.

    Parameters
    ----------
    api_token: token provided by generalsystem.com to access the running DFI environments.
    base_url: Base url where the service is located
    query_timeout: Time after an unresponsive query will be dropped.
    progress_bar: Visualise a progress bar if True (slows down the execution, typically used for demos and tests).

    Examples
    --------
    ```python
    connection = dfi.Connect("<token>", "<base_url>")
    ```
    """

    def __init__(
        self,
        api_token: str,
        base_url: str | None = None,
        query_timeout: int | None = 60,
        progress_bar: bool | None = False,
    ) -> None:
        self.api_token = api_token
        self.base_url = base_url
        self.query_timeout = query_timeout

        # TODO: remove headers here and pass them into this class from Client
        self.streaming_headers = {
            "Authorization": f"Bearer {api_token}",
            "Accept": "text/event-stream",
        }
        self.synchronous_headers = {
            "Authorization": f"Bearer {api_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self.progress_bar = progress_bar

    def __repr__(self) -> str:
        """Class representation."""
        return f"{self.__class__.__name__}(api_token=<***>, base_url={self.base_url}, query_timeout={self.query_timeout}, progress_bar={self.progress_bar})"

    def __str__(self) -> str:
        """Class string formatting."""
        return f"{self.__class__.__name__}(api_token=<***>, base_url={self.base_url}, query_timeout={self.query_timeout}, progress_bar={self.progress_bar})"

    def api_get(
        self,
        endpoint: str,
        stream: bool = True,
        params: dict | None = None,  # type: ignore
    ) -> requests.models.Response:
        """Wrap requests.get method.

        Parameters
        ----------
        endpoint:
            The endpoint of the URL.  Will be added as a suffix to the base_url.
        stream:
            Whether to use streaming headers or synchronous headers.
        params:
            Dictionary, list of tuples or bytes to send in the query string for the request.
        """
        headers = self.streaming_headers if stream else self.synchronous_headers
        url = f"{self.base_url}/{endpoint}"

        response = requests.get(
            url,
            headers=headers,
            stream=stream,
            params=params,
            timeout=self.query_timeout,
        )

        try:
            response.raise_for_status()
        except HTTPError as exc:
            msg = format_response_log(response, HTTPMethod.GET, url, headers, params)

            _logger.error(f"DFIResponseError: {dumps(msg, indent=4)}")
            raise DFIResponseError(msg) from exc

        return response

    def api_post(
        self,
        endpoint: str,
        stream: bool = True,
        params: dict | None = None,  # type: ignore
        json: dict | list | None = None,  # type: ignore
        data: dict | None = None,  # type: ignore
    ) -> requests.models.Response:
        """Wrap requests.post method.

        Parameters
        ----------
        endpoint:
            The endpoint of the URL.  Will be added as a suffix to the base_url.
        stream:
            Whether to use streaming headers or synchronous headers.
        params:
            Dictionary, list of tuples or bytes to send in the query string for the request.
        data:
            Dictionary, list of tuples, bytes, or file-like object to send in the body of the request
        json:
            A JSON serializable Python object to send in the body of the request.  Will set the
            "Content-Type: application/json" in the header.
        """
        headers = self.streaming_headers if stream else self.synchronous_headers
        url = f"{self.base_url}/{endpoint}"

        response = requests.post(
            url,
            headers=headers,
            json=json,
            data=data,
            stream=stream,
            params=params,
            timeout=self.query_timeout,
        )

        try:
            response.raise_for_status()
        except HTTPError as exc:
            msg = format_response_log(response, HTTPMethod.POST, url, headers, params, json)

            _logger.error(f"DFIResponseError: {dumps(msg, indent=4)}")
            raise DFIResponseError(msg) from exc

        return response

    def api_put(
        self,
        endpoint: str,
        stream: bool = True,
        params: dict | None = None,  # type: ignore
        json: dict | None = None,  # type: ignore
        data: dict | None = None,  # type: ignore
    ) -> requests.models.Response:
        """Wrap requests.put method.

        Parameters
        ----------
        endpoint:
            The endpoint of the URL.  Will be added as a suffix to the base_url.
        stream:
            Whether to use streaming headers or synchronous headers.
        params:
            Dictionary, list of tuples or bytes to send in the query string for the request.
        data:
            Dictionary, list of tuples, bytes, or file-like object to send in the body of the request
        json:
            A JSON serializable Python object to send in the body of the request.  Will set the
            "Content-Type: application/json" in the header.
        """
        headers = self.streaming_headers if stream else self.synchronous_headers
        url = f"{self.base_url}/{endpoint}"

        response = requests.put(
            url,
            headers=headers,
            json=json,
            data=data,
            stream=stream,
            params=params,
            timeout=self.query_timeout,
        )

        try:
            response.raise_for_status()
        except HTTPError as exc:
            msg = format_response_log(response, HTTPMethod.PUT, url, headers, params, json)

            _logger.error(f"DFIResponseError: {dumps(msg, indent=4)}")
            raise DFIResponseError(msg) from exc

        return response

    def api_delete(
        self,
        endpoint: str,
        stream: bool = True,
        params: dict | None = None,  # type: ignore
        json: dict | list | None = None,  # type: ignore
        data: dict | None = None,  # type: ignore
    ) -> requests.models.Response:
        """Wrap requests.delete method.

        Parameters
        ----------
        endpoint:
            The endpoint of the URL.  Will be added as a suffix to the base_url.
        stream:
            Whether to use streaming headers or synchronous headers.
        params:
            Dictionary, list of tuples or bytes to send in the query string for the request.
        data:
            Dictionary, list of tuples, bytes, or file-like object to send in the body of the request
        json:
            A JSON serializable Python object to send in the body of the request.  Will set the
            "Content-Type: application/json" in the header.
        """
        headers = self.streaming_headers if stream else self.synchronous_headers

        url = f"{self.base_url}/{endpoint}"
        response = requests.delete(
            url,
            headers=headers,
            json=json,
            data=data,
            stream=stream,
            params=params,
            timeout=self.query_timeout,
        )

        try:
            response.raise_for_status()
        except HTTPError as exc:
            msg = format_response_log(response, HTTPMethod.DELETE, url, headers, params, json)

            _logger.error(f"DFIResponseError: {dumps(msg, indent=4)}")
            raise DFIResponseError(msg) from exc

        return response

    def api_patch(
        self,
        endpoint: str,
        stream: bool = True,
        params: dict | None = None,  # type: ignore
        json: dict | None = None,  # type: ignore
        data: dict | None = None,  # type: ignore
    ) -> requests.models.Response:
        """Wrap requests.patch method.

        Parameters
        ----------
        endpoint:
            The endpoint of the URL.  Will be added as a suffix to the base_url.
        stream:
            Whether to use streaming headers or synchronous headers.
        params:
            Dictionary, list of tuples or bytes to send in the query string for the request.
        data:
            Dictionary, list of tuples, bytes, or file-like object to send in the body of the request
        json:
            A JSON serializable Python object to send in the body of the request.  Will set the
            "Content-Type: application/json" in the header.
        """
        headers = self.streaming_headers if stream else self.synchronous_headers
        url = f"{self.base_url}/{endpoint}"

        response = requests.patch(
            url,
            headers=headers,
            json=json,
            data=data,
            stream=stream,
            params=params,
            timeout=self.query_timeout,
        )

        try:
            response.raise_for_status()
        except HTTPError as exc:
            msg = format_response_log(response, HTTPMethod.PATCH, url, headers, params, json)

            _logger.error(f"DFIResponseError: {dumps(msg, indent=4)}")
            raise DFIResponseError(msg) from exc

        return response


def format_response_log(
    response: Response,
    method: HTTPMethod,
    url: str,
    headers: dict,
    params: dict | None = None,
    payload: dict | list | None = None,
) -> dict[str, Any]:
    """Human-friendly formatting for a response.

    Parameters
    ----------
    resp:
        a response object
    method:
        the HTTP method used (e.g. GET / POST / PUT / PATCH  / DELETE)
    url:
        the queried url
    headers:
        request headers
    params:
        request params
    payload:
        request payload

    Raises
    ------
    DFIResponseError
        If there was an error querying the DFI API.
    """
    msg = f"STATUS CODE: {response.status_code} - {HTTPStatus(response.status_code).name}"
    msg += f"ERROR: {response.text}"
    msg += f"METHOD: {method.name}"
    msg += f"URL: {url}"
    msg += f"PARAMS: {dumps(params, sort_keys=True, indent=4)}"

    # prevent from showing the user token to terminal and logs
    headers = headers.copy()
    headers["Authorization"] = "Bearer XXX"
    msg += f"HEADERS: {dumps(headers, sort_keys=True, indent=4)}"

    log = {
        "STATUS CODE": response.status_code,
        "STATUS NAME": HTTPStatus(response.status_code).name,
        "ERROR": response.text,
        "METHOD": method.name,
        "URL": url,
        "PARAMS": params,
        "HEADERS": headers,
        "PAYLOAD": payload,
    }

    msg += f"PAYLOAD: {dumps(payload, sort_keys=True, indent=4)}"

    return log
