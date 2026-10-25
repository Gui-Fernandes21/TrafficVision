#!/bin/bash
run() {
	echo "=== $1 ==="
	bash -c "$1" 2>&1
	local rc=$?
	echo "[exit $rc]"
	printf "\n"
}

main() {
	run "uname -a"
	run "free -h"
	run "python3 -c 'import tensorrt as t; print(t.__version__)'"
	run "/usr/local/cuda/bin/nvcc --version"
	run "python3 --version"
	run "python3 -c 'import cv2 as cv; print(cv.__version__)'"
	run "python3 -c 'import cv2; print(cv2.getBuildInformation())' | grep -E 'GStreamer|CUDA'"
	run "df -h"
	run "nvpmodel -q"
	run "swapon --show"
	run "cat /etc/os-release"
	run "cat /etc/nv_tegra_release"
	run "gst-inspect-1.0 nvv4l2decoder"
	run "tr -d '\000' < /proc/device-tree/model && echo"
	run "python3 -c 'import numpy as np; print(np.__version__)'"
	run "dpkg-query -W nvidia-l4t-core nvidia-jetpack libnvinfer8 libcudnn8 python3-numpy"
	run "ldd --version | head -1"
	run 'for z in /sys/devices/virtual/thermal/thermal_zone*; do echo "$(cat "$z/type"): $(cat "$z/temp") mC"; done'
	run "grep . /sys/block/mmcblk0/device/{type,name,manfid,oemid,date}"
	run "systemctl get-default"
	run "pgrep -l Xorg"
}

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUT_DIR="$SCRIPT_DIR/../docs/evidence"
mkdir -p "$OUT_DIR"

main > "$OUT_DIR/inventory-$(date +%F).txt"
