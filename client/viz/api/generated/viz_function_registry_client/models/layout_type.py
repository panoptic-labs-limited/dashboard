from enum import Enum


class LayoutType(str, Enum):
    COLUMN = "column"
    DASHBOARD = "dashboard"
    INPUT = "input"
    PAGE = "page"
    ROW = "row"
    SECTION = "section"
    TAB = "tab"
    TABS = "tabs"
    WIDGET = "widget"

    def __str__(self) -> str:
        return str(self.value)
