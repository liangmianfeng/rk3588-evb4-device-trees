# Nervus RK3588 EVB4 - Vendor Linux 6.1

## Platform

- Board DTS family: Rockchip RK3588 EVB4 LP4 V10
- Target board: Nervus RK3588 EVB4
- Kernel: Rockchip Vendor Linux 6.1
- Kernel source version: v6.1.115-122303-g372ce582b94a
- Kernel branch: kernel-rk35xx-6.1
- Kernel commit: 372ce582b94a3360a29727c3c49c88bb7509da22
- Architecture: ARM64

## Files

| File | Description |
|---|---|
| rk3588-evb4-lp4-v10-linux.dts | Linux board DTS entry |
| rk3588-evb4-lp4-v10.dts | Android board DTS entry |
| rk3588-evb4-lp4.dtsi | Shared EVB4 LP4 V10 board description |
| rk3588-evb4-lp4-v10-linux.dtb | Compiled Vendor Linux DTB |

## Dependencies

The DTS files include common Rockchip kernel device-tree files, including:

- rk3588.dtsi
- rk3588-evb.dtsi
- rk3588-rk806-single.dtsi
- rk3588-linux.dtsi
- rk3588-android.dtsi
- dt-bindings/usb/pd.h

These common files are not duplicated in this directory. Use the matching Vendor kernel source tree and commit listed above to compile the DTS files.

## Build and verification notes

The Linux DTB was obtained from the Vendor 6.1 kernel build tree at the commit listed above.

Only the Linux DTB is included. The Android DTS source is included for reference; an Android DTB is not provided or claimed to be verified.

SHA256 checksums for the three DTS source files and the Linux DTB are recorded in `vendor-6.1-SHA256SUMS.txt`.
