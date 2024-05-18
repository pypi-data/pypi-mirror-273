from dataclasses import dataclass, field
from typing import List
from .button import Button
from .key_code import VirtualKeyCode

@dataclass
class KeyboardState:
    @dataclass
    class ModeiferKeys:
        control_left:  bool
        shift_left:    bool
        alt_left:      bool
        os_left:       bool
        control_right: bool
        shift_right:   bool
        alt_right:     bool
        os_right:      bool

    modifier_keys: ModeiferKeys
    regular_keys:  List[VirtualKeyCode]

    def to_bytes(self) -> bytes:
        key0 = ((self.modifier_keys.control_left  << 0)
              | (self.modifier_keys.shift_left    << 1)
              | (self.modifier_keys.alt_left      << 2)
              | (self.modifier_keys.os_left       << 3)
              | (self.modifier_keys.control_right << 4)
              | (self.modifier_keys.shift_right   << 5)
              | (self.modifier_keys.alt_right     << 6)
              | (self.modifier_keys.os_right      << 7))
        return bytes([key0] + [virtual_key_code.to_hid_key_code() for virtual_key_code in self.regular_keys])


@dataclass
class KeyboardLEDsState:
    num_lock:    bool
    caps_lock:   bool
    scroll_lock: bool
    compose:     bool
    kana:        bool


@dataclass
class ButtonsState:
    left:    bool
    right:   bool
    middle:  bool
    button4: bool
    button5: bool


@dataclass
class MouseState:
    @dataclass
    class Buttons:
        left:   bool
        right:  bool
        middle: bool
        button4: bool
        button5: bool

    @dataclass
    class Axes:
        x: int
        y: int
        w: int

    buttons: Buttons
    axes:    Axes

    def to_bytes(self) -> bytes:
        return (((self.buttons.left   << Button.LEFT)
               | (self.buttons.right  << Button.RIGHT)
               | (self.buttons.right  << Button.MIDDLE)
               | (self.buttons.right  << Button.BUTTON4)
               | (self.buttons.middle << Button.BUTTON5)).to_bytes(1, 'little')
              + self.axes.x.to_bytes(2, 'little')
              + self.axes.y.to_bytes(2, 'little')
              + self.axes.w.to_bytes(2, 'little'))


@dataclass
class KeyboardStateMask:
    @dataclass
    class ModeiferKeys:
        control_left:  bool = False
        shift_left:    bool = False
        alt_left:      bool = False
        os_left:       bool = False
        control_right: bool = False
        shift_right:   bool = False
        alt_right:     bool = False
        os_right:      bool = False

    modifier_keys: ModeiferKeys = field(default_factory=ModeiferKeys)
    regular_keys:  List[bool]   = field(default_factory=lambda: [False] * 7)

    def to_bytes(self) -> bytes:
        mask0 = ((self.modifier_keys.control_left  << 0)
               | (self.modifier_keys.shift_left    << 1)
               | (self.modifier_keys.alt_left      << 2)
               | (self.modifier_keys.os_left       << 3)
               | (self.modifier_keys.control_right << 4)
               | (self.modifier_keys.shift_right   << 5)
               | (self.modifier_keys.alt_right     << 6)
               | (self.modifier_keys.os_right      << 7))

        mask1 = 0
        for i in range(7):
            mask1 |= self.regular_keys[i] << i

        return bytes([mask0, mask1])


@dataclass
class MouseStateMask:
    @dataclass
    class Buttons:
        left:   bool = False
        right:  bool = False
        middle: bool = False

    @dataclass
    class Axes:
        x: bool = False
        y: bool = False
        w: bool = False

    buttons: Buttons = field(default_factory=Buttons)
    axes:    Axes    = field(default_factory=Axes)

    def to_bytes(self) -> bytes:
        return ((self.buttons.left   << 0)
              | (self.buttons.right  << 1)
              | (self.buttons.middle << 2)
              | (self.axes.x         << 3)
              | (self.axes.y         << 4)
              | (self.axes.w         << 5)).to_bytes(1, 'little')
