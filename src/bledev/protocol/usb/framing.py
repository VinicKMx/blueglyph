"""Binary framing for the versioned USB protocol."""

from __future__ import annotations

import struct
import zlib
from dataclasses import dataclass
from typing import Self

from bledev.protocol.usb.types import (
    HEADER_FORMAT,
    HEADER_SIZE,
    MAX_PAYLOAD_LENGTH,
    PROTOCOL_MAGIC,
    PROTOCOL_VERSION,
    TRAILER_FORMAT,
    TRAILER_SIZE,
)

_MAGIC_BYTES = struct.pack("<H", PROTOCOL_MAGIC)


class USBProtocolError(Exception):
    """Base class for structured USB protocol parsing failures."""


class FrameTruncatedError(USBProtocolError):
    """A complete frame was required but fewer bytes were available."""


class FrameProtocolVersionError(USBProtocolError):
    """A frame used an unsupported protocol version."""


class FramePayloadTooLargeError(USBProtocolError):
    """A frame announced a payload larger than the configured parser limit."""


class FrameChecksumError(USBProtocolError):
    """A frame checksum did not match the header and payload bytes."""


@dataclass(frozen=True, slots=True)
class USBFrame:
    """A single framed message on the firmware USB protocol."""

    message_type: int
    sequence: int
    timestamp_us: int
    payload: bytes = b""
    protocol_version: int = PROTOCOL_VERSION

    def __post_init__(self) -> None:
        if not 0 <= self.message_type <= 0xFF:
            msg = "message_type must fit in uint8"
            raise ValueError(msg)
        if not 0 <= self.sequence <= 0xFFFFFFFF:
            msg = "sequence must fit in uint32"
            raise ValueError(msg)
        if self.timestamp_us < 0:
            msg = "timestamp_us must be non-negative"
            raise ValueError(msg)
        if len(self.payload) > MAX_PAYLOAD_LENGTH:
            msg = "payload exceeds the protocol uint16 length field"
            raise ValueError(msg)
        object.__setattr__(self, "payload", bytes(self.payload))

    def encode(self) -> bytes:
        """Encode this frame using little-endian header fields and a CRC32 trailer."""

        header = struct.pack(
            HEADER_FORMAT,
            PROTOCOL_MAGIC,
            self.protocol_version,
            self.message_type,
            len(self.payload),
            self.sequence,
            self.timestamp_us,
        )
        crc = _crc32(header, self.payload)
        return header + self.payload + struct.pack(TRAILER_FORMAT, crc)

    @classmethod
    def decode_exact(cls, data: bytes, *, max_payload_length: int = MAX_PAYLOAD_LENGTH) -> Self:
        """Decode one complete frame and reject trailing or missing bytes."""

        if len(data) < HEADER_SIZE + TRAILER_SIZE:
            raise FrameTruncatedError("frame is shorter than the protocol header and trailer")

        magic, version, message_type, payload_length, sequence, timestamp_us = struct.unpack(
            HEADER_FORMAT,
            data[:HEADER_SIZE],
        )
        if magic != PROTOCOL_MAGIC:
            msg = f"invalid frame magic 0x{magic:04X}"
            raise USBProtocolError(msg)
        if version != PROTOCOL_VERSION:
            msg = f"unsupported protocol version {version}"
            raise FrameProtocolVersionError(msg)
        if payload_length > max_payload_length:
            msg = f"payload length {payload_length} exceeds parser limit {max_payload_length}"
            raise FramePayloadTooLargeError(msg)

        expected_length = HEADER_SIZE + payload_length + TRAILER_SIZE
        if len(data) != expected_length:
            msg = f"frame length {len(data)} does not match announced length {expected_length}"
            raise FrameTruncatedError(msg)

        payload_start = HEADER_SIZE
        payload_end = payload_start + payload_length
        payload = data[payload_start:payload_end]
        expected_crc = struct.unpack(TRAILER_FORMAT, data[payload_end:expected_length])[0]
        actual_crc = _crc32(data[:HEADER_SIZE], payload)
        if expected_crc != actual_crc:
            msg = f"frame CRC mismatch: expected 0x{expected_crc:08X}, got 0x{actual_crc:08X}"
            raise FrameChecksumError(msg)

        return cls(
            protocol_version=version,
            message_type=message_type,
            sequence=sequence,
            timestamp_us=timestamp_us,
            payload=payload,
        )


class FrameParser:
    """Incremental USB frame parser that can resynchronize after leading garbage bytes."""

    def __init__(self, *, max_payload_length: int = MAX_PAYLOAD_LENGTH) -> None:
        if max_payload_length < 0 or max_payload_length > MAX_PAYLOAD_LENGTH:
            msg = f"max_payload_length must be between 0 and {MAX_PAYLOAD_LENGTH}"
            raise ValueError(msg)
        self._buffer = bytearray()
        self._max_payload_length = max_payload_length

    def feed(self, chunk: bytes) -> list[USBFrame]:
        """Append bytes from USB and return every complete frame currently available."""

        if chunk:
            self._buffer.extend(chunk)

        frames: list[USBFrame] = []
        while True:
            magic_index = self._buffer.find(_MAGIC_BYTES)
            if magic_index < 0:
                self._keep_possible_partial_magic()
                break
            if magic_index:
                del self._buffer[:magic_index]
            if len(self._buffer) < HEADER_SIZE:
                break

            payload_length = struct.unpack_from("<H", self._buffer, 4)[0]
            if payload_length > self._max_payload_length:
                del self._buffer[: len(_MAGIC_BYTES)]
                msg = (
                    f"payload length {payload_length} "
                    f"exceeds parser limit {self._max_payload_length}"
                )
                raise FramePayloadTooLargeError(msg)

            frame_length = HEADER_SIZE + payload_length + TRAILER_SIZE
            if len(self._buffer) < frame_length:
                break

            frame_bytes = bytes(self._buffer[:frame_length])
            del self._buffer[:frame_length]
            frames.append(
                USBFrame.decode_exact(frame_bytes, max_payload_length=self._max_payload_length),
            )
        return frames

    def _keep_possible_partial_magic(self) -> None:
        if self._buffer.endswith(_MAGIC_BYTES[:1]):
            self._buffer[:] = self._buffer[-1:]
        else:
            self._buffer.clear()


def _crc32(header: bytes, payload: bytes) -> int:
    return zlib.crc32(payload, zlib.crc32(header)) & 0xFFFFFFFF
