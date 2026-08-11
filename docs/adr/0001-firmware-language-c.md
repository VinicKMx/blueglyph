# 0001: Use C for Firmware

## Context

The capture firmware runs on nRF52840 hardware and must interact directly with Zephyr, RADIO, TIMER, PPI, EasyDMA, interrupts, and USB.
The firmware should be small, deterministic, and easy to inspect by embedded contributors.

## Decision

Firmware is written in C using Zephyr and, when appropriate, nRF Connect SDK components.

## Consequences

- The firmware can use Zephyr APIs and Nordic peripheral headers directly.
- Low-level capture code can be kept close to the hardware.
- Host-side semantic logic must stay out of firmware.
- Firmware tests and CI must account for Zephyr tooling.

## Alternatives Considered

- Rust firmware: attractive for memory safety, but it would add toolchain and ecosystem complexity before the capture path is proven.
- C++ firmware: not needed for the current low-level module boundaries.

