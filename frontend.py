"""
LinguaFlow — Streamlit frontend
Premium colorful UI with full language support.
"""
import os
import base64
import requests
import streamlit as st
 
# ----------------------------------------------------------------------
#  Backend URL
# ----------------------------------------------------------------------
try:
    BACKEND_URL = st.secrets.get("BACKEND_URL", os.getenv("BACKEND_URL", "http://localhost:5000"))
except Exception:
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5000")
 
BACKEND_URL = BACKEND_URL.rstrip("/")
 
# ----------------------------------------------------------------------
#  Full language list (80+ languages)
# ----------------------------------------------------------------------
LANGUAGES = {
    "Auto Detect": "auto",
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Dutch": "nl",
    "Russian": "ru",
    "Polish": "pl",
    "Ukrainian": "uk",
    "Czech": "cs",
    "Slovak": "sk",
    "Hungarian": "hu",
    "Romanian": "ro",
    "Bulgarian": "bg",
    "Croatian": "hr",
    "Serbian": "sr",
    "Slovenian": "sl",
    "Greek": "el",
    "Turkish": "tr",
    "Albanian": "sq",
    "Estonian": "et",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Finnish": "fi",
    "Swedish": "sv",
    "Norwegian": "no",
    "Danish": "da",
    "Icelandic": "is",
    "Irish": "ga",
    "Welsh": "cy",
    "Catalan": "ca",
    "Basque": "eu",
    "Galician": "gl",
    "Maltese": "mt",
    "Arabic": "ar",
    "Hebrew": "iw",
    "Persian": "fa",
    "Urdu": "ur",
    "Hindi": "hi",
    "Bengali": "bn",
    "Punjabi": "pa",
    "Gujarati": "gu",
    "Marathi": "mr",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Sinhala": "si",
    "Nepali": "ne",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Japanese": "ja",
    "Korean": "ko",
    "Vietnamese": "vi",
    "Thai": "th",
    "Indonesian": "id",
    "Malay": "ms",
    "Filipino": "tl",
    "Khmer": "km",
    "Lao": "lo",
    "Burmese": "my",
    "Mongolian": "mn",
    "Kazakh": "kk",
    "Uzbek": "uz",
    "Azerbaijani": "az",
    "Armenian": "hy",
    "Georgian": "ka",
    "Swahili": "sw",
    "Amharic": "am",
    "Hausa": "ha",
    "Yoruba": "yo",
    "Igbo": "ig",
    "Zulu": "zu",
    "Xhosa": "xh",
    "Afrikaans": "af",
    "Somali": "so",
    "Sundanese": "su",
    "Javanese": "jv",
    "Esperanto": "eo",
    "Latin": "la",
}
 
LANGUAGE_NAMES = list(LANGUAGES.keys())
CODE_TO_NAME = {v: k for k, v in LANGUAGES.items()}
 
# ----------------------------------------------------------------------
#  Page config
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="LinguaFlow — Premium Translator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)
 
# ----------------------------------------------------------------------
#  Premium colorful CSS
# ----------------------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&family=Space+Grotesk:wght@500;700&display=swap');
 
/* ---------- BASE ---------- */
.stApp {
    background:
        radial-gradient(ellipse at top left,    rgba(139,92,246,0.18), transparent 50%),
        radial-gradient(ellipse at top right,   rgba(239,68,68,0.15),  transparent 50%),
        radial-gradient(ellipse at bottom left, rgba(245,158,11,0.15), transparent 50%),
        radial-gradient(ellipse at bottom right,rgba(30,58,138,0.20),  transparent 50%),
        #05050f;
    color: #e8e8f0;
    font-family: 'Inter', sans-serif;
}
header[data-testid="stHeader"] {background: transparent;}
#MainMenu, footer {visibility: hidden;}
 
.block-container {padding-top: 2rem; max-width: 1200px;}
 
/* ---------- HEADER ---------- */
.lf-logo {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3rem;
    font-weight: 900;
    background: linear-gradient(90deg, #a78bfa, #ec4899, #f97316, #fbbf24);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    letter-spacing: -0.02em;
}
.lf-tagline {color: #94a3b8; font-size: 1rem; margin-top: -0.3rem;}
 
.lf-chips {display: flex; gap: 0.6rem; flex-wrap: wrap; margin-top: 0.8rem;}
.lf-chip {
    padding: 0.35rem 0.9rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    border: 1px solid;
}
.lf-chip-purple {color:#c4b5fd; background:rgba(139,92,246,0.12); border-color:rgba(139,92,246,0.4);}
.lf-chip-blue   {color:#93c5fd; background:rgba(59,130,246,0.12); border-color:rgba(59,130,246,0.4);}
.lf-chip-orange {color:#fdba74; background:rgba(249,115,22,0.12); border-color:rgba(249,115,22,0.4);}
.lf-chip-green  {color:#86efac; background:rgba(34,197,94,0.12);  border-color:rgba(34,197,94,0.4);}
 
/* ---------- HERO ---------- */
.lf-hero {
    font-size: 2.4rem; font-weight: 800; line-height: 1.15;
    margin: 1.5rem 0 0.5rem;
}
.lf-hero-grad {
    background: linear-gradient(90deg, #a78bfa, #ec4899, #ef4444, #f97316, #fbbf24);
    -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
}
 
/* ---------- CARDS ---------- */
.lf-card {
    background: linear-gradient(180deg, rgba(20,20,40,0.7), rgba(10,10,25,0.85));
    border: 1px solid rgba(139,92,246,0.18);
    border-radius: 18px;
    padding: 1.4rem;
    margin: 1rem 0;
    position: relative;
    overflow: hidden;
}
.lf-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #ef4444, #f97316, #fbbf24, #22c55e, #3b82f6, #8b5cf6, #ec4899);
    background-size: 200% 100%;
    animation: shimmer 4s linear infinite;
}
@keyframes shimmer {
    0%   {background-position: 0% 50%;}
    100% {background-position: 200% 50%;}
}
 
.lf-label {
    display: flex; align-items: center; gap: 0.5rem;
    font-size: 0.8rem; font-weight: 800; letter-spacing: 0.12em;
    text-transform: uppercase; margin-bottom: 0.6rem;
}
.lf-dot {width: 10px; height: 10px; border-radius: 50%;}
.lf-dot-purple {background: #a78bfa; box-shadow: 0 0 12px #a78bfa;}
.lf-dot-orange {background: #f97316; box-shadow: 0 0 12px #f97316;}
.lf-dot-pink   {background: #ec4899; box-shadow: 0 0 12px #ec4899;}
.lf-dot-green  {background: #22c55e; box-shadow: 0 0 12px #22c55e;}
 
.lf-label-purple {color: #c4b5fd;}
.lf-label-orange {color: #fdba74;}
.lf-label-pink   {color: #f9a8d4;}
.lf-label-green  {color: #86efac;}
 
/* ---------- INPUTS ---------- */
.stSelectbox > div > div {
    background: rgba(15,15,30,0.85) !important;
    border: 1px solid rgba(139,92,246,0.3) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
}
.stTextArea textarea {
    background: rgba(15,15,30,0.85) !important;
    border: 1px solid rgba(139,92,246,0.3) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    font-size: 1rem !important;
}
/* Bright output text */
.stTextArea textarea[disabled] {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    opacity: 1 !important;
    background: rgba(20,15,40,0.9) !important;
    border: 1px solid rgba(167,139,250,0.5) !important;
    font-weight: 500 !important;
}
 
/* ---------- BUTTONS ---------- */
.stButton > button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    border: none !important;
    padding: 0.6rem 1.2rem !important;
    transition: all 0.2s ease !important;
    color: #ffffff !important;
}
.stButton > button:hover {transform: translateY(-2px); filter: brightness(1.15);}
 
/* Primary (Translate) — purple → red → orange */
.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #8b5cf6, #ec4899, #f97316) !important;
    box-shadow: 0 6px 20px rgba(139,92,246,0.4) !important;
    font-size: 1.05rem !important;
}
</style>
""",
    unsafe_allow_html=True,
)
 
# ----------------------------------------------------------------------
#  Header
# ----------------------------------------------------------------------
st.markdown(
    """
<div>
  <h1 class="lf-logo">🌐 LinguaFlow</h1>
  <p class="lf-tagline">Premium AI translation across 80+ languages</p>
  <div class="lf-chips">
    <span class="lf-chip lf-chip-purple">⚡ Real-time</span>
    <span class="lf-chip lf-chip-blue">🌍 80+ languages</span>
    <span class="lf-chip lf-chip-orange">🔊 Audio output</span>
    <span class="lf-chip lf-chip-green">✨ Free forever</span>
  </div>
  <p class="lf-hero">Translate anything,
    <span class="lf-hero-grad">instantly.</span>
  </p>
</div>
""",
    unsafe_allow_html=True,
)
 
# ----------------------------------------------------------------------
#  Backend health check
# ----------------------------------------------------------------------
def check_backend():
    try:
        r = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return r.status_code == 200
    except Exception:
        return False
 
backend_ok = check_backend()
if backend_ok:
    st.success(f"✅ Backend connected: {BACKEND_URL}")
else:
    st.error(f"❌ Backend not reachable: {BACKEND_URL}")
 
# ----------------------------------------------------------------------
#  Session state
# ----------------------------------------------------------------------
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "source_lang" not in st.session_state:
    st.session_state.source_lang = "English"
if "target_lang" not in st.session_state:
    st.session_state.target_lang = "Spanish"
 
# ----------------------------------------------------------------------
#  Language selectors
# ----------------------------------------------------------------------
st.markdown('<div class="lf-card">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([5, 1, 5])
 
with col1:
    st.markdown(
        '<div class="lf-label lf-label-purple"><span class="lf-dot lf-dot-purple"></span>Source Language</div>',
        unsafe_allow_html=True,
    )
    src_idx = LANGUAGE_NAMES.index(st.session_state.source_lang) if st.session_state.source_lang in LANGUAGE_NAMES else 1
    source_lang = st.selectbox(
        "Source",
        LANGUAGE_NAMES,
        index=src_idx,
        key="src_select",
        label_visibility="collapsed",
    )
    st.session_state.source_lang = source_lang
 
with col2:
    st.write("")
    st.write("")
    if st.button("⇄", key="swap_btn", help="Swap languages"):
        if st.session_state.source_lang != "Auto Detect":
            st.session_state.source_lang, st.session_state.target_lang = (
                st.session_state.target_lang,
                st.session_state.source_lang,
            )
            st.session_state.input_text, st.session_state.translated_text = (
                st.session_state.translated_text,
                st.session_state.input_text,
            )
            st.rerun()
 
with col3:
    st.markdown(
        '<div class="lf-label lf-label-orange"><span class="lf-dot lf-dot-orange"></span>Target Language</div>',
        unsafe_allow_html=True,
    )
    # Target should never be "Auto Detect"
    target_options = [n for n in LANGUAGE_NAMES if n != "Auto Detect"]
    tgt_idx = target_options.index(st.session_state.target_lang) if st.session_state.target_lang in target_options else 0
    target_lang = st.selectbox(
        "Target",
        target_options,
        index=tgt_idx,
        key="tgt_select",
        label_visibility="collapsed",
    )
    st.session_state.target_lang = target_lang
 
st.markdown("</div>", unsafe_allow_html=True)
 
# ----------------------------------------------------------------------
#  Text input + output
# ----------------------------------------------------------------------
col_in, col_out = st.columns(2)
 
with col_in:
    st.markdown('<div class="lf-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="lf-label lf-label-pink"><span class="lf-dot lf-dot-pink"></span>📝 Input Text</div>',
        unsafe_allow_html=True,
    )
    input_text = st.text_area(
        "Input",
        value=st.session_state.input_text,
        height=220,
        key="input_area",
        label_visibility="collapsed",
        placeholder="Type or paste text here...",
    )
    st.session_state.input_text = input_text
    st.caption(f"📊 {len(input_text)} characters")
    st.markdown("</div>", unsafe_allow_html=True)
 
with col_out:
    st.markdown('<div class="lf-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="lf-label lf-label-green"><span class="lf-dot lf-dot-green"></span>🌍 Translation</div>',
        unsafe_allow_html=True,
    )
    st.text_area(
        "Output",
        value=st.session_state.translated_text,
        height=220,
        key="output_area",
        label_visibility="collapsed",
        disabled=True,
    )
    st.caption(f"📊 {len(st.session_state.translated_text)} characters")
    st.markdown("</div>", unsafe_allow_html=True)
 
# ----------------------------------------------------------------------
#  Action buttons
# ----------------------------------------------------------------------
btn1, btn2, btn3, btn4 = st.columns(4)
 
with btn1:
    translate_clicked = st.button("✨ Translate Now", type="primary", use_container_width=True)
 
with btn2:
    speak_clicked = st.button("🔊 Speak", use_container_width=True)
 
with btn3:
    copy_clicked = st.button("📋 Copy", use_container_width=True)
 
with btn4:
    clear_clicked = st.button("🗑 Clear", use_container_width=True)
 
# ----------------------------------------------------------------------
#  Translate
# ----------------------------------------------------------------------
if translate_clicked:
    if not st.session_state.input_text.strip():
        st.warning("⚠ Please enter some text to translate.")
    elif st.session_state.source_lang == st.session_state.target_lang:
        st.warning("⚠ Source and target languages are the same. Please pick different languages.")
    else:
        with st.spinner("Translating..."):
            try:
                payload = {
                    "text": st.session_state.input_text,
                    "source_lang": LANGUAGES[st.session_state.source_lang],
                    "target_lang": LANGUAGES[st.session_state.target_lang],
                }
                r = requests.post(f"{BACKEND_URL}/translate", json=payload, timeout=30)
                if r.status_code == 200:
                    data = r.json()
                    if data.get("translated_text"):
                        st.session_state.translated_text = data["translated_text"]
                        if data.get("detected_lang"):
                            detected = CODE_TO_NAME.get(data["detected_lang"], data["detected_lang"])
                            st.info(f"🔍 Detected language: {detected}")
                        st.rerun()
                    else:
                        st.error(f"Translation failed: {data.get('error', 'unknown error')}")
                else:
                    st.error(f"⚠ Backend returned HTTP {r.status_code}: {r.text}")
            except Exception as e:
                st.error(f"❌ Connection error: {e}")
 
# ----------------------------------------------------------------------
#  Speak
# ----------------------------------------------------------------------
if speak_clicked:
    if not st.session_state.translated_text.strip():
        st.warning("⚠ Translate something first.")
    else:
        with st.spinner("Generating audio..."):
            try:
                payload = {
                    "text": st.session_state.translated_text,
                    "lang": LANGUAGES[st.session_state.target_lang],
                }
                r = requests.post(f"{BACKEND_URL}/speak", json=payload, timeout=30)
                if r.status_code == 200:
                    data = r.json()
                    if data.get("audio_b64"):
                        audio_bytes = base64.b64decode(data["audio_b64"])
                        st.audio(audio_bytes, format="audio/mp3")
                    else:
                        st.error(f"Audio failed: {data.get('error', 'unknown error')}")
                else:
                    st.error(f"⚠ Backend returned HTTP {r.status_code}")
            except Exception as e:
                st.error(f"❌ Connection error: {e}")
 
# ----------------------------------------------------------------------
#  Clear
# ----------------------------------------------------------------------
if clear_clicked:
    st.session_state.input_text = ""
    st.session_state.translated_text = ""
    st.rerun()
 
# ----------------------------------------------------------------------
#  Copy (UI hint)
# ----------------------------------------------------------------------
if copy_clicked:
    if st.session_state.translated_text:
        st.code(st.session_state.translated_text, language=None)
        st.success("✅ Translation shown above — select and copy.")
    else:
        st.warning("⚠ Nothing to copy yet.")
 
# ----------------------------------------------------------------------
#  Footer
# ----------------------------------------------------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#64748b; font-size:0.85rem;'>"
    "Made with 💜 — LinguaFlow • 80+ languages • Free forever"
    "</p>",
    unsafe_allow_html=True,
)