# Compatibility report

**Status: M0 complete (2026-10-25).** This report replaces the "presumed" and "reported" rows in spec §2 with evidence from the device. Nothing here is "device validated" in the spec §4 sense yet. That label requires a successful GPU smoke test (M2).

| | |
|---|---|
| Inventory runs | 2026-10-24, 2026-10-25 |
| Script | `scripts/inventory.sh` as of commit `7851005` |
| Evidence | [`docs/evidence/inventory-2026-10-25.txt`](evidence/inventory-2026-10-25.txt). Contains no IP addresses, MAC addresses, serial numbers or usernames. The hostname is left visible by choice: it only has meaning on the local network and already appears in the commit author name |

## Evidence labels

- **Confirmed**: read from inventory output on the device.
- **Reported**: stated by the owner, not checked by a command.
- **Pending**: not measured yet. Each pending row names the command or check that resolves it.

## Device and operating system

| Item | Spec expectation | Observed | Source | Status |
|---|---|---|---|---|
| Module | Jetson Nano 4GB (not Orin Nano) | "NVIDIA Jetson Nano Developer Kit", 3.9G total RAM, board `t210ref` (Tegra X1) | `/proc/device-tree/model`, `free -h`, `/etc/nv_tegra_release` | Confirmed: Jetson Nano 4GB Developer Kit |
| Architecture | aarch64 | aarch64 | `uname -a` | Confirmed |
| Kernel | 4.9.253-tegra | 4.9.253-tegra, built 2022-02-19 | `uname -a` | Confirmed |
| OS | Ubuntu 18.04 | Ubuntu 18.04.6 LTS (Bionic Beaver) | `cat /etc/os-release` | Confirmed |
| L4T | 32.7.1 | R32, revision 7.1 (GCID 29818004, dated 2022-02-19); package `nvidia-l4t-core` 32.7.1-20220219090432 | `cat /etc/nv_tegra_release`, `dpkg-query -W nvidia-l4t-core` | Confirmed: L4T 32.7.1 |
| JetPack | 4.6.1 | L4T 32.7.1 is the JetPack 4.6.1 release; CUDA, cuDNN and TensorRT versions match | `/etc/nv_tegra_release` and next section | Confirmed. The `nvidia-jetpack` meta-package is not installed, but its component packages are (next section) |
| glibc | — | 2.27 (Ubuntu GLIBC 2.27-3ubuntu1.4) | `ldd --version` | Confirmed. Below the 2.28 that current Node.js binaries need; see decision 0002 |

## NVIDIA libraries

| Item | Spec expectation | Observed | Source | Status |
|---|---|---|---|---|
| CUDA toolkit | 10.2 | Release 10.2, V10.2.300 | `/usr/local/cuda/bin/nvcc --version` | Confirmed |
| TensorRT (Python bindings) | 8.2.1 | 8.2.1.8 | `python3 -c "import tensorrt as t; print(t.__version__)"` | Confirmed under the system Python |
| TensorRT (runtime package) | 8.2.1 | `libnvinfer8` 8.2.1-1+cuda10.2 | `dpkg-query -W libnvinfer8` | Confirmed |
| cuDNN | 8.2.1 | `libcudnn8` 8.2.1.32-1+cuda10.2 | `dpkg-query -W libcudnn8` | Confirmed |
| JetPack meta-package | Record if present | `nvidia-jetpack` not installed | `dpkg-query -W nvidia-jetpack` | Not installed. The component packages above are present, so the runtime is unaffected (spec §6) |

## Python and libraries

| Item | Spec expectation | Observed | Source | Status |
|---|---|---|---|---|
| Python | 3.6.x | 3.6.9 | `python3 --version` | Confirmed. All edge code must run under 3.6.9 |
| OpenCV | Keep the vendor package | 4.1.1 | `cv2.__version__` | Confirmed |
| OpenCV GStreamer support | — | YES (1.14.5) | `cv2.getBuildInformation()` | Confirmed |
| OpenCV CUDA support | — | No CUDA line in the build information | `cv2.getBuildInformation()` | Built without CUDA. Expected for the stock package: GPU work goes through jetson-inference, OpenCV handles CPU-side work. Do not rebuild |
| NumPy | Prefer the existing vendor build | 1.13.3, from the Ubuntu apt package `python3-numpy` 1:1.13.3-2ubuntu1 | `numpy.__version__`, `dpkg-query -W python3-numpy` | Confirmed. Do not upgrade with pip. Keep `packages/vision_core` free of NumPy |

## Video decoding

| Item | Spec expectation | Observed | Source | Status |
|---|---|---|---|---|
| Hardware decoder | `nvv4l2decoder` plugin available | Present. Plugin `nvvideo4linux2` 1.14.0 at `/usr/lib/aarch64-linux-gnu/gstreamer-1.0/libgstnvvideo4linux2.so`, device `/dev/nvhost-nvdec` | `gst-inspect-1.0 nvv4l2decoder` | Confirmed |
| Decodable formats | H.264 for the first fixture | H.264, H.265, MPEG-4, MPEG-1/2, DivX 4/5, VP8, VP9, JPEG | `gst-inspect-1.0 nvv4l2decoder` (sink capabilities) | Confirmed by plugin capabilities. Actual decoding of a test file is checked in M2 |
| Decoder output | — | `video/x-raw(memory:NVMM)` | `gst-inspect-1.0 nvv4l2decoder` (src capabilities) | Confirmed. See Notes |
| GStreamer package versions | Record | GStreamer 1.14.5 linked into OpenCV | `cv2.getBuildInformation()` | Full package list recorded during M2 |

## Memory, storage, power and cooling

| Item | Spec expectation | Observed | Source | Status |
|---|---|---|---|---|
| RAM | About 4GB | 3.9G total; 521M used and 3.2G available at the time of the evidence run | `free -h` | Confirmed |
| Desktop session | Headless operation | Boots to the desktop (`graphical.target`); the `Xorg` display server was running | `systemctl get-default`, `pgrep -l Xorg` | Confirmed. The RAM figures above include the display server. A running desktop takes memory away from inference, so record its state for every benchmark. See Notes |
| Swap | Unknown | 1.9G, all zram: 4 devices of 495.5M at priority 5, 0B used. No swap on disk | `swapon --show` | Confirmed. zram costs CPU time to compress, so watch swap use during benchmarks |
| Storage | Unknown | microSD (`/dev/mmcblk0p1`): 118G, 13G used, 101G available. Card: SanDisk (manufacturer ID 0x000003, OEM ID 0x5344 = "SD"), product name SC128 (128GB), manufactured 09/2019 | `df -h`, `grep . /sys/block/mmcblk0/device/{type,name,manfid,oemid,date}` | Confirmed. The card's ID doesn't reveal the SanDisk product line or speed class. `serial` and `cid` are deliberately not read: they contain the card's unique serial number. Real read and write speed is measured in M5 if storage turns out to be a bottleneck |
| Power mode | Don't assume high power | MAXN (mode 0) | `nvpmodel -q`, run without sudo | Confirmed. Without sudo the EMC limit can't be read (error 13, permission denied) |
| Power supply | Unknown | Barrel jack (a 5V input on the Nano); current rating unknown, label not accessible | Owner | Open assumption. Check during M5 for under-power symptoms: reboots or shutdowns under load, and over-current warnings in `dmesg` (`soctherm: OC ALARM`) |
| Cooling | Unknown | Fan installed | Owner | Reported. `nvpmodel` warns "fan mode is not set". Check that the fan spins under load, for example `cat /sys/devices/pwm-fan/target_pwm` |
| Temperatures (idle) | Unknown | 2026-10-25, idle: AO-therm 33.5°C, CPU-therm 26.0°C, GPU-therm 22.0°C, PLL-therm 21.0°C, thermal-fan-est 24.0°C. PMIC-Die reports 50°C | `/sys/devices/virtual/thermal/thermal_zone*/{type,temp}` (values in millidegrees) | Confirmed as an idle baseline. Ignore PMIC-Die: its driver reports fixed alarm-threshold levels, not a live measurement. Temperatures under load are measured in M5 |

## Network and access

| Item | Spec expectation | Observed | Source | Status |
|---|---|---|---|---|
| Wi-Fi | Edimax EW-7811Un V2 works | Working | Owner | Reported. Keep the driver and settings unchanged; throughput not measured |
| SSH | Headless SSH works | Working | Owner | Reported |

## Notes

- `nvcc` is not on the default PATH. Scripts call `/usr/local/cuda/bin/nvcc` directly; don't change the global PATH.
- Run the inventory with the system interpreter. A virtual environment created without `--system-site-packages` hides `tensorrt`, `cv2` and `numpy`, because all three are installed as system packages, so the same import commands would fail inside it.
- Exit codes are only a hint. `nvpmodel` exits with code 0 even when it prints errors, and `dpkg-query` exits with code 1 when any one listed package is missing, even though it still reports the others. Read the output.
- NumPy 1.13.3 is from 2017 and the vendor OpenCV was built against it. Replacing it risks breaking the bindings confirmed above. Shared tracking and counting code is plain Python so it behaves the same under 3.6.9 here and 3.11 on the companion.
- Decoded frames from `nvv4l2decoder` live in NVIDIA hardware buffer memory (NVMM), not memory Python can read directly. jetson-utils handles the conversion. A hand-built OpenCV GStreamer pipeline needs `nvvidconv` to copy frames out.
- Device-tree strings such as `/proc/device-tree/model` end with a NUL byte instead of a newline. Strip it with `tr -d '\000'` so text tools don't treat the output file as binary.
- The board boots to the desktop. Booting without it (`sudo systemctl set-default multi-user.target`, undone with `graphical.target`) would free memory for the M2 build and for benchmarks. Not done; it's a reversible choice to make before M2.

## M0 checklist

- [x] Confirm board, OS, L4T and JetPack release.
- [x] Confirm hardware video decoder.
- [x] Confirm NumPy version and origin.
- [x] Confirm NVIDIA package versions (L4T core, TensorRT, cuDNN) and glibc.
- [x] Finish `scripts/inventory.sh`: thermal zones, NUL stripped from the device-tree model output, output path independent of the current directory.
- [x] Record idle temperatures.
- [x] Commit the final inventory output as evidence.
- [x] Add the microSD card model and desktop session state to `scripts/inventory.sh`.
- [x] Accept `docs/decisions/0002-deployment-profile.md`.

## Carried into M1

- [ ] Companion computer: record its OS and the exact Python 3.11 and Node 22 versions.

## Open assumptions

Spec §14 allows M0 to close with unresolved assumptions, as long as they are listed here.

- **Power supply rating.** Unknown because the adapter label isn't accessible. MAXN mode can draw more than a weak supply delivers, so watch for the symptoms listed in the power supply row during sustained runs. If they appear, record them and manually switch to the 5W mode (`sudo nvpmodel -m 1`) for a comparison run, rather than assuming the supply is adequate.
- **Cooling under load.** A fan is installed, but whether it runs automatically is unverified until M5.
