
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
}


main > ../inv_output/inventory-$(date +%F).txt
