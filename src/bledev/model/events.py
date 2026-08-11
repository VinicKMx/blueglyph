"""Typed events shared by capture, protocol, diagnostics, CLI, and future TUI code."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class InformationSource(StrEnum):
    """Origin of information presented to the user."""

    PASSIVE = "passive"
    CAPTURED = "captured"
    ACTIVE = "active"
    DERIVED = "derived"


class BlePhy(StrEnum):
    """BLE physical layer used for a captured radio event."""

    LE_1M = "le_1m"
    LE_2M = "le_2m"
    LE_CODED = "le_coded"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class EvidenceRef:
    """Stable reference from a semantic object back to the packet or event that proves it."""

    packet_sequence: int | None = None
    event_id: str | None = None
    source: InformationSource = InformationSource.CAPTURED


@dataclass(frozen=True, slots=True)
class RawRadioPacket:
    """Hardware-timestamped radio packet as emitted by the capture pipeline."""

    timestamp_us: int
    sequence: int
    channel: int
    phy: BlePhy
    rssi_dbm: int | None
    crc_ok: bool
    access_address: int
    pdu: bytes
    flags: frozenset[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if self.timestamp_us < 0:
            msg = "timestamp_us must be non-negative"
            raise ValueError(msg)
        if self.sequence < 0:
            msg = "sequence must be non-negative"
            raise ValueError(msg)
        if not 0 <= self.channel <= 39:
            msg = "BLE channel must be in the range 0..39"
            raise ValueError(msg)
        if not 0 <= self.access_address <= 0xFFFFFFFF:
            msg = "access_address must fit in uint32"
            raise ValueError(msg)
        object.__setattr__(self, "pdu", bytes(self.pdu))
