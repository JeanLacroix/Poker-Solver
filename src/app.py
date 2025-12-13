import asyncio
import pathlib
import sys
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

# Import solver helpers; tolerate being run as a module or as a script.
try:
    from .poker_solver_cli import (
        calculate_equity,
        calculate_equity_details,
        parse_hero,
        parse_range,
    )
    from . import poker_solver as ps
except ImportError:
    # Fallback for invocations like `uvicorn app:app --app-dir src`
    here = pathlib.Path(__file__).resolve().parent
    if str(here) not in sys.path:
        sys.path.append(str(here))
    from poker_solver_cli import (  # type: ignore
        calculate_equity,
        calculate_equity_details,
        parse_hero,
        parse_range,
    )
    import poker_solver as ps  # type: ignore

app = FastAPI()

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Poker Solver App</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');

  :root {
    --bg: #020617;
    --panel: #020617;
    --card: #020617;
    --accent: #22c55e;
    --accent-2: #a3e635;
    --text: #f9fafb;
    --muted: #9ca3af;
    --danger: #f97373;
    --border: rgba(148, 163, 184, 0.35);
  }

  * { box-sizing: border-box; }

  body {
    margin: 0;
    font-family: 'Space Grotesk', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background:
      radial-gradient(circle at 15% 0%, rgba(34, 197, 94, 0.20), transparent 55%),
      radial-gradient(circle at 85% 0%, rgba(59, 130, 246, 0.18), transparent 55%),
      radial-gradient(circle at 50% 100%, #052e16 0, #020617 55%);
    color: var(--text);
    min-height: 100vh;
    padding: 32px 20px 24px;
    display: flex;
    justify-content: center;
  }

  .page {
    width: 100%;
    max-width: 1240px;
  }

  .container {
    display: grid;
    grid-template-columns: 1.05fr 0.95fr;
    gap: 20px;
  }

  header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 20px;
  }

  .brand {
    font-weight: 700;
    letter-spacing: 0.5px;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .chip {
    padding: 4px 10px;
    border-radius: 999px;
    background: rgba(22, 163, 74, 0.18);
    border: 1px solid var(--border);
    color: var(--accent-2);
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }

  .panel {
    background: radial-gradient(circle at top left, rgba(34,197,94,0.25), rgba(15,23,42,0.96));
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 18px 18px 16px;
    box-shadow: 0 18px 55px rgba(0,0,0,0.55);
    backdrop-filter: blur(8px);
  }

  .panel h2 {
    margin: 0 0 10px 0;
    font-size: 18px;
    letter-spacing: 0.02em;
  }

  .section-caption {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 14px;
  }

  .section-block {
    border: 1px solid rgba(148,163,184,0.45);
    background: radial-gradient(circle at top, rgba(15,118,110,0.22), var(--card));
    border-radius: 14px;
    padding: 12px 12px 10px;
    margin-bottom: 12px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
  }

  .section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    margin-bottom: 10px;
  }

  .section-header h3 {
    margin: 0;
    font-size: 16px;
    letter-spacing: 0.01em;
  }

  form {
    display: grid;
    gap: 14px;
  }

  label {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    font-weight: 600;
  }

  .hint {
    font-size: 12px;
    color: var(--muted);
  }

  .pill-row {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }

  .pill {
    padding: 7px 12px;
    border-radius: 999px;
    background: rgba(15,23,42,0.8);
    color: var(--muted);
    border: 1px solid var(--border);
    cursor: pointer;
    user-select: none;
    transition: all 0.15s ease;
    font-size: 12px;
  }

  .pill:hover {
    border-color: rgba(34,197,94,0.6);
    color: var(--text);
  }

  .pill.active {
    background: rgba(22,163,74,0.28);
    border-color: rgba(34,197,94,0.9);
    color: var(--text);
  }

  .pill.active::after {
    content: 'ON';
    margin-left: 8px;
    font-weight: 700;
    color: var(--accent-2);
  }

  input[type="text"],
  input[type="number"] {
    width: 100%;
    padding: 10px 12px;
    border-radius: 10px;
    border: 1px solid var(--border);
    background: rgba(15,23,42,0.95);
    color: var(--text);
    font-size: 13px;
  }

  input::placeholder { color: var(--muted); }

  button {
    padding: 11px 16px;
    border-radius: 999px;
    background: radial-gradient(circle at top left, var(--accent-2), var(--accent));
    color: #022c22;
    border: none;
    font-weight: 700;
    cursor: pointer;
    transition: transform 0.1s ease, box-shadow 0.1s ease, filter 0.1s ease;
    font-size: 13px;
  }

  button:hover {
    transform: translateY(-1px);
    filter: brightness(1.05);
    box-shadow: 0 14px 30px rgba(21,128,61,0.6);
  }

  button:active {
    transform: translateY(0);
    box-shadow: 0 5px 14px rgba(21,128,61,0.55);
  }

  .pill,
  button { font-family: 'Space Grotesk', 'Segoe UI', sans-serif; }

  .card-grid {
    display: grid;
    grid-template-columns: repeat(13, minmax(32px, 1fr));
    gap: 4px;
    background: rgba(15,23,42,0.96);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 10px;
  }

  .card {
    padding: 7px 4px;
    border-radius: 9px;
    text-align: center;
    font-weight: 600;
    background: rgba(15,23,42,1);
    border: 1px solid transparent;
    cursor: pointer;
    transition: all 0.12s ease;
    font-size: 12px;
  }

  .card:hover {
    border-color: rgba(34,197,94,0.6);
  }

  .card.sel {
    background: rgba(22,163,74,0.28);
    border-color: rgba(34,197,94,0.9);
    color: #ecfdf3;
  }

  .hero-matrix {
    width: 100%;
    border-collapse: collapse;
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
    background: rgba(15,23,42,0.96);
  }

  .hero-matrix th,
  .hero-matrix td {
    border: 1px solid rgba(30,64,175,0.65);
    padding: 7px 4px;
    text-align: center;
    font-size: 12px;
  }

  .hero-matrix th {
    color: var(--muted);
    background: rgba(15,23,42,0.9);
    font-weight: 600;
  }

  .hero-cell {
    cursor: pointer;
    background: rgba(15,23,42,0.9);
    transition: all 0.12s ease;
    font-weight: 700;
  }

  .hero-cell:hover {
    background: rgba(34,197,94,0.14);
  }

  .hero-cell.sel {
    background: rgba(22,163,74,0.3);
    color: #ecfdf3;
    border-color: rgba(74,222,128,0.9);
  }

  .suit-s { color: #38bdf8; }
  .suit-c { color: #22c55e; }
  .suit-h { color: #fb7185; }
  .suit-d { color: #fde047; }

  .matrix {
    border-collapse: collapse;
    width: 100%;
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
  }

  .matrix td {
    border: 1px solid rgba(30,64,175,0.65);
    padding: 7px 4px;
    text-align: center;
    font-size: 12px;
    cursor: pointer;
    background: rgba(15,23,42,0.9);
    transition: background 0.12s ease, color 0.12s ease, border-color 0.12s ease;
  }

  .matrix td:hover {
    background: rgba(34,197,94,0.14);
  }

  .matrix td.sel {
    background: rgba(22,163,74,0.3);
    color: #ecfdf3;
    border-color: rgba(74,222,128,0.9);
  }

  /* shared highlight glow */
  .matrix td.sel,
  .card.sel,
  .hero-cell.sel {
    box-shadow:
      0 0 0 1px rgba(74,222,128,0.7),
      0 10px 18px rgba(0,0,0,0.55);
  }

  .row {
    display: flex;
    gap: 10px;
    align-items: center;
    flex-wrap: wrap;
  }

  .controls {
    display: flex;
    gap: 10px;
    align-items: center;
    flex-wrap: wrap;
  }

  .inline-stat {
    padding: 6px 10px;
    border-radius: 999px;
    background: rgba(15,23,42,0.9);
    border: 1px solid var(--border);
    font-size: 13px;
    color: var(--muted);
  }

  .inline-stat span {
    color: var(--accent-2);
  }

  .result-box {
    padding: 12px;
    border-radius: 12px;
    background: rgba(15,23,42,0.9);
    border: 1px solid var(--border);
    margin-top: 8px;
    min-height: 42px;
    font-size: 14px;
  }

  .result { font-weight: 700; }

  .error { color: var(--danger); }

  .charts h3 { margin: 0 0 8px 0; font-size: 14px; }

  .charts .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 14px;
  }

  .charts canvas {
    background: rgba(15,23,42,0.96);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 6px;
  }

  ul { padding-left: 18px; }
  li { color: var(--muted); margin: 4px 0; }

  @media (max-width: 920px) {
    .container {
      grid-template-columns: 1fr;
    }
  }
</style>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
<div class="page">
<header>
  <div class="brand">
    <div class="chip">Poker Equity</div>
    <div>
      <div style="font-size:22px; line-height:1.1;">Poker Solver App</div>
      <div class="hint">Pick your hero, shape villain ranges, lock a runout, then simulate.</div>
    </div>
  </div>
  <div class="inline-stat">Current hero: <span id="heroDisplay">{hero}</span></div>
</header>

<div class="container">
  <div class="panel">
    <h2>Simulation Setup</h2>
    <div class="section-caption">Choose hero cards, villain ranges, and optional fixed boards.</div>
    <form id="equity-form" method="get">
      <div class="section-block">
        <div class="section-header">
          <h3>Hero Selection</h3>
          <span class="hint">Pick exactly two cards.</span>
        </div>
        <div id="heroGrid"></div>
        <input type="hidden" id="hero" name="hero" value="{hero}" required>
      </div>

      <div class="section-block">
        <div class="section-header">
          <h3>Villain Options</h3>
          <span class="hint">Toggle between all combos or build a custom range matrix.</span>
        </div>
        <div class="pill-row">
          <span class="pill active" id="villainAll" aria-pressed="true">All possible hands</span>
          <span class="pill" id="villainRange" aria-pressed="false">Use range matrix</span>
        </div>
        <div id="rangeMatrixWrapper" style="margin-top:10px; display:none;"></div>
        <input type="text" id="villain_range" name="villain_range" value="{villain}" placeholder="AA,KK,AKs" style="display:none;">
      </div>

      <div class="section-block">
        <div class="section-header">
          <h3>Runout Selection</h3>
          <span class="hint">Random runouts or lock 3-5 community cards.</span>
        </div>
        <div class="pill-row">
          <span class="pill active" id="runoutAll" aria-pressed="true">All possible runouts</span>
          <span class="pill" id="runoutSpecified" aria-pressed="false">Specified runout</span>
        </div>
        <div id="runoutGridWrapper" style="display:none; margin-top:10px;"></div>
      </div>

      <div class="section-block">
        <div class="section-header">
          <h3>Iterations</h3>
          <span class="hint">Higher counts produce smoother estimates.</span>
        </div>
        <div class="row">
          <div style="flex:1;">
            <input type="number" id="iterations" name="iterations" value="{iterations}" min="1" required>
          </div>
          <div style="display:flex; align-items:flex-end;">
            <button type="submit">Calculate Equity</button>
          </div>
          <span id="status" class="hint"></span>
        </div>
      </div>
    </form>
    <div class="result-box" id="result">{result}</div>
  </div>

  <div class="panel">
    <h2>Results & Charts</h2>
    <div class="section-caption">Win/draw ratios, hand distributions, and sample runouts.</div>
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
      <div style="margin-top:0.5rem; color:var(--muted);" id="comboCount"></div>
    </div>
  </div>
</div>

</div>

<script>
const form = document.getElementById('equity-form');
const statusEl = document.getElementById('status');
const resultEl = document.getElementById('result');
const examplesEl = document.getElementById('examples');
const comboEl = document.getElementById('comboCount');
let madeChart, wonChart, lostChart;

function applySelectionHighlight(el, isSelected) {
  el.classList.toggle('sel', isSelected);
  el.dataset.selected = isSelected ? 'true' : 'false';
}

const ranks = ['A','K','Q','J','T','9','8','7','6','5','4','3','2'];
const suits = ['s','c','h','d'];
const suitLabel = { s: 'S', c: 'C', h: 'H', d: 'D' };

const heroGrid = document.getElementById('heroGrid');
const heroHidden = document.getElementById('hero');
const heroDisplay = document.getElementById('heroDisplay');
let heroSel = [];

function renderHeroGrid() {
  heroGrid.innerHTML = '';
  const table = document.createElement('table');
  table.className = 'hero-matrix';
  const thead = document.createElement('thead');
  const headRow = document.createElement('tr');
  headRow.appendChild(document.createElement('th'));
  ranks.forEach(r => {
    const th = document.createElement('th');
    th.textContent = r;
    headRow.appendChild(th);
  });
  thead.appendChild(headRow);
  table.appendChild(thead);

  const tbody = document.createElement('tbody');
  suits.forEach(s => {
    const tr = document.createElement('tr');
    const suitTh = document.createElement('th');
    suitTh.textContent = suitLabel[s] || s.toUpperCase();
    suitTh.className = 'suit-' + s;
    tr.appendChild(suitTh);
    ranks.forEach(r => {
      const card = r + s;
      const td = document.createElement('td');
      td.className = 'hero-cell suit-' + s;
      applySelectionHighlight(td, heroSel.includes(card));
      td.textContent = card;
      td.onclick = () => {
        const idx = heroSel.indexOf(card);
        if (idx >= 0) {
          heroSel.splice(idx,1);
        } else if (heroSel.length < 2) {
          heroSel.push(card);
        }
        if (heroSel.length > 2) heroSel = heroSel.slice(0,2);
        heroHidden.value = heroSel.join('');
        heroDisplay.textContent = heroHidden.value || '(none)';
        renderHeroGrid();
        if (runoutSpecPill && runoutSpecPill.classList.contains('active')) renderRunoutGrid();
      };
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);
  heroGrid.appendChild(table);
}

(function initHeroFromValue(){
  const v = (heroHidden.value||'').trim();
  if (v.length === 4) heroSel = [v.slice(0,2), v.slice(2)];
})();
renderHeroGrid();

// villain matrix
const villainAllPill = document.getElementById('villainAll');
const villainRangePill = document.getElementById('villainRange');
const rangeMatrixWrapper = document.getElementById('rangeMatrixWrapper');
const villainRangeInput = document.getElementById('villain_range');
let rangeSel = new Set();

function handLabel(i,j){
  const r1 = ranks[i];
  const r2 = ranks[j];
  if (i === j) return r1 + r2;
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
      applySelectionHighlight(td, rangeSel.has(label));
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
  const isAll = mode === 'all';
  villainAllPill.classList.toggle('active', isAll);
  villainRangePill.classList.toggle('active', !isAll);
  villainAllPill.setAttribute('aria-pressed', isAll);
  villainRangePill.setAttribute('aria-pressed', !isAll);
  rangeMatrixWrapper.style.display = isAll ? 'none' : '';
  villainRangeInput.style.display = isAll ? 'none' : '';
}
villainAllPill.onclick = () => setVillainMode('all');
villainRangePill.onclick = () => setVillainMode('range');
setVillainMode('all');

// runout grid
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
      div.className = 'card';
      applySelectionHighlight(div, runoutSel.includes(card));
      div.textContent = card;
      div.onclick = () => {
        const idx = runoutSel.indexOf(card);
        if (idx >= 0) runoutSel.splice(idx,1);
        else if (runoutSel.length < 5) runoutSel.push(card);
        renderRunoutGrid();
      };
      if (heroSel.includes(card)) {
        div.style.opacity = 0.5;
        div.style.pointerEvents='none';
      }
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
  const isAll = mode === 'all';
  runoutAllPill.classList.toggle('active', isAll);
  runoutSpecPill.classList.toggle('active', !isAll);
  runoutAllPill.setAttribute('aria-pressed', isAll);
  runoutSpecPill.setAttribute('aria-pressed', !isAll);
  runoutGridWrapper.style.display = isAll ? 'none' : '';
  if (!isAll) renderRunoutGrid();
}
runoutAllPill.onclick = () => setRunoutMode('all');
runoutSpecPill.onclick = () => setRunoutMode('specified');
setRunoutMode('all');

function renderBarChart(ctx, dataMap, title) {
  const labels = Object.keys(dataMap);
  const data = labels.map(k => dataMap[k]);
  return new Chart(ctx, {
    type: 'bar',
    data: { labels, datasets: [{ label: title, data, backgroundColor: '#16a34a' }] },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: v => (v*100).toFixed(1)+'%'
          }
        }
      },
      plugins: { legend: { display:false } }
    }
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
    const resp = await fetch('/api/equity', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ hero, villain_range, iterations, villain_mode, runout_mode, runout })
    });
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
    villain_mode: str | None = None
    runout_mode: str | None = None
    runout: list[str] | None = None

@app.post("/api/equity")
async def api_equity(req: EquityRequest) -> JSONResponse:
    try:
        hero_cards = parse_hero(req.hero)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    villain_mode = (req.villain_mode or 'all').lower()
    runout_mode = (req.runout_mode or 'all').lower()

    try:
        if villain_mode == 'range':
            villain_combos = parse_range(req.villain_range or '')
        else:
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
