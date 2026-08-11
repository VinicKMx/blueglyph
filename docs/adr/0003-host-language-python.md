# 0003: Use Python for Host Software

## Context

The host must provide CLI, TUI, protocol parsing, capture management, reports, and active BLE integration.
The project should be easy for BLE and embedded developers to extend.

## Decision

Host software is written in Python 3.12 or newer.

## Consequences

- Typer, Rich, Textual, pytest, Hypothesis, Ruff, mypy, Bleak, and pyserial fit naturally.
- The public library API can be used by scripts and tests.
- Performance-sensitive components can be measured first and moved to Rust later only if profiling proves the need.

## Alternatives Considered

- Rust-first host: rejected for the initial architecture because it would raise contribution and integration costs before bottlenecks are measured.
- C/C++ host: rejected because it would slow iteration on UX, diagnostics, and report generation.

