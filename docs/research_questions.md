# Research Questions

These three questions are the spine of the project. Every experiment should trace back to one of them.

## RQ1 — Latency and jitter

**How much EKF compute latency and timing jitter can a localization pipeline tolerate before ATE, RPE, drift, or NIS gate rejection degrade significantly?**

Hardware knobs: EKF predict latency, EKF update latency, random timing jitter, deadline length, CPU frequency, update rate.

Estimator outcomes: ATE, RPE, max drift, missed-update count, stale-update count, NIS gate rejection rate.

Working hypothesis: occasional missed updates are likely more damaging to localization accuracy than the average latency alone would suggest — tail behavior, not mean behavior, may be the thing that matters.

## RQ2 — Numeric precision

**How much numeric precision can be reduced before covariance behavior, NIS gating, and localization accuracy become unstable?**

Hardware knobs: float64, float32, fixed-point-like Q24.8 / Q16.16 / Q12.20, mixed precision, quantized matrix operations.

Estimator outcomes: ATE, RPE, covariance sanity (trace, determinant, positive-definiteness), NIS distribution, false-reject rate, false-accept rate, divergence count.

Working hypothesis: lower precision reduces compute cost but can increase estimator instability, particularly through the covariance update and the NIS gate's dependence on inverting a small, potentially ill-conditioned matrix.

## RQ3 — Acceleration

**Which architecture gives the best robot-level outcome: CPU-only, CPU plus matrix accelerator, vector-style accelerator, or specialized EKF accelerator?**

Hardware configurations: CPU-only float, CPU-only fixed-point, CPU + matrix-multiply accelerator, CPU + NIS accelerator, CPU + full EKF-update accelerator, a hypothetical vector unit.

Outcomes: latency, energy proxy, ATE, RPE, missed-deadline rate, accuracy-per-energy, accuracy-per-area proxy.

Working hypothesis: the architecture with the best isolated kernel speedup will not necessarily produce the best localization accuracy, if it introduces precision loss, scheduling overhead, or a bottleneck in the part of the pipeline it doesn't accelerate.

## Why these three, and not others

Each question isolates one axis of the hardware/estimator interaction (timing, numerics, architecture choice) so results can be attributed to a single cause. Cross-cutting questions (e.g., outlier robustness under low precision) are legitimate follow-ups once RQ1-RQ3 have baseline answers, not a substitute for them.
