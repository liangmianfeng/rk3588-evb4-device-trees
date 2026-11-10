# RK3588 EVB4 Device Trees

Device tree sources and compiled DTBs for the **Nervus RK3588 EVB4** board.

This repository maintains two separate device-tree versions:

- **Vendor Linux 6.1** — Rockchip Vendor kernel device trees.
- **Mainline Linux 7.1.3** — Armbian Mainline kernel device tree, customized for the Nervus RK3588 EVB4 hardware.

## Repository Structure

```text
.
├── README.md
├── vendor-6.1/
│   ├── README.md
│   ├── rk3588-evb4-lp4-v10-linux.dts
│   ├── rk3588-evb4-lp4-v10.dts
│   ├── rk3588-evb4-lp4.dtsi
│   ├── rk3588-evb4-lp4-v10-linux.dtb
│   └── vendor-6.1-SHA256SUMS.txt
│
└── mainline-7.1.3/
    ├── README.md
    ├── rk3588-evb4-nervus-es8388-uart0m2-uart5.dts
    ├── rk3588-evb4-nervus-es8388_ok.dtb
    └── rk3588-evb4-mainline-SHA256SUMS.txt
```

## Versions

| Directory | Kernel | Description |
|---|---|---|
| `vendor-6.1/` | Rockchip Vendor Linux 6.1 | RK3588 EVB4 LP4 V10 board device trees |
| `mainline-7.1.3/` | Armbian Mainline Linux 7.1.3 | Nervus EVB4 customized device tree, including ES8388 and UART configuration |

## Verification

Each version directory contains:

- Device tree source files (`.dts` / `.dtsi`)
- Compiled device tree binary (`.dtb`), where available
- SHA256 checksum manifest
- Version-specific documentation

Use the matching kernel source tree and device-tree dependencies when compiling DTS files.

**Do not mix Vendor and Mainline device trees.** Their kernel versions, bindings, and hardware configurations may differ.

## Important Notes

- The Vendor Android DTS is provided as source reference only; no Android DTB is included.
- The Mainline DTS and DTB are documented in their respective README.
- Check the SHA256 manifest before using or modifying any files.

## License

Refer to the original Rockchip and Linux kernel source files for their applicable SPDX license identifiers and copyright notices.
