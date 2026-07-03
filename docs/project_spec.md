# Project Spec

## Identity

RoboFusionBench is a clean-room benchmark for studying how hardware constraints — latency, jitter, missed deadlines, numeric precision, and acceleration — affect EKF-based robot localization accuracy.

The architecture angle is the point, not a side note. This is an architecture/accelerator evaluation project that happens to use EKF localization as its workload, not a robotics project that happens to touch hardware.

## Thesis

The best hardware design for robot localization is not necessarily the one with the fastest EKF kernel. It is the design that preserves estimator stability and closed-loop accuracy under real-time, energy, and precision constraints.

## What "done" looks like for a claim

It is not enough to report cycles, latency, throughput, area, or energy for an accelerated kernel in isolation. Every hardware-side result must be connected to an estimator-level or mission-level outcome: ATE, RPE, drift, NIS gate behavior, missed-update rate, or mission success/failure. A hardware design choice that isn't shown to move one of those numbers hasn't been evaluated for this project's purposes.

## Clean-room boundary

Nothing in this repository may depend on or reference prior employer code, data, simulators, sensor configurations, repo structure, constants, diagrams, performance numbers, or architecture. Every line here is original and safe to publish.

Allowed as general public domain concepts: 2D robot localization, the Extended Kalman Filter, noisy odometry, noisy absolute-position sensing, latency/jitter modeling, fixed-point arithmetic, matrix accelerators, and RISC-V-style SoC concepts.

## Scope lock

**In scope for the MVP**: a 2D robot world, a small set of trajectory generators, a truth simulator, synthetic sensors, an EKF localizer, a hardware timing/precision model, metrics, plots, sweep-based experiments, and a technical report.

**Out of scope for the MVP** (possible future work, not now): real SLAM, camera-based perception, MuJoCo/ROS integration, real robot hardware, a full RISC-V SoC or ASIC flow, FPGA deployment, multi-robot simulation, 3D pose estimation, visual feature tracking, path planning, deep learning.

If a proposed feature doesn't serve the thesis above, it gets cut, regardless of how interesting it is on its own.

## Contributions

1. A clean-room 2D EKF localization benchmark that evaluates robot-level estimation quality, not just filter correctness.
2. A hardware-aware execution model that injects latency, jitter, missed deadlines, stale updates, and numeric precision effects into the EKF loop as it runs.
3. A comparative architecture study connecting CPU-only, fixed-point, vector-style, and accelerator-assisted EKF execution to closed-loop localization metrics.
4. (Stretch) A small synthesizable RTL matrix engine used to calibrate the accelerator timing/energy model against real synthesis estimates.

## Design philosophy

Start abstract and calibrate downward toward real hardware, rather than starting with an ASIC flow:

```
Level 0: ideal math model (no hardware effects)
Level 1: latency / energy model
Level 2: precision / quantization model
Level 3: accelerator model
Level 4: RTL block
Level 5: synthesis estimate
Level 6: SoC / FPGA / embedded validation (not planned for this project)
```

Useful research output exists by Level 3. Levels 4-5 make the accelerator numbers credible rather than assumed; they are a stretch goal, not a prerequisite for the core thesis.

## Bounds (the box everything must fit inside)

- **Application**: EKF-based 2D robot localization.
- **Hardware concern**: latency, jitter, precision, acceleration.
- **Architecture question**: which hardware design choices preserve estimator accuracy under resource constraints?
- **Outputs**: metrics, plots, a technical report, the repo itself, and optionally an RTL artifact.
