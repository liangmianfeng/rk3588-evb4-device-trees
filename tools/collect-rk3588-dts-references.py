#!/usr/bin/env python3
"""
Collect RK3588-family Linux device-tree sources and recursive #include
dependencies from the exact local Vendor 6.1 and Mainline 7.1.3 trees.

Run:
  python3 tools/collect-rk3588-dts-references.py

Optional source-tree overrides:
  VENDOR_KERNEL=/path/to/vendor/kernel MAINLINE_KERNEL=/path/to/mainline/kernel ...
"""
from pathlib import Path
import hashlib
import os
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "vendor-6.1": Path(os.environ.get(
        "VENDOR_KERNEL",
        str(Path.home() / "rk3588-source-check/armbian-build/cache/sources/linux-kernel-worktree/6.1__rk35xx__arm64")
    )).expanduser(),
    "mainline-7.1.3": Path(os.environ.get(
        "MAINLINE_KERNEL", "/mnt/d/linux-7.1.3/linux-7.1.3"
    )).expanduser(),
}
INCLUDE_RE = re.compile(r'^\s*#\s*include\s*[<"]([^">]+)[">]', re.MULTILINE)
FAMILY_RE = re.compile(r"^rk3588.*\.(?:dts|dtsi|dtso)$")

def run_git(tree, *args):
    try:
        return subprocess.check_output(
            ["git", "-C", str(tree), *args],
            stderr=subprocess.DEVNULL, text=True
        ).strip()
    except Exception:
        return "unavailable"

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def inside(path, parent):
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False

def resolve_include(name, including_file, kernel_root, repo_roots):
    inc = Path(name)
    candidates = []
    if inc.is_absolute():
        candidates.append(inc)
    else:
        candidates.append(including_file.parent / inc)
        candidates.extend([
            kernel_root / "arch/arm64/boot/dts/rockchip" / inc,
            kernel_root / "arch/arm64/boot/dts" / inc,
            kernel_root / "arch/arm64/boot/dts/include" / inc,
            kernel_root / "include" / inc,
            kernel_root / inc,
        ])
        for repo_root in repo_roots:
            candidates.append(repo_root / inc)
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
            if resolved.is_file():
                return resolved
        except OSError:
            pass
    return None

def collect(label, kernel_root):
    kernel_root = kernel_root.resolve()
    if not kernel_root.is_dir():
        raise SystemExit(f"ERROR: kernel source directory not found: {kernel_root}")

    rockchip_dir = kernel_root / "arch/arm64/boot/dts/rockchip"
    if not rockchip_dir.is_dir():
        raise SystemExit(f"ERROR: Rockchip DTS directory not found: {rockchip_dir}")

    out_root = ROOT / "reference" / label / "kernel"
    repo_roots = [ROOT / "vendor-6.1", ROOT / "mainline-7.1.3", ROOT]

    # Include every RK3588/RK3588S-family DTS/DTSI in this kernel version.
    starters = sorted(
        p.resolve() for p in rockchip_dir.iterdir()
        if p.is_file() and FAMILY_RE.match(p.name)
    )
    # Also walk the exact board DTS files maintained in this repository.
    if label == "vendor-6.1":
        starters += [
            ROOT / "vendor-6.1/rk3588-evb4-lp4-v10-linux.dts",
            ROOT / "vendor-6.1/rk3588-evb4-lp4-v10.dts",
            ROOT / "vendor-6.1/rk3588-evb4-lp4.dtsi",
        ]
    else:
        starters += [
            ROOT / "mainline-7.1.3/rk3588-evb4-nervus-es8388-uart0m2-uart5.dts"
        ]

    seen = set()
    copied = set()
    unresolved = set()
    stack = [Path(p).resolve() for p in starters if Path(p).is_file()]

    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)

        # Preserve kernel files using their original paths relative to the tree.
        if inside(current, kernel_root):
            rel = current.relative_to(kernel_root)
            destination = out_root / rel
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(current, destination)
            copied.add(destination)

        try:
            content = current.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        for include_name in INCLUDE_RE.findall(content):
            found = resolve_include(include_name, current, kernel_root, repo_roots)
            if found is None:
                unresolved.add(f"{current}: {include_name}")
            elif found not in seen:
                stack.append(found)

    # Keep a relevant subset of .config for driver/binding context.
    config = kernel_root / ".config"
    if config.is_file():
        prefixes = (
            "CONFIG_DRM", "CONFIG_ROCKCHIP", "CONFIG_USB", "CONFIG_TYPEC",
            "CONFIG_PHY", "CONFIG_STMMAC", "CONFIG_DWMAC", "CONFIG_NET",
            "CONFIG_MDIO", "CONFIG_SND_SOC", "CONFIG_I2C", "CONFIG_MFD",
            "CONFIG_REGULATOR", "CONFIG_PINCTRL", "CONFIG_COMMON_CLK",
        )
        lines = [
            line for line in config.read_text(errors="replace").splitlines()
            if line.startswith(prefixes) or (
                line.startswith("# CONFIG_") and
                any(key in line for key in prefixes)
            )
        ]
        ref_dir = ROOT / "reference" / label
        ref_dir.mkdir(parents=True, exist_ok=True)
        (ref_dir / "kernel-config-relevant.txt").write_text(
            "\n".join(lines) + "\n", encoding="utf-8"
        )

    commit = run_git(kernel_root, "rev-parse", "HEAD")
    branch = run_git(kernel_root, "branch", "--show-current")
    describe = run_git(kernel_root, "describe", "--always", "--dirty")
    ref_dir = ROOT / "reference" / label
    ref_dir.mkdir(parents=True, exist_ok=True)
    info = [
        f"# {label} RK3588 device-tree reference snapshot",
        "",
        f"- Source tree: {kernel_root}",
        f"- Git branch: {branch}",
        f"- Git commit: {commit}",
        f"- Git describe: {describe}",
        "- Scope: all rk3588* DTS/DTSI/DTSO files in arch/arm64/boot/dts/rockchip/",
        "  plus their recursively referenced #include dependencies.",
        "- These are reference copies; compile against the original matching kernel tree.",
        "",
    ]
    (ref_dir / "SOURCE-INFO.md").write_text("\n".join(info), encoding="utf-8")

    manifest = ref_dir / "SHA256SUMS.txt"
    files = sorted(p for p in ref_dir.rglob("*") if p.is_file() and p != manifest)
    manifest.write_text(
        "".join(f"{sha256(p)}  {p.relative_to(ref_dir).as_posix()}\n" for p in files),
        encoding="utf-8"
    )

    print(f"\n[{label}]")
    print(f"Source: {kernel_root}")
    print(f"Branch: {branch}")
    print(f"Commit: {commit}")
    print(f"RK3588 family DTS/DTSI starters: {len(starters)}")
    print(f"Kernel reference files copied: {len(copied)}")
    print(f"Output: {ref_dir}")
    if unresolved:
        print(f"Unresolved includes: {len(unresolved)}")
        for item in sorted(unresolved):
            print(f"  WARNING: {item}")
    else:
        print("Unresolved includes: 0")

def main():
    for label, source in SOURCES.items():
        collect(label, source)
    print("\nCollection finished. Review with:")
    print("  git status --short")
    print("  du -sh reference/")
    print("Then commit and push the reviewed reference snapshot.")

if __name__ == "__main__":
    main()
