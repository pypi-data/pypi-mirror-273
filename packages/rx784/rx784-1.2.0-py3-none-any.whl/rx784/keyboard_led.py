from enum import IntEnum

class KeyboardLED(IntEnum):
    NUM_LOCK    = 0b00000001
    CAPS_LOCK   = 0b00000010
    SCROLL_LOCK = 0b00000100
    COMPOSE     = 0b00001000
    KANA        = 0b00010000
