"""Host-side BLE debugger library."""

from importlib.metadata import PackageNotFoundError, version

from bledev.model.capture import CaptureMetadata, CaptureSession, CaptureStatistics
from bledev.model.events import BlePhy, InformationSource, RawRadioPacket

try:
    __version__ = version("bledev")
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
