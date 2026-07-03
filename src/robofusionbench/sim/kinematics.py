"""Pure unicycle kinematics — no state, no I/O, no randomness."""

import numpy as np


def unicycle_step(state: np.ndarray, v: float, omega: float, dt: float) -> np.ndarray:
    """Advance a [x, y, theta] state by one forward-Euler step.

    Heading is left unwrapped; wrapping is a concern for angle differences
    (metrics, EKF innovation), not for the raw kinematic integration here.
    """
    x, y, theta = state
    return np.array(
        [
            x + v * np.cos(theta) * dt,
            y + v * np.sin(theta) * dt,
            theta + omega * dt,
        ]
    )
