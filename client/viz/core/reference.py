"""Referenceable base class for entities that can be referenced in params."""

from __future__ import annotations

from pydantic import BaseModel


class Referenceable(BaseModel):
    """
    Marker base class for entities that can be referenced in params.

    Used in params to create bindings between widgets/inputs and input values.
    BaseInput extends this class, so any Input can be used in params and will
    serialize to {"ref": "<id>"}.

    The actual `id` field is inherited from LayoutNode. This class exists
    to provide a type marker for the params serializer.
    """
    pass
