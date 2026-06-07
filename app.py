import streamlit as st
import streamlit.components.v1 as components

# Set konfigurasi halaman agar penuh (Wide Mode)
st.set_page_config(page_title="Kalkulator Laplace RLC", layout="wide")

# Kode HTML + JS baru lu yang sudah diperbarui tampilannya
html_code = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Kalkulator Transformasi Laplace - Rangkaian RL, RC, RLC Seri</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Courier New', monospace;
    background: #0a0e1a;
    color: #e0e8ff;
    min-height: 100vh;
  }
  .header {
    background: linear-gradient(135deg, #0d1b3e 0%, #1a0d3e 100%);
    border-bottom: 1px solid #2a3a6e;
    padding: 1.5rem 2rem;
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  .header-icon {
    width: 48px; height: 48px;
    background: #1e3a8a;
    border: 1px solid #3b82f6;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
  }
  .header h1 { font-size: 1.3rem; font-weight: bold; color: #93c5fd; letter-spacing: 1px; }
  .header p { font-size: 0.75rem; color: #6b7db3; margin-top: 2px; }
  .main { display: grid; grid-template-columns: 320px 1fr; gap: 0; min-height: calc(100vh - 80px); }
  .sidebar {
    background: #0d1324;
    border-right: 1px solid #1e2d52;
    padding: 1.5rem;
    overflow-y: auto;
  }
  .section-label {
    font-size: 0.65rem;
    letter-spacing: 2px;
    color: #4a5a8a;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
    margin-top: 1.5rem;
  }
  .section-label:first-child { margin-top: 0; }
  .circuit-tabs { display: flex; gap: 4px; margin-bottom: 1rem; }
  .tab-btn {
    flex: 1;
    padding: 8px 4px;
    background: #111827;
    border: 1px solid #1e2d52;
    border-radius: 6px;
    color: #6b7db3;
    font-size: 0.75rem;
    font-family: 'Courier New', monospace;
    cursor: pointer;
    transition: all 0.2s;
  }
  .tab-btn.active { background: #1e3a8a; border-color: #3b82f6; color: #93c5fd; }
  .tab-btn:hover:not(.active) { background: #1a2540; border-color: #2a3a6e; color: #93c5fd; }
  .param-group { margin-bottom: 0.75rem; }
  .param-label {
    display: flex; justify-content: space-between; align-items: center;
    font-size: 0.75rem; color: #6b7db3; margin-bottom: 4px;
  }
  .param-label span { color: #fbbf24; font-size: 0.8rem; font-weight: bold; }
  input[type="number"] {
    width: 100%;
    background: #111827;
    border: 1px solid #1e2d52;
    border-radius: 4px;
    color: #e0e8ff;
    padding: 6px 10px;
    font-size: 0.85rem;
    font-family: 'Courier New', monospace;
    outline: none;
    transition: border-color 0.2s;
  }
  input[type="number"]:focus { border-color: #3b82f6; }
  .unit-badge {
    display: inline-block;
    background: #1a2540;
    border: 1px solid #2a3a6e;
    border-radius: 3px;
    padding: 2px 6px;
    font-size: 0.65rem;
    color: #4a5a8a;
    margin-top: 3px;
  }
  .calc-btn {
    width: 100%;
    padding: 10px;
    background: #1e3a8a;
    border: 1px solid #3b82f6;
    border-radius: 6px;
    color: #93c5fd;
    font-size: 0.85rem;
    font-family: 'Courier New', monospace;
    cursor: pointer;
    margin-top: 1rem;
    transition: all 0.2s;
    letter-spacing: 1px;
  }
  .calc-btn:hover { background: #2563eb; color: #fff; }
  .calc-btn:active { transform: scale(0.98); }
  .reset-btn {
    width: 100%;
    padding: 8px;
    background: transparent;
    border: 1px solid #2a3a6e;
    border-radius: 6px;
    color: #6b7db3;
    font-size: 0.75rem;
    font-family: 'Courier New', monospace;
    cursor: pointer;
    margin-top: 6px;
    transition: all 0.2s;
  }
  .reset-btn:hover { border-color: #4a5a8a; color: #93c5fd; }
  .content { padding: 1.5rem; overflow-y: auto; }
  .circuit-diagram {
    background: #0d1324;
    border: 1px solid #1e2d52;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1.5rem;
    text-align: center;
  }
  .circuit-diagram svg { max-width: 100%; }
  .results-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.5rem; }
  .result-card { background: #0d1324; border: 1px solid #1e2d52; border-radius: 8px; padding: 1rem 1.25rem; }
  .result-card .label { font-size: 0.65rem; letter-spacing: 2px; text-transform: uppercase; color: #4a5a8a; margin-bottom: 6px; }
  .result-card .value { font-size: 0.95rem; color: #93c5fd; font-weight: bold; word-break: break-all; }
  .result-card .value.formula { font-size: 0.85rem; color: #a78bfa; font-style: italic; }
  .result-card.highlight { border-color: #3b82f6; background: #0f1e3d; }
  .steps-panel { background: #0d1324; border: 1px solid #1e2d52; border-radius: 8px; padding: 1.25rem; margin-bottom: 1.5rem; }
  .steps-panel h3 { font-size: 0.7rem; letter-spacing: 2px; text-transform: uppercase; color: #4a5a8a; margin-bottom: 1rem; }
  .step { display: flex; gap: 12px; margin-bottom: 1rem; align-items: flex-start; }
  .step-num {
    width: 24px; height: 24px; min-width: 24px;
    background: #1e3a8a; border: 1px solid #3b82f6;
    border-radius: 4px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.7rem; color: #93c5fd; font-weight: bold;
  }
  .step-content { flex: 1; }
  .step-title { font-size: 0.8rem; color: #93c5fd; margin-bottom: 4px; }
  .step-formula {
    font-size: 0.8rem; color: #a78bfa;
    background: #0a0e1a; border: 1px solid #1e2d52;
    border-radius: 4px; padding: 6px 10px; margin-top: 4px;
    word-break: break-all;
  }
  .chart-container { background: #0d1324; border: 1px solid #1e2d52; border-radius: 8px; padding: 1.25rem; margin-bottom: 1.5rem; }
  .chart-container h3 { font-size: 0.7rem; letter-spacing: 2px; text-transform: uppercase; color: #4a5a8a; margin-bottom: 1rem; }
  canvas { width: 100% !important; }
  .table-panel { background: #0d1324; border: 1px solid #1e2d52; border-radius: 8px; padding: 1.25rem; }
  .table-panel h3 { font-size: 0.7rem; letter-spacing: 2px; text-transform: uppercase; color: #4a5a8a; margin-bottom: 1rem; }
  table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
  th {
    text-align: left; padding: 6px 10px;
    background: #111827; color: #6b7db3;
    border-bottom: 1px solid #1e2d52;
    font-weight: normal; font-size: 0.7rem; letter-spacing: 1px;
  }
  td { padding: 6px 10px; border-bottom: 1px solid #111827; color: #e0e8ff; }
  tr:hover td { background: #111827; }
  .empty-state { text-align: center; padding: 3rem; color: #4a5a8a; font-size: 0.85rem; }
  .empty-state .big { font-size: 2.5rem; margin-bottom: 1rem; opacity: 0.4; }
  .badge-RL { color: #34d399; }
  .badge-RC { color: #f472b6; }
  .badge-RLC { color: #fbbf24; }
  @media (max-width: 700px) {
    .main { grid-template-columns: 1fr; }
    .results-grid { grid-template-columns: 1fr; }
  }
</style>
</head>
<body>
<div class="header">
  <div class="header-icon">⚡</div>
  <div>
    <h1>TRANSFORMASI LAPLACE — RANGKAIAN LISTRIK SERI</h1>
    <p>Analisis Rangkaian RL · RC · RLC | Berbasis Hukum Kirchhoff II</p>
  </div>
</div>
<div class="main">
  <div class="sidebar">
    <div class="section-label">Tipe Rangkaian</div>
    <div class="circuit-tabs">
      <button class="tab-btn active" onclick="setCircuit('RL')">RL</button>
      <button class="tab-btn" onclick="setCircuit('RC')">RC</button>
      <button class="tab-btn" onclick="setCircuit('RLC')">RLC</button>
    </div>
    <div class="section-label">Parameter Komponen</div>
    <div class="param-group">
      <div class="param-label">Resistor (R) <span id="r-val">500</span></div>
      <input type="number" id="inp-R" value="500" step="1" min="0.001" oninput="document.getElementById('r-val').textContent=this.value">
      <span class="unit-badge">Ohm (Ω)</span>
    </div>
    <div class="param-group" id="grp-L">
      <div class="param-label">Induktor (L) <span id="l-val">27</span></div>
      <input type="number" id="inp-L" value="27" step="0.1" min="0.001" oninput="document.getElementById('l-val').textContent=this.value">
      <span class="unit-badge">Henry (H)</span>
    </div>
    <div class="param-group" id="grp-C" style="display:none;">
      <div class="param-label">Kapasitor (C) <span id="c-val">0.0012</span></div>
      <input type="number" id="inp-C" value="0.0012" step="0.0001" min="0.000001" oninput="document.getElementById('c-val').textContent=this.value">
      <span class="unit-badge">Farad (F)</span>
    </div>
    <div class="param-group">
      <div class="param-label">Tegangan DC (V) <span id="v-val">20</span></div>
      <input type="number" id="inp-V" value="20" step="1" min="0.001" oninput="document.getElementById('v-val').textContent=this.value">
      <span class="unit-badge">Volt (V)</span>
    </div>
    <div class="section-label">Rentang Waktu Simulasi</div>
    <div class="param-group">
      <div class="param-label">t maks <span id="tmax-val">100</span></div>
      <input type="number" id="inp-tmax" value="100" step="1" min="1" oninput="document.getElementById('tmax-val').textContent=this.value">
      <span class="unit-badge">detik (s)</span>
    </div>
    <button class="calc-btn" onclick="calculate()">▶  HITUNG &amp; SIMULASI</button>
    <button class="reset-btn" onclick="resetDefaults()">↺  Reset ke Default (Paper)</button>
  </div>
  <div class="content" id="content">
    <div class="empty-state">
      <div class="big">⚡</div>
      <p>Pilih tipe rangkaian, masukkan nilai parameter,<br>lalu tekan <strong>HITUNG &amp; SIMULASI</strong></p>
    </div>
  </div>
</div>
<script>
let currentCircuit = 'RL';
function setCircuit(type) {
  currentCircuit = type;
  document.querySelectorAll('.tab-btn').forEach((b, i) => {
    b.classList.toggle('active', ['RL','RC','RLC'][i] === type);
  });
  document.getElementById('grp-L').style.display = ['RL','RLC'].includes(type) ? '' : 'none';
  document.getElementById('grp-C').style.display = ['RC','RLC'].includes(type) ? '' : 'none';
}
function resetDefaults() {
  document.getElementById('inp-R').value = 500;
  document.getElementById('inp-L').value = 27;
  document.getElementById('inp-C').value = 0.0012;
  document.getElementById('inp-V').value = 20;
  document.getElementById('inp-tmax').value = 100;
  ['r','l','c','v','tmax'].forEach(k => {
    const el = document.getElementById(k+'-val');
    const inp = document.getElementById('inp-'+k.toUpperCase());
    if (el && inp) el.textContent = inp.value;
  });
}
function fmtNum(n, d=4) {
  if (Math.abs(n) < 1e-10) return '0';
  if (Math.abs(n) >= 1e-3 && Math.abs(n) < 1e6) return parseFloat(n.toFixed(d)).toString();
  return n.toExponential(3);
}
function calculate() {
  const R = parseFloat(document.getElementById('inp-R').value);
  const L = parseFloat(document.getElementById('inp-L').value) || 1;
  const C = parseFloat(document.getElementById('inp-C').value) || 1;
  const V = parseFloat(document.getElementById('inp-V').value);
  const tmax = parseFloat(document.getElementById('inp-tmax').value);
  let result = null;
  if (currentCircuit === 'RL') { result = calcRL(R, L, V, tmax); } 
  else if (currentCircuit === 'RC') { result = calcRC(R, C, V, tmax); } 
  else { result = calcRLC(R, L, C, V, tmax); }
  renderResults(result);
}
function calcRL(R, L, V, tmax) {
  const alpha = R / L; const A = V / R; const B = -V / R;
  const iFunc = t => A + B * Math.exp(-alpha * t);
  const steps = [
    { title: 'Persamaan Diferensial (Hukum Kirchhoff II)', formula: `R·i(t) + L·di(t)/dt = v(t)` },
    { title: 'Bagi kedua ruas dengan L', formula: `di(t)/dt + (R/L)·i(t) = v(t)/L` },
    { title: 'Terapkan Transformasi Laplace', formula: `s·I(s) + (R/L)·I(s) = V/(L·s)` },
    { title: 'Substitusi nilai parameter', formula: `s·I(s) + ${fmtNum(alpha)}·I(s) = ${fmtNum(V/L)}/s` },
    { title: 'Faktorkan & selesaikan I(s)', formula: `I(s) = ${fmtNum(V/L)} / [s·(s + ${fmtNum(alpha)})]` },
    { title: 'Dekomposisi fraksional parsial', formula: `I(s) = ${fmtNum(A)}/s + ${fmtNum(B)}/(s + ${fmtNum(alpha)})` },
    { title: 'Invers Transformasi Laplace → i(t)', formula: `i(t) = ${fmtNum(A)} + ${fmtNum(B)}·e^(−${fmtNum(alpha)}t) A` },
  ];
  const tau = 1 / alpha; const timeData = linspace(0, tmax, 300); const currentData = timeData.map(iFunc);
  return {
    type: 'RL', formula: `i(t) = ${fmtNum(A)} − ${fmtNum(Math.abs(B))}·e^(−${fmtNum(alpha)}t) A`,
    params: { R, L, V }, derived: { alpha: fmtNum(alpha), tau: fmtNum(tau), Iss: fmtNum(A) },
    steps, timeData, currentData, tableRows: buildTable(timeData, currentData, tmax),
    svgDiagram: svgRL(R, L, V), colorClass: 'badge-RL', iFunc, tmax
  };
}
function calcRC(R, C, V, tmax) {
  const alpha = 1 / (R * C); const A = V / R;
  const iFunc = t => A * Math.exp(-alpha * t);
  const steps = [
    { title: 'Persamaan Diferensial (Hukum Kirchhoff II)', formula: `R·i(t) + (1/C)·∫i(t)dt = v(t)` },
    { title: 'Terapkan Transformasi Laplace', formula: `R·I(s) + (1/C)·I(s)/s = V/s` },
    { title: 'Kalikan kedua ruas dengan s', formula: `(Rs + 1/C)·I(s) = V` },
    { title: 'Substitusi nilai parameter', formula: `(${R}s + ${fmtNum(1/C)})·I(s) = ${V}` },
    { title: 'Selesaikan I(s)', formula: `I(s) = ${fmtNum(A)} / (s + ${fmtNum(alpha)})` },
    { title: 'Invers Transformasi Laplace → i(t)', formula: `i(t) = ${fmtNum(A)}·e^(−${fmtNum(alpha)}t) A` },
  ];
  const tau = R * C; const timeData = linspace(0, tmax, 300); const currentData = timeData.map(iFunc);
  return {
    type: 'RC', formula: `i(t) = ${fmtNum(A)}·e^(−${fmtNum(alpha)}t) A`,
    params: { R, C, V }, derived: { alpha: fmtNum(alpha), tau: fmtNum(tau), Iss: '0 (kapasitor penuh)' },
    steps, timeData, currentData, tableRows: buildTable(timeData, currentData, tmax),
    svgDiagram: svgRC(R, C, V), colorClass: 'badge-RC', iFunc, tmax
  };
}
function calcRLC(R, L, C, V, tmax) {
  const b = R / L; const c = 1 / (L * C); const disc = b*b - 4*c;
  let formula, steps, iFunc;
  if (disc > 0) {
    const s1 = (-b + Math.sqrt(disc)) / 2; const s2 = (-b - Math.sqrt(disc)) / 2;
    const A = (V/L) / (s1 - s2); const B = -(V/L) / (s1 - s2);
    iFunc = t => A * Math.exp(s1*t) + B * Math.exp(s2*t);
    formula = `i(t) = ${fmtNum(A)}·e^(${fmtNum(s1)}t) + ${fmtNum(B)}·e^(${fmtNum(s2)}t) A`;
    steps = [
      { title: 'Persamaan Diferensial (Hukum Kirchhoff II)', formula: `R·i(t) + L·di/dt + (1/C)·∫i dt = v(t)` },
      { title: 'Bagi dengan L & Terapkan Transformasi Laplace', formula: `s²I(s) + (R/L)·sI(s) + (1/LC)·I(s) = V/(Ls)` },
      { title: 'Kalikan dengan s & faktorkan', formula: `(s² + ${fmtNum(b)}s + ${fmtNum(c)})·I(s) = ${fmtNum(V/L)}` },
      { title: 'Faktorkan penyebut (rumus ABC)', formula: `s₁ = ${fmtNum(s1,4)}, s₂ = ${fmtNum(s2,4)}` },
      { title: 'Dekomposisi fraksional parsial', formula: `I(s) = ${fmtNum(A)}/(s−${fmtNum(s1)}) + ${fmtNum(B)}/(s−${fmtNum(s2)})` },
      { title: 'Invers Transformasi Laplace → i(t)', formula },
    ];
  } else if (disc === 0) {
    const s1 = -b/2; const A = V/L;
    iFunc = t => A * t * Math.exp(s1*t);
    formula = `i(t) = ${fmtNum(A)}·t·e^(${fmtNum(s1)}t) A  [critically damped]`;
    steps = [
      { title: 'Persamaan Diferensial', formula: `R·i + L·di/dt + (1/C)·∫i dt = v(t)` },
      { title: 'Discriminant = 0 → critically damped', formula: `s₁ = s₂ = ${fmtNum(s1)}` },
      { title: 'I(s) dengan akar ganda', formula: `I(s) = ${fmtNum(V/L)} / (s − ${fmtNum(s1)})²` },
      { title: 'Invers Transformasi Laplace → i(t)', formula },
    ];
  } else {
    const sigma = -b/2; const omega = Math.sqrt(-disc)/2; const A = (V/L) / omega;
    iFunc = t => A * Math.exp(sigma*t) * Math.sin(omega*t);
    formula = `i(t) = ${fmtNum(A)}·e^(${fmtNum(sigma)}t)·sin(${fmtNum(omega)}t) A  [underdamped]`;
    steps = [
      { title: 'Persamaan Diferensial', formula: `R·i + L·di/dt + (1/C)·∫i dt = v(t)` },
      { title: 'Discriminant < 0 → underdamped (osilasi)', formula: `σ = ${fmtNum(sigma)}, ωd = ${fmtNum(omega)}` },
      { title: 'I(s) akar kompleks konjugat', formula: `I(s) = ${fmtNum(V/L)} / [(s+${fmtNum(-sigma)})² + ${fmtNum(omega)}²]` },
      { title: 'Invers Transformasi Laplace → i(t)', formula },
    ];
  }
  const timeData = linspace(0, tmax, 300); const currentData = timeData.map(iFunc);
  return {
    type: 'RLC', formula, params: { R, L, C, V },
    derived: { b: fmtNum(b), discriminant: fmtNum(disc), regime: disc>0?'Overdamped':disc===0?'Critically Damped':'Underdamped' },
    steps, timeData, currentData, tableRows: buildTable(timeData, currentData, tmax),
    svgDiagram: svgRLC(R, L, C, V), colorClass: 'badge-RLC', iFunc, tmax
  };
}
function linspace(a, b, n) { const arr = []; for (let i = 0; i < n; i++) arr.push(a + (b-a)*i/(n-1)); return arr; }
function buildTable(t, i, tmax) {
  const rows = []; const intervals = 10;
  for (let step = 0; step <= intervals; step++) {
    const tv = (tmax / intervals) * step;
    const idx = t.findIndex(x => x >= tv);
    if (idx >= 0) rows.push({ t: tv.toFixed(1), i: i[idx] });
  }
  return rows;
}
function renderResults(r) {
  const colors = { RL: '#34d399', RC: '#f472b6', RLC: '#fbbf24' }; const col = colors[r.type];
  const tableHTML = r.tableRows.map(row => `<tr><td>${row.t} s</td><td>${fmtNum(row.i, 6)} A</td></tr>`).join('');
  const stepsHTML = r.steps.map((s, i) => `
    <div class="step">
      <div class="step-num">${i+1}</div>
      <div class="step-content">
        <div class="step-title">${s.title}</div>
        <div class="step-formula">${s.formula}</div>
      </div>
    </div>`).join('');
  const derivedHTML = Object.entries(r.derived).map(([k,v]) => `<div class="result-card"><div class="label">${k}</div><div class="value">${v}</div></div>`).join('');
  document.getElementById('content').innerHTML = `
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:1.5rem;"><span style="font-size:0.7rem;letter-spacing:2px;text-transform:uppercase;color:#4a5a8a;">Hasil:</span><span style="font-size:1rem;font-weight:bold;color:${col};">Rangkaian ${r.type} Seri</span></div>
    <div class="circuit-diagram">${r.svgDiagram}</div>
    <div class="results-grid"><div class="result-card highlight" style="grid-column:1/-1;"><div class="label">Persamaan Arus i(t) — Hasil Transformasi Laplace</div><div class="value formula" style="color:${col};font-size:1rem;">${r.formula}</div></div>${derivedHTML}</div>
    <div class="steps-panel"><h3>Langkah-langkah Penyelesaian</h3>${stepsHTML}</div>
    <div class="chart-container"><h3>Grafik Arus i(t) terhadap Waktu</h3><canvas id="chart-canvas" height="260"></canvas></div>
    <div class="table-panel"><h3>Tabel Perbandingan Nilai i(t)</h3><table><thead><tr><th>t (detik)</th><th>i(t) — Transformasi Laplace</th></tr></thead><tbody>${tableHTML}</tbody></table></div>`;
  renderChart(r.timeData, r.currentData, r.type, col);
}
let chartInstance = null;
function renderChart(t, i, type, col) {
  if (chartInstance) { chartInstance.destroy(); chartInstance = null; }
  const ctx = document.getElementById('chart-canvas').getContext('2d');
  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: t.map(x => x.toFixed(1)),
      datasets: [{ label: `i(t) — Rangkaian ${type} Seri`, data: i, borderColor: col, backgroundColor: col + '18', borderWidth: 2, pointRadius: 0, fill: true, tension: 0.4 }]
    },
    options: {
      responsive: true, maintainAspectRatio: false, animation: { duration: 600 },
      plugins: {
        legend: { labels: { color: '#93c5fd', font: { family: 'Courier New', size: 12 } } },
        tooltip: { backgroundColor: '#0d1324', borderColor: '#1e2d52', borderWidth: 1, titleColor: '#93c5fd', bodyColor: '#e0e8ff', callbacks: { label: ctx => `i(t) = ${ctx.raw.toExponential(4)} A` } }
      },
      scales: {
        x: { ticks: { color: '#6b7db3', font: { family: 'Courier New', size: 11 }, maxTicksLimit: 10 }, grid: { color: '#1e2d52' }, title: { display: true, text: 'Waktu (detik)', color: '#6b7db3', font: { family: 'Courier New' } } },
        y: { ticks: { color: '#6b7db3', font: { family: 'Courier New', size: 11 }, callback: v => v.toExponential(2) }, grid: { color: '#1e2d52' }, title: { display: true, text: 'Arus i(t) [Ampere]', color: '#6b7db3', font: { family: 'Courier New' } } }
      }
    }
  });
}
function svgRL(R, L, V) {
  return `<svg width="480" height="140" viewBox="0 0 480 140" xmlns="http://www.w3.org/2000/svg"><style>text{font-family:'Courier New';fill:#e0e8ff;font-size:11px}</style><line x1="40" y1="30" x2="440" y2="30" stroke="#3b82f6" stroke-width="1.5"/><line x1="40" y1="110" x2="440" y2="110" stroke="#3b82f6" stroke-width="1.5"/><line x1="40" y1="30" x2="40" y2="110" stroke="#3b82f6" stroke-width="1.5"/><line x1="440" y1="30" x2="440" y2="110" stroke="#3b82f6" stroke-width="1.5"/><rect x="155" y="20" width="70" height="20" rx="3" fill="none" stroke="#34d399" stroke-width="1.5"/><text x="178" y="33">R</text><text x="145" y="55" font-size="10" fill="#34d399">${R} Ω</text><rect x="290" y="20" width="70" height="20" rx="4" fill="none" stroke="#34d399" stroke-width="1.5"/><text x="316" y="33">L</text><text x="280" y="55" font-size="10" fill="#34d399">${L} H</text><rect x="28" y="60" width="24" height="40" rx="3" fill="none" stroke="#fbbf24" stroke-width="1.5"/><text x="33" y="84">V</text><text x="10" y="105" font-size="10" fill="#fbbf24">${V} V</text><text x="200" y="95" fill="#6b7db3" font-size="10">→ i(t)</text></svg>`;
}
function svgRC(R, C, V) {
  return `<svg width="480" height="140" viewBox="0 0 480 140" xmlns="http://www.w3.org/2000/svg"><style>text{font-family:'Courier New';fill:#e0e8ff;font-size:11px}</style><line x1="40" y1="30" x2="440" y2="30" stroke="#3b82f6" stroke-width="1.5"/><line x1="40" y1="110" x2="440" y2="110" stroke="#3b82f6" stroke-width="1.5"/><line x1="40" y1="30" x2="40" y2="110" stroke="#3b82f6" stroke-width="1.5"/><line x1="440" y1="30" x2="440" y2="110" stroke="#3b82f6" stroke-width="1.5"/><rect x="155" y="20" width="70" height="20" rx="3" fill="none" stroke="#f472b6" stroke-width="1.5"/><text x="178" y="33">R</text><text x="145" y="55" font-size="10" fill="#f472b6">${R} Ω</text><line x1="303" y1="20" x2="303" y2="40" stroke="#f472b6" stroke-width="2"/><line x1="297" y1="20" x2="309" y2="20" stroke="#f472b6" stroke-width="1.5"/><line x1="297" y1="40" x2="309" y2="40" stroke="#f472b6" stroke-width="1.5"/><text x="316" y="33">C</text><text x="280" y="55" font-size="10" fill="#f472b6">${C} F</text><rect x="28" y="60" width="24" height="40" rx="3" fill="none" stroke="#fbbf24" stroke-width="1.5"/><text x="33" y="84">V</text><text x="10" y="105" font-size="10" fill="#fbbf24">${V} V</text><text x="200" y="95" fill="#6b7db3" font-size="10">→ i(t)</text></svg>`;
}
function svgRLC(R, L, C, V) {
  return `<svg width="480" height="140" viewBox="0 0 480 140" xmlns="http://www.w3.org/2000/svg"><style>text{font-family:'Courier New';fill:#e0e8ff;font-size:11px}</style><line x1="40" y1="30" x2="440" y2="30" stroke="#3b82f6" stroke-width="1.5"/><line x1="40" y1="110" x2="440" y2="110" stroke="#3b82f6" stroke-width="1.5"/><line x1="40" y1="30" x2="40" y2="110" stroke="#3b82f6" stroke-width="1.5"/><line x1="440" y1="30" x2="440" y2="110" stroke="#3b82f6" stroke-width="1.5"/><rect x="95" y="20" width="60" height="20" rx="3" fill="none" stroke="#fbbf24" stroke-width="1.5"/><text x="116" y="33">R</text><text x="88" y="55" font-size="10" fill="#fbbf24">${R} Ω</text><rect x="210" y="20" width="60" height="20" rx="4" fill="none" stroke="#fbbf24" stroke-width="1.5"/><text x="232" y="33">L</text><text x="200" y="55" font-size="10" fill="#fbbf24">${L} H</text><line x1="333" y1="20" x2="333" y2="40" stroke="#fbbf24" stroke-width="2"/><line x1="327" y1="20" x2="339" y2="20" stroke="#fbbf24" stroke-width="1.5"/><line x1="327" y1="40" x2="339" y2="40" stroke="#fbbf24" stroke-width="1.5"/><text x="346" y="33">C</text><text x="318" y="55" font-size="10" fill="#fbbf24">${C} F</text><rect x="28" y="60" width="24" height="40" rx="3" fill="none" stroke="#93c5fd" stroke-width="1.5"/><text x="33" y="84">V</text><text x="10" y="105" font-size="10" fill="#93c5fd">${V} V</text><text x="200" y="95" fill="#6b7db3" font-size="10">→ i(t)</text></svg>`;
}
</script>
</body>
</html>
"""

# Di sini letak perbaikannya: scrolling=True (bukan scroller=True)
components.html(html_code, height=1100, scrolling=True)
