from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.component_response import ComponentResponse
from ...models.component_update import ComponentUpdate
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
        alias: str,
        *,
        body: ComponentUpdate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/components/{alias}",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
        body: ComponentUpdate,
) -> Response[ComponentResponse | HTTPValidationError]:
    """Update Component

     Update a component.

    Args:
        alias (str):
        body (ComponentUpdate): Schema for updating a component.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ComponentResponse | HTTPValidationError]
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
        body: ComponentUpdate,
) -> ComponentResponse | HTTPValidationError | None:
    """Update Component

     Update a component.

    Args:
        alias (str):
        body (ComponentUpdate): Schema for updating a component.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ComponentResponse | HTTPValidationError
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
        body: ComponentUpdate,
) -> Response[ComponentResponse | HTTPValidationError]:
    """Update Component

     Update a component.

    Args:
        alias (str):
        body (ComponentUpdate): Schema for updating a component.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ComponentResponse | HTTPValidationError]
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
        body: ComponentUpdate,
) -> ComponentResponse | HTTPValidationError | None:
    """Update Component

     Update a component.

    Args:
        alias (str):
        body (ComponentUpdate): Schema for updating a component.

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
            body=body,
        )
    ).parsed
