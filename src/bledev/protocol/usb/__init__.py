"""Versioned USB protocol framing."""

from bledev.protocol.usb.framing import (
    FrameChecksumError,
    FrameParser,
    FramePayloadTooLargeError,
    FrameProtocolVersionError,
    FrameTruncatedError,
    USBFrame,
    USBProtocolError,
)
from bledev.protocol.usb.types import (
    HEADER_SIZE,
    MAX_PAYLOAD_LENGTH,
    PROTOCOL_MAGIC,
    PROTOCOL_VERSION,
    TRAILER_SIZE,
    MessageType,
)

__all__ = [
    "HEADER_SIZE",
    "MAX_PAYLOAD_LENGTH",
    "PROTOCOL_MAGIC",
    "PROTOCOL_VERSION",
    "TRAILER_SIZE",
    "FrameChecksumError",
    "FrameParser",
    "FramePayloadTooLargeError",
    "FrameProtocolVersionError",
    "FrameTruncatedError",
    "MessageType",
    "USBFrame",
    "USBProtocolError",
]
