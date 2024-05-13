# Code generated by smithy-python-codegen DO NOT EDIT.

from smithy_core.aio.utils import async_list
from smithy_http import tuples_to_fields
from smithy_http.aio import HTTPResponse as _HTTPResponse
from smithy_http.aio.interfaces import HTTPRequest, HTTPResponse
from smithy_http.interfaces import HTTPClientConfiguration, HTTPRequestConfiguration

from borneo_python_client.errors import ServiceError


class TestHttpServiceError(ServiceError):
    """A test error that subclasses the service-error for protocol tests."""

    def __init__(self, request: HTTPRequest):
        self.request = request


class RequestTestHTTPClient:
    """An asynchronous HTTP client solely for testing purposes."""

    def __init__(self, *, client_config: HTTPClientConfiguration | None = None):
        self._client_config = client_config

    async def send(
        self,
        *,
        request: HTTPRequest,
        request_config: HTTPRequestConfiguration | None = None,
    ) -> HTTPResponse:
        # Raise the exception with the request object to bypass actual request handling
        raise TestHttpServiceError(request)


class ResponseTestHTTPClient:
    """An asynchronous HTTP client solely for testing purposes."""

    def __init__(
        self,
        *,
        client_config: HTTPClientConfiguration | None = None,
        status: int = 200,
        headers: list[tuple[str, str]] | None = None,
        body: bytes = b"",
    ):
        self._client_config = client_config
        self.status = status
        self.fields = tuples_to_fields(headers or [])
        self.body = body

    async def send(
        self,
        *,
        request: HTTPRequest,
        request_config: HTTPRequestConfiguration | None = None,
    ) -> _HTTPResponse:
        # Pre-construct the response from the request and return it
        return _HTTPResponse(
            status=self.status,
            fields=self.fields,
            body=async_list([self.body]),
        )
