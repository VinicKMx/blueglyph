# Architecture

`bledev` is a BLE debugger built around one rule:

> The hardware captures; the host interprets.

The firmware should remain small, deterministic, and focused on radio capture, hardware timestamps, RSSI, CRC status, buffering, and USB transport.
The host owns parsing, protocol reconstruction, state tracking, diagnostics, persistence, reports, and UI.

## Target Architecture

```text
CLI / TUI
  |
Application API
  |
CaptureSession and Event Model
  |
Semantic Engine      Diagnostic Engine      Capture Management
  |                  |                      |
GAP / LL / L2CAP / ATT / GATT / SMP         PCAPNG / replay / export
  |
Backends: nRF52840 USB, PCAP replay, Active BLE, Wireshark extcap
  |
nRF52840 firmware: RADIO / TIMER / PPI / EasyDMA / USB
```

## Boundaries

These boundaries are architectural constraints:

- radio capture is separate from USB transport;
- USB framing is separate from BLE protocol parsing;
- protocol parsing is separate from the application model;
- diagnostics are separate from CLI and TUI rendering;
- PCAP replay is separate from live transport;
- active BLE operations are separate from passive observation.

## Event Model

The application must not depend everywhere on raw packet bytes.
Higher-level objects need evidence references back to lower-level events.

Initial model layers:

- `RawRadioPacket`;
- `CaptureSession`;
- `CaptureStatistics`;
- `EvidenceRef`.

Planned layers:

- decoded Link Layer packets;
- L2CAP frames;
- ATT messages and transactions;
- GATT operations;
- connection events;
- device events;
- diagnostic events.

## Information Sources

User-facing information must mark its origin:

- `PASSIVE`: observed from radio traffic;
- `CAPTURED`: observed during a captured connection;
- `ACTIVE`: obtained by an explicit host-side BLE operation;
- `DERIVED`: inferred by host analysis.

An inference must not be presented as a direct observation.

## Current Checkpoint

The repository currently establishes the engineering foundation:

- Python packaging and tooling;
- typed capture/event models;
- USB protocol framing tests;
- Zephyr firmware module boundaries;
- project documentation and ADRs;
- CI definitions.

The current firmware does not yet capture radio traffic.
The current host does not yet parse BLE advertisements or write PCAPNG.

