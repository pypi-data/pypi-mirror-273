from enum import IntEnum

class Button(IntEnum):
    LEFT    = 0
    RIGHT   = 1
    MIDDLE  = 2
    BUTTON4 = 3
    BUTTON5 = 4

    def to_bytes(self) -> bytes:
        return super().to_bytes(1, 'little')
