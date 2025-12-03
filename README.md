# Poker Solver (Equity Calculator)

Minimal, fast equity calculator. Enter a hero hand and a villain range, run
Monte Carlo simulations, and get an equity estimate.

- Web app (FastAPI + Uvicorn) with an interactive hero/villain selector and charts
- CLI tool for quick terminal checks or scripting
- Optional timing/plotting helpers for experimentation

> This is an equity calculator, not a full GTO solver.

---

## Setup

```bash
git clone https://github.com/JeanLacroix/Poker-Solver.git
cd Poker-Solver
python -m venv .venv
.\.venv\Scripts\activate  # or: source .venv/bin/activate
pip install -r requirements.txt
```

## Run the web app

```bash
uvicorn src.app:app --reload --reload-dir src
```

Open http://127.0.0.1:8000 and use the UI to pick a hero hand, choose a villain
range (all combos or a custom matrix), optionally lock a runout, and run a Monte
Carlo simulation.

### API endpoint

`POST /api/equity` expects JSON:

```json
{
  "hero": "AsKd",
  "villain_range": "AA,KK,AKs",
  "iterations": 2000,
  "villain_mode": "range",
  "runout_mode": "all",
  "runout": ["As", "Kd", "Qc", "Jh", "2s"]
}
```

Use `villain_mode: "range"` to restrict to the provided combos or `all` to expand
to every possible two-card combo excluding the hero cards. Set `runout_mode` to
`specified` (with 3-5 cards in `runout`) to lock the board, otherwise `all`
generates random runouts.

Returns equity plus win/draw ratios and distributions for charting.

## CLI usage

```bash
python -m src.poker_solver_cli --hero AsKd --villain_range "AA,KK,AKs" --iterations 5000
```

Outputs the estimated equity for the supplied hero hand versus the expanded
villain range.

## Optional timing/plotting helpers

`time_analysis.py` contains small experiments for runtime exploration. It uses
matplotlib to show plots:

```bash
python time_analysis.py --mode range-size     # or: iterations, combined
```
