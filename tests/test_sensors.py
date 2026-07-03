import numpy as np

from robofusionbench.sensors.absolute_position import simulate_absolute_position
from robofusionbench.sensors.odometry import simulate_odometry


def test_absolute_position_noise_matches_configured_statistics():
    rng = np.random.default_rng(0)
    n = 20_000
    x_true = np.zeros(n)
    y_true = np.zeros(n)
    noise_std_x, noise_std_y = 0.1, 0.2

    meas = simulate_absolute_position(x_true, y_true, rng, noise_std_x=noise_std_x, noise_std_y=noise_std_y)

    assert abs(np.mean(meas.measured_x)) < 0.01
    assert abs(np.mean(meas.measured_y)) < 0.01
    assert np.isclose(np.std(meas.measured_x), noise_std_x, rtol=0.05)
    assert np.isclose(np.std(meas.measured_y), noise_std_y, rtol=0.05)


def test_odometry_noise_matches_configured_statistics_when_bias_is_disabled():
    rng = np.random.default_rng(1)
    n = 20_000
    v_true = np.full(n, 1.0)
    omega_true = np.zeros(n)
    noise_std_v = 0.05

    meas = simulate_odometry(
        v_true, omega_true, dt=0.01, rng=rng,
        noise_std_v=noise_std_v, noise_std_omega=0.05,
        bias_walk_std_v=0.0, bias_walk_std_omega=0.0,
    )

    assert np.allclose(meas.bias_v, 0.0)
    residual = meas.measured_v - v_true
    assert abs(np.mean(residual)) < 0.01
    assert np.isclose(np.std(residual), noise_std_v, rtol=0.05)


def test_odometry_bias_random_walk_variance_grows_with_time():
    """A Wiener process has Var[bias(t)] proportional to t. Check that the
    variance across many independent realizations at a late tick is
    substantially larger than at an early tick, roughly matching the time
    ratio (with a generous margin for Monte Carlo noise at this sample
    count)."""
    n = 2000
    early, late = 500, 1999
    dt = 0.01
    bias_walk_std = 0.1
    num_seeds = 200

    v_true = np.zeros(n)
    omega_true = np.zeros(n)

    early_biases = []
    late_biases = []
    for seed in range(num_seeds):
        rng = np.random.default_rng(seed)
        meas = simulate_odometry(
            v_true, omega_true, dt=dt, rng=rng,
            noise_std_v=0.0, noise_std_omega=0.0,
            bias_walk_std_v=bias_walk_std, bias_walk_std_omega=0.0,
        )
        early_biases.append(meas.bias_v[early])
        late_biases.append(meas.bias_v[late])

    var_early = np.var(early_biases)
    var_late = np.var(late_biases)

    expected_ratio = (late + 1) / (early + 1)  # ticks elapsed, ~= time ratio
    assert var_late > var_early * (expected_ratio / 2)  # generous margin
