import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import io
import time

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LinguaFlow · Language Translator",
    page_icon="🌐",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Import font */
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Sora', sans-serif; }

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Page background */
.stApp { background: #0d0f14; }

/* Main container width */
.block-container { max-width: 800px; padding-top: 2rem; }

/* Headings */
h1 { 
    background: linear-gradient(135deg, #ffffff 0%, #a78bfa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700 !important;
    letter-spacing: -0.03em;
    text-align: center;
}

/* Subheading */
.subtitle {
    text-align: center;
    color: #8892a4;
    font-size: 0.9rem;
    margin-top: -0.8rem;
    margin-bottom: 1.5rem;
}

/* Select boxes */
.stSelectbox > div > div {
    background: #161a23 !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
    color: #e8eaf2 !important;
}

/* Text areas */
.stTextArea textarea {
    background: #161a23 !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
    color: #e8eaf2 !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 1rem !important;
}
.stTextArea textarea:focus {
    border-color: rgba(255,255,255,0.18) !important;
    box-shadow: none !important;
}

/* Translate button */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #5b7fff, #a78bfa) !important;
    border: none !important;
    border-radius: 12px !important;
    color: white !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.65rem 1.5rem !important;
    font-family: 'Sora', sans-serif !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* Output box */
.output-box {
    background: #161a23;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    color: #e8eaf2;
    font-size: 1rem;
    line-height: 1.65;
    min-height: 120px;
    word-wrap: break-word;
    white-space: pre-wrap;
}
.output-box.empty { color: #4a5568; }

/* History item */
.history-card {
    background: #161a23;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 0.85rem 1rem;
    margin-bottom: 0.6rem;
}
.history-langs {
    font-size: 0.68rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #4a5568;
    margin-bottom: 0.4rem;
    font-family: 'DM Mono', monospace;
}
.history-src { font-size: 0.85rem; color: #8892a4; }
.history-tgt { font-size: 0.85rem; color: #e8eaf2; margin-top: 4px; }

/* Section divider label */
.section-label {
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #4a5568;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    padding-bottom: 0.4rem;
    margin: 1.5rem 0 0.8rem;
}

/* Info chips */
.chip {
    display: inline-block;
    background: rgba(91,127,255,0.12);
    border: 1px solid rgba(91,127,255,0.25);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.75rem;
    color: #8ba4ff;
    margin-right: 6px;
}

/* Character counter */
.char-counter {
    font-size: 0.72rem;
    color: #4a5568;
    text-align: right;
    margin-top: -0.8rem;
    margin-bottom: 0.5rem;
    font-family: monospace;
}
.char-counter.warn { color: #f87171; }

/* Audio player label */
.audio-label {
    font-size: 0.75rem;
    color: #8892a4;
    margin-bottom: 4px;
}

/* Success badge */
.badge-ok {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(52,211,153,0.1);
    border: 1px solid rgba(52,211,153,0.25);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.75rem;
    color: #34d399;
}
</style>
""", unsafe_allow_html=True)

# ── Language map ───────────────────────────────────────────────────────────────
LANGUAGES = {
    "Afrikaans": "af", "Albanian": "sq", "Arabic": "ar", "Armenian": "hy",
    "Azerbaijani": "az", "Basque": "eu", "Belarusian": "be", "Bengali": "bn",
    "Bosnian": "bs", "Bulgarian": "bg", "Catalan": "ca",
    "Chinese (Simplified)": "zh-CN", "Chinese (Traditional)": "zh-TW",
    "Croatian": "hr", "Czech": "cs", "Danish": "da", "Dutch": "nl",
    "English": "en", "Esperanto": "eo", "Estonian": "et", "Finnish": "fi",
    "French": "fr", "Galician": "gl", "Georgian": "ka", "German": "de",
    "Greek": "el", "Gujarati": "gu", "Haitian Creole": "ht", "Hebrew": "iw",
    "Hindi": "hi", "Hungarian": "hu", "Icelandic": "is", "Indonesian": "id",
    "Irish": "ga", "Italian": "it", "Japanese": "ja", "Kannada": "kn",
    "Kazakh": "kk", "Korean": "ko", "Latvian": "lv", "Lithuanian": "lt",
    "Macedonian": "mk", "Malay": "ms", "Maltese": "mt", "Marathi": "mr",
    "Mongolian": "mn", "Nepali": "ne", "Norwegian": "no", "Persian": "fa",
    "Polish": "pl", "Portuguese": "pt", "Punjabi": "pa", "Romanian": "ro",
    "Russian": "ru", "Serbian": "sr", "Slovak": "sk", "Slovenian": "sl",
    "Spanish": "es", "Swahili": "sw", "Swedish": "sv", "Tamil": "ta",
    "Telugu": "te", "Thai": "th", "Turkish": "tr", "Ukrainian": "uk",
    "Urdu": "ur", "Uzbek": "uz", "Vietnamese": "vi", "Welsh": "cy",
    "Yiddish": "yi", "Zulu": "zu",
}

LANG_NAMES = ["Auto Detect"] + sorted(LANGUAGES.keys())
TARGET_LANG_NAMES = sorted(LANGUAGES.keys())

# ── Session state ──────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "translation" not in st.session_state:
    st.session_state.translation = ""
if "tts_audio" not in st.session_state:
    st.session_state.tts_audio = None

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("# 🌐 LinguaFlow")
st.markdown(
    '<p class="subtitle">Powered by deep-translator · Google Translate API · 60+ languages</p>',
    unsafe_allow_html=True,
)

# ── Language selectors ─────────────────────────────────────────────────────────
col_src, col_swap, col_tgt = st.columns([5, 1, 5])

with col_src:
    source_lang_name = st.selectbox(
        "Source Language",
        LANG_NAMES,
        index=0,
        key="src_select",
    )

with col_swap:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    swap = st.button("⇄", help="Swap languages", key="swap_btn")

with col_tgt:
    default_tgt_idx = TARGET_LANG_NAMES.index("Spanish")
    target_lang_name = st.selectbox(
        "Target Language",
        TARGET_LANG_NAMES,
        index=default_tgt_idx,
        key="tgt_select",
    )

# Handle swap
if swap:
    if source_lang_name != "Auto Detect" and source_lang_name in TARGET_LANG_NAMES:
        src_idx = LANG_NAMES.index(source_lang_name)
        tgt_idx = TARGET_LANG_NAMES.index(target_lang_name)
        # Streamlit reruns — just swap and rerun via query param trick
        st.session_state["_swap_src"] = target_lang_name
        st.session_state["_swap_tgt"] = source_lang_name
        st.rerun()

# Apply pending swap
if "_swap_src" in st.session_state:
    swap_src = st.session_state.pop("_swap_src")
    swap_tgt = st.session_state.pop("_swap_tgt")
    st.session_state["src_select"] = swap_src
    st.session_state["tgt_select"] = swap_tgt
    st.rerun()

# ── Input text area ────────────────────────────────────────────────────────────
st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
input_text = st.text_area(
    "Enter text to translate",
    placeholder="Type or paste your text here…",
    height=150,
    max_chars=500,
    key="input_text",
    label_visibility="collapsed",
)

# Character counter
char_len = len(input_text)
warn_cls = "warn" if char_len > 450 else ""
st.markdown(
    f'<div class="char-counter {warn_cls}">{char_len} / 500</div>',
    unsafe_allow_html=True,
)

# ── Translate button ───────────────────────────────────────────────────────────
translate_clicked = st.button("Translate →", key="translate_btn", type="primary")

# ── Translation logic ──────────────────────────────────────────────────────────
if translate_clicked:
    if not input_text.strip():
        st.warning("Please enter some text to translate.")
    else:
        src_code = (
            "auto"
            if source_lang_name == "Auto Detect"
            else LANGUAGES[source_lang_name]
        )
        tgt_code = LANGUAGES[target_lang_name]

        if src_code != "auto" and src_code == tgt_code:
            st.error("Source and target languages must be different.")
        else:
            with st.spinner("Translating…"):
                try:
                    translator = GoogleTranslator(source=src_code, target=tgt_code)
                    result = translator.translate(input_text.strip())
                    st.session_state.translation = result
                    st.session_state.tts_audio = None  # reset audio on new translation

                    # Save to history (max 6)
                    st.session_state.history.insert(0, {
                        "src_lang": source_lang_name,
                        "tgt_lang": target_lang_name,
                        "src_text": input_text.strip(),
                        "tgt_text": result,
                    })
                    st.session_state.history = st.session_state.history[:6]

                except Exception as e:
                    st.error(f"Translation error: {e}")
                    st.session_state.translation = ""

# ── Output area ────────────────────────────────────────────────────────────────
st.markdown("<div class='section-label'>Translation</div>", unsafe_allow_html=True)

translation = st.session_state.translation
if translation:
    st.markdown(f'<div class="output-box">{translation}</div>', unsafe_allow_html=True)

    # Action row: copy info + TTS
    col_badge, col_tts = st.columns([3, 2])

    with col_badge:
        st.markdown(
            f'<div style="margin-top:10px"><span class="badge-ok">✓ Translated to {target_lang_name}</span></div>',
            unsafe_allow_html=True,
        )
        # Copy hint
        st.markdown(
            '<p style="font-size:0.75rem;color:#4a5568;margin-top:6px;">Select text above to copy</p>',
            unsafe_allow_html=True,
        )

    with col_tts:
        if st.button("🔊 Listen (TTS)", key="tts_btn"):
            with st.spinner("Generating audio…"):
                try:
                    tgt_code = LANGUAGES[target_lang_name]
                    tts = gTTS(text=translation, lang=tgt_code, slow=False)
                    audio_buffer = io.BytesIO()
                    tts.write_to_fp(audio_buffer)
                    audio_buffer.seek(0)
                    st.session_state.tts_audio = audio_buffer.read()
                except Exception as e:
                    st.error(f"TTS error: {e}")

    # Audio player
    if st.session_state.tts_audio:
        st.markdown('<div class="audio-label">🎵 Audio playback</div>', unsafe_allow_html=True)
        st.audio(st.session_state.tts_audio, format="audio/mp3")

else:
    st.markdown(
        '<div class="output-box empty">Translation will appear here after you click Translate →</div>',
        unsafe_allow_html=True,
    )

# ── History ────────────────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown("<div class='section-label'>Recent Translations</div>", unsafe_allow_html=True)

    for i, item in enumerate(st.session_state.history):
        src_preview = item["src_text"][:80] + ("…" if len(item["src_text"]) > 80 else "")
        tgt_preview = item["tgt_text"][:80] + ("…" if len(item["tgt_text"]) > 80 else "")
        st.markdown(f"""
        <div class="history-card">
            <div class="history-langs">{item['src_lang']} → {item['tgt_lang']}</div>
            <div class="history-src">{src_preview}</div>
            <div class="history-tgt">{tgt_preview}</div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("Clear history", key="clear_history"):
        st.session_state.history = []
        st.rerun()

# ── Footer ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; margin-top:3rem; color:#4a5568; font-size:0.75rem;'>
    Built with Streamlit · deep-translator · gTTS &nbsp;·&nbsp; CodeAlpha AI Internship — Task 1
</div>
""", unsafe_allow_html=True)
