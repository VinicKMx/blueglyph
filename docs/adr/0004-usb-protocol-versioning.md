# 0004: Use an Explicitly Versioned Binary USB Protocol

## Context

The firmware and host need a reliable transport contract for high-rate capture data.
Text logs cannot provide unambiguous framing, loss detection, or compatibility checks.

## Decision

The USB protocol uses binary frames with:

- magic bytes;
- protocol version;
- message type;
- payload length;
- sequence number;
- firmware timestamp;
- CRC32 trailer.

## Consequences

- The host can reject corrupted frames.
- Sequence gaps can become explicit packet-loss evidence.
- Protocol mismatches can fail loudly instead of corrupting sessions silently.
- Payload schemas can evolve under a versioned frame contract.

## Alternatives Considered

- Text protocol: rejected because logs are for humans and cannot be the capture transport.
- Raw packet streaming without framing: rejected because recovery and diagnostics would be fragile.

