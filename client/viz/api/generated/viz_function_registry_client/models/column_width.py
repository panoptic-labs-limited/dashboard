from enum import Enum


class ColumnWidth(str, Enum):
    VALUE_0 = "1/1"
    VALUE_1 = "1/2"
    VALUE_2 = "1/3"
    VALUE_3 = "2/3"
    VALUE_4 = "1/4"
    VALUE_5 = "3/4"
    VALUE_6 = "1/6"
    VALUE_7 = "5/6"

    def __str__(self) -> str:
        return str(self.value)
