from enum import IntEnum

class VirtualKeyCode(IntEnum):
    INVALID         = 0
    BACKSPACE       = 8
    TAB             = 9
    ENTER           = 13
    SHIFT           = 16
    CONTROL         = 17
    ALT             = 18
    PAUSE           = 19
    CAPS_LOCK       = 20
    ESCAPE          = 27
    SPACE           = 32
    PAGE_UP         = 33
    PAGE_DOWN       = 34
    END             = 35
    HOME            = 36
    ARROW_LEFT      = 37
    ARROW_UP        = 38
    ARROW_RIGHT     = 39
    ARROW_DOWN      = 40
    PRINT_SCREEN    = 44
    INSERT          = 45
    DELETE          = 46
    DIGIT0          = 48
    DIGIT1          = 49
    DIGIT2          = 50
    DIGIT3          = 51
    DIGIT4          = 52
    DIGIT5          = 53
    DIGIT6          = 54
    DIGIT7          = 55
    DIGIT8          = 56
    DIGIT9          = 57
    KEY_A           = 65
    KEY_B           = 66
    KEY_C           = 67
    KEY_D           = 68
    KEY_E           = 69
    KEY_F           = 70
    KEY_G           = 71
    KEY_H           = 72
    KEY_I           = 73
    KEY_J           = 74
    KEY_K           = 75
    KEY_L           = 76
    KEY_M           = 77
    KEY_N           = 78
    KEY_O           = 79
    KEY_P           = 80
    KEY_Q           = 81
    KEY_R           = 82
    KEY_S           = 83
    KEY_T           = 84
    KEY_U           = 85
    KEY_V           = 86
    KEY_W           = 87
    KEY_X           = 88
    KEY_Y           = 89
    KEY_Z           = 90
    OS_LEFT         = 91
    OS_RIGHT        = 92
    CONTEXT_MENU    = 93
    NUMPAD0         = 96
    NUMPAD1         = 97
    NUMPAD2         = 98
    NUMPAD3         = 99
    NUMPAD4         = 100
    NUMPAD5         = 101
    NUMPAD6         = 102
    NUMPAD7         = 103
    NUMPAD8         = 104
    NUMPAD9         = 105
    NUMPAD_MULTIPLY = 106
    NUMPAD_ADD      = 107
    NUMPAD_ENTER    = 108
    NUMPAD_SUBTRACT = 109
    NUMPAD_DECIMAL  = 110
    NUMPAD_DIVIDE   = 111
    F1              = 112
    F2              = 113
    F3              = 114
    F4              = 115
    F5              = 116
    F6              = 117
    F7              = 118
    F8              = 119
    F9              = 120
    F10             = 121
    F11             = 122
    F12             = 123
    NUM_LOCK        = 144
    SCROLL_LOCK     = 145
    SHIFT_LEFT      = 160
    SHIFT_RIGHT     = 161
    CONTROL_LEFT    = 162
    CONTROL_RIGHT   = 163
    ALT_LEFT        = 164
    ALT_RIGHT       = 165
    SEMICOLON       = 186
    EQUAL           = 187
    COMMA           = 188
    MINUS           = 189
    PERIOD          = 190
    SLASH           = 191
    BACKQUOTE       = 192
    BRACKET_LEFT    = 219
    BACKSLASH       = 220
    BRACKET_RIGHT   = 221
    QUOTE           = 222

    def to_bytes(self) -> bytes:
        return super().to_bytes(1, 'little')

    def to_hid_key_code(self) -> "HIDKeyCode":
        if   self == VirtualKeyCode.BACKSPACE      : return HIDKeyCode.BACKSPACE
        elif self == VirtualKeyCode.TAB            : return HIDKeyCode.TAB
        elif self == VirtualKeyCode.ENTER          : return HIDKeyCode.ENTER
        elif self == VirtualKeyCode.SHIFT          : return HIDKeyCode.SHIFT_LEFT
        elif self == VirtualKeyCode.CONTROL        : return HIDKeyCode.CONTROL_LEFT
        elif self == VirtualKeyCode.ALT            : return HIDKeyCode.ALT_LEFT
        elif self == VirtualKeyCode.PAUSE          : return HIDKeyCode.PAUSE
        elif self == VirtualKeyCode.CAPS_LOCK      : return HIDKeyCode.CAPS_LOCK
        elif self == VirtualKeyCode.ESCAPE         : return HIDKeyCode.ESCAPE
        elif self == VirtualKeyCode.SPACE          : return HIDKeyCode.SPACE
        elif self == VirtualKeyCode.PAGE_UP        : return HIDKeyCode.PAGE_UP
        elif self == VirtualKeyCode.PAGE_DOWN      : return HIDKeyCode.PAGE_DOWN
        elif self == VirtualKeyCode.END            : return HIDKeyCode.END
        elif self == VirtualKeyCode.HOME           : return HIDKeyCode.HOME
        elif self == VirtualKeyCode.ARROW_LEFT     : return HIDKeyCode.ARROW_LEFT
        elif self == VirtualKeyCode.ARROW_UP       : return HIDKeyCode.ARROW_UP
        elif self == VirtualKeyCode.ARROW_RIGHT    : return HIDKeyCode.ARROW_RIGHT
        elif self == VirtualKeyCode.ARROW_DOWN     : return HIDKeyCode.ARROW_DOWN
        elif self == VirtualKeyCode.PRINT_SCREEN   : return HIDKeyCode.PRINT_SCREEN
        elif self == VirtualKeyCode.INSERT         : return HIDKeyCode.INSERT
        elif self == VirtualKeyCode.DELETE         : return HIDKeyCode.DELETE
        elif self == VirtualKeyCode.DIGIT0         : return HIDKeyCode.DIGIT0
        elif self == VirtualKeyCode.DIGIT1         : return HIDKeyCode.DIGIT1
        elif self == VirtualKeyCode.DIGIT2         : return HIDKeyCode.DIGIT2
        elif self == VirtualKeyCode.DIGIT3         : return HIDKeyCode.DIGIT3
        elif self == VirtualKeyCode.DIGIT4         : return HIDKeyCode.DIGIT4
        elif self == VirtualKeyCode.DIGIT5         : return HIDKeyCode.DIGIT5
        elif self == VirtualKeyCode.DIGIT6         : return HIDKeyCode.DIGIT6
        elif self == VirtualKeyCode.DIGIT7         : return HIDKeyCode.DIGIT7
        elif self == VirtualKeyCode.DIGIT8         : return HIDKeyCode.DIGIT8
        elif self == VirtualKeyCode.DIGIT9         : return HIDKeyCode.DIGIT9
        elif self == VirtualKeyCode.KEY_A          : return HIDKeyCode.KEY_A
        elif self == VirtualKeyCode.KEY_B          : return HIDKeyCode.KEY_B
        elif self == VirtualKeyCode.KEY_C          : return HIDKeyCode.KEY_C
        elif self == VirtualKeyCode.KEY_D          : return HIDKeyCode.KEY_D
        elif self == VirtualKeyCode.KEY_E          : return HIDKeyCode.KEY_E
        elif self == VirtualKeyCode.KEY_F          : return HIDKeyCode.KEY_F
        elif self == VirtualKeyCode.KEY_G          : return HIDKeyCode.KEY_G
        elif self == VirtualKeyCode.KEY_H          : return HIDKeyCode.KEY_H
        elif self == VirtualKeyCode.KEY_I          : return HIDKeyCode.KEY_I
        elif self == VirtualKeyCode.KEY_J          : return HIDKeyCode.KEY_J
        elif self == VirtualKeyCode.KEY_K          : return HIDKeyCode.KEY_K
        elif self == VirtualKeyCode.KEY_L          : return HIDKeyCode.KEY_L
        elif self == VirtualKeyCode.KEY_M          : return HIDKeyCode.KEY_M
        elif self == VirtualKeyCode.KEY_N          : return HIDKeyCode.KEY_N
        elif self == VirtualKeyCode.KEY_O          : return HIDKeyCode.KEY_O
        elif self == VirtualKeyCode.KEY_P          : return HIDKeyCode.KEY_P
        elif self == VirtualKeyCode.KEY_Q          : return HIDKeyCode.KEY_Q
        elif self == VirtualKeyCode.KEY_R          : return HIDKeyCode.KEY_R
        elif self == VirtualKeyCode.KEY_S          : return HIDKeyCode.KEY_S
        elif self == VirtualKeyCode.KEY_T          : return HIDKeyCode.KEY_T
        elif self == VirtualKeyCode.KEY_U          : return HIDKeyCode.KEY_U
        elif self == VirtualKeyCode.KEY_V          : return HIDKeyCode.KEY_V
        elif self == VirtualKeyCode.KEY_W          : return HIDKeyCode.KEY_W
        elif self == VirtualKeyCode.KEY_X          : return HIDKeyCode.KEY_X
        elif self == VirtualKeyCode.KEY_Y          : return HIDKeyCode.KEY_Y
        elif self == VirtualKeyCode.KEY_Z          : return HIDKeyCode.KEY_Z
        elif self == VirtualKeyCode.OS_LEFT        : return HIDKeyCode.OS_LEFT
        elif self == VirtualKeyCode.OS_RIGHT       : return HIDKeyCode.OS_RIGHT
        elif self == VirtualKeyCode.CONTEXT_MENU   : return HIDKeyCode.CONTEXT_MENU
        elif self == VirtualKeyCode.NUMPAD0        : return HIDKeyCode.NUMPAD0
        elif self == VirtualKeyCode.NUMPAD1        : return HIDKeyCode.NUMPAD1
        elif self == VirtualKeyCode.NUMPAD2        : return HIDKeyCode.NUMPAD2
        elif self == VirtualKeyCode.NUMPAD3        : return HIDKeyCode.NUMPAD3
        elif self == VirtualKeyCode.NUMPAD4        : return HIDKeyCode.NUMPAD4
        elif self == VirtualKeyCode.NUMPAD5        : return HIDKeyCode.NUMPAD5
        elif self == VirtualKeyCode.NUMPAD6        : return HIDKeyCode.NUMPAD6
        elif self == VirtualKeyCode.NUMPAD7        : return HIDKeyCode.NUMPAD7
        elif self == VirtualKeyCode.NUMPAD8        : return HIDKeyCode.NUMPAD8
        elif self == VirtualKeyCode.NUMPAD9        : return HIDKeyCode.NUMPAD9
        elif self == VirtualKeyCode.NUMPAD_MULTIPLY: return HIDKeyCode.NUMPAD_MULTIPLY
        elif self == VirtualKeyCode.NUMPAD_ADD     : return HIDKeyCode.NUMPAD_ADD
        elif self == VirtualKeyCode.NUMPAD_ENTER   : return HIDKeyCode.NUMPAD_ENTER
        elif self == VirtualKeyCode.NUMPAD_SUBTRACT: return HIDKeyCode.NUMPAD_SUBTRACT
        elif self == VirtualKeyCode.NUMPAD_DECIMAL : return HIDKeyCode.NUMPAD_DECIMAL
        elif self == VirtualKeyCode.NUMPAD_DIVIDE  : return HIDKeyCode.NUMPAD_DIVIDE
        elif self == VirtualKeyCode.F1             : return HIDKeyCode.F1
        elif self == VirtualKeyCode.F2             : return HIDKeyCode.F2
        elif self == VirtualKeyCode.F3             : return HIDKeyCode.F3
        elif self == VirtualKeyCode.F4             : return HIDKeyCode.F4
        elif self == VirtualKeyCode.F5             : return HIDKeyCode.F5
        elif self == VirtualKeyCode.F6             : return HIDKeyCode.F6
        elif self == VirtualKeyCode.F7             : return HIDKeyCode.F7
        elif self == VirtualKeyCode.F8             : return HIDKeyCode.F8
        elif self == VirtualKeyCode.F9             : return HIDKeyCode.F9
        elif self == VirtualKeyCode.F10            : return HIDKeyCode.F10
        elif self == VirtualKeyCode.F11            : return HIDKeyCode.F11
        elif self == VirtualKeyCode.F12            : return HIDKeyCode.F12
        elif self == VirtualKeyCode.NUM_LOCK       : return HIDKeyCode.NUM_LOCK
        elif self == VirtualKeyCode.SCROLL_LOCK    : return HIDKeyCode.SCROLL_LOCK
        elif self == VirtualKeyCode.SHIFT_LEFT     : return HIDKeyCode.SHIFT_LEFT
        elif self == VirtualKeyCode.SHIFT_RIGHT    : return HIDKeyCode.SHIFT_RIGHT
        elif self == VirtualKeyCode.CONTROL_LEFT   : return HIDKeyCode.CONTROL_LEFT
        elif self == VirtualKeyCode.CONTROL_RIGHT  : return HIDKeyCode.CONTROL_RIGHT
        elif self == VirtualKeyCode.ALT_LEFT       : return HIDKeyCode.ALT_LEFT
        elif self == VirtualKeyCode.ALT_RIGHT      : return HIDKeyCode.ALT_RIGHT
        elif self == VirtualKeyCode.SEMICOLON      : return HIDKeyCode.SEMICOLON
        elif self == VirtualKeyCode.EQUAL          : return HIDKeyCode.EQUAL
        elif self == VirtualKeyCode.COMMA          : return HIDKeyCode.COMMA
        elif self == VirtualKeyCode.MINUS          : return HIDKeyCode.MINUS
        elif self == VirtualKeyCode.PERIOD         : return HIDKeyCode.PERIOD
        elif self == VirtualKeyCode.SLASH          : return HIDKeyCode.SLASH
        elif self == VirtualKeyCode.BACKQUOTE      : return HIDKeyCode.BACKQUOTE
        elif self == VirtualKeyCode.BRACKET_LEFT   : return HIDKeyCode.BRACKET_LEFT
        elif self == VirtualKeyCode.BACKSLASH      : return HIDKeyCode.BACKSLASH
        elif self == VirtualKeyCode.BRACKET_RIGHT  : return HIDKeyCode.BRACKET_RIGHT
        elif self == VirtualKeyCode.QUOTE          : return HIDKeyCode.QUOTE
        else                                       : return HIDKeyCode.INVALID


class HIDKeyCode(IntEnum):
    INVALID         = 0
    KEY_A           = 4
    KEY_B           = 5
    KEY_C           = 6
    KEY_D           = 7
    KEY_E           = 8
    KEY_F           = 9
    KEY_G           = 10
    KEY_H           = 11
    KEY_I           = 12
    KEY_J           = 13
    KEY_K           = 14
    KEY_L           = 15
    KEY_M           = 16
    KEY_N           = 17
    KEY_O           = 18
    KEY_P           = 19
    KEY_Q           = 20
    KEY_R           = 21
    KEY_S           = 22
    KEY_T           = 23
    KEY_U           = 24
    KEY_V           = 25
    KEY_W           = 26
    KEY_X           = 27
    KEY_Y           = 28
    KEY_Z           = 29
    DIGIT1          = 30
    DIGIT2          = 31
    DIGIT3          = 32
    DIGIT4          = 33
    DIGIT5          = 34
    DIGIT6          = 35
    DIGIT7          = 36
    DIGIT8          = 37
    DIGIT9          = 38
    DIGIT0          = 39
    ENTER           = 40
    ESCAPE          = 41
    BACKSPACE       = 42
    TAB             = 43
    SPACE           = 44
    MINUS           = 45
    EQUAL           = 46
    BRACKET_LEFT    = 47
    BRACKET_RIGHT   = 48
    BACKSLASH       = 49
    NON_US_SHARP    = 50
    SEMICOLON       = 51
    QUOTE           = 52
    BACKQUOTE       = 53
    COMMA           = 54
    PERIOD          = 55
    SLASH           = 56
    CAPS_LOCK       = 57
    F1              = 58
    F2              = 59
    F3              = 60
    F4              = 61
    F5              = 62
    F6              = 63
    F7              = 64
    F8              = 65
    F9              = 66
    F10             = 67
    F11             = 68
    F12             = 69
    PRINT_SCREEN    = 70
    SCROLL_LOCK     = 71
    PAUSE           = 72
    INSERT          = 73
    HOME            = 74
    PAGE_UP         = 75
    DELETE          = 76
    END             = 77
    PAGE_DOWN       = 78
    ARROW_RIGHT     = 79
    ARROW_LEFT      = 80
    ARROW_DOWN      = 81
    ARROW_UP        = 82
    NUM_LOCK        = 83
    NUMPAD_DIVIDE   = 84
    NUMPAD_MULTIPLY = 85
    NUMPAD_SUBTRACT = 86
    NUMPAD_ADD      = 87
    NUMPAD_ENTER    = 88
    NUMPAD1         = 89
    NUMPAD2         = 90
    NUMPAD3         = 91
    NUMPAD4         = 92
    NUMPAD5         = 93
    NUMPAD6         = 94
    NUMPAD7         = 95
    NUMPAD8         = 96
    NUMPAD9         = 97
    NUMPAD0         = 98
    NUMPAD_DECIMAL  = 99
    NON_US_SLASH    = 100
    CONTEXT_MENU    = 101
    CONTROL_LEFT    = 224
    SHIFT_LEFT      = 225
    ALT_LEFT        = 226
    OS_LEFT         = 227
    CONTROL_RIGHT   = 228
    SHIFT_RIGHT     = 229
    ALT_RIGHT       = 230
    OS_RIGHT        = 231

    def to_bytes(self) -> bytes:
        return super().to_bytes(1, 'little')

    def to_virtual_key_code(self) -> "VirtualKeyCode":
        if   self == HIDKeyCode.KEY_A          : return VirtualKeyCode.KEY_A
        elif self == HIDKeyCode.KEY_B          : return VirtualKeyCode.KEY_B
        elif self == HIDKeyCode.KEY_C          : return VirtualKeyCode.KEY_C
        elif self == HIDKeyCode.KEY_D          : return VirtualKeyCode.KEY_D
        elif self == HIDKeyCode.KEY_E          : return VirtualKeyCode.KEY_E
        elif self == HIDKeyCode.KEY_F          : return VirtualKeyCode.KEY_F
        elif self == HIDKeyCode.KEY_G          : return VirtualKeyCode.KEY_G
        elif self == HIDKeyCode.KEY_H          : return VirtualKeyCode.KEY_H
        elif self == HIDKeyCode.KEY_I          : return VirtualKeyCode.KEY_I
        elif self == HIDKeyCode.KEY_J          : return VirtualKeyCode.KEY_J
        elif self == HIDKeyCode.KEY_K          : return VirtualKeyCode.KEY_K
        elif self == HIDKeyCode.KEY_L          : return VirtualKeyCode.KEY_L
        elif self == HIDKeyCode.KEY_M          : return VirtualKeyCode.KEY_M
        elif self == HIDKeyCode.KEY_N          : return VirtualKeyCode.KEY_N
        elif self == HIDKeyCode.KEY_O          : return VirtualKeyCode.KEY_O
        elif self == HIDKeyCode.KEY_P          : return VirtualKeyCode.KEY_P
        elif self == HIDKeyCode.KEY_Q          : return VirtualKeyCode.KEY_Q
        elif self == HIDKeyCode.KEY_R          : return VirtualKeyCode.KEY_R
        elif self == HIDKeyCode.KEY_S          : return VirtualKeyCode.KEY_S
        elif self == HIDKeyCode.KEY_T          : return VirtualKeyCode.KEY_T
        elif self == HIDKeyCode.KEY_U          : return VirtualKeyCode.KEY_U
        elif self == HIDKeyCode.KEY_V          : return VirtualKeyCode.KEY_V
        elif self == HIDKeyCode.KEY_W          : return VirtualKeyCode.KEY_W
        elif self == HIDKeyCode.KEY_X          : return VirtualKeyCode.KEY_X
        elif self == HIDKeyCode.KEY_Y          : return VirtualKeyCode.KEY_Y
        elif self == HIDKeyCode.KEY_Z          : return VirtualKeyCode.KEY_Z
        elif self == HIDKeyCode.DIGIT1         : return VirtualKeyCode.DIGIT1
        elif self == HIDKeyCode.DIGIT2         : return VirtualKeyCode.DIGIT2
        elif self == HIDKeyCode.DIGIT3         : return VirtualKeyCode.DIGIT3
        elif self == HIDKeyCode.DIGIT4         : return VirtualKeyCode.DIGIT4
        elif self == HIDKeyCode.DIGIT5         : return VirtualKeyCode.DIGIT5
        elif self == HIDKeyCode.DIGIT6         : return VirtualKeyCode.DIGIT6
        elif self == HIDKeyCode.DIGIT7         : return VirtualKeyCode.DIGIT7
        elif self == HIDKeyCode.DIGIT8         : return VirtualKeyCode.DIGIT8
        elif self == HIDKeyCode.DIGIT9         : return VirtualKeyCode.DIGIT9
        elif self == HIDKeyCode.DIGIT0         : return VirtualKeyCode.DIGIT0
        elif self == HIDKeyCode.ENTER          : return VirtualKeyCode.ENTER
        elif self == HIDKeyCode.ESCAPE         : return VirtualKeyCode.ESCAPE
        elif self == HIDKeyCode.BACKSPACE      : return VirtualKeyCode.BACKSPACE
        elif self == HIDKeyCode.TAB            : return VirtualKeyCode.TAB
        elif self == HIDKeyCode.SPACE          : return VirtualKeyCode.SPACE
        elif self == HIDKeyCode.MINUS          : return VirtualKeyCode.MINUS
        elif self == HIDKeyCode.EQUAL          : return VirtualKeyCode.EQUAL
        elif self == HIDKeyCode.BRACKET_LEFT   : return VirtualKeyCode.BRACKET_LEFT
        elif self == HIDKeyCode.BRACKET_RIGHT  : return VirtualKeyCode.BRACKET_RIGHT
        elif self == HIDKeyCode.BACKSLASH      : return VirtualKeyCode.BACKSLASH
        elif self == HIDKeyCode.SEMICOLON      : return VirtualKeyCode.SEMICOLON
        elif self == HIDKeyCode.QUOTE          : return VirtualKeyCode.QUOTE
        elif self == HIDKeyCode.BACKQUOTE      : return VirtualKeyCode.BACKQUOTE
        elif self == HIDKeyCode.COMMA          : return VirtualKeyCode.COMMA
        elif self == HIDKeyCode.PERIOD         : return VirtualKeyCode.PERIOD
        elif self == HIDKeyCode.SLASH          : return VirtualKeyCode.SLASH
        elif self == HIDKeyCode.CAPS_LOCK      : return VirtualKeyCode.CAPS_LOCK
        elif self == HIDKeyCode.F1             : return VirtualKeyCode.F1
        elif self == HIDKeyCode.F2             : return VirtualKeyCode.F2
        elif self == HIDKeyCode.F3             : return VirtualKeyCode.F3
        elif self == HIDKeyCode.F4             : return VirtualKeyCode.F4
        elif self == HIDKeyCode.F5             : return VirtualKeyCode.F5
        elif self == HIDKeyCode.F6             : return VirtualKeyCode.F6
        elif self == HIDKeyCode.F7             : return VirtualKeyCode.F7
        elif self == HIDKeyCode.F8             : return VirtualKeyCode.F8
        elif self == HIDKeyCode.F9             : return VirtualKeyCode.F9
        elif self == HIDKeyCode.F10            : return VirtualKeyCode.F10
        elif self == HIDKeyCode.F11            : return VirtualKeyCode.F11
        elif self == HIDKeyCode.F12            : return VirtualKeyCode.F12
        elif self == HIDKeyCode.PRINT_SCREEN   : return VirtualKeyCode.PRINT_SCREEN
        elif self == HIDKeyCode.SCROLL_LOCK    : return VirtualKeyCode.SCROLL_LOCK
        elif self == HIDKeyCode.PAUSE          : return VirtualKeyCode.PAUSE
        elif self == HIDKeyCode.INSERT         : return VirtualKeyCode.INSERT
        elif self == HIDKeyCode.HOME           : return VirtualKeyCode.HOME
        elif self == HIDKeyCode.PAGE_UP        : return VirtualKeyCode.PAGE_UP
        elif self == HIDKeyCode.DELETE         : return VirtualKeyCode.DELETE
        elif self == HIDKeyCode.END            : return VirtualKeyCode.END
        elif self == HIDKeyCode.PAGE_DOWN      : return VirtualKeyCode.PAGE_DOWN
        elif self == HIDKeyCode.ARROW_RIGHT    : return VirtualKeyCode.ARROW_RIGHT
        elif self == HIDKeyCode.ARROW_LEFT     : return VirtualKeyCode.ARROW_LEFT
        elif self == HIDKeyCode.ARROW_DOWN     : return VirtualKeyCode.ARROW_DOWN
        elif self == HIDKeyCode.ARROW_UP       : return VirtualKeyCode.ARROW_UP
        elif self == HIDKeyCode.NUM_LOCK       : return VirtualKeyCode.NUM_LOCK
        elif self == HIDKeyCode.NUMPAD_DIVIDE  : return VirtualKeyCode.NUMPAD_DIVIDE
        elif self == HIDKeyCode.NUMPAD_MULTIPLY: return VirtualKeyCode.NUMPAD_MULTIPLY
        elif self == HIDKeyCode.NUMPAD_SUBTRACT: return VirtualKeyCode.NUMPAD_SUBTRACT
        elif self == HIDKeyCode.NUMPAD_ADD     : return VirtualKeyCode.NUMPAD_ADD
        elif self == HIDKeyCode.NUMPAD_ENTER   : return VirtualKeyCode.NUMPAD_ENTER
        elif self == HIDKeyCode.NUMPAD1        : return VirtualKeyCode.NUMPAD1
        elif self == HIDKeyCode.NUMPAD2        : return VirtualKeyCode.NUMPAD2
        elif self == HIDKeyCode.NUMPAD3        : return VirtualKeyCode.NUMPAD3
        elif self == HIDKeyCode.NUMPAD4        : return VirtualKeyCode.NUMPAD4
        elif self == HIDKeyCode.NUMPAD5        : return VirtualKeyCode.NUMPAD5
        elif self == HIDKeyCode.NUMPAD6        : return VirtualKeyCode.NUMPAD6
        elif self == HIDKeyCode.NUMPAD7        : return VirtualKeyCode.NUMPAD7
        elif self == HIDKeyCode.NUMPAD8        : return VirtualKeyCode.NUMPAD8
        elif self == HIDKeyCode.NUMPAD9        : return VirtualKeyCode.NUMPAD9
        elif self == HIDKeyCode.NUMPAD0        : return VirtualKeyCode.NUMPAD0
        elif self == HIDKeyCode.NUMPAD_DECIMAL : return VirtualKeyCode.NUMPAD_DECIMAL
        elif self == HIDKeyCode.CONTEXT_MENU   : return VirtualKeyCode.CONTEXT_MENU
        elif self == HIDKeyCode.CONTROL_LEFT   : return VirtualKeyCode.CONTROL_LEFT
        elif self == HIDKeyCode.SHIFT_LEFT     : return VirtualKeyCode.SHIFT_LEFT
        elif self == HIDKeyCode.ALT_LEFT       : return VirtualKeyCode.ALT_LEFT
        elif self == HIDKeyCode.OS_LEFT        : return VirtualKeyCode.OS_LEFT
        elif self == HIDKeyCode.CONTROL_RIGHT  : return VirtualKeyCode.CONTROL_RIGHT
        elif self == HIDKeyCode.SHIFT_RIGHT    : return VirtualKeyCode.SHIFT_RIGHT
        elif self == HIDKeyCode.ALT_RIGHT      : return VirtualKeyCode.ALT_RIGHT
        elif self == HIDKeyCode.OS_RIGHT       : return VirtualKeyCode.OS_RIGHT
        else                                   : return VirtualKeyCode.INVALID

