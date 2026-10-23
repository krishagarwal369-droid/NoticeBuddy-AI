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

/* ===== NOTICEBUDDY NEON ARCADE THEME ===== */
/* Strong visible grid directly on the app background */
.stApp {
    position: relative;
    isolation: isolate;
    overflow-x: hidden;
    background-color: #070B19 !important;
    background-image:
        linear-gradient(rgba(102, 122, 255, 0.13) 1px, transparent 1px),
        linear-gradient(90deg, rgba(102, 122, 255, 0.13) 1px, transparent 1px),
        radial-gradient(ellipse at 80% 12%, rgba(125, 62, 255, 0.29), transparent 34%),
        radial-gradient(ellipse at 10% 54%, rgba(0, 180, 255, 0.17), transparent 38%),
        radial-gradient(ellipse at 56% 100%, rgba(87, 51, 255, 0.13), transparent 40%),
        linear-gradient(135deg, #070B19 0%, #10162F 48%, #0C1832 100%);
    background-size: 42px 42px, 42px 42px, auto, auto, auto, 100% 100%;
    background-position: center center;
    background-attachment: fixed;
}

/* Animated perspective floor and luminous atmosphere */
.stApp::before {
    content: "";
    position: fixed;
    left: -12%;
    bottom: -32%;
    width: 124%;
    height: 82%;
    pointer-events: none;
    z-index: 0;
    background-image:
        linear-gradient(rgba(103, 132, 255, 0.46) 1px, transparent 1px),
        linear-gradient(90deg, rgba(103, 132, 255, 0.46) 1px, transparent 1px);
    background-size: 40px 40px;
    transform: perspective(430px) rotateX(60deg);
    transform-origin: center bottom;
    mask-image: linear-gradient(to top, rgba(0,0,0,0.95), transparent 92%);
    opacity: 0.75;
    animation: floorPulse 7s ease-in-out infinite alternate;
}
.stApp::after {
    content: "";
    position: fixed;
    top: 13%;
    right: -115px;
    width: 370px;
    height: 370px;
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
    background: radial-gradient(circle, rgba(137, 83, 255, 0.42), rgba(27, 145, 255, 0.14) 42%, transparent 72%);
    filter: blur(22px);
    animation: neonDrift 7s ease-in-out infinite alternate;
}

/* Streamlit content surfaces stay transparent, above the decoration */
.stAppViewContainer,
div[data-testid="stMain"],
div[data-testid="stMainBlockContainer"],
.main,
header[data-testid="stHeader"] {
    position: relative;
    z-index: 1;
    background: transparent !important;
}
section[data-testid="stSidebar"] {
    position: relative;
    z-index: 2;
    background: linear-gradient(180deg, #0A1025, #11122B 58%, #07152A) !important;
    border-right: 1px solid rgba(111, 108, 255, 0.40);
    box-shadow: 8px 0 32px rgba(39, 28, 109, 0.18);
}

/* HERO — big glowing sci-fi glass panel */
.hero {
    position: relative;
    isolation: isolate;
    overflow: hidden;
    padding: 42px 40px;
    border-radius: 27px;
    background:
        radial-gradient(ellipse at 88% 30%, rgba(148, 74, 255, 0.35), transparent 32%),
        radial-gradient(ellipse at 8% 100%, rgba(0, 190, 255, 0.19), transparent 44%),
        linear-gradient(118deg, rgba(39, 26, 94, 0.98), rgba(13, 75, 123, 0.96), rgba(17, 22, 52, 0.98));
    border: 1px solid rgba(143, 127, 255, 0.82);
    box-shadow: 0 0 0 1px rgba(76, 150, 255, 0.14), 0 18px 55px rgba(37, 26, 124, 0.43), inset 0 1px 0 rgba(255,255,255,0.13);
}
.hero::before {
    content: "";
    position: absolute;
    width: 300px;
    height: 300px;
    right: -35px;
    top: -95px;
    border: 1px solid rgba(193, 184, 255, 0.38);
    border-radius: 50%;
    box-shadow: 0 0 0 18px rgba(122, 103, 255, 0.05), 0 0 0 42px rgba(122, 103, 255, 0.035), inset 0 0 35px rgba(112, 121, 255, 0.12);
    transform: rotate(-24deg);
    animation: orbitFloat 9s ease-in-out infinite alternate;
    z-index: 0;
    pointer-events: none;
}
.hero::after {
    z-index: 0;
    opacity: 0.68;
    filter: blur(1px);
}
.hero > * {
    position: relative;
    z-index: 1;
}
.hero h1 {
    text-shadow: 0 0 26px rgba(156, 134, 255, 0.35);
    letter-spacing: -1.5px;
}
.hero p {
    max-width: 680px;
    font-size: 1.06rem;
}
.eyebrow {
    display: inline-flex;
    align-items: center;
    padding: 8px 13px;
    border: 1px solid rgba(185, 174, 255, 0.5);
    border-radius: 999px;
    background: rgba(105, 81, 255, 0.18);
    box-shadow: 0 0 22px rgba(120, 87, 255, 0.22);
}

/* Color-strip stat cards with a more obvious 3D lift */
.metric {
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(ellipse at 100% 0%, rgba(102, 85, 255, 0.20), transparent 54%),
        linear-gradient(145deg, rgba(28, 38, 76, 0.98), rgba(11, 23, 47, 0.98));
    border: 1px solid rgba(99, 119, 196, 0.62);
    border-radius: 19px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.07), 0 12px 30px rgba(0,0,0,0.22);
    transform-style: preserve-3d;
    transition: transform 0.32s ease, box-shadow 0.32s ease, border-color 0.32s ease;
}
.metric::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #8E61FF, #279BFF, #39E6D1);
    box-shadow: 0 0 19px rgba(112, 104, 255, 0.68);
}
.metric::after {
    content: "";
    position: absolute;
    width: 84px;
    height: 84px;
    right: -32px;
    bottom: -42px;
    border: 1px solid rgba(141, 126, 255, 0.26);
    border-radius: 50%;
    box-shadow: 0 0 0 12px rgba(107, 99, 255, 0.05), 0 0 0 24px rgba(107, 99, 255, 0.04);
    pointer-events: none;
}
.metric:hover {
    transform: perspective(950px) rotateY(-6deg) rotateX(4deg) translateY(-8px) scale(1.015);
    box-shadow: 0 21px 44px rgba(80, 66, 255, 0.28);
    border-color: rgba(145, 129, 255, 0.95);
}
.metric-label {
    text-transform: uppercase;
    letter-spacing: 1.7px;
    font-size: 11px;
}
.metric-value {
    text-shadow: 0 0 18px rgba(90, 147, 255, 0.18);
}

/* Frosted glass info cards with luminous top edge */
.panel {
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(ellipse at 100% 0%, rgba(77, 88, 206, 0.16), transparent 42%),
        linear-gradient(145deg, rgba(23, 33, 65, 0.94), rgba(9, 20, 42, 0.96));
    border: 1px solid rgba(93, 116, 183, 0.62);
    border-radius: 20px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.07), 0 15px 35px rgba(0,0,0,0.18);
    transition: border-color 0.25s ease, box-shadow 0.25s ease, transform 0.25s ease;
}
.panel::before {
    content: "";
    position: absolute;
    left: 22px;
    right: 22px;
    top: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(122, 115, 255, 0.85), rgba(44, 195, 255, 0.70), transparent);
}
.panel:hover {
    transform: translateY(-2px);
    border-color: rgba(123, 134, 255, 0.84);
    box-shadow: 0 18px 38px rgba(58, 70, 160, 0.20);
}

/* Bright gradient call-to-action buttons */
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(105deg, #8A4DFF 0%, #536BFF 48%, #169CF5 100%) !important;
    background-size: 180% 180% !important;
    color: white !important;
    border: 1px solid rgba(195, 184, 255, 0.45) !important;
    border-radius: 14px !important;
    font-weight: 800 !important;
    letter-spacing: 0.2px;
    box-shadow: 0 8px 25px rgba(91, 83, 255, 0.30), inset 0 1px 0 rgba(255,255,255,0.18);
    transition: transform 0.22s ease, box-shadow 0.22s ease, filter 0.22s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-3px) scale(1.01);
    filter: brightness(1.12);
    box-shadow: 0 12px 34px rgba(91, 83, 255, 0.53);
}

/* Inputs and uploader styled to match the neon look */
div[data-testid="stTextArea"] textarea {
    background: rgba(9, 17, 37, 0.96) !important;
    border: 1px solid rgba(84, 107, 179, 0.75) !important;
    border-radius: 15px !important;
    box-shadow: inset 0 2px 12px rgba(0,0,0,0.20);
}
div[data-testid="stTextArea"] textarea:focus {
    border-color: #9A82FF !important;
    box-shadow: 0 0 0 2px rgba(141, 122, 255, 0.22), 0 0 22px rgba(109, 89, 255, 0.16) !important;
}
div[data-testid="stFileUploader"] {
    background: rgba(12, 22, 45, 0.88) !important;
    border: 1px dashed rgba(115, 142, 230, 0.86) !important;
    border-radius: 16px !important;
    box-shadow: inset 0 0 25px rgba(67, 94, 255, 0.07);
}
div[data-testid="stSelectbox"] > div > div {
    background: rgba(12, 22, 45, 0.94);
    border-color: rgba(88, 109, 179, 0.72);
    border-radius: 13px;
}
hr {
    border-image: linear-gradient(90deg, transparent, rgba(121, 113, 255, 0.7), rgba(37, 167, 255, 0.5), transparent) 1;
}
h2 {
    text-shadow: 0 0 18px rgba(101, 110, 255, 0.16);
}
.small-note {
    color: #AAB6D8;
    font-size: 12px;
}

/* Animation */
@keyframes floorPulse {
    from { transform: perspective(430px) rotateX(60deg) translateY(0); }
    to { transform: perspective(430px) rotateX(60deg) translateY(22px); }
}
@keyframes neonDrift {
    from { transform: translate(-15px, -10px) scale(0.92); }
    to { transform: translate(-95px, 52px) scale(1.14); }
}
@keyframes orbitFloat {
    from { transform: rotate(-24deg) translateY(-5px); }
    to { transform: rotate(12deg) translateY(14px); }
}
@media (prefers-reduced-motion: reduce) {
    .hero::after, .hero::before, .stApp::before, .stApp::after {
        animation: none;
    }
    .metric, .panel, .stButton > button, .stDownloadButton > button {
        transition: none;
    }
}


/* Robot art in the hero panel */
.hero-content {
    display: grid;
    grid-template-columns: minmax(0, 1.08fr) minmax(220px, 0.92fr);
    align-items: center;
    gap: 1.15rem;
    position: relative;
    z-index: 1;
}
.hero-copy {
    min-width: 0;
    position: relative;
    z-index: 2;
}
.hero-robot-wrap {
    min-width: 0;
    min-height: 265px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    z-index: 1;
}
.hero-robot-wrap::before {
    content: "";
    position: absolute;
    width: 86%;
    aspect-ratio: 1;
    max-width: 340px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(59, 126, 255, 0.30), rgba(121, 67, 255, 0.15) 45%, transparent 72%);
    filter: blur(14px);
    animation: neonDrift 7s ease-in-out infinite alternate;
}
.hero-robot {
    position: relative;
    display: block;
    width: 100%;
    max-width: 330px;
    max-height: 345px;
    height: auto;
    object-fit: contain;
    border: 0;
    border-radius: 18px;
    mix-blend-mode: screen;
    filter: drop-shadow(0 0 24px rgba(72, 96, 255, 0.34));
    animation: robotFloat 5s ease-in-out infinite;
}
@keyframes robotFloat {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(-9px) rotate(1deg); }
}
@media (max-width: 760px) {
    .hero-content {
        grid-template-columns: 1fr;
        gap: 0.35rem;
    }
    .hero { padding: 28px 22px; }
    .hero-robot-wrap { min-height: 160px; margin-top: 0.25rem; }
    .hero-robot { max-height: 225px; max-width: 245px; }
    .hero h1 { font-size: clamp(30px, 8vw, 42px); }
}


/* Creator credit */
.creator-byline {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    margin-top: 14px;
    padding: 8px 13px;
    border: 1px solid rgba(150, 137, 255, 0.50);
    border-radius: 999px;
    background: linear-gradient(100deg, rgba(121, 78, 255, 0.20), rgba(37, 160, 255, 0.12));
    color: #E7E7FF;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.25px;
    box-shadow: 0 0 20px rgba(113, 90, 255, 0.16), inset 0 1px 0 rgba(255,255,255,0.08);
}
.creator-byline .creator-star {
    color: #64D9FF;
    text-shadow: 0 0 12px rgba(100, 217, 255, 0.7);
    font-size: 15px;
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
robot_image_url = "https://raw.githubusercontent.com/krishagarwal369-droid/NoticeBuddy-AI/main/Neon%20AI%20Robot%20Greeting.png"

st.markdown(f"""
<div class="hero">
  <div class="hero-content">
    <div class="hero-copy">
      <div class="eyebrow">YOUR PERSONAL NOTICE ASSISTANT</div>
      <h1>Confusing notices?<br>We've got you. ✨</h1>
      <p>Turn college, scholarship and government notices into
      simple explanations and clear next steps.</p>
      <div class="creator-byline"><span class="creator-star">✦</span> Built by Kushagra Agarwal</div>
    </div>
    <div class="hero-robot-wrap">
      <img class="hero-robot" src="{robot_image_url}" alt="NoticeBuddy AI robot assistant">
    </div>
  </div>
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
