"""Capture session construction helpers."""

from __future__ import annotations

from blueglyph import __version__
from blueglyph.model.capture import CaptureMetadata, CaptureSession


def new_capture_session(
    *, hardware: str | None = None, firmware_version: str | None = None
) -> CaptureSession:
    """Create a host-side capture session with explicit provenance metadata."""

    metadata = CaptureMetadata(
        host_version=__version__,
        hardware=hardware,
        firmware_version=firmware_version,
    )
    return CaptureSession(metadata=metadata)
