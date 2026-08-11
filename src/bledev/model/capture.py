"""Capture session model."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from bledev.model.events import RawRadioPacket


@dataclass(frozen=True, slots=True)
class CaptureMetadata:
    """Metadata that travels with a capture session and later reports."""

    host_version: str
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    hardware: str | None = None
    firmware_version: str | None = None
    notes: str | None = None


@dataclass(slots=True)
class CaptureStatistics:
    """Loss and malformed-input counters that must never be hidden from users."""

    packets_captured: int = 0
    packets_dropped: int = 0
    malformed_frames: int = 0

    @property
    def drop_rate(self) -> float:
        total = self.packets_captured + self.packets_dropped
        if total == 0:
            return 0.0
        return self.packets_dropped / total


@dataclass(slots=True)
class CaptureSession:
    """Application-level object shared by live capture, replay, reports, CLI, and TUI."""

    metadata: CaptureMetadata
    packets: list[RawRadioPacket] = field(default_factory=list)
    statistics: CaptureStatistics = field(default_factory=CaptureStatistics)

    def add_packet(self, packet: RawRadioPacket) -> None:
        self.packets.append(packet)
        self.statistics.packets_captured += 1

    def record_packet_loss(self, count: int = 1) -> None:
        if count < 0:
            msg = "packet loss count must be non-negative"
            raise ValueError(msg)
        self.statistics.packets_dropped += count

    def record_malformed_frame(self) -> None:
        self.statistics.malformed_frames += 1
