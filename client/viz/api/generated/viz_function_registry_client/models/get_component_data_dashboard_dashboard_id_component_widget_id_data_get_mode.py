from enum import Enum


class GetComponentDataDashboardDashboardIdComponentWidgetIdDataGetMode(str, Enum):
    RAW = "raw"
    TRANSFORMED = "transformed"

    def __str__(self) -> str:
        return str(self.value)
