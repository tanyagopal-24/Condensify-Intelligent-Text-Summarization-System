import streamlit as st
import nltk
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader
from docx import Document
import time

# Page Configuration
st.set_page_config(
    page_title="Condensify",
    page_icon="📚",
    layout="wide"
)

# Styling 
st.markdown("""
<style>
.big-title {
    font-size: clamp(80px, 12vw, 156px);
    font-weight: 900;
    color: #ffffff !important;
    margin-bottom: 5px;
    text-align: left;
    line-height: 1.05;
}
.subtitle {
    font-size:14px;
    color: gray;
}
.small-text {
    font-size:13px !important;
}
.summary-box {
    background-color: #1e1e1e;
    padding: 18px;
    border-radius: 14px;
    animation: fadeIn 0.8s ease-in;
}
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
</style>
""", unsafe_allow_html=True)

# Header Section
colA, colB = st.columns([1.2, 6], vertical_alignment="center")

with colA:
    st.image("https://cdn-icons-png.flaticon.com/512/3145/3145765.png", width=80)

with colB:
    st.markdown('<p class="big-title"><i>Condensify</i></p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Interactive NLP-Based Intelligent Text Summarization</p>',
        unsafe_allow_html=True
    )
    st.caption("Transform long documents into intelligent concise summaries instantly.")

# NLTK Setup
try:
    nltk.data.find('tokenizers/punkt')
except:
    nltk.download('punkt')

# Sidebar 
with st.sidebar:
    st.header("⚙️ Controls")
    num_sentences = st.slider("Summary Sentences", 1, 10, 3)
    show_chart = st.toggle("Show Chart", True)
    show_metrics = st.toggle("Show Metrics", True)

    st.markdown("---")
    st.markdown("### 🧠 Engine")
    st.caption("• NLTK Tokenization")
    st.caption("• TF-IDF Vectorization")
    st.caption("• Unsupervised Extractive Model")

# File Upload 
uploaded_file = st.file_uploader(
    "📂 Upload TXT, PDF, or Word File",
    type=["txt", "pdf", "docx"]
)

text = ""

if uploaded_file:

    if uploaded_file.type == "application/pdf":
        pdf = PdfReader(uploaded_file)
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted

    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"

    elif uploaded_file.type == "text/plain":
        text = uploaded_file.read().decode("utf-8")

else:
    text = st.text_area("✍️ Or Enter Text Below:", height=220)

# Summarization Function
def summarize_text(text, num_sentences):
    sentences = sent_tokenize(text)

    if len(sentences) <= num_sentences:
        return text

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(sentences)

    sentence_scores = np.array(tfidf_matrix.sum(axis=1)).flatten()
    top_indices = sentence_scores.argsort()[-num_sentences:]
    top_indices = sorted(top_indices)

    summary = " ".join([sentences[i] for i in top_indices])
    return summary

# Generate Button 
if st.button("🚀 Generate Summary"):

    if text.strip():

        progress_bar = st.progress(0)
        status_text = st.empty()

        status_text.text("📖 Parsing document...")
        time.sleep(0.4)
        progress_bar.progress(25)

        status_text.text("🧠 Vectorizing sentences...")
        time.sleep(0.4)
        progress_bar.progress(50)

        status_text.text("📊 Ranking sentences...")
        time.sleep(0.4)
        progress_bar.progress(75)

        status_text.text("🔎 Condensing content...")
        summary = summarize_text(text, num_sentences)
        time.sleep(0.4)
        progress_bar.progress(100)

        status_text.empty()
        progress_bar.empty()

        st.success("Summary Generated Successfully!")

        st.markdown("### 📌 Summary Output")
        st.markdown(
            f'<div class="summary-box small-text">{summary}</div>',
            unsafe_allow_html=True
        )

        # Metrics
        original_length = len(text.split())
        summary_length = len(summary.split())

        retained_percentage = round((summary_length / original_length) * 100, 2)
        reduction_percentage = round(100 - retained_percentage, 2)

        if show_metrics:
            col1, col2, col3 = st.columns(3)
            col1.metric("Original Words", original_length)
            col2.metric("Summary Words", summary_length)
            col3.metric("Content Reduced", f"{reduction_percentage}%")

        # Chart 
        if show_chart:
            st.markdown("### 📊 Comparison Chart")
            fig, ax = plt.subplots(figsize=(4, 3))
            ax.bar(["Original", "Summary"], [original_length, summary_length])
            ax.set_ylabel("Words")
            st.pyplot(fig)

        # Download
        st.download_button(
            "⬇ Download Summary",
            summary,
            file_name="summary.txt",
            mime="text/plain"
        )

    else:
        st.warning("Please enter or upload text first.")