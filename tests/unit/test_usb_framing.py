from __future__ import annotations

import pytest
from hypothesis import given
from hypothesis import strategies as st

from blueglyph.protocol.usb import (
    HEADER_SIZE,
    PROTOCOL_VERSION,
    TRAILER_SIZE,
    FrameChecksumError,
    FrameParser,
    FramePayloadTooLargeError,
    FrameProtocolVersionError,
    MessageType,
    USBFrame,
)


@given(payload=st.binary(max_size=512))
def test_frame_round_trip(payload: bytes) -> None:
    frame = USBFrame(
        message_type=MessageType.RADIO_PACKET,
        sequence=42,
        timestamp_us=123_456,
        payload=payload,
    )

    decoded = USBFrame.decode_exact(frame.encode())

    assert decoded == frame


def test_incremental_parser_waits_for_split_frame() -> None:
    parser = FrameParser()
    encoded = USBFrame(
        message_type=MessageType.STATISTICS,
        sequence=7,
        timestamp_us=999,
        payload=b"stats",
    ).encode()

    assert parser.feed(encoded[:3]) == []
    assert parser.feed(encoded[3:]) == [
        USBFrame(
            message_type=MessageType.STATISTICS,
            sequence=7,
            timestamp_us=999,
            payload=b"stats",
        ),
    ]


def test_parser_discards_leading_noise_and_recovers() -> None:
    parser = FrameParser()
    frame = USBFrame(
        message_type=MessageType.DEVICE_STATUS,
        sequence=1,
        timestamp_us=2,
        payload=b"ok",
    )

    assert parser.feed(b"\x00\xffjunk" + frame.encode()) == [frame]


def test_decode_rejects_corrupt_crc() -> None:
    encoded = bytearray(
        USBFrame(
            message_type=MessageType.ERROR,
            sequence=1,
            timestamp_us=2,
            payload=b"error",
        ).encode(),
    )
    encoded[-1] ^= 0xFF

    with pytest.raises(FrameChecksumError):
        USBFrame.decode_exact(bytes(encoded))


def test_decode_rejects_unsupported_protocol_version() -> None:
    encoded = bytearray(
        USBFrame(
            message_type=MessageType.FIRMWARE_INFO,
            sequence=1,
            timestamp_us=2,
            payload=b"version",
        ).encode(),
    )
    encoded[2] = PROTOCOL_VERSION + 1

    with pytest.raises(FrameProtocolVersionError):
        USBFrame.decode_exact(bytes(encoded))


def test_parser_rejects_payload_larger_than_configured_limit() -> None:
    parser = FrameParser(max_payload_length=3)
    frame = USBFrame(
        message_type=MessageType.LOG,
        sequence=1,
        timestamp_us=2,
        payload=b"four",
    )

    with pytest.raises(FramePayloadTooLargeError):
        parser.feed(frame.encode())


def test_encoded_frame_length_matches_header_payload_trailer() -> None:
    payload = b"abc"
    encoded = USBFrame(
        message_type=MessageType.TIME_SYNC,
        sequence=3,
        timestamp_us=4,
        payload=payload,
    ).encode()

    assert len(encoded) == HEADER_SIZE + len(payload) + TRAILER_SIZE
