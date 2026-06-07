import streamlit as st
import streamlit.components.v1 as components

# 1. Mengatur konfigurasi halaman agar penuh (Wide Mode)
st.set_page_config(page_title="Kalkulator Laplace RLC", layout="wide")

# 2. String HTML yang sudah dibersihkan dari karakter backtick pengganggu interpreter Python
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
    margin-top: 6px;
    display: inline-block;
    font-size: 0.75rem;
    color: #34d399;
    background: rgba(52, 211, 153, 0.1);
    border: 1px solid rgba(52, 211, 153, 0.3);
    padding: 3px 10px;
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

  .circuit-tabs {
    display: flex; gap: 4px; margin-bottom: 1rem;
  }

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

  .tab-btn.active {
    background: #1e3a8a;
    border-color: #3b82f6;
    color: #93c5fd;
  }

  .tab-btn:hover:not(.active) {
    background: #1a2540;
    border-color: #2a3a6e;
    color: #93c5fd;
  }

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
    border-radius:
