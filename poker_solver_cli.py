#!/usr/bin/env python3
# coding: utf-8

"""
A simple command‑line interface for the poker equity calculator.

This script uses core functions from ``poker_solver.py`` to estimate the
equity of a given hero hand against a specified villain hand range.  It
avoids graphical interfaces (such as Tkinter) entirely so that it can be
run in headless environments like terminals or continuous integration
servers.  The hero hand must be supplied as exactly four characters
representing two cards (e.g. ``AsKd`` for ace of spades and king of
diamonds).  The villain range is a comma‑separated list of hand
descriptors in standard shorthand (e.g. ``AA,KK,AKs``).  You can also
specify how many Monte Carlo simulations to run using ``--iterations``.

Example usage::

    python3 poker_solver_cli.py --hero AsKd --villain_range "AA,KK,AKs" --iterations 5000

This will estimate the hero equity of AsKd versus a range consisting of
pocket aces, pocket kings and suited ace‑king over 5000 random deals.
"""

import argparse
import random
from typing import List

import poker_solver as ps


def parse_hero(hero_str: str) -> List[str]:
    """Convert a hero string like 'AsKd' into the computing representation.

    The input string should contain exactly four characters: rank and suit
    for the first card followed by rank and suit for the second card.  Ranks
    may be denoted by A, K, Q, J, T or digits 9–2.  Suits should be one
    of ``s`` (spades), ``c`` (clubs), ``h`` (hearts) or ``d`` (diamonds).

    Returns a list of two strings suitable for passing to
    ``ConvertHandWhenLetters``.
    """
    s = hero_str.replace(" ", "").strip()
    if len(s) != 4:
        raise ValueError(
            f"Hero hand '{hero_str}' must contain exactly two cards e.g. 'AsKd'"
        )
    card1 = s[:2]
    card2 = s[2:]
    return ps.ConvertHandWhenLetters([card1, card2])


def parse_range(range_str: str) -> List[List[str]]:
    """Parse a comma‑separated range string into a list of concrete combos.

    ``range_str`` should be a comma‑separated list of shorthand hand
    descriptors such as ``AA``, ``AKs``, ``QJo``.  Each descriptor is
    expanded into all specific two‑card combinations using
    ``UsualHandToComputingHandsInRange`` and concatenated into one list.
    """
    parts = [part.strip().upper() for part in range_str.split(',') if part.strip()]
    combos: List[List[str]] = []
    for descriptor in parts:
        combos.extend(ps.UsualHandToComputingHandsInRange(descriptor))
    return combos


def calculate_equity(hero: List[str], villain_combos: List[List[str]], iterations: int) -> float:
    """Estimate equity by Monte Carlo simulation.

    A random villain hand is sampled from ``villain_combos`` on each
    iteration, a random runout is generated and the resulting showdown is
    classified using ``WinOrLose``.  The function returns the proportion of
    hero wins plus half the proportion of ties over the total number of
    simulations.
    """
    win = draw = lose = 0
    for _ in range(iterations):
        villain = random.choice(villain_combos)
        runout = ps.RandomRunout(hero, villain)
        result = ps.WinOrLose(hero, villain, runout)
        if result == "win":
            win += 1
        elif result == "draw":
            draw += 1
        else:
            lose += 1
    return (win + 0.5 * draw) / iterations


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Estimate equity of a hero hand versus a villain range using Monte Carlo simulation."
        )
    )
    parser.add_argument(
        "--hero",
        required=True,
        help="Hero cards (e.g. AsKd for ace of spades and king of diamonds)",
    )
    parser.add_argument(
        "--villain_range",
        required=True,
        help=(
            "Villain hand range as a comma‑separated list of descriptors "
            "(e.g. 'AA,KK,AKs'). Each descriptor will be expanded into "
            "all specific two‑card combinations."
        ),
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=1000,
        help="Number of random deals to simulate (default: 1000)",
    )
    args = parser.parse_args()

    try:
        hero = parse_hero(args.hero)
    except ValueError as exc:
        parser.error(str(exc))
    villain_combos = parse_range(args.villain_range)
    if not villain_combos:
        parser.error("Villain range must expand to at least one combination.")

    eq = calculate_equity(hero, villain_combos, args.iterations)
    hero_readable = args.hero.upper()
    print(
        f"Estimated equity for hero hand {hero_readable} against range {args.villain_range}: {eq:.4f}"
    )


if __name__ == "__main__":
    main()