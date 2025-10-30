import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from poker_solver_cli import (
    parse_hero,
    parse_range,
    calculate_equity,
    calculate_equity_details,
)
import poker_solver as ps

app = FastAPI()

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Poker Solver App</title>
<style>
  body { font-family: Arial, sans-serif; background: #f5f5f5; margin: 2rem; }
  .container { max-width: 900px; background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin: 0 auto; }
  label { display: block; margin-top: 1rem; font-weight: bold; }
  input[type="text"], input[type="number"] { width: 100%; padding: 0.5rem; margin-top: 0.25rem; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
  button { margin-top: 1rem; padding: 0.5rem 1rem; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
  button:hover { background: #0056b3; }
  .result { margin-top: 1.5rem; font-weight: bold; }
  .error { color: #c00; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
  .charts { margin-top: 1.5rem; }
  canvas { background: #fafafa; border: 1px solid #eee; border-radius: 4px; padding: 0.5rem; }
  .toggle-group { margin-top: 0.5rem; display:flex; gap:0.75rem; align-items:center; flex-wrap: wrap; }
  .matrix { border-collapse: collapse; }
  .matrix td { border: 1px solid #ddd; padding: 4px; text-align:center; cursor: pointer; font-size: 12px; }
  .matrix td.sel { background:#2e7d32; color:#fff; }
  .card-grid { display:grid; grid-template-columns: repeat(13, 1fr); gap:4px; }
  .card { padding:6px 4px; border:1px solid #ddd; background:#eee; cursor:pointer; text-align:center; font-size:12px; }
  .card.sel { background:#2e7d32; color:#fff; }
  .pill { padding: 2px 8px; border:1px solid #aaa; border-radius: 999px; cursor: pointer; }
  .pill.active { background:#007bff; color:#fff; border-color:#007bff; }
</style>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
<div class="container">
<h1>Poker Solver App</h1>
<form id="equity-form" method="get">
  <label>Hero Cards</label>
  <div class="toggle-group" style="margin-bottom:0.25rem; color:#666;">
    Select exactly two cards below. Current: <span id="heroDisplay">{hero}</span>
  </div>
  <div id="heroGrid" class="card-grid"></div>
  <input type="hidden" id="hero" name="hero" value="{hero}" required>

  <label>Villain Range</label>
  <div class="toggle-group">
    <span class="pill active" id="villainAll">All possible hands</span>
    <span class="pill" id="villainRange">Use range matrix</span>
  </div>
  <div id="rangeMatrixWrapper" style="margin-top:0.5rem; display:none;"></div>
  <input type="text" id="villain_range" name="villain_range" value="{villain}" placeholder="AA,KK,AKs" style="display:none;">

  <label>Runout</label>
  <div class="toggle-group">
    <span class="pill active" id="runoutAll">All possible runouts</span>
    <span class="pill" id="runoutSpecified">Specified runout</span>
  </div>
  <div id="runoutGridWrapper" style="display:none; margin-top:0.5rem;"></div>

  <label for="iterations">Number of Iterations</label>
  <input type="number" id="iterations" name="iterations" value="{iterations}" min="1" required>
  <button type="submit">Calculate Equity</button>
  <span id="status" style="margin-left:1rem;"></span>
</form>
<div id="result">{result}</div>

<div class="charts">
  <div class="grid">
    <div>
      <h3>Hero Made-Hand Distribution</h3>
      <canvas id="madeChart" width="400" height="300"></canvas>
    </div>
    <div>
      <h3>Won With Distribution</h3>
      <canvas id="wonChart" width="400" height="300"></canvas>
    </div>
  </div>
  <div style="margin-top:1rem;">
    <h3>Lost To Distribution</h3>
    <canvas id="lostChart" width="820" height="300"></canvas>
  </div>
  <div style="margin-top:1rem;">
    <h3>Sample Runouts</h3>
    <ul id="examples"></ul>
  </div>
  <div style="margin-top:0.5rem; color:#555;" id="comboCount"></div>
</div>

<script>
const form = document.getElementById('equity-form');
const statusEl = document.getElementById('status');
const resultEl = document.getElementById('result');
const examplesEl = document.getElementById('examples');
const comboEl = document.getElementById('comboCount');
let madeChart, wonChart, lostChart;
// Suits and ranks for grids
const ranks = ['A','K','Q','J','T','9','8','7','6','5','4','3','2'];
const suits = ['s','c','h','d'];

// Build hero card grid
const heroGrid = document.getElementById('heroGrid');
const heroHidden = document.getElementById('hero');
const heroDisplay = document.getElementById('heroDisplay');
let heroSel = [];
function renderHeroGrid() {
  heroGrid.innerHTML = '';
  suits.forEach(s => {
    ranks.forEach(r => {
      const card = r + s;
      const div = document.createElement('div');
      div.className = 'card' + (heroSel.includes(card) ? ' sel' : '');
      div.textContent = card;
      div.onclick = () => {
        const idx = heroSel.indexOf(card);
        if (idx >= 0) {
          heroSel.splice(idx,1);
        } else if (heroSel.length < 2) {
          heroSel.push(card);
        }
        // enforce max 2
        if (heroSel.length > 2) heroSel = heroSel.slice(0,2);
        heroHidden.value = heroSel.join('');
        heroDisplay.textContent = heroHidden.value || '(none)';
        renderHeroGrid();
      };
      heroGrid.appendChild(div);
    });
  });
}
// Initialize hero selection from prefilled value if any
(function initHeroFromValue(){
  const v = (heroHidden.value||'').trim();
  if (v.length === 4) heroSel = [v.slice(0,2), v.slice(2)];
})();
renderHeroGrid();

// Villain range matrix (13x13)
const villainAllPill = document.getElementById('villainAll');
const villainRangePill = document.getElementById('villainRange');
const rangeMatrixWrapper = document.getElementById('rangeMatrixWrapper');
const villainRangeInput = document.getElementById('villain_range');
let rangeSel = new Set();
function handLabel(i,j){
  const r1 = ranks[i];
  const r2 = ranks[j];
  if (i === j) return r1 + r2; // pairs
  return (i < j) ? (r1 + r2 + 's') : (r2 + r1 + 'o');
}
function renderRangeMatrix(){
  const table = document.createElement('table');
  table.className = 'matrix';
  for (let i=0;i<13;i++){
    const tr = document.createElement('tr');
    for (let j=0;j<13;j++){
      const td = document.createElement('td');
      const label = handLabel(i,j);
      td.textContent = label;
      if (rangeSel.has(label)) td.classList.add('sel');
      td.onclick = () => {
        if (rangeSel.has(label)) rangeSel.delete(label); else rangeSel.add(label);
        renderRangeMatrix();
      };
      tr.appendChild(td);
    }
    table.appendChild(tr);
  }
  rangeMatrixWrapper.innerHTML = '';
  rangeMatrixWrapper.appendChild(table);
  villainRangeInput.value = Array.from(rangeSel).join(',');
}
renderRangeMatrix();
function setVillainMode(mode){
  if (mode === 'all'){
    villainAllPill.classList.add('active');
    villainRangePill.classList.remove('active');
    rangeMatrixWrapper.style.display = 'none';
    villainRangeInput.style.display = 'none';
  } else {
    villainAllPill.classList.remove('active');
    villainRangePill.classList.add('active');
    rangeMatrixWrapper.style.display = '';
    villainRangeInput.style.display = '';
  }
}
villainAllPill.onclick = () => setVillainMode('all');
villainRangePill.onclick = () => setVillainMode('range');
setVillainMode('all');

// Runout selection grid
const runoutAllPill = document.getElementById('runoutAll');
const runoutSpecPill = document.getElementById('runoutSpecified');
const runoutGridWrapper = document.getElementById('runoutGridWrapper');
let runoutSel = [];
function renderRunoutGrid(){
  const grid = document.createElement('div');
  grid.className = 'card-grid';
  suits.forEach(s => {
    ranks.forEach(r => {
      const card = r + s;
      const div = document.createElement('div');
      div.className = 'card' + (runoutSel.includes(card) ? ' sel' : '');
      div.textContent = card;
      div.onclick = () => {
        const idx = runoutSel.indexOf(card);
        if (idx >= 0) runoutSel.splice(idx,1);
        else if (runoutSel.length < 5) runoutSel.push(card);
        renderRunoutGrid();
      };
      // disable hero cards
      if (heroSel.includes(card)) div.style.opacity = 0.5, div.style.pointerEvents='none';
      grid.appendChild(div);
    });
  });
  runoutGridWrapper.innerHTML = '';
  const info = document.createElement('div');
  info.style.marginBottom = '0.25rem';
  info.textContent = 'Select 3 to 5 community cards (flop/turn/river order not enforced). Selected: ' + runoutSel.join(' ');
  runoutGridWrapper.appendChild(info);
  runoutGridWrapper.appendChild(grid);
}
function setRunoutMode(mode){
  if (mode === 'all'){
    runoutAllPill.classList.add('active');
    runoutSpecPill.classList.remove('active');
    runoutGridWrapper.style.display = 'none';
  } else {
    runoutAllPill.classList.remove('active');
    runoutSpecPill.classList.add('active');
    runoutGridWrapper.style.display = '';
    renderRunoutGrid();
  }
}
runoutAllPill.onclick = () => setRunoutMode('all');
runoutSpecPill.onclick = () => setRunoutMode('specified');
setRunoutMode('all');

function renderBarChart(ctx, dataMap, title) {
  const labels = Object.keys(dataMap);
  const data = labels.map(k => dataMap[k]);
  return new Chart(ctx, {
    type: 'bar',
    data: { labels, datasets: [{ label: title, data, backgroundColor: '#4e79a7' }] },
    options: { responsive: true, scales: { y: { beginAtZero: true, ticks: { callback: v => (v*100).toFixed(1)+'%' } } }, plugins: { legend: { display:false } } }
  });
}

function updateCharts(res) {
  const made = res.made_distribution || {}; 
  const won = res.won_with_distribution || {};
  const lost = res.lost_to_distribution || {};
  if (madeChart) madeChart.destroy();
  if (wonChart) wonChart.destroy();
  if (lostChart) lostChart.destroy();
  madeChart = renderBarChart(document.getElementById('madeChart'), made, 'Made-Hand');
  wonChart = renderBarChart(document.getElementById('wonChart'), won, 'Won With');
  lostChart = renderBarChart(document.getElementById('lostChart'), lost, 'Lost To');
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const hero = document.getElementById('hero').value.trim();
  const villain_mode = villainRangePill.classList.contains('active') ? 'range' : 'all';
  const villain_range = document.getElementById('villain_range').value.trim();
  const runout_mode = runoutSpecPill.classList.contains('active') ? 'specified' : 'all';
  const runout = runoutSel.slice();
  const iterations = parseInt(document.getElementById('iterations').value, 10) || 1000;
  if (!hero) return;
  if (villain_mode === 'range' && !villain_range) return;
  if (runout_mode === 'specified' && runout.length < 3) { alert('Select at least 3 community cards.'); return; }
  statusEl.textContent = 'Running...';
  resultEl.innerHTML = '';
  examplesEl.innerHTML = '';
  comboEl.textContent = '';
  try {
    const resp = await fetch('/api/equity', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ hero, villain_range, iterations, villain_mode, runout_mode, runout }) });
    if (!resp.ok) {
      const text = await resp.text();
      throw new Error(text || ('HTTP '+resp.status));
    }
    const res = await resp.json();
    const eq = (res.equity ?? 0).toFixed(4);
    const win = ((res.win_ratio ?? 0)*100).toFixed(2);
    const drw = ((res.draw_ratio ?? 0)*100).toFixed(2);
    resultEl.innerHTML = `<p class='result'>Estimated equity: ${eq} (Win ${win}%, Draw ${drw}%)</p>`;
    updateCharts(res);
    if (Array.isArray(res.examples)) {
      res.examples.forEach(ex => {
        const li = document.createElement('li');
        li.textContent = `Runout ${ex.runout.join(' ')} | Villain ${ex.villain.join(', ')} | Hero ${ex.hero_hand} vs Villain ${ex.villain_hand} => ${ex.result}`;
        examplesEl.appendChild(li);
      });
    }
    if (typeof res.combo_count === 'number') {
      comboEl.textContent = `Expanded villain range to ${res.combo_count} combos.`;
    }
  } catch (err) {
    resultEl.innerHTML = `<p class='result error'>Error: ${err}</p>`;
  } finally {
    statusEl.textContent = '';
  }
});
</script>
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
    return (
        HTML_TEMPLATE
        .replace("{hero}", hero_input)
        .replace("{villain}", villain_input)
        .replace("{iterations}", str(iterations))
        .replace("{result}", result_html)
    )


class EquityRequest(BaseModel):
    hero: str
    villain_range: str
    iterations: int = 1000
    villain_mode: str | None = None  # 'all' or 'range'
    runout_mode: str | None = None   # 'all' or 'specified'
    runout: list[str] | None = None  # optional 3-5 cards in usual notation like ['As','Kd',...]


@app.post("/api/equity")
async def api_equity(req: EquityRequest) -> JSONResponse:
    try:
        hero_cards = parse_hero(req.hero)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    villain_mode = (req.villain_mode or 'all').lower()
    runout_mode = (req.runout_mode or 'all').lower()

    # Villain combos resolution
    try:
        if villain_mode == 'range':
            villain_combos = parse_range(req.villain_range or '')
        else:
            # all possible villain two-card combos excluding hero cards
            villain_combos = []
            all_cards = [f"{n}{s}" for s in 'schd' for n in range(2,15)]
            remaining = [c for c in all_cards if c not in hero_cards]
            for i in range(len(remaining)):
                for j in range(i+1, len(remaining)):
                    villain_combos.append([remaining[i], remaining[j]])
        if not villain_combos:
            raise ValueError("Villain range must expand to at least one combination.")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    loop = asyncio.get_running_loop()
    # Runout handling: if specified, convert and use fixed or completed runouts per iteration
    def simulate():
        iterations = int(req.iterations)
        win = draw = lose = 0
        made_counts = {k: 0 for k in [
            "High Card", "Pair", "2 Pair", "Three of a kind",
            "Straight", "Flush", "Full", "Four of a kind", "Straight Flush"
        ]}
        won_with_counts = {k: 0 for k in made_counts}
        lost_to_counts = {k: 0 for k in made_counts}
        examples = []

        # Prepare specified runout in computing format if provided
        runout_spec = None
        if runout_mode == 'specified' and req.runout:
            try:
                runout_spec = ps.ConvertHandWhenLetters([c for c in req.runout])
            except Exception:
                raise ValueError("Invalid runout cards; use forms like As,Kd,...")

        import random as _random
        for i in range(iterations):
            villain = _random.choice(villain_combos)
            if runout_spec is None:
                runout = ps.RandomRunout(hero_cards, villain)
            else:
                if len(runout_spec) >= 5:
                    runout = runout_spec[:5]
                else:
                    runout = ps.RandomRunoutCompleter(runout_spec, hero_cards)

            hero_hand = ps.HandCategory(hero_cards, runout)
            villain_hand = ps.HandCategory(villain, runout)
            result = ps.WinOrLose(hero_cards, villain, runout)

            made_counts[hero_hand[0][0]] += 1
            if result == "win":
                win += 1
                won_with_counts[hero_hand[0][0]] += 1
            elif result == "draw":
                draw += 1
            else:
                lose += 1
                lost_to_counts[villain_hand[0][0]] += 1

            if i < 5:
                examples.append({
                    "runout": runout,
                    "villain": villain,
                    "hero_hand": hero_hand[0][0],
                    "villain_hand": villain_hand[0][0],
                    "result": result,
                })

        total = iterations or 1
        equity = (win + 0.5 * draw) / total
        win_ratio = win / total
        draw_ratio = draw / total
        def to_freq(counts):
            denom = sum(counts.values()) or 1
            return {k: counts[k] / denom for k in counts}
        return {
            "equity": equity,
            "win_ratio": win_ratio,
            "draw_ratio": draw_ratio,
            "made_distribution": to_freq(made_counts),
            "won_with_distribution": to_freq(won_with_counts),
            "lost_to_distribution": to_freq(lost_to_counts),
            "examples": examples,
            "combo_count": len(villain_combos),
        }

    try:
        result = await loop.run_in_executor(None, simulate)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return JSONResponse(result)
