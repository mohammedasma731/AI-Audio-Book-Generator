from gtts import gTTS
import tempfile, os
import streamlit as st

def generate_audio(text, lang="en"):
    tts = gTTS(text=text, lang=lang)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp.name)
    return tmp.name

st.title("🎧 Text to Audio Generator")

text = st.text_area("Enter Text to Convert")
lang = st.selectbox("Language", ["English (en)", "Hindi (hi)", "French (fr)", "German (de)", "Spanish (es)"])
lang_code = lang.split("(")[-1].strip(")")

if st.button("Generate Audio"):
    if text.strip():
        audio_path = generate_audio(text, lang_code)
        st.audio(audio_path, format="audio/mp3")
        with open(audio_path, "rb") as f:
            st.download_button("Download Audio", f, file_name="audiobook.mp3")
        os.remove(audio_path)
