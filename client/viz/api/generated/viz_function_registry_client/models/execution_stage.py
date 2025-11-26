from enum import Enum


class ExecutionStage(str, Enum):
    LOAD = "load"
    LOAD_TRANSFORM = "load_transform"
    LOAD_TRANSFORM_RENDER = "load_transform_render"

    def __str__(self) -> str:
        return str(self.value)
