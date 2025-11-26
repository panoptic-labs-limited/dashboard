from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.component_execution_request import ComponentExecutionRequest
from ...models.component_execution_response import ComponentExecutionResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    alias: str,
    *,
    body: ComponentExecutionRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/execute/component/{alias}",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ComponentExecutionResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = ComponentExecutionResponse.from_dict(response.json())

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
) -> Response[ComponentExecutionResponse | HTTPValidationError]:
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
    body: ComponentExecutionRequest,
) -> Response[ComponentExecutionResponse | HTTPValidationError]:
    """Execute Component

     Execute a component by alias with specified stage.

    Args:
        alias (str):
        body (ComponentExecutionRequest): Request to execute a component.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ComponentExecutionResponse | HTTPValidationError]
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
    body: ComponentExecutionRequest,
) -> ComponentExecutionResponse | HTTPValidationError | None:
    """Execute Component

     Execute a component by alias with specified stage.

    Args:
        alias (str):
        body (ComponentExecutionRequest): Request to execute a component.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ComponentExecutionResponse | HTTPValidationError
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
    body: ComponentExecutionRequest,
) -> Response[ComponentExecutionResponse | HTTPValidationError]:
    """Execute Component

     Execute a component by alias with specified stage.

    Args:
        alias (str):
        body (ComponentExecutionRequest): Request to execute a component.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ComponentExecutionResponse | HTTPValidationError]
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
    body: ComponentExecutionRequest,
) -> ComponentExecutionResponse | HTTPValidationError | None:
    """Execute Component

     Execute a component by alias with specified stage.

    Args:
        alias (str):
        body (ComponentExecutionRequest): Request to execute a component.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ComponentExecutionResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            alias=alias,
            client=client,
            body=body,
        )
    ).parsed
