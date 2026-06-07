import streamlit as st
import streamlit.components.v1 as components

# Mengatur konfigurasi halaman Streamlit agar memenuhi layar (Wide Mode)
st.set_page_config(page_title="Simulator Laplace", layout="wide")

# Ini adalah kode HTML + JS Premium yang sudah kita buat sebelumnya
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
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: #0f111a; color: #f1f3f9; min-height: 100vh; display: flex; flex-direction: column;
  }
  .navbar { background: #161925; border-bottom: 1px solid #22273a; padding: 1.25rem 2rem; display: flex; justify-content: space-between; align-items: center; }
  .brand-section { display: flex; align-items: center; gap: 12px; }
  .brand-logo { font-size: 2rem; }
  .brand-title h1 { font-size: 1.4rem; font-weight: 700; color: #ffffff; }
  .brand-title p { font-size: 0.85rem; color: #94a3b8; margin-top: 2px; }
  .dashboard-container { display: flex; flex: 1; overflow: hidden; }
  .sidebar { width: 340px; background: #161925; border-right: 1px solid #22273a; padding: 1.75rem; overflow-y: auto; display: flex; flex-direction: column; gap: 1.5rem; }
  .sidebar-section-title { font-size: 0.95rem; font-weight: 600; color: #ffffff; display: flex; align-items: center; gap: 8px; border-bottom: 1px solid #22273a; padding-bottom: 8px; }
  .circuit-tabs { display: flex; background: #0f111a; padding: 4px; border-radius: 8px; gap: 4px; }
  .tab-btn { flex: 1; padding: 10px; background: transparent; border: none; border-radius: 6px; color: #94a3b8; font-size: 0.85rem; font-weight: 600; cursor: pointer; transition: all 0.2s; }
  .tab-btn.active { background: #1e293b; color: #3b82f6; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
  .tab-btn:hover:not(.active) { color: #ffffff; background: rgba(255,255,255,0.03); }
  .param-group { display: flex; flex-direction: column; gap: 6px; margin-bottom: 0.5rem; }
  .param-label-container { display: flex; justify-content: space-between; font-size: 0.85rem; color: #94a3b8; }
  .param-value { color: #ef4444; font-weight: 600; }
  .slider-input { -webkit-appearance: none; width: 100%; height: 6px; background: #2d3142; border-radius: 3px; outline: none; }
  .slider-input::-webkit-slider-thumb { -webkit-appearance: none; appearance: none; width: 16px; height: 16px; border-radius: 50%; background: #ef4444; cursor: pointer; transition: transform 0.1s; }
  .slider-input::-webkit-slider-thumb:hover { transform: scale(1.2); }
  .input-number-wrapper { display: flex; background: #0f111a; border: 1px solid #2d3142; border-radius: 6px; overflow: hidden; }
  .input-number-wrapper button { background: transparent; border: none; color: #94a3b8; width: 36px; font-size: 1.1rem; cursor: pointer; }
  .input-number-wrapper button:hover { background: #2d3142; color: #ffffff; }
  .input-number-raw { flex: 1; background: transparent; border: none; color: #ffffff; text-align: center; padding: 8px; font-size: 0.9rem; outline: none; }
  .calc-btn { background: #3b82f6; color: white; border: none; padding: 12px; border-radius: 8px; font-weight: 600; font-size: 0.95rem; cursor: pointer; transition: background 0.2s; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2); }
  .calc-btn:hover { background: #2563eb; }
  .reset-btn { background: transparent; color: #94a3b8; border: 1px solid #2d3142; padding: 10px; border-radius: 8px; font-size: 0.85rem; cursor: pointer; }
  .reset-btn:hover { border-color: #94a3b8; color: white; }
  .main-content { flex: 1; padding: 2rem; overflow-y: auto; background: #0f111a; }
  .dashboard-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 1.5rem; margin-top: 1.5rem; }
  @media (max-width: 1024px) { .dashboard-grid { grid-template-columns: 1fr; } .dashboard-container { flex-direction: column; } .sidebar { width: 100%; } }
  .card { background: #161925; border: 1px solid #22273a; border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 20px rgba(0,0,0,0.15); }
  .card-title { font-size: 1.1rem; font-weight: 600; margin-bottom: 1.25rem; display: flex; align-items: center; gap: 8px; color: #ffffff; }
  .visual-panel { background: #1a1e2e; border-radius: 8px; padding: 1.5rem; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 200px; border: 1px dashed #2d3142; }
  .results-grid-mini { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 1rem; margin-top: 1rem; }
  .mini-stat-card { background: #0f111a; border: 1px solid #22273a; padding: 10px 14px; border-radius: 8px; }
  .mini-stat-label { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }
  .mini-stat-value { font-size: 1.1rem; font-weight: 700; color: #3b82f6; margin-top: 4px; }
  .formula-box { background: #0f111a; border-left: 4px solid #3b82f6; padding: 12px; border-radius: 0 8px 8px 0; font-family: monospace; font-size: 0.95rem; color: #a78bfa; margin-top: 0.5rem; overflow-x: auto; }
  .steps-list { display: flex; flex-direction: column; gap: 1rem; margin-top: 1rem; }
  .step-item { display: flex; gap: 12px; }
  .step-badge { width: 24px; height: 24px; background: rgba(59, 130, 246, 0.1); border: 1px solid #3b82f6; color: #3b82f6; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: bold; flex-shrink: 0; }
  .step-text-title { font-size: 0.85rem; font-weight: 600; color: #ffffff; }
  .step-text-formula { font-size: 0.8rem; color: #94a3b8; font-family: monospace; margin-top: 4px; }
  table { width: 100%; border-collapse: collapse; margin-top: 0.75rem; font-size: 0.85rem; }
  th { text-align: left; padding: 10px; background: #0f111a; color: #94a3b8; font-weight: 600; border-bottom: 1px solid #22273a; }
  td { padding: 10px; border-bottom: 1px solid #161925; color: #f1f3f9; }
  tr:hover td { background: rgba(255,255,255,0.01); }
  .empty-state { text-align: center; padding: 4rem 2rem; color: #64748b; }
  .empty-state-icon { font-size: 3rem; margin-bottom: 1rem; opacity: 0.5; }
</style>
</head>
<body>
<div class="navbar">
  <div class="brand-section">
    <div class="brand-logo">🛸</div>
    <div class="brand-title">
      <h1>Simulator Transformasi Laplace Rangkaian Seri</h1>
      <p>Analisis Respons Transien Matematika Teknik & Rangkaian RL / RC / RLC Seri</p>
    </div>
  </div>
</div>
<div class="dashboard-container">
  <div class="sidebar">
    <div>
      <div class="sidebar-section-title">⚙️ Tipe Rangkaian</div>
      <div class="circuit-tabs" style="margin-top: 10px;">
        <button class="tab-btn active" onclick="setCircuit('RL')">RL Seri</button>
        <button class="tab-btn" onclick="setCircuit('RC')">RC Seri</button>
        <button class="tab-btn" onclick="setCircuit('RLC')">RLC Seri</button>
      </div>
    </div>
    <div>
      <div class="sidebar-section-title">📊 Parameter Fisik</div>
      <div style="display: flex; flex-direction: column; gap: 1.25rem; margin-top: 12px;">
        <div class="param-group">
          <div class="param-label-container"><label for="slide-R">Resistansi (R) [Ohm]</label><span class="param-value" id="lbl-R">500.00</span></div>
          <input type="range" id="slide-R" class="slider-input" min="1" max="2000" value="500" oninput="syncParam('R', this.value)">
        </div>
        <div class="param-group" id="container-L">
          <div class="param-label-container"><label for="slide-L">Induktansi (L) [Henry]</label><span class="param-value" id="lbl-L">27.00</span></div>
          <input type="range" id="slide-L" class="slider-input" min="0.1" max="100" step="0.1" value="27" oninput="syncParam('L', this.value)">
        </div>
        <div class="param-group" id="container-C" style="display:none;">
          <div class="param-label-container"><label for="slide-C">Kapasitansi (C) [Farad]</label><span class="param-value" id="lbl-C">0.0012</span></div>
          <input type="range" id="slide-C" class="slider-input" min="0.0001" max="0.05" step="0.0001" value="0.0012" oninput="syncParam('C', this.value)">
        </div>
        <div class="param-group">
          <div class="param-label-container"><label for="slide-V">Tegangan DC Sumber (V) [Volt]</label><span class="param-value" id="lbl-V">20.00</span></div>
          <input type="range" id="slide-V" class="slider-input" min="1" max="250" value="20" oninput="syncParam('V', this.value)">
        </div>
      </div>
    </div>
    <div>
      <div class="sidebar-section-title">⏱️ Rentang Waktu Simulasi</div>
      <div style="margin-top: 12px;">
        <div class="param-group">
          <div class="input-number-wrapper">
            <button onclick="adjustTmax(-5)">-</button>
            <input type="number" id="inp-tmax" class="input-number-raw" value="100" min="1" max="1000" onchange="runSimulation()">
            <button onclick="adjustTmax(5)">+</button>
          </div>
        </div>
      </div>
    </div>
    <button class="calc-btn" onclick="runSimulation()">▶ JALANKAN SIMULASI</button>
    <button class="reset-btn" onclick="resetToDefault()">↺ Reset Parameter</button>
  </div>
  <div class="main-content" id="workspace"></div>
</div>
<script>
let activeCircuit = 'RL';
function setCircuit(type) {
  activeCircuit = type;
  document.querySelectorAll('.tab-btn').forEach((btn, idx) => { btn.classList.toggle('active', ['RL','RC','RLC'][idx] === type); });
  document.getElementById('container-L').style.display = ['RL','RLC'].includes(type) ? '' : 'none';
  document.getElementById('container-C').style.display = ['RC','RLC'].includes(type) ? '' : 'none';
  runSimulation();
}
function syncParam(param, value) {
  document.getElementById('lbl-' + param).textContent = param === 'C' ? parseFloat(value).toFixed(4) : parseFloat(value).toFixed(2);
  runSimulation();
}
function adjustTmax(amount) {
  const input = document.getElementById('inp-tmax');
  input.value = Math.max(1, (parseInt(input.value) || 100) + amount);
  runSimulation();
}
function resetToDefault() {
  document.getElementById('slide-R').value = 500; document.getElementById('slide-L').value = 27; document.getElementById('slide-C').value = 0.0012; document.getElementById('slide-V').value = 20; document.getElementById('inp-tmax').value = 100;
  syncParam('R', 500); syncParam('L', 27); syncParam('C', 0.0012); syncParam('V', 20);
}
function formatValue(num) { return Math.abs(num) < 1e-6 ? '0' : (Math.abs(num) >= 1e-3 && Math.abs(num) < 1e5 ? parseFloat(num.toFixed(4)).toString() : num.toExponential(3)); }
function generateTimeData(maxVal) { let p = []; for(let i=0; i<300; i++) p.push((maxVal * i) / 299); return p; }
function runSimulation() {
  const R = parseFloat(document.getElementById('slide-R').value), L = parseFloat(document.getElementById('slide-L').value)||1, C = parseFloat(document.getElementById('slide-C').value)||1, V = parseFloat(document.getElementById('slide-V').value), tmax = parseFloat(document.getElementById('inp-tmax').value)||100;
  let r = activeCircuit === 'RL' ? handleRL(R,L,V,tmax) : (activeCircuit === 'RC' ? handleRC(R,C,V,tmax) : handleRLC(R,L,C,V,tmax));
  renderWorkspace(r);
}
function handleRL(R,L,V,tmax) {
  const alpha = R/L, Iss = V/R, tau = 1/alpha, f = t => Iss * (1 - Math.exp(-alpha * t)), tP = generateTimeData(tmax);
  return { type:'RL', color:'#ef4444', formula:`i(t) = ${formatValue(Iss)} · (1 - e^(-${formatValue(alpha)}·t)) A`, derived:{"Alpha":formatValue(alpha),"Tau":formatValue(tau)+" s","Iss":formatValue(Iss)+" A"}, steps:[{title:"KVL",formula:"V = R·i(t) + L·[di/dt]"},{title:"Laplace Invers",formula:`i(t) = ${formatValue(Iss)} · (1 - e^(-${formatValue(alpha)}·t))`}], timePoints:tP, currentPoints:tP.map(f), svg:drawRL(), tmax };
}
function handleRC(R,C,V,tmax) {
  const alpha = 1/(R*C), Ip = V/R, tau = R*C, f = t => Ip * Math.exp(-alpha * t), tP = generateTimeData(tmax);
  return { type:'RC', color:'#3b82f6', formula:`i(t) = ${formatValue(Ip)} · e^(-${formatValue(alpha)}·t) A`, derived:{"Alpha":formatValue(alpha),"Tau":formatValue(tau)+" s","Iss":"0 A"}, steps:[{title:"KVL",formula:"V = R·i + 1/C ∫i dt"},{title:"Laplace Invers",formula:`i(t) = ${formatValue(Ip)} · e^(-${formatValue(alpha)}·t)`}], timePoints:tP, currentPoints:tP.map(f), svg:drawRC(), tmax };
}
function handleRLC(R,L,C,V,tmax) {
  const alpha = R/(2*L), w0 = 1/Math.sqrt(L*C), disc = (R/L)*(R/L) - 4/(L*C);
  let f, form, reg = disc>0 ? "Overdamped" : (disc===0 ? "Critically Damped" : "Underdamped");
  if(disc>0){ const s1=-alpha+Math.sqrt(disc/4), s2=-alpha-Math.sqrt(disc/4), A=(V/L)/(s1-s2); f=t=>A*(Math.exp(s1*t)-Math.exp(s2*t)); form=`i(t) = ${formatValue(A)} · [e^(${formatValue(s1)}t) - e^(${formatValue(s2)}t)] A`; }
  else if(disc===0){ const A=V/L; f=t=>A*t*Math.exp(-alpha*t); form=`i(t) = ${formatValue(A)} · t · e^(-${formatValue(alpha)}t) A`; }
  else { const wd=Math.sqrt(w0*w0-alpha*alpha), A=(V/L)/wd; f=t=>A*Math.exp(-alpha*t)*Math.sin(wd*t); form=`i(t) = ${formatValue(A)} · e^(-${formatValue(alpha)}t) · sin(${formatValue(wd)}t) A`; }
  const tP = generateTimeData(tmax);
  return { type:'RLC', color:'#10b981', formula:form, derived:{"Alpha":formatValue(alpha),"Omega0":formatValue(w0),"Regime":reg}, steps:[{title:"KVL RLC",formula:"L i'' + R i' + 1/C i = 0"},{title:"Regime",formula:reg}], timePoints:tP, currentPoints:tP.map(f), svg:drawRLC(), tmax };
}
function renderWorkspace(r) {
  let stats = Object.entries(r.derived).map(([k,v]) => `<div class="mini-stat-card"><div class="mini-stat-label">${k}</div><div class="mini-stat-value" style="color:${r.color}">${v}</div></div>`).join('');
  let steps = r.steps.map((s,i) => `<div class="step-item"><div class="step-badge" style="border-color:${r.color};color:${r.color};background:${r.color}10">${i+1}</div><div><div class="step-text-title">${s.title}</div><div class="step-text-formula">${s.formula}</div></div></div>`).join('');
  let rows = ""; const inter = r.tmax/6;
  for(let x=0; x<=r.tmax; x+=inter) { let idx = r.timePoints.findIndex(v=>v>=x); if(idx>=0) rows+=`<tr><td>${r.timePoints[idx].toFixed(2)} s</td><td>${r.currentPoints[idx].toExponential(4)} A</td></tr>`; }
  document.getElementById('workspace').innerHTML = `
    <div style="margin-bottom:1.5rem;"><h2>📈 Grafik Respons Transien Rangkaian ${r.type}</h2><p style="color:#94a3b8;font-size:0.9rem;">Kalkulasi matematika Transformasi Laplace real-time.</p></div>
    <div class="dashboard-grid">
      <div style="display:flex;flex-direction:column;gap:1.5rem;">
        <div class="card"><div class="card-title">📈 Kurva Respons Arus i(t)</div><div style="position:relative;height:280px;"><canvas id="canvas-chart"></canvas></div></div>
        <div class="card"><div class="card-title">📐 Formulasi Hasil Laplace</div><div class="formula-box" style="border-left-color:${r.color}">${r.formula}</div><div class="results-grid-mini">${stats}</div></div>
        <div class="card"><div class="card-title">📝 Langkah Penyelesaian</div><div class="steps-list">${steps}</div></div>
      </div>
      <div style="display:flex;flex-direction:column;gap:1.5rem;">
        <div class="card"><div class="card-title">✈️ Skema Visual</div><div class="visual-panel">${r.svg}</div></div>
        <div class="card"><div class="card-title">📋 Tabel Sampling</div><table><thead><tr><th>Waktu</th><th>Arus</th></tr></thead><tbody>${rows}</tbody></table></div>
      </div>
    </div>`;
  renderChartObject(r);
}
let activeChart = null;
function renderChartObject(r) {
  if(activeChart) activeChart.destroy();
  activeChart = new Chart(document.getElementById('canvas-chart').getContext('2d'), {
    type: 'line', data: { labels: r.timePoints.map(t=>t.toFixed(1)), datasets: [{ data: r.currentPoints, borderColor: r.color, backgroundColor: r.color+'10', fill: true, borderWidth: 2, pointRadius: 0, tension: 0.3 }] },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { grid: { color: '#22273a' }, ticks: { color: '#64748b', maxTicksLimit: 12 } }, y: { grid: { color: '#22273a' }, ticks: { color: '#64748b' } } } }
  });
}
function drawRL() { return `<svg width="100%" height="130" viewBox="0 0 240 130"><rect width="240" height="130" rx="6" fill="#11131e"/><path d="M 30 90 L 30 30 L 90 30" fill="none" stroke="#475569" stroke-width="2"/><rect x="90" y="22" width="40" height="16" fill="#1e293b" stroke="#ef4444" stroke-width="2" rx="2"/><path d="M 130 30 L 160 30 Q 165 20 170 30 Q 175 20 180 30 Q 185 20 190 30 L 210 30 L 210 90 L 30 90" fill="none" stroke="#475569" stroke-width="2"/><circle cx="30" cy="60" r="10" fill="#1e293b" stroke="#3b82f6" stroke-width="2"/><text x="26" y="63" fill="#ffffff" font-size="10">V</text></svg>`; }
function drawRC() { return `<svg width="100%" height="130" viewBox="0 0 240 130"><rect width="240" height="130" rx="6" fill="#11131e"/><path d="M 30 90 L 30 30 L 90 30" fill="none" stroke="#475569" stroke-width="2"/><rect x="90" y="22" width="40" height="16" fill="#1e293b" stroke="#3b82f6" stroke-width="2" rx="2"/><path d="M 130 30 L 165 30 M 165 18 L 165 42 M 173 18 L 173 42 M 173 30 L 210 30 L 210 90 L 30 90" fill="none" stroke="#475569" stroke-width="2"/><circle cx="30" cy="60" r="10" fill="#1e293b" stroke="#3b82f6" stroke-width="2"/><text x="26" y="63" fill="#ffffff" font-size="10">V</text></svg>`; }
function drawRLC() { return `<svg width="100%" height="130" viewBox="0 0 240 130"><rect width="240" height="130" rx="6" fill="#11131e"/><path d="M 30 90 L 30 30 L 70 30" fill="none" stroke="#475569" stroke-width="2"/><rect x="70" y="24" width="30" height="12" fill="#1e293b" stroke="#10b981" stroke-width="2" rx="1"/><path d="M 100 30 L 120 30 Q 124 22 128 30 Q 132 22 136 30 L 165 30 M 165 20 L 165 40 M 171 20 L 171 40 M 171 30 L 210 30 L 210 90 L 30 90" fill="none" stroke="#475569" stroke-width="2"/><circle cx="30" cy="60" r="10" fill="#1e293b" stroke="#3b82f6" stroke-width="2"/><text x="26" y="63" fill="#ffffff" font-size="10">V</text></svg>`; }
window.onload = function() { resetToDefault(); };
</script>
</body>
</html>
"""

# Komponen inti Streamlit untuk merender full-HTML di atas ke web secara responsif
components.html(html_code, height=900, scroller=True)
