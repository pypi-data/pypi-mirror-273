import serial
from typing import Tuple, Optional
from .button import Button
from .command import Command
from .key_code import VirtualKeyCode
from .keyboard_led import KeyboardLED
from .state import ButtonsState, KeyboardState, KeyboardLEDsState, MouseState, KeyboardStateMask, MouseStateMask
from .status import Status


class Device:
    def __init__(self):
        self.__ser = serial.Serial()

    def open(self, port: str) -> Status:
        try:
            self.__ser.port          = port
            self.__ser.baudrate      = 250000
            self.__ser.timeout       = 50
            self.__ser.write_timeout = 50
            self.__ser.open()
            return Status.SUCCESS
        except serial.SerialException:
            return Status.SERIAL_ERROR

    def close(self) -> Status:
        if self.__ser.is_open:
            self.__ser.close()
            return Status.SUCCESS
        else:
            return Status.SERIAL_ERROR

    def reboot(self) -> Status:
        status = self.__send_packet(Command.REBOOT)
        if status != Status.SUCCESS: return status

        status, data = self.__recv_packet(Command.REBOOT, 1)
        if status != Status.SUCCESS: return status

        return data[0]

    def key_down(self, virtual_key_code: VirtualKeyCode) -> Status:
        status = self.__send_packet(Command.KEY_DOWN, virtual_key_code.to_hid_key_code().to_bytes())
        if status != Status.SUCCESS: return status

        status, data = self.__recv_packet(Command.KEY_DOWN, 1)
        if status != Status.SUCCESS: return status

        return data[0]

    def key_up(self, virtual_key_code: VirtualKeyCode) -> Status:
        status = self.__send_packet(Command.KEY_UP, virtual_key_code.to_hid_key_code().to_bytes())
        if status != Status.SUCCESS: return status

        status, data = self.__recv_packet(Command.KEY_UP, 1)
        if status != Status.SUCCESS: return status

        return data[0]

    def release_all_keys(self) -> Status:
        status = self.__send_packet(Command.RELEASE_ALL_KEYS)
        if status != Status.SUCCESS: return status

        status, data = self.__recv_packet(Command.RELEASE_ALL_KEYS, 1)
        if status != Status.SUCCESS: return status

        return data[0]

    def get_key_state(self, virtual_key_code: VirtualKeyCode) -> Tuple[Status, bool]:
        status = self.__send_packet(Command.GET_KEY_STATE, virtual_key_code.to_hid_key_code().to_bytes())
        if (status != Status.SUCCESS): return status, False

        status, data = self.__recv_packet(Command.GET_KEY_STATE, 1)
        if (status != Status.SUCCESS): return status, False

        return Status.SUCCESS, data[0] == 1

    def get_keyboard_leds_state(self) -> Tuple[Status, Optional[KeyboardLEDsState]]:
        status = self.__send_packet(Command.GET_KEYBOARD_LEDS_STATE)
        if (status != Status.SUCCESS): return status, None

        status, data = self.__recv_packet(Command.GET_KEYBOARD_LEDS_STATE, 1)
        if (status != Status.SUCCESS): return status, None

        return Status.SUCCESS, KeyboardLEDsState(data[0] & KeyboardLED.NUM_LOCK    != 0,
                                                 data[0] & KeyboardLED.CAPS_LOCK   != 0,
                                                 data[0] & KeyboardLED.SCROLL_LOCK != 0,
                                                 data[0] & KeyboardLED.COMPOSE     != 0,
                                                 data[0] & KeyboardLED.KANA        != 0)

    def get_keyboard_state(self) -> Tuple[Status, Optional[KeyboardState]]:
        status = self.__send_packet(Command.GET_KEYBOARD_STATE)
        if (status != Status.SUCCESS): return status, None

        status, keys = self.__recv_packet(Command.GET_KEYBOARD_STATE, 8)
        if (status != Status.SUCCESS): return status, None

        return Status.SUCCESS, KeyboardState(
            KeyboardState.ModeiferKeys(
                keys[0] & (1 << 0) != 0,
                keys[0] & (1 << 1) != 0,
                keys[0] & (1 << 2) != 0,
                keys[0] & (1 << 3) != 0,
                keys[0] & (1 << 4) != 0,
                keys[0] & (1 << 5) != 0,
                keys[0] & (1 << 6) != 0,
                keys[0] & (1 << 7) != 0,
            ),
            [VirtualKeyCode(keys[i + 1]) for i in range(7)]
        )

    def send_keyboard_state(self, keyboard_state: KeyboardState, keyboard_state_mask: KeyboardStateMask) -> Status:
        status =  self.__send_packet(Command.SEND_KEYBOARD_STATE,
                                     keyboard_state_mask.to_bytes() + keyboard_state.to_bytes())
        if status != Status.SUCCESS: return status

        status, data = self.__recv_packet(Command.SEND_KEYBOARD_STATE, 1)
        if status != Status.SUCCESS: return status

        return data[0]

    def button_down(self, button: Button) -> Status:
        status = self.__send_packet(Command.BUTTON_DOWN, button.to_bytes())
        if status != Status.SUCCESS: return status

        status, data = self.__recv_packet(Command.BUTTON_DOWN, 1)
        if status != Status.SUCCESS: return status

        return data[0]

    def button_up(self, button: Button) -> Status:
        status = self.__send_packet(Command.BUTTON_UP, button.to_bytes())
        if status != Status.SUCCESS: return status

        status, data = self.__recv_packet(Command.BUTTON_UP, 1)
        if status != Status.SUCCESS: return status

        return data[0]

    def release_all_buttons(self) -> Status:
        status = self.__send_packet(Command.RELEASE_ALL_BUTTONS)
        if status != Status.SUCCESS: return status

        status, data = self.__recv_packet(Command.RELEASE_ALL_BUTTONS, 1)
        if status != Status.SUCCESS: return status

        return data[0]

    def get_buttons_state(self) -> Tuple[Status, Optional[ButtonsState]]:
        status = self.__send_packet(Command.GET_BUTTONS_STATE)
        if (status != Status.SUCCESS): return status, None

        status, state = self.__recv_packet(Command.GET_BUTTONS_STATE, 1)
        if (status != Status.SUCCESS): return status, None

        return Status.SUCCESS, ButtonsState(
            state[0] & (1 << Button.LEFT)    != 0,
            state[0] & (1 << Button.RIGHT)   != 0,
            state[0] & (1 << Button.MIDDLE)  != 0,
            state[0] & (1 << Button.BUTTON4) != 0,
            state[0] & (1 << Button.BUTTON5) != 0,
        )

    def move_rel(self, x: int, y: int) -> Status:
        status = self.__send_packet(Command.MOVE_REL,
                                    x.to_bytes(2, 'little', signed=True) + y.to_bytes(2, 'little', signed=True))
        if status != Status.SUCCESS: return status

        status, data = self.__recv_packet(Command.MOVE_REL, 1)
        if status != Status.SUCCESS: return status

        return data[0]

    def scroll_rel(self, w: int) -> Status:
        status = self.__send_packet(Command.SCROLL_REL, w.to_bytes(2, 'little', signed=True))
        if status != Status.SUCCESS: return status

        status, data = self.__recv_packet(Command.SCROLL_REL, 1)
        if status != Status.SUCCESS: return status

        return data[0]

    def get_rel_mouse_state(self) -> Tuple[Status, Optional[MouseState]]:
        status = self.__send_packet(Command.GET_REL_MOUSE_STATE)
        if (status != Status.SUCCESS): return status, None

        status, data = self.__recv_packet(Command.GET_REL_MOUSE_STATE, 1)
        if (status != Status.SUCCESS): return status, None

        return Status.SUCCESS, MouseState(
            MouseState.Buttons(
                data[0] & (1 << Button.LEFT)    != 0,
                data[0] & (1 << Button.RIGHT)   != 0,
                data[0] & (1 << Button.MIDDLE)  != 0,
                data[0] & (1 << Button.BUTTON4) != 0,
                data[0] & (1 << Button.BUTTON5) != 0,
            ),
            MouseState.Axes(0, 0, 0)
        )

    def send_rel_mouse_state(self, mouse_state: MouseState, mouse_state_mask: MouseStateMask) -> Status:
        status = self.__send_packet(Command.SEND_REL_MOUSE_STATE,
                                    mouse_state_mask.to_bytes() + mouse_state.to_bytes())
        if status != Status.SUCCESS: return status

        status, data = self.__recv_packet(Command.SEND_REL_MOUSE_STATE, 1)
        if status != Status.SUCCESS: return status

        return data[0]

    def init_abs_system(self, screen_width: int, screen_height: int) -> Status:
        status = self.__send_packet(Command.INIT_ABS_SYSTEM,
                                    screen_width.to_bytes(2, 'little', signed=True) + screen_height.to_bytes(2, 'little', signed=True))
        if status != Status.SUCCESS: return status

        status, data = self.__recv_packet(Command.INIT_ABS_SYSTEM, 1)
        if status != Status.SUCCESS: return status

        return data[0]

    def move_abs(self, x: int, y: int) -> Status:
        status = self.__send_packet(Command.MOVE_ABS,
                                    x.to_bytes(2, 'little', signed=True) + y.to_bytes(2, 'little', signed=True))
        if status != Status.SUCCESS: return status

        status, data = self.__recv_packet(Command.MOVE_ABS, 1)
        if status != Status.SUCCESS: return status

        return data[0]

    def scroll_abs(self, w: int) -> Status:
        status = self.__send_packet(Command.SCROLL_ABS, w.to_bytes(2, 'little', signed=True))
        if status != Status.SUCCESS: return status

        status, data = self.__recv_packet(Command.SCROLL_ABS, 1)
        if status != Status.SUCCESS: return status

        return data[0]

    def get_pos(self) -> Tuple[Status, int, int]:
        status = self.__send_packet(Command.GET_POS)
        if (status != Status.SUCCESS): return status, -1, -1

        status, data = self.__recv_packet(Command.GET_POS, 4)
        if (status != Status.SUCCESS): return status, -1, -1

        return (Status.SUCCESS,
                int.from_bytes(data[0:2], 'little', signed=True),
                int.from_bytes(data[2:4], 'little', signed=True))

    def set_pos(self, x: int, y: int) -> Status:
        status = self.__send_packet(Command.SET_POS,
                                    x.to_bytes(2, 'little', signed=True) + y.to_bytes(2, 'little', signed=True))
        if status != Status.SUCCESS: return status

        status, data = self.__recv_packet(Command.SET_POS, 1)
        if status != Status.SUCCESS: return status

        return data[0]

    def get_wheel_axis(self) -> Tuple[Status, int]:
        status = self.__send_packet(Command.GET_WHEEL_AXIS)
        if (status != Status.SUCCESS): return status, 0

        status, data = self.__recv_packet(Command.GET_WHEEL_AXIS, 2)
        if (status != Status.SUCCESS): return status, 0

        return (Status.SUCCESS, int.from_bytes(data, 'little', signed=True))

    def set_wheel_axis(self, w: int) -> Status:
        status = self.__send_packet(Command.SET_WHEEL_AXIS, w.to_bytes(2, 'little', signed=True))
        if status != Status.SUCCESS: return status

        status, data = self.__recv_packet(Command.SET_WHEEL_AXIS, 1)
        if status != Status.SUCCESS: return status

        return data[0]

    def get_axes(self) -> Tuple[Status, int, int, int]:
        status = self.__send_packet(Command.GET_AXES)
        if (status != Status.SUCCESS): return status, -1, -1, 0

        status, data = self.__recv_packet(Command.GET_AXES, 6)
        if (status != Status.SUCCESS): return status, -1, -1, 0

        return (Status.SUCCESS,
                int.from_bytes(data[0:2], 'little', signed=True),
                int.from_bytes(data[2:4], 'little', signed=True),
                int.from_bytes(data[4:6], 'little', signed=True))

    def set_axes(self, x: int, y: int, w: int) -> Status:
        status = self.__send_packet(Command.SET_AXES,
                                    x.to_bytes(2, 'little', signed=True) + y.to_bytes(2, 'little', signed=True) + w.to_bytes(2, 'little', signed=True))
        if status != Status.SUCCESS: return status

        status, data = self.__recv_packet(Command.SET_AXES, 1)
        if status != Status.SUCCESS: return status

        return data[0]

    def get_abs_mouse_state(self) -> Tuple[Status, Optional[MouseState]]:
        status = self.__send_packet(Command.GET_ABS_MOUSE_STATE)
        if (status != Status.SUCCESS): return status, None

        status, data = self.__recv_packet(Command.GET_ABS_MOUSE_STATE, 7)
        if (status != Status.SUCCESS): return status, None

        return Status.SUCCESS, MouseState(
            MouseState.Buttons(
                data[0] & (1 << Button.LEFT)    != 0,
                data[0] & (1 << Button.RIGHT)   != 0,
                data[0] & (1 << Button.MIDDLE)  != 0,
                data[0] & (1 << Button.BUTTON4) != 0,
                data[0] & (1 << Button.BUTTON5) != 0,
            ),
            MouseState.Axes(
                int.from_bytes(data[1:3], 'little', signed=True),
                int.from_bytes(data[3:5], 'little', signed=True),
                int.from_bytes(data[5:7], 'little', signed=True)
            )
        )

    def send_abs_mouse_state(self, mouse_state: MouseState, mouse_state_mask: MouseStateMask) -> Status:
        status = self.__send_packet(Command.SEND_ABS_MOUSE_STATE,
                                    mouse_state_mask.to_bytes() + mouse_state.to_bytes())
        if status != Status.SUCCESS: return status

        status, data = self.__recv_packet(Command.SEND_ABS_MOUSE_STATE, 1)
        if status != Status.SUCCESS: return status

        return data[0]

    def config_hid_vendor_id(self, vendor_id: int) -> Status:
        status = self.__send_packet(Command.CONFIG_HID_VENDOR_ID, vendor_id.to_bytes(2, 'little'))
        if (status != Status.SUCCESS): return status

        status, data = self.__recv_packet(Command.CONFIG_HID_VENDOR_ID, 1)
        if (status != Status.SUCCESS): return status

        return Status(data[0])

    def config_hid_product_id(self, product_id: int) -> Status:
        status = self.__send_packet(Command.CONFIG_HID_PRODUCT_ID, product_id.to_bytes(2, 'little'))
        if (status != Status.SUCCESS): return status

        status, data = self.__recv_packet(Command.CONFIG_HID_PRODUCT_ID, 1)
        if (status != Status.SUCCESS): return status

        return Status(data[0])

    def config_hid_version_number(self, version_number: int) -> Status:
        status = self.__send_packet(Command.CONFIG_HID_VERSION_NUMBER, version_number.to_bytes(2, 'little'))
        if (status != Status.SUCCESS): return status

        status, data = self.__recv_packet(Command.CONFIG_HID_VERSION_NUMBER, 1)
        if (status != Status.SUCCESS): return status

        return Status(data[0])

    def config_hid_manufacturer_string(self, manufacturer_string: str) -> Status:
        status = self.__send_packet(Command.CONFIG_HID_MANUFACTURER_STRING, manufacturer_string.encode('utf-16-le'))
        if (status != Status.SUCCESS): return status

        status, data = self.__recv_packet(Command.CONFIG_HID_MANUFACTURER_STRING)
        if (status != Status.SUCCESS): return status

        return Status(data[0])

    def config_hid_product_string(self, product_string: str) -> Status:
        status = self.__send_packet(Command.CONFIG_HID_PRODUCT_STRING, product_string.encode('utf-16-le'))
        if (status != Status.SUCCESS): return status

        status, data = self.__recv_packet(Command.CONFIG_HID_PRODUCT_STRING)
        if (status != Status.SUCCESS): return status

        return Status(data[0])

    def get_hid_vendor_id(self) -> Tuple[Status, int]:
        status = self.__send_packet(Command.GET_HID_VENDOR_ID)
        if (status != Status.SUCCESS): return status, -1

        status, data = self.__recv_packet(Command.GET_HID_VENDOR_ID)
        if (status != Status.SUCCESS): return status, -1

        data_size = len(data)
        if data_size == 0: return Status.INVALID_RESPONSE_PACKET, -1

        status = Status(data[0])
        if data_size == 1 and status != Status.SUCCESS: return status, -1
        if data_size != 3 or status != Status.SUCCESS: return Status.INVALID_RESPONSE_PACKET, -1

        return Status.SUCCESS, int.from_bytes(data[1:3], 'little')

    def get_hid_product_id(self) -> Tuple[Status, int]:
        status = self.__send_packet(Command.GET_HID_PRODUCT_ID)
        if (status != Status.SUCCESS): return status, -1

        status, data = self.__recv_packet(Command.GET_HID_PRODUCT_ID)
        if (status != Status.SUCCESS): return status, -1

        data_size = len(data)
        if data_size == 0: return Status.INVALID_RESPONSE_PACKET, -1

        status = Status(data[0])
        if data_size == 1 and status != Status.SUCCESS: return status, -1
        if data_size != 3 or status != Status.SUCCESS: return Status.INVALID_RESPONSE_PACKET, -1

        return Status.SUCCESS, int.from_bytes(data[1:3], 'little')

    def get_hid_version_number(self) -> Tuple[Status, int]:
        status = self.__send_packet(Command.GET_HID_VERSION_NUMBER)
        if (status != Status.SUCCESS): return status, -1

        status, data = self.__recv_packet(Command.GET_HID_VERSION_NUMBER)
        if (status != Status.SUCCESS): return status, -1

        data_size = len(data)
        if data_size == 0: return Status.INVALID_RESPONSE_PACKET, -1

        status = Status(data[0])
        if data_size == 1 and status != Status.SUCCESS: return status, -1
        if data_size != 3 or status != Status.SUCCESS: return Status.INVALID_RESPONSE_PACKET, -1

        return Status.SUCCESS, int.from_bytes(data[1:3], 'little')

    def get_hid_manufacturer_string(self) -> Tuple[Status, str]:
        status = self.__send_packet(Command.GET_HID_MANUFACTURER_STRING)
        if (status != Status.SUCCESS): return status, ''

        status, data = self.__recv_packet(Command.GET_HID_MANUFACTURER_STRING)
        if (status != Status.SUCCESS): return status, ''

        data_size = len(data)
        if data_size == 0: return Status.INVALID_RESPONSE_PACKET, ''

        status = Status(data[0])
        if data_size == 1: return status, ''
        if status != Status.SUCCESS: return Status.INVALID_RESPONSE_PACKET, ''

        return Status.SUCCESS, data[1:].decode('utf-16-le')

    def get_hid_product_string(self) -> Tuple[Status, str]:
        status = self.__send_packet(Command.GET_HID_PRODUCT_STRING)
        if (status != Status.SUCCESS): return status, ''

        status, data = self.__recv_packet(Command.GET_HID_PRODUCT_STRING)
        if (status != Status.SUCCESS): return status, ''

        data_size = len(data)
        if data_size == 0: return Status.INVALID_RESPONSE_PACKET, ''

        status = Status(data[0])
        if data_size == 1: return status, ''
        if status != Status.SUCCESS: return Status.INVALID_RESPONSE_PACKET, ''

        return Status.SUCCESS, data[1:].decode('utf-16-le')

    def get_device_id(self) -> Tuple[Status, bytes]:
        status = self.__send_packet(Command.GET_DEVICE_ID)
        if (status != Status.SUCCESS): return status, b''

        return self.__recv_packet(Command.GET_DEVICE_ID, 20)

    def get_device_serial_number(self) -> Tuple[Status, bytes]:
        status = self.__send_packet(Command.GET_DEVICE_SERIAL_NUMBER)
        if (status != Status.SUCCESS): return status, b''

        return self.__recv_packet(Command.GET_DEVICE_SERIAL_NUMBER, 20)

    def get_firmware_version(self) -> Tuple[Status, int]:
        status = self.__send_packet(Command.GET_FIRMWARE_VERSION)
        if (status != Status.SUCCESS): return status, -1

        status, data = self.__recv_packet(Command.GET_FIRMWARE_VERSION, 2)
        if (status != Status.SUCCESS): return status, -1

        return Status.SUCCESS, int.from_bytes(data, 'little')

    def __send_packet(self, cmd: Command, data: bytes = b'') -> Status:
        try:
            packet = b'\xBE' + cmd.to_bytes(1, 'little') + len(data).to_bytes(1, 'little') + data + B'\xED';
            if self.__ser.write(packet) == len(packet):
                return Status.SUCCESS
            else:
                return Status.SERIAL_ERROR
        except serial.SerialException:
            return Status.SERIAL_ERROR

    def __recv_packet(self, cmd: Command, expected_size: Optional[int] = None) -> Tuple[Status, bytes]:
        try:
            for _ in range(100):
                packet_head = self.__ser.read(1)
                if len(packet_head) != 1: return Status.SERIAL_ERROR, b''
                if packet_head == b'\xBE': break
            else:
                return Status.INVALID_RESPONSE_PACKET, b''

            packet_cmd = self.__ser.read(1)
            if len(packet_cmd) != 1: return Status.SERIAL_ERROR, b''
            if packet_cmd[0] != cmd: return Status.INVALID_RESPONSE_PACKET, b''

            data_size = self.__ser.read(1)
            if len(data_size) != 1: return Status.SERIAL_ERROR, b''

            data_size = data_size[0]
            data = self.__ser.read(data_size) if data_size != 0 else b''
            if len(data) != data_size: return Status.SERIAL_ERROR, b''

            packet_tail = self.__ser.read(1)
            if len(packet_tail) != 1: return Status.SERIAL_ERROR, b''
            if packet_tail != b'\xED': return Status.INVALID_RESPONSE_PACKET, b''

            if expected_size != None and expected_size != data_size: return Status.INVALID_RESPONSE_PACKET, b''

            return Status.SUCCESS, data
        except serial.SerialException:
            return Status.SERIAL_ERROR
