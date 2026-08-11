"""Host-side BLE debugger library."""

from importlib.metadata import PackageNotFoundError, version

from blueglyph.model.capture import CaptureMetadata, CaptureSession, CaptureStatistics
from blueglyph.model.events import BlePhy, InformationSource, RawRadioPacket

try:
    __version__ = version("blueglyph")
except PackageNotFoundError:
    __version__ = "0.0.0+local"

__all__ = [
    "BlePhy",
    "CaptureMetadata",
    "CaptureSession",
    "CaptureStatistics",
    "InformationSource",
    "RawRadioPacket",
    "__version__",
]
