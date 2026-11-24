"""
QuantumCalc • Advanced Scientific Calculator
Dual-Mode Application Entry Point:
- Desktop: Tkinter GUI with High-DPI support when run locally (python main.py)
- Cloud / Web: Vercel Serverless Function & Web App (exports 'app', 'application', 'handler')
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import urllib.parse

# Ensure local calculator module is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from calculator.engine import CalculatorEngine

# Initialize global engine instance for serverless requests
server_engine = CalculatorEngine(angle_mode="DEG")

WEB_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>QuantumCalc • Advanced Scientific Calculator</title>
  <link rel="icon" type="image/png" href="https://raw.githubusercontent.com/teju-developer/calculater.py/main/assets/calculator_icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-app: #0c0a14;
      --bg-surface: #141122;
      --bg-display: #100d1e;
      --border-color: #261f42;
      --fg-text: #f8fafc;
      --fg-muted: #94a3b8;
      --accent-primary: #8b5cf6;
      --accent-secondary: #a855f7;
      --accent-highlight: #06b6d4;
      --btn-num-bg: #1c1830;
      --btn-num-fg: #f1f5f9;
      --btn-num-hover: #292347;
      --btn-op-bg: #251d3d;
      --btn-op-fg: #c084fc;
      --btn-op-hover: #362a57;
      --btn-sci-bg: #161329;
      --btn-sci-fg: #38bdf8;
      --btn-sci-hover: #221c3d;
      --btn-action-bg: #311822;
      --btn-action-fg: #f87171;
      --btn-action-hover: #46202f;
      --btn-equal-bg: #7c3aed;
      --btn-equal-fg: #ffffff;
      --btn-equal-hover: #6d28d9;
      --btn-mem-bg: #18142b;
      --btn-mem-fg: #cbd5e1;
      --history-bg: #100d1c;
      --history-card: #18142a;
    }

    [data-theme="ocean_blue"] {
      --bg-app: #070d19;
      --bg-surface: #0d1829;
      --bg-display: #091220;
      --border-color: #172a45;
      --fg-text: #f0f9ff;
      --fg-muted: #7dd3fc;
      --accent-primary: #0284c7;
      --accent-secondary: #00f2fe;
      --accent-highlight: #38bdf8;
      --btn-num-bg: #112239;
      --btn-num-fg: #f8fafc;
      --btn-num-hover: #193152;
      --btn-op-bg: #152c4a;
      --btn-op-fg: #38bdf8;
      --btn-op-hover: #1d3d66;
      --btn-sci-bg: #0e1d32;
      --btn-sci-fg: #22d3ee;
      --btn-sci-hover: #172d4c;
      --btn-action-bg: #2c1722;
      --btn-action-fg: #fb7185;
      --btn-action-hover: #422030;
      --btn-equal-bg: #0284c7;
      --btn-equal-fg: #ffffff;
      --btn-equal-hover: #0369a1;
      --btn-mem-bg: #0f2036;
      --btn-mem-fg: #bae6fd;
      --history-bg: #08101e;
      --history-card: #0f2038;
    }

    [data-theme="light_minimal"] {
      --bg-app: #f1f5f9;
      --bg-surface: #ffffff;
      --bg-display: #f8fafc;
      --border-color: #cbd5e1;
      --fg-text: #0f172a;
      --fg-muted: #64748b;
      --accent-primary: #4f46e5;
      --accent-secondary: #6366f1;
      --accent-highlight: #0ea5e9;
      --btn-num-bg: #ffffff;
      --btn-num-fg: #0f172a;
      --btn-num-hover: #f1f5f9;
      --btn-op-bg: #ede9fe;
      --btn-op-fg: #6d28d9;
      --btn-op-hover: #ddd6fe;
      --btn-sci-bg: #f8fafc;
      --btn-sci-fg: #0284c7;
      --btn-sci-hover: #e2e8f0;
      --btn-action-bg: #fee2e2;
      --btn-action-fg: #dc2626;
      --btn-action-hover: #fecaca;
      --btn-equal-bg: #4f46e5;
      --btn-equal-fg: #ffffff;
      --btn-equal-hover: #4338ca;
      --btn-mem-bg: #f1f5f9;
      --btn-mem-fg: #475569;
      --history-bg: #f8fafc;
      --history-card: #ffffff;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
    body {
      background: var(--bg-app);
      color: var(--fg-text);
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 16px;
      transition: background 0.25s ease, color 0.25s ease;
    }

    .calc-wrapper {
      display: flex;
      gap: 16px;
      max-width: 960px;
      width: 100%;
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 24px;
      padding: 20px;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.45);
    }

    .main-panel {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .header-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 4px;
    }

    .brand {
      font-size: 0.85rem;
      font-weight: 800;
      letter-spacing: 1.5px;
      color: var(--accent-primary);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .mem-badge {
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--fg-muted);
      padding: 2px 6px;
      border-radius: 6px;
      transition: color 0.2s;
    }
    .mem-badge.active { color: var(--accent-highlight); background: rgba(6, 182, 212, 0.15); }

    .header-actions { display: flex; gap: 6px; }

    .pill-btn {
      background: var(--btn-sci-bg);
      color: var(--btn-sci-fg);
      border: 1px solid var(--border-color);
      padding: 5px 10px;
      border-radius: 10px;
      font-size: 0.75rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
      transition: all 0.15s;
    }
    .pill-btn:hover { background: var(--btn-sci-hover); color: var(--fg-text); transform: translateY(-1px); }

    .display-card {
      background: var(--bg-display);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 16px 20px;
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      min-height: 95px;
      justify-content: space-between;
    }

    .expr-line {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.95rem;
      color: var(--fg-muted);
      min-height: 20px;
      word-break: break-all;
      text-align: right;
    }

    .result-line {
      font-family: 'JetBrains Mono', monospace;
      font-size: 2.2rem;
      font-weight: 700;
      color: var(--fg-text);
      word-break: break-all;
      text-align: right;
      transition: color 0.15s;
    }
    .result-line.has-result { color: var(--accent-secondary); }
    .result-line.error { color: var(--btn-action-fg); font-size: 1.5rem; }

    .mem-bar {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 6px;
    }
    .mem-btn {
      background: var(--btn-mem-bg);
      color: var(--btn-mem-fg);
      border: 1px solid var(--border-color);
      padding: 6px 0;
      border-radius: 8px;
      font-size: 0.75rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.15s;
    }
    .mem-btn:hover { background: var(--btn-num-hover); color: var(--fg-text); }

    .keypad-grid {
      display: grid;
      grid-template-columns: 3fr 4fr;
      gap: 12px;
      margin-top: 4px;
    }
    .keypad-grid.standard-only { grid-template-columns: 1fr; }
    .keypad-grid.standard-only .sci-col { display: none; }

    .sci-col {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
    }

    .std-col {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
    }

    .btn {
      height: 52px;
      border-radius: 12px;
      border: 1px solid var(--border-color);
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 1.05rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.12s ease;
      outline: none;
    }
    .btn:active { transform: scale(0.96); }

    .btn-num { background: var(--btn-num-bg); color: var(--btn-num-fg); }
    .btn-num:hover { background: var(--btn-num-hover); }

    .btn-op { background: var(--btn-op-bg); color: var(--btn-op-fg); }
    .btn-op:hover { background: var(--btn-op-hover); }

    .btn-sci { background: var(--btn-sci-bg); color: var(--btn-sci-fg); font-size: 0.9rem; }
    .btn-sci:hover { background: var(--btn-sci-hover); color: var(--fg-text); }

    .btn-action { background: var(--btn-action-bg); color: var(--btn-action-fg); }
    .btn-action:hover { background: var(--btn-action-hover); }

    .btn-equal { background: var(--btn-equal-bg); color: var(--btn-equal-fg); border: none; }
    .btn-equal:hover { background: var(--btn-equal-hover); box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4); }

    /* History Drawer */
    .history-drawer {
      width: 250px;
      background: var(--history-bg);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      transition: all 0.2s ease;
    }
    .history-drawer.hidden { display: none; }

    .hist-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 8px;
    }
    .hist-title { font-size: 0.9rem; font-weight: 700; }
    .hist-clear {
      background: transparent;
      border: none;
      color: var(--btn-action-fg);
      font-size: 0.75rem;
      font-weight: 700;
      cursor: pointer;
    }

    .hist-list {
      flex: 1;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 6px;
      max-height: 380px;
    }
    .hist-item {
      background: var(--history-card);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 8px 10px;
      cursor: pointer;
      transition: all 0.15s;
    }
    .hist-item:hover { border-color: var(--accent-primary); transform: translateX(2px); }
    .hist-time { font-size: 0.7rem; color: var(--fg-muted); }
    .hist-expr { font-size: 0.85rem; color: var(--fg-text); font-family: 'JetBrains Mono', monospace; word-break: break-all; }
    .hist-res { font-size: 0.95rem; font-weight: 700; color: var(--accent-primary); text-align: right; }

    .footer {
      margin-top: 14px;
      text-align: center;
      font-size: 0.8rem;
      color: var(--fg-muted);
    }
    .footer a { color: var(--accent-highlight); text-decoration: none; font-weight: 600; }

    @media (max-width: 768px) {
      .calc-wrapper { flex-direction: column; padding: 14px; }
      .keypad-grid { grid-template-columns: 1fr; }
      .history-drawer { width: 100%; max-height: 200px; }
    }
  </style>
</head>
<body data-theme="midnight_purple">

  <div class="calc-wrapper">
    <div class="main-panel">
      <!-- Top Bar -->
      <div class="header-bar">
        <div class="brand">
          <span>⚡</span> QUANTUM•CALC
          <span class="mem-badge" id="memBadge">[ M ]</span>
        </div>
        <div class="header-actions">
          <button class="pill-btn" onclick="toggleMode()" id="modeBtn">🔬 Scientific</button>
          <button class="pill-btn" onclick="toggleAngle()" id="angleBtn">📐 DEG</button>
          <button class="pill-btn" onclick="cycleTheme()" id="themeBtn">🔮 Theme</button>
          <button class="pill-btn" onclick="toggleHistory()" id="histBtn">🕒 History</button>
        </div>
      </div>

      <!-- Display -->
      <div class="display-card">
        <div class="expr-line" id="exprLine"></div>
        <div class="result-line" id="resultLine">0</div>
      </div>

      <!-- Memory Bar -->
      <div class="mem-bar">
        <button class="mem-btn" onclick="memClear()">MC</button>
        <button class="mem-btn" onclick="memRecall()">MR</button>
        <button class="mem-btn" onclick="memAdd()">M+</button>
        <button class="mem-btn" onclick="memSub()">M-</button>
        <button class="mem-btn" onclick="memStore()">MS</button>
      </div>

      <!-- Keypad -->
      <div class="keypad-grid" id="keypadGrid">
        <!-- Scientific Keypad -->
        <div class="sci-col" id="sciCol">
          <button class="btn btn-sci" onclick="appendFunc('sin')">sin</button>
          <button class="btn btn-sci" onclick="appendFunc('cos')">cos</button>
          <button class="btn btn-sci" onclick="appendFunc('tan')">tan</button>
          <button class="btn btn-sci" onclick="appendFunc('asin')">asin</button>
          <button class="btn btn-sci" onclick="appendFunc('acos')">acos</button>
          <button class="btn btn-sci" onclick="appendFunc('atan')">atan</button>
          <button class="btn btn-sci" onclick="appendFunc('sqrt')">√x</button>
          <button class="btn btn-sci" onclick="applySquare()">x²</button>
          <button class="btn btn-sci" onclick="applyCube()">x³</button>
          <button class="btn btn-sci" onclick="appendToken('^')">xʸ</button>
          <button class="btn btn-sci" onclick="appendFunc('log')">log</button>
          <button class="btn btn-sci" onclick="appendFunc('ln')">ln</button>
          <button class="btn btn-sci" onclick="appendToken('!')">n!</button>
          <button class="btn btn-sci" onclick="appendFunc('abs')">|x|</button>
          <button class="btn btn-sci" onclick="appendToken('π')">π</button>
        </div>

        <!-- Standard Keypad -->
        <div class="std-col">
          <button class="btn btn-action" onclick="clearAll()">AC</button>
          <button class="btn btn-action" onclick="deleteChar()">DEL</button>
          <button class="btn btn-op" onclick="appendToken('%')">%</button>
          <button class="btn btn-op" onclick="appendToken('÷')">÷</button>

          <button class="btn btn-num" onclick="appendToken('7')">7</button>
          <button class="btn btn-num" onclick="appendToken('8')">8</button>
          <button class="btn btn-num" onclick="appendToken('9')">9</button>
          <button class="btn btn-op" onclick="appendToken('×')">×</button>

          <button class="btn btn-num" onclick="appendToken('4')">4</button>
          <button class="btn btn-num" onclick="appendToken('5')">5</button>
          <button class="btn btn-num" onclick="appendToken('6')">6</button>
          <button class="btn btn-op" onclick="appendToken('−')">−</button>

          <button class="btn btn-num" onclick="appendToken('1')">1</button>
          <button class="btn btn-num" onclick="appendToken('2')">2</button>
          <button class="btn btn-num" onclick="appendToken('3')">3</button>
          <button class="btn btn-op" onclick="appendToken('+')">+</button>

          <button class="btn btn-num" onclick="toggleSign()">±</button>
          <button class="btn btn-num" onclick="appendToken('0')">0</button>
          <button class="btn btn-num" onclick="appendToken('.')">.</button>
          <button class="btn btn-equal" onclick="calculateResult()">=</button>
        </div>
      </div>
    </div>

    <!-- History Drawer -->
    <div class="history-drawer hidden" id="historyDrawer">
      <div class="hist-head">
        <span class="hist-title">History</span>
        <button class="hist-clear" onclick="clearHistory()">🗑️ Clear</button>
      </div>
      <div class="hist-list" id="histList">
        <div style="text-align: center; color: var(--fg-muted); padding: 20px; font-size: 0.8rem;">No calculations yet.</div>
      </div>
    </div>
  </div>

  <div class="footer">
    Desktop Edition Available • Run <code>python main.py</code> locally • Powered by Safe AST Engine
  </div>

  <script>
    let expr = "";
    let angleMode = "DEG";
    let memory = 0;
    let isScientific = true;
    let hasResult = false;
    let history = JSON.parse(localStorage.getItem('qc_hist') || '[]');
    const themes = ["midnight_purple", "ocean_blue", "light_minimal"];
    let themeIdx = themes.indexOf(localStorage.getItem('qc_theme') || "midnight_purple");
    if (themeIdx === -1) themeIdx = 0;
    document.body.setAttribute('data-theme', themes[themeIdx]);

    const exprLine = document.getElementById('exprLine');
    const resultLine = document.getElementById('resultLine');
    const memBadge = document.getElementById('memBadge');
    const histDrawer = document.getElementById('historyDrawer');
    const histList = document.getElementById('histList');
    const keypadGrid = document.getElementById('keypadGrid');
    const modeBtn = document.getElementById('modeBtn');
    const angleBtn = document.getElementById('angleBtn');

    renderHistory();

    function updateDisplay(val, isRes = false, isErr = false) {
      resultLine.innerText = val || "0";
      resultLine.className = 'result-line' + (isRes ? ' has-result' : '') + (isErr ? ' error' : '');
    }

    function appendToken(t) {
      if (hasResult && "0123456789.π".includes(t)) {
        expr = "";
        hasResult = false;
      } else if (hasResult) {
        hasResult = false;
      }
      expr += t;
      updateDisplay(expr);
    }

    function appendFunc(f) {
      if (hasResult) {
        expr = f + "(" + expr + ")";
        hasResult = false;
      } else {
        expr += f + "(";
      }
      updateDisplay(expr);
    }

    function applySquare() {
      if (!expr) return;
      expr = "(" + expr + ")^2";
      updateDisplay(expr);
    }

    function applyCube() {
      if (!expr) return;
      expr = "(" + expr + ")^3";
      updateDisplay(expr);
    }

    function toggleSign() {
      if (!expr || expr === "0") return;
      if (expr.startsWith("-(") && expr.endsWith(")")) {
        expr = expr.slice(2, -1);
      } else if (expr.startsWith("-")) {
        expr = expr.slice(1);
      } else {
        expr = "-(" + expr + ")";
      }
      updateDisplay(expr);
    }

    function deleteChar() {
      if (hasResult) { clearAll(); return; }
      expr = expr.slice(0, -1);
      updateDisplay(expr || "0");
    }

    function clearAll() {
      expr = "";
      hasResult = false;
      exprLine.innerText = "";
      updateDisplay("0");
    }

    async function calculateResult() {
      if (!expr.trim()) return;
      const raw = expr;
      exprLine.innerText = raw + " =";

      try {
        const resp = await fetch('/api/calculate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ expression: raw, angle_mode: angleMode })
        });
        const data = await resp.json();
        if (data.ok) {
          updateDisplay(data.result, true);
          expr = String(data.result).replace(/\\s/g, '');
          hasResult = true;
          addHistory(raw, data.result);
        } else {
          updateDisplay(data.error || "Error", false, true);
          hasResult = true;
        }
      } catch (err) {
        // Fallback calculation in client
        updateDisplay("Error", false, true);
      }
    }

    function memClear() { memory = 0; updateMemBadge(); }
    function memRecall() { appendToken(String(memory)); }
    function memAdd() { memory += parseFloat(resultLine.innerText) || 0; updateMemBadge(); }
    function memSub() { memory -= parseFloat(resultLine.innerText) || 0; updateMemBadge(); }
    function memStore() { memory = parseFloat(resultLine.innerText) || 0; updateMemBadge(); }
    function updateMemBadge() {
      if (Math.abs(memory) > 1e-12) {
        memBadge.innerText = "[ M: " + memory + " ]";
        memBadge.classList.add('active');
      } else {
        memBadge.innerText = "[ M ]";
        memBadge.classList.remove('active');
      }
    }

    function toggleMode() {
      isScientific = !isScientific;
      keypadGrid.classList.toggle('standard-only', !isScientific);
      modeBtn.innerText = isScientific ? "🔬 Scientific" : "🔢 Standard";
    }

    function toggleAngle() {
      angleMode = angleMode === "DEG" ? "RAD" : "DEG";
      angleBtn.innerText = "📐 " + angleMode;
    }

    function cycleTheme() {
      themeIdx = (themeIdx + 1) % themes.length;
      const theme = themes[themeIdx];
      document.body.setAttribute('data-theme', theme);
      localStorage.setItem('qc_theme', theme);
    }

    function toggleHistory() {
      histDrawer.classList.toggle('hidden');
    }

    function addHistory(expression, result) {
      const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
      history.unshift({ expression, result, time: now });
      if (history.length > 50) history.pop();
      localStorage.setItem('qc_hist', JSON.stringify(history));
      renderHistory();
    }

    function clearHistory() {
      history = [];
      localStorage.removeItem('qc_hist');
      renderHistory();
    }

    function renderHistory() {
      if (!history.length) {
        histList.innerHTML = '<div style="text-align:center;color:var(--fg-muted);padding:20px;font-size:0.8rem;">No calculations yet.</div>';
        return;
      }
      histList.innerHTML = history.map(item => `
        <div class="hist-item" onclick="loadHist('${item.result}')">
          <div class="hist-time">${item.time}</div>
          <div class="hist-expr">${item.expression}</div>
          <div class="hist-res">= ${item.result}</div>
        </div>
      `).join('');
    }

    function loadHist(res) {
      expr = String(res).replace(/\\s/g, '');
      updateDisplay(res, true);
      hasResult = true;
    }

    // Keyboard support
    window.addEventListener('keydown', (e) => {
      if (e.key >= '0' && e.key <= '9') appendToken(e.key);
      else if (e.key === '+') appendToken('+');
      else if (e.key === '-') appendToken('−');
      else if (e.key === '*') appendToken('×');
      else if (e.key === '/') { e.preventDefault(); appendToken('÷'); }
      else if (e.key === '.') appendToken('.');
      else if (e.key === '%') appendToken('%');
      else if (e.key === '(' || e.key === ')') appendToken(e.key);
      else if (e.key === '^') appendToken('^');
      else if (e.key === '!') appendToken('!');
      else if (e.key === 'Enter' || e.key === '=') { e.preventDefault(); calculateResult(); }
      else if (e.key === 'Backspace') deleteChar();
      else if (e.key === 'Escape') clearAll();
    });
  </script>
</body>
</html>"""


# ----------------- Vercel WSGI / HTTP Serverless Handlers -----------------

def app(environ, start_response):
    """
    Standard WSGI entrypoint for Vercel Serverless Function runtime.
    Serves the QuantumCalc Web App and evaluates /api/calculate queries.
    """
    path = environ.get("PATH_INFO", "/")
    method = environ.get("REQUEST_METHOD", "GET")

    # API calculation endpoint
    if path == "/api/calculate" and method == "POST":
        try:
            content_length = int(environ.get("CONTENT_LENGTH", 0))
            body_bytes = environ["wsgi.input"].read(content_length)
            data = json.loads(body_bytes.decode("utf-8"))
            expression = data.get("expression", "")
            mode = data.get("angle_mode", "DEG")

            server_engine.set_angle_mode(mode)
            ok, res = server_engine.evaluate(expression)

            if ok:
                result_str = server_engine.format_result(res)
                response_data = json.dumps({"ok": True, "result": result_str})
                start_response("200 OK", [("Content-Type", "application/json")])
                return [response_data.encode("utf-8")]
            else:
                response_data = json.dumps({"ok": False, "error": str(res)})
                start_response("200 OK", [("Content-Type", "application/json")])
                return [response_data.encode("utf-8")]
        except Exception as e:
            err_data = json.dumps({"ok": False, "error": f"Server Error: {str(e)}"})
            start_response("500 Internal Server Error", [("Content-Type", "application/json")])
            return [err_data.encode("utf-8")]

    # Default / Home route: Serve Interactive Web GUI
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
    return [WEB_HTML.encode("utf-8")]


# Alias for WSGI compatibility
application = app


class handler(BaseHTTPRequestHandler):
    """
    BaseHTTPRequestHandler entrypoint for Vercel HTTP handler runtime.
    """

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(WEB_HTML.encode("utf-8"))

    def do_POST(self):
        if self.path == "/api/calculate":
            try:
                length = int(self.headers.get("content-length", 0))
                body = self.rfile.read(length).decode("utf-8")
                data = json.loads(body)
                expression = data.get("expression", "")
                mode = data.get("angle_mode", "DEG")

                server_engine.set_angle_mode(mode)
                ok, res = server_engine.evaluate(expression)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                if ok:
                    result_str = server_engine.format_result(res)
                    resp = json.dumps({"ok": True, "result": result_str})
                else:
                    resp = json.dumps({"ok": False, "error": str(res)})
                self.wfile.write(resp.encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"ok": False, "error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


# ----------------- Desktop Application Launcher -----------------

def enable_high_dpi_awareness():
    """Enable high-DPI awareness on Windows for crystal-clear font rendering."""
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            try:
                import ctypes
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass


def run_desktop():
    """Launch the Tkinter desktop GUI when running on a local desktop."""
    enable_high_dpi_awareness()
    import tkinter as tk
    from calculator.ui import CalculatorUI

    root = tk.Tk()
    ui = CalculatorUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_desktop()
