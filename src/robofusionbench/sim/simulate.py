"""Truth simulation loop: commands -> integrated ground-truth trajectory."""

from dataclasses import dataclass

import numpy as np

from robofusionbench.sim.kinematics import unicycle_step
from robofusionbench.sim.trajectories import generate_commands


@dataclass
class TruthRun:
    time: np.ndarray
    x: np.ndarray
    y: np.ndarray
    theta: np.ndarray
    v_cmd: np.ndarray
    omega_cmd: np.ndarray


def simulate_truth(
    trajectory: str,
    duration: float,
    dt: float,
    initial_state=(0.0, 0.0, 0.0),
    **traj_kwargs,
) -> TruthRun:
    """Integrate a trajectory's commands through unicycle kinematics.

    Returns N+1 states (including the initial state) for N command ticks.
    """
    v_cmd, omega_cmd = generate_commands(trajectory, duration, dt, **traj_kwargs)
    n = len(v_cmd)

    x = np.empty(n + 1)
    y = np.empty(n + 1)
    theta = np.empty(n + 1)
    x[0], y[0], theta[0] = initial_state

    state = np.array(initial_state, dtype=float)
    for k in range(n):
        state = unicycle_step(state, v_cmd[k], omega_cmd[k], dt)
        x[k + 1], y[k + 1], theta[k + 1] = state

    time = np.arange(n + 1) * dt
    return TruthRun(time=time, x=x, y=y, theta=theta, v_cmd=v_cmd, omega_cmd=omega_cmd)
