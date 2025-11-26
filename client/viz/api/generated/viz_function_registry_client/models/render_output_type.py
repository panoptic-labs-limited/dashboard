from enum import Enum


class RenderOutputType(str, Enum):
    ALTAIR = "altair"
    CUSTOM = "custom"
    PLOTLY = "plotly"
    VEGA_LITE = "vega_lite"

    def __str__(self) -> str:
        return str(self.value)
