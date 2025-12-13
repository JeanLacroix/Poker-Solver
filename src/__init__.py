"""
Package initializer for Poker-Solver.

Exports the FastAPI app and core helpers for convenient imports, while
still keeping the modules importable directly (src.app, src.poker_solver_cli).
"""

from .app import app
from .poker_solver_cli import (
    calculate_equity,
    calculate_equity_details,
    main as cli_main,
    parse_hero,
    parse_range,
)
from .poker_solver import (
    ChooseHeroHand,
    ChosenRunout,
    ConvertHandWhenLetters,
    EquityCalculator,
    HandCategory,
    RankToNumber,
    RandomRunout,
    RandomRunoutCompleter,
    RandomRunoutVsRange,
    RandomVillain,
    SelectVillainRange,
    SetOfQuestions,
    UsualHandToComputingHandsInRange,
    WinOrLose,
)
from . import poker_solver as solver

__all__ = [
    "app",
    # CLI helpers
    "parse_hero",
    "parse_range",
    "calculate_equity",
    "calculate_equity_details",
    "cli_main",
    # Core solver functions (also available under solver.<name>)
    "ChooseHeroHand",
    "ChosenRunout",
    "ConvertHandWhenLetters",
    "EquityCalculator",
    "HandCategory",
    "RankToNumber",
    "RandomRunout",
    "RandomRunoutCompleter",
    "RandomRunoutVsRange",
    "RandomVillain",
    "SelectVillainRange",
    "SetOfQuestions",
    "UsualHandToComputingHandsInRange",
    "WinOrLose",
    # Module itself
    "solver",
]
