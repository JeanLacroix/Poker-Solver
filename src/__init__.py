"""
Package initializer for Poker-Solver.

Exports the FastAPI app and core helpers for convenient imports, while
still keeping the modules importable directly (src.app, src.poker_solver_cli).
"""

from .app import app
from .poker_solver_cli import (
    parse_hero,
    parse_range,
    calculate_equity,
    calculate_equity_details,
)
from . import poker_solver as solver

__all__ = [
    "app",
    "parse_hero",
    "parse_range",
    "calculate_equity",
    "calculate_equity_details",
    "solver",
]
