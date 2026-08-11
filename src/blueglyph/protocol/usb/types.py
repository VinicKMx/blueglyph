"""Constants and enums for the firmware-to-host USB protocol."""

from __future__ import annotations

from enum import IntEnum
from struct import calcsize

PROTOCOL_MAGIC = 0xB1E0
PROTOCOL_VERSION = 1
MAX_PAYLOAD_LENGTH = 65535

HEADER_FORMAT = "<HBBHIQ"
TRAILER_FORMAT = "<I"
HEADER_SIZE = calcsize(HEADER_FORMAT)
TRAILER_SIZE = calcsize(TRAILER_FORMAT)


class MessageType(IntEnum):
    """Firmware-to-host and host-to-firmware message classes."""

    RADIO_PACKET = 0x01
    DEVICE_STATUS = 0x02
    CAPTURE_STATUS = 0x03
    ERROR = 0x04
    COMMAND_RESPONSE = 0x05
    FIRMWARE_INFO = 0x06
    TIME_SYNC = 0x07
    STATISTICS = 0x08
    LOG = 0x09
