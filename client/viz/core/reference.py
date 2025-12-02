"""Named reference base class."""

from __future__ import annotations

from pydantic import BaseModel, Field


class NamedReference(BaseModel):
    """
    Reference to a named entity.

    Used in params to create bindings between widgets/inputs and input values.
    Input extends this class, so any Input can be used where NamedReference is expected.

    When serialized in params, becomes: {"ref": "<name>"}
    """
    name: str = Field(..., description="Reference name")
