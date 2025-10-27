from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from poker_solver_cli import parse_hero, parse_range, calculate_equity

app = FastAPI()

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Poker Solver App</title>
<style>
  body { font-family: Arial, sans-serif; background: #f5f5f5; margin: 2rem; }
  .container { max-width: 600px; background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin: 0 auto; }
  label { display: block; margin-top: 1rem; font-weight: bold; }
  input[type="text"], input[type="number"] { width: 100%; padding: 0.5rem; margin-top: 0.25rem; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
  button { margin-top: 1rem; padding: 0.5rem 1rem; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
  button:hover { background: #0056b3; }
  .result { margin-top: 1.5rem; font-weight: bold; }
  .error { color: #c00; }
</style>
</head>
<body>
<div class="container">
<h1>Poker Solver App</h1>
<form method="get">
  <label for="hero">Hero Hand (e.g. AsKd)</label>
  <input type="text" id="hero" name="hero" value="{hero}" required>
  <label for="villain_range">Villain Range (comma-separated, e.g. AA,KK,AKs)</label>
  <input type="text" id="villain_range" name="villain_range" value="{villain}" required>
  <label for="iterations">Number of Iterations</label>
  <input type="number" id="iterations" name="iterations" value="{iterations}" min="1" required>
  <button type="submit">Calculate Equity</button>
</form>
{result}
</div>
</body>
</html>"""

@app.get("/", response_class=HTMLResponse)
async def index(hero: str = "", villain_range: str = "", iterations: int = 1000) -> str:
    hero_input = hero.strip()
    villain_input = villain_range.strip()
    result_html = ""
    if hero_input and villain_input:
        try:
            hero_cards = parse_hero(hero_input)
            villain_combos = parse_range(villain_input)
            if not villain_combos:
                raise ValueError("Villain range must expand to at least one combination.")
            eq = calculate_equity(hero_cards, villain_combos, iterations)
            result_html = f"<p class='result'>Estimated equity: {eq:.4f}</p>"
        except Exception as exc:
            result_html = f"<p class='result error'>Error: {exc}</p>"
    return HTML_TEMPLATE.format(hero=hero_input, villain=villain_input, iterations=iterations, result=result_html)
