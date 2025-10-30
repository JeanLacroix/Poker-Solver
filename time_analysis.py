"""
Timing analysis tools for the poker solver.

This module isolates runtime/plotting experiments so they can be run on demand
without affecting application imports. Nothing executes on import.
"""

from __future__ import annotations

import argparse
import timeit
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (required for 3D projection)


def simulate_villain_range(size: int) -> list[str]:
    return [f"Hand{i}" for i in range(size)]


def equity_calculator(flattened_range: list[str], num_iterations: int) -> list[str]:
    # Placeholder for actual calculation: iterates over range and iterations
    results: list[str] = []
    for _ in range(num_iterations):
        for hand in flattened_range:
            results.append(hand)
    return results


def time_equity_calculator(flattened_range_size: int, num_iterations: int) -> tuple[float, float]:
    setup_code = (
        "from __main__ import equity_calculator, simulate_villain_range; "
        f"flattened_range=simulate_villain_range({flattened_range_size})"
    )
    stmt = f"equity_calculator(flattened_range, {num_iterations})"
    times = timeit.repeat(stmt=stmt, setup=setup_code, repeat=5, number=1)
    return float(np.mean(times)), float(np.std(times))


def analyze_by_range_size() -> None:
    range_sizes = [10, 50, 100, 200, 500, 1000]
    num_iterations = 100
    mean_times: list[float] = []
    std_devs: list[float] = []

    for size in range_sizes:
        mean_time, std_dev = time_equity_calculator(size, num_iterations)
        mean_times.append(mean_time)
        std_devs.append(std_dev)

    plt.figure(figsize=(8, 6))
    plt.errorbar(range_sizes, mean_times, yerr=std_devs, fmt='-o', capsize=5, label='Runtime')
    plt.title("Runtime vs Flattened Range Size (100 iterations)")
    plt.xlabel("Flattened Range Size")
    plt.ylabel("Execution Time (seconds)")
    plt.grid(True)
    plt.legend()
    plt.show()


def analyze_by_iterations() -> None:
    range_size = 100
    iteration_counts = [10, 50, 100, 500, 1000, 5000]
    mean_times: list[float] = []
    std_devs: list[float] = []

    for iterations in iteration_counts:
        mean_time, std_dev = time_equity_calculator(range_size, iterations)
        mean_times.append(mean_time)
        std_devs.append(std_dev)

    plt.figure(figsize=(8, 6))
    plt.errorbar(iteration_counts, mean_times, yerr=std_devs, fmt='-o', capsize=5, label='Runtime')
    plt.title("Runtime vs Number of Iterations")
    plt.xlabel("Number of Iterations")
    plt.ylabel("Execution Time (seconds)")
    plt.grid(True)
    plt.legend()
    plt.show()


def analyze_combined() -> None:
    range_sizes = [10, 50, 100, 200, 500]
    iteration_counts = [10, 50, 100, 500, 1000]
    runtimes = np.zeros((len(range_sizes), len(iteration_counts)))

    for i, size in enumerate(range_sizes):
        for j, iterations in enumerate(iteration_counts):
            mean_time, _ = time_equity_calculator(size, iterations)
            runtimes[i, j] = mean_time

    X, Y = np.meshgrid(iteration_counts, range_sizes)
    Z = runtimes

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, Z, cmap="viridis")
    ax.set_title("Runtime as a Function of Flattened Range Size and Iterations")
    ax.set_xlabel("Number of Iterations")
    ax.set_ylabel("Flattened Range Size")
    ax.set_zlabel("Execution Time (seconds)")
    plt.show()

    plt.figure(figsize=(8, 6))
    plt.imshow(
        runtimes,
        cmap="viridis",
        aspect="auto",
        origin="lower",
        extent=[min(iteration_counts), max(iteration_counts), min(range_sizes), max(range_sizes)],
    )
    plt.colorbar(label="Execution Time (seconds)")
    plt.title("Heatmap: Runtime vs Flattened Range Size and Iterations")
    plt.xlabel("Number of Iterations")
    plt.ylabel("Flattened Range Size")
    plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run timing analysis on equity loop placeholders.")
    parser.add_argument(
        "--mode",
        choices=["range-size", "iterations", "combined"],
        default="range-size",
        help="Which analysis to run",
    )
    args = parser.parse_args()

    if args.mode == "range-size":
        analyze_by_range_size()
    elif args.mode == "iterations":
        analyze_by_iterations()
    else:
        analyze_combined()


if __name__ == "__main__":
    main()

