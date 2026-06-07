import streamlit as st
import pdfplumber
import docx

# --- Helper Function ---
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

    else:
        st.error("Unsupported file format!")
        return ""

# --- Streamlit UI ---
st.set_page_config(page_title="Audiobook Generator - Milestone 1", page_icon="📂")

st.title("📂 File Upload & Text Extraction")

uploaded_file = st.file_uploader("Upload your text, PDF, or Word file")

if uploaded_file:
    extracted_text = extract_text(uploaded_file)
    if extracted_text:
        st.success("✅ Text extracted successfully!")
        st.text_area("Extracted Text", extracted_text[:2000], height=300)
