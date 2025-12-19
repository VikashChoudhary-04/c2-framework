# OPSEC Considerations (Educational)

This document explains operational security concepts demonstrated
in this lab and their limitations.

## Implemented
- HTTPS transport to avoid plaintext traffic
- AES-GCM encryption
- Randomized beacon intervals (jitter)
- Minimal console output

## What This Does NOT Bypass
- Modern EDR solutions
- Behavioral detection
- Memory inspection
- Kernel-level monitoring

## How Real Attackers Improve This (High Level)
- Domain fronting
- Staged payloads
- In-memory execution
- Environment-based keys

This project intentionally avoids these techniques.
