from enum import Enum


class Direction(Enum):
    FORWARD = 1
    BACK = 2
    REPLACE = 3
    def to_graphical(self) -> str:
        if self is Direction.BACK:
            return "right"
        else:
            return "left"
