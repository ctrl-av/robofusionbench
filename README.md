# RoboFusionBench

**A clean-room benchmark for studying how hardware constraints — latency, jitter, missed deadlines, numeric precision, and acceleration — affect EKF-based robot localization accuracy.**

This is not primarily a robotics project. It is an architecture/accelerator evaluation project that uses EKF-based 2D localization as the workload, so that hardware design choices can be judged by their effect on closed-loop estimator behavior, not just by kernel-level speed.

## Motivation

A faster matrix-multiply kernel is not automatically a better localization system. RoboFusionBench links hardware execution effects — compute latency, timing jitter, missed real-time deadlines, and reduced numeric precision — directly into an EKF's predict/update loop, and measures the consequence at the level of estimator and mission metrics rather than just cycles and throughput.

## What this benchmark measures

- **Estimator metrics**: ATE, RPE, drift, NIS gate acceptance/rejection, covariance sanity, failure/divergence rate.
- **Hardware metrics**: cycles and latency per predict/update, deadline miss rate, energy proxy, accelerator utilization.

See [docs/research_questions.md](docs/research_questions.md) for the questions this is designed to answer, and [docs/experiment_plan.md](docs/experiment_plan.md) for how they'll be tested.

## System overview

```
trajectory generator
        v
truth robot simulator
        v
fake sensor generator (odometry, absolute-position)
        v
EKF localization (predict / update / NIS gate)
        v
hardware constraint model (latency, jitter, precision, deadline policy)
        v
metrics (ATE, RPE, drift, gate stats, deadline stats)
        v
plots + technical report
```

The hardware model is consulted *during* the run, before deciding whether an update meets its deadline — hardware behavior is allowed to change estimator behavior, not just get reported after the fact.

## Repository structure

```
src/robofusionbench/   package code (sim, sensors, ekf, hardware, metrics, experiments, plotting, utils)
tests/                 unit and acceptance tests
docs/                  project spec, research questions, experiment plan, figures
results/               raw/processed experiment output and plots (gitignored except structure)
```

## Current status

Project scaffolding only. No simulation, sensor, or EKF code yet. Following the build order in [docs/experiment_plan.md](docs/experiment_plan.md):

1. Truth trajectory simulator (line, circle, figure-eight) with analytic sanity tests — not started
2. Sensor noise models (odometry + bias random walk, absolute-position) — not started
3. Baseline EKF localization, with dead-reckoning baseline comparison as the first acceptance gate — not started
4. Hardware-aware execution model (latency, jitter, deadlines) — not started
5. Precision / quantization model — not started
6. Architecture comparison and RTL calibration artifact — not started

## How to run

```
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
```

Experiment sweep commands will be documented here once `src/robofusionbench/experiments/` exists.

## Future work

Small synthesizable matrix-engine RTL block (3x3 matrix-vector multiply, then a 2x2 inverse / NIS calculator) to calibrate the accelerator hardware model against real synthesis estimates.
