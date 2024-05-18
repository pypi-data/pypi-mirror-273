from enum import IntEnum


class Command(IntEnum):
    REBOOT                         = 1

    KEY_DOWN                       = 11
    KEY_UP                         = 12
    RELEASE_ALL_KEYS               = 13
    GET_KEY_STATE                  = 14
    GET_KEYBOARD_LEDS_STATE        = 15
    GET_KEYBOARD_STATE             = 16
    SEND_KEYBOARD_STATE            = 17

    BUTTON_DOWN                    = 31
    BUTTON_UP                      = 32
    RELEASE_ALL_BUTTONS            = 33
    GET_BUTTONS_STATE              = 34

    MOVE_REL                       = 51
    SCROLL_REL                     = 52
    GET_REL_MOUSE_STATE            = 53
    SEND_REL_MOUSE_STATE           = 54

    INIT_ABS_SYSTEM                = 71
    MOVE_ABS                       = 72
    SCROLL_ABS                     = 73
    GET_POS                        = 74
    SET_POS                        = 75
    GET_WHEEL_AXIS                 = 76
    SET_WHEEL_AXIS                 = 77
    GET_AXES                       = 78
    SET_AXES                       = 79
    GET_ABS_MOUSE_STATE            = 80
    SEND_ABS_MOUSE_STATE           = 81

    GET_HID_VENDOR_ID              = 91
    GET_HID_PRODUCT_ID             = 92
    GET_HID_VERSION_NUMBER         = 93
    GET_HID_MANUFACTURER_STRING    = 94
    GET_HID_PRODUCT_STRING         = 95

    CONFIG_HID_VENDOR_ID           = 111
    CONFIG_HID_PRODUCT_ID          = 112
    CONFIG_HID_VERSION_NUMBER      = 113
    CONFIG_HID_MANUFACTURER_STRING = 114
    CONFIG_HID_PRODUCT_STRING      = 115

    GET_DEVICE_ID                  = 131
    GET_DEVICE_SERIAL_NUMBER       = 132
    GET_FIRMWARE_VERSION           = 133
