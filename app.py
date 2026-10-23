import fitz
import streamlit as st
from PIL import Image
from google import genai
import easyocr
import numpy as np

st.set_page_config(
    page_title="NoticeBuddy AI",
    page_icon="📄",
    layout="wide"
)

# ---------- DESIGN ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: linear-gradient(135deg,#080D1C,#111631,#101D39);
    color: #F4F6FF;
    font-family: Inter, sans-serif;
}
header[data-testid="stHeader"] {
    background: transparent;
}
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
}
h1,h2,h3,p,label {
    color: #F4F6FF !important;
}
.hero {
    position: relative;
    overflow: hidden;
    isolation: isolate;
    padding: 36px;
    border-radius: 24px;
    background: linear-gradient(120deg,#29205D,#164477,#151A36);
    border: 1px solid #5147A0;
    margin-bottom: 24px;
    box-shadow: 0 15px 45px #11142D;
}
.hero h1 {
    font-size: clamp(30px,4vw,48px);
    line-height: 1.15;
    margin: 12px 0;
}
.hero p {
    color: #D0D8F4 !important;
}
.eyebrow {
    color: #B9AEFF;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
}
.hero::after {
    content: "";
    position: absolute;
    width: 210px;
    height: 210px;
    right: 7%;
    top: 10%;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%,
        #D1C7FF,#8057FF 35%,#238CFF 65%,transparent 75%);
    box-shadow: 0 0 70px #7857FF;
    filter: blur(2px);
    opacity: .8;
    animation: floatOrb 6s ease-in-out infinite;
    z-index: -1;
}
@keyframes floatOrb {
    0%,100% { transform: translate(0,0) scale(1); }
    50% { transform: translate(-18px,15px) scale(1.08); }
}
.metric {
    background: #171F3D;
    border: 1px solid #303B65;
    border-radius: 17px;
    padding: 20px;
    transition: .3s;
    min-height: 105px;
    margin-bottom: 10px;
}
.metric:hover {
    transform: perspective(800px) rotateX(4deg)
               rotateY(-4deg) translateY(-6px);
    box-shadow: 0 15px 30px #27205A;
    border-color: #8574FF;
}
.metric-label {
    color: #ABB8DB;
    font-size: 13px;
}
.metric-value {
    font-size: 21px;
    font-weight: 800;
    margin-top: 10px;
    color: white;
}
.panel {
    background: #141C35;
    border: 1px solid #303B60;
    border-radius: 18px;
    padding: 22px;
    margin: 10px 0;
}
div[data-testid="stTextArea"] textarea {
    background: #101831 !important;
    color: white !important;
    border: 1px solid #35446F !important;
    border-radius: 12px !important;
}
div[data-testid="stFileUploader"] {
    background: #101831;
    border: 1px dashed #5969A5;
    border-radius: 12px;
    padding: 12px;
}
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(100deg,#7857F6,#3989FF);
    color: white;
    border: 0;
    border-radius: 12px;
    font-weight: 700;
    min-height: 45px;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    color: white;
    box-shadow: 0 0 20px #5144A0;
}
div[data-testid="stSidebar"] {
    background: #0B1022;
    border-right: 1px solid #283253;
}
hr { border-color: #293557; }
.small-note { color: #AAB6D8; font-size: 12px; }

@media (prefers-reduced-motion: reduce) {
    .hero::after { animation: none; }
}

/* DECORATIVE FUTURISTIC BACKGROUND */
.stApp {
    position: relative;
    isolation: isolate;
    overflow-x: hidden;
    background:
        radial-gradient(ellipse at 82% 14%, rgba(118, 82, 255, 0.22), transparent 32%),
        radial-gradient(ellipse at 8% 65%, rgba(37, 133, 255, 0.12), transparent 38%),
        linear-gradient(135deg, #080D1C 0%, #111631 52%, #101D39 100%);
}

/* Soft perspective grid on the page floor */
.stApp::before {
    content: "";
    position: fixed;
    left: -15%;
    bottom: -28%;
    width: 130%;
    height: 78%;
    pointer-events: none;
    z-index: 0;
    background-image:
        linear-gradient(rgba(117, 134, 255, 0.34) 1px, transparent 1px),
        linear-gradient(90deg, rgba(117, 134, 255, 0.34) 1px, transparent 1px);
    background-size: 46px 46px;
    transform: perspective(460px) rotateX(58deg);
    transform-origin: center bottom;
    mask-image: linear-gradient(to top, rgba(0, 0, 0, 0.9), transparent 90%);
    opacity: 0.72;
    animation: gridDrift 8s ease-in-out infinite alternate;
}

/* Large drifting purple-blue glow */
.stApp::after {
    content: "";
    position: fixed;
    top: 14%;
    right: -100px;
    width: 340px;
    height: 340px;
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
    background: radial-gradient(circle, rgba(126, 76, 255, 0.33), rgba(35, 140, 255, 0.12) 45%, transparent 72%);
    filter: blur(24px);
    animation: glowDrift 8s ease-in-out infinite alternate;
}

/* Keep all Streamlit surfaces transparent so the decoration is visible */
.stAppViewContainer,
div[data-testid="stMain"],
div[data-testid="stMainBlockContainer"],
.main,
header[data-testid="stHeader"] {
    position: relative;
    z-index: 1;
    background-color: transparent !important;
}
section[data-testid="stSidebar"] {
    position: relative;
    z-index: 2;
    background: #0B1022;
}

/* Hero card: richer gradient + visible floating orb */
.hero {
    position: relative;
    isolation: isolate;
    overflow: hidden;
    background:
        radial-gradient(circle at 88% 28%, rgba(126, 76, 255, 0.28), transparent 28%),
        linear-gradient(120deg, rgba(41, 32, 93, 0.96), rgba(22, 68, 119, 0.94), rgba(21, 26, 54, 0.97));
    border: 1px solid rgba(135, 123, 255, 0.72);
    box-shadow: 0 14px 46px rgba(24, 22, 75, 0.52), inset 0 1px 0 rgba(255,255,255,0.08);
}
.hero::after {
    z-index: 0;
    opacity: 0.58;
}
.hero > * {
    position: relative;
    z-index: 1;
}
.hero h1 {
    text-shadow: 0 0 24px rgba(145, 120, 255, 0.22);
}
.eyebrow {
    display: inline-block;
    padding: 7px 11px;
    border: 1px solid rgba(185, 174, 255, 0.35);
    border-radius: 999px;
    background: rgba(115, 86, 255, 0.13);
    box-shadow: 0 0 22px rgba(120, 87, 255, 0.12);
}

/* Decorative accent and responsive 3D cards */
.metric {
    position: relative;
    overflow: hidden;
    background: linear-gradient(145deg, rgba(27, 36, 70, 0.98), rgba(19, 27, 52, 0.98));
    border: 1px solid rgba(91, 111, 177, 0.46);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.045), 0 10px 24px rgba(0,0,0,0.12);
    transform-style: preserve-3d;
    transition: transform 0.35s ease, box-shadow 0.35s ease, border-color 0.35s ease;
}
.metric::before {
    content: "";
    position: absolute;
    top: 0;
    left: 16px;
    right: 16px;
    height: 2px;
    border-radius: 999px;
    background: linear-gradient(90deg, #7C5CFF, #3989FF, #4FE2D0);
    box-shadow: 0 0 16px rgba(112, 104, 255, 0.45);
}
.metric:hover {
    transform: perspective(900px) rotateY(-4deg) rotateX(3deg) translateY(-6px);
    box-shadow: 0 18px 40px rgba(77, 69, 255, 0.24);
    border-color: rgba(133, 116, 255, 0.8);
}

/* Glass-like info panels */
.panel {
    background: linear-gradient(145deg, rgba(23, 32, 61, 0.88), rgba(15, 24, 47, 0.94));
    border: 1px solid rgba(84, 103, 166, 0.55);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.04), 0 12px 28px rgba(0,0,0,0.12);
    transition: border-color 0.25s ease, transform 0.25s ease, box-shadow 0.25s ease;
}
.panel:hover {
    border-color: rgba(117, 130, 255, 0.68);
    box-shadow: 0 14px 30px rgba(58, 70, 160, 0.15);
}

/* Neon buttons and focused inputs */
.stButton > button, .stDownloadButton > button {
    box-shadow: 0 5px 18px rgba(91, 83, 255, 0.22);
    transition: transform 0.2s ease, box-shadow 0.2s ease, filter 0.2s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-2px);
    filter: brightness(1.08);
    box-shadow: 0 8px 26px rgba(91, 83, 255, 0.42);
}
div[data-testid="stTextArea"] textarea:focus {
    border-color: #8D7AFF !important;
    box-shadow: 0 0 0 2px rgba(141, 122, 255, 0.18) !important;
}

/* Motion */
@keyframes gridDrift {
    from { transform: perspective(460px) rotateX(58deg) translateY(0); }
    to   { transform: perspective(460px) rotateX(58deg) translateY(18px); }
}
@keyframes glowDrift {
    from { transform: translate(-15px, -10px) scale(0.92); }
    to   { transform: translate(-95px, 52px) scale(1.12); }
}
@media (prefers-reduced-motion: reduce) {
    .hero::after, .stApp::before, .stApp::after {
        animation: none;
    }
    .metric, .panel, .stButton > button, .stDownloadButton > button {
        transition: none;
    }
}

</style>  

""", unsafe_allow_html=True)


# ---------- OCR ----------
@st.cache_resource
def get_reader():
    return easyocr.Reader(["en"], gpu=False)


# ---------- AI ----------
def explain_notice(text, language):
    client = genai.Client(
        api_key=st.secrets["GEMMA_API_KEY"]
    )

    prompt = f"""
You are NoticeBuddy AI, a careful notice explanation assistant.

Explain this notice in {language}, using simple student-friendly language.
Use only information present in the notice. Never invent facts,
dates, eligibility criteria, fees, links or required documents.
If information is missing, say "Not mentioned in the notice".
Flag uncertain OCR text and remind the user to verify details
against the original official notice.

Use these sections:
## ✨ Simple Summary
## 📅 Important Dates
## 🎯 Eligibility
## 📑 Required Documents
## ✅ What To Do Next
## ⚠️ Important Notes

NOTICE:
{text}
"""
    response = client.models.generate_content(
        model="gemma-4-26b-a4b-it",
        contents=prompt
    )
    return response.text or "No explanation was returned."


# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 📄 NoticeBuddy AI")
    st.caption("Your personal notice assistant")
    st.markdown("---")
    page = st.radio(
        "NAVIGATION",
        ["🏠 Dashboard", "📘 How it works", "ℹ️ About"]
    )
    st.markdown("---")
    st.markdown("**AI-powered notice help**")
    st.caption("Read • Understand • Take action")


# ---------- HERO ----------
st.markdown("""
<div class="hero">
  <div class="eyebrow">YOUR PERSONAL NOTICE ASSISTANT</div>
  <h1>Confusing notices?<br>We've got you. ✨</h1>
  <p>Turn college, scholarship and government notices into
  simple explanations and clear next steps.</p>
</div>
""", unsafe_allow_html=True)


if page == "📘 How it works":
    st.markdown("## How it works")
    st.markdown("""
    <div class="panel">
    <h3>01 · Upload</h3>Paste notice text or upload an image.
    <hr>
    <h3>02 · Understand</h3>AI explains it in your selected language.
    <hr>
    <h3>03 · Take action</h3>Review dates, eligibility and documents.
    </div>
    """, unsafe_allow_html=True)

elif page == "ℹ️ About":
    st.markdown("## About NoticeBuddy AI")
    st.markdown("""
    <div class="panel">
    NoticeBuddy AI helps students understand official notices
    more easily by extracting text and organizing important details.
    <br><br>
    Always verify important information with the original official notice.
    </div>
    """, unsafe_allow_html=True)

else:
    # ---------- DASHBOARD ----------
    c1, c2, c3 = st.columns(3)

    for col, title, value in [
        (c1, "INPUT", "Text + Image"),
        (c2, "POWERED BY", "Generative AI"),
        (c3, "BUILT FOR", "Students 🎓")
    ]:
        with col:
            st.markdown(
                f'<div class="metric"><div class="metric-label">'
                f'{title}</div><div class="metric-value">{value}'
                f'</div></div>',
                unsafe_allow_html=True
            )

    left, right = st.columns([1.05, .95], gap="large")

    with left:
        st.markdown("## 📝 Analyze a notice")
        language = st.selectbox(
            "Explanation language", ["English", "Hindi"]
        )
        notice = st.text_area(
            "Paste notice text",
            placeholder="Paste your notice here...",
            height=190
        )
        uploaded_file = st.file_uploader(
            "Or upload a notice image",
            type=["png", "jpg", "jpeg","pdf"]
        )
        analyze = st.button(
            "✨ Extract & Explain",
            type="primary",
            use_container_width=True
        )

    with right:
        st.markdown("## 💡 What you'll get")
        st.markdown("""
        <div class="panel">
        <h3>📌 Simple summary</h3>Understand the main message.
        <hr>
        <h3>📅 Important dates</h3>Find deadlines in the notice.
        <hr>
        <h3>🎯 Eligibility</h3>See the stated requirements.
        <hr>
        <h3>📑 Document checklist</h3>Review required documents.
        </div>
        """, unsafe_allow_html=True)

    if analyze:
        text = notice.strip()

        if uploaded_file:
            try:
                with st.spinner("Reading your notice..."):
                    if uploaded_file.name.lower().endswith(".pdf"):
                        import fitz
                        pdf = fitz.open(
                            stream=uploaded_file.getvalue(),
                            filetype="pdf"
                        )
                        pdf_text = "\n".join(
                            page.get_text() for page in pdf
                        )
                        pdf.close()
                        text = (text + "\n" + pdf_text).strip()

                        if not pdf_text.strip():
                            st.warning(
                                "PDF has no selectable text. "
                                "Scanned PDF needs OCR."
                            )
                    else:
                        image = Image.open(uploaded_file).convert("RGB")
                        results = get_reader().readtext(np.array(image))
                        image_text = " ".join(item[1] for item in results)
                        text = (text + "\n" + image_text).strip()

            except Exception as e:
                st.error(f"Could not read file: {e}")
                text = ""

        if not text:
            st.warning("Please paste text or upload an image.")
        else:
            with st.expander("View extracted notice text"):
                st.write(text)

            try:
                with st.spinner("🧠 AI is analyzing your notice..."):
                    explanation = explain_notice(text, language)

                st.markdown("## 🤖 Your notice explained")
                st.markdown(
                    '<div class="panel">',
                    unsafe_allow_html=True
                )
                st.markdown(explanation)
                st.markdown("</div>", unsafe_allow_html=True)

                st.download_button(
                    "⬇️ Download explanation",
                    data=explanation,
                    file_name="noticebuddy_explanation.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(
                    "AI request failed. Check internet, API key and model access."
                )
                st.caption(f"Technical details: {e}")

st.markdown("---")
st.markdown(
    '<p class="small-note" style="text-align:center">'
    'NoticeBuddy AI · Making important information easier to understand.'
    '</p>',
    unsafe_allow_html=True
)
