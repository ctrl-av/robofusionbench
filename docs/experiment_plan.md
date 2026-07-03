# Experiment Plan

## Build order

The benchmark is worthless until the baseline estimator is trustworthy. Hardware-aware experiments are meaningless before that. Order:

1. **Truth simulator** — trajectory generators (line, circle, figure-eight) + unicycle kinematics, verified against analytic invariants (circle radius = v/omega, line has zero cross-track error).
2. **Sensors** — odometry (noise + slowly-drifting bias) and absolute-position (noisier per-tick, but non-drifting), verified against their configured noise statistics.
3. **Baseline EKF** — state `[x, y, theta]`, predict/update/NIS gate, compared against an odometry-only dead-reckoning baseline on the *same* measurement stream. **Acceptance gate: over a fixed set of 20 seeds, on a circle trajectory under default noise, the EKF's RMSE ATE must be lower than dead-reckoning's RMSE ATE on every one of the 20 seeds.** Fixed seeds make this deterministic in CI. Nothing hardware-related is meaningful until this passes.
4. **Hardware execution model** — latency, jitter, deadline policy (MVP: skip late update), wired in *during* the simulation loop so a missed deadline actually changes what the EKF sees.
5. **Precision model** — software quantization (float32, Q24.8, Q16.16, Q12.20 at minimum), applied at the state/covariance level first.
6. **Architecture comparison** — named hardware profiles (CPU-only, fixed-point CPU, matrix accelerator, EKF-update accelerator) evaluated on both hardware and estimator metrics together.
7. **(Stretch) RTL calibration** — a small fixed-size matrix engine (3x3 matrix-vector multiply) simulated and, if a synthesis toolchain is available, given real area/timing numbers to replace assumed accelerator cycle counts.

## Experiment matrix, in the order they'll actually be run

### Experiment A — Sanity baseline
- Trajectory: circle. Hardware: ideal (zero latency). Precision: float64.
- Expected: EKF tracks truth noticeably better than odometry-only dead reckoning.
- This *is* the Commit 4 acceptance test, run once as a sanity check and again as an automated test.

### Experiment B — Latency sweep (RQ1)
- Sweep: update latency in `{0, 1, 2, 5, 7, 9, 10, 20}` ms, precision fixed at float64, deadline policy = skip late update.
- The deadline (`dt` = 10 ms at the default 100 Hz tick rate) applies to the *total* per-tick compute budget: predict latency + update latency must together fit within `dt`, not update latency alone. Predict latency is held fixed and small in this sweep so update latency is the only thing moving.
- The 10 ms and 20 ms points are expected to saturate: at that point every update misses the deadline, the policy skips every correction, and the run degrades to permanent predict-only (dead reckoning). Both points should land at effectively the same RMSE ATE — that saturation *is* the result (total correction starvation), not a bug. The 7 ms and 9 ms points exist specifically to resolve the transition curve between "mostly fine" and "fully saturated" before the cliff.
- Plot: update latency (x) vs. RMSE ATE (y); secondary plot vs. missed-update rate.

### Experiment C — Update-rate sweep (supporting RQ1)
- Sweep: absolute-position correction every `{1, 2, 5, 10, 20}` ticks.
- Expected: fewer corrections -> more drift. Establishes the baseline cost of *not* accelerating, independent of jitter.

### Experiment D — Precision sweep (RQ2)
- Sweep: `{float64, float32, Q24.8, Q16.16, Q12.20, Q8.8}`.
- Record: ATE, RPE, NIS rejection rate, covariance trace, failure rate.
- Expected: degradation is not linear — a threshold precision exists below which NIS gating and covariance sanity break down before ATE visibly does.

### Experiment E — Architecture comparison (RQ3)
- Compare: CPU float32, CPU fixed-point, CPU + matrix accelerator, CPU + EKF-update accelerator (add vector-style accelerator if time permits).
- Plot: energy proxy per update (x) vs. RMSE ATE (y), points labeled by architecture. This is the central "computer architecture paper" result.

### Experiment F — Jitter sweep (RQ1, deferred until B-E are solid)
- Sweep: `{0%, 10%, 25%, 50%, burst}` jitter at matched average latency.
- Tests whether tail latency is worse than average latency at the same mean cost.

### Experiment G — Outlier robustness (optional, deferred)
- Inject absolute-sensor outliers at rate `{0%, 1%, 5%, 10%}`; test whether low precision or stale predictions change gate robustness (false accept/reject).

Experiments F and G are real and planned, but are explicitly sequenced after A-E so that the core latency/precision/architecture story is complete and correct before adding jitter and outlier complexity on top of it.

## Defaults (unless an experiment overrides them)

```
duration = 30 s, dt = 0.01 s (100 Hz), seeds = 50-100
trajectory = circle or figure-eight, initial state = [0, 0, 0]
EKF state = [x, y, theta], gate_threshold = 5.991 (95%, 2 dof)
absolute-position update rate = 10 Hz (default; experiments may override explicitly)
deadline policy = skip late update
```

## Failure conditions (for mission-level success/failure metrics)

A run is marked failed if any of the following are true at **any single tick** (instantaneous, not aggregate — this models mission failure, which is triggered by the worst moment, not the average): instantaneous ATE_t exceeds 2.0 m, instantaneous drift exceeds 3.0 m, the state or covariance contains NaN/Inf, or the covariance becomes non-positive-definite. The NIS gate rejection rate is evaluated over the whole run (it's not meaningful per-tick) and fails the run if it exceeds 80%. RMSE ATE and RMSE RPE remain reported separately as aggregate accuracy summaries — they are not failure criteria. These thresholds are tuned for this toy 2D world and may be revisited once real distributions are observed.
