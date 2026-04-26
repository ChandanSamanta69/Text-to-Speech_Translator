"""
frontend.py — Streamlit UI Layer (Premium Colorful Edition)
==================================
All UI code lives here. Calls the Flask backend API over HTTP.
No direct imports from backend.py or api.py.
 
Run with:  streamlit run frontend.py
(Flask backend must be running separately: python backend.py)
"""
 
import base64
import logging
import os
import requests
import streamlit as st
from dotenv import load_dotenv
 
# ── Load environment variables from .env file ──
load_dotenv()
 
logging.basicConfig(level=logging.INFO)
 
# ─────────────────────────────────────────────────────────
# FLASK BACKEND BASE URL
# ─────────────────────────────────────────────────────────
 
BACKEND_URL = os.getenv("BACKEND_URL", "https://linguaflow-backend.onrender.com")
 
 
# ─────────────────────────────────────────────────────────
# HTTP CLIENT HELPERS
# ─────────────────────────────────────────────────────────
 
def _get(path: str) -> dict:
    try:
        r = requests.get(f"{BACKEND_URL}{path}", timeout=10)
        if not r.ok:
            return {
                "error": f"Backend returned HTTP {r.status_code}: {r.text[:200]}",
                "_http_status": r.status_code,
            }
        return r.json()
    except requests.ConnectionError:
        return {"error": f"Cannot connect to backend at {BACKEND_URL}. Is it running?", "_connection_error": True}
    except requests.Timeout:
        return {"error": "Backend request timed out. The server may be overloaded.", "_timeout": True}
    except Exception as exc:
        return {"error": f"Unexpected error contacting backend: {exc}"}
 
 
def _post(path: str, payload: dict) -> dict:
    try:
        r = requests.post(f"{BACKEND_URL}{path}", json=payload, timeout=30)
        if not r.ok:
            return {
                "error": f"Backend returned HTTP {r.status_code}: {r.text[:200]}",
                "_http_status": r.status_code,
            }
        return r.json()
    except requests.ConnectionError:
        return {"error": f"Cannot connect to backend at {BACKEND_URL}. Is it running?", "_connection_error": True}
    except requests.Timeout:
        return {"error": "Backend request timed out. The server may be overloaded.", "_timeout": True}
    except Exception as exc:
        return {"error": f"Unexpected error contacting backend: {exc}"}
 
 
# ─────────────────────────────────────────────────────────
# HEALTH CHECK
# ─────────────────────────────────────────────────────────
 
def _health_check() -> dict:
    try:
        r = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if r.status_code == 200:
            return {"ok": True, "status": r.json()}
        return {"ok": False, "error": f"HTTP {r.status_code}"}
    except requests.ConnectionError:
        return {"ok": False, "error": f"Cannot connect to {BACKEND_URL}"}
    except requests.Timeout:
        return {"ok": False, "error": "Health check timed out"}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}
 
 
# ─────────────────────────────────────────────────────────
# LOAD LANGUAGE LISTS FROM BACKEND
# ─────────────────────────────────────────────────────────
 
@st.cache_data(show_spinner=False)
def _load_languages() -> dict:
    data = _get("/languages")
    if data.get("error"):
        return {
            "source_codes":  ["auto", "en"],
            "target_codes":  ["en"],
            "source_labels": ["🔍 Detect Language", "English"],
            "target_labels": ["English"],
            "_fallback": True,
            "_error": data.get("error"),
        }
    data["_fallback"] = False
    return data
 
 
_lang_data    = _load_languages()
SOURCE_CODES  = _lang_data.get("source_codes",  ["auto", "en"])
TARGET_CODES  = _lang_data.get("target_codes",  ["en"])
SOURCE_LABELS = _lang_data.get("source_labels", ["🔍 Detect Language", "English"])
TARGET_LABELS = _lang_data.get("target_labels", ["English"])
 
 
# ─────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────
 
st.set_page_config(
    page_title="LinguaFlow — AI Translation",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)
 
# ─────────────────────────────────────────────────────────
# PREMIUM COLORFUL DESIGN SYSTEM
# ─────────────────────────────────────────────────────────
 
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
 
<style>
/* ════════════════════════════════════════════
   PREMIUM COLOR TOKENS
   ════════════════════════════════════════════ */
:root {
  /* Dark base */
  --bg:            #05050f;
  --surface:       #0a0a1a;
  --surface-2:     #0f0f22;
  --surface-3:     #141430;
  --border:        rgba(255,255,255,0.07);
  --border-bright: rgba(255,255,255,0.15);
 
  /* Rainbow palette */
  --purple:        #9333ea;
  --purple-bright: #c026d3;
  --violet:        #7c3aed;
  --navy:          #1e3a8a;
  --blue:          #2563eb;
  --blue-bright:   #3b82f6;
  --red:           #dc2626;
  --red-bright:    #ef4444;
  --orange:        #ea580c;
  --orange-bright: #f97316;
  --yellow:        #d97706;
  --yellow-bright: #fbbf24;
  --green:         #16a34a;
  --green-bright:  #22c55e;
 
  /* Glow alphas */
  --glow-purple:   rgba(147,51,234,0.30);
  --glow-blue:     rgba(37,99,235,0.28);
  --glow-orange:   rgba(234,88,12,0.25);
  --glow-green:    rgba(22,197,94,0.25);
  --glow-red:      rgba(220,38,38,0.25);
 
  /* Text */
  --text:          #f0f0ff;
  --text-2:        #a0a0c0;
  --text-3:        #50506a;
 
  --font-ui:   'Outfit', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
 
  --r-sm:  6px;  --r-md: 14px; --r-lg: 20px;
  --r-xl:  28px; --r-2xl: 40px;
}
 
/* ─── BASE ─── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: var(--font-ui) !important;
}
 
/* Animated mesh background */
[data-testid="stAppViewContainer"]::before {
  content: '';
  position: fixed; inset: 0; pointer-events: none; z-index: 0;
  background:
    radial-gradient(ellipse 80% 50% at 5%  0%,   rgba(124,58,237,.18)  0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 95% 5%,   rgba(220,38,38,.12)   0%, transparent 55%),
    radial-gradient(ellipse 50% 35% at 80% 95%,  rgba(234,88,12,.14)   0%, transparent 55%),
    radial-gradient(ellipse 55% 40% at 15% 90%,  rgba(37,99,235,.12)   0%, transparent 55%),
    radial-gradient(ellipse 40% 30% at 50% 50%,  rgba(147,51,234,.06)  0%, transparent 60%);
  animation: meshPulse 10s ease-in-out infinite alternate;
}
@keyframes meshPulse {
  0%   { opacity: 0.8; }
  100% { opacity: 1.0; }
}
 
/* ─── HIDE STREAMLIT CHROME ─── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }
 
/* ─── TYPOGRAPHY ─── */
h1,h2,h3,h4 {
  font-family: var(--font-ui) !important;
  letter-spacing: -0.03em !important;
  color: var(--text) !important;
}
 
/* ─── TEXTAREA ─── */
textarea,
[data-testid="stTextArea"] textarea {
  background: var(--surface-2) !important;
  border: 1.5px solid var(--border) !important;
  border-radius: var(--r-lg) !important;
  color: var(--text) !important;
  font-family: var(--font-ui) !important;
  font-size: .975rem !important;
  line-height: 1.75 !important;
  padding: 16px !important;
  transition: border-color .2s, box-shadow .2s !important;
}
textarea:focus,
[data-testid="stTextArea"] textarea:focus {
  border-color: var(--violet) !important;
  box-shadow: 0 0 0 3px var(--glow-purple) !important;
  outline: none !important;
}
 
/* ─── SELECTBOX ─── */
[data-testid="stSelectbox"] > div > div {
  background: var(--surface-2) !important;
  border: 1.5px solid var(--border) !important;
  border-radius: var(--r-md) !important;
  color: var(--text) !important;
  font-family: var(--font-ui) !important;
  font-size: .9rem !important;
}
[data-testid="stSelectbox"] > div > div:focus-within {
  border-color: var(--violet) !important;
  box-shadow: 0 0 0 3px var(--glow-purple) !important;
}
[data-testid="stSelectbox"] svg { color: var(--text-2) !important; }
 
/* ─── BUTTONS — default ─── */
.stButton > button {
  background: linear-gradient(135deg, var(--violet) 0%, var(--purple-bright) 100%) !important;
  color: #fff !important;
  border: none !important;
  border-radius: var(--r-md) !important;
  font-family: var(--font-ui) !important;
  font-weight: 600 !important;
  font-size: .88rem !important;
  letter-spacing: .02em !important;
  padding: .6rem 1.4rem !important;
  box-shadow: 0 4px 20px var(--glow-purple) !important;
  transition: transform .15s ease, box-shadow .15s ease !important;
  width: 100%;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 36px var(--glow-purple) !important;
}
.stButton > button:active  { transform: translateY(0) !important; }
.stButton > button:disabled { opacity: .4 !important; transform: none !important; }
 
/* ─── CARDS ─── */
.lf-card {
  background: linear-gradient(145deg, var(--surface) 0%, var(--surface-2) 100%);
  border: 1px solid var(--border);
  border-radius: var(--r-xl);
  padding: 28px 32px;
  margin-bottom: 16px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 8px 40px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.06);
}
 
/* Top shimmer line with rainbow gradient */
.lf-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg,
    var(--violet), var(--blue-bright), var(--green-bright),
    var(--yellow-bright), var(--orange-bright), var(--red-bright),
    var(--purple-bright), var(--violet));
  background-size: 200% 100%;
  animation: shimmer 4s linear infinite;
}
@keyframes shimmer {
  0%   { background-position: 0% 0%; }
  100% { background-position: 200% 0%; }
}
 
/* Lang card — purple/navy tint */
.lf-card-lang::after {
  content: '';
  position: absolute;
  bottom: -40px; right: -40px;
  width: 160px; height: 160px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(124,58,237,.15) 0%, transparent 70%);
  pointer-events: none;
}
 
/* Translate card — orange/red tint */
.lf-card-translate::after {
  content: '';
  position: absolute;
  top: -40px; left: -40px;
  width: 180px; height: 180px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(234,88,12,.10) 0%, transparent 70%);
  pointer-events: none;
}
 
/* ─── BADGE ─── */
.badge {
  display: inline-flex; align-items: center; gap: 5px;
  font-size: .65rem; font-weight: 700; letter-spacing: .1em;
  text-transform: uppercase;
  padding: 4px 12px; border-radius: 100px;
}
.badge-tech {
  background: linear-gradient(135deg, rgba(124,58,237,.2), rgba(37,99,235,.2));
  border: 1px solid rgba(124,58,237,.35);
  color: #c4b5fd;
}
.badge-success {
  background: rgba(22,197,94,.12);
  border: 1px solid rgba(22,197,94,.28);
  color: var(--green-bright);
}
.badge-warn {
  background: rgba(251,191,36,.12);
  border: 1px solid rgba(251,191,36,.28);
  color: var(--yellow-bright);
}
.badge-error {
  background: rgba(239,68,68,.12);
  border: 1px solid rgba(239,68,68,.28);
  color: var(--red-bright);
}
 
/* ─── ALERTS ─── */
.alert {
  border-radius: var(--r-md);
  padding: .75rem 1.1rem;
  font-size: .875rem;
  font-weight: 500;
  margin-top: .6rem;
}
.alert-error   { background: rgba(239,68,68,.10);  border:1px solid rgba(239,68,68,.25);  color: #fca5a5; }
.alert-success { background: rgba(22,197,94,.10);  border:1px solid rgba(22,197,94,.25);  color: #86efac; }
.alert-warn    { background: rgba(251,191,36,.10); border:1px solid rgba(251,191,36,.25); color: #fde68a; }
 
/* ─── SECTION LABELS ─── */
.section-label {
  font-size: .65rem; font-weight: 700;
  letter-spacing: .12em; text-transform: uppercase;
  color: var(--text-3); margin-bottom: 7px;
}
 
/* ─── CHAR COUNT ─── */
.char-count      { font-size: .72rem; color: var(--text-3); text-align: right; margin-top:-8px; }
.char-count-warn { color: var(--yellow-bright) !important; }
.char-count-over { color: var(--red-bright)    !important; }
 
/* ─── MISC ─── */
hr { border-color: var(--border) !important; margin: 24px 0 !important; }
audio {
  width: 100%; height: 36px;
  border-radius: var(--r-md);
  background: var(--surface-2);
  margin-top: 8px;
}
[data-testid="column"] { padding: 0 6px !important; }
.stSpinner > div { border-top-color: var(--purple) !important; }
 
/* ─── CONNECTION DOTS ─── */
.dot-online  { width:10px;height:10px;border-radius:50%;background:var(--green-bright);box-shadow:0 0 10px var(--green-bright);display:inline-block; }
.dot-offline { width:10px;height:10px;border-radius:50%;background:var(--red-bright);box-shadow:0 0 10px var(--red-bright);display:inline-block; }
 
/* ─── STAT CHIPS (header row) ─── */
.stat-chip {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 5px 14px; border-radius: 100px;
  font-size: .72rem; font-weight: 600; letter-spacing:.04em;
}
.chip-purple { background: rgba(147,51,234,.18); border:1px solid rgba(147,51,234,.35); color:#d8b4fe; }
.chip-blue   { background: rgba(59,130,246,.18); border:1px solid rgba(59,130,246,.35); color:#93c5fd; }
.chip-orange { background: rgba(249,115,22,.18); border:1px solid rgba(249,115,22,.35); color:#fdba74; }
.chip-green  { background: rgba(34,197,94,.18);  border:1px solid rgba(34,197,94,.35);  color:#86efac; }
 
/* ─── DIVIDER WORD ─── */
.divider-word {
  display:flex; align-items:center; gap:10px;
  color: var(--text-3); font-size:.7rem; font-weight:700;
  letter-spacing:.1em; text-transform:uppercase; margin:18px 0;
}
.divider-word::before,.divider-word::after {
  content:''; flex:1; height:1px;
  background: linear-gradient(90deg, transparent, var(--border), transparent);
}
 
/* ─── TRANSLATE BUTTON OVERRIDE ─── */
.translate-bar .stButton > button {
  background: linear-gradient(135deg,
    var(--violet) 0%, var(--purple) 30%,
    var(--red) 65%, var(--orange-bright) 100%) !important;
  font-size: 1.05rem !important;
  font-weight: 800 !important;
  letter-spacing: .06em !important;
  padding: 1rem 0 !important;
  border-radius: var(--r-lg) !important;
  box-shadow:
    0 6px 40px rgba(147,51,234,.45),
    0 0 0 1px rgba(147,51,234,.20),
    inset 0 1px 0 rgba(255,255,255,.12) !important;
  text-transform: uppercase !important;
}
.translate-bar .stButton > button:hover {
  transform: translateY(-3px) !important;
  box-shadow:
    0 14px 56px rgba(147,51,234,.60),
    0 0 0 1px rgba(147,51,234,.35),
    inset 0 1px 0 rgba(255,255,255,.15) !important;
}
 
/* ─── SWAP BUTTON OVERRIDE ─── */
.swap-btn .stButton > button {
  background: linear-gradient(135deg, var(--navy) 0%, var(--blue) 100%) !important;
  box-shadow: 0 4px 20px var(--glow-blue) !important;
  font-size: 1.1rem !important;
  padding: .55rem !important;
}
.swap-btn .stButton > button:hover {
  box-shadow: 0 8px 32px var(--glow-blue) !important;
}
 
/* ─── CLEAR BUTTON ─── */
.clear-btn .stButton > button {
  background: linear-gradient(135deg, rgba(220,38,38,.7) 0%, rgba(234,88,12,.7) 100%) !important;
  box-shadow: 0 4px 16px var(--glow-red) !important;
}
 
/* ─── SPEAK BUTTON ─── */
.speak-btn .stButton > button {
  background: linear-gradient(135deg, var(--green) 0%, var(--blue-bright) 100%) !important;
  box-shadow: 0 4px 16px var(--glow-green) !important;
}
 
/* ─── COPY BUTTON ─── */
.copy-btn .stButton > button {
  background: linear-gradient(135deg, var(--yellow) 0%, var(--orange) 100%) !important;
  box-shadow: 0 4px 16px var(--glow-orange) !important;
}
</style>
""", unsafe_allow_html=True)
 
 
# ─────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────
 
_defaults = {
    "translated_text": "",
    "detected_lang":   "",
    "src_audio_html":  "",
    "tgt_audio_html":  "",
    "error_msg":       "",
    "success_msg":     "",
    "warn_msg":        "",
}
for _k, _v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v
 
 
# ─────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────
 
def _audio_player_html(audio_b64: str) -> str:
    return f'<audio controls autoplay src="data:audio/mp3;base64,{audio_b64}"></audio>'
 
 
def _clear_messages():
    st.session_state.error_msg   = ""
    st.session_state.success_msg = ""
    st.session_state.warn_msg    = ""
 
 
# ─────────────────────────────────────────────────────────
# CONNECTION STATUS BANNER
# ─────────────────────────────────────────────────────────
 
_health = _health_check()
if _health["ok"]:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:1rem;
                padding:8px 16px;background:rgba(22,197,94,.06);
                border:1px solid rgba(22,197,94,.15);border-radius:100px;
                width:fit-content;">
      <span class="dot-online"></span>
      <span style="font-size:.76rem;color:#86efac;font-weight:600;">Backend connected</span>
      <span style="font-size:.72rem;color:var(--text-3);">— <code style="color:#a0a0c0;">{BACKEND_URL}</code></span>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:.8rem;
                padding:8px 16px;background:rgba(239,68,68,.06);
                border:1px solid rgba(239,68,68,.18);border-radius:100px;
                width:fit-content;">
      <span class="dot-offline"></span>
      <span style="font-size:.76rem;color:#fca5a5;font-weight:600;">
        Backend disconnected — {_health.get('error', 'Unknown error')}
      </span>
    </div>
    <div class="alert alert-error" style="margin-bottom:1.2rem;">
      ⚠ Cannot reach backend at <code>{BACKEND_URL}</code>.<br>
      Run: &nbsp;<code>python backend.py</code>
    </div>
    """, unsafe_allow_html=True)
 
if _lang_data.get("_fallback"):
    st.markdown(f"""
    <div class="alert alert-warn" style="margin-bottom:1.2rem;">
      ⚡ Using fallback language list. {_lang_data.get('_error', '')}
    </div>
    """, unsafe_allow_html=True)
 
 
# ─────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────
 
st.markdown("""
<div style="display:flex;align-items:center;justify-content:space-between;
            padding:1.2rem 0 2rem;">
 
  <!-- Logo + Name -->
  <div style="display:flex;align-items:center;gap:14px;">
    <div style="width:48px;height:48px;flex-shrink:0;
                background:linear-gradient(135deg,#7c3aed,#dc2626,#ea580c);
                border-radius:16px;display:flex;align-items:center;
                justify-content:center;font-size:24px;
                box-shadow:0 6px 24px rgba(124,58,237,.5);">🌐</div>
    <div>
      <div style="font-size:1.6rem;font-weight:900;letter-spacing:-0.05em;
                  background:linear-gradient(90deg,#c4b5fd,#818cf8,#f0abfc,#fb923c,#fbbf24);
                  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                  line-height:1;">LinguaFlow</div>
      <div style="font-size:.65rem;color:#50506a;letter-spacing:.1em;
                  text-transform:uppercase;font-weight:700;margin-top:1px;">
        Translation Suite
      </div>
    </div>
  </div>
 
  <!-- Stat chips -->
  <div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end;">
    <span class="stat-chip chip-purple">🔤 100+ Languages</span>
    <span class="stat-chip chip-blue">⚡ Auto-Detect</span>
    <span class="stat-chip chip-orange">🔊 Text-to-Speech</span>
    <span class="stat-chip chip-green">🌍 Free API</span>
  </div>
</div>
""", unsafe_allow_html=True)
 
# Hero headline
st.markdown("""
<div style="text-align:center;margin-bottom:2.8rem;">
  <h1 style="font-size:clamp(1.8rem,4.5vw,3.2rem);font-weight:900;line-height:1.08;
              margin-bottom:.8rem;letter-spacing:-0.04em;">
    Break every language barrier,
    <br>
    <span style="background:linear-gradient(135deg,#a855f7,#ec4899,#ef4444,#f97316,#fbbf24);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
      instantly.
    </span>
  </h1>
  <p style="color:#7070a0;font-size:1rem;font-weight:400;letter-spacing:.01em;">
    Powered by MyMemory · gTTS · Flask · Streamlit
  </p>
</div>
""", unsafe_allow_html=True)
 
 
# ─────────────────────────────────────────────────────────
# LANGUAGE SELECTOR CARD
# ─────────────────────────────────────────────────────────
 
st.markdown('<div class="lf-card lf-card-lang">', unsafe_allow_html=True)
 
col_src, col_mid, col_tgt = st.columns([10, 2, 10])
 
with col_src:
    st.markdown("""
    <p class="section-label" style="color:#a78bfa;">
      🟣 Source Language
    </p>""", unsafe_allow_html=True)
    src_label = st.selectbox("Source", SOURCE_LABELS, index=0,
                              label_visibility="collapsed", key="sel_src")
    src_code  = SOURCE_CODES[SOURCE_LABELS.index(src_label)]
 
with col_mid:
    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="swap-btn">', unsafe_allow_html=True)
    swap_clicked = st.button("⇄", key="btn_swap",
                              help="Swap source and target languages",
                              use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
 
with col_tgt:
    st.markdown("""
    <p class="section-label" style="color:#fb923c;">
      🟠 Target Language
    </p>""", unsafe_allow_html=True)
    default_tgt  = TARGET_LABELS.index("Spanish") if "Spanish" in TARGET_LABELS else 0
    tgt_label    = st.selectbox("Target", TARGET_LABELS, index=default_tgt,
                                 label_visibility="collapsed", key="sel_tgt")
    tgt_code     = TARGET_CODES[TARGET_LABELS.index(tgt_label)]
 
st.markdown("</div>", unsafe_allow_html=True)
 
 
# ─────────────────────────────────────────────────────────
# TRANSLATION PANELS CARD
# ─────────────────────────────────────────────────────────
 
st.markdown('<div class="lf-card lf-card-translate">', unsafe_allow_html=True)
 
left_panel, right_panel = st.columns(2)
 
# ── LEFT — Input ──
with left_panel:
    st.markdown("""
    <p class="section-label" style="color:#818cf8;">✏️ Input Text</p>
    """, unsafe_allow_html=True)
 
    source_text = st.text_area(
        "Input",
        value=st.session_state.get("src_text_val", ""),
        height=240,
        max_chars=5000,
        placeholder="Type or paste your text here…",
        label_visibility="collapsed",
        key="input_textarea",
    )
 
    char_len  = len(source_text)
    cnt_class = "char-count-over" if char_len > 5000 else ("char-count-warn" if char_len > 4500 else "")
    st.markdown(f'<p class="char-count {cnt_class}">{char_len:,} / 5,000</p>',
                unsafe_allow_html=True)
 
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
        clear_clicked = st.button("✕  Clear", key="btn_clear", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="speak-btn">', unsafe_allow_html=True)
        tts_src_clicked = st.button("🔊 Speak", key="btn_tts_src", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
 
    if st.session_state.src_audio_html:
        st.markdown(st.session_state.src_audio_html, unsafe_allow_html=True)
 
# ── RIGHT — Output ──
with right_panel:
    detected = st.session_state.detected_lang
    lbl = '<p class="section-label" style="color:#34d399;">🌍 Translation</p>'
    if detected:
        lbl += f'<span class="badge badge-success" style="margin-bottom:7px;display:inline-flex;">🔍 {detected}</span>'
    st.markdown(lbl, unsafe_allow_html=True)
 
    st.text_area(
        "Output",
        value=st.session_state.translated_text,
        height=240,
        placeholder="Translation appears here…",
        label_visibility="collapsed",
        disabled=True,
    )
    o1, o2, _ = st.columns(3)
    with o1:
        st.markdown('<div class="copy-btn">', unsafe_allow_html=True)
        copy_clicked = st.button("📋 Copy", key="btn_copy", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with o2:
        st.markdown('<div class="speak-btn">', unsafe_allow_html=True)
        tts_tgt_clicked = st.button("🔊 Speak", key="btn_tts_tgt", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
 
    if st.session_state.tgt_audio_html:
        st.markdown(st.session_state.tgt_audio_html, unsafe_allow_html=True)
 
st.markdown("</div>", unsafe_allow_html=True)
 
 
# ─────────────────────────────────────────────────────────
# TRANSLATE BUTTON
# ─────────────────────────────────────────────────────────
 
st.markdown('<div class="lf-card translate-bar" style="padding:20px 28px;">', unsafe_allow_html=True)
_, btn_col, _ = st.columns([2, 5, 2])
with btn_col:
    translate_clicked = st.button(
        "🌐  Translate Now",
        key="btn_translate",
        use_container_width=True,
        help="Translate the input text",
    )
st.markdown("</div>", unsafe_allow_html=True)
 
 
# ─────────────────────────────────────────────────────────
# EVENT HANDLERS
# ─────────────────────────────────────────────────────────
 
# ── Translate ──
if translate_clicked:
    _clear_messages()
    st.session_state.detected_lang  = ""
    st.session_state.src_audio_html = ""
    st.session_state.tgt_audio_html = ""
 
    with st.spinner("Translating…"):
        result = _post("/translate", {
            "text": source_text,
            "source_lang": src_code,
            "target_lang": tgt_code,
        })
 
    if result.get("error"):
        st.session_state.error_msg = result["error"]
    else:
        translated = result.get("translated_text") or ""
        st.session_state.translated_text = translated
        st.session_state.detected_lang   = result.get("detected_lang") or ""
        st.session_state.success_msg     = "Translation complete ✓"
    st.rerun()
 
# ── Swap ──
if swap_clicked:
    _clear_messages()
    swap = _post("/swap", {
        "src_code": src_code,
        "tgt_code": tgt_code,
        "src_text": source_text,
        "tgt_text": st.session_state.translated_text,
    })
    if swap.get("swapped"):
        new_src_label = SOURCE_LABELS[SOURCE_CODES.index(swap["new_src_code"])]
        new_tgt_label = TARGET_LABELS[TARGET_CODES.index(swap["new_tgt_code"])]
        st.session_state["sel_src"]      = new_src_label
        st.session_state["sel_tgt"]      = new_tgt_label
        st.session_state["src_text_val"] = swap["new_src_text"]
        st.session_state.translated_text = swap["new_tgt_text"]
        st.session_state.detected_lang   = ""
        st.session_state.src_audio_html  = ""
        st.session_state.tgt_audio_html  = ""
    else:
        st.session_state.warn_msg = "Set source language (not 'Detect') before swapping."
    st.rerun()
 
# ── Clear ──
if clear_clicked:
    for key in ("translated_text","detected_lang","src_audio_html","tgt_audio_html","src_text_val"):
        st.session_state[key] = ""
    _clear_messages()
    st.rerun()
 
# ── Copy ──
if copy_clicked:
    if st.session_state.translated_text:
        b64 = base64.b64encode(st.session_state.translated_text.encode()).decode()
        st.markdown(f"""
        <script>
        (async()=>{{
          const t = atob("{b64}");
          await navigator.clipboard.writeText(t);
        }})();
        </script>""", unsafe_allow_html=True)
        st.session_state.success_msg = "Copied to clipboard ✓"
    else:
        st.session_state.warn_msg = "Nothing to copy — translate something first."
    st.rerun()
 
# ── TTS: Source ──
if tts_src_clicked:
    _clear_messages()
    if source_text.strip():
        lang = "en" if src_code == "auto" else src_code
        with st.spinner("Generating speech…"):
            res = _post("/speak", {"text": source_text, "lang": lang})
        if res.get("error"):
            st.session_state.error_msg = res["error"]
        else:
            st.session_state.src_audio_html = _audio_player_html(res["audio_b64"])
            st.session_state.tgt_audio_html = ""
            if res.get("tts_fallback"):
                st.session_state.warn_msg = "TTS unavailable for that language — played in English."
    else:
        st.session_state.warn_msg = "Enter some text before using speech."
    st.rerun()
 
# ── TTS: Target ──
if tts_tgt_clicked:
    _clear_messages()
    if st.session_state.translated_text.strip():
        with st.spinner("Generating speech…"):
            res = _post("/speak", {"text": st.session_state.translated_text, "lang": tgt_code})
        if res.get("error"):
            st.session_state.error_msg = res["error"]
        else:
            st.session_state.tgt_audio_html = _audio_player_html(res["audio_b64"])
            st.session_state.src_audio_html = ""
            if res.get("tts_fallback"):
                st.session_state.warn_msg = "TTS unavailable for that language — played in English."
    else:
        st.session_state.warn_msg = "Translate something first before using speech."
    st.rerun()
 
 
# ─────────────────────────────────────────────────────────
# STATUS MESSAGES
# ─────────────────────────────────────────────────────────
 
if st.session_state.error_msg:
    st.markdown(f'<div class="alert alert-error">⚠ {st.session_state.error_msg}</div>',
                unsafe_allow_html=True)
 
if st.session_state.warn_msg:
    st.markdown(f'<div class="alert alert-warn">⚡ {st.session_state.warn_msg}</div>',
                unsafe_allow_html=True)
 
if st.session_state.success_msg:
    st.markdown(f'<div class="alert alert-success">✓ {st.session_state.success_msg}</div>',
                unsafe_allow_html=True)
 
 
# ─────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────
 
st.markdown("""
<div style="text-align:center;margin-top:3.5rem;padding-top:1.5rem;
            border-top:1px solid rgba(255,255,255,0.05);">
  <div style="font-size:.7rem;letter-spacing:.06em;margin-bottom:10px;">
    <span style="background:linear-gradient(90deg,#a78bfa,#60a5fa,#34d399,#fbbf24,#f87171);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:700;">
      LinguaFlow Translation Suite
    </span>
  </div>
  <div style="color:#30304a;font-size:.7rem;">
    Python &nbsp;·&nbsp; Streamlit &nbsp;·&nbsp; Flask &nbsp;·&nbsp; MyMemory API &nbsp;·&nbsp; gTTS
  </div>
</div>
""", unsafe_allow_html=True)