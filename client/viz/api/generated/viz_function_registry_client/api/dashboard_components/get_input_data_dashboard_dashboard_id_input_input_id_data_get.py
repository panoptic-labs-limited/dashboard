from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    dashboard_id: str,
    input_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/dashboard/{dashboard_id}/input/{input_id}/data",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = response.json()
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
) -> Response[Any | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    dashboard_id: str,
    input_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Any | HTTPValidationError]:
    """Get Input Data

     Get data for an input (e.g., dropdown options from a data source function).

    Returns the options/data to populate the input in the UI.

    Args:
        dashboard_id (str):
        input_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        dashboard_id=dashboard_id,
        input_id=input_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    dashboard_id: str,
    input_id: str,
    *,
    client: AuthenticatedClient,
) -> Any | HTTPValidationError | None:
    """Get Input Data

     Get data for an input (e.g., dropdown options from a data source function).

    Returns the options/data to populate the input in the UI.

    Args:
        dashboard_id (str):
        input_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        dashboard_id=dashboard_id,
        input_id=input_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    dashboard_id: str,
    input_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Any | HTTPValidationError]:
    """Get Input Data

     Get data for an input (e.g., dropdown options from a data source function).

    Returns the options/data to populate the input in the UI.

    Args:
        dashboard_id (str):
        input_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        dashboard_id=dashboard_id,
        input_id=input_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dashboard_id: str,
    input_id: str,
    *,
    client: AuthenticatedClient,
) -> Any | HTTPValidationError | None:
    """Get Input Data

     Get data for an input (e.g., dropdown options from a data source function).

    Returns the options/data to populate the input in the UI.

    Args:
        dashboard_id (str):
        input_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            dashboard_id=dashboard_id,
            input_id=input_id,
            client=client,
        )
    ).parsed
