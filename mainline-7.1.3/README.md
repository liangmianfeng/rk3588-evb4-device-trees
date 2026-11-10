# Nervus RK3588 EVB4 — Mainline Linux 7.1.3

Device tree files for the Nervus RK3588 EVB4 board, based on the
Armbian Mainline Linux 7.1.3 kernel.

## Files

| File | Description |
|---|---|
| `rk3588-evb4-nervus-es8388-uart0m2-uart5.dts` | DTS source for the board |
| `rk3588-evb4-nervus-es8388_ok.dtb` | Verified DTB currently used on the board |
| `rk3588-evb4-mainline-SHA256SUMS.txt` | SHA256 checksums |

## Platform

- Board: Nervus RK3588 EVB4
- Kernel family: Mainline
- Kernel version: 7.1.3
- Armbian branch: edge
- Architecture: ARM64
- Audio codec: ES8388

## Verification

The DTS source was compiled with `dtc` and its output was compared
against the DTB used on the board.

The compiled DTB matched the board DTB byte-for-byte.

Example:

```bash
dtc -I dts -O dtb \
  -o /tmp/nervus-verify.dtb \
  rk3588-evb4-nervus-es8388-uart0m2-uart5.dts

cmp /tmp/nervus-verify.dtb \
  rk3588-evb4-nervus-es8388_ok.dtb
```



`cmp` returns no output and exit status 0 when the two files are identical.

The DTS contains some DTC warnings. They have been retained without
modification because the compiled output matches the DTB used on the board.

## Notes

- The DTB is the verified board version.
- Keep the DTS and DTB filenames unchanged so that the checksum
  manifest remains valid.
- This directory contains Mainline 7.1.3 files only.
