# Hardware

## Primary Development Hardware

The nRF52840 DK is the main development board.
It provides practical debugging access during firmware work.

## Final User Hardware

The nRF52840 Dongle is the intended final user capture device.
Production workflows must not assume that a J-Link debugger is attached.

## Firmware Responsibilities

Firmware should provide:

- hardware-generated timestamps;
- channel and PHY metadata;
- RSSI;
- CRC status;
- raw PDU bytes;
- sequence numbers;
- packet loss and overrun statistics;
- USB transport framing.

Firmware should not own high-level BLE semantics such as GATT interpretation or diagnostics.

## Supported Build Targets

Supported Zephyr build targets:

```text
nrf52840dk/nrf52840
nrf52840dongle/nrf52840
```
