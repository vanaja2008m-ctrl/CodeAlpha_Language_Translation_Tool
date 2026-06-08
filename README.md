# 🌐 LinguaFlow — Language Translation Tool

**CodeAlpha AI Internship — Task 1**

A sleek language translation web app built with **Streamlit**, **deep-translator**, and **gTTS**.

---

## Features

- 🌍 Translate text across **60+ languages**
- 🔍 **Auto-detect** source language
- 🔊 **Text-to-Speech** playback of translated text (via gTTS)
- 🔄 **Swap** source and target languages instantly
- 🕐 **Translation history** — last 6 translations saved per session
- 500-character input limit with live counter

---

## Tech Stack

| Library | Purpose |
|---|---|
| `streamlit` | Web UI framework |
| `deep-translator` | Google Translate API wrapper |
| `gTTS` | Google Text-to-Speech audio generation |

---

## Setup & Run

### 1. Clone / download

```bash
git clone https://github.com/YOUR_USERNAME/CodeAlpha_LanguageTranslationTool
cd CodeAlpha_LanguageTranslationTool
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

The app opens automatically at **http://localhost:8501**

---

## Project Structure

```
CodeAlpha_LanguageTranslationTool/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md
```

---

## How It Works

1. User enters text and selects source + target languages
2. `deep-translator` sends the text to Google Translate and returns the result
3. The translated text is displayed in the output panel
4. Optionally, `gTTS` converts the translated text to speech and plays it in-browser via Streamlit's `st.audio`

---
