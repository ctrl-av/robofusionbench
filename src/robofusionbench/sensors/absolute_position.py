"""Absolute-position sensor: noisier per tick than odometry, but non-drifting.

This models the correction input generically (camera-like / GPS-like /
beacon — deliberately unspecified, per the clean-room boundary). It produces
a per-tick noisy measurement unconditionally; deciding *which* ticks the EKF
actually gets to see (the 10 Hz-style update rate, and later, missed
deadlines) is a scheduling concern that belongs to the simulation loop and
hardware model, not to the sensor itself.
"""

from dataclasses import dataclass

import numpy as np


@dataclass
class AbsolutePositionMeasurement:
    measured_x: np.ndarray
    measured_y: np.ndarray


def simulate_absolute_position(
    x_true: np.ndarray,
    y_true: np.ndarray,
    rng: np.random.Generator,
    noise_std_x: float = 0.1,
    noise_std_y: float = 0.1,
) -> AbsolutePositionMeasurement:
    n = len(x_true)
    measured_x = x_true + rng.normal(0.0, noise_std_x, size=n)
    measured_y = y_true + rng.normal(0.0, noise_std_y, size=n)
    return AbsolutePositionMeasurement(measured_x=measured_x, measured_y=measured_y)
