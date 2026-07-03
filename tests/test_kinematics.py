import numpy as np

from robofusionbench.sim.kinematics import unicycle_step


def test_pure_forward_motion_moves_along_heading():
    state = np.array([0.0, 0.0, 0.0])
    next_state = unicycle_step(state, v=2.0, omega=0.0, dt=0.1)
    assert np.allclose(next_state, [0.2, 0.0, 0.0])


def test_pure_rotation_does_not_move_position():
    state = np.array([1.0, -1.0, 0.0])
    next_state = unicycle_step(state, v=0.0, omega=1.0, dt=0.1)
    assert np.allclose(next_state, [1.0, -1.0, 0.1])


def test_forward_motion_respects_heading():
    state = np.array([0.0, 0.0, np.pi / 2])
    next_state = unicycle_step(state, v=1.0, omega=0.0, dt=1.0)
    assert np.allclose(next_state, [0.0, 1.0, np.pi / 2], atol=1e-9)
