import streamlit as st
import requests
import pdfplumber, docx

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

st.title("🧠 LLM-Based Text Rewriter")

backend_url = st.text_input("Backend URL", value="http://127.0.0.1:8000")
api_key = st.text_input("OpenAI API Key", type="password")
uploaded_file = st.file_uploader("Upload a document")

if uploaded_file:
    text = extract_text(uploaded_file)
    st.text_area("Extracted Text", text[:2000])

    style_prompt = st.text_input("Narration Style", value="an engaging audiobook style")

    if st.button("Rewrite Text"):
        payload = {"text": text, "style_prompt": style_prompt, "api_key": api_key}
        response = requests.post(f"{backend_url}/rewrite", json=payload)
        rewritten = response.json().get("rewritten_text", "")
        st.text_area("Rewritten Text", rewritten)
