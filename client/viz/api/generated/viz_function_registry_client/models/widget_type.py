from enum import Enum


class WidgetType(str, Enum):
    CHART = "chart"
    CUSTOM = "custom"
    IMAGE = "image"
    METRIC = "metric"
    TABLE = "table"
    TEXT = "text"

    def __str__(self) -> str:
        return str(self.value)
