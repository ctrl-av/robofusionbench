"""Trajectory generators: each produces (v_cmd, omega_cmd) command arrays.

Commands are deterministic — no controller, no feedback from the estimate.
Each generator returns arrays of length N = round(duration / dt), one
command pair per simulation tick.
"""

import numpy as np


def _num_ticks(duration: float, dt: float) -> int:
    return round(duration / dt)


def line_commands(duration: float, dt: float, speed: float = 1.0):
    """Straight line at constant speed: omega = 0 always."""
    n = _num_ticks(duration, dt)
    return np.full(n, speed), np.zeros(n)


def circle_commands(duration: float, dt: float, speed: float = 1.0, radius: float = 2.0):
    """Constant-radius circle: omega = speed / radius, held constant.

    Positive radius/speed gives counterclockwise motion (omega > 0).
    """
    n = _num_ticks(duration, dt)
    omega = speed / radius
    return np.full(n, speed), np.full(n, omega)


def figure_eight_commands(
    duration: float,
    dt: float,
    speed: float = 1.0,
    omega_amplitude: float = 1.5,
    frequency: float = 0.1,
):
    """Two connected loops: omega(t) = omega_amplitude * sin(2*pi*frequency*t).

    Curvature alternates sign, tracing a lemniscate-like path. Heading
    returns exactly to its starting value after every full period
    T = 1 / frequency, since sin integrates to zero over a full period —
    that periodicity is the trajectory's one exact analytic invariant.
    """
    n = _num_ticks(duration, dt)
    t = np.arange(n) * dt
    omega = omega_amplitude * np.sin(2 * np.pi * frequency * t)
    return np.full(n, speed), omega


TRAJECTORIES = {
    "line": line_commands,
    "circle": circle_commands,
    "figure_eight": figure_eight_commands,
}


def generate_commands(name: str, duration: float, dt: float, **kwargs):
    if name not in TRAJECTORIES:
        raise ValueError(f"Unknown trajectory '{name}'. Known: {sorted(TRAJECTORIES)}")
    return TRAJECTORIES[name](duration, dt, **kwargs)
