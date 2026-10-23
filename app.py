import fitz
import streamlit as st
from PIL import Image
from google import genai
import easyocr
import numpy as np
import re
import json
from html import escape as html_escape
import uuid
import calendar as calendar_module
from datetime import date, datetime, timedelta
import streamlit.components.v1 as components
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
    background: linear-gradient(100deg, #FFFFFF 0%, #C7C4FF 42%, #76D7FF 82%, #FFFFFF 100%);
    background-size: 220% auto;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent !important;
    color: transparent !important;
    text-shadow: 0 0 26px rgba(156, 134, 255, 0.22);
    letter-spacing: -1.5px;
    animation: titleShimmer 8s ease-in-out infinite alternate;
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
    .hero::after, .hero::before, .stApp::before, .stApp::after,
    .hero-robot, .hero-robot-wrap::after, .hero-particles span, .hero h1 {
        animation: none;
    }
    .metric, .panel, .stButton > button, .stDownloadButton > button {
        transition: none;
    }
}


/* Tiny floating stars in the hero panel */
.hero-particles {
    position: absolute;
    inset: 0;
    overflow: hidden;
    z-index: 0;
    pointer-events: none;
}
.hero-particles span {
    position: absolute;
    display: block;
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background: #A9B8FF;
    box-shadow: 0 0 9px 2px rgba(115, 143, 255, 0.72);
    opacity: 0;
    animation: particleRise 8s ease-in-out infinite;
}
.hero-particles span:nth-child(1) { left: 7%; top: 74%; animation-delay: -1s; }
.hero-particles span:nth-child(2) { left: 18%; top: 24%; width: 3px; height: 3px; animation-delay: -5s; }
.hero-particles span:nth-child(3) { left: 36%; top: 82%; animation-delay: -3s; }
.hero-particles span:nth-child(4) { left: 54%; top: 16%; width: 3px; height: 3px; animation-delay: -6s; }
.hero-particles span:nth-child(5) { left: 71%; top: 72%; animation-delay: -2s; }
.hero-particles span:nth-child(6) { left: 91%; top: 30%; width: 5px; height: 5px; animation-delay: -4s; }
.hero-particles span:nth-child(7) { left: 43%; top: 45%; width: 2px; height: 2px; animation-delay: -7s; }
.hero-particles span:nth-child(8) { left: 83%; top: 86%; width: 3px; height: 3px; animation-delay: -1.5s; }
@keyframes particleRise {
    0%, 100% { transform: translate3d(0, 12px, 0) scale(0.55); opacity: 0; }
    22%, 72% { opacity: 0.86; }
    50% { transform: translate3d(16px, -16px, 0) scale(1.25); opacity: 1; }
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
    background: radial-gradient(circle, rgba(59, 126, 255, 0.34), rgba(121, 67, 255, 0.18) 45%, transparent 72%);
    filter: blur(14px);
    animation: neonDrift 7s ease-in-out infinite alternate;
    z-index: 0;
}
.hero-robot-wrap::after {
    content: "";
    position: absolute;
    width: 88%;
    max-width: 350px;
    aspect-ratio: 1;
    border-radius: 50%;
    border: 1px solid rgba(109, 205, 255, 0.48);
    box-shadow: 0 0 0 12px rgba(103, 105, 255, 0.055), 0 0 0 26px rgba(103, 105, 255, 0.035), inset 0 0 28px rgba(70, 130, 255, 0.12);
    transform: perspective(400px) rotateX(62deg) rotateZ(-12deg);
    animation: robotRing 16s linear infinite;
    pointer-events: none;
    z-index: 1;
}
.hero-robot-wrap {
    z-index: 2;
}
.hero-robot {
    z-index: 2;
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
@keyframes robotRing {
    from { transform: perspective(400px) rotateX(62deg) rotateZ(-12deg); }
    to { transform: perspective(400px) rotateX(62deg) rotateZ(348deg); }
}
@keyframes titleShimmer {
    from { background-position: 0% center; }
    to { background-position: 100% center; }
}
@media (max-width: 760px) {
    .hero-content {
        grid-template-columns: 1fr;
        gap: 0.35rem;
    }
    .hero { padding: 28px 22px; }
    .hero-robot-wrap { min-height: 160px; margin-top: 0.25rem; }
    .hero-robot { max-height: 225px; max-width: 245px; }
    .hero-robot-wrap::after { max-width: 230px; }
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


/* ===== PREMIUM TOP NAVBAR ===== */
.top-nav {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    margin: 0 0 1.15rem 0;
    padding: 13px 17px;
    border: 1px solid rgba(117, 139, 220, 0.38);
    border-radius: 18px;
    background: linear-gradient(105deg, rgba(15, 24, 52, 0.91), rgba(30, 24, 69, 0.82), rgba(11, 35, 61, 0.89));
    box-shadow: 0 10px 28px rgba(0,0,0,0.16), inset 0 1px 0 rgba(255,255,255,0.07);
    backdrop-filter: blur(16px);
}
.top-nav-brand { display: flex; align-items: center; gap: 11px; min-width: 0; }
.top-nav-logo {
    width: 42px; height: 42px; flex: 0 0 42px;
    display: grid; place-items: center;
    border: 1px solid rgba(184, 169, 255, 0.65);
    border-radius: 13px;
    color: white; font-weight: 900; font-size: 14px;
    background: linear-gradient(140deg, #8054FF, #168DEB);
    box-shadow: 0 0 22px rgba(111, 85, 255, 0.32), inset 0 1px 0 rgba(255,255,255,0.25);
}
.top-nav-wordmark { color: #F5F5FF; font-size: 16px; font-weight: 800; line-height: 1.15; }
.top-nav-wordmark b {
    color: #7EE7FF;
    text-shadow: 0 0 13px rgba(65, 199, 255, 0.45);
}
.top-nav-wordmark small {
    display: block; margin-top: 4px;
    color: #9EAED5; font-size: 9px; font-weight: 700; letter-spacing: 1.7px;
}
.top-nav-right { display: flex; align-items: center; justify-content: flex-end; gap: 15px; flex-wrap: wrap; }
.nav-status {
    display: inline-flex; align-items: center; gap: 7px;
    padding: 7px 10px; border: 1px solid rgba(63, 218, 183, 0.28);
    border-radius: 999px; background: rgba(27, 179, 141, 0.08);
    color: #A8FFE8; font-size: 10px; font-weight: 800; letter-spacing: 1px;
}
.nav-status i {
    display: inline-block; width: 7px; height: 7px; border-radius: 50%;
    background: #46E2B6; box-shadow: 0 0 11px rgba(70, 226, 182, 0.85);
    animation: statusPulse 1.8s ease-in-out infinite;
}
.nav-journey { color: #C4CDEF; font-size: 10px; font-weight: 800; letter-spacing: 1.1px; white-space: nowrap; }
.nav-journey b { color: #8E80FF; padding: 0 3px; }
@keyframes statusPulse {
    0%,100% { opacity: 1; box-shadow: 0 0 10px rgba(70,226,182,0.6); }
    50% { opacity: 0.48; box-shadow: 0 0 3px rgba(70,226,182,0.3); }
}
@media (max-width: 640px) {
    .top-nav { align-items: flex-start; flex-direction: column; padding: 12px; }
    .top-nav-right { justify-content: flex-start; gap: 8px; }
    .nav-journey { font-size: 9px; }
}

/* ===== ANIMATED UPLOAD BOX ===== */
div[data-testid="stFileUploader"] {
    position: relative;
    isolation: isolate;
    overflow: hidden;
    border: 1px dashed rgba(113, 151, 255, 0.88) !important;
    background: linear-gradient(130deg, rgba(11, 24, 49, 0.96), rgba(27, 22, 66, 0.88)) !important;
    box-shadow: inset 0 0 28px rgba(65, 98, 255, 0.09), 0 0 0 1px rgba(100, 115, 255, 0.07);
}
div[data-testid="stFileUploader"]::before {
    content: "";
    position: absolute;
    top: 0; left: -38%; width: 34%; height: 2px;
    background: linear-gradient(90deg, transparent, #8D7BFF, #54DFFF, transparent);
    box-shadow: 0 0 13px rgba(91, 155, 255, 0.62);
    animation: uploadSweep 3.2s linear infinite;
    pointer-events: none;
    z-index: 0;
}
div[data-testid="stFileUploader"] > div { position: relative; z-index: 1; }
@keyframes uploadSweep {
    from { left: -38%; }
    to { left: 104%; }
}

/* ===== AI SCANNER + WAVEFORM DURING ANALYSIS ===== */
.ai-activity-card {
    margin: 0.6rem 0 1.2rem;
    padding: 17px 19px 15px;
    border: 1px solid rgba(107, 131, 220, 0.57);
    border-radius: 19px;
    background: linear-gradient(135deg, rgba(16, 27, 56, 0.97), rgba(25, 23, 67, 0.96), rgba(9, 33, 56, 0.96));
    box-shadow: 0 12px 34px rgba(33, 37, 124, 0.20), inset 0 1px 0 rgba(255,255,255,0.06);
}
.ai-activity-header { display: flex; align-items: center; gap: 9px; color: #EEF0FF; font-size: 13px; }
.activity-pulse {
    display: inline-block; width: 8px; height: 8px; flex: 0 0 8px; border-radius: 50%;
    background: #58E8D0; box-shadow: 0 0 14px rgba(88,232,208,0.78);
    animation: statusPulse 1.2s ease-in-out infinite;
}
.activity-live {
    margin-left: auto; padding: 5px 8px; border-radius: 999px;
    border: 1px solid rgba(89, 209, 255, 0.34);
    color: #85E4FF; background: rgba(36, 147, 213, 0.10);
    font-size: 9px; font-weight: 900; letter-spacing: 1.2px;
}
.scanner-stage {
    height: 112px; position: relative; overflow: hidden; margin: 14px 0 8px;
    border: 1px solid rgba(93, 122, 211, 0.23); border-radius: 12px;
    background-image: linear-gradient(rgba(94, 125, 232, 0.07) 1px, transparent 1px), linear-gradient(90deg, rgba(94, 125, 232, 0.07) 1px, transparent 1px);
    background-size: 18px 18px;
}
.scanner-doc {
    width: 55%; max-width: 260px; height: 76px; margin: 17px auto 0; padding: 13px 15px;
    border-radius: 5px; border: 1px solid rgba(139, 154, 255, 0.36);
    background: rgba(21, 33, 68, 0.69); box-shadow: 0 0 22px rgba(80, 103, 255, 0.08);
}
.doc-line { display: block; height: 3px; margin: 0 0 8px; border-radius: 999px; background: rgba(137, 164, 255, 0.53); }
.doc-line.long { width: 96%; }
.doc-line.medium { width: 70%; }
.doc-line.short { width: 43%; }
.scanner-beam {
    position: absolute; left: 7%; right: 7%; height: 2px; top: 3%;
    background: linear-gradient(90deg, transparent, #5CE5FF 18%, #A99AFF 50%, #5CE5FF 82%, transparent);
    box-shadow: 0 0 13px 2px rgba(66, 200, 255, 0.48);
    animation: scannerMove 2.1s ease-in-out infinite alternate;
}
.scanner-corner { position: absolute; width: 13px; height: 13px; border-color: #6CDFFF; border-style: solid; opacity: 0.9; }
.scanner-corner.top-left { left: 10px; top: 10px; border-width: 1px 0 0 1px; }
.scanner-corner.bottom-right { right: 10px; bottom: 10px; border-width: 0 1px 1px 0; }
@keyframes scannerMove {
    from { top: 4%; }
    to { top: 94%; }
}
.ai-waveform { display: flex; align-items: center; justify-content: center; gap: 4px; height: 28px; margin: 7px 0 3px; }
.ai-waveform span {
    display: block; height: 8px; width: 3px; border-radius: 999px;
    background: linear-gradient(180deg, #7FEAFF, #8F78FF);
    box-shadow: 0 0 7px rgba(91, 174, 255, 0.33);
    animation: waveformPulse 0.9s ease-in-out infinite alternate;
}
.ai-waveform span:nth-child(3n) { animation-delay: -0.6s; }
.ai-waveform span:nth-child(3n+1) { animation-delay: -0.25s; }
.ai-waveform span:nth-child(4n) { height: 18px; }
.ai-waveform span:nth-child(5n) { height: 23px; }
@keyframes waveformPulse {
    from { transform: scaleY(0.45); opacity: 0.52; }
    to { transform: scaleY(1.25); opacity: 1; }
}
.ai-activity-caption { margin-top: 5px; text-align: center; color: #AAB9E7; font-size: 11px; letter-spacing: 0.4px; }

/* ===== COLORFUL AI RESULT CARDS ===== */
div[class*="st-key-result-card-"] {
    position: relative;
    overflow: hidden;
    margin: 0.75rem 0 !important;
    padding: 1rem 1.25rem 0.9rem !important;
    border: 1px solid rgba(100, 124, 194, 0.56) !important;
    border-radius: 18px !important;
    background: linear-gradient(135deg, rgba(22, 33, 67, 0.95), rgba(11, 24, 47, 0.96)) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.055), 0 10px 27px rgba(0,0,0,0.12) !important;
}
div[class*="st-key-result-card-"] h4 { margin-top: 0.25rem; color: #EDEBFF !important; }
div[class*="st-key-result-card-0"] { border-left: 4px solid #A78BFA !important; }
div[class*="st-key-result-card-1"] { border-left: 4px solid #42D8FF !important; }
div[class*="st-key-result-card-2"] { border-left: 4px solid #FF9BD8 !important; }
div[class*="st-key-result-card-3"] { border-left: 4px solid #58E2BE !important; }
div[class*="st-key-result-card-4"] { border-left: 4px solid #FFCF70 !important; }
div[class*="st-key-result-card-5"] { border-left: 4px solid #7FA8FF !important; }

/* Accessibility: reduce decorative motion when requested */
@media (prefers-reduced-motion: reduce) {
    .nav-status i, div[data-testid="stFileUploader"]::before,
    .scanner-beam, .ai-waveform span {
        animation: none;
    }
}


/* Neon section dividers */
h2::after {
    content: "";
    display: block;
    width: 74px;
    height: 3px;
    margin-top: 9px;
    border-radius: 999px;
    background: linear-gradient(90deg, #9B6BFF, #4CCEFF, transparent);
    box-shadow: 0 0 13px rgba(90, 128, 255, 0.38);
}

/* Small glassy icon badges on stat cards */
.metric-icon {
    position: absolute;
    right: 17px;
    top: 17px;
    min-width: 35px;
    height: 35px;
    display: inline-grid;
    place-items: center;
    border-radius: 11px;
    border: 1px solid rgba(164, 155, 255, 0.45);
    background: linear-gradient(135deg, rgba(119, 83, 255, 0.28), rgba(37, 157, 255, 0.16));
    color: #DCD9FF;
    font-size: 18px;
    box-shadow: 0 0 18px rgba(104, 92, 255, 0.16), inset 0 1px 0 rgba(255,255,255,0.12);
}
.metric-label { padding-right: 44px; }

/* Animated workflow timeline */
.workflow-timeline {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 7px;
    margin: 13px 2px 3px;
}
.workflow-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    min-width: 0;
    color: #AEBBE1;
    font-size: 9px;
    letter-spacing: 0.45px;
    text-transform: uppercase;
    animation: workflowGlow 4.4s ease-in-out infinite;
}
.workflow-step span {
    display: grid;
    place-items: center;
    width: 26px;
    height: 26px;
    border-radius: 50%;
    border: 1px solid rgba(117, 145, 255, 0.55);
    background: rgba(54, 67, 129, 0.45);
    color: #E3E7FF;
    font-size: 9px;
    font-weight: 900;
}
.workflow-step b { font-size: 9px; font-weight: 800; }
.workflow-timeline > i {
    flex: 1;
    height: 1px;
    min-width: 8px;
    margin-top: -14px;
    background: linear-gradient(90deg, rgba(129, 105, 255, 0.18), rgba(86, 205, 255, 0.72), rgba(129, 105, 255, 0.18));
    background-size: 200% 100%;
    animation: timelineRun 2.4s linear infinite;
}
.workflow-step:nth-of-type(1) { animation-delay: 0s; }
.workflow-step:nth-of-type(3) { animation-delay: 1.1s; }
.workflow-step:nth-of-type(5) { animation-delay: 2.2s; }
.workflow-step:nth-of-type(7) { animation-delay: 3.3s; }
@keyframes workflowGlow {
    0%, 18%, 100% { color: #8999C6; }
    9% { color: #E9F9FF; }
}
@keyframes timelineRun {
    from { background-position: 100% 0; }
    to { background-position: -100% 0; }
}

/* Result-card icon badges */
div[class*="st-key-result-card-"] h4 {
    display: flex;
    align-items: center;
    gap: 8px;
    line-height: 1.3;
}
div[class*="st-key-result-card-0"] h4::before,
div[class*="st-key-result-card-1"] h4::before,
div[class*="st-key-result-card-2"] h4::before,
div[class*="st-key-result-card-3"] h4::before,
div[class*="st-key-result-card-4"] h4::before,
div[class*="st-key-result-card-5"] h4::before {
    content: "✦";
    display: inline-grid;
    place-items: center;
    width: 27px;
    height: 27px;
    flex: 0 0 27px;
    border-radius: 9px;
    border: 1px solid rgba(155, 142, 255, 0.4);
    background: linear-gradient(145deg, rgba(132, 93, 255, 0.25), rgba(35, 177, 255, 0.12));
    color: #97E9FF;
    font-size: 14px;
    box-shadow: 0 0 14px rgba(108, 93, 255, 0.12);
}
div[class*="st-key-result-card-1"] h4::before { content: "◷"; color: #7FEAFF; }
div[class*="st-key-result-card-2"] h4::before { content: "◎"; color: #FFB5E3; }
div[class*="st-key-result-card-3"] h4::before { content: "▤"; color: #72F1CE; }
div[class*="st-key-result-card-4"] h4::before { content: "✓"; color: #FFD47C; }
div[class*="st-key-result-card-5"] h4::before { content: "i"; color: #94BAFF; }

/* Premium team footer */
.site-footer {
    margin-top: 24px;
    padding: 22px 24px 17px;
    border: 1px solid rgba(104, 126, 197, 0.42);
    border-radius: 20px;
    background: linear-gradient(120deg, rgba(14, 24, 50, 0.96), rgba(27, 22, 63, 0.93), rgba(10, 31, 53, 0.96));
    box-shadow: 0 14px 35px rgba(0,0,0,0.17), inset 0 1px 0 rgba(255,255,255,0.06);
}
.site-footer-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 18px;
}
.footer-brand { color: #F5F5FF; font-size: 18px; font-weight: 900; letter-spacing: -0.4px; }
.footer-brand b { color: #7DE4FF; }
.footer-tagline { margin-top: 6px; color: #AAB8DE; font-size: 12px; }
.footer-maker {
    display: inline-flex; align-items: center; gap: 7px;
    padding: 8px 12px; margin-top: 9px;
    border: 1px solid rgba(147, 130, 255, 0.40);
    border-radius: 999px; color: #E5E2FF;
    background: rgba(107, 83, 255, 0.12); font-size: 11px; font-weight: 800;
}
.footer-links { display: flex; gap: 9px; flex-wrap: wrap; margin-top: 12px; }
.site-footer a {
    color: #B8EFFF !important;
    text-decoration: none !important;
    font-size: 11px;
    font-weight: 700;
}
.footer-link-pill {
    display: inline-flex; align-items: center;
    padding: 8px 10px; border-radius: 10px;
    border: 1px solid rgba(99, 127, 198, 0.40);
    background: rgba(21, 39, 76, 0.56);
}
.site-footer a:hover { color: white !important; text-shadow: 0 0 12px rgba(85, 205, 255, 0.6); }
.footer-team {
    margin-top: 17px; padding-top: 14px;
    border-top: 1px solid rgba(112, 132, 197, 0.26);
    display: flex; justify-content: space-between; align-items: center;
    flex-wrap: wrap; gap: 9px; color: #AAB7D9; font-size: 11px;
}
.footer-team strong { color: #E5E8FF; }
.footer-legal { color: #8698C3; font-size: 10px; line-height: 1.6; margin-top: 12px; }
@media (max-width: 540px) {
    .site-footer { padding: 18px 15px 15px; }
    .workflow-step { font-size: 8px; }
    .workflow-timeline { gap: 4px; }
    .workflow-step span { width: 23px; height: 23px; }
}
@media (prefers-reduced-motion: reduce) {
    .workflow-step, .workflow-timeline > i { animation: none; }
}



/* ===== MAJOR REDESIGN: HOME + COMMAND CENTER ===== */
.page-heading { margin: 0.2rem 0 1.2rem; }
.page-heading .eyebrow { margin-bottom: 10px; }
.page-heading h1 {
    margin: 8px 0 6px;
    font-size: clamp(28px, 4vw, 42px);
    letter-spacing: -1px;
    color: #F4F6FF;
    text-shadow: 0 0 24px rgba(113, 104, 255, 0.18);
}
.page-heading p { color: #AEBDE5 !important; max-width: 780px; }
.home-actions { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin: 4px 0 26px; }
.home-feature-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 14px;
    margin: 17px 0 26px;
}
.home-feature-card {
    position: relative;
    min-height: 185px;
    padding: 21px 19px;
    overflow: hidden;
    border: 1px solid rgba(102, 130, 204, 0.53);
    border-radius: 19px;
    background: linear-gradient(145deg, rgba(24, 35, 72, 0.95), rgba(10, 24, 48, 0.96));
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.06), 0 13px 28px rgba(0,0,0,0.14);
    transition: transform .28s ease, border-color .28s ease, box-shadow .28s ease;
}
.home-feature-card::after {
    content: "";
    position: absolute;
    right: -35px;
    bottom: -56px;
    width: 130px;
    height: 130px;
    border: 1px solid rgba(111, 132, 255, 0.23);
    border-radius: 50%;
    box-shadow: 0 0 0 14px rgba(115, 95, 255, 0.035), 0 0 0 30px rgba(115, 95, 255, 0.025);
}
.home-feature-card:hover {
    transform: translateY(-5px);
    border-color: rgba(130, 151, 255, 0.85);
    box-shadow: 0 18px 38px rgba(67, 75, 194, 0.20);
}
.feature-icon {
    width: 45px;
    height: 45px;
    display: grid;
    place-items: center;
    border-radius: 14px;
    margin-bottom: 16px;
    font-size: 22px;
    border: 1px solid rgba(171, 166, 255, 0.45);
    background: linear-gradient(135deg, rgba(127, 86, 255, 0.28), rgba(36, 173, 255, 0.16));
    box-shadow: 0 0 22px rgba(104, 89, 255, 0.14);
}
.home-feature-card h3 { font-size: 16px; margin: 0 0 7px; color: #F3F4FF; }
.home-feature-card p { font-size: 12px; line-height: 1.65; color: #AEBBE0 !important; margin: 0; }
.home-section-title { margin: 25px 0 4px; font-size: 22px; font-weight: 800; color: #F3F5FF; }
.home-section-subtitle { margin: 0 0 15px; color: #A7B5DC; font-size: 13px; }
.workflow-home {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 11px;
    margin: 15px 0 28px;
}
.workflow-home-step {
    padding: 15px 14px;
    background: rgba(13, 24, 49, 0.74);
    border: 1px solid rgba(96, 120, 191, 0.38);
    border-radius: 15px;
}
.workflow-home-step span { display: block; color: #7EE7FF; font-size: 10px; font-weight: 900; letter-spacing: 1.5px; margin-bottom: 8px; }
.workflow-home-step b { display: block; color: #EFF0FF; font-size: 13px; margin-bottom: 5px; }
.workflow-home-step p { color: #A5B4DA !important; font-size: 11px; line-height: 1.55; margin: 0; }
.workspace-card {
    padding: 20px;
    border: 1px solid rgba(96, 123, 194, 0.52);
    border-radius: 18px;
    background: linear-gradient(145deg, rgba(20, 32, 66, 0.8), rgba(10, 22, 44, 0.78));
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
}
.workspace-kicker { color: #7FE6FF; font-size: 10px; font-weight: 900; letter-spacing: 1.6px; text-transform: uppercase; margin-bottom: 8px; }
.workspace-title { color: #F1F3FF; font-size: 19px; font-weight: 800; margin-bottom: 7px; }
.workspace-copy { color: #AAB9DF; font-size: 12px; line-height: 1.65; }
.workspace-list { display: grid; gap: 10px; margin-top: 16px; }
.workspace-list div { display: flex; gap: 10px; align-items: flex-start; color: #D8E0FF; font-size: 12px; line-height: 1.55; }
.workspace-list span { color: #7FE6FF; font-size: 16px; }
.page-chip {
    display: inline-flex; align-items: center; gap: 7px;
    padding: 7px 10px; margin-bottom: 10px;
    border-radius: 999px; border: 1px solid rgba(117, 138, 226, 0.38);
    background: rgba(40, 53, 108, 0.35); color: #C9D5FF;
    font-size: 10px; font-weight: 800; letter-spacing: 1px;
}
.page-chip i { width: 6px; height: 6px; background: #5DE4C1; border-radius: 50%; box-shadow: 0 0 9px rgba(93,228,193,.7); }
.sidebar-cta {
    margin-top: 13px; padding: 12px 13px;
    border-radius: 13px; border: 1px solid rgba(114, 132, 222, 0.32);
    background: linear-gradient(110deg, rgba(107, 75, 255, 0.13), rgba(29, 144, 221, 0.08));
    color: #AEBDE5; font-size: 11px; line-height: 1.5;
}
@media (max-width: 800px) {
    .home-feature-grid { grid-template-columns: 1fr; }
    .home-feature-card { min-height: auto; }
    .workflow-home { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 480px) {
    .workflow-home { grid-template-columns: 1fr 1fr; gap: 8px; }
    .workflow-home-step { padding: 12px 10px; }
    .workspace-card { padding: 15px; }
}



/* ===== STUDENT COMMAND DASHBOARD ===== */
.deadline-row {
    display: flex;
    align-items: center;
    gap: 11px;
    margin: 9px 0;
    padding: 11px 12px;
    border: 1px solid rgba(95, 119, 190, 0.42);
    border-radius: 14px;
    background: linear-gradient(110deg, rgba(19, 31, 63, 0.90), rgba(11, 24, 47, 0.92));
}
.deadline-date {
    flex: 0 0 43px;
    height: 45px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    color: #FFFFFF;
    font-size: 17px;
    font-weight: 900;
    background: linear-gradient(140deg, rgba(124, 84, 255, .42), rgba(24, 145, 226, .30));
    border: 1px solid rgba(135, 142, 255, .4);
}
.deadline-date small { color: #B9CBFF; font-size: 9px; letter-spacing: 1px; }
.deadline-detail { flex: 1; min-width: 0; }
.deadline-detail b { display: block; color: #EAF0FF; font-size: 12px; line-height: 1.5; }
.deadline-detail small { display: block; color: #9BAED8; font-size: 10px; line-height: 1.45; margin-top: 3px; }
.deadline-pill {
    flex: 0 0 auto;
    padding: 6px 8px;
    border-radius: 999px;
    border: 1px solid rgba(124, 141, 206, .42);
    background: rgba(72, 93, 163, .16);
    color: #C5D2FF;
    font-size: 9px;
    font-weight: 900;
    letter-spacing: .45px;
}
.deadline-pill.soon { color: #FFE4A1; border-color: rgba(255, 198, 89, .38); background: rgba(255, 177, 54, .08); }
.deadline-pill.today { color: #FFB7C7; border-color: rgba(255, 112, 153, .46); background: rgba(255, 78, 132, .10); }
.calendar-title { margin: 12px 0; color: #E4E9FF; font-size: 21px; font-weight: 900; letter-spacing: -.4px; }
.calendar-weekday {
    text-align: center; padding: 8px 1px;
    color: #91A6D8; font-size: 9px; font-weight: 900; letter-spacing: 1px;
}
.calendar-cell {
    min-height: 58px;
    margin: 2px 0;
    padding: 7px 3px 5px;
    text-align: center;
    border-radius: 9px;
    border: 1px solid rgba(77, 97, 153, .30);
    background: rgba(16, 27, 52, .63);
    color: #DCE5FF;
}
.calendar-cell strong { display: block; font-size: 13px; }
.calendar-cell span { display: inline-block; margin-top: 6px; color: #92E9FF; font-size: 8px; line-height: 1.2; }
.calendar-cell.has-events {
    border-color: rgba(104, 127, 255, .74);
    background: linear-gradient(145deg, rgba(103, 78, 227, .25), rgba(24, 126, 194, .17));
    box-shadow: inset 0 0 12px rgba(103, 98, 255, .09);
}
.calendar-cell.empty { opacity: .18; background: transparent; border-color: transparent; }
@media (max-width: 620px) {
    .deadline-row { gap: 7px; padding: 9px 8px; }
    .deadline-date { flex-basis: 37px; height: 41px; }
    .deadline-pill { padding: 5px 6px; font-size: 8px; }
    .calendar-cell { min-height: 48px; padding: 6px 1px 3px; }
    .calendar-cell span { font-size: 7px; }
}

</style>  

""", unsafe_allow_html=True)


# ---------- OCR ----------
@st.cache_resource
def get_reader():
    return easyocr.Reader(["en"], gpu=False)


# ---------- AI ----------
def generate_notice_response(client, prompt):
    """Try the current stable Gemini model first, then supported Gemma fallbacks."""
    model_order = [
        "gemini-3.8-flash",
        "gemma-4-26b-a4b-it",
        "gemma-4-31b-it",
    ]
    failures = []

    for model_name in model_order:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            response_text = getattr(response, "text", None)
            if response_text and response_text.strip():
                st.session_state["last_ai_model"] = model_name
                return response_text
            failures.append(f"{model_name}: empty response")
        except Exception as exc:
            # Try the next provider model instead of failing the whole feature.
            failures.append(f"{model_name}: {str(exc)[:220]}")

    failure_summary = " | ".join(failures)
    raise RuntimeError(
        "All NoticeBuddy AI models failed. Check the Google AI Studio API key, "
        "model availability/quota, or retry after a short wait. Attempts: "
        + failure_summary
    )


def explain_notice(text, language):
    client = genai.Client(
        api_key=st.secrets["GEMMA_API_KEY"]
    )

    prompt = f"""
You are NoticeBuddy AI, a careful notice explanation assistant.

Explain this notice in {language}, using simple student-friendly language.
Use only information present in the notice. Never invent facts,
dates, eligibility criteria, fees, links or required documents.
Do not cite ChatGPT, OpenAI, or any AI assistant as a source.
Do not invent source names, references, citations, or a "Source" label.
Treat the user-provided notice as the only source; if asked to name the
source, say "Source: User-provided notice".
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
    response_text = generate_notice_response(client, prompt)
    return response_text or "No explanation was returned."


def answer_notice_question(notice_text, explanation, question, language):
    """Answer a follow-up using the specific notice as the source of truth."""
    client = genai.Client(api_key=st.secrets["GEMMA_API_KEY"])
    prompt = f"""
You are NoticeBuddy AI answering a student's follow-up about a notice.
Reply in {language}, using simple student-friendly language.
Use the original notice as the source of truth. Do not invent deadlines,
eligibility, costs, documents, links, or conditions. If the answer is not
stated in the notice, clearly say it is not mentioned. Do not cite ChatGPT,
OpenAI, or any AI assistant as a source. Encourage official verification
for important decisions.

ORIGINAL NOTICE:
{notice_text}

EXISTING EXPLANATION (context only; defer to the original notice):
{explanation}

STUDENT QUESTION:
{question}
"""
    response_text = generate_notice_response(client, prompt)
    return response_text or "No answer was returned."


def extract_notice_dates(notice_text):
    """Extract explicit full dates; avoids guessing from month/year alone."""
    month_tokens = (
        "January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|"
        "July|Jul|August|Aug|September|Sep|Sept|October|Oct|November|Nov|"
        "December|Dec"
    )
    month_number = {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
        "jul": 7, "aug": 8, "sep": 9, "sept": 9, "oct": 10,
        "nov": 11, "dec": 12
    }
    patterns = [
        (re.compile(r"\b(20\d{2})[-/.](\d{1,2})[-/.](\d{1,2})\b"),
         lambda m: (int(m.group(1)), int(m.group(2)), int(m.group(3)))),
        (re.compile(r"\b(\d{1,2})[/-](\d{1,2})[/-](20\d{2})\b"),
         lambda m: (int(m.group(3)), int(m.group(2)), int(m.group(1)))),
        (re.compile(rf"\b(\d{{1,2}})(?:st|nd|rd|th)?\s+({month_tokens})\.?,?\s+(20\d{{2}})\b", re.IGNORECASE),
         lambda m: (int(m.group(3)), month_number[m.group(2).lower()[:4] if m.group(2).lower()[:4] == "sept" else m.group(2).lower()[:3]], int(m.group(1)))),
        (re.compile(rf"\b({month_tokens})\.?\s+(\d{{1,2}})(?:st|nd|rd|th)?[,]?\s+(20\d{{2}})\b", re.IGNORECASE),
         lambda m: (int(m.group(3)), month_number[m.group(1).lower()[:4] if m.group(1).lower()[:4] == "sept" else m.group(1).lower()[:3]], int(m.group(2)))),
    ]
    found = {}
    for line in notice_text.splitlines():
        line = line.strip()
        if not line:
            continue
        matches = []
        for pattern, converter in patterns:
            for match in pattern.finditer(line):
                try:
                    year, month, day_num = converter(match)
                    parsed = date(year, month, day_num)
                    matches.append((match.start(), match.end(), parsed))
                except (ValueError, KeyError, IndexError):
                    continue
        for start, end, parsed in sorted(matches, key=lambda item: item[0]):
            iso = parsed.isoformat()
            context = line
            if len(context) > 150:
                context = context[max(0, start - 52):min(len(line), end + 65)].strip()
            if iso not in found:
                found[iso] = {
                    "date": iso,
                    "label": context[:150] or "Date found in notice",
                    "kind": "Notice date"
                }
    return sorted(found.values(), key=lambda item: item["date"])


def add_analysis_record(notice_text, explanation, language):
    """Keep personal notice history only in this browser session."""
    first_line = next((line.strip(" #\t") for line in notice_text.splitlines() if line.strip()), "")
    title = first_line[:88] + ("…" if len(first_line) > 88 else "")
    if not title:
        title = "Notice analysis"
    record = {
        "id": uuid.uuid4().hex[:12],
        "title": title,
        "source_text": notice_text,
        "explanation": explanation,
        "language": language,
        "analyzed_at": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "dates": extract_notice_dates(notice_text),
        "saved": False
    }
    st.session_state.setdefault("notice_history", []).insert(0, record)
    st.session_state["latest_notice_id"] = record["id"]
    return record


def toggle_saved_notice(notice_id):
    for item in st.session_state.get("notice_history", []):
        if item.get("id") == notice_id:
            item["saved"] = not item.get("saved", False)
            break


def delete_notice_record(notice_id):
    st.session_state["notice_history"] = [
        item for item in st.session_state.get("notice_history", [])
        if item.get("id") != notice_id
    ]
    st.session_state.setdefault("notice_chats", {}).pop(notice_id, None)
    if st.session_state.get("latest_notice_id") == notice_id:
        remaining = st.session_state["notice_history"]
        st.session_state["latest_notice_id"] = remaining[0]["id"] if remaining else None


def get_all_date_events():
    events = []
    for record in st.session_state.get("notice_history", []):
        for index, item in enumerate(record.get("dates", [])):
            events.append({
                "id": f'{record["id"]}-date-{index}',
                "date": item["date"],
                "label": item.get("label", "Date found in notice"),
                "source": record.get("title", "Saved notice"),
                "kind": "From notice"
            })
    for item in st.session_state.get("manual_deadlines", []):
        events.append({
            "id": item["id"],
            "date": item["date"],
            "label": item["label"],
            "source": item.get("note", "Personal reminder"),
            "kind": "Personal reminder"
        })
    return sorted(events, key=lambda item: (item["date"], item["label"]))


def render_read_aloud(text_to_read, language):
    """Use the browser's built-in speech engine; no extra API or library needed."""
    payload = json.dumps(text_to_read, ensure_ascii=False).replace("</", "<\\/")
    speech_language = "hi-IN" if language == "Hindi" else "en-IN"
    components.html(f"""
    <div style="font-family:Arial,sans-serif;display:flex;gap:9px;align-items:center;flex-wrap:wrap">
      <button onclick="speakText()" style="cursor:pointer;border:1px solid #766BFF;border-radius:10px;padding:9px 13px;background:linear-gradient(100deg,#8054FF,#168DEB);color:white;font-weight:700">🔊 Listen</button>
      <button onclick="stopText()" style="cursor:pointer;border:1px solid #455A8A;border-radius:10px;padding:9px 13px;background:#101B37;color:#C9D8FF;font-weight:700">■ Stop</button>
      <span id="speechStatus" style="font-size:12px;color:#AAB9E7">Uses your browser's speech voice</span>
    </div>
    <script>
      const noticeBuddySpeechText = {payload};
      const noticeBuddySpeechLang = "{speech_language}";
      function speakText() {{
        if (!("speechSynthesis" in window)) {{
          document.getElementById("speechStatus").textContent = "Speech is not supported by this browser.";
          return;
        }}
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(noticeBuddySpeechText);
        utterance.lang = noticeBuddySpeechLang;
        utterance.rate = 0.94;
        utterance.onstart = () => document.getElementById("speechStatus").textContent = "Reading aloud…";
        utterance.onend = () => document.getElementById("speechStatus").textContent = "Finished";
        window.speechSynthesis.speak(utterance);
      }}
      function stopText() {{
        if ("speechSynthesis" in window) window.speechSynthesis.cancel();
        document.getElementById("speechStatus").textContent = "Stopped";
      }}
    </script>
    """, height=56)


def render_saved_analysis(record):
    st.markdown('<div class="home-section-title">🤖 Your notice explained</div>', unsafe_allow_html=True)
    action_col, voice_col = st.columns([1, 1], gap="small")
    with action_col:
        st.button(
            "★ Unsave notice" if record.get("saved") else "☆ Save notice",
            key=f"toggle-saved-{record['id']}",
            on_click=toggle_saved_notice,
            args=(record["id"],),
            use_container_width=True
        )
    with voice_col:
        render_read_aloud(record.get("explanation", ""), record.get("language", "English"))

    render_explanation_cards(record.get("explanation", ""))
    st.download_button(
        "⬇️ Download explanation",
        data=record.get("explanation", ""),
        file_name="noticebuddy_explanation.txt",
        mime="text/plain",
        key=f"download-{record['id']}"
    )

    if record.get("dates"):
        with st.expander(f"📅 Dates detected in this notice ({len(record['dates'])})"):
            for item in record["dates"]:
                st.markdown(f"**{item['date']}** — {item['label']}")

    with st.expander("💬 Chat with this notice", expanded=False):
        chats = st.session_state.setdefault("notice_chats", {}).setdefault(record["id"], [])
        with st.form(key=f"chat-form-{record['id']}"):
            question = st.text_input(
                "Ask a question about this notice",
                placeholder="e.g., Which documents are required?",
                key=f"chat-question-{record['id']}"
            )
            submitted = st.form_submit_button("Ask NoticeBuddy ✨", use_container_width=True)
        if submitted:
            if not question.strip():
                st.warning("Write a question first.")
            else:
                try:
                    with st.spinner("Finding the answer in your notice..."):
                        answer = answer_notice_question(
                            record.get("source_text", ""),
                            record.get("explanation", ""),
                            question.strip(),
                            record.get("language", "English")
                        )
                    chats.append({"role": "user", "text": question.strip()})
                    chats.append({"role": "assistant", "text": answer})
                except Exception as exc:
                    st.error("NoticeBuddy could not answer after trying its available AI models.")
                    st.info("Retry in a moment. If the problem continues, check GEMMA_API_KEY in Streamlit Secrets and the Google AI Studio quota.")
                    st.caption(f"Technical details: {exc}")
        for message in chats:
            if message.get("role") == "user":
                st.chat_message("user").write(message.get("text", ""))
            else:
                st.chat_message("assistant").write(message.get("text", ""))


def render_explanation_cards(explanation):
    """Display each AI response section as a separate, colorful card."""
    parts = re.split(r"(?m)^##\s+", explanation.strip())
    sections = []

    if len(parts) > 1:
        if parts[0].strip():
            sections.append(("Additional Details", parts[0].strip()))
        for part in parts[1:]:
            lines = part.splitlines()
            if not lines:
                continue
            title = lines[0].strip().lstrip("#").strip()
            body = "\n".join(lines[1:]).strip()
            if title or body:
                sections.append((title or "Notice Details", body))
    else:
        sections.append(("Notice Summary", explanation.strip()))

    for index, (title, body) in enumerate(sections):
        with st.container(key=f"result-card-{index}"):
            st.markdown(f"#### {title}")
            if body:
                st.markdown(body)


AI_ACTIVITY_HTML = """
<div class="ai-activity-card">
  <div class="ai-activity-header">
    <span class="activity-pulse"></span>
    <strong>NoticeBuddy AI is working</strong>
    <span class="activity-live">LIVE SCAN</span>
  </div>
  <div class="scanner-stage" aria-hidden="true">
    <div class="scanner-doc">
      <span class="doc-line long"></span>
      <span class="doc-line medium"></span>
      <span class="doc-line short"></span>
      <span class="doc-line long"></span>
      <span class="doc-line medium"></span>
      <span class="doc-line short"></span>
    </div>
    <div class="scanner-beam"></div>
    <div class="scanner-corner top-left"></div>
    <div class="scanner-corner bottom-right"></div>
  </div>
  <div class="ai-waveform" aria-label="AI analysis animation">
    <span></span><span></span><span></span><span></span><span></span>
    <span></span><span></span><span></span><span></span><span></span>
    <span></span><span></span><span></span><span></span><span></span>
    <span></span><span></span><span></span><span></span><span></span>
    <span></span><span></span><span></span><span></span>
  </div>
  <div class="workflow-timeline" aria-label="Notice analysis workflow">
    <div class="workflow-step"><span>01</span><b>Read</b></div>
    <i></i>
    <div class="workflow-step"><span>02</span><b>Extract</b></div>
    <i></i>
    <div class="workflow-step"><span>03</span><b>Analyze</b></div>
    <i></i>
    <div class="workflow-step"><span>04</span><b>Summarize</b></div>
  </div>
  <div class="ai-activity-caption">Reading key details · organizing dates · preparing your summary</div>
</div>
"""


# All history is scoped to the user's active Streamlit session.
st.session_state.setdefault("notice_history", [])
st.session_state.setdefault("manual_deadlines", [])
st.session_state.setdefault("notice_chats", {})
st.session_state.setdefault("latest_notice_id", None)


# ---------- APP NAVIGATION ----------
def go_to_analyzer():
    st.session_state["main_navigation"] = "✨ Analyzer"


with st.sidebar:
    st.markdown("## 📄 NoticeBuddy AI")
    st.caption("Your personal notice assistant")
    st.markdown("---")
    page = st.radio(
        "NAVIGATION",
        ["🏠 Home", "📊 Dashboard", "✨ Analyzer", "📘 How it works", "ℹ️ About"],
        key="main_navigation"
    )
    st.markdown(
        '<div class="sidebar-cta"><b style="color:#EEF1FF">Understand every notice.</b><br>'
        'Turn complicated information into simple steps, dates and checklists.</div>',
        unsafe_allow_html=True
    )
    st.markdown("---")
    st.caption("Built by Kushagra Agarwal")


# ---------- PREMIUM TOP NAVBAR ----------
st.markdown("""
<div class="top-nav">
  <div class="top-nav-brand">
    <span class="top-nav-logo">NB</span>
    <span class="top-nav-wordmark">NoticeBuddy <b>AI</b><small>SMART NOTICE ASSISTANT</small></span>
  </div>
  <div class="top-nav-right">
    <span class="nav-status"><i></i> AI POWERED</span>
    <span class="nav-journey">READ <b>•</b> UNDERSTAND <b>•</b> ACT</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ---------- HOME ----------
if page == "🏠 Home":
    robot_image_url = "https://raw.githubusercontent.com/krishagarwal369-droid/NoticeBuddy-AI/main/Neon%20AI%20Robot%20Greeting.png"
    st.markdown(f"""
    <div class="hero">
      <div class="hero-content">
        <div class="hero-particles" aria-hidden="true">
          <span></span><span></span><span></span><span></span>
          <span></span><span></span><span></span><span></span>
        </div>
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

    home_left, home_right = st.columns([1.0, 1.0], gap="large")
    with home_left:
        st.markdown(
            '<div class="page-chip"><i></i> NOTICE CLARITY, REIMAGINED</div>',
            unsafe_allow_html=True
        )
        st.button(
            "✨ Start Analyzing a Notice",
            key="home_start_analyzer",
            use_container_width=True,
            on_click=go_to_analyzer
        )
    with home_right:
        st.markdown(
            '<div style="padding:12px 2px;color:#9FB0DB;font-size:12px;line-height:1.7">'
            'Paste text or add a notice image/PDF. Get a simple summary, key dates, eligibility and next steps—'
            'then verify important details against the original notice.</div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="home-section-title">One notice. Clear next steps.</div>'
                '<div class="home-section-subtitle">Designed to make dense official information easier for students to understand.</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="home-feature-grid">
      <article class="home-feature-card">
        <div class="feature-icon">📄</div>
        <h3>Read the notice</h3>
        <p>Paste text, upload an image for OCR, or extract selectable text from a PDF.</p>
      </article>
      <article class="home-feature-card">
        <div class="feature-icon">🧠</div>
        <h3>Understand the details</h3>
        <p>Get a student-friendly explanation in English or Hindi, grounded in the provided notice.</p>
      </article>
      <article class="home-feature-card">
        <div class="feature-icon">✅</div>
        <h3>Know what to do next</h3>
        <p>Review the dates, eligibility and document requirements the notice actually mentions.</p>
      </article>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="home-section-title">How NoticeBuddy works</div>'
                '<div class="home-section-subtitle">Four simple steps from a complex notice to a clearer plan.</div>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="workflow-home">
      <div class="workflow-home-step"><span>STEP 01</span><b>Upload</b><p>Paste text or choose an image/PDF.</p></div>
      <div class="workflow-home-step"><span>STEP 02</span><b>Extract</b><p>Read text from images or selectable PDFs.</p></div>
      <div class="workflow-home-step"><span>STEP 03</span><b>Analyze</b><p>AI organizes the key information.</p></div>
      <div class="workflow-home-step"><span>STEP 04</span><b>Take action</b><p>Review the summary and verify official details.</p></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="workspace-card">
      <div class="workspace-kicker">Built for clarity</div>
      <div class="workspace-title">Your notice stays the source of truth.</div>
      <div class="workspace-copy">NoticeBuddy helps explain the text; it does not replace an official notice or guarantee eligibility. Always confirm deadlines, conditions and submission rules with the issuing organization.</div>
    </div>
    """, unsafe_allow_html=True)


# ---------- STUDENT COMMAND DASHBOARD ----------
elif page == "📊 Dashboard":
    st.markdown("""
    <div class="page-heading">
      <div class="eyebrow">STUDENT COMMAND DASHBOARD</div>
      <h1>Your notices. One place.</h1>
      <p>Review this session's analysis history, saved notices, important dates and personal deadline reminders.</p>
    </div>
    """, unsafe_allow_html=True)

    records = st.session_state.get("notice_history", [])
    saved_records = [item for item in records if item.get("saved")]
    all_events = get_all_date_events()
    today = date.today()
    upcoming_events = []
    for event in all_events:
        try:
            event_date = date.fromisoformat(event["date"])
            if event_date >= today:
                upcoming_events.append((event_date, event))
        except (ValueError, TypeError):
            continue
    upcoming_events.sort(key=lambda pair: pair[0])

    metric_columns = st.columns(4)
    metric_data = [
        ("ANALYZED", str(len(records)), "📄"),
        ("SAVED", str(len(saved_records)), "★"),
        ("DATES FOUND", str(len(all_events)), "◷"),
        ("UPCOMING", str(len(upcoming_events)), "✦")
    ]
    for column, (label, value, icon) in zip(metric_columns, metric_data):
        with column:
            st.markdown(
                f'<div class="metric"><span class="metric-icon">{icon}</span>'
                f'<div class="metric-label">{label}</div>'
                f'<div class="metric-value">{value}</div></div>',
                unsafe_allow_html=True
            )

    overview_tab, saved_tab, calendar_tab, history_tab = st.tabs([
        "📌 Overview", "⭐ Saved notices", "📅 Calendar", "🗂️ History"
    ])

    with overview_tab:
        overview_left, overview_right = st.columns([1.05, 0.95], gap="large")
        with overview_left:
            st.markdown('<div class="home-section-title">Upcoming dates</div>', unsafe_allow_html=True)
            st.markdown('<div class="home-section-subtitle">Dates recognized in your notices plus reminders you add yourself.</div>', unsafe_allow_html=True)
            if not upcoming_events:
                st.info("No upcoming dates yet. Analyze a notice or add a reminder in the Calendar tab.")
            else:
                for event_date, event in upcoming_events[:6]:
                    remaining = (event_date - today).days
                    if remaining == 0:
                        countdown = "TODAY"
                        class_name = "today"
                    elif remaining == 1:
                        countdown = "1 DAY LEFT"
                        class_name = "soon"
                    else:
                        countdown = f"{remaining} DAYS LEFT"
                        class_name = "soon" if remaining <= 7 else "normal"
                    st.markdown(
                        f'<div class="deadline-row">'
                        f'<div class="deadline-date">{event_date.strftime("%d")}<small>{event_date.strftime("%b").upper()}</small></div>'
                        f'<div class="deadline-detail"><b>{html_escape(event["label"])}</b>'
                        f'<small>{html_escape(event["kind"])} · {html_escape(event["source"])}</small></div>'
                        f'<span class="deadline-pill {class_name}">{countdown}</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
        with overview_right:
            st.markdown("""
            <div class="workspace-card">
              <div class="workspace-kicker">Quick actions</div>
              <div class="workspace-title">Keep moving forward</div>
              <div class="workspace-list">
                <div><span>✦</span><span><b>Analyze a new notice</b><br>Extract the important information from a fresh notice.</span></div>
                <div><span>★</span><span><b>Save important notices</b><br>Bookmark them in the Saved notices tab.</span></div>
                <div><span>◷</span><span><b>Add a personal reminder</b><br>Track a date even when the notice wording is unclear.</span></div>
              </div>
            </div>
            """, unsafe_allow_html=True)
            st.button(
                "✨ Analyze a new notice",
                key="dashboard_open_analyzer",
                use_container_width=True,
                on_click=go_to_analyzer
            )
            if records:
                export_data = json.dumps(records, ensure_ascii=False, indent=2)
                st.download_button(
                    "⬇️ Export session history (JSON)",
                    data=export_data,
                    file_name="noticebuddy_session_history.json",
                    mime="application/json",
                    key="export_notice_history",
                    use_container_width=True
                )
        st.caption("Privacy note: history and saved notices are held only in this active app session. They are not stored in a permanent database and may be cleared when the session ends.")

    with saved_tab:
        st.markdown('<div class="home-section-title">Your saved notices</div>', unsafe_allow_html=True)
        if not saved_records:
            st.info("No saved notices yet. Analyze a notice, then choose ☆ Save notice to bookmark it here.")
        for record in saved_records:
            with st.expander(f"⭐ {record['title']}", expanded=False):
                st.caption(f"Analyzed {record['analyzed_at']} · {len(record.get('dates', []))} date(s) detected")
                st.markdown(record.get("explanation", "No explanation stored."))
                button_col, delete_col = st.columns(2)
                with button_col:
                    st.button(
                        "★ Unsave",
                        key=f"unsave-saved-{record['id']}",
                        on_click=toggle_saved_notice,
                        args=(record["id"],),
                        use_container_width=True
                    )
                with delete_col:
                    st.button(
                        "🗑️ Delete",
                        key=f"delete-saved-{record['id']}",
                        on_click=delete_notice_record,
                        args=(record["id"],),
                        use_container_width=True
                    )

    with calendar_tab:
        st.markdown('<div class="home-section-title">Deadline calendar</div>', unsafe_allow_html=True)
        st.markdown('<div class="home-section-subtitle">Full dates are detected from notice text. Add a manual reminder whenever you need one.</div>', unsafe_allow_html=True)
        with st.form("manual_deadline_form", clear_on_submit=True):
            reminder_title = st.text_input("Reminder title", placeholder="e.g., Submit scholarship documents")
            reminder_date = st.date_input("Reminder date", value=date.today() + timedelta(days=7))
            reminder_note = st.text_input("Optional note", placeholder="e.g., Bring the original documents")
            reminder_submitted = st.form_submit_button("＋ Add reminder", use_container_width=True)
        if reminder_submitted:
            if not reminder_title.strip():
                st.warning("Enter a title for the reminder.")
            else:
                st.session_state.setdefault("manual_deadlines", []).append({
                    "id": uuid.uuid4().hex[:12],
                    "date": reminder_date.isoformat(),
                    "label": reminder_title.strip(),
                    "note": reminder_note.strip() or "Personal reminder",
                    "kind": "Manual reminder"
                })
                st.success("Reminder added to this session's calendar.")

        chosen_date = st.date_input("Choose month to display", value=date.today(), key="calendar_month")
        year, month = chosen_date.year, chosen_date.month
        month_label = date(year, month, 1).strftime("%B %Y")
        st.markdown(f'<div class="calendar-title">{month_label}</div>', unsafe_allow_html=True)
        events = get_all_date_events()
        events_by_date = {}
        for event in events:
            events_by_date.setdefault(event["date"], []).append(event)

        weekday_columns = st.columns(7, gap="small")
        for column, weekday in zip(weekday_columns, ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]):
            with column:
                st.markdown(f'<div class="calendar-weekday">{weekday}</div>', unsafe_allow_html=True)
        for week in calendar_module.monthcalendar(year, month):
            week_columns = st.columns(7, gap="small")
            for column, day_number in zip(week_columns, week):
                with column:
                    if not day_number:
                        st.markdown('<div class="calendar-cell empty"></div>', unsafe_allow_html=True)
                    else:
                        iso_date = date(year, month, day_number).isoformat()
                        day_events = events_by_date.get(iso_date, [])
                        cell_class = "calendar-cell has-events" if day_events else "calendar-cell"
                        event_badge = f'<span>{len(day_events)} date(s)</span>' if day_events else '<span>&nbsp;</span>'
                        st.markdown(
                            f'<div class="{cell_class}"><strong>{day_number}</strong>{event_badge}</div>',
                            unsafe_allow_html=True
                        )

        month_events = [
            item for item in events
            if item["date"].startswith(f"{year:04d}-{month:02d}-")
        ]
        st.markdown('<div class="home-section-title">Dates in this month</div>', unsafe_allow_html=True)
        if not month_events:
            st.info("No dates in this month. Dates are only added when a full date is recognized in a notice or you add a reminder.")
        for event in month_events:
            date_value = date.fromisoformat(event["date"])
            delta = (date_value - today).days
            if delta < 0:
                countdown = f"{abs(delta)} day(s) ago"
            elif delta == 0:
                countdown = "Today"
            elif delta == 1:
                countdown = "Tomorrow"
            else:
                countdown = f"In {delta} days"
            st.markdown(
                f'<div class="deadline-row">'
                f'<div class="deadline-date">{date_value.strftime("%d")}<small>{date_value.strftime("%b").upper()}</small></div>'
                f'<div class="deadline-detail"><b>{html_escape(event["label"])}</b>'
                f'<small>{html_escape(event["kind"])} · {html_escape(event["source"])}</small></div>'
                f'<span class="deadline-pill normal">{countdown}</span></div>',
                unsafe_allow_html=True
            )
        st.caption("Calendar reminders are local to this active session. Check the original notice before acting on a detected date.")

    with history_tab:
        st.markdown('<div class="home-section-title">Recent analyses</div>', unsafe_allow_html=True)
        if not records:
            st.info("Your analyzed notices will appear here.")
        for record in records:
            with st.expander(record["title"], expanded=False):
                st.caption(f"Analyzed {record['analyzed_at']} · {'⭐ Saved' if record.get('saved') else 'Not saved'}")
                st.markdown(record.get("explanation", "No explanation stored."))
                action_col, delete_col = st.columns(2)
                with action_col:
                    st.button(
                        "★ Unsave" if record.get("saved") else "☆ Save",
                        key=f"toggle-history-{record['id']}",
                        on_click=toggle_saved_notice,
                        args=(record["id"],),
                        use_container_width=True
                    )
                with delete_col:
                    st.button(
                        "🗑️ Delete record",
                        key=f"delete-history-{record['id']}",
                        on_click=delete_notice_record,
                        args=(record["id"],),
                        use_container_width=True
                    )


# ---------- ANALYZER COMMAND CENTER ----------
elif page == "✨ Analyzer":
    st.markdown("""
    <div class="page-heading">
      <div class="eyebrow">NOTICEBUDDY COMMAND CENTER</div>
      <h1>Analyze your notice</h1>
      <p>Bring a notice in. Get a clearer, structured explanation out.</p>
    </div>
    <div class="page-chip"><i></i> READY FOR YOUR NOTICE</div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1.03, 0.97], gap="large")
    with left:
        st.markdown("""
        <div class="workspace-card">
          <div class="workspace-kicker">01 / Input</div>
          <div class="workspace-title">Add a notice</div>
          <div class="workspace-copy">Paste notice text, upload an image, or use a PDF with selectable text.</div>
        </div>
        """, unsafe_allow_html=True)
        language = st.selectbox(
            "Explanation language", ["English", "Hindi"], key="analysis_language"
        )
        notice = st.text_area(
            "Paste notice text",
            placeholder="Paste the official notice text here...",
            height=210,
            key="notice_text"
        )
        uploaded_file = st.file_uploader(
            "Or upload a notice image/PDF",
            type=["png", "jpg", "jpeg", "pdf"],
            key="notice_upload"
        )
        analyze = st.button(
            "✨ Extract & Explain",
            type="primary",
            use_container_width=True,
            key="analyze_notice"
        )

    with right:
        st.markdown("""
        <div class="workspace-card">
          <div class="workspace-kicker">02 / What you'll get</div>
          <div class="workspace-title">A clear action brief</div>
          <div class="workspace-copy">The AI response is organized into cards so the most useful details are easier to scan.</div>
          <div class="workspace-list">
            <div><span>✦</span><span><b>Simple summary</b><br>Understand the main purpose.</span></div>
            <div><span>◷</span><span><b>Important dates</b><br>Spot stated dates and deadlines.</span></div>
            <div><span>◎</span><span><b>Eligibility</b><br>Review criteria present in the notice.</span></div>
            <div><span>▤</span><span><b>Required documents</b><br>Check what the notice asks for.</span></div>
            <div><span>✓</span><span><b>Next steps</b><br>See suggested actions based on the text.</span></div>
          </div>
        </div>
        <div class="workspace-copy" style="margin-top:14px">🔒 Your API key should be stored only in Streamlit Secrets, never in the public repository.</div>
        """, unsafe_allow_html=True)

    if analyze:
        text = notice.strip()

        if uploaded_file:
            try:
                with st.spinner("Reading your notice..."):
                    if uploaded_file.name.lower().endswith(".pdf"):
                        pdf = fitz.open(
                            stream=uploaded_file.getvalue(),
                            filetype="pdf"
                        )
                        pdf_text = "\n".join(page.get_text() for page in pdf)
                        pdf.close()
                        text = (text + "\n" + pdf_text).strip()

                        if not pdf_text.strip():
                            st.warning(
                                "This PDF has no selectable text. Scanned PDFs need OCR; upload the page as an image for now."
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
            st.warning("Please paste notice text or upload an image/PDF with readable text.")
        else:
            with st.expander("View extracted notice text"):
                st.write(text)

            st.markdown('<div class="home-section-title">03 / AI analysis</div>', unsafe_allow_html=True)
            activity_slot = st.empty()
            try:
                with st.spinner("🧠 AI is analyzing your notice..."):
                    activity_slot.markdown(AI_ACTIVITY_HTML, unsafe_allow_html=True)
                    explanation = explain_notice(text, language)

            except Exception as e:
                activity_slot.empty()
                st.error("NoticeBuddy could not get an AI response after trying its available models.")
                st.info("Wait a few seconds and retry. If this keeps happening, check that GEMMA_API_KEY in Streamlit Secrets is a valid Google AI Studio API key and that its quota is available.")
                st.caption(f"Technical details: {e}")

            else:
                activity_slot.empty()
                record = add_analysis_record(text, explanation, language)
                st.success("Notice analyzed and added to this session's history. Use ☆ Save notice to bookmark it.")
                render_saved_analysis(record)

    else:
        latest_id = st.session_state.get("latest_notice_id")
        latest_record = next(
            (item for item in st.session_state.get("notice_history", []) if item.get("id") == latest_id),
            None
        )
        if latest_record:
            st.markdown('<div class="home-section-title">Your latest session analysis</div>', unsafe_allow_html=True)
            render_saved_analysis(latest_record)


# ---------- HOW IT WORKS ----------
elif page == "📘 How it works":
    st.markdown("""
    <div class="page-heading">
      <div class="eyebrow">A SIMPLE WORKFLOW</div>
      <h1>From notice to next steps</h1>
      <p>NoticeBuddy organizes information from the notice you provide. Use the original notice as the final authority.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="workflow-home">
      <div class="workflow-home-step"><span>01 / INPUT</span><b>Paste or upload</b><p>Add notice text, an image, or a selectable-text PDF.</p></div>
      <div class="workflow-home-step"><span>02 / EXTRACT</span><b>Read the text</b><p>Image OCR extracts readable text; PDFs use selectable text.</p></div>
      <div class="workflow-home-step"><span>03 / EXPLAIN</span><b>Use AI carefully</b><p>Gemma organizes the text into student-friendly sections.</p></div>
      <div class="workflow-home-step"><span>04 / VERIFY</span><b>Check official details</b><p>Confirm dates and requirements with the issuing organization.</p></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="workspace-card">
      <div class="workspace-kicker">Important limitation</div>
      <div class="workspace-title">Scanned PDFs need a readable image for OCR.</div>
      <div class="workspace-copy">The current version extracts selectable text from PDFs. If a PDF is just scanned pages, upload the page as an image for OCR.</div>
    </div>
    """, unsafe_allow_html=True)
    st.button(
        "✨ Open the Analyzer",
        key="how_to_analyzer",
        use_container_width=True,
        on_click=go_to_analyzer
    )


# ---------- ABOUT ----------
elif page == "ℹ️ About":
    st.markdown("""
    <div class="page-heading">
      <div class="eyebrow">THE PROJECT</div>
      <h1>NoticeBuddy AI</h1>
      <p>A student-focused assistant that turns dense notices into structured, easier-to-understand information.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="home-feature-grid">
      <article class="home-feature-card"><div class="feature-icon">🧠</div><h3>AI explanation</h3><p>Uses the Google GenAI SDK to request an explanation in English or Hindi.</p></article>
      <article class="home-feature-card"><div class="feature-icon">🔎</div><h3>Text extraction</h3><p>EasyOCR handles uploaded images; PyMuPDF extracts selectable PDF text.</p></article>
      <article class="home-feature-card"><div class="feature-icon">🎓</div><h3>Student-first design</h3><p>Highlights summaries, dates, eligibility, documents and next steps.</p></article>
    </div>
    <div class="workspace-card">
      <div class="workspace-kicker">Project team</div>
      <div class="workspace-title">Built by Kushagra Agarwal, Kartik Sharma and Kanishk Shakya</div>
      <div class="workspace-copy">Contact: krishagarwal369@gmail.com · +91 79063 87966 · 7060414455</div>
      <div class="workspace-list">
        <div><span>↗</span><span><a href="https://github.com/krishagarwal369-droid" target="_blank" rel="noopener noreferrer">Kushagra / GitHub</a></span></div>
        <div><span>↗</span><span><a href="https://github.com/kartik45cloud" target="_blank" rel="noopener noreferrer">Kartik / GitHub</a></span></div>
        <div><span>↗</span><span><a href="https://github.com/Kanishk095" target="_blank" rel="noopener noreferrer">Kanishk / GitHub</a></span></div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.button(
        "✨ Start analyzing",
        key="about_to_analyzer",
        use_container_width=True,
        on_click=go_to_analyzer
    )


st.markdown("""
<footer class="site-footer">
  <div class="site-footer-top">
    <div>
      <div class="footer-brand">NoticeBuddy <b>AI</b></div>
      <div class="footer-tagline">Read clearly. Understand confidently. Take action.</div>
      <div class="footer-maker">✦ Built by Kushagra Agarwal</div>
    </div>
    <div>
      <div class="footer-tagline"><strong>TEAM & CONTACT</strong></div>
      <div class="footer-links">
        <a class="footer-link-pill" href="mailto:krishagarwal369@gmail.com">✉ Team email</a>
        <a class="footer-link-pill" href="tel:+917906387966">☎ +91 79063 87966</a>
        <a class="footer-link-pill" href="tel:+917060414455">☎ 7060414455</a>
      </div>
    </div>
  </div>
  <div class="footer-team">
    <span><strong>Team</strong> · Kushagra Agarwal · Kartik Sharma · Kanishk Shakya</span>
    <span>
      <a href="https://github.com/krishagarwal369-droid" target="_blank" rel="noopener noreferrer">GitHub</a>
      &nbsp;·&nbsp;
      <a href="https://github.com/kartik45cloud" target="_blank" rel="noopener noreferrer">Kartik</a>
      &nbsp;·&nbsp;
      <a href="https://github.com/Kanishk095" target="_blank" rel="noopener noreferrer">Kanishk</a>
    </span>
  </div>
  <div class="footer-legal">NoticeBuddy AI supports understanding, not official decision-making. Always confirm deadlines and requirements against the original official notice.</div>
</footer>
""", unsafe_allow_html=True)
