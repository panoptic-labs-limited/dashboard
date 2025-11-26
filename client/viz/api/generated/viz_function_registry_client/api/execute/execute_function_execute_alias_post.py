from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.execution_request import ExecutionRequest
from ...models.execution_response import ExecutionResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    alias: str,
    *,
    body: ExecutionRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/execute/{alias}",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ExecutionResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = ExecutionResponse.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ExecutionResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    alias: str,
    *,
    client: AuthenticatedClient,
    body: ExecutionRequest,
) -> Response[ExecutionResponse | HTTPValidationError]:
    """Execute Function

     Execute a function by alias.

    Args:
        alias (str):
        body (ExecutionRequest): Request to execute a function.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExecutionResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        alias=alias,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    alias: str,
    *,
    client: AuthenticatedClient,
    body: ExecutionRequest,
) -> ExecutionResponse | HTTPValidationError | None:
    """Execute Function

     Execute a function by alias.

    Args:
        alias (str):
        body (ExecutionRequest): Request to execute a function.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExecutionResponse | HTTPValidationError
    """

    return sync_detailed(
        alias=alias,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    alias: str,
    *,
    client: AuthenticatedClient,
    body: ExecutionRequest,
) -> Response[ExecutionResponse | HTTPValidationError]:
    """Execute Function

     Execute a function by alias.

    Args:
        alias (str):
        body (ExecutionRequest): Request to execute a function.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExecutionResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        alias=alias,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    alias: str,
    *,
    client: AuthenticatedClient,
    body: ExecutionRequest,
) -> ExecutionResponse | HTTPValidationError | None:
    """Execute Function

     Execute a function by alias.

    Args:
        alias (str):
        body (ExecutionRequest): Request to execute a function.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExecutionResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            alias=alias,
            client=client,
            body=body,
        )
    ).parsed
