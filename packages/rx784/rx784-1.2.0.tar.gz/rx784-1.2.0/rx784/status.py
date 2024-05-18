from enum import IntEnum


class Status(IntEnum):
    SUCCESS                 = 0
    SERIAL_ERROR            = 1
    READ_FLASH_ERROR        = 2
    WRITE_FLASH_ERROR       = 3
    INVALID_SIZE            = 4
    INVALID_COMMNAD_PACKET  = 5
    INVALID_RESPONSE_PACKET = 6
