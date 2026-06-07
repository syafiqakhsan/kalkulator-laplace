import streamlit as st
import streamlit.components.v1 as components

# Set konfigurasi halaman agar penuh (Wide Mode)
st.set_page_config(page_title="Kalkulator Laplace RLC", layout="wide")

# Kode HTML + JS baru dengan tambahan "By Syafiq" di bagian header
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
  .author-badge {
    margin-top: 4px;
    display: inline-block;
    font-size: 0.75rem;
    color: #34d399;
    background: rgba(52, 211, 153, 0.1);
    border: 1px solid rgba(52, 211, 153, 0.3);
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: bold;
    letter-spacing: 0.5px;
  }
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
    <div class="author-badge">⚙️ Created by Syafiq</div>
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
    b.classList.
