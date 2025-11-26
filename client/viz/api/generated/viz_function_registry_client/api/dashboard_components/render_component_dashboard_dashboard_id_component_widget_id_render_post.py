from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.widget_render_request import WidgetRenderRequest
from ...types import Response


def _get_kwargs(
    dashboard_id: str,
    widget_id: str,
    *,
    body: WidgetRenderRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/dashboard/{dashboard_id}/component/{widget_id}/render",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
    widget_id: str,
    *,
    client: AuthenticatedClient,
    body: WidgetRenderRequest,
) -> Response[Any | HTTPValidationError]:
    """Render Component

     Render a component (full execution: load → transform → render).

    Args:
        dashboard_id: ID of the dashboard
        widget_id: ID of the widget to render
        request: Widget render request containing input values

    Returns the final rendered output (Plotly figure, Vega-Lite spec, etc.)

    Args:
        dashboard_id (str):
        widget_id (str):
        body (WidgetRenderRequest): Request to render a single widget.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        dashboard_id=dashboard_id,
        widget_id=widget_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    dashboard_id: str,
    widget_id: str,
    *,
    client: AuthenticatedClient,
    body: WidgetRenderRequest,
) -> Any | HTTPValidationError | None:
    """Render Component

     Render a component (full execution: load → transform → render).

    Args:
        dashboard_id: ID of the dashboard
        widget_id: ID of the widget to render
        request: Widget render request containing input values

    Returns the final rendered output (Plotly figure, Vega-Lite spec, etc.)

    Args:
        dashboard_id (str):
        widget_id (str):
        body (WidgetRenderRequest): Request to render a single widget.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        dashboard_id=dashboard_id,
        widget_id=widget_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    dashboard_id: str,
    widget_id: str,
    *,
    client: AuthenticatedClient,
    body: WidgetRenderRequest,
) -> Response[Any | HTTPValidationError]:
    """Render Component

     Render a component (full execution: load → transform → render).

    Args:
        dashboard_id: ID of the dashboard
        widget_id: ID of the widget to render
        request: Widget render request containing input values

    Returns the final rendered output (Plotly figure, Vega-Lite spec, etc.)

    Args:
        dashboard_id (str):
        widget_id (str):
        body (WidgetRenderRequest): Request to render a single widget.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        dashboard_id=dashboard_id,
        widget_id=widget_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dashboard_id: str,
    widget_id: str,
    *,
    client: AuthenticatedClient,
    body: WidgetRenderRequest,
) -> Any | HTTPValidationError | None:
    """Render Component

     Render a component (full execution: load → transform → render).

    Args:
        dashboard_id: ID of the dashboard
        widget_id: ID of the widget to render
        request: Widget render request containing input values

    Returns the final rendered output (Plotly figure, Vega-Lite spec, etc.)

    Args:
        dashboard_id (str):
        widget_id (str):
        body (WidgetRenderRequest): Request to render a single widget.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            dashboard_id=dashboard_id,
            widget_id=widget_id,
            client=client,
            body=body,
        )
    ).parsed
