import streamlit as st
import streamlit.components.v1 as components

# Mengatur konfigurasi halaman Streamlit agar memenuhi layar (Wide Mode)
st.set_page_config(layout="wide", page_title="ROBOLINK-RLC Simulator")

# Seluruh kode HTML dimasukkan ke dalam variabel string triple-quotes Python
html_code = """
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>ROBOLINK-RLC | Wireless Communication System</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background: #030609;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: flex-start;
      padding: 24px 16px;
      font-family: 'Share Tech Mono', monospace;
    }

    .app {
      background: #060a10;
      color: #b0c4d8;
      width: 100%;
      max-width: 1100px;
      border-radius: 16px;
      padding: 24px;
      position: relative;
      overflow: hidden;
      border: 1px solid #0e2a1e;
    }

    /* Background effects */
    .dots-bg {
      position: absolute; inset: 0;
      background-image: radial-gradient(rgba(0,255,180,0.06) 1px, transparent 1px);
      background-size: 28px 28px;
      pointer-events: none; z-index: 0;
    }
    .scanline {
      position: absolute; inset: 0;
      background: repeating-linear-gradient(
        0deg, transparent, transparent 3px,
        rgba(0,255,180,0.012) 3px, rgba(0,255,180,0.012) 4px
      );
      pointer-events: none; z-index: 0;
    }
    .glow-corner {
      position: absolute;
      width: 120px; height: 120px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(0,255,180,0.07), transparent 70%);
      pointer-events: none; z-index: 0;
    }
    .glow-tl { top: -30px; left: -30px; }
    .glow-br { bottom: -30px; right: -30px; }

    /* Corner brackets */
    .corner { position: absolute; width: 16px; height: 16px; z-index: 2; }
    .c-tl { top: 10px; left: 10px; border-top: 2px solid #00ffb4; border-left: 2px solid #00ffb4; }
    .c-tr { top: 10px; right: 10px; border-top: 2px solid #00ffb4; border-right: 2px solid #00ffb4; }
    .c-bl { bottom: 10px; left: 10px; border-bottom: 2px solid #00ffb4; border-left: 2px solid #00ffb4; }
    .c-br { bottom: 10px; right: 10px; border-bottom: 2px solid #00ffb4; border-right: 2px solid #00ffb4; }

    .z1 { position: relative; z-index: 1; }

    /* ---- TOP BAR ---- */
    .top-bar {
      display: flex; align-items: center;
      justify-content: space-between;
      margin-bottom: 20px;
      border-bottom: 1px solid #0e2a1e;
      padding-bottom: 14px;
    }
    .logo {
      font-family: 'Orbitron', monospace;
      font-size: 16px; font-weight: 700;
      color: #00ffb4; letter-spacing: 4px;
    }
    .logo span {
      color: #3a6a8a; font-size: 10px;
      font-family: 'Share Tech Mono', monospace;
      letter-spacing: 2px; display: block; margin-top: 3px;
    }
    .status-row { display: flex; align-items: center; gap: 10px; }
    .dot {
      width: 9px; height: 9px; border-radius: 50%;
      background: #00ffb4; animation: pulse 1.4s infinite;
    }
    .dot.warn { background: #ffaa00; }
    .dot.off  { background: #ff4466; animation: none; }
    @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.25} }
    .status-txt { font-size: 11px; color: #3a6a8a; letter-spacing: 1px; }

    /* ---- MAIN GRID ---- */
    .main-grid {
      display: grid;
      grid-template-columns: 240px 1fr;
      gap: 14px;
    }

    /* ---- PANELS ---- */
    .panel {
      background: #0a1520;
      border: 1px solid #0e2a1e;
      border-radius: 8px;
      padding: 14px;
    }
    .panel-title {
      font-size: 9px; color: #00ffb4;
      letter-spacing: 2px; margin-bottom: 12px;
      border-bottom: 1px solid #0e2a1e;
      padding-bottom: 7px;
    }

    /* ---- ROBOT SVG ---- */
    .robot-wrap { text-align: center; margin-bottom: 12px; }
    .robot-svg { width: 80px; height: 100px; }

    .robot-status {
      display: flex; align-items: center; gap: 9px;
      background: #050d15; border: 1px solid #0e2a1e;
      border-radius: 7px; padding: 9px 12px; margin-bottom: 0;
    }
    .r-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
    .r-online { background: #00ffb4; box-shadow: 0 0 8px #00ffb4; }
    .r-warn   { background: #ffaa00; box-shadow: 0 0 8px #ffaa00; }
    .r-offline{ background: #ff4466; }
    .r-msg { font-size: 11px; letter-spacing: 1px; }

    /* ---- PARAMS ---- */
    .side-panel { display: flex; flex-direction: column; gap: 12px; }

    .param-row { margin-bottom: 12px; }
    .param-lbl {
      font-size: 10px; color: #3a6a8a; letter-spacing: 1px;
      margin-bottom: 5px; display: flex;
      justify-content: space-between; align-items: center;
    }
    .param-lbl em { color: #00ffb4; font-style: normal; font-size: 12px; }

    input[type=range] {
      width: 100%; accent-color: #00ffb4;
      cursor: pointer; margin-bottom: 5px;
    }
    input[type=number] {
      width: 100%; background: #060a10;
      border: 1px solid #0e2a1e; color: #b0c4d8;
      font-family: 'Share Tech Mono', monospace;
      font-size: 13px; padding: 6px 9px;
      border-radius: 4px; outline: none;
      transition: border-color .2s;
    }
    input[type=number]:focus { border-color: #00ffb4; }

    .calc-btn {
      width: 100%; padding: 11px;
      background: transparent;
      border: 1px solid #00ffb4; color: #00ffb4;
      font-family: 'Orbitron', monospace;
      font-size: 10px; letter-spacing: 3px;
      cursor: pointer; border-radius: 5px;
      margin-top: 2px; transition: all .2s;
    }
    .calc-btn:hover { background: #002a1a; }
    .calc-btn:active { transform: scale(0.97); }

    /* ---- RIGHT PANEL ---- */
    .right-panel { display: flex; flex-direction: column; gap: 12px; }

    /* Metrics */
    .metrics {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
    }
    .m-card {
      background: #0a1520; border: 1px solid #0e2a1e;
      border-radius: 7px; padding: 11px; text-align: center;
    }
    .m-lbl { font-size: 8px; color: #3a6a8a; letter-spacing: 1px; margin-bottom: 5px; }
    .m-val {
      font-family: 'Orbitron', monospace;
      font-size: 15px; font-weight: 700;
    }
    .m-unit { font-size: 8px; color: #3a6a8a; margin-top: 3px; }
    .c-green { color: #00ffb4; }
    .c-blue  { color: #00aaff; }
    .c-amber { color: #ffaa00; }
    .c-pink  { color: #ff44aa; }

    /* Formula */
    .formula-box {
      background: #0a1520; border: 1px solid #0e2a1e;
      border-radius: 8px; padding: 14px;
    }
    .f-title { font-size: 9px; color: #00ffb4; letter-spacing: 2px; margin-bottom: 8px; }
    .f-eq {
      font-family: 'Share Tech Mono', monospace;
      font-size: 14px; color: #ffaa00;
      min-height: 22px; word-break: break-all;
    }
    .f-sub { font-size: 10px; color: #3a6a8a; margin-top: 6px; line-height: 1.7; }

    /* Chart */
    .chart-box {
      background: #0a1520; border: 1px solid #0e2a1e;
      border-radius: 8px; padding: 14px;
    }
    .chart-header {
      display: flex; justify-content: space-between;
      align-items: center; margin-bottom: 10px;
    }
    .chart-title { font-size: 9px; color: #00ffb4; letter-spacing: 2px; }
    .mode-badge {
      font-size: 9px; padding: 2px 9px;
      border-radius: 3px; letter-spacing: 1px;
    }
    .mb-under { background: #001a30; color: #00aaff; border: 1px solid #004488; }
    .mb-over  { background: #1a0a00; color: #ffaa00; border: 1px solid #884400; }
    .mb-crit  { background: #0d001a; color: #ff44aa; border: 1px solid #660088; }

    /* Signal row */
    .signal-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }

    /* Signal bar */
    .bar-row { display: flex; align-items: center; gap: 8px; margin-bottom: 7px; }
    .bar-lbl { font-size: 10px; color: #3a6a8a; width: 80px; flex-shrink: 0; }
    .bar-track {
      flex: 1; height: 6px; background: #060a10;
      border-radius: 3px; overflow: hidden;
    }
    .bar-fill { height: 100%; border-radius: 3px; transition: width .6s; }
    .bar-pct { font-size: 10px; width: 34px; text-align: right; }

    /* Char list */
    .char-item {
      font-size: 11px; display: flex;
      align-items: center; gap: 8px;
      padding: 3px 0; border-bottom: 1px solid #0e2a1e;
    }
    .char-item:last-child { border-bottom: none; }
    .char-ico { color: #00ffb4; flex-shrink: 0; }

    /* Footer Credits */
    .footer-credits {
      width: 100%;
      max-width: 1100px;
      margin-top: 12px;
      text-align: right;
      font-size: 11px;
      color: #3a6a8a;
      letter-spacing: 2px;
      font-family: 'Orbitron', sans-serif;
    }
    .footer-credits span {
      color: #00ffb4;
      font-weight: 700;
    }

    /* Responsive */
    @media (max-width: 750px) {
      .main-grid { grid-template-columns: 1fr; }
      .metrics { grid-template-columns: repeat(2, 1fr); }
      .signal-row { grid-template-columns: 1fr; }
      .footer-credits { text-align: center; }
    }
  </style>
</head>
<body>

<div class="app">
  <div class="dots-bg"></div>
  <div class="scanline"></div>
  <div class="glow-corner glow-tl"></div>
  <div class="glow-corner glow-br"></div>
  <div class="corner c-tl"></div>
  <div class="corner c-tr"></div>
  <div class="corner c-bl"></div>
  <div class="corner c-br"></div>

  <div class="z1">

    <div class="top-bar">
      <div class="logo">
        ⚡ ROBOLINK-RLC
        <span>// WIRELESS COMMUNICATION SYSTEM v2.0 — Transformasi Laplace</span>
      </div>
      <div class="status-row">
        <div class="dot" id="sys-dot"></div>
        <span class="status-txt" id="sys-status">SYSTEM ONLINE</span>
      </div>
    </div>

    <div class="main-grid">

      <div class="side-panel">

        <div class="panel">
          <div class="panel-title">// ROBOT NODE</div>
          <div class="robot-wrap">
            <svg class="robot-svg" viewBox="0 0 80 100" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="18" y="6" width="44" height="30" rx="6" fill="#0a2030" stroke="#00ffb4" stroke-width="1.3"/>
              <rect x="26" y="14" width="10" height="8" rx="3" fill="#00ffb4" opacity="0.85"/>
              <rect x="44" y="14" width="10" height="8" rx="3" fill="#00aaff" opacity="0.85"/>
              <rect x="30" y="27" width="20" height="4" rx="2" fill="#ffaa00" opacity="0.7"/>
              <line x1="40" y1="6" x2="40" y2="0" stroke="#00ffb4" stroke-width="1.8"/>
              <circle cx="40" cy="0" r="2.5" fill="#00ffb4" opacity="0.9"/>
              <rect x="12" y="38" width="56" height="32" rx="5" fill="#0a2030" stroke="#00aaff" stroke-width="1.1"/>
              <rect x="18" y="44" width="18" height="16" rx="3" fill="#060a10" stroke="#00ffb4" stroke-width="0.8"/>
              <rect x="44" y="44" width="18" height="16" rx="3" fill="#060a10" stroke="#3a6a8a" stroke-width="0.8"/>
              <circle cx="27" cy="52" r="5" fill="#00ffb4" opacity="0.45"/>
              <circle cx="53" cy="52" r="4" fill="#00aaff" opacity="0.4"/>
              <rect x="5" y="40" width="8" height="18" rx="4" fill="#0a2030" stroke="#3a6a8a" stroke-width="0.9"/>
              <rect x="67" y="40" width="8" height="18" rx="4" fill="#0a2030" stroke="#3a6a8a" stroke-width="0.9"/>
              <rect x="18" y="72" width="16" height="24" rx="4" fill="#0a2030" stroke="#3a6a8a" stroke-width="0.9"/>
              <rect x="46" y="72" width="16" height="24" rx="4" fill="#0a2030" stroke="#3a6a8a" stroke-width="0.9"/>
              <rect x="14" y="91" width="22" height="7" rx="2.5" fill="#0a2030" stroke="#00aaff" stroke-width="0.8"/>
              <rect x="44" y="91" width="22" height="7" rx="2.5" fill="#0a2030" stroke="#00aaff" stroke-width="0.8"/>
            </svg>
          </div>
          <div class="robot-status">
            <div class="r-dot r-online" id="r-dot"></div>
            <span class="r-msg" id="r-msg" style="color:#00ffb4">ROBOT ONLINE</span>
          </div>
        </div>

        <div class="panel">
          <div class="panel-title">// PARAMETER RANGKAIAN RLC</div>

          <div class="param-row">
            <div class="param-lbl">RESISTOR <em id="lbl-R">500 Ω</em></div>
            <input type="range" id="sl-R" min="10" max="2000" value="500" step="10" oninput="syncSlider('R')">
            <input type="number" id="inp-R" value="500" min="0.1" oninput="syncInput('R')">
          </div>

          <div class="param-row">
            <div class="param-lbl">INDUKTOR <em id="lbl-L">27 H</em></div>
            <input type="range" id="sl-L" min="0.1" max="100" value="27" step="0.1" oninput="syncSlider('L')">
            <input type="number" id="inp-L" value="27" min="0.001" step="0.1" oninput="syncInput('L')">
          </div>

          <div class="param-row">
            <div class="param-lbl">KAPASITOR <em id="lbl-C">0.0012 F</em></div>
            <input type="range" id="sl-C" min="0.0001" max="0.01" value="0.0012" step="0.0001" oninput="syncSlider('C')">
            <input type="number" id="inp-C" value="0.0012" min="0.000001" step="0.0001" oninput="syncInput('C')">
          </div>

          <div class="param-row">
            <div class="param-lbl">TEGANGAN TX <em id="lbl-V">20 V</em></div>
            <input type="range" id="sl-V" min="1" max="100" value="20" step="1" oninput="syncSlider('V')">
            <input type="number" id="inp-V" value="20" min="0.1" oninput="syncInput('V')">
          </div>

          <button class="calc-btn" onclick="calculate()">▶ TRANSMIT SIGNAL</button>
        </div>

      </div><div class="right-panel">

        <div class="metrics">
          <div class="m-card">
            <div class="m-lbl">FREK. RESONANSI</div>
            <div class="m-val c-green" id="m-f0">—</div>
            <div class="m-unit">Hz</div>
          </div>
          <div class="m-card">
            <div class="m-lbl">FAKTOR REDAMAN ζ</div>
            <div class="m-val c-blue" id="m-zeta">—</div>
            <div class="m-unit">rasio</div>
          </div>
          <div class="m-card">
            <div class="m-lbl">KONSTANTA WAKTU τ</div>
            <div class="m-val c-amber" id="m-tau">—</div>
            <div class="m-unit">detik</div>
          </div>
          <div class="m-card">
            <div class="m-lbl">PUNCAK ARUS</div>
            <div class="m-val c-pink" id="m-ipeak">—</div>
            <div class="m-unit">Ampere</div>
          </div>
        </div>

        <div class="formula-box">
          <div class="f-title">// SOLUSI TRANSFORMASI LAPLACE → i(t)</div>
          <div class="f-eq" id="f-eq">Tekan TRANSMIT SIGNAL untuk menghitung...</div>
          <div class="f-sub" id="f-sub"></div>
        </div>

        <div class="chart-box">
          <div class="chart-header">
            <span class="chart-title">// GRAFIK SINYAL NIRKABEL i(t) vs WAKTU</span>
            <span class="mode-badge mb-under" id="mode-badge">—</span>
          </div>
          <div style="position:relative; height:220px;">
            <canvas id="main-chart"
              role="img"
              aria-label="Grafik arus i(t) sinyal nirkabel robot RLC terhadap waktu">
              Grafik arus nirkabel robot RLC terhadap waktu.
            </canvas>
          </div>
        </div>

        <div class="signal-row">

          <div class="panel">
            <div class="panel-title">// KUALITAS SINYAL TX → RX</div>
            <div id="sig-bars">
              <div style="font-size:11px;color:#3a6a8a;">Belum dihitung...</div>
            </div>
          </div>

          <div class="panel">
            <div class="panel-title">// KARAKTERISTIK SISTEM</div>
            <div id="char-list">
              <div class="char-item" style="color:#3a6a8a;">Belum dihitung...</div>
            </div>
          </div>

        </div></div></div></div></div><div class="footer-credits">
  DEVELOPED BY: <span>SYAFIQ AKHSAN</span>
</div>

<script>
  let chart = null;

  const units = { R: 'Ω', L: 'H', C: 'F', V: 'V' };

  function syncSlider(p) {
    const v = document.getElementById('sl-' + p).value;
    document.getElementById('inp-' + p).value = v;
    document.getElementById('lbl-' + p).textContent = parseFloat(v) + ' ' + units[p];
  }

  function syncInput(p) {
    const v = document.getElementById('inp-' + p).value;
    document.getElementById('sl-' + p).value = v;
    document.getElementById('lbl-' + p).textContent = parseFloat(v) + ' ' + units[p];
  }

  function barHtml(label, pct, color) {
    pct = Math.min(100, Math.max(0, pct));
    return `
      <div class="bar-row">
        <span class="bar-lbl">${label}</span>
        <div class="bar-track">
          <div class="bar-fill" style="width:${pct.toFixed(1)}%;background:${color};"></div>
        </div>
        <span class="bar-pct" style="color:${color}">${pct.toFixed(0)}%</span>
      </div>`;
  }

  function calculate() {
    console.log("Robolink-RLC Engine Core running. Authorized by: Syafiq Akhsan");

    const R  = parseFloat(document.getElementById('inp-R').value);
    const L  = parseFloat(document.getElementById('inp-L').value);
    const C  = parseFloat(document.getElementById('inp-C').value);
    const V  = parseFloat(document.getElementById('inp-V').value);

    const omega0 = 1 / Math.sqrt(L * C);
    const f0     = omega0 / (2 * Math.PI);
    const alpha  = R / (2 * L);
    const zeta   = R / (2 * Math.sqrt(L / C));
    const tau    = 1 / alpha;

    document.getElementById('m-f0').textContent   = f0 < 1 ? f0.toFixed(4) : f0.toFixed(3);
    document.getElementById('m-zeta').textContent = zeta.toFixed(4);
    document.getElementById('m-tau').textContent  = tau.toFixed(4);

    const N    = 350;
    const Tmax = Math.min(tau * 10, 30);
    const tArr = Array.from({ length: N }, (_, i) => i * Tmax / (N - 1));

    let iArr = [], formula = '', modeTxt = '', modeClass = '', charItems = [];

    if (zeta > 1) {
      const sd = Math.sqrt(alpha * alpha - omega0 * omega0);
      const s1 = -alpha + sd;
      const s2 = -alpha - sd;
      const A  =  (V / L) / (s1 - s2);
      const B  = -(V / L) / (s1 - s2);
      iArr     = tArr.map(t => A * Math.exp(s1 * t) + B * Math.exp(s2 * t));
      formula  = `i(t) = ${A.toFixed(5)}·e^(${s1.toFixed(3)}t) − ${Math.abs(B).toFixed(5)}·e^(${s2.toFixed(3)}t)  A`;
      modeTxt  = 'OVERDAMPED';
      modeClass = 'mb-over';
      charItems = [
        { ico: '▶', txt: 'Sistem teredam lebih', color: '#b0c4d8' },
        { ico: '▶', txt: 'Respons lambat & stabil', color: '#b0c4d8' },
        { ico: '▶', txt: 'Tanpa osilasi sinyal', color: '#b0c4d8' },
        { ico: '●', txt: `ζ = ${zeta.toFixed(4)}  (ζ > 1)`, color: '#ffaa00' },
      ];
    } else if (zeta < 1) {
      const wd = omega0 * Math.sqrt(1 - zeta * zeta);
      const A  = V / (L * wd);
      iArr     = tArr.map(t => A * Math.exp(-alpha * t) * Math.sin(wd * t));
      formula  = `i(t) = ${A.toFixed(5)}·e^(−${alpha.toFixed(3)}t)·sin(${wd.toFixed(3)}t)  A`;
      modeTxt  = 'UNDERDAMPED';
      modeClass = 'mb-under';
      charItems = [
        { ico: '▶', txt: 'Sistem teredam kurang', color: '#b0c4d8' },
        { ico: '▶', txt: 'Osilasi sinyal melemah', color: '#b0c4d8' },
        { ico: '▶', txt: 'Respons cepat, ada ringing', color: '#b0c4d8' },
        { ico: '●', txt: `ζ = ${zeta.toFixed(4)}  (ζ < 1)`, color: '#00aaff' },
      ];
    } else {
      const A = V / L;
      iArr    = tArr.map(t => A * t * Math.exp(-alpha * t));
      formula = `i(t) = ${A.toFixed(5)}·t·e^(−${alpha.toFixed(3)}t)  A`;
      modeTxt  = 'CRITICALLY DAMPED';
      modeClass = 'mb-crit';
      charItems = [
        { ico: '▶', txt: 'Teredam kritis — optimal', color: '#b0c4d8' },
        { ico: '▶', txt: 'Respons tercepat tanpa osilasi', color: '#b0c4d8' },
        { ico: '▶', txt: 'Ideal untuk komunikasi robot', color: '#b0c4d8' },
        { ico: '●', txt: `ζ = 1.0000  (kritis)`, color: '#ff44aa' },
      ];
    }

    const ipeak = Math.max(...iArr.map(Math.abs));
    document.getElementById('m-ipeak').textContent = ipeak.toFixed(5);

    document.getElementById('f-eq').textContent  = formula;
    document.getElementById('f-sub').innerHTML   =
      `ω₀ = ${omega0.toFixed(4)} rad/s &nbsp;|&nbsp; α = ${alpha.toFixed(4)} &nbsp;|&nbsp; ζ = ${zeta.toFixed(4)}<br>` +
      `s₁,₂ = −α ± √(α²−ω₀²) &nbsp;|&nbsp; τ = ${tau.toFixed(4)} s`;

    const badge = document.getElementById('mode-badge');
    badge.textContent = modeTxt;
    badge.className   = 'mode-badge ' + modeClass;

    document.getElementById('char-list').innerHTML = charItems.map(c =>
      `<div class="char-item">
        <span class="char-ico" style="color:${c.color}">${c.ico}</span>
        <span style="color:${c.color}">${c.txt}</span>
       </div>`
    ).join('');

    const snr        = Math.min(100, Math.max(5, (1 - Math.min(zeta, 3) / 3) * 100));
    const stability  = zeta <= 1 ? Math.min(100, zeta * 100) : Math.max(5, 100 - (zeta - 1) * 40);
    const bandwidth  = Math.min(100, (f0 / 10) * 100);
    const efficiency = Math.min(100, (ipeak / Math.max(V / R, 0.0001)) * 100);
    document.getElementById('sig-bars').innerHTML =
      barHtml('SNR',        snr,        '#00ffb4') +
      barHtml('STABILITY',  stability,  '#00aaff') +
      barHtml('BANDWIDTH',  bandwidth,  '#ffaa00') +
      barHtml('EFFICIENCY', efficiency, '#ff44aa');

    const rdot = document.getElementById('r-dot');
    const rmsg = document.getElementById('r-msg');
    const sdot = document.getElementById('sys-dot');
    if (zeta < 0.2) {
      rdot.className = 'r-dot r-warn'; rmsg.style.color = '#ffaa00';
      rmsg.textContent = 'SINYAL TIDAK STABIL';
      sdot.className = 'dot warn';
    } else if (zeta > 6) {
      rdot.className = 'r-dot r-offline'; rmsg.style.color = '#ff4466';
      rmsg.textContent = 'KONEKSI TERPUTUS';
      sdot.className = 'dot off';
    } else {
      rdot.className = 'r-dot r-online'; rmsg.style.color = '#00ffb4';
      rmsg.textContent = 'ROBOT ONLINE';
      sdot.className = 'dot';
    }

    const cLine = zeta > 1 ? '#ffaa00' : zeta < 1 ? '#00aaff' : '#ff44aa';
    const cFill = zeta > 1 ? 'rgba(255,170,0,0.10)' : zeta < 1 ? 'rgba(0,170,255,0.10)' : 'rgba(255,68,170,0.10)';

    if (chart) chart.destroy();
    chart = new Chart(document.getElementById('main-chart'), {
      type: 'line',
      data: {
        labels: tArr.map(t => t.toFixed(2)),
        datasets: [{
          label: 'i(t) [A]',
          data:  iArr.map(v => parseFloat(v.toFixed(8))),
          borderColor: cLine,
          backgroundColor: cFill,
          fill: true, pointRadius: 0,
          borderWidth: 2, tension: 0.3,
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: { label: ctx => `i(t) = ${ctx.parsed.y.toFixed(6)} A` },
            backgroundColor: '#0a1520',
            borderColor: cLine, borderWidth: 1,
            titleColor: '#3a6a8a', bodyColor: cLine,
            titleFont: { family: 'Share Tech Mono', size: 10 },
            bodyFont:  { family: 'Share Tech Mono', size: 11 },
          }
        },
        scales: {
          x: {
            ticks: { color: '#3a6a8a', font: { family: 'Share Tech Mono', size: 9 }, maxTicksLimit: 8, autoSkip: true },
            grid:  { color: 'rgba(0,255,180,0.04)' },
            border: { color: '#0e2a1e' },
            title: { display: true, text: 'Waktu (s)', color: '#3a6a8a', font: { family: 'Share Tech Mono', size: 9 } }
          },
          y: {
            ticks: { color: '#3a6a8a', font: { family: 'Share Tech Mono', size: 9 }, callback: v => v.toFixed(4) },
            grid:  { color: 'rgba(0,255,180,0.04)' },
            border: { color: '#0e2a1e' },
            title: { display: true, text: 'Arus (A)', color: '#3a6a8a', font: { family: 'Share Tech Mono', size: 9 } }
          }
        }
      }
    });
  }

  calculate();
</script>
</body>
</html>
"""

# Render komponen HTML dengan tinggi proporsional (misal: 800px atau menyesuaikan app)
components.html(html_code, height=750, scrolling=True)
