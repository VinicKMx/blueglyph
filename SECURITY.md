# Security Policy

`bledev` is a debugging, observability, protocol analysis, and interoperability testing project.
It is not intended for jamming, unauthorized injection, connection hijacking, or bypassing BLE security.

## Reporting Vulnerabilities

Please report security issues privately before public disclosure.
Until a dedicated security contact is configured, open a minimal issue asking for a private contact path without publishing exploit details.

Include:

- affected component;
- reproduction steps;
- hardware and host OS;
- impact;
- whether sensitive BLE identifiers or payloads are present.

## Sensitive Captures

BLE captures can contain identifiers, names, manufacturer data, and application payloads.
Do not add real captures to the regression corpus unless they are anonymized or confirmed to contain no sensitive data.

## Cryptography Scope

Encrypted payloads should be shown as encrypted.
The architecture may later support decryption when a user legitimately provides keys for their own session.
The project must not implement mechanisms intended to break or bypass BLE security.

