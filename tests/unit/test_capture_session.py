from __future__ import annotations

import pytest

from blueglyph.model import BlePhy, CaptureMetadata, CaptureSession, RawRadioPacket


def test_capture_session_tracks_packets_and_loss() -> None:
    session = CaptureSession(metadata=CaptureMetadata(host_version="test"))
    packet = RawRadioPacket(
        timestamp_us=100,
        sequence=1,
        channel=37,
        phy=BlePhy.LE_1M,
        rssi_dbm=-42,
        crc_ok=True,
        access_address=0x8E89BED6,
        pdu=b"\x02\x01\x06",
    )

    session.add_packet(packet)
    session.record_packet_loss(1)

    assert session.packets == [packet]
    assert session.statistics.packets_captured == 1
    assert session.statistics.packets_dropped == 1
    assert session.statistics.drop_rate == 0.5


def test_capture_session_rejects_negative_packet_loss() -> None:
    session = CaptureSession(metadata=CaptureMetadata(host_version="test"))

    with pytest.raises(ValueError, match="non-negative"):
        session.record_packet_loss(-1)


def test_raw_radio_packet_validates_channel() -> None:
    with pytest.raises(ValueError, match=r"0\.\.39"):
        RawRadioPacket(
            timestamp_us=100,
            sequence=1,
            channel=40,
            phy=BlePhy.LE_1M,
            rssi_dbm=None,
            crc_ok=False,
            access_address=0,
            pdu=b"",
        )
