# 0002. Split deployment: Jetson edge worker plus companion service

- **Status:** Accepted
- **Date:** 2026-10-25
- **Decider:** Gui Fernandes
- **Spec references:** §3 (architecture and deployment profiles), §4 (compatibility policy), §12 (acceptance gate 9)
- **Evidence:** `docs/compatibility.md`

## Context

The inventory confirmed the edge platform:

- Jetson Nano 4GB Developer Kit, 3.9G RAM shared between CPU and GPU, zram swap only, microSD storage.
- Ubuntu 18.04.6, L4T 32.7.1 (JetPack 4.6.1), CUDA 10.2, TensorRT 8.2.1.8.
- System Python 3.6.9 with vendor OpenCV 4.1.1 and apt NumPy 1.13.3. TensorRT's Python bindings work with this interpreter.

The rest of the project needs a modern stack: Python 3.11 for FastAPI 0.115.6 and Pydantic 2, and Node 22 to build the Nuxt 3 dashboard. That stack doesn't fit on the Jetson:

- TensorRT's bindings are tied to the system Python 3.6, so the service would need a second interpreter next to it. The spec forbids replacing `/usr/bin/python3`.
- The Jetson has glibc 2.27 (confirmed with `ldd --version`), while official Node.js Linux binaries since version 18 require glibc 2.28 or later.
- Every megabyte used by an API server, database or Node build is taken from the memory that decoding and inference need.

## Decision

Use the split profile recommended in spec §3.

- **Jetson: edge worker only.** System Python 3.6.9 with the vendor TensorRT, OpenCV and NumPy. Pipeline: local MP4 → decode → detect → track → count → run bundle and spool on local disk. No Node, API server or database server on the Jetson.
- **Companion computer: everything else.** FastAPI on Python 3.11, SQLite (decision 0001), and the static Nuxt 3 dashboard built with Node 22. The API binds to loopback by default.
- **Transfer.** In the MVP, completed run bundles are copied over SSH and imported on the companion. Online batch upload over the LAN or an SSH tunnel comes later (M5) and uses the same validation and idempotency code.
- **Independence.** A run on the Jetson must complete with no network and no API available.
- **Shared code.** `packages/vision_core` and `packages/contracts` must run unchanged under Python 3.6.9 and 3.11, using only the standard library.

## Alternatives considered

**All on the Jetson.** Not chosen for the MVP: it needs a second Python interpreter, Node 22 can't run on this glibc, and the service competes with inference for 4GB of shared memory. The spec allows trying it only after the split profile works.

**Python 3.6 FastAPI stack on the Jetson** (FastAPI 0.83.0 still declares Python 3.6 support; later releases dropped it). Not chosen: it pins the service to an old dependency graph that would need its own lock and security review. The spec treats it as a last resort for a LAN demo.

**L4T-matched containers on the Jetson.** Not chosen for the service: it adds complexity on a memory-constrained device. It stays available as a fallback if the inference backend fails to build natively (spec §4).

## Consequences

**Positive**

- Each side uses a stack its platform supports.
- The Jetson's memory goes to decoding and inference.
- M1, M3 and M4 can be developed and tested on the companion without the Jetson.

**Costs and things to watch**

- Two Python versions in one repository: separate lockfiles (spec §4 forbids forcing 3.6 and 3.11 into one lock), and CI must check that shared code still runs under 3.6.
- Shared code is limited to Python 3.6 syntax: no dataclasses, walrus operator, `f"{x=}"` or modern type-annotation syntax.
- Results reach the dashboard only after a transfer step. In the MVP that step is a manual `scp`.
- A companion machine is required. Which machine (likely the Windows development machine, natively or through WSL2) and its runtime versions are still to be recorded in `docs/compatibility.md`.

## Revisit when

- A live camera or on-device dashboard becomes a requirement.
- The Jetson is replaced or reflashed with a newer JetPack release.
- The transfer step becomes a bottleneck in practice.
