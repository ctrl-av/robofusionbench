"""Odometry sensor: good locally, drifts over time via a slow bias random walk.

Callers pass an explicit numpy.random.Generator rather than a global seed —
sweeps run many seeds per config (see docs/experiment_plan.md), and global
RNG state doesn't compose across that without silently breaking
reproducibility.
"""

from dataclasses import dataclass

import numpy as np


@dataclass
class OdometryMeasurement:
    measured_v: np.ndarray
    measured_omega: np.ndarray
    bias_v: np.ndarray
    bias_omega: np.ndarray


def simulate_odometry(
    v_true: np.ndarray,
    omega_true: np.ndarray,
    dt: float,
    rng: np.random.Generator,
    noise_std_v: float = 0.02,
    noise_std_omega: float = 0.02,
    bias_walk_std_v: float = 0.005,
    bias_walk_std_omega: float = 0.005,
    initial_bias: tuple[float, float] = (0.0, 0.0),
) -> OdometryMeasurement:
    """measured = true + slowly-drifting bias + per-tick Gaussian noise.

    The bias is a discretized Wiener process: each step's increment is drawn
    with std = bias_walk_std * sqrt(dt), which is what makes the random walk's
    variance scale correctly with elapsed time regardless of dt.
    """
    n = len(v_true)
    bias_v = initial_bias[0] + np.cumsum(rng.normal(0.0, bias_walk_std_v * np.sqrt(dt), size=n))
    bias_omega = initial_bias[1] + np.cumsum(rng.normal(0.0, bias_walk_std_omega * np.sqrt(dt), size=n))

    measured_v = v_true + bias_v + rng.normal(0.0, noise_std_v, size=n)
    measured_omega = omega_true + bias_omega + rng.normal(0.0, noise_std_omega, size=n)

    return OdometryMeasurement(
        measured_v=measured_v,
        measured_omega=measured_omega,
        bias_v=bias_v,
        bias_omega=bias_omega,
    )
