# 0005: Build the Host Around a Layered Event Model

## Context

The project needs to present raw packets, protocol reconstruction, state changes, diagnostics, reports, and UI views without duplicating parsing logic in each frontend.

## Decision

The host uses a layered event model.
Higher-level objects reference the lower-level evidence that produced them.

Initial layers are `RawRadioPacket`, `CaptureSession`, `CaptureStatistics`, and `EvidenceRef`.
Future layers include decoded Link Layer packets, L2CAP frames, ATT transactions, GATT operations, device events, connection events, and diagnostic events.

## Consequences

- CLI and TUI can consume the same application API.
- Diagnostics can show packet evidence.
- Offline replay can rebuild semantic views.
- The project avoids putting important behavior exclusively in UI code.

## Alternatives Considered

- UI-driven parsing: rejected because it would duplicate logic and make diagnostics hard to test.
- Raw-byte-only model: rejected because it would make semantic reporting and diagnostics brittle.

