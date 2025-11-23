"""Data sources for inputs.

Sources define where input configuration comes from.
Currently supports function-based sources for dynamic configuration.
"""

from typing import Generic, TypeVar, Callable, Any, Literal

from pydantic import BaseModel, Field

T = TypeVar('T')


class FunctionSource(BaseModel, Generic[T]):
    """
    Function-based data source for dynamic input configuration.

    The function is executed server-side and can depend on other inputs
    via the params mapping.

    Examples:
        # Simple function
        FunctionSource(func=get_regions)

        # With parameters from other inputs
        FunctionSource(
            func=get_regions_for_country,
            params={"country": "country"}  # Maps to "country" input
        )

        # With mixed static and dynamic params
        FunctionSource(
            func=get_cities,
            params={
                "country": "country",      # From input
                "min_population": 100000   # Static value
            }
        )
    """

    type: Literal["function"] = "function"
    func: Callable[..., T] = Field(..., description="Function returning config data")
    params: dict[str, Any] = Field(
        default_factory=dict,
        description="Parameters mapping (param_name -> input_name or static value)"
    )

    class Config:
        arbitrary_types_allowed = True  # Allow Callable type
