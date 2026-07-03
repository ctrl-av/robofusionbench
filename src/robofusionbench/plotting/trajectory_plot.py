"""Plot 1: truth trajectory visual sanity check."""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from robofusionbench.sim.simulate import TruthRun, simulate_truth


def plot_truth_trajectory(run: TruthRun, title: str | None = None, save_path: str | Path | None = None):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(run.x, run.y, linewidth=1.5)
    ax.plot(run.x[0], run.y[0], marker="o", color="green", label="start")
    ax.plot(run.x[-1], run.y[-1], marker="x", color="red", label="end")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_aspect("equal", adjustable="datalim")
    ax.legend()
    if title:
        ax.set_title(title)
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150)
    return fig


def main():
    parser = argparse.ArgumentParser(description="Plot a truth trajectory for a visual sanity check.")
    parser.add_argument("--trajectory", default="figure_eight", choices=["line", "circle", "figure_eight"])
    parser.add_argument("--duration", type=float, default=10.0)
    parser.add_argument("--dt", type=float, default=0.01)
    parser.add_argument("--out", default="results/plots/trajectory_demo.png")
    args = parser.parse_args()

    run = simulate_truth(args.trajectory, args.duration, args.dt)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plot_truth_trajectory(run, title=f"Truth trajectory: {args.trajectory}", save_path=out_path)
    print(f"Saved plot to {out_path}")


if __name__ == "__main__":
    main()
