import streamlit as st
import requests
from gtts import gTTS
import pdfplumber, docx, tempfile, io, base64, os

def extract_text(uploaded_file):
    if uploaded_file.name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".pdf"):
        text = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    elif uploaded_file.name.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        return "\n".join(p.text for p in doc.paragraphs)
    return ""

def rewrite_text(api_key, text, style_prompt, backend_url):
    payload = {"text": text, "api_key": api_key, "style_prompt": style_prompt}
    res = requests.post(f"{backend_url}/rewrite", json=payload)
    return res.json().get("rewritten_text", "")

def generate_audio(text, lang="en"):
    tts = gTTS(text=text, lang=lang)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp.name)
    return tmp.name

st.title("🎧 AI Audiobook Generator - Full Workflow")

backend_url = st.text_input("Backend URL", value="http://127.0.0.1:8000")
api_key = st.text_input("OpenAI API Key", type="password")
uploaded_file = st.file_uploader("Upload a file (.txt, .pdf, .docx)")

if uploaded_file:
    text = extract_text(uploaded_file)
    st.text_area("Extracted Text", text[:2000])
    style_prompt = st.text_input("Narration Style", value="an engaging audiobook style")

    if st.button("Rewrite Text"):
        rewritten = rewrite_text(api_key, text, style_prompt, backend_url)
        st.text_area("Rewritten Text", rewritten[:2000])
        lang = st.selectbox("Select Audio Language", ["English (en)", "Hindi (hi)", "French (fr)", "German (de)", "Spanish (es)"])
        lang_code = lang.split("(")[-1].strip(")")

        if st.button("Generate Audiobook"):
            audio_path = generate_audio(rewritten, lang=lang_code)
            st.audio(audio_path, format="audio/mp3")
            with open(audio_path, "rb") as f:
                st.download_button("⬇️ Download Audiobook", f, file_name="audiobook.mp3")
            os.remove(audio_path)
