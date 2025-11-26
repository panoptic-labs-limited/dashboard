from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.component_response import ComponentResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    alias: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/components/{alias}",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ComponentResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = ComponentResponse.from_dict(response.json())

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
) -> Response[ComponentResponse | HTTPValidationError]:
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
) -> Response[ComponentResponse | HTTPValidationError]:
    """Get Component

     Get a component by alias.

    Args:
        alias (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ComponentResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        alias=alias,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    alias: str,
    *,
    client: AuthenticatedClient,
) -> ComponentResponse | HTTPValidationError | None:
    """Get Component

     Get a component by alias.

    Args:
        alias (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ComponentResponse | HTTPValidationError
    """

    return sync_detailed(
        alias=alias,
        client=client,
    ).parsed


async def asyncio_detailed(
    alias: str,
    *,
    client: AuthenticatedClient,
) -> Response[ComponentResponse | HTTPValidationError]:
    """Get Component

     Get a component by alias.

    Args:
        alias (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ComponentResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        alias=alias,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    alias: str,
    *,
    client: AuthenticatedClient,
) -> ComponentResponse | HTTPValidationError | None:
    """Get Component

     Get a component by alias.

    Args:
        alias (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ComponentResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            alias=alias,
            client=client,
        )
    ).parsed
