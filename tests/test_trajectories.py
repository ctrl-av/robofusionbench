import numpy as np

from robofusionbench.sim.simulate import simulate_truth


def test_line_has_zero_cross_track_error():
    """Straight-line motion has omega = 0, so heading never changes and the
    Euler integration is exact (no curvature to discretize) — cross-track
    error should be zero to floating-point precision, not just approximately
    small."""
    theta0 = 0.3  # non-trivial heading to make sure the projection is exercised
    run = simulate_truth(
        "line", duration=10.0, dt=0.01, initial_state=(0.0, 0.0, theta0), speed=1.5
    )

    cross_track = -np.sin(theta0) * (run.x - run.x[0]) + np.cos(theta0) * (run.y - run.y[0])

    assert np.max(np.abs(cross_track)) < 1e-9


def test_circle_radius_matches_v_over_omega():
    """Constant v, constant omega traces a circle of radius v / omega. Forward
    Euler integration drifts the radius outward slightly over time (it's the
    same effect as explicit-Euler energy growth for rotational dynamics), so
    we use a short duration and a loose-but-meaningful relative tolerance
    rather than requiring an exact match."""
    speed = 1.0
    radius = 2.0
    theta0 = 0.0
    omega = speed / radius

    run = simulate_truth(
        "circle", duration=10.0, dt=0.01, initial_state=(0.0, 0.0, theta0),
        speed=speed, radius=radius,
    )

    # Analytic circle center for CCW motion (omega > 0): 90 degrees to the
    # left of the initial heading, distance `radius` away.
    cx = run.x[0] - radius * np.sin(theta0)
    cy = run.y[0] + radius * np.cos(theta0)

    dist_from_center = np.sqrt((run.x - cx) ** 2 + (run.y - cy) ** 2)

    assert np.allclose(dist_from_center, radius, rtol=0.03)
    # Sanity check the omega bookkeeping itself.
    assert np.allclose(run.omega_cmd, omega)


def test_figure_eight_heading_is_periodic():
    """omega(t) = amplitude * sin(2*pi*frequency*t) integrates to exactly
    zero over one full period (sum_{k=0}^{n-1} sin(2*pi*k/n) == 0 exactly for
    integer n), so heading must return to its starting value after exactly
    one period, up to floating-point rounding only."""
    frequency = 0.1
    period = 1.0 / frequency  # 10.0 s

    run = simulate_truth(
        "figure_eight", duration=period, dt=0.01, initial_state=(0.0, 0.0, 0.7),
        speed=1.0, omega_amplitude=1.0, frequency=frequency,
    )

    assert np.isclose(run.theta[-1], run.theta[0], atol=1e-9)
    # And it isn't trivially periodic because omega was always zero.
    assert np.max(np.abs(run.omega_cmd)) > 0.5


def test_unknown_trajectory_raises():
    import pytest

    with pytest.raises(ValueError):
        simulate_truth("spiral", duration=1.0, dt=0.01)
