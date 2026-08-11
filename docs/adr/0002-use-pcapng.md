# 0002: Use PCAPNG as the Canonical Packet Capture Format

## Context

BLE developers already use Wireshark for low-level packet inspection.
The project must interoperate with existing analysis workflows instead of inventing an incompatible capture format.

## Decision

PCAPNG is the canonical storage format for packets.
Project-specific semantic metadata may be stored alongside it, for example in JSON, but it must not replace PCAPNG.

## Consequences

- Captures can be opened in Wireshark.
- Offline replay and analysis can rebuild semantic state from recorded packets where possible.
- Additional metadata needs a clear mapping to packet evidence.

## Alternatives Considered

- Custom binary capture file: rejected because it would isolate the project from existing BLE tooling.
- JSON-only captures: rejected because raw packet fidelity and large-capture performance would suffer.

