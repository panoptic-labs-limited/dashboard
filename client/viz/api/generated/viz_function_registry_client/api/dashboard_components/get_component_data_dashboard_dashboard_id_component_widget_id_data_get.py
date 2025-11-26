from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_component_data_dashboard_dashboard_id_component_widget_id_data_get_mode import (
    GetComponentDataDashboardDashboardIdComponentWidgetIdDataGetMode,
)
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    dashboard_id: str,
    widget_id: str,
    *,
    mode: GetComponentDataDashboardDashboardIdComponentWidgetIdDataGetMode
    | Unset = GetComponentDataDashboardDashboardIdComponentWidgetIdDataGetMode.TRANSFORMED,
    params: None | str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_mode: str | Unset = UNSET
    if not isinstance(mode, Unset):
        json_mode = mode.value

    params["mode"] = json_mode

    json_params: None | str | Unset
    if isinstance(params, Unset):
        json_params = UNSET
    else:
        json_params = params
    params["params"] = json_params

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/dashboard/{dashboard_id}/component/{widget_id}/data",
        "params": params,
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
    widget_id: str,
    *,
    client: AuthenticatedClient,
    mode: GetComponentDataDashboardDashboardIdComponentWidgetIdDataGetMode
    | Unset = GetComponentDataDashboardDashboardIdComponentWidgetIdDataGetMode.TRANSFORMED,
    params: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    r"""Get Component Data

     Get component data without rendering.

    Args:
        mode: \"raw\" = load only, \"transformed\" = load + transform
        params: Optional JSON string of parameters

    Returns the data from load() or transform() stage.

    Args:
        dashboard_id (str):
        widget_id (str):
        mode (GetComponentDataDashboardDashboardIdComponentWidgetIdDataGetMode | Unset):  Default:
            GetComponentDataDashboardDashboardIdComponentWidgetIdDataGetMode.TRANSFORMED.
        params (None | str | Unset): JSON-encoded params

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        dashboard_id=dashboard_id,
        widget_id=widget_id,
        mode=mode,
        params=params,
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
    mode: GetComponentDataDashboardDashboardIdComponentWidgetIdDataGetMode
    | Unset = GetComponentDataDashboardDashboardIdComponentWidgetIdDataGetMode.TRANSFORMED,
    params: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    r"""Get Component Data

     Get component data without rendering.

    Args:
        mode: \"raw\" = load only, \"transformed\" = load + transform
        params: Optional JSON string of parameters

    Returns the data from load() or transform() stage.

    Args:
        dashboard_id (str):
        widget_id (str):
        mode (GetComponentDataDashboardDashboardIdComponentWidgetIdDataGetMode | Unset):  Default:
            GetComponentDataDashboardDashboardIdComponentWidgetIdDataGetMode.TRANSFORMED.
        params (None | str | Unset): JSON-encoded params

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
        mode=mode,
        params=params,
    ).parsed


async def asyncio_detailed(
    dashboard_id: str,
    widget_id: str,
    *,
    client: AuthenticatedClient,
    mode: GetComponentDataDashboardDashboardIdComponentWidgetIdDataGetMode
    | Unset = GetComponentDataDashboardDashboardIdComponentWidgetIdDataGetMode.TRANSFORMED,
    params: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    r"""Get Component Data

     Get component data without rendering.

    Args:
        mode: \"raw\" = load only, \"transformed\" = load + transform
        params: Optional JSON string of parameters

    Returns the data from load() or transform() stage.

    Args:
        dashboard_id (str):
        widget_id (str):
        mode (GetComponentDataDashboardDashboardIdComponentWidgetIdDataGetMode | Unset):  Default:
            GetComponentDataDashboardDashboardIdComponentWidgetIdDataGetMode.TRANSFORMED.
        params (None | str | Unset): JSON-encoded params

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        dashboard_id=dashboard_id,
        widget_id=widget_id,
        mode=mode,
        params=params,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dashboard_id: str,
    widget_id: str,
    *,
    client: AuthenticatedClient,
    mode: GetComponentDataDashboardDashboardIdComponentWidgetIdDataGetMode
    | Unset = GetComponentDataDashboardDashboardIdComponentWidgetIdDataGetMode.TRANSFORMED,
    params: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    r"""Get Component Data

     Get component data without rendering.

    Args:
        mode: \"raw\" = load only, \"transformed\" = load + transform
        params: Optional JSON string of parameters

    Returns the data from load() or transform() stage.

    Args:
        dashboard_id (str):
        widget_id (str):
        mode (GetComponentDataDashboardDashboardIdComponentWidgetIdDataGetMode | Unset):  Default:
            GetComponentDataDashboardDashboardIdComponentWidgetIdDataGetMode.TRANSFORMED.
        params (None | str | Unset): JSON-encoded params

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
            mode=mode,
            params=params,
        )
    ).parsed
