import fitz
import streamlit as st
from PIL import Image
from google import genai
from google.genai import types
import easyocr
import numpy as np
import re
import json
import csv
from io import StringIO
from html import escape as html_escape
import time
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Orbitron:wght@500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

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



/* ===== NEON NEXUS UI POLISH — visual-only layer ===== */
:root {
    --nb-violet: #8B5CFF;
    --nb-blue: #4D8DFF;
    --nb-cyan: #5CEBFF;
    --nb-mint: #76FFD3;
    --nb-glass: rgba(17, 27, 57, 0.74);
    --nb-border: rgba(131, 151, 255, 0.25);
}

/* Soft ambient glows; all effects stay behind the app content. */
.stApp {
    background-image:
        radial-gradient(ellipse at 12% 7%, rgba(84, 110, 255, 0.17), transparent 29%),
        radial-gradient(ellipse at 91% 23%, rgba(157, 76, 255, 0.20), transparent 31%),
        radial-gradient(ellipse at 55% 92%, rgba(0, 218, 255, 0.09), transparent 35%),
        linear-gradient(rgba(102, 122, 255, 0.105) 1px, transparent 1px),
        linear-gradient(90deg, rgba(102, 122, 255, 0.105) 1px, transparent 1px),
        linear-gradient(135deg, #070B19 0%, #10162F 48%, #0C1832 100%) !important;
    background-size: auto, auto, auto, 42px 42px, 42px 42px, 100% 100%;
    background-attachment: fixed;
}

/* Sharper, premium typography and a little more breathing room. */
.block-container {
    max-width: 1260px;
    padding-top: 1.6rem;
    padding-bottom: 3.5rem;
}
h1, h2, h3 {
    letter-spacing: -0.035em;
}
.eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    text-shadow: 0 0 18px rgba(139, 92, 255, .32);
}
.eyebrow::before {
    content: "";
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--nb-mint);
    box-shadow: 0 0 12px rgba(118, 255, 211, .8);
}

/* Hero becomes a luminous glass cockpit. */
.hero {
    border: 1px solid rgba(136, 133, 255, .48);
    background:
        radial-gradient(ellipse at 78% 12%, rgba(128, 78, 255, .27), transparent 37%),
        radial-gradient(ellipse at 8% 90%, rgba(39, 189, 255, .15), transparent 43%),
        linear-gradient(118deg, rgba(30, 26, 74, .96), rgba(14, 54, 91, .96) 58%, rgba(17, 23, 54, .97));
    box-shadow:
        0 25px 70px rgba(0, 0, 0, .28),
        0 0 0 1px rgba(92, 235, 255, .05) inset,
        0 0 42px rgba(103, 80, 255, .13);
}
.hero::before {
    content: "";
    pointer-events: none;
    position: absolute;
    inset: 0;
    border-radius: inherit;
    padding: 1px;
    background: linear-gradient(115deg, rgba(92, 235, 255, .68), transparent 28%, rgba(139, 92, 255, .55) 62%, transparent 82%, rgba(118, 255, 211, .45));
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    opacity: .72;
    z-index: -1;
}
.hero-robot {
    filter: drop-shadow(0 0 24px rgba(92, 235, 255, .18));
    transition: transform .55s cubic-bezier(.2,.8,.2,1), filter .55s ease;
}
.hero-robot:hover {
    transform: translateY(-7px) scale(1.025);
    filter: drop-shadow(0 0 35px rgba(92, 235, 255, .32));
}

/* Main content panels: glossy edge, floating hover, cleaner spacing. */
.workspace-card,
.home-feature-card,
.workflow-home-step,
.panel,
.metric {
    position: relative;
    isolation: isolate;
    background:
        linear-gradient(145deg, rgba(24, 35, 72, .91), rgba(10, 21, 43, .90)) !important;
    border: 1px solid var(--nb-border) !important;
    box-shadow:
        0 14px 32px rgba(0, 0, 0, .15),
        inset 0 1px 0 rgba(255, 255, 255, .045);
    transition:
        transform .28s cubic-bezier(.2,.8,.2,1),
        border-color .28s ease,
        box-shadow .28s ease,
        background .28s ease;
}
.workspace-card::after,
.home-feature-card::after,
.workflow-home-step::after,
.panel::after,
.metric::after {
    content: "";
    position: absolute;
    pointer-events: none;
    inset: 0;
    border-radius: inherit;
    background: linear-gradient(118deg, rgba(92, 235, 255, .075), transparent 33%, rgba(139, 92, 255, .065) 78%, transparent);
    opacity: .78;
    z-index: -1;
}
.workspace-card:hover,
.home-feature-card:hover,
.workflow-home-step:hover,
.panel:hover,
.metric:hover {
    transform: translateY(-4px);
    border-color: rgba(92, 235, 255, .48) !important;
    box-shadow:
        0 20px 42px rgba(0, 0, 0, .25),
        0 0 24px rgba(93, 116, 255, .12),
        inset 0 1px 0 rgba(255, 255, 255, .07);
}
.home-feature-card {
    overflow: hidden;
}
.feature-icon {
    box-shadow: 0 0 22px rgba(139, 92, 255, .16);
    transition: transform .28s ease, box-shadow .28s ease;
}
.home-feature-card:hover .feature-icon {
    transform: translateY(-3px) rotate(-3deg);
    box-shadow: 0 0 25px rgba(92, 235, 255, .18);
}
.workspace-kicker,
.metric-label,
.workflow-home-step span {
    text-transform: uppercase;
    letter-spacing: 1.25px;
}
.workspace-title {
    text-shadow: 0 0 22px rgba(130, 137, 255, .09);
}

/* Top nav and sidebar feel like a product, not default widgets. */
.top-nav {
    background: rgba(9, 16, 36, .68);
    border: 1px solid rgba(125, 148, 255, .21);
    box-shadow: 0 12px 38px rgba(0, 0, 0, .16), inset 0 1px 0 rgba(255, 255, 255, .045);
    backdrop-filter: blur(18px);
}
.top-nav-logo {
    box-shadow: 0 0 22px rgba(108, 98, 255, .25), inset 0 1px 0 rgba(255, 255, 255, .16);
}
.nav-status {
    border-color: rgba(118, 255, 211, .25) !important;
    background: rgba(118, 255, 211, .055) !important;
}
.nav-status i {
    box-shadow: 0 0 12px rgba(118, 255, 211, .85) !important;
}
div[data-testid="stSidebar"] {
    background:
        radial-gradient(ellipse at 10% 0%, rgba(104, 83, 255, .13), transparent 36%),
        linear-gradient(180deg, #0B1022, #090E1D) !important;
    border-right: 1px solid rgba(114, 139, 240, .24) !important;
}
div[data-testid="stSidebar"] div[role="radiogroup"] label {
    border-radius: 12px;
    padding: 8px 10px;
    transition: background .2s ease, border-color .2s ease, transform .2s ease;
}
div[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(93, 116, 255, .10);
    transform: translateX(2px);
}

/* Buttons have a moving highlight on hover, without changing their actions. */
.stButton > button,
.stDownloadButton > button,
div[data-testid="stFormSubmitButton"] > button {
    position: relative;
    overflow: hidden;
    isolation: isolate;
    border: 1px solid rgba(179, 191, 255, .28) !important;
    background: linear-gradient(105deg, #7B4EFF 0%, #536DFF 48%, #168DDE 100%) !important;
    box-shadow: 0 8px 22px rgba(67, 74, 212, .19), inset 0 1px 0 rgba(255,255,255,.15);
    transition: transform .22s ease, box-shadow .22s ease, filter .22s ease;
}
.stButton > button::before,
.stDownloadButton > button::before,
div[data-testid="stFormSubmitButton"] > button::before {
    content: "";
    position: absolute;
    top: -60%;
    left: -70%;
    width: 45%;
    height: 220%;
    transform: rotate(24deg);
    background: linear-gradient(90deg, transparent, rgba(255,255,255,.24), transparent);
    transition: left .55s ease;
    pointer-events: none;
    z-index: -1;
}
.stButton > button:hover,
.stDownloadButton > button:hover,
div[data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-2px);
    filter: saturate(1.12) brightness(1.06);
    box-shadow: 0 12px 28px rgba(77, 109, 255, .26), 0 0 20px rgba(92, 235, 255, .08);
}
.stButton > button:hover::before,
.stDownloadButton > button:hover::before,
div[data-testid="stFormSubmitButton"] > button:hover::before {
    left: 135%;
}
.stButton > button:active,
.stDownloadButton > button:active {
    transform: translateY(0) scale(.99);
}

/* Inputs glow only when focused; typography stays easy to read. */
div[data-testid="stTextArea"] textarea,
div[data-testid="stTextInput"] input,
div[data-testid="stDateInput"] input,
div[data-testid="stNumberInput"] input {
    background: rgba(8, 17, 38, .90) !important;
    border-color: rgba(104, 129, 218, .38) !important;
    border-radius: 13px !important;
    transition: border-color .2s ease, box-shadow .2s ease;
}
div[data-testid="stTextArea"] textarea:focus,
div[data-testid="stTextInput"] input:focus,
div[data-testid="stDateInput"] input:focus,
div[data-testid="stNumberInput"] input:focus {
    border-color: rgba(92, 235, 255, .78) !important;
    box-shadow: 0 0 0 3px rgba(92, 235, 255, .075), 0 0 22px rgba(92, 235, 255, .07) !important;
}
div[data-testid="stFileUploader"] {
    position: relative;
    overflow: hidden;
    background: linear-gradient(115deg, rgba(18, 28, 57, .92), rgba(12, 24, 47, .9)) !important;
    border-color: rgba(108, 136, 255, .62) !important;
}
div[data-testid="stFileUploader"]:hover {
    border-color: rgba(92, 235, 255, .8) !important;
    box-shadow: 0 0 24px rgba(82, 118, 255, .10);
}

/* Small details that make the dashboard feel more polished. */
.deadline-row {
    background:
        linear-gradient(105deg, rgba(29, 40, 82, .91), rgba(12, 25, 48, .93)) !important;
    border-color: rgba(111, 140, 231, .28) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.025);
    transition: transform .22s ease, border-color .22s ease, box-shadow .22s ease;
}
.deadline-row:hover {
    transform: translateX(3px);
    border-color: rgba(92, 235, 255, .45) !important;
    box-shadow: 0 8px 20px rgba(0, 0, 0, .12);
}
.calendar-cell {
    transition: transform .2s ease, border-color .2s ease, background .2s ease;
}
.calendar-cell:not(.empty):hover {
    transform: translateY(-2px);
    border-color: rgba(92, 235, 255, .56);
    background: rgba(50, 73, 135, .34);
}
.page-chip {
    border-color: rgba(92, 235, 255, .24);
    background: linear-gradient(100deg, rgba(94, 95, 255, .12), rgba(37, 184, 232, .07));
    box-shadow: inset 0 1px 0 rgba(255,255,255,.045);
}
.site-footer {
    background:
        radial-gradient(ellipse at 90% 0%, rgba(101, 81, 255, .10), transparent 38%),
        linear-gradient(135deg, rgba(19, 26, 60, .96), rgba(10, 25, 47, .97)) !important;
    border-color: rgba(120, 144, 235, .34) !important;
    box-shadow: 0 -8px 40px rgba(0, 0, 0, .10), inset 0 1px 0 rgba(255,255,255,.04);
}
.footer-link-pill {
    border-color: rgba(99, 141, 230, .32) !important;
    background: rgba(54, 79, 137, .15) !important;
    transition: transform .2s ease, border-color .2s ease, background .2s ease;
}
.footer-link-pill:hover {
    transform: translateY(-2px);
    border-color: rgba(92, 235, 255, .52) !important;
    background: rgba(54, 113, 166, .22) !important;
}

/* Keep motion polished but respect accessibility and small screens. */
@keyframes neonBreath {
    0%, 100% { box-shadow: 0 0 0 rgba(92, 235, 255, 0), inset 0 1px 0 rgba(255,255,255,.035); }
    50% { box-shadow: 0 0 22px rgba(91, 106, 255, .08), inset 0 1px 0 rgba(255,255,255,.07); }
}
.hero,
.top-nav {
    animation: neonBreath 7s ease-in-out infinite;
}
@media (max-width: 800px) {
    .block-container { padding-top: 1rem; }
    .hero { padding: 23px 18px; border-radius: 20px; }
    .top-nav { gap: 10px; }
    .nav-journey { display: none; }
    .workspace-card, .home-feature-card, .workflow-home-step { border-radius: 15px; }
}
@media (prefers-reduced-motion: reduce) {
    .hero, .top-nav { animation: none !important; }
    .hero-robot, .workspace-card, .home-feature-card, .workflow-home-step,
    .panel, .metric, .deadline-row, .calendar-cell, .feature-icon {
        transition: none !important;
        transform: none !important;
    }
}



/* ===== VOICE ASSISTANT STUDIO ===== */
.voice-studio-card {
    border-color: rgba(92, 235, 255, .36) !important;
    background:
        radial-gradient(ellipse at 8% 0%, rgba(87, 104, 255, .18), transparent 44%),
        linear-gradient(145deg, rgba(21, 34, 70, .96), rgba(10, 22, 45, .95)) !important;
}
.voice-context-card {
    border-color: rgba(166, 105, 255, .30) !important;
}
.voice-context-pill {
    margin: 12px 0 6px;
    padding: 10px 13px;
    border-radius: 12px;
    border: 1px solid rgba(118, 255, 211, .25);
    background: rgba(35, 160, 134, .075);
    color: #A7F9DD;
    font-size: 12px;
    overflow-wrap: anywhere;
}
.voice-message-card {
    margin: 8px 0 5px;
    padding: 15px 16px;
    border: 1px solid rgba(117, 138, 226, .34);
    border-radius: 16px;
    background: linear-gradient(120deg, rgba(23, 34, 71, .78), rgba(11, 24, 47, .88));
    box-shadow: inset 0 1px 0 rgba(255,255,255,.035);
}
.voice-message-meta {
    color: #8EA7DE;
    font-size: 9px;
    font-weight: 900;
    letter-spacing: 1.25px;
    margin-bottom: 8px;
}
.voice-question-text {
    color: #EDF3FF;
    font-size: 14px;
    font-weight: 750;
    line-height: 1.6;
    overflow-wrap: anywhere;
}
.voice-context-text {
    color: #A3B3DD;
    font-size: 10px;
    margin-top: 8px;
    overflow-wrap: anywhere;
}
div[data-testid="stAudioInput"] {
    padding: 13px;
    border: 1px solid rgba(103, 133, 244, .44);
    border-radius: 15px;
    background: linear-gradient(135deg, rgba(24, 35, 75, .60), rgba(11, 23, 45, .70));
    box-shadow: 0 0 20px rgba(92, 119, 255, .055);
}
div[data-testid="stAudioInput"] button {
    border-radius: 50% !important;
    border: 1px solid rgba(92, 235, 255, .42) !important;
}
div[data-testid="stAudio"] {
    border-radius: 12px;
    overflow: hidden;
}


/* ==========================================================
   NEXUS PROTOCOL — GRAND VISUAL REDESIGN
   This layer changes appearance only; app logic stays intact.
   ========================================================== */
.stApp {
    font-family: "Space Grotesk", Inter, sans-serif !important;
    background-color: #050816 !important;
    background-image:
        radial-gradient(ellipse at 14% 8%, rgba(64, 105, 255, .19), transparent 30%),
        radial-gradient(ellipse at 86% 4%, rgba(144, 64, 255, .23), transparent 28%),
        radial-gradient(ellipse at 55% 74%, rgba(15, 209, 255, .075), transparent 36%),
        linear-gradient(rgba(97, 123, 255, .075) 1px, transparent 1px),
        linear-gradient(90deg, rgba(97, 123, 255, .075) 1px, transparent 1px),
        linear-gradient(145deg, #050816 0%, #0A1026 52%, #090D1E 100%) !important;
    background-size: auto, auto, auto, 46px 46px, 46px 46px, 100% 100%;
    background-attachment: fixed;
}
.stApp::before {
    opacity: .30;
    filter: drop-shadow(0 0 18px rgba(78, 104, 255, .12));
}
.block-container {
    max-width: 1320px !important;
    padding-left: clamp(1rem, 3.4vw, 3.5rem) !important;
    padding-right: clamp(1rem, 3.4vw, 3.5rem) !important;
    padding-top: 1.15rem !important;
}
h1, h2, h3, p, label {
    font-family: "Space Grotesk", Inter, sans-serif;
}
h1, h2, h3 { letter-spacing: -.045em; }

/* Glass command navigation */
.top-nav {
    position: relative;
    overflow: hidden;
    min-height: 72px;
    border-radius: 22px !important;
    padding: 13px 18px !important;
    margin-bottom: 25px !important;
    background:
        radial-gradient(ellipse at 5% 0%, rgba(96, 118, 255, .15), transparent 38%),
        linear-gradient(110deg, rgba(11, 19, 45, .94), rgba(16, 18, 47, .91)) !important;
    border: 1px solid rgba(122, 148, 255, .29) !important;
    box-shadow: 0 18px 46px rgba(0,0,0,.20), inset 0 1px 0 rgba(255,255,255,.055);
    backdrop-filter: blur(22px);
}
.top-nav::after {
    content: "";
    position: absolute;
    left: 5%;
    right: 5%;
    bottom: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(81,220,255,.72), rgba(164,101,255,.7), transparent);
    opacity: .58;
}
.top-nav-logo {
    font-family: Orbitron, sans-serif !important;
    border-radius: 14px !important;
    background: linear-gradient(145deg, #9160FF, #4B7BFF 55%, #23C8ED) !important;
    box-shadow: 0 0 28px rgba(101, 105, 255, .38), inset 0 1px 0 rgba(255,255,255,.45) !important;
}
.top-nav-wordmark { font-family: Orbitron, "Space Grotesk", sans-serif; letter-spacing: -.035em; }
.top-nav-wordmark b {
    color: #68EDFF !important;
    text-shadow: 0 0 18px rgba(104,237,255,.40);
}
.nav-status {
    padding: 7px 10px !important;
    border-radius: 999px !important;
    border: 1px solid rgba(105, 255, 209, .24) !important;
    background: rgba(43, 223, 170, .06) !important;
    letter-spacing: 1px;
}

/* Fine circuitry and signal sparks inside the hero backdrop. */
.hero-circuit {
    position: absolute;
    z-index: 1;
    inset: 0;
    overflow: hidden;
    border-radius: inherit;
    pointer-events: none;
    background:
        linear-gradient(90deg, transparent 0 7%, rgba(93, 130, 255, .06) 7.05% 7.12%, transparent 7.2% 100%),
        linear-gradient(0deg, transparent 0 82%, rgba(93, 130, 255, .055) 82.05% 82.15%, transparent 82.2% 100%);
}
.hero-circuit span {
    position: absolute;
    display: block;
    width: 3px;
    height: 3px;
    border-radius: 50%;
    background: #72EFFF;
    box-shadow: 0 0 12px 2px rgba(92,235,255,.48);
    animation: circuitSpark 5s ease-in-out infinite;
}
.hero-circuit span:nth-child(1) { top: 13%; left: 43%; animation-delay: -.2s; }
.hero-circuit span:nth-child(2) { top: 24%; left: 8%; animation-delay: -1.4s; }
.hero-circuit span:nth-child(3) { top: 72%; left: 13%; animation-delay: -2.4s; }
.hero-circuit span:nth-child(4) { top: 18%; right: 14%; animation-delay: -3.2s; }
.hero-circuit span:nth-child(5) { top: 79%; right: 8%; animation-delay: -1.1s; }
.hero-circuit span:nth-child(6) { top: 45%; left: 49%; animation-delay: -2.9s; }
.hero-circuit span:nth-child(7) { top: 90%; left: 37%; animation-delay: -4s; }
.hero-circuit span:nth-child(8) { top: 9%; right: 37%; animation-delay: -1.8s; }
.hero-circuit span:nth-child(9) { bottom: 24%; right: 35%; animation-delay: -3.7s; }
.hero-circuit span:nth-child(10) { top: 55%; left: 4%; animation-delay: -.8s; }
.hero-circuit i {
    position: absolute;
    display: block;
    width: 35px;
    height: 35px;
    border: 1px solid rgba(103,180,255,.14);
    transform: rotate(45deg);
}
.hero-circuit i:nth-of-type(1) { top: 13%; left: 47%; }
.hero-circuit i:nth-of-type(2) { bottom: 17%; left: 6%; width: 19px; height: 19px; }
.hero-circuit i:nth-of-type(3) { top: 15%; right: 8%; width: 22px; height: 22px; }
.hero-circuit i:nth-of-type(4) { bottom: 18%; right: 13%; width: 26px; height: 26px; }
@keyframes circuitSpark {
    0%,100% { transform: translate3d(0,0,0) scale(.7); opacity: .35; }
    50% { transform: translate3d(4px,-9px,0) scale(1.3); opacity: 1; }
}

/* The main hero is now a cinematic, layered AI cockpit. */
.hero.hero-ultimate {
    position: relative !important;
    isolation: isolate;
    overflow: hidden !important;
    min-height: 530px;
    margin: 0 0 18px !important;
    padding: clamp(24px, 3.3vw, 47px) clamp(20px, 3.5vw, 48px) 0 !important;
    border-radius: 30px !important;
    border: 1px solid rgba(114, 137, 255, .48) !important;
    background:
        radial-gradient(ellipse at 72% 36%, rgba(76, 95, 255, .24), transparent 35%),
        radial-gradient(ellipse at 96% 7%, rgba(174, 68, 255, .20), transparent 27%),
        radial-gradient(ellipse at 8% 96%, rgba(0, 202, 255, .11), transparent 36%),
        linear-gradient(112deg, rgba(12, 18, 47, .99), rgba(16, 25, 64, .97) 48%, rgba(10, 16, 42, .99)) !important;
    box-shadow:
        0 30px 80px rgba(0,0,0,.32),
        0 0 55px rgba(85,90,255,.13),
        inset 0 1px 0 rgba(255,255,255,.08) !important;
}
.hero.hero-ultimate::before {
    content: "";
    position: absolute;
    inset: 0;
    z-index: -1;
    pointer-events: none;
    border-radius: inherit;
    background:
        linear-gradient(rgba(115,133,255,.09) 1px, transparent 1px),
        linear-gradient(90deg, rgba(115,133,255,.09) 1px, transparent 1px),
        radial-gradient(ellipse at 72% 45%, transparent 20%, rgba(5,8,22,.32) 80%);
    background-size: 34px 34px, 34px 34px, auto;
    mask-image: linear-gradient(90deg, rgba(0,0,0,.12), #000 55%, #000);
}
.hero.hero-ultimate::after {
    content: "";
    position: absolute;
    z-index: -1;
    top: -160px;
    right: -80px;
    width: 440px;
    height: 440px;
    border-radius: 50%;
    background: conic-gradient(from 45deg, rgba(98,109,255,.20), transparent 19%, rgba(83,235,255,.15) 29%, transparent 48%, rgba(168,78,255,.18) 67%, transparent 82%);
    filter: blur(18px);
    animation: nexusAuraSpin 24s linear infinite;
}
@keyframes nexusAuraSpin { to { transform: rotate(360deg); } }
.hero.hero-ultimate .hero-content {
    position: relative;
    z-index: 2;
    display: grid !important;
    grid-template-columns: minmax(0, 1.02fr) minmax(330px, .98fr) !important;
    align-items: center !important;
    gap: clamp(18px, 3vw, 46px) !important;
    min-height: 440px;
}
.hero-ultimate .hero-copy {
    padding: 18px 0 28px;
    max-width: 630px;
}
.hero-live-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    margin: 0 0 22px;
    padding: 8px 12px;
    border: 1px solid rgba(112, 155, 255, .35);
    border-radius: 999px;
    background: rgba(7, 18, 42, .62);
    color: #BDD4FF;
    font-size: 9px;
    line-height: 1;
    font-weight: 900;
    letter-spacing: 1.35px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.04), 0 0 22px rgba(83,110,255,.08);
}
.hero-live-pill b { color: #7B9BFF; }
.hero-live-dot {
    display: block;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #75FFD2;
    box-shadow: 0 0 13px rgba(117,255,210,.92);
    animation: heroDotPulse 1.8s ease-in-out infinite;
}
@keyframes heroDotPulse {
    0%,100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(.7); opacity: .55; }
}
.hero-ultimate .eyebrow {
    display: flex;
    align-items: center;
    gap: 9px;
    color: #9CAFFF !important;
    font-family: Orbitron, sans-serif;
    font-size: 10px;
    letter-spacing: 2px;
    line-height: 1.7;
}
.hero-ultimate .eyebrow::before {
    content: "";
    display: block;
    width: 23px;
    height: 1px;
    background: #66E9FF;
    box-shadow: 0 0 10px #66E9FF;
}
.hero-ultimate h1 {
    margin: 17px 0 18px !important;
    max-width: 670px;
    font-size: clamp(39px, 5.15vw, 70px) !important;
    font-weight: 800 !important;
    line-height: .99 !important;
    letter-spacing: -.065em !important;
    color: #F8FAFF !important;
    text-shadow: 0 8px 38px rgba(0,0,0,.20);
}
.hero-title-gradient {
    color: transparent;
    background: linear-gradient(92deg, #8C78FF 0%, #70AEFF 44%, #74F1F4 81%, #8CFFE2 100%);
    -webkit-background-clip: text;
    background-clip: text;
    filter: drop-shadow(0 0 24px rgba(91,153,255,.13));
}
.hero-ultimate .hero-copy > p {
    max-width: 465px;
    color: #B6C4E7 !important;
    font-size: clamp(13px, 1.2vw, 16px);
    line-height: 1.85;
}
.hero-tag-row {
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
    margin: 25px 0 24px;
}
.hero-tag-row span {
    display: inline-flex;
    gap: 7px;
    align-items: center;
    padding: 8px 10px;
    border-radius: 9px;
    border: 1px solid rgba(121,144,230,.24);
    background: linear-gradient(110deg, rgba(31,45,91,.54), rgba(11,23,49,.58));
    color: #C7D7FF;
    font-size: 9px;
    font-weight: 850;
    letter-spacing: .7px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.035);
}
.hero-tag-row i {
    color: #74E9FF;
    font-style: normal;
    font-size: 13px;
}
.hero-ultimate .creator-byline {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 9px 12px;
    border-radius: 999px;
    border: 1px solid rgba(126,143,255,.25);
    background: rgba(8,15,36,.38);
    color: #AABBE5 !important;
    font-size: 11px;
}
.hero-ultimate .creator-byline b {
    color: #EDF3FF;
    margin-left: 2px;
}

/* Glowing robot chamber with layered orbit rings and floating HUD. */
.hero-ultimate .hero-robot-wrap {
    position: relative !important;
    display: flex !important;
    align-items: center;
    justify-content: center;
    min-width: 0;
    min-height: 425px;
    overflow: visible !important;
    isolation: isolate;
}
.hero-ultimate .hero-robot-wrap::before {
    content: "";
    position: absolute;
    z-index: -2;
    width: min(92%, 420px);
    aspect-ratio: 1;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(76,119,255,.28), rgba(99,68,255,.11) 42%, transparent 71%);
    filter: blur(10px);
    animation: heroCoreBreath 5s ease-in-out infinite;
}
@keyframes heroCoreBreath {
    0%,100% { transform: scale(.94); opacity: .72; }
    50% { transform: scale(1.07); opacity: 1; }
}
.hero-ultimate .hero-robot-wrap::after { display: none !important; }
.hero-ultimate .hero-robot {
    position: relative;
    z-index: 3;
    display: block;
    width: 100%;
    max-width: 435px;
    max-height: 415px;
    object-fit: contain;
    animation: heroRobotFloat 6.2s ease-in-out infinite;
    filter: drop-shadow(0 20px 36px rgba(0,0,0,.22)) drop-shadow(0 0 24px rgba(83,191,255,.13));
}
@keyframes heroRobotFloat {
    0%,100% { transform: translateY(1px) rotate(-.5deg); }
    50% { transform: translateY(-11px) rotate(.5deg); }
}
.hero-orbit {
    position: absolute;
    top: 50%;
    left: 50%;
    border-radius: 50%;
    pointer-events: none;
    transform: translate(-50%, -50%);
}
.hero-orbit-outer {
    z-index: 1;
    width: min(100%, 440px);
    aspect-ratio: 1;
    border: 1px solid rgba(102,207,255,.36);
    box-shadow: 0 0 20px rgba(91,194,255,.08), inset 0 0 24px rgba(92,126,255,.06);
    animation: heroOrbitSpin 30s linear infinite;
}
.hero-orbit-outer::before,
.hero-orbit-outer::after {
    content: "";
    position: absolute;
    border-radius: 50%;
    border: 2px solid transparent;
}
.hero-orbit-outer::before {
    inset: 13px;
    border-top-color: rgba(125,118,255,.92);
    border-right-color: rgba(88,232,255,.58);
    transform: rotate(25deg);
}
.hero-orbit-outer::after {
    inset: -7px;
    border-bottom: 1px dashed rgba(152,132,255,.50);
    border-left: 1px dashed rgba(88,232,255,.42);
}
.hero-orbit-inner {
    z-index: 1;
    width: min(80%, 350px);
    aspect-ratio: 1;
    border: 1px dashed rgba(140,144,255,.28);
    box-shadow: 0 0 28px rgba(98,95,255,.07);
    animation: heroOrbitSpin 42s linear infinite reverse;
}
@keyframes heroOrbitSpin { to { rotate: 360deg; } }
.hero-orbit-core {
    position: absolute;
    z-index: 0;
    left: 50%;
    top: 50%;
    width: 70%;
    aspect-ratio: 1;
    transform: translate(-50%,-50%);
    border-radius: 50%;
    background: radial-gradient(circle, rgba(81,117,255,.15), rgba(35,61,127,.07) 45%, transparent 72%);
    box-shadow: 0 0 90px rgba(72,106,255,.09);
}
.hero-orbit-node {
    position: absolute;
    z-index: 4;
    display: grid;
    place-items: center;
    width: 34px;
    height: 34px;
    border-radius: 12px;
    color: #BCFAFF;
    background: rgba(18,31,68,.87);
    border: 1px solid rgba(104,230,255,.55);
    box-shadow: 0 0 23px rgba(72,195,255,.15), inset 0 1px 0 rgba(255,255,255,.09);
    font-size: 15px;
    backdrop-filter: blur(12px);
}
.node-one { top: 16%; left: 13%; animation: nodeFloat 5s ease-in-out infinite; }
.node-two { top: 28%; right: 7%; animation: nodeFloat 6s ease-in-out infinite reverse; }
.node-three { bottom: 18%; left: 15%; animation: nodeFloat 5.5s ease-in-out infinite; }
@keyframes nodeFloat { 0%,100% { translate: 0 0; } 50% { translate: 0 -8px; } }
.hero-hud {
    position: absolute;
    z-index: 5;
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 10px 12px;
    border-radius: 13px;
    background: linear-gradient(135deg, rgba(16,29,63,.92), rgba(8,17,40,.86));
    border: 1px solid rgba(117,156,255,.39);
    box-shadow: 0 16px 38px rgba(0,0,0,.24), inset 0 1px 0 rgba(255,255,255,.07);
    backdrop-filter: blur(14px);
}
.hero-hud-top { top: 9%; right: -1%; }
.hero-hud-bottom { bottom: 9%; left: -1%; }
.hero-hud-icon, .hero-wave-icon {
    display: grid;
    place-items: center;
    width: 30px;
    height: 30px;
    border-radius: 9px;
    color: #8AF0FF;
    background: rgba(92,177,255,.12);
    font-size: 17px;
}
.hero-wave-icon { color: #B4A1FF; background: rgba(144,99,255,.15); }
.hero-hud small {
    display: block;
    color: #8FA6DA;
    font-size: 8px;
    font-weight: 800;
    letter-spacing: 1px;
    white-space: nowrap;
}
.hero-hud b {
    display: block;
    margin-top: 3px;
    color: #F0F5FF;
    font-family: Orbitron, sans-serif;
    font-size: 9px;
    letter-spacing: .5px;
    white-space: nowrap;
}
.hero-hud-top > i {
    display: block;
    width: 6px;
    height: 6px;
    margin-left: 5px;
    border-radius: 50%;
    background: #73FFD1;
    box-shadow: 0 0 10px rgba(115,255,209,.9);
}

/* Hero ribbon and manifesto turn the fold into an experience. */
.hero-bottom-ribbon {
    position: relative;
    z-index: 4;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 15px;
    min-height: 63px;
    margin: 0 -48px;
    padding: 13px clamp(18px, 3.5vw, 48px);
    border-top: 1px solid rgba(118,142,244,.22);
    background: linear-gradient(90deg, rgba(9,16,38,.74), rgba(13,24,51,.88), rgba(10,16,37,.78));
}
.ribbon-label {
    color: #778EBE;
    font-size: 8px;
    font-weight: 900;
    letter-spacing: 1.65px;
    margin-right: 2px;
}
.hero-bottom-ribbon > span:not(.ribbon-label):not(.ribbon-live) {
    color: #C6D5F5;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: .6px;
}
.hero-bottom-ribbon > span i {
    color: #73E8FF;
    font-style: normal;
    font-family: Orbitron, sans-serif;
    margin-right: 5px;
}
.ribbon-separator { color: #485B94; font-weight: 400; }
.ribbon-live {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    margin-left: auto;
    color: #84EFD3;
    font-size: 8px;
    font-weight: 900;
    letter-spacing: 1px;
}
.ribbon-live i { width: 5px; height: 5px; border-radius: 50%; background: #7CFFD8; box-shadow: 0 0 9px #7CFFD8; }
.home-hero-manifesto {
    position: relative;
    display: flex;
    align-items: center;
    gap: 24px;
    margin: 0 0 30px;
    padding: 16px 20px;
    border-radius: 17px;
    border: 1px solid rgba(112,139,226,.17);
    background: linear-gradient(100deg, rgba(20,29,61,.55), rgba(10,18,39,.34));
    box-shadow: inset 0 1px 0 rgba(255,255,255,.025);
}
.home-hero-manifesto > div { display: flex; flex-direction: column; gap: 5px; min-width: max-content; }
.manifesto-kicker { color: #7EDFFD; font-size: 8px; letter-spacing: 1.5px; font-weight: 900; }
.home-hero-manifesto b { color: #EBF1FF; font-size: 15px; letter-spacing: -.4px; }
.home-hero-manifesto p { flex: 1; margin: 0; color: #96A8D1 !important; font-size: 11px; line-height: 1.6; }
.manifesto-arrow { color: #8F91FF; font-size: 25px; }

/* Make the feature area feel like a designed product showcase. */
.home-section-title {
    position: relative;
    margin-top: 30px !important;
    margin-bottom: 7px !important;
    font-size: clamp(21px, 2.6vw, 29px) !important;
    font-weight: 800;
    letter-spacing: -.055em !important;
}
.home-section-subtitle {
    max-width: 720px;
    color: #9DADD4 !important;
    font-size: 12px !important;
    line-height: 1.7;
}
.home-feature-card {
    min-height: 205px;
    overflow: hidden;
    border-radius: 20px !important;
}
.home-feature-card h3 { font-size: 19px !important; }
.home-feature-card p { color: #AAB9DD !important; line-height: 1.75; }
.feature-icon {
    width: 49px !important;
    height: 49px !important;
    display: grid !important;
    place-items: center;
    border-radius: 15px !important;
    background: linear-gradient(140deg, rgba(125,87,255,.19), rgba(50,185,255,.10)) !important;
    border: 1px solid rgba(112,143,255,.26) !important;
}
.workflow-home-step { min-height: 140px; border-radius: 17px !important; }
.workflow-home-step b { font-size: 16px; }
.workspace-card { border-radius: 21px !important; }

/* Unified ambient decoration across all pages. */
.page-heading {
    position: relative;
    overflow: hidden;
    border-radius: 23px;
    padding: 25px 28px;
    margin-bottom: 18px;
    border: 1px solid rgba(113,139,234,.22);
    background:
        radial-gradient(ellipse at 100% 0%, rgba(124,77,255,.13), transparent 42%),
        linear-gradient(110deg, rgba(16,26,56,.68), rgba(9,17,38,.55));
}
.page-heading h1 {
    margin: 10px 0 !important;
    font-size: clamp(29px, 4vw, 44px) !important;
    letter-spacing: -.055em !important;
}
.page-heading p { max-width: 770px; color: #A9B9DE !important; line-height: 1.7; }
.metric { min-height: 120px; border-radius: 18px !important; }
.metric-value { font-family: Orbitron, sans-serif; color: #EAF3FF; }
.deadline-row, .calendar-cell, .voice-message-card { backdrop-filter: blur(10px); }

/* Small screens keep the hero spectacular without sacrificing readability. */
@media (max-width: 900px) {
    .hero.hero-ultimate { min-height: 0; }
    .hero-ultimate .hero-content {
        grid-template-columns: minmax(0, 1fr) minmax(260px, .8fr) !important;
        gap: 10px !important;
        min-height: 410px;
    }
    .hero-ultimate h1 { font-size: clamp(36px, 5.2vw, 54px) !important; }
    .hero-ultimate .hero-robot-wrap { min-height: 355px; }
    .hero-ultimate .hero-robot { max-height: 350px; }
    .hero-bottom-ribbon { margin-left: -28px; margin-right: -28px; }
    .ribbon-label { display: none; }
}
@media (max-width: 650px) {
    .hero.hero-ultimate { padding: 23px 17px 0 !important; border-radius: 22px !important; }
    .hero-ultimate .hero-content { display: flex !important; flex-direction: column; align-items: stretch !important; gap: 0 !important; }
    .hero-ultimate .hero-copy { padding: 5px 0 0; }
    .hero-live-pill { margin-bottom: 16px; font-size: 8px; letter-spacing: .8px; }
    .hero-ultimate .eyebrow { font-size: 9px; }
    .hero-ultimate h1 { font-size: clamp(38px, 11vw, 54px) !important; line-height: 1.02 !important; }
    .hero-ultimate .hero-copy > p { font-size: 13px; }
    .hero-tag-row { gap: 5px; margin: 18px 0; }
    .hero-tag-row span { font-size: 8px; padding: 7px 8px; }
    .hero-ultimate .hero-robot-wrap { min-height: 275px; margin-top: -3px; }
    .hero-ultimate .hero-robot { max-height: 295px; max-width: 330px; }
    .hero-orbit-outer { width: min(100%, 300px); }
    .hero-orbit-inner { width: min(76%, 245px); }
    .hero-hud { padding: 8px; gap: 6px; }
    .hero-hud-top { top: 3%; right: -1%; }
    .hero-hud-bottom { bottom: 4%; left: -1%; }
    .hero-hud-icon, .hero-wave-icon { width: 25px; height: 25px; }
    .hero-hud small { font-size: 7px; }
    .hero-hud b { font-size: 8px; }
    .hero-orbit-node { width: 28px; height: 28px; }
    .hero-bottom-ribbon { margin: 0 -17px; padding: 12px 15px; gap: 9px; }
    .hero-bottom-ribbon > span:not(.ribbon-label):not(.ribbon-live) { font-size: 8px; }
    .ribbon-separator { display: none; }
    .ribbon-live { margin-left: 0; width: 100%; padding-top: 7px; border-top: 1px solid rgba(118,142,244,.13); }
    .home-hero-manifesto { align-items: flex-start; gap: 10px; padding: 14px; }
    .home-hero-manifesto > div { min-width: 0; }
    .home-hero-manifesto b { font-size: 13px; }
    .home-hero-manifesto p { font-size: 10px; }
    .manifesto-arrow { display: none; }
}
@media (prefers-reduced-motion: reduce) {
    .hero.hero-ultimate::after,
    .hero-live-dot,
    .hero-orbit,
    .hero-robot,
    .hero-orbit-node { animation: none !important; }
    .hero-robot { transform: none !important; }
}



/* =========================================================
   NEXUS 2.0 — ADVANCED BENTO / ORBITAL DESIGN SYSTEM
   Visual-only styles; no analysis or navigation logic changed.
   ========================================================= */
.nexus-section-head {
    position: relative;
    margin: 42px 0 20px;
    padding: 0 1px;
}
.nexus-section-kicker {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
    color: #86CFFF;
    font-family: Orbitron, sans-serif;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1.35px;
    line-height: 1.8;
}
.nexus-section-kicker > span {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #82FFE1;
    box-shadow: 0 0 12px rgba(130,255,225,.8);
    animation: nexusKickerPulse 2.6s ease-in-out infinite;
}
.nexus-section-kicker > i {
    display: inline-block;
    width: 35px;
    height: 1px;
    background: linear-gradient(90deg, rgba(93,216,255,.7), transparent);
}
@keyframes nexusKickerPulse { 0%,100% { opacity: .65; scale: .82; } 50% { opacity: 1; scale: 1.15; } }
.nexus-section-title {
    margin-top: 14px;
    color: #F3F6FF;
    font-size: clamp(30px, 4.2vw, 51px);
    font-weight: 800;
    line-height: 1.04;
    letter-spacing: -.065em;
}
.nexus-section-title b, .nexus-process-head h2 b {
    color: transparent;
    background: linear-gradient(95deg, #9182FF, #76BFFF 50%, #7BF3E5);
    -webkit-background-clip: text;
    background-clip: text;
}
.nexus-section-head > p, .nexus-process-head > p {
    max-width: 650px;
    margin-top: 12px;
    color: #A4B6DC !important;
    font-size: 12px;
    line-height: 1.8;
}
.nexus-signal-strip {
    position: relative;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 13px;
    overflow: hidden;
    margin: 18px 0 15px;
    padding: 13px 16px;
    border: 1px solid rgba(100,136,235,.23);
    border-radius: 14px;
    background: linear-gradient(105deg, rgba(13,24,52,.89), rgba(18,22,55,.72));
    box-shadow: inset 0 1px 0 rgba(255,255,255,.04);
}
.nexus-signal-strip::after {
    content: "";
    position: absolute;
    top: 0; bottom: 0; left: -30%;
    width: 23%;
    background: linear-gradient(90deg, transparent, rgba(98,221,255,.055), transparent);
    transform: skewX(-22deg);
    animation: signalSweep 7.5s ease-in-out infinite;
    pointer-events: none;
}
@keyframes signalSweep { 0%,25% { left: -30%; } 70%,100% { left: 130%; } }
.nexus-signal-brand {
    color: #E7EFFF;
    font-family: Orbitron, sans-serif;
    font-size: 12px;
    font-weight: 900;
}
.nexus-signal-brand b { color: #75EFFF; }
.nexus-signal-item {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    color: #A6B9E4;
    font-size: 8px;
    font-weight: 850;
    letter-spacing: .9px;
    white-space: nowrap;
}
.nexus-signal-item i {
    display: inline-block;
    width: 5px; height: 5px;
    border-radius: 50%;
    background: #7CFFD6;
    box-shadow: 0 0 9px rgba(124,255,214,.7);
}
.nexus-signal-arrow { color: #576FAB; font-size: 13px; font-weight: 400; }
.nexus-signal-tail {
    margin-left: auto;
    color: #5F76A9;
    font-family: Orbitron, sans-serif;
    font-size: 7px;
    letter-spacing: .8px;
}

/* Bento canvas: intentionally varied card proportions. */
.nexus-bento-grid {
    display: grid;
    grid-template-columns: 1.15fr .85fr;
    grid-template-rows: minmax(340px, auto) minmax(300px, auto);
    gap: 13px;
    margin: 0 0 43px;
}
.nexus-bento-card {
    position: relative;
    overflow: hidden;
    isolation: isolate;
    min-width: 0;
    padding: 22px;
    border-radius: 22px;
    border: 1px solid rgba(115,142,235,.25);
    background:
        radial-gradient(ellipse at 92% 0%, rgba(101,86,255,.10), transparent 36%),
        linear-gradient(145deg, rgba(19,31,66,.91), rgba(9,17,37,.97));
    box-shadow: 0 18px 42px rgba(0,0,0,.13), inset 0 1px 0 rgba(255,255,255,.045);
    transition: border-color .35s ease, transform .35s cubic-bezier(.2,.8,.2,1), box-shadow .35s ease;
}
.nexus-bento-card::before {
    content: "";
    position: absolute;
    inset: 0;
    z-index: -1;
    border-radius: inherit;
    opacity: .72;
    pointer-events: none;
    background:
        linear-gradient(110deg, rgba(97,136,255,.06), transparent 45%),
        radial-gradient(ellipse at 100% 100%, rgba(39,190,255,.05), transparent 45%);
}
.nexus-bento-card::after {
    content: "";
    position: absolute;
    top: 0; left: 10%; right: 10%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(124,205,255,.6), rgba(160,124,255,.5), transparent);
    opacity: .58;
    pointer-events: none;
}
.nexus-bento-card:hover {
    transform: translateY(-5px);
    border-color: rgba(103,216,255,.46);
    box-shadow: 0 24px 48px rgba(0,0,0,.23), 0 0 27px rgba(81,109,255,.10), inset 0 1px 0 rgba(255,255,255,.07);
}
.bento-ai { grid-row: span 2; }
.bento-ai::before {
    background:
        radial-gradient(ellipse at 100% 20%, rgba(105,71,255,.20), transparent 48%),
        radial-gradient(ellipse at 18% 82%, rgba(18,169,255,.09), transparent 49%),
        linear-gradient(110deg, rgba(97,136,255,.055), transparent 45%);
}
.bento-voice { background: radial-gradient(ellipse at 86% 15%, rgba(61,99,255,.16), transparent 42%), linear-gradient(145deg, rgba(20,31,67,.93), rgba(9,16,36,.98)); }
.bento-deadline { background: radial-gradient(ellipse at 100% 100%, rgba(8,198,207,.09), transparent 53%), linear-gradient(145deg, rgba(17,34,60,.92), rgba(8,18,35,.98)); }
.bento-library { background: radial-gradient(ellipse at 100% 0%, rgba(161,80,255,.12), transparent 45%), linear-gradient(145deg, rgba(23,27,61,.92), rgba(10,16,36,.98)); }
.bento-topline { display:flex; align-items:center; gap:10px; position:relative; z-index:2; }
.bento-icon {
    display:grid; place-items:center;
    width:37px; height:37px;
    border-radius:12px;
    border:1px solid rgba(127,158,255,.32);
    color:#9DEEFF;
    background:linear-gradient(140deg, rgba(125,88,255,.18), rgba(45,159,255,.09));
    font-size:18px;
    box-shadow:0 0 20px rgba(105,117,255,.10);
}
.bento-index { color:#7F95C3; font-family:Orbitron,sans-serif; font-size:8px; letter-spacing:1.2px; font-weight:800; }
.bento-corner { margin-left:auto; color:#718DCC; font-size:17px; }
.bento-overline { margin-top:26px; color:#74DEFF; font-family:Orbitron,sans-serif; font-size:8px; font-weight:800; letter-spacing:1.55px; }
.nexus-bento-card h3 {
    position:relative;
    z-index:2;
    margin:10px 0 9px !important;
    color:#F1F5FF !important;
    font-size:clamp(24px, 2.8vw, 36px) !important;
    line-height:1.04 !important;
    letter-spacing:-.06em !important;
}
.nexus-bento-card h3 em { color:transparent; background:linear-gradient(90deg,#A293FF,#75C7FF 60%,#82F5E0); -webkit-background-clip:text; background-clip:text; font-style:normal; }
.nexus-bento-card p {
    max-width:460px;
    color:#A5B6DD !important;
    font-size:11px !important;
    line-height:1.8 !important;
}
.bento-ai .bento-copy { max-width:390px; position:relative; z-index:2; }
.bento-ambient-ring {
    position:absolute;
    top:10%; right:-23%;
    width:330px; height:330px;
    border-radius:50%;
    border:1px solid rgba(118,127,255,.10);
    box-shadow:0 0 0 22px rgba(116,124,255,.025), 0 0 0 45px rgba(116,124,255,.018);
    pointer-events:none;
    animation: ambientTurn 28s linear infinite;
}
.bento-ambient-ring::before,.bento-ambient-ring::after {
    content:""; position:absolute; border-radius:50%; border:1px dashed rgba(105,211,255,.14);
}
.bento-ambient-ring::before { inset:22px; }
.bento-ambient-ring::after { inset:56px; border-color:rgba(162,111,255,.18); }
@keyframes ambientTurn { to { rotate:360deg; } }
.nexus-mini-terminal {
    position:relative; z-index:2;
    max-width:450px;
    margin-top:25px;
    padding:16px;
    border-radius:16px;
    border:1px solid rgba(114,151,255,.24);
    background:linear-gradient(145deg, rgba(6,14,32,.88), rgba(13,24,48,.86));
    box-shadow:0 18px 34px rgba(0,0,0,.18), inset 0 1px 0 rgba(255,255,255,.035);
}
.terminal-top { display:flex; justify-content:space-between; align-items:center; gap:10px; color:#748DBD; font-family:Orbitron,sans-serif; font-size:7px; font-weight:800; letter-spacing:.8px; }
.terminal-lights { display:flex; gap:4px; }
.terminal-lights i { display:block; width:5px; height:5px; border-radius:50%; background:#596D9F; }
.terminal-lights i:first-child { background:#A48EFF; box-shadow:0 0 8px rgba(164,142,255,.55); }
.terminal-scan { display:flex; align-items:center; gap:9px; margin:16px 0 12px; padding:9px 10px; border-radius:9px; border:1px solid rgba(103,217,255,.16); background:rgba(46,117,162,.07); color:#A7DFFF; font-size:9px; font-weight:800; letter-spacing:.65px; }
.terminal-scan span { width:6px; height:6px; border-radius:50%; background:#78FFD2; box-shadow:0 0 10px #78FFD2; }
.terminal-scan i { margin-left:auto; color:#78FFD2; font-size:7px; font-style:normal; letter-spacing:1px; }
.terminal-rule { height:6px; margin:10px 0; overflow:hidden; border-radius:99px; background:rgba(107,132,190,.13); }
.terminal-rule span { display:block; height:100%; border-radius:inherit; background:linear-gradient(90deg, rgba(116,98,255,.7), rgba(93,218,255,.68)); box-shadow:0 0 10px rgba(93,218,255,.24); }
.terminal-result { display:flex; align-items:center; gap:10px; margin-top:16px; padding:12px 10px; border-radius:11px; border:1px solid rgba(120,255,216,.17); background:rgba(57,183,151,.055); }
.terminal-result-icon { display:grid; place-items:center; width:29px; height:29px; border-radius:9px; background:rgba(130,255,223,.11); color:#8BFFE1; }
.terminal-result small { display:block; color:#75BFB8; font-size:7px; font-family:Orbitron,sans-serif; letter-spacing:1px; }
.terminal-result b { display:block; margin-top:4px; color:#DAFDF2; font-size:10px; }
.terminal-check { margin-left:auto; color:#8DFFD4; font-size:16px; }
.bento-voice-orb { position:relative; float:right; width:92px; height:92px; margin:10px 3px 0 12px; display:grid; place-items:center; }
.bento-voice-orb::before,.bento-voice-orb::after { content:""; position:absolute; inset:0; border:1px solid rgba(118,143,255,.26); border-radius:50%; }
.bento-voice-orb::before { transform:scale(.76); border-style:dashed; animation:ambientTurn 16s linear infinite; }
.bento-voice-orb::after { transform:scale(1.12); border-color:rgba(91,232,255,.18); box-shadow:0 0 22px rgba(91,232,255,.05); }
.voice-orb-core { display:grid; place-items:center; width:48px; height:48px; border-radius:17px; color:#E9F7FF; font-family:Orbitron,sans-serif; font-size:12px; font-weight:900; background:linear-gradient(145deg,rgba(130,92,255,.55),rgba(30,155,221,.4)); border:1px solid rgba(148,197,255,.48); box-shadow:0 0 23px rgba(95,114,255,.25), inset 0 1px 0 rgba(255,255,255,.24); }
.bento-voice-orb > span { position:absolute; width:6px; height:6px; border-radius:50%; background:#84FFE2; box-shadow:0 0 9px #84FFE2; }
.bento-voice-orb > span:nth-child(2) { top:3px; left:44px; }
.bento-voice-orb > span:nth-child(3) { right:0; bottom:27px; background:#B5A1FF; box-shadow:0 0 9px #B5A1FF; }
.bento-voice-orb > span:nth-child(4) { left:11px; bottom:8px; }
.bento-wave { display:flex; align-items:center; gap:3px; height:28px; margin-top:20px; overflow:hidden; }
.bento-wave i { display:block; width:3px; border-radius:9px; height:var(--wave-height, 13px); background:linear-gradient(180deg,#8D7EFF,#60DBFF); box-shadow:0 0 8px rgba(96,219,255,.22); animation:miniWave .95s ease-in-out infinite alternate; }
.bento-wave i:nth-child(3n) { --wave-height:22px; animation-delay:-.35s; }
.bento-wave i:nth-child(3n + 1) { --wave-height:10px; animation-delay:-.1s; }
.bento-wave i:nth-child(3n + 2) { --wave-height:17px; animation-delay:-.55s; }
@keyframes miniWave { from { height:5px; opacity:.55; } to { height:var(--wave-height,13px); opacity:1; } }
.bento-calendar-preview { margin-top:15px; padding:12px; border:1px solid rgba(98,176,226,.18); border-radius:14px; background:rgba(5,15,33,.47); }
.calendar-preview-head { display:flex; align-items:center; justify-content:space-between; color:#A5DFFF; font-family:Orbitron,sans-serif; font-size:8px; letter-spacing:1px; }
.calendar-preview-head span { color:#708AB7; font-size:7px; }
.calendar-preview-days,.calendar-preview-numbers { display:grid; grid-template-columns:repeat(7,minmax(0,1fr)); gap:4px; margin-top:12px; text-align:center; }
.calendar-preview-days span { color:#687FAE; font-size:8px; }
.calendar-preview-numbers span { display:grid; place-items:center; min-height:27px; border-radius:7px; background:rgba(57,84,138,.10); color:#A9BBE3; font-size:9px; }
.calendar-preview-numbers .calendar-preview-mark { color:#061826; background:linear-gradient(145deg,#82F5E0,#70CFFF); font-weight:900; box-shadow:0 0 14px rgba(95,229,232,.17); }
.calendar-preview-foot { display:flex; align-items:center; gap:7px; margin-top:11px; color:#78BEBE; font-size:7px; font-weight:900; letter-spacing:.8px; }
.calendar-preview-foot i { display:block; width:5px; height:5px; border-radius:50%; background:#79FBD8; box-shadow:0 0 8px #79FBD8; }
.bento-stack { position:relative; width:100%; height:110px; margin-top:19px; perspective:600px; }
.stack-sheet { position:absolute; width:190px; max-width:75%; height:88px; border-radius:12px; border:1px solid rgba(126,149,241,.26); }
.sheet-back { left:12px; top:0; transform:rotate(-8deg); background:linear-gradient(135deg,rgba(102,87,255,.13),rgba(19,36,68,.5)); }
.sheet-mid { left:26px; top:4px; transform:rotate(5deg); background:linear-gradient(135deg,rgba(43,165,218,.15),rgba(12,30,53,.7)); }
.sheet-front { left:19px; top:8px; padding:12px; background:linear-gradient(135deg,rgba(20,37,73,.98),rgba(9,21,43,.98)); box-shadow:0 12px 25px rgba(0,0,0,.22); }
.sheet-front > span { display:block; color:#71BFD9; font-size:7px; font-family:Orbitron,sans-serif; letter-spacing:1px; }
.sheet-front b { display:block; margin-top:8px; color:#E4EBFF; font-size:12px; }
.sheet-front > i { display:block; margin-top:4px; color:#7F91B9; font-size:6px; font-style:normal; letter-spacing:.4px; }
.stack-lines { width:82%; height:4px; margin-top:9px; border-radius:8px; background:linear-gradient(90deg,#6378C9 70%,transparent 70%); opacity:.45; }
.stack-star { position:absolute; top:2px; left:192px; color:#A5A1FF; font-size:24px; text-shadow:0 0 14px rgba(165,161,255,.5); animation:starBlink 3s ease-in-out infinite; }
@keyframes starBlink { 0%,100% { opacity:.5; transform:scale(.9) rotate(-8deg); } 50% { opacity:1; transform:scale(1.1) rotate(7deg); } }
.bento-local-note { display:flex; align-items:center; gap:7px; margin-top:14px; color:#8DA8CA; font-size:7px; font-weight:900; letter-spacing:.7px; }
.bento-local-note span { width:5px; height:5px; border-radius:50%; background:#87EFD0; box-shadow:0 0 8px #87EFD0; }

/* A connected pipeline rail replaces generic floating feature tiles. */
.nexus-process-head { display:flex; align-items:end; justify-content:space-between; gap:22px; margin:36px 0 15px; }
.nexus-process-head h2 { margin:10px 0 0; color:#F0F4FF; font-size:clamp(23px,3vw,33px); letter-spacing:-.055em; }
.nexus-process-head > p { max-width:350px; margin:0 0 2px; font-size:10px; }
.nexus-process-rail { display:grid; grid-template-columns:minmax(0,1fr) 24px minmax(0,1fr) 24px minmax(0,1fr) 24px minmax(0,1fr); align-items:center; gap:4px; margin-bottom:30px; }
.process-node { min-width:0; min-height:130px; padding:16px; border:1px solid rgba(112,140,232,.23); border-radius:17px; background:linear-gradient(145deg,rgba(19,32,65,.8),rgba(9,17,37,.82)); box-shadow:inset 0 1px 0 rgba(255,255,255,.04); transition:transform .25s ease,border-color .25s ease; }
.process-node:hover { transform:translateY(-4px); border-color:rgba(93,219,255,.48); }
.process-node-top { display:flex; justify-content:space-between; align-items:center; color:#7188C3; font-family:Orbitron,sans-serif; font-size:8px; }
.process-node-top i { display:grid; place-items:center; width:26px; height:26px; border-radius:9px; color:#A2EFFF; background:rgba(93,193,255,.09); border:1px solid rgba(93,193,255,.16); font-style:normal; font-size:13px; }
.process-node > b { display:block; margin-top:13px; color:#EAF0FF; font-size:13px; }
.process-node > p { margin:6px 0 0; color:#91A7D1 !important; font-size:9px !important; line-height:1.65; }
.process-connector { position:relative; height:1px; background:rgba(99,126,202,.25); }
.process-connector span { position:absolute; top:-2px; left:0; width:5px; height:5px; border-radius:50%; background:#70E9FF; box-shadow:0 0 9px #70E9FF; animation:connectorTravel 2.4s ease-in-out infinite; }
@keyframes connectorTravel { from { left:0; opacity:.3; } 50% { opacity:1; } to { left:calc(100% - 5px); opacity:.3; } }

/* Navigation selected state and restrained ambient motion. */
div[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    border:1px solid rgba(118,153,255,.32);
    background:linear-gradient(100deg,rgba(111,84,255,.18),rgba(47,153,220,.08));
    box-shadow:inset 3px 0 0 #8B82FF,0 5px 18px rgba(0,0,0,.10);
}
div[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p { color:#F0F5FF !important; font-weight:800; }
.stApp::after {
    content:"";
    position:fixed;
    z-index:-1;
    top:17%;
    right:-180px;
    width:330px;
    height:520px;
    border-radius:50%;
    background:linear-gradient(180deg,rgba(117,71,255,.045),rgba(58,207,255,.035));
    filter:blur(60px);
    pointer-events:none;
    animation:ambientDrift 18s ease-in-out infinite alternate;
}
@keyframes ambientDrift { from { transform:translate3d(0,-20px,0); } to { transform:translate3d(-110px,45px,0); } }

@media (max-width: 950px) {
    .nexus-bento-grid { grid-template-columns:1fr 1fr; grid-template-rows:auto; }
    .bento-ai { grid-row:auto; grid-column:span 2; }
    .bento-ai .bento-copy { max-width:520px; }
    .nexus-mini-terminal { max-width:560px; }
    .nexus-process-rail { grid-template-columns:1fr 20px 1fr; row-gap:10px; }
    .process-connector:nth-of-type(4) { display:none; }
    .nexus-signal-tail { display:none; }
}
@media (max-width: 620px) {
    .nexus-section-head { margin-top:32px; }
    .nexus-section-kicker { font-size:8px; gap:7px; }
    .nexus-section-kicker > i { width:17px; }
    .nexus-signal-strip { gap:9px; padding:12px 11px; }
    .nexus-signal-brand { width:100%; padding-bottom:8px; border-bottom:1px solid rgba(110,136,222,.14); }
    .nexus-signal-arrow { display:none; }
    .nexus-signal-item { font-size:7px; }
    .nexus-bento-grid { grid-template-columns:1fr; gap:10px; }
    .bento-ai { grid-column:auto; }
    .nexus-bento-card { padding:17px; border-radius:18px; }
    .nexus-bento-card h3 { font-size:29px !important; }
    .nexus-mini-terminal { padding:12px; }
    .bento-voice-orb { width:72px; height:72px; margin-right:0; }
    .voice-orb-core { width:40px; height:40px; border-radius:14px; }
    .stack-star { left:min(192px,66%); }
    .nexus-process-head { display:block; }
    .nexus-process-head > p { margin-top:9px; }
    .nexus-process-rail { grid-template-columns:1fr; gap:8px; }
    .process-node { min-height:0; padding:14px; }
    .process-connector { display:block !important; width:1px; height:12px; margin-left:23px; }
    .process-connector span { top:0; left:-2px; width:5px; height:5px; animation:connectorTravelVertical 2.4s ease-in-out infinite; }
    @keyframes connectorTravelVertical { from { top:0; opacity:.3; } to { top:calc(100% - 5px); opacity:.3; } }
}
@media (prefers-reduced-motion: reduce) {
    .nexus-signal-strip::after, .nexus-section-kicker > span, .bento-ambient-ring,
    .bento-voice-orb::before, .bento-voice-orb > span, .bento-wave i,
    .stack-star, .process-connector span, .stApp::after { animation:none !important; }
    .nexus-bento-card, .process-node { transition:none !important; }
}



/* =========================================================
   NEXUS 3.0 — DIMENSIONAL INTERFACE / VISUAL-ONLY OVERRIDES
   ========================================================= */
html { scroll-behavior: smooth; }
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: #070C1B; }
::-webkit-scrollbar-thumb {
    border: 2px solid #070C1B;
    border-radius: 99px;
    background: linear-gradient(180deg, #7D6CFF, #34C7EA);
}
::-webkit-scrollbar-thumb:hover { background: linear-gradient(180deg, #A493FF, #70F1FF); }

.stApp::after {
    position: fixed !important;
    inset: -12% !important;
    z-index: -1 !important;
    width: auto !important;
    height: auto !important;
    border-radius: 0 !important;
    pointer-events: none !important;
    opacity: .9;
    filter: blur(34px);
    background:
        radial-gradient(ellipse at 18% 14%, rgba(42, 121, 255, .10), transparent 24%),
        radial-gradient(ellipse at 85% 23%, rgba(152, 63, 255, .11), transparent 28%),
        radial-gradient(ellipse at 64% 82%, rgba(30, 226, 220, .055), transparent 29%);
    animation: nexusAuroraDrift 25s ease-in-out infinite alternate;
}
@keyframes nexusAuroraDrift {
    0% { transform: translate3d(-1%, -1%, 0) scale(1); }
    50% { transform: translate3d(1%, 1.5%, 0) scale(1.025); }
    100% { transform: translate3d(-.5%, 1%, 0) scale(1.01); }
}

/* Thin technical grid overlay and quiet glass finish for all page headers. */
.page-heading {
    isolation: isolate;
    box-shadow: 0 16px 42px rgba(0,0,0,.12), inset 0 1px 0 rgba(255,255,255,.055);
}
.page-heading::before {
    content: "";
    position: absolute;
    z-index: 0;
    inset: 0;
    pointer-events: none;
    opacity: .7;
    background:
        linear-gradient(rgba(119,143,255,.055) 1px, transparent 1px),
        linear-gradient(90deg, rgba(119,143,255,.055) 1px, transparent 1px);
    background-size: 24px 24px;
    mask-image: linear-gradient(90deg, transparent, #000 70%);
}
.page-heading::after {
    content: "";
    position: absolute;
    right: -28px;
    top: -65px;
    width: 190px;
    height: 190px;
    border: 1px solid rgba(106,167,255,.17);
    border-radius: 50%;
    box-shadow: 0 0 0 18px rgba(103,123,255,.025), 0 0 0 37px rgba(103,123,255,.018);
    pointer-events: none;
}
.page-heading > * { position: relative; z-index: 1; }

/* Bento cards get a slow energy trace along the rim. */
.nexus-bento-card {
    transform-style: preserve-3d;
}
.nexus-bento-card::after {
    top: 0;
    left: -75%;
    right: auto;
    width: 55%;
    height: 1px;
    opacity: .8;
    background: linear-gradient(90deg, transparent, rgba(115,237,255,.78), rgba(165,137,255,.62), transparent);
    animation: bentoEnergyTrace 9s ease-in-out infinite;
}
.nexus-bento-card:nth-child(2)::after { animation-delay: -2s; }
.nexus-bento-card:nth-child(3)::after { animation-delay: -4s; }
.nexus-bento-card:nth-child(4)::after { animation-delay: -6s; }
@keyframes bentoEnergyTrace {
    0%, 15% { left: -75%; opacity: 0; }
    30% { opacity: .8; }
    63%, 100% { left: 125%; opacity: 0; }
}
.nexus-bento-card:hover .bento-icon {
    color: #EDFDFF;
    border-color: rgba(113,239,255,.65);
    box-shadow: 0 0 24px rgba(88,219,255,.18);
    transform: translateY(-2px) rotate(-3deg);
}
.bento-icon { transition: transform .25s ease, box-shadow .25s ease, border-color .25s ease; }
.nexus-mini-terminal {
    overflow: hidden;
}
.nexus-mini-terminal::after {
    content: "";
    display: block;
    height: 2px;
    width: 45%;
    margin-top: 12px;
    border-radius: 99px;
    background: linear-gradient(90deg, #9B8CFF, #6CEBFF, transparent);
    box-shadow: 0 0 14px rgba(108,235,255,.27);
    animation: terminalSignal 5.5s ease-in-out infinite;
}
@keyframes terminalSignal {
    0%, 100% { transform: translateX(-10%); opacity: .5; }
    50% { transform: translateX(125%); opacity: 1; }
}

/* Upgrade all Streamlit tab bars, including Dashboard tabs. */
div[data-testid="stTabs"] div[role="tablist"] {
    gap: 7px;
    padding: 6px;
    border-radius: 16px;
    border: 1px solid rgba(117,142,233,.19);
    background: rgba(7,14,32,.66);
    box-shadow: inset 0 1px 0 rgba(255,255,255,.025);
}
div[data-testid="stTabs"] button[role="tab"] {
    position: relative;
    border-radius: 11px;
    padding: 10px 13px;
    color: #92A7D5;
    font-size: 12px;
    font-weight: 750;
    transition: background .2s ease, color .2s ease, box-shadow .2s ease;
}
div[data-testid="stTabs"] button[role="tab"]:hover {
    color: #EAF3FF;
    background: rgba(87,111,202,.12);
}
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #F4F7FF;
    background: linear-gradient(105deg, rgba(116,83,255,.23), rgba(41,159,226,.13));
    box-shadow: inset 0 0 0 1px rgba(135,162,255,.23), 0 4px 14px rgba(0,0,0,.12);
}
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"]::after {
    content: "";
    position: absolute;
    left: 22%;
    right: 22%;
    bottom: 0;
    height: 2px;
    border-radius: 99px;
    background: linear-gradient(90deg, #A18EFF, #64EAFF);
    box-shadow: 0 0 10px rgba(100,234,255,.3);
}

/* Expanders become layered HUD accordions rather than plain boxes. */
div[data-testid="stExpander"] {
    overflow: hidden;
    border: 1px solid rgba(118,143,230,.24) !important;
    border-radius: 15px !important;
    background: linear-gradient(115deg, rgba(15,26,54,.67), rgba(9,18,39,.63)) !important;
    transition: border-color .22s ease, box-shadow .22s ease;
}
div[data-testid="stExpander"]:hover {
    border-color: rgba(100,206,255,.39) !important;
    box-shadow: 0 8px 22px rgba(0,0,0,.12);
}
div[data-testid="stExpander"] details summary {
    padding-top: 10px;
    padding-bottom: 10px;
}
div[data-testid="stExpander"] details[open] summary {
    border-bottom: 1px solid rgba(112,139,224,.16);
    background: rgba(63,82,154,.07);
}

/* Selects, forms and uploaded files get matching borders and focus states. */
div[data-baseweb="select"] > div {
    border-color: rgba(109,133,218,.35) !important;
    border-radius: 12px !important;
    background: rgba(8,17,38,.83) !important;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: rgba(96,223,255,.72) !important;
    box-shadow: 0 0 0 3px rgba(96,223,255,.065) !important;
}
div[data-testid="stForm"] {
    padding: 15px;
    border: 1px solid rgba(113,139,228,.20);
    border-radius: 17px;
    background: linear-gradient(135deg, rgba(17,29,60,.50), rgba(7,15,33,.46));
}
div[data-testid="stFileUploader"] section {
    border-radius: 12px;
}
div[data-testid="stFileUploader"] button {
    border: 1px solid rgba(108,151,255,.30) !important;
    border-radius: 9px !important;
}

/* Result cards are a little more editorial and high-contrast. */
div[class*="st-key-result-card-"] {
    position: relative;
    overflow: hidden;
    margin: 10px 0;
    padding: 5px 17px 12px;
    border: 1px solid rgba(119,145,234,.23);
    border-radius: 15px;
    background: linear-gradient(105deg, rgba(19,31,65,.78), rgba(8,18,39,.78));
    box-shadow: inset 0 1px 0 rgba(255,255,255,.03);
}
div[class*="st-key-result-card-"]::before {
    content: "";
    position: absolute;
    left: 0; top: 14px; bottom: 14px;
    width: 2px;
    border-radius: 99px;
    background: linear-gradient(180deg, #A08BFF, #63E6FF);
    box-shadow: 0 0 12px rgba(99,230,255,.23);
}
div[class*="st-key-result-card-"] h4 {
    color: #E7F0FF !important;
    letter-spacing: -.025em;
}
div[class*="st-key-result-card-"] p,
div[class*="st-key-result-card-"] li {
    color: #B5C4E4 !important;
    line-height: 1.75;
}

/* More intentional focus rings for keyboard users. */
button:focus-visible, input:focus-visible, textarea:focus-visible {
    outline: 2px solid rgba(104,226,255,.8) !important;
    outline-offset: 3px !important;
}
@media (max-width: 620px) {
    div[data-testid="stTabs"] div[role="tablist"] { gap: 3px; padding: 4px; }
    div[data-testid="stTabs"] button[role="tab"] { padding: 8px 9px; font-size: 10px; }
    .page-heading { padding: 19px 17px; border-radius: 18px; }
    .page-heading::after { width: 130px; height: 130px; top: -45px; right: -35px; }
    div[data-testid="stForm"] { padding: 11px; }
}
@media (prefers-reduced-motion: reduce) {
    .stApp::after, .nexus-bento-card::after, .nexus-mini-terminal::after {
        animation: none !important;
    }
}



/* =========================================================
   SITE-WIDE 3D ENVIRONMENT — PERSPECTIVE FLOOR + HOLOGRAPHIC OBJECTS
   CSS-only background effect. No content or feature logic changes.
   ========================================================= */

/* Turn the existing floor into a deeper, moving perspective grid. */
.stApp::before {
    left: -8% !important;
    bottom: -43% !important;
    width: 116% !important;
    height: 86% !important;
    z-index: 0 !important;
    transform: perspective(460px) rotateX(62deg) scale(1.08) !important;
    transform-origin: center bottom !important;
    background-image:
        linear-gradient(rgba(89, 142, 255, .34) 1px, transparent 1px),
        linear-gradient(90deg, rgba(89, 142, 255, .34) 1px, transparent 1px),
        radial-gradient(ellipse at 50% 0%, rgba(76, 198, 255, .14), transparent 64%) !important;
    background-size: 54px 54px, 54px 54px, 100% 100% !important;
    background-position: 0 0, 0 0, center !important;
    background-repeat: repeat, repeat, no-repeat !important;
    opacity: .58 !important;
    filter: drop-shadow(0 0 18px rgba(78, 111, 255, .18));
    mask-image: linear-gradient(to top, rgba(0,0,0,.98) 3%, rgba(0,0,0,.72) 52%, transparent 94%) !important;
    animation: noticeBuddy3DFloorTravel 18s linear infinite !important;
}
@keyframes noticeBuddy3DFloorTravel {
    from { background-position: 0 0, 0 0, center; }
    to { background-position: 0 270px, 0 270px, center; }
}

/* Holographic wireframe globe floating on the right side of every page. */
.stAppViewContainer::before {
    content: "";
    position: fixed;
    z-index: 0;
    top: 12vh;
    right: -150px;
    width: clamp(260px, 36vw, 520px);
    aspect-ratio: 1;
    border: 1px solid rgba(115, 164, 255, .18);
    border-radius: 50%;
    pointer-events: none;
    background:
        radial-gradient(ellipse 29% 50% at 50% 50%, transparent 96%, rgba(95, 221, 255, .32) 98%, transparent 100%),
        radial-gradient(ellipse 50% 27% at 50% 50%, transparent 96%, rgba(157, 117, 255, .36) 98%, transparent 100%),
        radial-gradient(ellipse 18% 50% at 50% 50%, transparent 96%, rgba(95, 221, 255, .30) 98%, transparent 100%),
        radial-gradient(ellipse 39% 50% at 50% 50%, transparent 96%, rgba(120, 135, 255, .25) 98%, transparent 100%),
        repeating-radial-gradient(circle at 50% 50%, transparent 0 42px, rgba(100, 143, 255, .11) 43px, transparent 44px 66px),
        radial-gradient(circle at 34% 29%, rgba(75, 144, 255, .12), rgba(114, 63, 255, .035) 46%, transparent 72%);
    box-shadow:
        inset 0 0 62px rgba(95, 112, 255, .09),
        0 0 70px rgba(72, 130, 255, .08),
        0 0 0 26px rgba(91, 120, 255, .016),
        0 0 0 55px rgba(91, 120, 255, .012);
    transform: perspective(900px) rotateY(-28deg) rotateX(12deg);
    transform-style: preserve-3d;
    opacity: .58;
    filter: drop-shadow(0 0 14px rgba(89, 126, 255, .12));
    animation: noticeBuddy3DGlobe 22s ease-in-out infinite alternate;
}
@keyframes noticeBuddy3DGlobe {
    0% { transform: perspective(900px) rotateY(-31deg) rotateX(12deg) translate3d(0,0,0); }
    50% { transform: perspective(900px) rotateY(-20deg) rotateX(18deg) translate3d(-17px,18px,0); }
    100% { transform: perspective(900px) rotateY(-34deg) rotateX(8deg) translate3d(8px,-12px,0); }
}

/* Second wireframe plane creates a foreground/background depth cue. */
.stAppViewContainer::after {
    content: "";
    position: fixed;
    z-index: 0;
    left: -190px;
    bottom: -125px;
    width: clamp(370px, 48vw, 680px);
    height: clamp(250px, 35vw, 470px);
    border: 1px solid rgba(85, 205, 255, .15);
    border-radius: 34%;
    pointer-events: none;
    transform: perspective(720px) rotateX(61deg) rotateZ(-24deg);
    transform-origin: center center;
    background:
        linear-gradient(90deg, rgba(90, 194, 255, .07) 1px, transparent 1px),
        linear-gradient(rgba(90, 194, 255, .07) 1px, transparent 1px),
        radial-gradient(ellipse at 55% 40%, rgba(44, 104, 255, .09), transparent 65%);
    background-size: 38px 38px, 38px 38px, 100% 100%;
    box-shadow:
        inset 0 0 55px rgba(63, 147, 255, .045),
        0 0 45px rgba(65, 169, 255, .045);
    opacity: .52;
    animation: noticeBuddy3DPlane 19s ease-in-out infinite alternate;
}
@keyframes noticeBuddy3DPlane {
    from { transform: perspective(720px) rotateX(61deg) rotateZ(-24deg) translate3d(0,0,0); }
    to { transform: perspective(720px) rotateX(56deg) rotateZ(-19deg) translate3d(20px,-10px,0); }
}

/* Keep the real app content above the decorative 3D environment. */
div[data-testid="stMain"],
div[data-testid="stMainBlockContainer"],
header[data-testid="stHeader"] {
    position: relative !important;
    z-index: 2 !important;
    background: transparent !important;
}
div[data-testid="stSidebar"] {
    position: relative !important;
    z-index: 3 !important;
}
.stAppViewContainer {
    isolation: isolate;
}

/* Additional atmospheric light behind cards for depth. */
.nexus-bento-grid,
.nexus-process-rail,
.workspace-card,
.page-heading {
    position: relative;
    z-index: 2;
}
@media (max-width: 760px) {
    .stAppViewContainer::before {
        width: 290px;
        right: -190px;
        top: 17vh;
        opacity: .28;
    }
    .stAppViewContainer::after {
        width: 360px;
        height: 250px;
        left: -210px;
        bottom: -110px;
        opacity: .26;
    }
    .stApp::before {
        opacity: .30 !important;
        bottom: -48% !important;
    }
}
@media (prefers-reduced-motion: reduce) {
    .stApp::before,
    .stAppViewContainer::before,
    .stAppViewContainer::after {
        animation: none !important;
    }
}


/* =========================================================
   NOTICEBUDDY — ATELIER REDESIGN
   Warm ivory, ink navy, and electric blue. Visual-only layer.
   Keeps the existing app logic and navigation untouched.
   ========================================================= */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --nb-bg: #F5F7FB;
    --nb-paper: #FFFFFF;
    --nb-paper-soft: #F9FAFD;
    --nb-ink: #17243A;
    --nb-muted: #68768B;
    --nb-blue: #315CF5;
    --nb-blue-deep: #2145D8;
    --nb-cyan: #55BDEB;
    --nb-line: #E2E8F2;
    --nb-shadow: 0 16px 42px rgba(30, 52, 94, .075);
}
html, body, [class*="css"] { font-family: "DM Sans", "Manrope", sans-serif !important; }
.stApp {
    color: var(--nb-ink) !important;
    background-color: var(--nb-bg) !important;
    background-image:
        radial-gradient(ellipse at 88% 6%, rgba(83, 132, 255, .115), transparent 32%),
        radial-gradient(ellipse at 4% 48%, rgba(107, 198, 235, .10), transparent 32%),
        linear-gradient(180deg, #FAFBFE 0%, #F3F6FB 100%) !important;
    background-attachment: fixed !important;
}
.stApp::before {
    left: -8% !important;
    bottom: -48% !important;
    width: 116% !important;
    height: 74% !important;
    background-image:
        linear-gradient(rgba(66, 104, 206, .07) 1px, transparent 1px),
        linear-gradient(90deg, rgba(66, 104, 206, .07) 1px, transparent 1px) !important;
    background-size: 62px 62px !important;
    transform: perspective(520px) rotateX(62deg) !important;
    opacity: .26 !important;
    filter: none !important;
    mask-image: linear-gradient(to top, rgba(0,0,0,.7), transparent 88%) !important;
    animation: none !important;
}
.stApp::after {
    background: radial-gradient(circle, rgba(78, 137, 255, .11), rgba(84, 189, 235, .055) 42%, transparent 72%) !important;
    filter: blur(28px) !important;
    opacity: .8 !important;
    animation: none !important;
}
.stAppViewContainer::before {
    right: -220px !important;
    top: 7vh !important;
    opacity: .14 !important;
    border-color: rgba(75, 121, 226, .17) !important;
    filter: none !important;
    box-shadow: 0 0 0 26px rgba(91,120,255,.012) !important;
    animation-duration: 32s !important;
}
.stAppViewContainer::after {
    opacity: .12 !important;
    border-color: rgba(63, 156, 210, .15) !important;
    filter: none !important;
    animation-duration: 30s !important;
}
.stAppViewContainer, div[data-testid="stMain"], div[data-testid="stMainBlockContainer"],
.main, header[data-testid="stHeader"] {
    background: transparent !important;
}
.block-container {
    max-width: 1320px !important;
    padding-top: 1.6rem !important;
    padding-bottom: 3.2rem !important;
}
h1, h2, h3, h4, h5, h6, p, label, li,
div[data-testid="stMarkdownContainer"], div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] li, div[data-testid="stWidgetLabel"] p {
    color: var(--nb-ink) !important;
    text-shadow: none !important;
}
h1, h2, h3, h4 { letter-spacing: -.035em !important; }
h1 { font-weight: 800 !important; }
h2 { font-weight: 750 !important; }
p, li { line-height: 1.72; }
a { color: var(--nb-blue) !important; }
hr {
    border-color: var(--nb-line) !important;
    border-image: none !important;
}
.small-note, .metric-label, .workspace-copy, .home-section-subtitle,
.nexus-section-head > p, .nexus-process-head > p {
    color: var(--nb-muted) !important;
}

/* Navigation and sidebar */
section[data-testid="stSidebar"], div[data-testid="stSidebar"] {
    background: rgba(255,255,255,.93) !important;
    border-right: 1px solid var(--nb-line) !important;
    box-shadow: 8px 0 30px rgba(25, 45, 83, .035) !important;
    backdrop-filter: blur(18px);
}
div[data-testid="stSidebar"] * { color: #34425A !important; }
div[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #64738B !important;
}
div[data-testid="stSidebar"] div[role="radiogroup"] label {
    border: 1px solid transparent !important;
    border-radius: 13px !important;
    padding: 9px 11px !important;
    transition: background .2s ease, border-color .2s ease, transform .2s ease !important;
}
div[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: #F2F5FF !important;
    border-color: #E0E7FF !important;
    transform: translateX(2px);
}
div[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(100deg, #EAF0FF, #F2F7FF) !important;
    border-color: #D9E3FF !important;
    box-shadow: inset 3px 0 0 var(--nb-blue), 0 5px 16px rgba(49,92,245,.055) !important;
}
div[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {
    color: var(--nb-blue-deep) !important;
    font-weight: 800 !important;
}
.top-nav {
    background: rgba(255,255,255,.88) !important;
    border: 1px solid rgba(222,230,242,.9) !important;
    box-shadow: 0 8px 30px rgba(35,55,95,.055) !important;
    backdrop-filter: blur(18px) !important;
}
.top-nav-brand, .top-nav-wordmark { color: var(--nb-ink) !important; }
.top-nav-logo {
    background: linear-gradient(135deg, #315CF5, #53B8EE) !important;
    box-shadow: 0 7px 18px rgba(49,92,245,.22) !important;
}
.nav-status, .nav-journey {
    color: #5D6C83 !important;
    background: #F4F7FC !important;
    border-color: #E2E8F2 !important;
}
.nav-status i, .nav-journey i { color: var(--nb-blue) !important; }

/* Main hero: airy editorial layout instead of dark sci-fi glass */
.hero, .hero.hero-ultimate {
    color: var(--nb-ink) !important;
    background:
        radial-gradient(ellipse at 92% 12%, rgba(88,145,255,.13), transparent 34%),
        radial-gradient(ellipse at 0% 100%, rgba(81,190,227,.10), transparent 44%),
        linear-gradient(125deg, rgba(255,255,255,.99), rgba(248,250,255,.98)) !important;
    border: 1px solid #DDE6F5 !important;
    border-radius: 30px !important;
    box-shadow: 0 24px 65px rgba(40,66,120,.085), inset 0 1px 0 #fff !important;
    padding: clamp(24px, 4vw, 48px) !important;
}
.hero::before {
    border-color: rgba(66, 111, 221, .13) !important;
    box-shadow: 0 0 0 20px rgba(66,111,221,.025), 0 0 0 46px rgba(66,111,221,.018) !important;
    opacity: .7 !important;
}
.hero::after {
    background: radial-gradient(circle at 30% 30%, rgba(185,214,255,.75), rgba(84,145,255,.20) 45%, transparent 73%) !important;
    box-shadow: none !important;
    filter: blur(12px) !important;
    opacity: .45 !important;
}
.hero > *, .hero .hero-content, .hero .hero-copy { z-index: 2 !important; }
.hero .hero-live-pill, .hero .eyebrow, .hero .hero-tag-row span {
    color: #3655AE !important;
    background: #EEF3FF !important;
    border-color: #DCE6FF !important;
    box-shadow: none !important;
}
.hero .hero-live-dot { background: #20B984 !important; box-shadow: 0 0 0 4px rgba(32,185,132,.12) !important; }
.hero h1, .hero.hero-ultimate h1, .hero .hero-title-gradient {
    color: #14233D !important;
    background: linear-gradient(100deg, #14233D 0%, #315CF5 58%, #168DBA 100%) !important;
    background-clip: text !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    text-shadow: none !important;
    letter-spacing: -.055em !important;
    animation: none !important;
}
.hero p, .hero .hero-copy > p { color: #5E6D83 !important; }
.hero .creator-byline, .hero .creator-byline b { color: #738099 !important; }
.hero .hero-bottom-ribbon {
    background: rgba(246,249,255,.88) !important;
    border-color: #E1E8F4 !important;
}
.hero .hero-bottom-ribbon > span, .hero .ribbon-label { color: #65748B !important; }
.hero .hero-orbit-outer, .hero .hero-orbit-inner { border-color: rgba(62,104,221,.22) !important; box-shadow: none !important; }
.hero .hero-orbit-core { box-shadow: 0 10px 30px rgba(49,92,245,.20) !important; }
.hero .hero-hud, .hero .hero-hud-top, .hero .hero-hud-bottom {
    background: rgba(255,255,255,.85) !important;
    border-color: #DEE7F5 !important;
    box-shadow: 0 10px 30px rgba(36,58,98,.08) !important;
    color: #53647C !important;
}
.hero .hero-hud b, .hero .hero-hud small { color: #34435C !important; }

/* Section headings and callout strips */
.nexus-section-kicker, .nexus-section-kicker > span {
    color: #4162C9 !important;
    letter-spacing: .14em !important;
}
.nexus-section-kicker > i { color: #3E74E8 !important; }
.nexus-section-title { color: #17243A !important; }
.nexus-section-title b, .nexus-process-head h2 b {
    color: #315CF5 !important;
    background: none !important;
    -webkit-text-fill-color: #315CF5 !important;
}
.nexus-signal-strip {
    background: rgba(255,255,255,.8) !important;
    border: 1px solid #E0E7F2 !important;
    box-shadow: 0 10px 25px rgba(31,55,98,.04) !important;
}
.nexus-signal-brand, .nexus-signal-item, .nexus-signal-tail { color: #586981 !important; }
.nexus-signal-brand b { color: #1E2E47 !important; }
.nexus-signal-item i, .nexus-signal-arrow { color: #315CF5 !important; }
.home-hero-manifesto { color: #53647C !important; }
.manifesto-kicker { color: #315CF5 !important; }
.home-hero-manifesto b { color: #17243A !important; }

/* Cards: flat premium surfaces, clear hierarchy, subtle blue lifts */
.metric, .panel, .workspace-card, .voice-studio-card, .voice-context-card,
.deadline-row, .calendar-cell, .voice-message-card, .home-feature-card,
.workflow-home-step, .process-node, .nexus-bento-card, .ai-activity-card {
    color: var(--nb-ink) !important;
    background: #FFFFFF !important;
    border: 1px solid #E1E7F0 !important;
    border-radius: 20px !important;
    box-shadow: 0 10px 30px rgba(34,55,91,.045) !important;
}
.panel, .workspace-card, .voice-studio-card, .voice-context-card { padding: 22px !important; }
.metric {
    position: relative !important;
    overflow: hidden !important;
    box-shadow: 0 10px 28px rgba(34,55,91,.05), inset 0 1px 0 #fff !important;
}
.metric::before {
    height: 3px !important;
    background: linear-gradient(90deg, #315CF5, #54BDEB) !important;
    box-shadow: none !important;
}
.metric::after { border-color: rgba(49,92,245,.13) !important; box-shadow: none !important; }
.metric:hover, .panel:hover, .workspace-card:hover, .nexus-bento-card:hover,
.home-feature-card:hover, .process-node:hover {
    border-color: #C8D6FB !important;
    box-shadow: 0 20px 42px rgba(49,92,245,.10) !important;
    transform: translateY(-3px) !important;
}
.metric-label, .metric-label * { color: #748197 !important; letter-spacing: .11em !important; }
.metric-value, .metric-value * { color: #17243A !important; text-shadow: none !important; }
.workspace-kicker, .bento-overline, .page-chip { color: #4766C7 !important; }
.workspace-title, .workspace-card h2, .workspace-card h3 { color: #182943 !important; }
.workspace-copy { color: #69788D !important; }
.page-heading {
    background: linear-gradient(120deg, #FFFFFF, #F3F7FF) !important;
    border: 1px solid #E0E8F5 !important;
    border-radius: 23px !important;
    box-shadow: var(--nb-shadow) !important;
}
.page-heading h1, .page-heading h2, .page-heading h3 { color: #17243A !important; }
.page-heading p, .page-heading .page-chip { color: #60718A !important; }
.nexus-bento-card {
    min-height: 265px !important;
    background: linear-gradient(145deg, #FFFFFF, #F8FAFF) !important;
    border-color: #E0E7F1 !important;
}
.nexus-bento-card::before {
    background: linear-gradient(90deg, #315CF5, #65C6EB) !important;
    opacity: .75 !important;
}
.nexus-bento-card::after { opacity: .12 !important; }
.nexus-bento-card h3, .nexus-bento-card h3 em { color: #182943 !important; }
.nexus-bento-card p { color: #6B7890 !important; }
.bento-icon, .feature-icon {
    background: #EEF3FF !important;
    color: #315CF5 !important;
    border-color: #DCE6FF !important;
    box-shadow: none !important;
}
.bento-index, .bento-corner { color: #9AA7BA !important; }
.nexus-mini-terminal {
    background: #F7F9FD !important;
    border: 1px solid #DFE7F3 !important;
    box-shadow: 0 10px 24px rgba(39,61,100,.045) !important;
}
.terminal-top { background: #EEF2F8 !important; border-color: #E1E7F0 !important; }
.terminal-rule, .terminal-scan { background: #E3EAF4 !important; }
.terminal-result { background: #ECF8F2 !important; border-color: #D7F0E4 !important; }
.terminal-result small, .terminal-result b { color: #2B775B !important; }
.bento-voice-orb { filter: saturate(.8); }
.bento-calendar-preview, .bento-stack { filter: saturate(.8); }
.nexus-process-rail { gap: 12px !important; }
.process-node { background: rgba(255,255,255,.93) !important; border-radius: 18px !important; }
.process-node-top, .process-node > b { color: #2A3D5A !important; }
.process-node > p { color: #6B7890 !important; }
.process-connector span { background: #A7BDF8 !important; box-shadow: none !important; }

/* Unified buttons and controls */
.stButton > button, .stDownloadButton > button, button[kind="primary"] {
    color: #FFFFFF !important;
    background: linear-gradient(110deg, #315CF5, #397EF7) !important;
    border: 1px solid rgba(40,82,222,.15) !important;
    border-radius: 13px !important;
    font-weight: 750 !important;
    min-height: 44px !important;
    box-shadow: 0 7px 16px rgba(49,92,245,.17) !important;
    transition: transform .18s ease, box-shadow .18s ease, filter .18s ease !important;
}
.stButton > button p, .stDownloadButton > button p { color: #FFFFFF !important; }
.stButton > button:hover, .stDownloadButton > button:hover, button[kind="primary"]:hover {
    color: #FFFFFF !important;
    transform: translateY(-2px) !important;
    filter: brightness(1.035) !important;
    box-shadow: 0 12px 24px rgba(49,92,245,.22) !important;
}
.stButton > button:focus, .stDownloadButton > button:focus { box-shadow: 0 0 0 3px rgba(49,92,245,.15) !important; }
.stButton > button[kind="secondary"], button[kind="secondary"] {
    color: #34445E !important;
    background: #FFFFFF !important;
    border: 1px solid #DCE4F0 !important;
    box-shadow: 0 3px 9px rgba(34,55,91,.035) !important;
}
.stButton > button[kind="secondary"] p { color: #34445E !important; }
input, textarea, select,
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stTextArea"] textarea {
    color: #1E2C44 !important;
    background: #FFFFFF !important;
    border: 1px solid #D9E2EF !important;
    border-radius: 12px !important;
    box-shadow: none !important;
}
div[data-testid="stTextArea"] textarea { min-height: 125px; }
input::placeholder, textarea::placeholder { color: #9AA6B8 !important; }
div[data-baseweb="select"] > div, div[data-testid="stSelectbox"] > div > div {
    color: #263650 !important;
    background: #FFFFFF !important;
    border-color: #D9E2EF !important;
    border-radius: 12px !important;
}
div[data-baseweb="select"] * { color: #263650 !important; }
div[role="listbox"], ul[role="listbox"] {
    background: #FFFFFF !important;
    border: 1px solid #E0E7F1 !important;
    box-shadow: 0 14px 35px rgba(24,43,78,.12) !important;
}
div[role="option"] { color: #273750 !important; }
div[role="option"]:hover, div[role="option"][aria-selected="true"] { background: #EEF3FF !important; }
div[data-testid="stFileUploader"] {
    background: #F9FBFF !important;
    border: 1.5px dashed #B9C9F1 !important;
    border-radius: 18px !important;
    padding: 14px !important;
    box-shadow: inset 0 0 0 4px rgba(49,92,245,.018) !important;
}
div[data-testid="stFileUploader"] section {
    background: transparent !important;
    border-radius: 13px !important;
}
div[data-testid="stFileUploader"] small,
div[data-testid="stFileUploader"] span,
div[data-testid="stFileUploader"] p { color: #62728B !important; }
div[data-testid="stFileUploader"] button {
    color: #315CF5 !important;
    background: #EEF3FF !important;
    border: 1px solid #DCE6FF !important;
    box-shadow: none !important;
}
div[data-testid="stFileUploader"] button p { color: #315CF5 !important; }
div[data-testid="stCheckbox"] label, div[data-testid="stRadio"] label { color: #34445E !important; }
div[data-testid="stSlider"] * { color: #34445E !important; }
div[data-testid="stForm"] {
    padding: 17px !important;
    border: 1px solid #E1E7F0 !important;
    border-radius: 18px !important;
    background: #FFFFFF !important;
    box-shadow: 0 8px 24px rgba(34,55,91,.04) !important;
}

/* Tabs, accordions, alerts and outputs */
div[data-testid="stTabs"] div[role="tablist"] {
    gap: 6px !important;
    padding: 5px !important;
    border: 1px solid #E2E8F2 !important;
    border-radius: 15px !important;
    background: rgba(255,255,255,.78) !important;
}
div[data-testid="stTabs"] button[role="tab"] {
    color: #68778D !important;
    border: 0 !important;
    background: transparent !important;
    border-radius: 10px !important;
    font-size: 13px !important;
}
div[data-testid="stTabs"] button[role="tab"] p { color: inherit !important; }
div[data-testid="stTabs"] button[role="tab"]:hover { color: #315CF5 !important; background: #F2F5FC !important; }
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #315CF5 !important;
    background: #EEF3FF !important;
    box-shadow: inset 0 0 0 1px #DCE6FF !important;
    font-weight: 800 !important;
}
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] p { color: #315CF5 !important; }
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"]::after {
    background: linear-gradient(90deg, #315CF5, #56BDEB) !important;
    box-shadow: none !important;
}
div[data-testid="stExpander"] {
    border: 1px solid #E1E7F0 !important;
    border-radius: 15px !important;
    background: #FFFFFF !important;
    box-shadow: 0 6px 20px rgba(34,55,91,.035) !important;
}
div[data-testid="stExpander"] details summary,
div[data-testid="stExpander"] details[open] summary {
    color: #263650 !important;
    background: #FFFFFF !important;
    border-color: #EAF0F7 !important;
}
div[data-testid="stExpander"] details summary p { color: #263650 !important; }
div[data-testid="stAlert"] {
    border-radius: 14px !important;
    border: 1px solid #DCE6F4 !important;
    box-shadow: none !important;
}
div[data-testid="stAlert"] p { color: #33445E !important; }
div[data-testid="stCode"], pre, code {
    color: #31425D !important;
    background: #F2F5FA !important;
    border-color: #E0E7F1 !important;
    border-radius: 12px !important;
}
div[data-testid="stDataFrame"], div[data-testid="stTable"] {
    border: 1px solid #E1E7F0 !important;
    border-radius: 13px !important;
    overflow: hidden;
}
div[data-testid="stAudio"] { border-radius: 13px !important; }
div[data-testid="stProgress"] > div { background: #E6ECF5 !important; border-radius: 99px !important; }
div[data-testid="stProgress"] > div > div { background: linear-gradient(90deg,#315CF5,#56BDEB) !important; border-radius: 99px !important; }

/* History, schedule and voice cards */
.deadline-date, .deadline-pill { color: #315CF5 !important; }
.deadline-detail, .voice-question-text, .voice-context-text, .voice-message-meta { color: #5F6F86 !important; }
.voice-context-pill { color: #315CF5 !important; background: #EEF3FF !important; border-color: #DCE6FF !important; }
.calendar-title, .calendar-weekday { color: #53647C !important; }
.calendar-cell { background: #FFFFFF !important; color: #30415A !important; border-color: #E2E8F2 !important; }
.calendar-cell.empty { background: transparent !important; border-color: transparent !important; box-shadow: none !important; }
.calendar-cell.normal { background: #FFFFFF !important; }
.calendar-cell:has(.deadline-pill) { border-color: #B9C9F8 !important; background: #F1F5FF !important; }
.workflow-home-step, .home-feature-card { background: linear-gradient(145deg,#FFFFFF,#FAFBFF) !important; }
.workflow-home-step h3, .home-feature-card h3 { color: #1C2B43 !important; }
.workflow-home-step p, .home-feature-card p { color: #69788D !important; }
.site-footer {
    background: rgba(255,255,255,.82) !important;
    border: 1px solid #E1E7F0 !important;
    border-radius: 22px !important;
    color: #66758B !important;
    box-shadow: 0 10px 28px rgba(34,55,91,.04) !important;
}
.site-footer *, .footer-tagline, .footer-maker, .footer-team, .footer-legal { color: #66758B !important; }
.footer-brand { color: #1B2A43 !important; }
.footer-link-pill { background: #F3F6FC !important; border-color: #E2E8F2 !important; color: #4B5C75 !important; }
::-webkit-scrollbar { width: 9px; height: 9px; }
::-webkit-scrollbar-track { background: #F1F4F9; }
::-webkit-scrollbar-thumb { background: #C7D2E4; border-radius: 99px; border: 2px solid #F1F4F9; }
::-webkit-scrollbar-thumb:hover { background: #9DADCA; }
button:focus-visible, input:focus-visible, textarea:focus-visible {
    outline: 2px solid rgba(49,92,245,.62) !important;
    outline-offset: 3px !important;
}
@media (max-width: 760px) {
    .hero, .hero.hero-ultimate { padding: 23px !important; border-radius: 22px !important; }
    .nexus-bento-card { min-height: 230px !important; }
    .stAppViewContainer::before { opacity: .07 !important; }
    .stAppViewContainer::after { opacity: .07 !important; }
    .stApp::before { opacity: .12 !important; }
    div[data-testid="stForm"] { padding: 12px !important; }
}
@media (prefers-reduced-motion: reduce) {
    .stApp::before, .stApp::after, .stAppViewContainer::before,
    .stAppViewContainer::after, .hero::before, .hero::after {
        animation: none !important;
    }
}


/* =========================================================
   RESTORE ORIGINAL NOTICEBUDDY MIDNIGHT NEON PALETTE
   Keep the refreshed layout/spacing; restore the old colours.
   ========================================================= */
:root {
    --nb-bg: #070B19;
    --nb-paper: #141C35;
    --nb-paper-soft: #101831;
    --nb-ink: #F4F6FF;
    --nb-muted: #AAB6D8;
    --nb-blue: #3989FF;
    --nb-blue-deep: #7857F6;
    --nb-cyan: #64EAFF;
    --nb-line: #303B60;
}
.stApp {
    color: #F4F6FF !important;
    background-color: #070B19 !important;
    background-image:
        linear-gradient(rgba(102,122,255,.105) 1px, transparent 1px),
        linear-gradient(90deg, rgba(102,122,255,.105) 1px, transparent 1px),
        radial-gradient(ellipse at 80% 12%, rgba(125,62,255,.24), transparent 34%),
        radial-gradient(ellipse at 10% 54%, rgba(0,180,255,.15), transparent 38%),
        radial-gradient(ellipse at 56% 100%, rgba(87,51,255,.12), transparent 40%),
        linear-gradient(135deg,#070B19 0%,#10162F 48%,#0C1832 100%) !important;
    background-size: 42px 42px,42px 42px,auto,auto,auto,100% 100% !important;
    background-position: center center !important;
    background-attachment: fixed !important;
}
.stApp::before {
    background-image:
        linear-gradient(rgba(103,132,255,.25) 1px,transparent 1px),
        linear-gradient(90deg,rgba(103,132,255,.25) 1px,transparent 1px) !important;
    opacity: .36 !important;
}
.stApp::after {
    background: radial-gradient(circle,rgba(137,83,255,.32),rgba(27,145,255,.11) 42%,transparent 72%) !important;
    opacity: .62 !important;
}
.stAppViewContainer::before {
    opacity: .36 !important;
    border-color: rgba(115,164,255,.18) !important;
    filter: drop-shadow(0 0 14px rgba(89,126,255,.12)) !important;
    box-shadow: inset 0 0 62px rgba(95,112,255,.09),0 0 70px rgba(72,130,255,.08),0 0 0 26px rgba(91,120,255,.016) !important;
}
.stAppViewContainer::after {
    opacity: .32 !important;
    border-color: rgba(85,205,255,.15) !important;
    filter: none !important;
}
.block-container { color: #F4F6FF !important; }
h1,h2,h3,h4,h5,h6,p,label,li,
div[data-testid="stMarkdownContainer"],
div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] li,
div[data-testid="stWidgetLabel"] p,
div[data-testid="stCaptionContainer"], .stMarkdown, .stText {
    color: #F4F6FF !important;
    text-shadow: none !important;
}
a { color: #70B7FF !important; }
.small-note,.metric-label,.workspace-copy,.home-section-subtitle,
.nexus-section-head > p,.nexus-process-head > p {
    color: #AAB6D8 !important;
}
/* Original dark sidebar and neon selected navigation */
section[data-testid="stSidebar"],div[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0A1025,#11122B 58%,#07152A) !important;
    border-right: 1px solid rgba(111,108,255,.40) !important;
    box-shadow: 8px 0 32px rgba(39,28,109,.18) !important;
}
div[data-testid="stSidebar"] * { color: #DFE7FF !important; }
div[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #AAB6D8 !important; }
div[data-testid="stSidebar"] div[role="radiogroup"] label {
    border-color: transparent !important;
    background: transparent !important;
}
div[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(90,111,210,.13) !important;
    border-color: rgba(118,143,230,.20) !important;
}
div[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(100deg,rgba(116,83,255,.23),rgba(41,159,226,.13)) !important;
    border-color: rgba(135,162,255,.23) !important;
    box-shadow: inset 3px 0 0 #8B7BFF,0 5px 18px rgba(0,0,0,.12) !important;
}
div[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {
    color: #F4F6FF !important;
}
/* Restore the purple-blue glass hero while keeping updated spacing */
.top-nav {
    background: rgba(8,15,34,.86) !important;
    border-color: rgba(90,112,183,.32) !important;
    box-shadow: 0 8px 30px rgba(0,0,0,.15) !important;
}
.top-nav-brand,.top-nav-wordmark { color: #F4F6FF !important; }
.nav-status,.nav-journey {
    color: #AAB6D8 !important;
    background: rgba(17,29,60,.68) !important;
    border-color: rgba(103,129,203,.32) !important;
}
.nav-status i,.nav-journey i { color: #64EAFF !important; }
.hero,.hero.hero-ultimate {
    color: #F4F6FF !important;
    background:
        radial-gradient(ellipse at 88% 30%,rgba(148,74,255,.34),transparent 32%),
        radial-gradient(ellipse at 8% 100%,rgba(0,190,255,.18),transparent 44%),
        linear-gradient(118deg,rgba(39,26,94,.98),rgba(13,75,123,.96),rgba(17,22,52,.98)) !important;
    border-color: rgba(143,127,255,.82) !important;
    box-shadow: 0 0 0 1px rgba(76,150,255,.14),0 18px 55px rgba(37,26,124,.40),inset 0 1px 0 rgba(255,255,255,.13) !important;
}
.hero::before {
    border-color: rgba(193,184,255,.38) !important;
    box-shadow: 0 0 0 18px rgba(122,103,255,.05),0 0 0 42px rgba(122,103,255,.035),inset 0 0 35px rgba(112,121,255,.12) !important;
}
.hero::after {
    background: radial-gradient(circle at 30% 30%,#D1C7FF,#8057FF 35%,#238CFF 65%,transparent 75%) !important;
    box-shadow: 0 0 70px #7857FF !important;
    filter: blur(2px) !important;
    opacity: .65 !important;
}
.hero .hero-live-pill,.hero .eyebrow,.hero .hero-tag-row span {
    color: #D6D0FF !important;
    background: rgba(105,81,255,.18) !important;
    border-color: rgba(185,174,255,.50) !important;
    box-shadow: 0 0 22px rgba(120,87,255,.18) !important;
}
.hero .hero-live-dot { background: #48F0B8 !important; box-shadow: 0 0 0 4px rgba(72,240,184,.12) !important; }
.hero h1,.hero.hero-ultimate h1,.hero .hero-title-gradient {
    color: transparent !important;
    background: linear-gradient(100deg,#FFFFFF 0%,#C7C4FF 42%,#76D7FF 82%,#FFFFFF 100%) !important;
    background-size: 220% auto !important;
    background-clip: text !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    text-shadow: 0 0 26px rgba(156,134,255,.22) !important;
    animation: titleShimmer 8s ease-in-out infinite alternate !important;
}
.hero p,.hero .hero-copy > p { color: #D0D8F4 !important; }
.hero .creator-byline,.hero .creator-byline b { color: #B6C5E4 !important; }
.hero .hero-bottom-ribbon {
    background: rgba(7,14,32,.66) !important;
    border-color: rgba(112,139,224,.22) !important;
}
.hero .hero-bottom-ribbon > span,.hero .ribbon-label { color: #B5C4E4 !important; }
.hero .hero-orbit-outer,.hero .hero-orbit-inner { border-color: rgba(155,143,255,.48) !important; }
.hero .hero-orbit-core { box-shadow: 0 10px 35px rgba(94,81,255,.34) !important; }
.hero .hero-hud,.hero .hero-hud-top,.hero .hero-hud-bottom {
    background: rgba(8,15,34,.80) !important;
    border-color: rgba(126,150,225,.33) !important;
    box-shadow: 0 10px 30px rgba(0,0,0,.2) !important;
    color: #B5C4E4 !important;
}
.hero .hero-hud b,.hero .hero-hud small { color: #F0F4FF !important; }
.nexus-section-kicker,.nexus-section-kicker > span { color: #B9AEFF !important; }
.nexus-section-kicker > i { color: #64EAFF !important; }
.nexus-section-title { color: #F4F6FF !important; }
.nexus-section-title b,.nexus-process-head h2 b {
    color: #A99AFF !important;
    background: none !important;
    -webkit-text-fill-color: #A99AFF !important;
}
.nexus-signal-strip {
    background: rgba(11,20,43,.82) !important;
    border-color: rgba(103,129,203,.32) !important;
    box-shadow: 0 10px 25px rgba(0,0,0,.12) !important;
}
.nexus-signal-brand,.nexus-signal-item,.nexus-signal-tail { color: #AAB9DA !important; }
.nexus-signal-brand b { color: #F4F6FF !important; }
.nexus-signal-item i,.nexus-signal-arrow { color: #75CFFF !important; }
.home-hero-manifesto { color: #B5C4E4 !important; }
.manifesto-kicker { color: #A99AFF !important; }
.home-hero-manifesto b { color: #F4F6FF !important; }
/* Dark glass cards, violet/cyan highlights */
.metric,.panel,.workspace-card,.voice-studio-card,.voice-context-card,
.deadline-row,.calendar-cell,.voice-message-card,.home-feature-card,
.workflow-home-step,.process-node,.nexus-bento-card,.ai-activity-card {
    color: #F4F6FF !important;
    background: linear-gradient(145deg,rgba(23,33,65,.97),rgba(9,20,42,.98)) !important;
    border-color: rgba(93,116,183,.55) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.045),0 12px 30px rgba(0,0,0,.20) !important;
}
.metric::before { background: linear-gradient(90deg,#8E61FF,#279BFF,#39E6D1) !important; box-shadow: 0 0 19px rgba(112,104,255,.45) !important; }
.metric::after { border-color: rgba(141,126,255,.26) !important; box-shadow: 0 0 0 12px rgba(107,99,255,.05),0 0 0 24px rgba(107,99,255,.04) !important; }
.metric-label,.metric-label * { color: #ABB8DB !important; }
.metric-value,.metric-value * { color: #FFFFFF !important; text-shadow: 0 0 18px rgba(90,147,255,.18) !important; }
.metric:hover,.panel:hover,.workspace-card:hover,.nexus-bento-card:hover,
.home-feature-card:hover,.process-node:hover {
    border-color: rgba(123,134,255,.84) !important;
    box-shadow: 0 18px 38px rgba(58,70,160,.20) !important;
}
.workspace-kicker,.bento-overline,.page-chip { color: #B9AEFF !important; }
.workspace-title,.workspace-card h2,.workspace-card h3 { color: #F4F6FF !important; }
.workspace-copy { color: #B5C4E4 !important; }
.page-heading {
    background: linear-gradient(125deg,rgba(24,31,65,.97),rgba(11,25,49,.97)) !important;
    border-color: rgba(101,122,202,.40) !important;
    box-shadow: 0 16px 42px rgba(0,0,0,.20),inset 0 1px 0 rgba(255,255,255,.055) !important;
}
.page-heading h1,.page-heading h2,.page-heading h3 { color: #F4F6FF !important; }
.page-heading p,.page-heading .page-chip { color: #B5C4E4 !important; }
.nexus-bento-card {
    background: linear-gradient(145deg,rgba(23,33,65,.97),rgba(9,20,42,.98)) !important;
    border-color: rgba(93,116,183,.55) !important;
}
.nexus-bento-card::before { background: linear-gradient(90deg,#8E61FF,#279BFF,#39E6D1) !important; }
.nexus-bento-card h3,.nexus-bento-card h3 em { color: #F0F4FF !important; }
.nexus-bento-card p { color: #B5C4E4 !important; }
.bento-icon,.feature-icon {
    background: rgba(104,104,255,.14) !important;
    color: #BEB4FF !important;
    border-color: rgba(140,130,255,.28) !important;
    box-shadow: 0 0 20px rgba(99,93,255,.10) !important;
}
.bento-index,.bento-corner { color: #8292B9 !important; }
.nexus-mini-terminal {
    background: rgba(6,14,32,.90) !important;
    border-color: rgba(112,139,224,.24) !important;
    box-shadow: 0 10px 24px rgba(0,0,0,.20) !important;
}
.terminal-top { background: rgba(24,36,68,.9) !important; border-color: rgba(112,139,224,.18) !important; }
.terminal-rule,.terminal-scan { background: rgba(112,139,224,.18) !important; }
.terminal-result { background: rgba(25,89,82,.28) !important; border-color: rgba(75,211,172,.19) !important; }
.terminal-result small,.terminal-result b { color: #79E3C2 !important; }
.process-node { background: rgba(16,28,57,.96) !important; }
.process-node-top,.process-node > b { color: #E8EEFF !important; }
.process-node > p { color: #AAB9DA !important; }
.process-connector span { background: #7E8DFF !important; box-shadow: 0 0 11px rgba(126,141,255,.36) !important; }
/* Button colour matches the original neon identity */
.stButton > button,.stDownloadButton > button,button[kind="primary"] {
    color: #FFFFFF !important;
    background: linear-gradient(105deg,#7857F6 0%,#536BFF 48%,#169CF5 100%) !important;
    border-color: rgba(195,184,255,.35) !important;
    box-shadow: 0 8px 25px rgba(91,83,255,.26),inset 0 1px 0 rgba(255,255,255,.13) !important;
}
.stButton > button p,.stDownloadButton > button p,button[kind="primary"] p { color: #FFFFFF !important; }
.stButton > button:hover,.stDownloadButton > button:hover,button[kind="primary"]:hover {
    color: #FFFFFF !important;
    filter: brightness(1.12) !important;
    box-shadow: 0 12px 34px rgba(91,83,255,.45) !important;
}
.stButton > button[kind="secondary"],button[kind="secondary"] {
    color: #DBE6FF !important;
    background: rgba(17,29,60,.86) !important;
    border-color: rgba(112,139,224,.34) !important;
    box-shadow: none !important;
}
.stButton > button[kind="secondary"] p { color: #DBE6FF !important; }
input,textarea,select,div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,div[data-testid="stTextArea"] textarea {
    color: #F4F6FF !important;
    background: rgba(9,17,37,.96) !important;
    border-color: rgba(84,107,179,.75) !important;
    border-radius: 12px !important;
    box-shadow: inset 0 2px 12px rgba(0,0,0,.20) !important;
}
input::placeholder,textarea::placeholder { color: #8799C0 !important; }
div[data-baseweb="select"] > div,div[data-testid="stSelectbox"] > div > div {
    color: #E7EEFF !important;
    background: rgba(12,22,45,.94) !important;
    border-color: rgba(88,109,179,.72) !important;
}
div[data-baseweb="select"] * { color: #E7EEFF !important; }
div[role="listbox"],ul[role="listbox"] {
    background: #101831 !important;
    border-color: #35446F !important;
    box-shadow: 0 14px 35px rgba(0,0,0,.38) !important;
}
div[role="option"] { color: #E7EEFF !important; }
div[role="option"]:hover,div[role="option"][aria-selected="true"] { background: #26345F !important; }
div[data-testid="stFileUploader"] {
    background: rgba(12,22,45,.88) !important;
    border-color: rgba(115,142,230,.86) !important;
    box-shadow: inset 0 0 25px rgba(67,94,255,.07) !important;
}
div[data-testid="stFileUploader"] section { background: transparent !important; }
div[data-testid="stFileUploader"] small,
div[data-testid="stFileUploader"] span,
div[data-testid="stFileUploader"] p { color: #B5C4E4 !important; }
div[data-testid="stFileUploader"] button {
    color: #DCE5FF !important;
    background: rgba(50,68,130,.46) !important;
    border-color: rgba(108,151,255,.30) !important;
}
div[data-testid="stFileUploader"] button p { color: #DCE5FF !important; }
div[data-testid="stCheckbox"] label,div[data-testid="stRadio"] label,
div[data-testid="stSlider"] * { color: #DCE5FF !important; }
div[data-testid="stForm"] {
    background: linear-gradient(135deg,rgba(17,29,60,.78),rgba(7,15,33,.72)) !important;
    border-color: rgba(113,139,228,.22) !important;
    box-shadow: 0 8px 24px rgba(0,0,0,.14) !important;
}
div[data-testid="stTabs"] div[role="tablist"] {
    background: rgba(8,17,38,.68) !important;
    border-color: rgba(112,139,224,.22) !important;
}
div[data-testid="stTabs"] button[role="tab"] { color: #92A7D5 !important; }
div[data-testid="stTabs"] button[role="tab"] p { color: inherit !important; }
div[data-testid="stTabs"] button[role="tab"]:hover { color: #EAF3FF !important; background: rgba(87,111,202,.12) !important; }
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #F4F7FF !important;
    background: linear-gradient(105deg,rgba(116,83,255,.23),rgba(41,159,226,.13)) !important;
    box-shadow: inset 0 0 0 1px rgba(135,162,255,.23),0 4px 14px rgba(0,0,0,.12) !important;
}
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] p { color: #F4F7FF !important; }
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"]::after {
    background: linear-gradient(90deg,#A18EFF,#64EAFF) !important;
    box-shadow: 0 0 10px rgba(100,234,255,.3) !important;
}
div[data-testid="stExpander"] {
    background: linear-gradient(115deg,rgba(15,26,54,.90),rgba(9,18,39,.88)) !important;
    border-color: rgba(118,143,230,.24) !important;
    box-shadow: none !important;
}
div[data-testid="stExpander"] details summary,
div[data-testid="stExpander"] details[open] summary {
    color: #E7EEFF !important;
    background: transparent !important;
    border-color: rgba(112,139,224,.16) !important;
}
div[data-testid="stExpander"] details summary p { color: #E7EEFF !important; }
div[data-testid="stAlert"] { background: rgba(15,29,57,.9) !important; border-color: rgba(112,139,224,.28) !important; }
div[data-testid="stAlert"] p { color: #DCE6FF !important; }
div[data-testid="stCode"],pre,code {
    color: #DCE6FF !important;
    background: #0D1831 !important;
    border-color: #26385E !important;
    border-radius: 12px !important;
}
div[data-testid="stDataFrame"],div[data-testid="stTable"] { border-color: rgba(112,139,224,.24) !important; }
.deadline-date,.deadline-pill { color: #83A7FF !important; }
.deadline-detail,.voice-question-text,.voice-context-text,.voice-message-meta { color: #B5C4E4 !important; }
.voice-context-pill { color: #C6BEFF !important; background: rgba(105,81,255,.16) !important; border-color: rgba(140,130,255,.28) !important; }
.calendar-title,.calendar-weekday { color: #B8C7E2 !important; }
.calendar-cell { color: #DCE6FF !important; background: rgba(18,29,58,.92) !important; border-color: rgba(112,139,224,.24) !important; }
.calendar-cell.empty { background: transparent !important; border-color: transparent !important; box-shadow: none !important; }
.calendar-cell.normal { background: rgba(18,29,58,.92) !important; }
.calendar-cell:has(.deadline-pill) { border-color: rgba(126,157,255,.6) !important; background: rgba(48,65,128,.48) !important; }
.workflow-home-step,.home-feature-card { background: linear-gradient(145deg,rgba(23,33,65,.97),rgba(9,20,42,.98)) !important; }
.workflow-home-step h3,.home-feature-card h3 { color: #F0F4FF !important; }
.workflow-home-step p,.home-feature-card p { color: #B5C4E4 !important; }
.site-footer {
    background: rgba(7,14,32,.78) !important;
    border-color: rgba(112,139,224,.22) !important;
    color: #B5C4E4 !important;
    box-shadow: 0 10px 28px rgba(0,0,0,.14) !important;
}
.site-footer *,.footer-tagline,.footer-maker,.footer-team,.footer-legal { color: #AAB6D8 !important; }
.footer-brand { color: #F4F6FF !important; }
.footer-link-pill { background: rgba(28,43,78,.8) !important; border-color: rgba(112,139,224,.24) !important; color: #DCE6FF !important; }
::-webkit-scrollbar-track { background: #0A1022 !important; }
::-webkit-scrollbar-thumb { background: #35456D !important; border-color: #0A1022 !important; }
::-webkit-scrollbar-thumb:hover { background: #52679D !important; }
@media (max-width: 760px) {
    .stAppViewContainer::before { opacity: .20 !important; }
    .stAppViewContainer::after { opacity: .17 !important; }
    .stApp::before { opacity: .22 !important; }
}


/* =========================================================
   MOTION PACK — EXTRA MOVING DECORATIONS (8 DISTINCT EFFECTS)
   Purple/blue neon identity retained. Decorative only.
   ========================================================= */

/* 1) Independent orbit accents rotate around the hero robot. */
.hero .hero-orbit-outer::before {
    animation: noticeOrbitArcSpin 17s linear infinite !important;
    transform-origin: center;
}
.hero .hero-orbit-outer::after {
    animation: noticeOrbitArcSpin 26s linear infinite reverse !important;
    transform-origin: center;
}
@keyframes noticeOrbitArcSpin {
    from { transform: rotate(25deg); }
    to { transform: rotate(385deg); }
}

/* 2) The robot glow gently breathes without changing its float motion. */
.hero .hero-robot {
    animation: robotFloat 5s ease-in-out infinite, noticeRobotGlow 4.6s ease-in-out infinite !important;
}
@keyframes noticeRobotGlow {
    0%,100% { filter: drop-shadow(0 0 20px rgba(72,96,255,.27)); }
    50% { filter: drop-shadow(0 0 38px rgba(96,119,255,.58)) drop-shadow(0 0 15px rgba(93,227,255,.20)); }
}

/* 3) A travelling light gradient sweeps over primary actions. */
.stButton > button, .stDownloadButton > button, button[kind="primary"] {
    background-size: 220% 220% !important;
    animation: noticeButtonFlow 7s ease-in-out infinite;
}
@keyframes noticeButtonFlow {
    0%,100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

/* 4) Stat-card halo rings softly pulse like a live status indicator. */
.metric::after {
    animation: noticeMetricPulse 5.5s ease-in-out infinite;
}
.metric:nth-child(2)::after { animation-delay: -1.4s; }
.metric:nth-child(3)::after { animation-delay: -2.8s; }
.metric:nth-child(4)::after { animation-delay: -4.1s; }
@keyframes noticeMetricPulse {
    0%,100% { opacity: .42; transform: scale(.94) rotate(0deg); }
    50% { opacity: .95; transform: scale(1.08) rotate(24deg); }
}

/* 5) Page-header orbital outline turns slowly behind its heading. */
.page-heading::after {
    animation: noticeHeadingOrbit 34s linear infinite;
    transform-origin: center;
}
@keyframes noticeHeadingOrbit {
    from { transform: rotate(0deg) scale(.98); }
    50% { transform: rotate(180deg) scale(1.04); }
    to { transform: rotate(360deg) scale(.98); }
}

/* 6) The top navigation's neon underline continuously sweeps. */
.top-nav::after {
    background-size: 220% 100% !important;
    animation: noticeNavSweep 5.8s ease-in-out infinite;
}
@keyframes noticeNavSweep {
    0%,100% { background-position: -100% center; opacity: .30; }
    50% { background-position: 200% center; opacity: .95; }
}

/* 7) A small light streak glides across the footer edge. */
.site-footer {
    position: relative;
    overflow: hidden;
}
.site-footer::before {
    content: "";
    position: absolute;
    top: 0;
    left: -35%;
    width: 32%;
    height: 2px;
    pointer-events: none;
    background: linear-gradient(90deg, transparent, rgba(103,225,255,.95), rgba(157,112,255,.86), transparent);
    box-shadow: 0 0 16px rgba(92,179,255,.32);
    animation: noticeFooterStreak 8.5s ease-in-out infinite;
}
@keyframes noticeFooterStreak {
    0%,12% { left: -35%; opacity: 0; }
    25% { opacity: .85; }
    82% { opacity: .85; }
    100% { left: 105%; opacity: 0; }
}

/* 8) Online status has a heartbeat pulse. */
.hero .hero-live-dot {
    animation: noticeStatusHeartbeat 2.4s ease-in-out infinite !important;
}
@keyframes noticeStatusHeartbeat {
    0%,100% { transform: scale(1); box-shadow: 0 0 0 3px rgba(72,240,184,.10), 0 0 9px rgba(72,240,184,.25); }
    18% { transform: scale(1.18); box-shadow: 0 0 0 7px rgba(72,240,184,.07), 0 0 17px rgba(72,240,184,.50); }
    34% { transform: scale(1); }
    48% { transform: scale(1.12); }
    62% { transform: scale(1); }
}

/* Extra micro-motion: slow sparkle on the section marker. */
.nexus-section-kicker > i {
    animation: noticeKickerSpark 3.6s ease-in-out infinite;
}
@keyframes noticeKickerSpark {
    0%,100% { opacity: .68; filter: brightness(1); transform: scale(.96); }
    50% { opacity: 1; filter: brightness(1.55); transform: scale(1.12); }
}

/* Keep animations gentle on narrow screens and honor accessibility settings. */
@media (max-width: 760px) {
    .hero .hero-orbit-outer::before,
    .hero .hero-orbit-outer::after { animation-duration: 28s !important; }
    .site-footer::before { animation-duration: 11s; }
}
@media (prefers-reduced-motion: reduce) {
    .hero .hero-orbit-outer::before,
    .hero .hero-orbit-outer::after,
    .hero .hero-robot,
    .stButton > button,
    .stDownloadButton > button,
    button[kind="primary"],
    .metric::after,
    .page-heading::after,
    .top-nav::after,
    .site-footer::before,
    .hero .hero-live-dot,
    .nexus-section-kicker > i {
        animation: none !important;
    }
}


/* =========================================================
   FULL-PAGE 4D CINEMATIC BACKDROP
   Two fixed, multi-depth layers behind all page content:
   drifting aurora, moving star field, and a perspective ribbon.
   ========================================================= */
div[data-testid="stMain"] {
    position: relative !important;
    isolation: isolate !important;
}
div[data-testid="stMain"]::before,
div[data-testid="stMain"]::after {
    content: "";
    position: fixed;
    inset: -12vh -9vw;
    pointer-events: none;
    overflow: hidden;
}
div[data-testid="stMain"]::before {
    z-index: 0;
    opacity: .56;
    mix-blend-mode: screen;
    background-image:
        radial-gradient(ellipse at 18% 28%, rgba(96,57,255,.25), transparent 31%),
        radial-gradient(ellipse at 82% 24%, rgba(0,183,255,.20), transparent 29%),
        radial-gradient(ellipse at 58% 82%, rgba(128,61,255,.19), transparent 34%),
        radial-gradient(circle, rgba(185,202,255,.68) 0 1px, transparent 1.8px),
        radial-gradient(circle, rgba(88,228,255,.54) 0 1.1px, transparent 1.9px),
        radial-gradient(circle, rgba(155,126,255,.48) 0 1px, transparent 2px);
    background-size:
        135% 130%, 125% 145%, 140% 130%,
        73px 81px, 119px 131px, 167px 153px;
    background-position:
        0% 0%, 100% 0%, 50% 100%,
        0 0, 38px 57px, 81px 29px;
    background-repeat: no-repeat, no-repeat, no-repeat, repeat, repeat, repeat;
    transform: perspective(1150px) rotateX(5deg) translateZ(0);
    transform-origin: center center;
    filter: drop-shadow(0 0 24px rgba(82,108,255,.12));
    animation: noticeBuddy4DAurora 34s ease-in-out infinite alternate;
}
@keyframes noticeBuddy4DAurora {
    0% {
        background-position: 0% 0%, 100% 0%, 50% 100%, 0 0, 38px 57px, 81px 29px;
        transform: perspective(1150px) rotateX(5deg) rotateY(-1deg) scale(1);
        filter: hue-rotate(0deg) drop-shadow(0 0 24px rgba(82,108,255,.12));
    }
    50% {
        background-position: 24% 18%, 72% 34%, 28% 68%, 0 95px, 92px 0, 0 76px;
        transform: perspective(1150px) rotateX(1deg) rotateY(2deg) scale(1.035);
        filter: hue-rotate(12deg) drop-shadow(0 0 35px rgba(82,108,255,.18));
    }
    100% {
        background-position: 100% 70%, 0% 100%, 75% 10%, 0 190px, 145px 0, 0 152px;
        transform: perspective(1150px) rotateX(7deg) rotateY(-2deg) scale(1.015);
        filter: hue-rotate(-8deg) drop-shadow(0 0 27px rgba(82,108,255,.14));
    }
}

/* A broad holographic ribbon moves on a different 3D plane and speed. */
div[data-testid="stMain"]::after {
    z-index: 1;
    inset: -28vh -25vw;
    opacity: .31;
    mix-blend-mode: screen;
    background:
        conic-gradient(from 12deg at 48% 48%,
            transparent 0deg,
            rgba(94,79,255,.04) 32deg,
            rgba(92,220,255,.22) 48deg,
            transparent 67deg,
            transparent 122deg,
            rgba(152,85,255,.18) 143deg,
            transparent 161deg,
            transparent 235deg,
            rgba(50,150,255,.14) 255deg,
            transparent 280deg,
            transparent 360deg),
        radial-gradient(ellipse at 50% 50%,
            transparent 22%,
            rgba(92,136,255,.12) 35%,
            transparent 48%,
            rgba(87,222,255,.07) 53%,
            transparent 64%);
    background-size: 100% 100%, 100% 100%;
    mask-image: radial-gradient(ellipse at 50% 48%, #000 5%, rgba(0,0,0,.78) 43%, transparent 76%);
    transform: perspective(950px) rotateX(58deg) rotateZ(-12deg) scale(1.35);
    transform-origin: center center;
    animation: noticeBuddy4DRibbon 27s ease-in-out infinite alternate;
}
@keyframes noticeBuddy4DRibbon {
    0% {
        transform: perspective(950px) rotateX(58deg) rotateZ(-12deg) scale(1.28) translate3d(-2%, 1%, 0);
        background-position: 0% 0%, 15% 20%;
        filter: hue-rotate(0deg);
    }
    50% {
        transform: perspective(950px) rotateX(49deg) rotateZ(4deg) scale(1.48) translate3d(2%, -2%, 0);
        background-position: 65% 35%, 55% 40%;
        filter: hue-rotate(18deg);
    }
    100% {
        transform: perspective(950px) rotateX(62deg) rotateZ(15deg) scale(1.36) translate3d(-1%, 3%, 0);
        background-position: 100% 100%, 85% 75%;
        filter: hue-rotate(-12deg);
    }
}

/* Explicit stacking: moving art stays behind text, forms, and buttons. */
div[data-testid="stMainBlockContainer"] {
    position: relative !important;
    z-index: 2 !important;
}
@media (max-width: 760px) {
    div[data-testid="stMain"]::before {
        opacity: .34;
        background-size: 145% 140%, 140% 145%, 150% 140%, 91px 99px, 137px 151px, 187px 173px;
    }
    div[data-testid="stMain"]::after { opacity: .16; }
}
@media (prefers-reduced-motion: reduce) {
    div[data-testid="stMain"]::before,
    div[data-testid="stMain"]::after {
        animation: none !important;
    }
}


/* =========================================================
   BENTO CARD HEIGHT FIX — REMOVE UNUSED EMPTY SPACE
   The large decoder card should size to its actual content,
   not stretch across two rows with a huge blank lower area.
   ========================================================= */
.nexus-bento-grid {
    grid-template-rows: auto auto !important;
    grid-auto-rows: min-content !important;
    align-items: start !important;
}
.nexus-bento-card {
    height: auto !important;
    min-height: 0 !important;
    align-self: start !important;
}
.bento-ai {
    grid-row: auto !important;
    height: fit-content !important;
    min-height: 0 !important;
    align-self: start !important;
}
.bento-ai .nexus-mini-terminal {
    margin-bottom: 0 !important;
}
@media (max-width: 950px) {
    .nexus-bento-grid {
        grid-template-rows: auto !important;
        grid-auto-rows: min-content !important;
        align-items: start !important;
    }
    .bento-ai {
        grid-row: auto !important;
        height: fit-content !important;
        min-height: 0 !important;
    }
}
@media (max-width: 620px) {
    .nexus-bento-grid { grid-template-rows: auto !important; }
    .nexus-bento-card, .bento-ai {
        height: fit-content !important;
        min-height: 0 !important;
    }
}


/* ACTION CENTER — dedicated workspace components */
.action-hero {
    position: relative; overflow: hidden; isolation: isolate;
    margin: 0 0 22px; padding: clamp(24px,3.2vw,40px);
    border-radius: 26px; border: 1px solid rgba(124,111,255,.44);
    background:
      radial-gradient(ellipse at 86% 12%,rgba(83,204,255,.22),transparent 30%),
      radial-gradient(ellipse at 10% 100%,rgba(126,65,255,.22),transparent 42%),
      linear-gradient(125deg,rgba(34,24,83,.98),rgba(13,51,91,.98),rgba(9,17,40,.98));
    box-shadow: 0 22px 55px rgba(0,0,0,.24),inset 0 1px 0 rgba(255,255,255,.09);
}
.action-hero::after {
    content:"";position:absolute;z-index:-1;width:300px;height:300px;right:-90px;top:-140px;
    border:1px solid rgba(119,220,255,.27);border-radius:50%;
    box-shadow:0 0 0 24px rgba(112,116,255,.05),0 0 0 52px rgba(112,116,255,.03);
    animation:actionHeroOrbit 26s linear infinite;
}
@keyframes actionHeroOrbit { to { transform:rotate(360deg); } }
.action-eyebrow { display:flex;align-items:center;gap:9px;color:#C4BCFF;font-size:9px;font-weight:900;letter-spacing:1.6px; }
.action-eyebrow span { display:inline-block;width:7px;height:7px;border-radius:50%;background:#65F0C6;box-shadow:0 0 14px rgba(101,240,198,.65); }
.action-hero h1 { margin:15px 0 10px;font-size:clamp(31px,4vw,48px);line-height:1.08;letter-spacing:-.05em;color:#F8FAFF !important; }
.action-hero h1 b { background:linear-gradient(95deg,#C3B5FF,#73E6FF);background-clip:text;-webkit-background-clip:text;-webkit-text-fill-color:transparent; }
.action-hero p { max-width:740px;color:#CAD5F1 !important;font-size:14px;line-height:1.8;margin:0; }
.action-hero-footer { display:flex;align-items:center;gap:12px;margin-top:25px;color:#9EB2DA;font-size:8px;font-weight:900;letter-spacing:1.4px; }
.action-hero-footer i { display:block;width:32px;height:1px;background:linear-gradient(90deg,#9E8BFF,#6EEBFF); }
.action-kpi { position:relative;overflow:hidden;padding:17px 18px;border-radius:17px;border:1px solid rgba(117,143,224,.24);background:linear-gradient(145deg,rgba(23,33,65,.96),rgba(9,20,42,.98));box-shadow:inset 0 1px 0 rgba(255,255,255,.04),0 12px 26px rgba(0,0,0,.13);margin-bottom:8px; }
.action-kpi::after { content:"";position:absolute;right:-23px;bottom:-35px;width:88px;height:88px;border:1px solid rgba(140,130,255,.20);border-radius:50%;box-shadow:0 0 0 12px rgba(107,99,255,.04);pointer-events:none; }
.action-kpi-top { display:flex;align-items:center;gap:8px;color:#9FB0D4;font-size:8px;font-weight:900;letter-spacing:1px; }
.action-kpi-top span { display:grid;place-items:center;width:25px;height:25px;border-radius:9px;background:rgba(130,118,255,.15);color:#BCB2FF;font-size:13px; }
.action-kpi strong { display:block;margin-top:9px;color:#F7FAFF;font-size:27px;line-height:1;font-weight:800; }
.action-kpi-green .action-kpi-top span { background:rgba(48,215,166,.12);color:#69E6BE; }
.action-kpi-red .action-kpi-top span { background:rgba(255,101,133,.12);color:#FF90A7; }
.action-progress-label { display:flex;justify-content:space-between;align-items:center;margin:7px 0 3px;color:#ACBBDD;font-size:12px; }
.action-progress-label b { color:#73E4FF;font-size:17px; }
.action-progress-caption { display:flex;flex-direction:column;justify-content:center;min-height:65px;padding-left:12px;border-left:1px solid rgba(120,144,220,.25); }
.action-progress-caption b { color:#EAF1FF;font-size:16px; }
.action-progress-caption span { color:#8FA3CA;font-size:10px; }
.action-section-title { display:flex;align-items:flex-start;gap:13px;margin:29px 0 14px; }
.action-section-title > span { display:grid;place-items:center;width:34px;height:34px;flex:0 0 34px;border:1px solid rgba(133,121,255,.34);border-radius:11px;background:rgba(105,88,255,.13);color:#BDB3FF;font-size:11px;font-weight:900; }
.action-section-title > div { display:flex;flex-direction:column;gap:3px; }
.action-section-title b { color:#F0F4FF;font-size:16px; }
.action-section-title small { color:#93A7CF;font-size:11px;line-height:1.6; }
.action-source-pill { display:flex;align-items:center;gap:12px;margin:12px 0;padding:13px 15px;border:1px solid rgba(115,142,230,.22);border-radius:14px;background:rgba(10,20,42,.76); }
.action-source-pill > span { display:grid;place-items:center;width:34px;height:34px;border-radius:10px;background:rgba(101,120,255,.15);color:#AFA3FF;font-size:16px; }
.action-source-pill > div { min-width:0;display:flex;flex-direction:column;gap:3px;flex:1; }
.action-source-pill small { color:#8FA6D4;font-size:8px;letter-spacing:1.3px;font-weight:900; }
.action-source-pill b { color:#EEF3FF;font-size:12px;overflow-wrap:anywhere; }
.action-source-pill em { color:#78DFFF;font-size:10px;font-style:normal;white-space:nowrap; }
div[class*="st-key-action_task_"] { padding:4px 0;margin:5px 0; }
.action-task-card { padding:11px 13px;border:1px solid rgba(113,138,215,.20);border-radius:13px;background:linear-gradient(110deg,rgba(16,29,58,.89),rgba(9,18,39,.90));min-width:0; }
.action-task-title { color:#EDF3FF;font-size:12px;font-weight:800;line-height:1.55;overflow-wrap:anywhere; }
.action-task-meta { color:#8EA4CC;font-size:9px;margin-top:4px;overflow-wrap:anywhere; }
.action-task-evidence { color:#AEBDE0;font-size:10px;line-height:1.6;margin-top:6px;padding-top:6px;border-top:1px solid rgba(113,138,215,.12);overflow-wrap:anywhere; }
.action-task-card.action-done { background:rgba(23,95,83,.22);border-color:rgba(60,219,173,.22); }
.action-task-card.action-done .action-task-title { color:#8FE8C9;text-decoration:line-through; }
.action-task-status { display:flex;flex-direction:column;align-items:flex-start;gap:7px;min-width:0; }
.action-task-status small { color:#91A5CA;font-size:9px;line-height:1.4; }
.action-priority { display:inline-block;padding:4px 7px;border-radius:99px;font-size:8px;font-weight:900;letter-spacing:.5px; }
.action-priority-high { color:#FF9AAA;background:rgba(255,91,119,.13);border:1px solid rgba(255,91,119,.20); }
.action-priority-normal { color:#BDB1FF;background:rgba(135,113,255,.13);border:1px solid rgba(135,113,255,.20); }
.action-priority-low { color:#83D7FA;background:rgba(51,166,222,.12);border:1px solid rgba(51,166,222,.20); }
.action-board-heading { display:flex;justify-content:space-between;gap:10px;margin:12px 0;color:#C7D5F0;font-size:11px; }
.action-board-heading span { color:#8298C4;font-weight:500; }
.action-empty-state { display:flex;align-items:center;flex-direction:column;text-align:center;padding:35px 22px;margin:10px 0;border:1px dashed rgba(113,138,215,.3);border-radius:20px;background:rgba(9,17,38,.44); }
.action-empty-state > span { display:grid;place-items:center;width:47px;height:47px;margin-bottom:12px;border-radius:15px;background:rgba(76,219,172,.12);color:#66E7BD;font-size:22px; }
.action-empty-state b { color:#EFF4FF;font-size:16px; }
.action-empty-state p { color:#96AACE !important;max-width:560px;font-size:11px;line-height:1.8; }
@media (max-width: 760px) {
    .action-hero { padding:22px 18px;border-radius:20px; }
    .action-hero-footer { gap:6px;font-size:7px;letter-spacing:.6px; }
    .action-hero-footer i { width:16px; }
    .action-section-title b { font-size:14px; }
    .action-source-pill { align-items:flex-start; }
    .action-source-pill em { font-size:9px;white-space:normal; }
    .action-task-card { padding:9px; }
    .action-task-title { font-size:10px; }
    .action-task-meta,.action-task-evidence { font-size:8px; }
    .action-task-status small { font-size:8px; }
}
@media (prefers-reduced-motion: reduce) {
    .action-hero::after { animation:none !important; }
}


/* =====================================================================
   NEBULA DECORATION PASS — VISUALS ONLY
   No Python logic, content, features, or interactions are changed here.
   Palette: midnight navy / violet plasma / electric cyan.
   ===================================================================== */
:root {
    --nb-nebula-violet: #9B83FF;
    --nb-nebula-blue: #4F85FF;
    --nb-nebula-cyan: #67E7FF;
    --nb-nebula-mint: #65F0C6;
    --nb-nebula-edge: rgba(126,145,255,.28);
    --nb-nebula-glass: rgba(10,18,41,.82);
}
html { scroll-behavior: smooth; }
.stApp {
    background-color: #070B19 !important;
    background-image:
        radial-gradient(ellipse at 15% 9%, rgba(91,67,255,.13), transparent 35%),
        radial-gradient(ellipse at 94% 38%, rgba(0,174,255,.09), transparent 34%),
        radial-gradient(ellipse at 48% 95%, rgba(129,57,255,.085), transparent 42%),
        linear-gradient(135deg,#070B19 0%,#0D132B 48%,#09172E 100%) !important;
    background-size: 130% 140%, 120% 130%, 140% 130%, 100% 100% !important;
    animation: nebulaColorDrift 34s ease-in-out infinite alternate;
}
@keyframes nebulaColorDrift {
    0% { background-position: 0% 0%,100% 30%,30% 100%,center; }
    50% { background-position: 35% 12%,70% 55%,60% 72%,center; }
    100% { background-position: 100% 35%,0% 100%,95% 10%,center; }
}
.block-container {
    padding-top: 1.15rem !important;
    padding-bottom: 3.7rem !important;
}
header[data-testid="stHeader"] {
    background: linear-gradient(180deg,rgba(7,11,25,.66),transparent) !important;
}

/* A more cinematic glass top bar with a travelling highlight. */
.top-nav {
    position: relative !important;
    isolation: isolate;
    overflow: hidden !important;
    border-radius: 19px !important;
    border-color: rgba(130,150,255,.38) !important;
    background:
        radial-gradient(ellipse at 0% 0%,rgba(107,86,255,.15),transparent 44%),
        linear-gradient(105deg,rgba(8,15,34,.96),rgba(19,24,57,.91),rgba(7,29,49,.95)) !important;
    box-shadow: 0 16px 42px rgba(0,0,0,.23), inset 0 1px 0 rgba(255,255,255,.08), 0 0 25px rgba(79,101,255,.055) !important;
    transform: translateZ(0);
}
.top-nav::before {
    content: "";
    position: absolute;
    z-index: -1;
    inset: 0;
    pointer-events: none;
    opacity: .46;
    background:
        linear-gradient(90deg,transparent,rgba(106,154,255,.06),transparent),
        repeating-linear-gradient(90deg,transparent 0 42px,rgba(108,154,255,.035) 43px,transparent 44px);
    background-size: 220% 100%,auto;
    animation: nebulaTopGrid 17s linear infinite;
}
@keyframes nebulaTopGrid {
    from { background-position: -100% 0,0 0; }
    to { background-position: 100% 0,44px 0; }
}
.top-nav-logo {
    position: relative;
    overflow: hidden;
    isolation: isolate;
    border-radius: 14px !important;
    background: linear-gradient(140deg,#9B66FF 0%,#536BFF 52%,#22C8ED 100%) !important;
    box-shadow: 0 0 0 1px rgba(206,195,255,.20),0 0 28px rgba(108,98,255,.35),inset 0 1px 0 rgba(255,255,255,.35) !important;
    animation: nebulaLogoFloat 6s ease-in-out infinite;
}
.top-nav-logo::after {
    content: "";
    position: absolute;
    top: -55%;
    left: -120%;
    width: 55%;
    height: 210%;
    transform: rotate(22deg);
    background: linear-gradient(90deg,transparent,rgba(255,255,255,.35),transparent);
    animation: nebulaLogoSweep 7s ease-in-out infinite;
    pointer-events: none;
}
@keyframes nebulaLogoFloat { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-2px); } }
@keyframes nebulaLogoSweep { 0%,25% { left:-120%; } 58%,100% { left:160%; } }
.top-nav-wordmark { letter-spacing: -.045em !important; }
.top-nav-wordmark b {
    color: #6DEAFF !important;
    text-shadow: 0 0 18px rgba(91,222,255,.48);
}
.top-nav-wordmark small { color: #7F91BA !important; letter-spacing: .18em !important; }
.nav-status {
    border-color: rgba(101,240,198,.24) !important;
    background: linear-gradient(100deg,rgba(39,202,158,.10),rgba(39,202,158,.035)) !important;
    box-shadow: inset 0 0 0 1px rgba(101,240,198,.035);
}
.nav-status i {
    animation: nebulaStatusBlink 2.5s ease-in-out infinite !important;
}
@keyframes nebulaStatusBlink {
    0%,100% { opacity:1; transform:scale(1); box-shadow:0 0 12px rgba(101,240,198,.85); }
    50% { opacity:.48; transform:scale(.78); box-shadow:0 0 3px rgba(101,240,198,.28); }
}
.nav-journey { transition: border-color .25s ease,background .25s ease,transform .25s ease; }
.nav-journey:hover { transform: translateY(-1px); border-color:rgba(112,224,255,.32) !important; }

/* Sidebar: subtle glass rail and crisp selected item. */
section[data-testid="stSidebar"], div[data-testid="stSidebar"] {
    background:
        radial-gradient(ellipse at 0% 0%,rgba(103,76,255,.14),transparent 34%),
        radial-gradient(ellipse at 100% 78%,rgba(10,153,255,.065),transparent 40%),
        linear-gradient(180deg,#0A1024 0%,#090D1D 52%,#07172B 100%) !important;
    border-right: 1px solid rgba(111,134,255,.28) !important;
    box-shadow: 12px 0 42px rgba(0,0,0,.16), inset -1px 0 0 rgba(255,255,255,.025) !important;
}
div[data-testid="stSidebar"] div[role="radiogroup"] { gap: 5px !important; }
div[data-testid="stSidebar"] div[role="radiogroup"] label {
    position: relative !important;
    overflow: hidden;
    border: 1px solid transparent !important;
    border-radius: 13px !important;
    padding: 9px 11px !important;
    transition: transform .22s ease,border-color .22s ease,background .22s ease,box-shadow .22s ease !important;
}
div[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    transform: translateX(3px) !important;
    background: linear-gradient(95deg,rgba(101,93,255,.13),rgba(35,163,255,.055)) !important;
    border-color: rgba(111,143,255,.23) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.035);
}
div[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(100deg,rgba(116,83,255,.24),rgba(41,159,226,.12)) !important;
    border-color: rgba(135,162,255,.31) !important;
    box-shadow: inset 3px 0 0 #8B82FF,0 8px 22px rgba(42,38,130,.17),inset 0 1px 0 rgba(255,255,255,.07) !important;
}
div[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked)::after {
    content: "";
    position: absolute;
    top: 0; right: 0; bottom: 0;
    width: 48%;
    background: linear-gradient(90deg,transparent,rgba(106,225,255,.055));
    pointer-events: none;
}
div[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
    letter-spacing: -.045em !important;
    text-shadow: 0 0 25px rgba(121,106,255,.16) !important;
}

/* Home hero: add circuit shimmer and refine the glass finish. */
.hero.hero-ultimate {
    box-shadow: 0 24px 66px rgba(0,0,0,.29),0 0 0 1px rgba(93,116,255,.10),inset 0 1px 0 rgba(255,255,255,.10) !important;
}
.hero-circuit {
    background-size: 100% 100%,100% 100% !important;
}
.hero-circuit::before {
    content: "";
    position: absolute;
    top: -20%;
    left: -60%;
    width: 34%;
    height: 145%;
    transform: rotate(16deg);
    background: linear-gradient(90deg,transparent,rgba(83,166,255,.045),rgba(170,121,255,.11),transparent);
    filter: blur(8px);
    animation: nebulaCircuitSweep 13s ease-in-out infinite;
}
.hero-circuit::after {
    content: "";
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    height: 1px;
    background: linear-gradient(90deg,transparent,rgba(102,224,255,.48),rgba(157,112,255,.46),transparent);
    opacity: .68;
}
@keyframes nebulaCircuitSweep {
    0%,15% { left:-60%; opacity:0; }
    35% { opacity:1; }
    80%,100% { left:130%; opacity:0; }
}
.hero-circuit span {
    width: 3px !important;
    height: 3px !important;
    box-shadow: 0 0 9px 2px rgba(92,235,255,.62),0 0 18px rgba(92,235,255,.20) !important;
}
.hero-circuit i {
    animation: nebulaCircuitSpark 4.3s ease-in-out infinite;
}
.hero-circuit i:nth-of-type(2) { animation-delay:-1.1s; }
.hero-circuit i:nth-of-type(3) { animation-delay:-2.3s; }
.hero-circuit i:nth-of-type(4) { animation-delay:-3.2s; }
@keyframes nebulaCircuitSpark {
    0%,100% { opacity:.25; filter:brightness(.8); transform:scale(.82); }
    50% { opacity:1; filter:brightness(1.7); transform:scale(1.18); }
}
.hero-ultimate .hero-copy { position: relative; }
.hero-ultimate .hero-copy::before {
    content: "";
    position: absolute;
    z-index: -1;
    left: -18px;
    top: 6%;
    width: 2px;
    height: 78%;
    border-radius: 99px;
    background: linear-gradient(180deg,transparent,rgba(161,137,255,.66),rgba(91,220,255,.40),transparent);
    box-shadow: 0 0 14px rgba(125,117,255,.22);
    opacity: .58;
}
.hero-tag-row span {
    position: relative;
    overflow: hidden;
    background: rgba(8,18,42,.68) !important;
    border-color: rgba(118,145,240,.30) !important;
    transition: transform .24s ease,border-color .24s ease,box-shadow .24s ease !important;
}
.hero-tag-row span::after {
    content: "";
    position: absolute;
    top: 0; bottom: 0; left: -90%;
    width: 45%;
    transform: skewX(-22deg);
    background: linear-gradient(90deg,transparent,rgba(177,223,255,.12),transparent);
    animation: nebulaChipShine 8.5s ease-in-out infinite;
    pointer-events: none;
}
.hero-tag-row span:nth-child(2)::after { animation-delay:-2.8s; }
.hero-tag-row span:nth-child(3)::after { animation-delay:-5.6s; }
.hero-tag-row span:hover {
    transform: translateY(-3px) !important;
    border-color: rgba(98,226,255,.54) !important;
    box-shadow: 0 8px 20px rgba(65,98,255,.13),inset 0 1px 0 rgba(255,255,255,.06) !important;
}
@keyframes nebulaChipShine {
    0%,18% { left:-90%; opacity:0; }
    35% { opacity:1; }
    65%,100% { left:150%; opacity:0; }
}
.creator-byline {
    position: relative;
    overflow: hidden;
    border-color: rgba(148,130,255,.42) !important;
    background: linear-gradient(100deg,rgba(104,83,255,.14),rgba(27,162,255,.07)) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.05),0 7px 20px rgba(25,29,94,.10);
}
.creator-byline::after {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    background: linear-gradient(105deg,transparent 32%,rgba(159,143,255,.09) 48%,transparent 64%);
    background-size: 230% 100%;
    animation: nebulaCreatorSheen 9s ease-in-out infinite;
}
@keyframes nebulaCreatorSheen {
    0%,30% { background-position: 150% 0; }
    70%,100% { background-position: -150% 0; }
}

/* Universal card polish: deeper glass, lift, and edge light. */
.workspace-card,.panel,.voice-studio-card,.voice-context-card,
.home-feature-card,.workflow-home-step,.process-node,
.deadline-row,.voice-message-card,.action-kpi,.action-task-card {
    transition:
        transform .28s cubic-bezier(.2,.75,.2,1),
        border-color .28s ease,
        box-shadow .28s ease,
        background-color .28s ease !important;
}
.workspace-card {
    position: relative !important;
    overflow: hidden;
    isolation: isolate;
    border-color: rgba(111,140,235,.37) !important;
    background:
        radial-gradient(ellipse at 100% 0%,rgba(100,87,255,.105),transparent 42%),
        linear-gradient(145deg,rgba(20,31,64,.91),rgba(8,20,41,.94)) !important;
    box-shadow: 0 16px 38px rgba(0,0,0,.17),inset 0 1px 0 rgba(255,255,255,.06) !important;
}
.workspace-card::before {
    content: "";
    position: absolute;
    z-index: -1;
    top: 0; left: 8%; right: 8%;
    height: 1px;
    background: linear-gradient(90deg,transparent,rgba(103,221,255,.7),rgba(155,117,255,.65),transparent);
    opacity: .62;
}
.workspace-card::after {
    content: "";
    position: absolute;
    top: -40px; right: -44px;
    width: 105px; height: 105px;
    border: 1px solid rgba(113,145,255,.14);
    border-radius: 50%;
    box-shadow: 0 0 0 13px rgba(113,145,255,.025),0 0 0 27px rgba(113,145,255,.018);
    pointer-events: none;
    transition: transform .5s ease,border-color .3s ease;
}
.workspace-card:hover {
    transform: translateY(-4px) !important;
    border-color: rgba(105,201,255,.46) !important;
    box-shadow: 0 22px 44px rgba(0,0,0,.22),0 0 24px rgba(78,114,255,.075),inset 0 1px 0 rgba(255,255,255,.075) !important;
}
.workspace-card:hover::after { transform: scale(1.16) rotate(15deg); border-color:rgba(113,198,255,.25); }
.workspace-kicker {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    color: #78E6FF !important;
    letter-spacing: .17em !important;
}
.workspace-kicker::before {
    content: "";
    width: 5px;height:5px;flex:0 0 5px;
    border-radius: 50%;
    background: #72E8FF;
    box-shadow: 0 0 10px rgba(101,221,255,.7);
}
.workspace-title { letter-spacing: -.035em !important; }
.workspace-copy { line-height: 1.78 !important; }
.workspace-list div {
    padding: 8px 9px;
    border: 1px solid transparent;
    border-radius: 11px;
    transition: transform .22s ease,background .22s ease,border-color .22s ease;
}
.workspace-list div:hover {
    transform: translateX(3px);
    border-color: rgba(115,145,242,.20);
    background: rgba(95,112,220,.065);
}
.workspace-list div > span:first-child { filter: drop-shadow(0 0 6px rgba(99,212,255,.20)); }
.home-feature-card {
    background:
        radial-gradient(ellipse at 100% 0%,rgba(105,84,255,.13),transparent 45%),
        linear-gradient(145deg,rgba(22,34,70,.96),rgba(8,19,41,.98)) !important;
    border-color: rgba(108,136,225,.38) !important;
}
.home-feature-card::after { opacity:.78; }
.home-feature-card:hover {
    transform: translateY(-6px) perspective(950px) rotateX(1.5deg) !important;
    border-color: rgba(97,219,255,.45) !important;
    box-shadow: 0 22px 42px rgba(0,0,0,.24),0 0 27px rgba(78,105,255,.10) !important;
}
.workflow-home-step {
    position: relative;
    overflow: hidden;
    background: linear-gradient(145deg,rgba(19,30,64,.94),rgba(8,19,40,.97)) !important;
}
.workflow-home-step::before {
    content: "";
    position: absolute;
    top: 0;left: 12px;right: 12px;height: 2px;
    background: linear-gradient(90deg,transparent,#827AFF,#5FE2FF,transparent);
    opacity: .7;
}
.workflow-home-step:hover,.process-node:hover {
    transform: translateY(-4px) !important;
    border-color: rgba(96,214,255,.38) !important;
    box-shadow: 0 18px 34px rgba(0,0,0,.22),0 0 22px rgba(93,106,255,.09) !important;
}
.panel {
    background:
        radial-gradient(ellipse at 100% 0%,rgba(85,96,220,.10),transparent 43%),
        linear-gradient(145deg,rgba(19,31,63,.96),rgba(8,19,39,.98)) !important;
    border-color: rgba(102,128,213,.32) !important;
    box-shadow: 0 12px 28px rgba(0,0,0,.16),inset 0 1px 0 rgba(255,255,255,.04) !important;
}
.panel:hover {
    transform: translateY(-3px) !important;
    border-color: rgba(105,175,255,.40) !important;
    box-shadow: 0 20px 38px rgba(0,0,0,.20),0 0 20px rgba(91,111,255,.075) !important;
}
.nexus-bento-card {
    background:
        radial-gradient(ellipse at 96% 0%,rgba(99,82,255,.14),transparent 42%),
        linear-gradient(145deg,rgba(22,33,69,.97),rgba(7,17,37,.98)) !important;
    border-color: rgba(112,139,230,.38) !important;
    box-shadow: 0 18px 42px rgba(0,0,0,.20),inset 0 1px 0 rgba(255,255,255,.055) !important;
}
.nexus-bento-card:hover {
    transform: translateY(-7px) perspective(1150px) rotateX(1deg) !important;
    border-color: rgba(93,222,255,.52) !important;
    box-shadow: 0 27px 55px rgba(0,0,0,.25),0 0 30px rgba(91,109,255,.12),inset 0 1px 0 rgba(255,255,255,.08) !important;
}
.nexus-bento-card .bento-icon {
    transition: transform .3s ease,box-shadow .3s ease !important;
}
.nexus-bento-card:hover .bento-icon {
    transform: translateY(-2px) rotate(-5deg) scale(1.06) !important;
    box-shadow: 0 0 23px rgba(104,201,255,.18) !important;
}
.metric {
    background:
        radial-gradient(ellipse at 100% 0%,rgba(119,86,255,.17),transparent 54%),
        linear-gradient(145deg,rgba(26,37,78,.96),rgba(8,20,42,.98)) !important;
    border-color: rgba(112,139,230,.38) !important;
    box-shadow: 0 13px 30px rgba(0,0,0,.20),inset 0 1px 0 rgba(255,255,255,.06) !important;
}
.metric:hover {
    transform: perspective(1100px) rotateY(-4deg) rotateX(3deg) translateY(-7px) !important;
    border-color: rgba(106,224,255,.60) !important;
    box-shadow: 0 24px 45px rgba(0,0,0,.24),0 0 25px rgba(95,110,255,.14) !important;
}
.metric-value { letter-spacing: -.04em !important; }

/* Page-heading banners look like a designed command interface. */
.page-heading {
    border-color: rgba(117,141,242,.32) !important;
    background:
        radial-gradient(ellipse at 100% 0%,rgba(100,80,255,.20),transparent 42%),
        radial-gradient(ellipse at 0% 100%,rgba(17,168,255,.08),transparent 45%),
        linear-gradient(110deg,rgba(15,25,56,.93),rgba(8,17,38,.87)) !important;
    box-shadow: 0 18px 44px rgba(0,0,0,.18),inset 0 1px 0 rgba(255,255,255,.06) !important;
}
.page-heading h1 {
    text-shadow: 0 0 34px rgba(114,106,255,.17) !important;
}
.page-heading::before {
    opacity: .92 !important;
    background-size: 27px 27px !important;
}
.page-heading::after {
    animation: noticeHeadingOrbit 36s linear infinite !important;
    border-color: rgba(104,218,255,.23) !important;
    box-shadow: 0 0 0 18px rgba(103,123,255,.035),0 0 0 37px rgba(103,123,255,.025),inset 0 0 34px rgba(99,119,255,.06) !important;
}
.eyebrow {
    color: #BEB2FF !important;
    letter-spacing: .18em !important;
}
.page-chip {
    position: relative;
    overflow: hidden;
    border-color: rgba(127,150,255,.34) !important;
    background: linear-gradient(100deg,rgba(91,79,255,.13),rgba(36,166,255,.07)) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.045);
}
.page-chip::after {
    content: "";
    position: absolute;
    top: 0;bottom: 0;left: -70%;
    width: 40%;
    background: linear-gradient(90deg,transparent,rgba(111,220,255,.13),transparent);
    transform: skewX(-20deg);
    animation: nebulaChipShine 9s ease-in-out infinite;
    pointer-events: none;
}
.home-section-title {
    letter-spacing: -.035em !important;
    text-shadow: 0 0 22px rgba(115,111,255,.10);
}
.home-section-title::before {
    content: "";
    display: inline-block;
    width: 4px;height: 17px;
    margin: 0 10px -3px 0;
    border-radius: 99px;
    background: linear-gradient(180deg,#A18CFF,#63E9FF);
    box-shadow: 0 0 13px rgba(107,143,255,.28);
}
.home-section-subtitle { line-height: 1.75 !important; }

/* Animated edge treatments and refined active states on controls. */
.stButton > button,.stDownloadButton > button,button[kind="primary"] {
    position: relative !important;
    overflow: hidden !important;
    isolation: isolate;
    border-radius: 13px !important;
    background: linear-gradient(110deg,#7957F6 0%,#526AFF 42%,#178FD9 78%,#7957F6 100%) !important;
    background-size: 260% 260% !important;
    box-shadow: 0 10px 26px rgba(75,81,242,.25),inset 0 1px 0 rgba(255,255,255,.18) !important;
    transition: transform .22s ease,filter .22s ease,box-shadow .22s ease !important;
}
.stButton > button::before,.stDownloadButton > button::before,button[kind="primary"]::before {
    content: "";
    position: absolute;
    z-index: -1;
    top: -70%;bottom: -70%;left: -70%;
    width: 36%;
    transform: rotate(19deg);
    background: linear-gradient(90deg,transparent,rgba(255,255,255,.19),transparent);
    animation: nebulaButtonSheen 8s ease-in-out infinite;
    pointer-events: none;
}
@keyframes nebulaButtonSheen {
    0%,22% { left:-70%;opacity:0; }
    36% { opacity:1; }
    68%,100% { left:135%;opacity:0; }
}
.stButton > button:hover,.stDownloadButton > button:hover,button[kind="primary"]:hover {
    transform: translateY(-3px) scale(1.012) !important;
    background-position: 100% 50% !important;
    box-shadow: 0 16px 35px rgba(80,83,255,.38),inset 0 1px 0 rgba(255,255,255,.24) !important;
    filter: brightness(1.08) saturate(1.08);
}
.stButton > button:active,.stDownloadButton > button:active {
    transform: translateY(0) scale(.99) !important;
}
.stButton > button[kind="secondary"],button[kind="secondary"] {
    background: linear-gradient(120deg,rgba(18,29,61,.98),rgba(11,20,43,.98)) !important;
    border: 1px solid rgba(119,144,236,.33) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.045),0 5px 16px rgba(0,0,0,.10) !important;
}
button:focus-visible,input:focus-visible,textarea:focus-visible {
    outline: 2px solid rgba(103,226,255,.86) !important;
    outline-offset: 3px !important;
    box-shadow: 0 0 0 5px rgba(103,226,255,.08) !important;
}
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stTextArea"] textarea {
    border-radius: 13px !important;
    border-color: rgba(105,132,220,.36) !important;
    background: linear-gradient(145deg,rgba(8,17,38,.97),rgba(12,22,46,.97)) !important;
    box-shadow: inset 0 2px 12px rgba(0,0,0,.18),0 0 0 1px rgba(94,123,255,.025) !important;
    transition: border-color .22s ease,box-shadow .22s ease,background .22s ease !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(103,220,255,.70) !important;
    box-shadow: inset 0 2px 12px rgba(0,0,0,.16),0 0 0 3px rgba(88,174,255,.09),0 0 24px rgba(98,107,255,.09) !important;
}
div[data-baseweb="select"] > div {
    transition: border-color .22s ease,box-shadow .22s ease,transform .22s ease !important;
}
div[data-baseweb="select"] > div:hover {
    border-color: rgba(116,154,255,.54) !important;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: rgba(96,223,255,.78) !important;
    box-shadow: 0 0 0 3px rgba(96,223,255,.09),0 0 20px rgba(96,131,255,.07) !important;
}
div[role="option"]:hover,div[role="option"][aria-selected="true"] {
    background: linear-gradient(90deg,rgba(98,83,255,.18),rgba(37,163,255,.09)) !important;
}
div[data-testid="stForm"] {
    border-radius: 20px !important;
    border-color: rgba(111,138,230,.29) !important;
    background: linear-gradient(140deg,rgba(15,26,55,.80),rgba(7,15,33,.75)) !important;
    box-shadow: 0 14px 34px rgba(0,0,0,.14),inset 0 1px 0 rgba(255,255,255,.045) !important;
}
div[data-testid="stForm"]:focus-within {
    border-color: rgba(114,167,255,.40) !important;
    box-shadow: 0 16px 38px rgba(0,0,0,.16),0 0 24px rgba(83,111,255,.055) !important;
}
div[data-testid="stFileUploader"] {
    border: 1px dashed rgba(130,151,255,.70) !important;
    border-radius: 19px !important;
    background:
        radial-gradient(ellipse at 100% 0%,rgba(101,84,255,.15),transparent 46%),
        linear-gradient(130deg,rgba(9,19,41,.97),rgba(21,20,54,.94)) !important;
    box-shadow: inset 0 0 30px rgba(65,98,255,.075),0 10px 28px rgba(0,0,0,.10) !important;
}
div[data-testid="stFileUploader"]::before { height:2px !important;opacity:.9; }
div[data-testid="stFileUploader"]::after {
    content:"";
    position:absolute;
    right:13px;top:13px;
    width:18px;height:18px;
    border-top:1px solid rgba(97,224,255,.45);
    border-right:1px solid rgba(97,224,255,.45);
    pointer-events:none;
}
div[data-testid="stFileUploader"] button {
    border-radius: 10px !important;
    border-color: rgba(112,157,255,.35) !important;
    box-shadow: none !important;
}
div[data-testid="stFileUploader"] button:hover {
    box-shadow: 0 0 17px rgba(87,121,255,.15) !important;
}

/* Tabs, accordions and result surfaces get a more active, layered feel. */
div[data-testid="stTabs"] div[role="tablist"] {
    padding: 6px !important;
    gap: 6px !important;
    border-radius: 17px !important;
    background: rgba(6,13,30,.69) !important;
    border-color: rgba(107,134,222,.25) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.035),0 8px 24px rgba(0,0,0,.09) !important;
}
div[data-testid="stTabs"] button[role="tab"] {
    border-radius: 12px !important;
    transition: color .22s ease,background .22s ease,transform .22s ease,box-shadow .22s ease !important;
}
div[data-testid="stTabs"] button[role="tab"]:hover { transform:translateY(-1px); }
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    box-shadow: inset 0 0 0 1px rgba(135,162,255,.29),0 5px 17px rgba(69,75,197,.10) !important;
}
div[data-testid="stExpander"] {
    border-radius: 16px !important;
    border-color: rgba(107,134,222,.28) !important;
    background: linear-gradient(120deg,rgba(13,24,49,.85),rgba(8,17,37,.85)) !important;
    box-shadow: 0 8px 22px rgba(0,0,0,.09) !important;
    transition: border-color .22s ease,box-shadow .22s ease !important;
}
div[data-testid="stExpander"]:hover {
    border-color: rgba(97,206,255,.40) !important;
    box-shadow: 0 12px 28px rgba(0,0,0,.13),0 0 18px rgba(75,106,255,.06) !important;
}
div[data-testid="stExpander"] details[open] summary {
    background: linear-gradient(90deg,rgba(96,82,255,.10),transparent) !important;
}
div[data-testid="stAlert"] {
    border-radius: 15px !important;
    border-color: rgba(117,143,232,.30) !important;
    box-shadow: 0 9px 23px rgba(0,0,0,.09),inset 0 1px 0 rgba(255,255,255,.035) !important;
}
div[data-testid="stProgress"] > div {
    height: 9px !important;
    border: 1px solid rgba(119,144,230,.22);
    background: rgba(9,18,39,.94) !important;
    border-radius: 99px !important;
    overflow: hidden;
}
div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg,#7257FF,#4F8CFF,#62E8FF) !important;
    background-size: 200% 100%;
    border-radius: 99px !important;
    box-shadow: 0 0 15px rgba(92,176,255,.26);
    animation: nebulaProgressFlow 6s linear infinite;
}
@keyframes nebulaProgressFlow { from { background-position:0 0; } to { background-position:200% 0; } }

/* Dashboard event tiles and calendars. */
.deadline-row {
    position: relative;
    overflow: hidden;
    border-radius: 15px !important;
    background: linear-gradient(110deg,rgba(18,30,62,.94),rgba(8,19,40,.96)) !important;
    border-color: rgba(105,132,220,.30) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.035),0 8px 22px rgba(0,0,0,.08);
}
.deadline-row::before {
    content:"";
    position:absolute;left:0;top:15%;bottom:15%;width:2px;
    border-radius:99px;
    background:linear-gradient(180deg,#A28CFF,#63E8FF);
    opacity:.6;
}
.deadline-row:hover {
    transform: translateX(3px) !important;
    border-color: rgba(105,212,255,.42) !important;
    box-shadow: 0 13px 28px rgba(0,0,0,.16),0 0 19px rgba(82,112,255,.06) !important;
}
.deadline-date { box-shadow: 0 6px 16px rgba(89,82,255,.13),inset 0 1px 0 rgba(255,255,255,.12); }
.deadline-pill { box-shadow: inset 0 1px 0 rgba(255,255,255,.04); }
.calendar-cell {
    position: relative;
    overflow: hidden;
    border-radius: 12px !important;
    transition: transform .2s ease,border-color .2s ease,box-shadow .2s ease !important;
}
.calendar-cell:hover:not(.empty) {
    transform: translateY(-3px) !important;
    border-color: rgba(98,218,255,.45) !important;
    box-shadow: 0 10px 24px rgba(0,0,0,.14),0 0 17px rgba(81,111,255,.08) !important;
}
.calendar-cell.has-events {
    border-color: rgba(125,141,255,.49) !important;
    background: linear-gradient(145deg,rgba(48,60,126,.38),rgba(13,27,53,.94)) !important;
}
.calendar-cell.has-events::after {
    content:"";
    position:absolute;top:5px;right:5px;
    width:5px;height:5px;border-radius:50%;
    background:#68E7FF;
    box-shadow:0 0 9px rgba(104,231,255,.7);
}
.deadline-pill.today,.deadline-pill.soon { box-shadow:0 0 13px rgba(100,224,255,.08); }

/* Voice studio, task board and the new Action Center styling. */
.voice-studio-card,.voice-context-card {
    border-radius: 22px !important;
    background:
        radial-gradient(ellipse at 100% 0%,rgba(89,86,255,.12),transparent 45%),
        linear-gradient(145deg,rgba(18,30,63,.95),rgba(8,19,40,.97)) !important;
}
.voice-message-card {
    position: relative;
    overflow: hidden;
    border-radius: 17px !important;
    border-color: rgba(105,135,224,.29) !important;
    background: linear-gradient(110deg,rgba(17,29,59,.96),rgba(8,18,39,.97)) !important;
    box-shadow: 0 12px 28px rgba(0,0,0,.15),inset 0 1px 0 rgba(255,255,255,.04) !important;
}
.voice-message-card::before {
    content:"";
    position:absolute;left:0;top:0;bottom:0;width:2px;
    background:linear-gradient(180deg,#A08AFF,#59DDFF);
    opacity:.75;
}
.voice-message-card:hover {
    transform: translateY(-3px) !important;
    border-color: rgba(98,207,255,.40) !important;
    box-shadow: 0 18px 36px rgba(0,0,0,.20),0 0 21px rgba(82,113,255,.07) !important;
}
.voice-context-pill { box-shadow: inset 0 1px 0 rgba(255,255,255,.06),0 0 18px rgba(111,99,255,.07); }
.action-hero {
    border-color: rgba(135,126,255,.50) !important;
    box-shadow: 0 24px 65px rgba(0,0,0,.28),inset 0 1px 0 rgba(255,255,255,.10),0 0 32px rgba(90,84,255,.06) !important;
}
.action-kpi {
    position: relative;
    border-color: rgba(112,139,230,.34) !important;
    background:
        radial-gradient(ellipse at 100% 0%,rgba(115,84,255,.13),transparent 48%),
        linear-gradient(145deg,rgba(22,33,68,.97),rgba(8,19,40,.98)) !important;
    transition: transform .24s ease,border-color .24s ease,box-shadow .24s ease !important;
}
.action-kpi::before {
    content:"";
    position:absolute;top:0;left:12px;right:12px;height:2px;
    background:linear-gradient(90deg,transparent,#8B7DFF,#61E5FF,transparent);
    opacity:.65;
}
.action-kpi:hover {
    transform: translateY(-4px) !important;
    border-color: rgba(103,219,255,.42) !important;
    box-shadow: 0 19px 38px rgba(0,0,0,.21),0 0 24px rgba(88,108,255,.08) !important;
}
.action-task-card {
    position: relative;
    overflow: hidden;
    border-radius: 14px !important;
    transition: transform .22s ease,border-color .22s ease,box-shadow .22s ease !important;
}
.action-task-card::before {
    content:"";
    position:absolute;left:0;top:12px;bottom:12px;width:2px;
    background:linear-gradient(180deg,#9285FF,#5CDFFF);
    opacity:.55;
}
.action-task-card:hover {
    transform: translateX(2px) !important;
    border-color: rgba(96,208,255,.39) !important;
    box-shadow: 0 12px 27px rgba(0,0,0,.16) !important;
}

/* The footer becomes a glowing end-cap to the page. */
.site-footer {
    position: relative;
    overflow: hidden;
    border-radius: 23px !important;
    border-color: rgba(115,139,230,.32) !important;
    background:
        radial-gradient(ellipse at 95% 0%,rgba(102,76,255,.13),transparent 42%),
        linear-gradient(120deg,rgba(10,18,39,.98),rgba(24,22,57,.96),rgba(7,25,43,.98)) !important;
    box-shadow: 0 18px 45px rgba(0,0,0,.19),inset 0 1px 0 rgba(255,255,255,.055) !important;
}
.footer-brand b { text-shadow:0 0 16px rgba(101,224,255,.30); }
.footer-link-pill {
    transition: transform .22s ease,border-color .22s ease,background .22s ease,box-shadow .22s ease !important;
}
.footer-link-pill:hover {
    transform: translateY(-3px) !important;
    border-color: rgba(94,222,255,.52) !important;
    box-shadow: 0 8px 22px rgba(55,108,255,.10) !important;
}

/* Cleaner technical separators, polished scrollbars and focus rings. */
hr {
    border: 0 !important;
    height: 1px !important;
    background: linear-gradient(90deg,transparent,rgba(115,134,255,.30),rgba(95,217,255,.28),transparent) !important;
    opacity: 1 !important;
}
::-webkit-scrollbar { width: 9px !important;height: 9px !important; }
::-webkit-scrollbar-track { background: #090F21 !important; }
::-webkit-scrollbar-thumb {
    border: 2px solid #090F21 !important;
    border-radius: 99px !important;
    background: linear-gradient(180deg,#7A6BFF,#319FD8) !important;
}
::-webkit-scrollbar-thumb:hover { background:linear-gradient(180deg,#AA8CFF,#61E5FF) !important; }
::selection { color:#FFFFFF;background:rgba(107,93,255,.53); }

/* Responsiveness and motion accessibility. */
@media (max-width: 760px) {
    .workspace-card:hover,.panel:hover,.home-feature-card:hover,
    .workflow-home-step:hover,.process-node:hover,.action-kpi:hover,
    .deadline-row:hover,.voice-message-card:hover {
        transform: none !important;
    }
    .hero-ultimate .hero-copy::before { left:-8px;opacity:.34; }
    .top-nav::before { opacity:.22; }
}
@media (prefers-reduced-motion: reduce) {
    .stApp,.top-nav::before,.top-nav-logo,.top-nav-logo::after,
    .nav-status i,.hero-circuit::before,.hero-circuit i,
    .hero-tag-row span::after,.creator-byline::after,
    .stButton > button::before,.stDownloadButton > button::before,
    button[kind="primary"]::before,div[data-testid="stProgress"] > div > div {
        animation: none !important;
    }
    html { scroll-behavior:auto; }
}



/* =====================================================================
   NOTICEBUDDY FOUR 3D INTERACTION SYSTEMS
   1) Pointer-driven cinematic hero parallax
   2) Perspective glass-card tilt + cursor light
   3) Focused 3D process rail
   4) Scroll-triggered depth reveal for existing content
   ===================================================================== */
.hero.hero-ultimate {
    perspective: 1280px;
    perspective-origin: 50% 45%;
    transform-style: preserve-3d;
}
.hero-robot-wrap {
    transform-style: preserve-3d;
    transform: translate3d(var(--nb-hero-shift-x, 0px), var(--nb-hero-shift-y, 0px), 0)
               rotateX(var(--nb-hero-rotate-x, 0deg))
               rotateY(var(--nb-hero-rotate-y, 0deg));
    will-change: transform;
    transition: transform .26s cubic-bezier(.2,.7,.2,1);
}
.hero-robot {
    transform-style: preserve-3d;
    backface-visibility: hidden;
    translate: var(--nb-robot-x, 0px) var(--nb-robot-y, 0px) 28px;
}
.hero-orbit-outer {
    transform-style: preserve-3d;
    translate: var(--nb-orbit-outer-x, 0px) var(--nb-orbit-outer-y, 0px) 4px;
}
.hero-orbit-inner {
    transform-style: preserve-3d;
    translate: var(--nb-orbit-inner-x, 0px) var(--nb-orbit-inner-y, 0px) 20px;
}
.hero-orbit-core {
    transform-style: preserve-3d;
    translate: var(--nb-core-x, 0px) var(--nb-core-y, 0px) 48px;
}
.hero-hud-top {
    translate: var(--nb-hud-top-x, 0px) var(--nb-hud-top-y, 0px) 24px;
}
.hero-hud-bottom {
    translate: var(--nb-hud-bottom-x, 0px) var(--nb-hud-bottom-y, 0px) 18px;
}
.hero-ultimate .hero-copy,
.hero-ultimate .hero-bottom-ribbon {
    transform: translateZ(8px);
}
.hero-robot-wrap,
.hero-robot,
.hero-orbit,
.hero-orbit-core,
.hero-orbit-node,
.hero-hud {
    backface-visibility: hidden;
}

/* Perspective glass cards. JS supplies per-card tilt and spotlight coordinates. */
.nb-3d-card {
    position: relative;
    isolation: isolate;
    transform-style: preserve-3d;
    backface-visibility: hidden;
    will-change: transform;
    transition:
        transform .20s cubic-bezier(.2,.8,.2,1),
        box-shadow .24s ease,
        border-color .24s ease !important;
}
.nb-card-glint {
    position: absolute;
    inset: 0;
    z-index: -1;
    display: block;
    border-radius: inherit;
    pointer-events: none;
    opacity: 0;
    background: radial-gradient(
        360px circle at var(--nb-card-glow-x, 50%) var(--nb-card-glow-y, 50%),
        rgba(111,218,255,.18),
        rgba(142,105,255,.09) 28%,
        transparent 62%
    );
    transition: opacity .18s ease;
}
.nb-3d-card.is-nb-3d-active .nb-card-glint { opacity: 1; }
.nb-3d-card.is-nb-3d-active {
    transform:
        perspective(1000px)
        rotateX(var(--nb-card-tilt-x, 0deg))
        rotateY(var(--nb-card-tilt-y, 0deg))
        translate3d(0, -4px, 7px) !important;
    box-shadow:
        0 24px 54px rgba(0,0,0,.27),
        0 0 0 1px rgba(116,210,255,.20),
        0 0 28px rgba(91,112,255,.12),
        inset 0 1px 0 rgba(255,255,255,.10) !important;
    border-color: rgba(116,210,255,.53) !important;
    filter: saturate(1.06);
}

/* 3D process rail: the hovered step rises forward, the rest visually recede. */
.nexus-process-rail {
    perspective: 1160px;
    transform-style: preserve-3d;
}
.process-node {
    transform-style: preserve-3d;
    backface-visibility: hidden;
    will-change: transform;
}
.process-node.nb-process-active {
    transform:
        perspective(760px)
        rotateX(var(--nb-process-tilt-x, 0deg))
        rotateY(var(--nb-process-tilt-y, 0deg))
        translate3d(0, -5px, 20px) !important;
    border-color: rgba(103,229,255,.62) !important;
    box-shadow:
        0 18px 36px rgba(0,0,0,.26),
        0 0 0 1px rgba(103,229,255,.12),
        0 0 24px rgba(81,151,255,.14),
        inset 0 1px 0 rgba(255,255,255,.09) !important;
}
.process-node.nb-process-active .process-node-top i {
    transform: translateZ(24px) scale(1.06);
    box-shadow: 0 0 18px rgba(104,225,255,.16);
}
.nexus-process-rail:has(.process-node.nb-process-active) .process-connector {
    background: linear-gradient(90deg,rgba(102,133,255,.18),rgba(94,222,255,.48),rgba(126,104,255,.24));
    transition: background .22s ease;
}

/* 3D reveal on the existing cards/steps as they enter the viewport. */
.nb-reveal-ready {
    opacity: 0;
    transform: translate3d(0, 19px, 0) rotateX(4deg);
    transform-origin: 50% 100%;
    transition:
        opacity .60s ease,
        transform .68s cubic-bezier(.2,.75,.2,1);
}
.nb-reveal-ready.nb-revealed {
    opacity: 1;
    transform: translate3d(0, 0, 0) rotateX(0deg);
}
.nb-revealed {
    opacity: 1;
}
.nb-3d-card.is-nb-3d-active.nb-revealed {
    transform:
        perspective(1000px)
        rotateX(var(--nb-card-tilt-x, 0deg))
        rotateY(var(--nb-card-tilt-y, 0deg))
        translate3d(0, -4px, 7px) !important;
}

/* Touch layouts get the same layered visual without precision pointer tracking. */
@media (max-width: 760px), (hover: none), (pointer: coarse) {
    .hero-robot-wrap { transition-duration: .45s; }
    .hero-robot,
    .hero-orbit-outer,
    .hero-orbit-inner,
    .hero-orbit-core,
    .hero-hud-top,
    .hero-hud-bottom {
        translate: none !important;
    }
    .nb-3d-card.is-nb-3d-active,
    .process-node.nb-process-active {
        transform: none !important;
        filter: none;
    }
    .nb-3d-card { will-change: auto; }
}
@media (prefers-reduced-motion: reduce) {
    .hero-robot-wrap,
    .nb-3d-card,
    .process-node,
    .nb-reveal-ready {
        transition: none !important;
        animation: none !important;
        will-change: auto !important;
    }
    .hero-robot-wrap,
    .nb-3d-card.is-nb-3d-active,
    .process-node.nb-process-active,
    .nb-reveal-ready,
    .nb-reveal-ready.nb-revealed {
        transform: none !important;
        translate: none !important;
        opacity: 1 !important;
        filter: none !important;
    }
}



/* =====================================================================
   NOTICEBUDDY SIGNATURE CSS-3D MASCOT
   An original, layered CSS 3D character; the existing PNG remains a fallback.
   ===================================================================== */
.nb-mascot-model {
    --nb-head-yaw: 0deg;
    --nb-head-pitch: 0deg;
    --nb-pupil-x: 0px;
    --nb-pupil-y: 0px;
    position: relative;
    display: block;
    width: 286px;
    height: 318px;
    max-width: 100%;
    flex: 0 0 auto;
    isolation: isolate;
    perspective: 920px;
    transform-style: preserve-3d;
    filter: drop-shadow(0 16px 24px rgba(0,0,0,.23));
    contain: layout style;
}
.nb-mascot-body-rig {
    position: absolute;
    inset: 0;
    transform-style: preserve-3d;
    translate: 0 0;
    animation: nbMascotBodyFloat 5.3s ease-in-out infinite;
}
@keyframes nbMascotBodyFloat {
    0%,100% { translate: 0 0; }
    50% { translate: 0 -7px; }
}
.nb-mascot-floor-shadow {
    position: absolute;
    left: 50%;
    bottom: 5px;
    width: 154px;
    height: 23px;
    border-radius: 50%;
    background: radial-gradient(ellipse,rgba(28,173,255,.22),rgba(116,73,255,.12) 46%,transparent 73%);
    filter: blur(5px);
    transform: translateX(-50%) translateZ(-22px);
    animation: nbMascotShadowPulse 5.3s ease-in-out infinite;
}
@keyframes nbMascotShadowPulse {
    0%,100% { opacity:.68; scale:1; }
    50% { opacity:.35; scale:.86; }
}
.nb-mascot-aura {
    position: absolute;
    top: 42px;
    left: 50%;
    width: 198px;
    height: 198px;
    border: 1px solid rgba(108,209,255,.20);
    border-radius: 50%;
    box-shadow: 0 0 0 10px rgba(98,119,255,.035), inset 0 0 22px rgba(82,151,255,.055);
    transform: translateX(-50%) translateZ(-14px) rotateX(67deg);
    pointer-events: none;
}
.nb-mascot-aura::before,
.nb-mascot-aura::after {
    content:"";
    position:absolute;
    inset:14px;
    border:1px dashed rgba(150,128,255,.22);
    border-radius:50%;
}
.nb-mascot-aura::after {
    inset:31px;
    border-style:solid;
    border-color:rgba(95,226,255,.15);
}
.nb-mascot-antenna {
    position:absolute;
    left:50%;
    top:1px;
    width:7px;
    height:29px;
    border-radius:9px;
    background:linear-gradient(90deg,#697FA9,#F5FCFF 45%,#788EB8);
    box-shadow:0 0 0 2px rgba(119,197,255,.08);
    transform:translateX(-50%) translateZ(38px);
    z-index:6;
}
.nb-mascot-antenna::before {
    content:"";
    position:absolute;
    top:-6px;
    left:50%;
    width:15px;
    height:15px;
    border:1px solid rgba(174,245,255,.88);
    border-radius:50%;
    background:radial-gradient(circle at 35% 28%,#F7FFFF 0%,#9DF7FF 18%,#3BBAFF 47%,#6557FF 78%);
    box-shadow:0 0 8px rgba(71,219,255,.72),0 0 19px rgba(98,96,255,.38);
    transform:translateX(-50%);
    animation:nbMascotAntennaPulse 3.2s ease-in-out infinite;
}
@keyframes nbMascotAntennaPulse {
    0%,100% { filter:brightness(.92); }
    50% { filter:brightness(1.22); }
}
.nb-mascot-head {
    position:absolute;
    top:20px;
    left:50%;
    width:158px;
    height:132px;
    z-index:8;
    transform-style:preserve-3d;
    transform:translateX(-50%) translateZ(34px) rotateX(var(--nb-head-pitch)) rotateY(var(--nb-head-yaw));
    transform-origin:50% 65%;
    transition:transform .28s cubic-bezier(.2,.7,.2,1);
}
.nb-mascot-head-shell {
    position:absolute;
    inset:0;
    overflow:visible;
    border:1px solid rgba(255,255,255,.92);
    border-radius:44% 44% 39% 39% / 44% 44% 47% 47%;
    background:
      radial-gradient(ellipse at 26% 14%,rgba(255,255,255,.97),transparent 34%),
      linear-gradient(115deg,#8E9CB7 0%,#F8FCFF 19%,#CFD9EA 43%,#FFFFFF 57%,#9EACC7 82%,#EFF7FF 100%);
    box-shadow:
      inset 0 3px 5px rgba(255,255,255,.92),
      inset 0 -7px 12px rgba(59,82,132,.25),
      0 8px 16px rgba(0,0,0,.22),
      0 0 22px rgba(86,187,255,.12);
    transform-style:preserve-3d;
}
.nb-mascot-head-shell::before {
    content:"";
    position:absolute;
    inset:5px 8px auto;
    height:16px;
    border-radius:50%;
    border-top:2px solid rgba(255,255,255,.87);
    opacity:.88;
    pointer-events:none;
}
.nb-mascot-head-shell::after {
    content:"";
    position:absolute;
    width:44px;
    height:7px;
    left:50%;
    bottom:5px;
    border-radius:50%;
    background:linear-gradient(90deg,#8DA1C2,#E9F3FF,#879BBE);
    box-shadow:0 2px 5px rgba(20,32,61,.24);
    transform:translateX(-50%) translateZ(3px);
}
.nb-mascot-ear {
    position:absolute;
    z-index:-1;
    top:43px;
    width:21px;
    height:40px;
    border-radius:9px;
    border:1px solid rgba(239,250,255,.8);
    background:linear-gradient(100deg,#687D9E,#F4F8FF 40%,#9EADC8 80%,#DCE9F8);
    box-shadow:inset 0 1px 2px #FFFFFF,0 4px 7px rgba(0,0,0,.22);
}
.nb-mascot-ear-left { left:-12px; transform:translateZ(-5px) rotateY(-20deg); }
.nb-mascot-ear-right { right:-12px; transform:translateZ(-5px) rotateY(20deg); }
.nb-mascot-ear span {
    position:absolute;
    left:50%;
    top:50%;
    width:5px;
    height:19px;
    border-radius:99px;
    background:linear-gradient(#8EF5FF,#4CA9FF);
    box-shadow:0 0 8px rgba(68,201,255,.62);
    transform:translate(-50%,-50%);
}
.nb-mascot-faceplate {
    position:absolute;
    inset:20px 12px 19px;
    overflow:hidden;
    border:1px solid rgba(104,204,255,.52);
    border-radius:37% 37% 34% 34% / 35% 35% 37% 37%;
    background:
      radial-gradient(ellipse at 50% 0%,rgba(47,75,124,.66),transparent 48%),
      linear-gradient(135deg,#071225 0%,#0E1B38 45%,#070D1D 100%);
    box-shadow:inset 0 0 0 2px rgba(255,255,255,.035),inset 0 10px 18px rgba(0,0,0,.42),0 0 13px rgba(54,174,255,.12);
    transform:translateZ(13px);
    transform-style:preserve-3d;
}
.nb-mascot-faceplate::before {
    content:"";
    position:absolute;
    top:0;
    left:17%;
    width:42%;
    height:31%;
    border-radius:0 0 100% 12%;
    background:linear-gradient(110deg,rgba(255,255,255,.13),transparent 82%);
    transform:skewX(-16deg);
}
.nb-mascot-eye {
    position:absolute;
    top:34%;
    display:block;
    width:28px;
    height:25px;
    border-radius:48% 48% 44% 44%;
    background:radial-gradient(ellipse at 48% 36%,rgba(153,249,255,.20),rgba(24,173,255,.07) 58%,transparent 74%);
    box-shadow:0 0 8px rgba(43,194,255,.18);
    animation:nbMascotBlink 5.5s infinite;
    transform-origin:center;
}
.nb-mascot-eye-left { left:21px; }
.nb-mascot-eye-right { right:21px; animation-delay:.10s; }
@keyframes nbMascotBlink {
    0%,42%,45%,100% { scale:1 1; }
    43.3%,44% { scale:1 .08; }
}
.nb-mascot-pupil {
    position:absolute;
    top:50%;
    left:50%;
    width:13px;
    height:17px;
    border-radius:50%;
    background:radial-gradient(circle at 35% 27%,#FFFFFF 0%,#D9FFFF 12%,#74F4FF 33%,#22B4FF 66%,#3674FF 100%);
    box-shadow:0 0 5px #72F4FF,0 0 13px rgba(35,190,255,.84),0 0 21px rgba(77,122,255,.30);
    transform:translate(calc(-50% + var(--nb-pupil-x)),calc(-50% + var(--nb-pupil-y))) translateZ(2px);
    transition:transform .18s ease,filter .22s ease;
}
.nb-mascot-pupil::after {
    content:"";
    position:absolute;
    top:3px;
    left:3px;
    width:3px;
    height:4px;
    border-radius:50%;
    background:white;
    box-shadow:0 0 3px white;
}
.nb-mascot-mouth {
    position:absolute;
    left:50%;
    top:70%;
    width:25px;
    height:9px;
    border-bottom:2px solid #8BF4FF;
    border-radius:0 0 70% 70%;
    filter:drop-shadow(0 0 4px rgba(84,224,255,.8));
    transform:translateX(-50%) translateZ(3px);
}
.nb-mascot-cheek {
    position:absolute;
    top:62%;
    width:10px;
    height:4px;
    border-radius:50%;
    background:rgba(72,180,255,.42);
    filter:blur(1px);
}
.nb-mascot-cheek-left { left:14px; }
.nb-mascot-cheek-right { right:14px; }
.nb-mascot-neck {
    position:absolute;
    z-index:4;
    top:136px;
    left:50%;
    width:48px;
    height:34px;
    border-radius:12px 12px 15px 15px;
    border:1px solid rgba(238,249,255,.65);
    background:linear-gradient(90deg,#657B9E,#F0F6FF 24%,#9DACC6 53%,#E6F0FF 78%,#7186AA);
    box-shadow:inset 0 2px 3px rgba(255,255,255,.75),0 5px 10px rgba(0,0,0,.2);
    transform:translateX(-50%) translateZ(15px);
}
.nb-mascot-neck::after {
    content:"";
    position:absolute;
    bottom:5px;
    left:50%;
    width:28px;
    height:3px;
    border-radius:9px;
    background:linear-gradient(90deg,#7D6CFF,#7CEBFF);
    box-shadow:0 0 7px rgba(105,206,255,.48);
    transform:translateX(-50%);
}
.nb-mascot-torso {
    position:absolute;
    top:157px;
    left:50%;
    width:139px;
    height:115px;
    z-index:5;
    border:1px solid rgba(255,255,255,.9);
    border-radius:35% 35% 26% 26% / 31% 31% 22% 22%;
    background:
      radial-gradient(ellipse at 28% 6%,rgba(255,255,255,.95),transparent 34%),
      linear-gradient(105deg,#92A1BE,#F5FAFF 23%,#CDD8EA 43%,#FFFFFF 51%,#B7C6DF 75%,#F1F7FF 91%,#8798B9);
    box-shadow:
      inset 0 3px 5px rgba(255,255,255,.9),
      inset 0 -8px 15px rgba(45,67,114,.23),
      0 10px 16px rgba(0,0,0,.22);
    transform:translateX(-50%) translateZ(15px);
    transform-style:preserve-3d;
}
.nb-mascot-torso::before {
    content:"";
    position:absolute;
    inset:8px 11px auto;
    height:19px;
    border-top:1px solid rgba(255,255,255,.92);
    border-radius:50%;
}
.nb-mascot-torso::after {
    content:"";
    position:absolute;
    bottom:8px;
    left:50%;
    width:74px;
    height:8px;
    border-radius:50%;
    background:linear-gradient(90deg,#687B9E,#E8F5FF,#8B9BB9);
    box-shadow:0 2px 4px rgba(42,63,103,.2);
    transform:translateX(-50%) translateZ(4px);
}
.nb-mascot-chest-panel {
    position:absolute;
    top:25px;
    left:50%;
    width:51px;
    height:40px;
    display:grid;
    place-items:center;
    border-radius:11px;
    border:1px solid rgba(102,179,255,.48);
    background:linear-gradient(145deg,rgba(14,33,68,.97),rgba(8,17,40,.99));
    color:#BDF8FF;
    font:800 15px/1 "Space Grotesk",sans-serif;
    letter-spacing:-1px;
    text-shadow:0 0 10px rgba(91,221,255,.64);
    box-shadow:inset 0 1px 0 rgba(255,255,255,.1),0 0 14px rgba(67,155,255,.16);
    transform:translateX(-50%) translateZ(14px);
}
.nb-mascot-chest-panel::after {
    content:"";
    position:absolute;
    inset:4px;
    border:1px solid rgba(107,230,255,.23);
    border-radius:7px;
}
.nb-mascot-status-light {
    position:absolute;
    top:74px;
    left:50%;
    width:15px;
    height:4px;
    border-radius:99px;
    background:linear-gradient(90deg,#9477FF,#73F2FF);
    box-shadow:0 0 8px rgba(85,222,255,.65);
    transform:translateX(-50%) translateZ(7px);
}
.nb-mascot-arm {
    position:absolute;
    top:163px;
    width:41px;
    height:92px;
    z-index:4;
    transform-style:preserve-3d;
    transform-origin:50% 13px;
}
.nb-mascot-arm-left { left:48px; transform:translateZ(7px) rotateZ(16deg); }
.nb-mascot-arm-right { right:48px; transform:translateZ(7px) rotateZ(-16deg); }
.nb-mascot-shoulder {
    position:absolute;
    top:0;
    left:3px;
    width:34px;
    height:32px;
    border-radius:13px;
    border:1px solid rgba(255,255,255,.86);
    background:linear-gradient(110deg,#7A8CAB,#F5FAFF 36%,#B4C4DD 70%,#F4F9FF);
    box-shadow:inset 0 2px 3px rgba(255,255,255,.8),0 4px 8px rgba(0,0,0,.17);
}
.nb-mascot-shoulder::after {
    content:"";
    position:absolute;
    inset:8px 10px;
    border-radius:6px;
    background:linear-gradient(135deg,#8A74FF,#65E8FF);
    box-shadow:0 0 7px rgba(91,203,255,.33);
}
.nb-mascot-forearm {
    position:absolute;
    top:24px;
    left:8px;
    width:26px;
    height:48px;
    border:1px solid rgba(255,255,255,.84);
    border-radius:10px 10px 12px 12px;
    background:linear-gradient(100deg,#7F91B1,#F9FCFF 30%,#BDCBE0 72%,#F1F7FF);
    box-shadow:inset 0 2px 3px rgba(255,255,255,.88),0 5px 7px rgba(0,0,0,.15);
}
.nb-mascot-forearm::after {
    content:"";
    position:absolute;
    top:6px;
    left:50%;
    width:3px;
    height:17px;
    border-radius:5px;
    background:linear-gradient(#8B79FF,#76EBFF);
    box-shadow:0 0 6px rgba(92,212,255,.45);
    transform:translateX(-50%);
}
.nb-mascot-hand {
    position:absolute;
    bottom:0;
    left:8px;
    width:26px;
    height:20px;
    border-radius:9px 9px 12px 12px;
    border:1px solid rgba(248,252,255,.85);
    background:linear-gradient(100deg,#879AB9,#F7FBFF 34%,#BFCDE2 75%,#EDF7FF);
    box-shadow:inset 0 1px 2px white,0 2px 4px rgba(0,0,0,.14);
}
.nb-mascot-hand::before,
.nb-mascot-hand::after {
    content:"";
    position:absolute;
    bottom:-4px;
    width:7px;
    height:10px;
    border-radius:0 0 5px 5px;
    background:linear-gradient(90deg,#9FAFC9,#F1F7FF,#8E9FBD);
}
.nb-mascot-hand::before { left:3px; }
.nb-mascot-hand::after { right:3px; }
.nb-mascot-orbit {
    position:absolute;
    top:130px;
    left:50%;
    width:187px;
    height:67px;
    border:1px solid rgba(88,221,255,.52);
    border-radius:50%;
    box-shadow:0 0 10px rgba(69,187,255,.12),inset 0 0 8px rgba(84,115,255,.08);
    transform:translateX(-50%) translateZ(26px) rotateX(67deg) rotateZ(-14deg);
    pointer-events:none;
    animation:nbMascotOrbit 18s linear infinite;
}
@keyframes nbMascotOrbit { to { rotate:0 0 1 360deg; } }
.nb-mascot-orbit::before {
    content:"";
    position:absolute;
    width:7px;
    height:7px;
    left:14%;
    top:18%;
    border-radius:50%;
    background:#9CF8FF;
    box-shadow:0 0 8px #55DFFF,0 0 15px rgba(102,108,255,.7);
}
.nb-mascot-shoulder .nb-mascot-joint {
    position:absolute;
    z-index:2;
    bottom:-5px;
    left:50%;
    width:15px;
    height:15px;
    border:1px solid rgba(255,255,255,.9);
    border-radius:50%;
    background:radial-gradient(circle at 35% 27%,#FFFFFF,#A4BEDD 53%,#5E759A);
    box-shadow:0 2px 5px rgba(0,0,0,.2);
    transform:translateX(-50%) translateZ(5px);
}
.nb-mascot-spark {
    position:absolute;
    z-index:9;
    color:#B9F8FF;
    text-shadow:0 0 9px #55DFFF;
    font-size:13px;
    animation:nbMascotSparkle 4s ease-in-out infinite;
    pointer-events:none;
}
.nb-mascot-spark-one { top:76px; left:19px; }
.nb-mascot-spark-two { right:16px; top:125px; animation-delay:-1.8s; }
@keyframes nbMascotSparkle {
    0%,100% { opacity:.30; scale:.78; }
    50% { opacity:.95; scale:1.1; }
}
.nb-mascot-fallback {
    display:none;
    width:100%;
    max-width:310px;
    max-height:318px;
    height:auto;
    object-fit:contain;
    filter:drop-shadow(0 0 24px rgba(72,96,255,.34));
    mix-blend-mode:screen;
}
.nb-mascot-hotspot {
    position:absolute;
    z-index:4;
    left:50%;
    top:50%;
    width:186px;
    height:270px;
    padding:0;
    border:1px solid transparent;
    border-radius:48% 48% 35% 35%;
    background:transparent;
    box-shadow:none;
    transform:translate(-50%,-48%);
    cursor:pointer;
    outline:none;
    transition:border-color .2s ease,background .2s ease,box-shadow .2s ease;
}
.nb-mascot-hotspot:focus-visible {
    border-color:rgba(103,229,255,.9);
    background:rgba(83,195,255,.035);
    box-shadow:0 0 0 3px rgba(103,205,255,.14),0 0 22px rgba(100,108,255,.14);
}
.nb-mascot-hotspot:hover {
    border-color:rgba(122,213,255,.12);
}
.nb-mascot-model[data-state="looking"] .nb-mascot-pupil {
    filter:brightness(1.12);
}
.nb-mascot-model[data-state="looking"] .nb-mascot-faceplate {
    box-shadow:inset 0 0 0 2px rgba(255,255,255,.035),inset 0 10px 18px rgba(0,0,0,.42),0 0 18px rgba(54,174,255,.20);
}
.nb-mascot-model[data-state="greeting"] .nb-mascot-arm-right {
    animation:nbMascotWave .92s cubic-bezier(.33,.05,.2,1) 1;
}
@keyframes nbMascotWave {
    0% { transform:translateZ(7px) rotateZ(-16deg); }
    24% { transform:translateZ(16px) rotateZ(-64deg); }
    45% { transform:translateZ(16px) rotateZ(-48deg); }
    67% { transform:translateZ(16px) rotateZ(-64deg); }
    86%,100% { transform:translateZ(7px) rotateZ(-16deg); }
}
.nb-mascot-model[data-state="thinking"] .nb-mascot-pupil {
    box-shadow:0 0 6px #72F4FF,0 0 17px rgba(35,190,255,.94),0 0 24px rgba(98,96,255,.42);
    animation:nbMascotThinkGlow 1.8s ease-in-out infinite alternate;
}
@keyframes nbMascotThinkGlow {
    from { filter:brightness(.88); }
    to { filter:brightness(1.25); }
}
.nb-mascot-model[data-state="thinking"] .nb-mascot-orbit {
    animation-duration:5.5s;
    border-color:rgba(102,223,255,.72);
}
.nb-mascot-model[data-state="listening"] .nb-mascot-eye {
    box-shadow:0 0 14px rgba(70,219,255,.36);
}
.nb-mascot-model[data-state="success"] .nb-mascot-pupil {
    background:radial-gradient(circle at 35% 27%,#FFFFFF 0%,#D9FFFF 12%,#A3F8DF 33%,#33D7B0 66%,#219EAF 100%);
}
.nb-mascot-model[data-state="error"] .nb-mascot-status-light {
    background:linear-gradient(90deg,#9477FF,#FF8AAE);
    box-shadow:0 0 8px rgba(255,138,174,.5);
}
.nb-mascot-compact {
    width:286px;
    height:318px;
    max-width:none;
    transform:scale(.39);
    transform-origin:top left;
    filter:drop-shadow(0 8px 15px rgba(0,0,0,.2));
}
.nb-activity-mascot {
    display:flex;
    align-items:center;
    gap:4px;
    min-height:112px;
    margin:2px 0 8px;
    padding:9px 12px;
    overflow:hidden;
    border:1px solid rgba(112,184,255,.20);
    border-radius:15px;
    background:linear-gradient(110deg,rgba(8,18,40,.36),rgba(44,45,109,.15));
}
.nb-activity-mascot-visual {
    width:112px;
    height:106px;
    flex:0 0 112px;
    position:relative;
    overflow:hidden;
}
.nb-activity-mascot-copy {
    display:flex;
    flex-direction:column;
    gap:4px;
    min-width:0;
    color:#EAF5FF;
}
.nb-activity-mascot-copy b {
    font-size:12px;
    letter-spacing:.01em;
}
.nb-activity-mascot-copy span {
    font-size:10px;
    line-height:1.6;
    color:#93B5D9;
}
@supports not (transform-style:preserve-3d) {
    .nb-mascot-model { display:none !important; }
    .nb-mascot-fallback { display:block !important; }
    .nb-mascot-hotspot { display:none !important; }
}
@media (max-width:760px) {
    .nb-mascot-model:not(.nb-mascot-compact) {
        width:244px;
        height:280px;
        scale:.90;
        transform-origin:center center;
    }
    .nb-mascot-hotspot { width:164px;height:242px; }
    .nb-activity-mascot { padding:7px;gap:0; }
    .nb-activity-mascot-visual { width:82px;height:96px;flex-basis:82px; }
    .nb-mascot-compact { transform:scale(.31); }
    .nb-activity-mascot-copy b { font-size:11px; }
}
@media (prefers-reduced-motion:reduce) {
    .nb-mascot-body-rig,.nb-mascot-floor-shadow,.nb-mascot-antenna::before,
    .nb-mascot-eye,.nb-mascot-orbit,.nb-mascot-spark,
    .nb-mascot-model[data-state="thinking"] .nb-mascot-pupil {
        animation:none !important;
    }
    .nb-mascot-head,.nb-mascot-pupil,.nb-mascot-hotspot { transition:none !important; }
    .nb-mascot-model,.nb-mascot-model * { scroll-behavior:auto !important; }
    .nb-mascot-model[data-state="greeting"] .nb-mascot-arm-right { animation:none !important; }
}

</style>  

""", unsafe_allow_html=True)


# ---------- SIGNATURE CSS-3D NOTICEBUDDY MASCOT ----------
ROBOT_IMAGE_URL = "https://raw.githubusercontent.com/krishagarwal369-droid/NoticeBuddy-AI/main/Neon%20AI%20Robot%20Greeting.png"


def build_mascot_markup(fallback_url="", compact=False, state="idle"):
    """Build the original CSS 3D mascot. The existing robot art remains a fallback."""
    root_classes = "nb-mascot-model nb-mascot-compact" if compact else "nb-mascot-model"
    safe_state = html_escape(state, quote=True)
    safe_url = html_escape(fallback_url, quote=True)
    return f"""
    <div class="{root_classes}" data-state="{safe_state}" aria-hidden="true">
      <div class="nb-mascot-floor-shadow"></div>
      <div class="nb-mascot-body-rig">
        <div class="nb-mascot-aura"></div>
        <div class="nb-mascot-orbit"></div>
        <div class="nb-mascot-antenna"></div>
        <span class="nb-mascot-spark nb-mascot-spark-one">✦</span>
        <span class="nb-mascot-spark nb-mascot-spark-two">✧</span>
        <div class="nb-mascot-arm nb-mascot-arm-left">
          <div class="nb-mascot-shoulder"><i class="nb-mascot-joint"></i></div>
          <div class="nb-mascot-forearm"></div>
          <div class="nb-mascot-hand"></div>
        </div>
        <div class="nb-mascot-arm nb-mascot-arm-right">
          <div class="nb-mascot-shoulder"><i class="nb-mascot-joint"></i></div>
          <div class="nb-mascot-forearm"></div>
          <div class="nb-mascot-hand"></div>
        </div>
        <div class="nb-mascot-torso">
          <div class="nb-mascot-chest-panel">NB</div>
          <div class="nb-mascot-status-light"></div>
        </div>
        <div class="nb-mascot-neck"></div>
        <div class="nb-mascot-head">
          <div class="nb-mascot-ear nb-mascot-ear-left"><span></span></div>
          <div class="nb-mascot-ear nb-mascot-ear-right"><span></span></div>
          <div class="nb-mascot-head-shell">
            <div class="nb-mascot-faceplate">
              <span class="nb-mascot-eye nb-mascot-eye-left"><i class="nb-mascot-pupil"></i></span>
              <span class="nb-mascot-eye nb-mascot-eye-right"><i class="nb-mascot-pupil"></i></span>
              <span class="nb-mascot-cheek nb-mascot-cheek-left"></span>
              <span class="nb-mascot-cheek nb-mascot-cheek-right"></span>
              <span class="nb-mascot-mouth"></span>
            </div>
          </div>
        </div>
      </div>
    </div>
    """.strip()


# ---------- OCR ----------
@st.cache_resource
def get_reader():
    return easyocr.Reader(["en"], gpu=False)


# ---------- AI ----------
def generate_notice_response(client, prompt):
    """Try several currently documented Gemini text models if one is overloaded."""
    model_order = [
        "gemini-3.8-flash",
        "gemini-3.6-flash",
        "gemini-3.5-flash-lite",
    ]
    failures = []

    for index, model_name in enumerate(model_order):
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
            failures.append(f"{model_name}: {str(exc)[:220]}")
            # A short pause can help with transient service overloads.
            if index < len(model_order) - 1:
                time.sleep(0.8)

    failure_summary = " | ".join(failures)
    raise RuntimeError(
        "Google AI could not answer with any configured model. "
        "If errors are 503/UNAVAILABLE or 500/INTERNAL, the provider may be "
        "temporarily overloaded; if errors are 401/403, check the API key/access. "
        "Attempts: " + failure_summary
    )


def matching_notice_lines(notice_text, keywords, limit=7):
    """Return original notice lines containing any requested keyword."""
    results = []
    seen = set()
    for raw_line in notice_text.splitlines():
        line = re.sub(r"\s+", " ", raw_line).strip().lstrip("•*- \t")
        if not line:
            continue
        lowered = line.lower()
        if any(keyword in lowered for keyword in keywords) and lowered not in seen:
            seen.add(lowered)
            results.append(line)
            if len(results) >= limit:
                break
    return results


def build_offline_explanation(notice_text, language):
    """Provide transparent rule-based extraction when the AI provider is down."""
    lines = [re.sub(r"\s+", " ", line).strip() for line in notice_text.splitlines()]
    lines = [line for line in lines if line]
    summary = lines[:4]

    dates_found = extract_notice_dates(notice_text)
    date_lines = [f'{item["date"]} — {item["label"]}' for item in dates_found]

    eligibility = matching_notice_lines(notice_text, [
        "eligib", "eligible", "qualif", "enrolled", "student must",
        "must be", "who have", "who can", "year ", "class ", " पात्र", "पात्र"
    ])
    documents = matching_notice_lines(notice_text, [
        "document", "certificate", "marksheet", "mark sheet", "passbook",
        "identity card", " id card", "aadhaar", "passport", "proof", "photograph"
    ])
    actions = matching_notice_lines(notice_text, [
        "submit", "upload", "complete", "apply", "attend", "visit",
        "report", "register", "carry", "clear", "contact", "before",
        "last date", "deadline", "verify", "verification", " जमा", "करें"
    ])
    notes = matching_notice_lines(notice_text, [
        "important note", "note:", "must ", "should ", "otherwise",
        "provisional", "late", "subject to", "not mentioned", "fictional"
    ])

    if language == "Hindi":
        title_summary = "✨ सरल सारांश"
        title_dates = "📅 महत्वपूर्ण तिथियाँ"
        title_eligibility = "🎯 पात्रता से जुड़ी पंक्तियाँ"
        title_docs = "📑 दस्तावेज़ों से जुड़ी पंक्तियाँ"
        title_actions = "✅ अगले कदमों से जुड़ी पंक्तियाँ"
        title_notes = "⚠️ ज़रूरी नोट्स"
        empty = "इस हिस्से से जुड़ी कोई स्पष्ट पंक्ति नहीं मिली।"
    else:
        title_summary = "✨ Simple Summary"
        title_dates = "📅 Important Dates"
        title_eligibility = "🎯 Eligibility"
        title_docs = "📑 Required Documents"
        title_actions = "✅ What To Do Next"
        title_notes = "⚠️ Important Notes"
        empty = "No clearly matching line was found in the notice."

    def section(title, values):
        value_lines = values if values else [empty]
        return "## " + title + "\n" + "\n".join("- " + value for value in value_lines)

    return "\n\n".join([
        section(title_summary, summary),
        section(title_dates, date_lines),
        section(title_eligibility, eligibility),
        section(title_docs, documents),
        section(title_actions, actions),
        section(title_notes, notes)
    ])


def offline_answer_notice_question(notice_text, question, language):
    """Return source lines rather than inventing an AI answer during an outage."""
    q = question.lower()
    if any(word in q for word in ["date", "deadline", "when", "last day", "last date", "kab", "tithi", "तारीख", "कब", "अंतिम तिथि"]):
        dates_found = extract_notice_dates(notice_text)
        lines = [f'{item["date"]} — {item["label"]}' for item in dates_found]
    elif any(word in q for word in ["document", "certificate", "marksheet", "passbook", "required", "दस्तावेज़", "कागज"]):
        lines = matching_notice_lines(notice_text, [
            "document", "certificate", "marksheet", "mark sheet", "passbook",
            "identity card", "aadhaar", "proof", "required documents"
        ])
    elif any(word in q for word in ["eligib", "eligible", "qualif", "who can", "पात्र"]):
        lines = matching_notice_lines(notice_text, [
            "eligib", "eligible", "qualif", "enrolled", "student must",
            "must be", "who have", "who can", "year ", "class "
        ])
    elif any(word in q for word in ["next step", "what to do", "submit", "upload", "action", "karna", "कैसे करें", "क्या करना"]):
        lines = matching_notice_lines(notice_text, [
            "submit", "upload", "complete", "apply", "attend",
            "report", "register", "carry", "clear", "contact", "before", "verify"
        ])
    else:
        terms = [
            word for word in re.findall(r"[a-zA-Z]{4,}", q)
            if word not in {"what", "which", "when", "where", "does", "this", "that", "from", "with", "about", "have", "will", "your", "notice", "tell", "please"}
        ]
        lines = matching_notice_lines(notice_text, terms) if terms else []

    if language == "Hindi":
        heading = "AI सेवा अभी उपलब्ध नहीं है, इसलिए नीचे मूल नोटिस की मिलती-जुलती पंक्तियाँ दी गई हैं—यह AI-जनरेटेड उत्तर नहीं है।"
        fallback = "नोटिस में इस सवाल से जुड़ी कोई स्पष्ट पंक्ति नहीं मिली। कृपया मूल नोटिस देखें।"
    else:
        heading = "The AI service is temporarily unavailable, so these are matching lines from the original notice—not an AI-generated answer."
        fallback = "I couldn't find a clearly matching line. Please check the original notice."

    body = "\n".join("- " + line for line in lines) if lines else fallback
    return heading + "\n\n" + body


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


def transcribe_voice_question(audio_bytes, speech_language="Auto detect"):
    """Transcribe a short microphone recording into text."""
    client = genai.Client(api_key=st.secrets["GEMMA_API_KEY"])
    language_instruction = {
        "Hindi": "Transcribe in Devanagari Hindi.",
        "English": "Transcribe in English.",
        "Hinglish": "Preserve the natural mix of spoken Hindi and English.",
        "Auto detect": "Detect Hindi, English, or Hinglish and preserve the spoken language naturally."
    }.get(speech_language, "Detect the spoken language.")
    audio_part = types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav")
    prompt = f"""
Transcribe this recording accurately.
{language_instruction}
Return only the recognized words. Do not answer the question or add commentary.
If any words are unclear, mark those parts as [unclear].
"""
    return generate_notice_response(client, [prompt, audio_part]).strip()


def answer_voice_question(question, language, record=None):
    """Answer a voice question using the selected notice when available."""
    if record:
        return answer_notice_question(
            record.get("source_text", ""), record.get("explanation", ""), question, language
        )
    client = genai.Client(api_key=st.secrets["GEMMA_API_KEY"])
    prompt = f"""
You are NoticeBuddy AI, a helpful voice assistant for students.
Reply in {language}, using concise, natural, student-friendly wording.
Help with using NoticeBuddy and general study/productivity questions.
For official deadlines, eligibility, fees, or documents, never guess. Ask the
student to analyze or select the original notice first. Encourage official verification.

Student's voice question:
{question}
"""
    return generate_notice_response(client, prompt)


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
                    st.warning("AI chat is temporarily unavailable. Showing matching lines from the notice instead.")
                    answer = offline_answer_notice_question(
                        record.get("source_text", ""),
                        question.strip(),
                        record.get("language", "English")
                    )
                    chats.append({"role": "user", "text": question.strip()})
                    chats.append({"role": "assistant", "text": answer})
                    st.caption(f"AI service details: {exc}")
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


AI_ACTIVITY_HTML = f"""
<div class="ai-activity-card">
  <div class="ai-activity-header">
    <span class="activity-pulse"></span>
    <strong>NoticeBuddy AI is working</strong>
    <span class="activity-live">LIVE SCAN</span>
  </div>
  <div class="nb-activity-mascot" role="status" aria-label="NoticeBuddy is analyzing your notice">
    <div class="nb-activity-mascot-visual">
      {build_mascot_markup(ROBOT_IMAGE_URL, compact=True, state="thinking")}
    </div>
    <div class="nb-activity-mascot-copy">
      <b>I'm reading the fine print.</b>
      <span>Extracting details and preparing a clear explanation. This animation appears only while the real analysis request is running.</span>
    </div>
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
st.session_state.setdefault("voice_history", [])
st.session_state.setdefault("voice_draft_transcript", "")
st.session_state.setdefault("action_tasks", [])


# ---------- APP NAVIGATION ----------
def go_to_analyzer():
    st.session_state["main_navigation"] = "✨ Analyzer"


def go_to_action_center():
    st.session_state["main_navigation"] = "✅ Action Center"


def sync_action_task_completion(task_id):
    """Persist checkbox changes before progress is recalculated."""
    completed = bool(st.session_state.get(f"action_done_{task_id}", False))
    for task in st.session_state.get("action_tasks", []):
        if task.get("id") == task_id:
            task["completed"] = completed
            break


with st.sidebar:
    st.markdown("## 📄 NoticeBuddy AI")
    st.caption("Your personal notice assistant")
    st.markdown("---")
    page = st.radio(
        "NAVIGATION",
        ["🏠 Home", "📊 Dashboard", "✅ Action Center", "🎙️ Voice Assistant", "✨ Analyzer", "📘 How it works", "ℹ️ About"],
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
    robot_image_url = ROBOT_IMAGE_URL
    st.markdown(f"""
    <div class="hero hero-ultimate">
      <div class="hero-circuit" aria-hidden="true">
        <span></span><span></span><span></span><span></span><span></span>
        <span></span><span></span><span></span><span></span><span></span>
        <i></i><i></i><i></i><i></i>
      </div>
      <div class="hero-content">
        <div class="hero-copy">
          <div class="hero-live-pill"><span class="hero-live-dot"></span> NOTICE INTELLIGENCE <b>·</b> SYSTEM ONLINE</div>
          <div class="eyebrow">YOUR PERSONAL AI NOTICE ASSISTANT</div>
          <h1>Turn every notice<br>into <span class="hero-title-gradient">a clear plan.</span></h1>
          <p>Dense college circulars. Scholarship deadlines. Official documents.
          Let AI turn the fine print into your next clear move.</p>
          <div class="hero-tag-row">
            <span><i>✦</i> AI EXPLAINER</span>
            <span><i>◷</i> DEADLINE RADAR</span>
            <span><i>⌁</i> VOICE ASSISTANT</span>
          </div>
          <div class="creator-byline"><span class="creator-star">✦</span> Crafted by <b>Kushagra Agarwal</b></div>
        </div>
        <div class="hero-robot-wrap">
          <div class="hero-orbit hero-orbit-outer" aria-hidden="true"></div>
          <div class="hero-orbit hero-orbit-inner" aria-hidden="true"></div>
          <div class="hero-orbit-core" aria-hidden="true"></div>
          <div class="hero-orbit-node node-one" aria-hidden="true">✦</div>
          <div class="hero-orbit-node node-two" aria-hidden="true">◷</div>
          <div class="hero-orbit-node node-three" aria-hidden="true">⌁</div>
          <div class="hero-hud hero-hud-top">
            <span class="hero-hud-icon">◈</span>
            <div><small>NOTICE CORE</small><b>AI READY</b></div>
            <i></i>
          </div>
          {build_mascot_markup(robot_image_url)}
          <img class="nb-mascot-fallback" src="{robot_image_url}" alt="" aria-hidden="true">
          <button class="nb-mascot-hotspot" type="button" aria-label="Make the NoticeBuddy mascot wave"
                  title="Click for a friendly hello"></button>
          <div class="hero-hud hero-hud-bottom">
            <span class="hero-wave-icon">〰</span>
            <div><small>INTELLIGENCE ENGINE</small><b>READ · DECODE · ACT</b></div>
          </div>
        </div>
      </div>
      <div class="hero-bottom-ribbon">
        <span class="ribbon-label">YOUR ADVANTAGE</span>
        <span><i>01</i> READ SMARTER</span><b class="ribbon-separator">/</b>
        <span><i>02</i> FIND DEADLINES</span><b class="ribbon-separator">/</b>
        <span><i>03</i> MOVE WITH CLARITY</span>
        <span class="ribbon-live"><i></i> MADE FOR STUDENTS</span>
      </div>
    </div>
    <div class="home-hero-manifesto">
      <div><span class="manifesto-kicker">NOT JUST A SUMMARY</span><b>Your next move, made clear.</b></div>
      <p>From the first line to the final deadline—one focused workspace for every notice.</p>
      <span class="manifesto-arrow">↘</span>
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

    st.markdown("""
    <div class="nexus-section-head">
      <div class="nexus-section-kicker"><span></span> THE NOTICE INTELLIGENCE PLATFORM <i></i> CORE CAPABILITIES</div>
      <div class="nexus-section-title">Not just read.<br><b>Understood.</b></div>
      <p>One focused workspace. Every important detail brought into view.</p>
    </div>
    <div class="nexus-signal-strip">
      <span class="nexus-signal-brand">NB <b>/ CORE</b></span>
      <span class="nexus-signal-item"><i></i> DOCUMENT INPUT</span>
      <b class="nexus-signal-arrow">→</b>
      <span class="nexus-signal-item"><i></i> AI EXPLANATION</span>
      <b class="nexus-signal-arrow">→</b>
      <span class="nexus-signal-item"><i></i> CLEAR NEXT STEPS</span>
      <span class="nexus-signal-tail">NOTICE CLARITY SYSTEM</span>
    </div>
    <div class="nexus-bento-grid">
      <article class="nexus-bento-card bento-ai">
        <div class="bento-topline"><span class="bento-icon">◈</span><span class="bento-index">01 / INTELLIGENCE</span><span class="bento-corner">↗</span></div>
        <div class="bento-copy">
          <div class="bento-overline">THE NOTICE DECODER</div>
          <h3>Decode the<br><em>fine print.</em></h3>
          <p>Turn long circulars into a structured brief with summaries, dates, eligibility, documents and next steps.</p>
        </div>
        <div class="nexus-mini-terminal">
          <div class="terminal-top"><span>NOTICE ANALYSIS / UI PREVIEW</span><span class="terminal-lights"><i></i><i></i><i></i></span></div>
          <div class="terminal-scan"><span></span><b>TEXT EXTRACTION</b><i>READY</i></div>
          <div class="terminal-rule"><span style="width:92%"></span></div>
          <div class="terminal-rule"><span style="width:68%"></span></div>
          <div class="terminal-rule"><span style="width:81%"></span></div>
          <div class="terminal-result"><span class="terminal-result-icon">✦</span><div><small>STRUCTURED OUTPUT</small><b>Summary · Dates · Actions</b></div><span class="terminal-check">✓</span></div>
        </div>
        <div class="bento-ambient-ring"></div>
      </article>
      <article class="nexus-bento-card bento-voice">
        <div class="bento-topline"><span class="bento-icon">⌁</span><span class="bento-index">02 / VOICE STUDIO</span></div>
        <div class="bento-voice-orb"><div class="voice-orb-core">NB</div><span></span><span></span><span></span></div>
        <div class="bento-overline">SPEAK NATURALLY</div>
        <h3>Your voice.<br><em>Your assistant.</em></h3>
        <p>Ask in Hindi, English or Hinglish. Review the transcript, get an answer and listen to the reply.</p>
        <div class="bento-wave" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
      </article>
      <article class="nexus-bento-card bento-deadline">
        <div class="bento-topline"><span class="bento-icon">◷</span><span class="bento-index">03 / DEADLINE RADAR</span></div>
        <div class="bento-overline">KEEP THE NEXT DATE IN SIGHT</div>
        <h3>Dates become<br><em>decisions.</em></h3>
        <p>Spot explicit full dates in notices, review countdowns and add your own reminders.</p>
        <div class="bento-calendar-preview">
          <div class="calendar-preview-head"><b>DATE RADAR</b><span>PREVIEW</span></div>
          <div class="calendar-preview-days"><span>M</span><span>T</span><span>W</span><span>T</span><span>F</span><span>S</span><span>S</span></div>
          <div class="calendar-preview-numbers"><span>01</span><span>02</span><span>03</span><span>04</span><span>05</span><span class="calendar-preview-mark">06</span><span>07</span></div>
          <div class="calendar-preview-foot"><i></i> DEADLINES STAND OUT</div>
        </div>
      </article>
      <article class="nexus-bento-card bento-library">
        <div class="bento-topline"><span class="bento-icon">▤</span><span class="bento-index">04 / SESSION LIBRARY</span></div>
        <div class="bento-stack" aria-hidden="true"><div class="stack-sheet sheet-back"></div><div class="stack-sheet sheet-mid"></div><div class="stack-sheet sheet-front"><span>NOTICE / 001</span><b>Saved analysis</b><i>SUMMARY · DATES · ACTIONS</i><div class="stack-lines"></div></div><span class="stack-star">✦</span></div>
        <div class="bento-overline">YOUR WORKSPACE</div>
        <h3>Keep your<br><em>work in reach.</em></h3>
        <p>Save important notices, revisit recent analyses and export session history when needed.</p>
        <div class="bento-local-note"><span></span> PRIVATE TO THE ACTIVE SESSION</div>
      </article>
    </div>
    <div class="nexus-process-head">
      <div><div class="nexus-section-kicker"><span></span> THE PIPELINE</div><h2>From notice <b>to next move.</b></h2></div>
      <p>A deliberate workflow, designed to reduce confusion—not replace the official source.</p>
    </div>
    <div class="nexus-process-rail">
      <div class="process-node"><div class="process-node-top"><span>01</span><i>↗</i></div><b>Ingest</b><p>Paste text or upload a readable image/PDF.</p></div>
      <div class="process-connector"><span></span></div>
      <div class="process-node"><div class="process-node-top"><span>02</span><i>⌗</i></div><b>Extract</b><p>Read the text that can be found in the notice.</p></div>
      <div class="process-connector"><span></span></div>
      <div class="process-node"><div class="process-node-top"><span>03</span><i>✦</i></div><b>Understand</b><p>Organize the details into clear sections.</p></div>
      <div class="process-connector"><span></span></div>
      <div class="process-node"><div class="process-node-top"><span>04</span><i>✓</i></div><b>Act</b><p>Verify official requirements, then plan the next step.</p></div>
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
        st.button("✅ Open Action Center", key="dashboard_open_action_center", on_click=go_to_action_center, use_container_width=True)
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



# ---------- NOTICEBUDDY ACTION CENTER ----------
elif page == "✅ Action Center":
    st.markdown("""
    <div class="action-hero">
      <div class="action-eyebrow"><span></span> NOTICEBUDDY / ACTION CENTER</div>
      <h1>From notice to <b>done.</b></h1>
      <p>Turn the exact instructions in your notices into a trackable plan. Add your own tasks, set priorities, watch due dates and export your checklist.</p>
      <div class="action-hero-footer"><span>01 / EXTRACT</span><i></i><span>02 / ORGANIZE</span><i></i><span>03 / COMPLETE</span></div>
    </div>
    """, unsafe_allow_html=True)

    all_notice_records = st.session_state.get("notice_history", [])
    action_tasks = st.session_state.setdefault("action_tasks", [])
    today_action = date.today()
    action_flash_message = st.session_state.pop("action_flash_message", None)
    if action_flash_message:
        st.success(action_flash_message)

    def _action_priority(task):
        return task.get("priority", "Normal")

    def _action_is_overdue(task):
        due = task.get("due_date", "")
        if not due or task.get("completed"):
            return False
        try:
            return date.fromisoformat(due) < today_action
        except (ValueError, TypeError):
            return False

    completed_count = sum(1 for task in action_tasks if task.get("completed"))
    open_count = len(action_tasks) - completed_count
    overdue_count = sum(1 for task in action_tasks if _action_is_overdue(task))
    completion_pct = int((completed_count / len(action_tasks)) * 100) if action_tasks else 0
    selected_action_record = None

    kpi_cols = st.columns(4)
    kpi_items = [
        ("TOTAL TASKS", str(len(action_tasks)), "◈", "action-kpi-blue"),
        ("IN PROGRESS", str(open_count), "↗", "action-kpi-violet"),
        ("COMPLETED", str(completed_count), "✓", "action-kpi-green"),
        ("OVERDUE", str(overdue_count), "!", "action-kpi-red"),
    ]
    for col, (label, value, icon, kpi_class) in zip(kpi_cols, kpi_items):
        with col:
            st.markdown(
                f'<div class="action-kpi {kpi_class}"><div class="action-kpi-top"><span>{icon}</span><small>{label}</small></div><strong>{value}</strong></div>',
                unsafe_allow_html=True
            )

    progress_left, progress_right = st.columns([0.72, 0.28])
    with progress_left:
        st.markdown(
            f'<div class="action-progress-label"><span>Overall completion</span><b>{completion_pct}%</b></div>',
            unsafe_allow_html=True
        )
        st.progress(completion_pct / 100 if action_tasks else 0.0, text="Checklist progress")
    with progress_right:
        st.markdown(
            f'<div class="action-progress-caption"><b>{completed_count} of {len(action_tasks)}</b><span>tasks completed</span></div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="action-section-title"><span>01</span><div><b>Build a checklist from a notice</b><small>Suggestions are extracted from your original notice text—not invented requirements.</small></div></div>', unsafe_allow_html=True)
    if not all_notice_records:
        st.info("Pehle Analyzer page par ek notice analyze kar. Uske baad yahan se source-based checklist bana sakta hai.")
        st.button("✨ Open Analyzer", key="action_open_analyzer_empty", on_click=go_to_analyzer, use_container_width=True)
    else:
        notice_options = ["No notice selected"] + [
            f"{index + 1}. {record.get('title', 'Untitled notice')}" for index, record in enumerate(all_notice_records)
        ]
        selected_notice_label = st.selectbox(
            "Select an analyzed notice",
            notice_options,
            key="action_center_notice_select",
            help="The checklist is built from the selected notice's extracted source text and dates."
        )
        if selected_notice_label != "No notice selected":
            selected_index = notice_options.index(selected_notice_label) - 1
            if 0 <= selected_index < len(all_notice_records):
                selected_action_record = all_notice_records[selected_index]
                st.markdown(
                    f'<div class="action-source-pill"><span>▤</span><div><small>SELECTED SOURCE</small><b>{html_escape(selected_action_record.get("title", "Untitled notice"))}</b></div><em>{len(selected_action_record.get("dates", []))} date(s) detected</em></div>',
                    unsafe_allow_html=True
                )

        if st.button(
            "✦ Generate checklist from this notice",
            key="action_generate_from_notice",
            type="primary",
            disabled=selected_action_record is None,
            use_container_width=True
        ):
            record = selected_action_record
            source_id = record.get("id")
            source_title = record.get("title", "Notice")
            source_text = record.get("source_text", "") or ""
            existing_signatures = {
                (item.get("source_notice_id"), item.get("evidence", ""))
                for item in action_tasks if item.get("evidence")
            }
            candidate_lines = []
            seen_lines = set()
            action_pattern = re.compile(
                r"\b(submit|upload|apply|register|visit|report|carry|bring|attach|complete|verify|contact|pay|renew|collect|download|fill|email|send|provide|produce|present|appear|deadline|last date|due date|must submit|must carry|should submit|required to|on or before|no later than|applications close|registration closes|valid till)\b|जमा|अपलोड|आवेदन|भरें|ले जाएं|संपर्क|अंतिम तिथि|प्रस्तुत|सत्यापित|करें",
                re.IGNORECASE
            )
            for raw_line in source_text.splitlines():
                clean_line = re.sub(r"\s+", " ", raw_line).strip().lstrip("•*- \t")
                normalized_line = clean_line.casefold()
                if len(clean_line) < 18 or len(clean_line) > 420:
                    continue
                if normalized_line in seen_lines or not action_pattern.search(clean_line):
                    continue
                seen_lines.add(normalized_line)
                candidate_lines.append(clean_line)
                if len(candidate_lines) >= 12:
                    break

            new_tasks = []
            notice_dates = record.get("dates", []) or []

            def _priority_for_line(line):
                if re.search(r"urgent|immediately|last date|deadline|no later than|on or before|must submit|अंतिम तिथि|तुरंत", line, re.IGNORECASE):
                    return "High"
                if re.search(r"verify|check|confirm|contact|सत्यापित|जांच", line, re.IGNORECASE):
                    return "Low"
                return "Normal"

            def _date_for_line(line):
                normalized_source = re.sub(r"\s+", " ", line).casefold()
                for date_item in notice_dates:
                    date_label = re.sub(r"\s+", " ", str(date_item.get("label", ""))).casefold()
                    if normalized_source == date_label or normalized_source in date_label or date_label in normalized_source:
                        return date_item.get("date", "")
                    if len(normalized_source) > 70 and (normalized_source[:70] in date_label or date_label[:70] in normalized_source):
                        return date_item.get("date", "")
                return ""

            for source_line in candidate_lines:
                signature = (source_id, source_line)
                if signature in existing_signatures:
                    continue
                due_value = _date_for_line(source_line)
                new_tasks.append({
                    "id": uuid.uuid4().hex[:12],
                    "title": source_line[:170] + ("…" if len(source_line) > 170 else ""),
                    "evidence": source_line,
                    "source_notice_id": source_id,
                    "source_title": source_title,
                    "due_date": due_value,
                    "priority": _priority_for_line(source_line),
                    "category": "From notice",
                    "completed": False,
                    "created_at": datetime.now().isoformat(timespec="minutes"),
                    "origin": "notice"
                })
                existing_signatures.add(signature)

            # Keep dates visible even if the notice phrases them without an action verb.
            for date_item in notice_dates[:8]:
                date_evidence = str(date_item.get("label", "Date stated in notice"))
                date_signature = (source_id, date_evidence)
                if date_signature in existing_signatures:
                    continue
                date_label = date_evidence[:135] + ("…" if len(date_evidence) > 135 else "")
                new_tasks.append({
                    "id": uuid.uuid4().hex[:12],
                    "title": "Verify date stated in the notice",
                    "evidence": date_evidence,
                    "source_notice_id": source_id,
                    "source_title": source_title,
                    "due_date": date_item.get("date", ""),
                    "priority": "High" if re.search(r"deadline|last date|due|submit by|final date|अंतिम तिथि", date_evidence, re.IGNORECASE) else "Normal",
                    "category": "Notice date",
                    "completed": False,
                    "created_at": datetime.now().isoformat(timespec="minutes"),
                    "origin": "notice"
                })
                existing_signatures.add(date_signature)

            if new_tasks:
                action_tasks.extend(new_tasks)
                st.session_state["action_flash_message"] = f"Checklist built: {len(new_tasks)} task(s) added from {source_title}."
                st.rerun()
            else:
                st.info("Is notice se koi naya matching action/date nahi mila, ya checklist pehle hi ban chuki hai. Neeche manual task add kar sakta hai.")

    st.markdown('<div class="action-section-title"><span>02</span><div><b>Add your own task</b><small>Track a personal follow-up, document collection, call or study step.</small></div></div>', unsafe_allow_html=True)
    with st.form("action_add_task_form", clear_on_submit=True):
        manual_title = st.text_input("Task name", placeholder="e.g. Scan my marksheet and save a PDF")
        manual_cols = st.columns([1, 1, 1])
        with manual_cols[0]:
            manual_priority = st.selectbox("Priority", ["High", "Normal", "Low"], index=1)
        with manual_cols[1]:
            manual_category = st.selectbox("Category", ["Documents", "Submit / Apply", "Follow up", "Verify", "Study / Prepare", "Other"])
        with manual_cols[2]:
            manual_has_due_date = st.checkbox("Set due date", value=False)
            manual_due_date = st.date_input("Due date", value=today_action + timedelta(days=7))
        manual_note = st.text_input("Optional note", placeholder="Add a small detail or reference")
        manual_submitted = st.form_submit_button("＋ Add task to my plan", use_container_width=True)

    if manual_submitted:
        if not manual_title.strip():
            st.warning("Task name empty hai — pehle task ka naam likh.")
        else:
            linked_id = selected_action_record.get("id") if selected_action_record else None
            linked_title = selected_action_record.get("title", "Notice") if selected_action_record else "Personal task"
            task_evidence = manual_note.strip() or "Manually added by you"
            action_tasks.append({
                "id": uuid.uuid4().hex[:12],
                "title": manual_title.strip(),
                "evidence": task_evidence,
                "source_notice_id": linked_id,
                "source_title": linked_title,
                "due_date": manual_due_date.isoformat() if manual_has_due_date else "",
                "priority": manual_priority,
                "category": manual_category,
                "completed": False,
                "created_at": datetime.now().isoformat(timespec="minutes"),
                "origin": "manual"
            })
            st.session_state["action_flash_message"] = "Task added to your Action Center."
            st.rerun()

    st.markdown('<div class="action-section-title"><span>03</span><div><b>Your action board</b><small>Mark tasks complete, filter the list and export the whole plan.</small></div></div>', unsafe_allow_html=True)
    if action_tasks:
        filter_value = st.radio(
            "Show tasks",
            ["All tasks", "To do", "Completed", "Overdue"],
            horizontal=True,
            key="action_task_filter"
        )
        visible_tasks = []
        for task in action_tasks:
            is_overdue = _action_is_overdue(task)
            if filter_value == "To do" and task.get("completed"):
                continue
            if filter_value == "Completed" and not task.get("completed"):
                continue
            if filter_value == "Overdue" and not is_overdue:
                continue
            visible_tasks.append(task)

        st.markdown(f'<div class="action-board-heading"><b>{len(visible_tasks)} <span>task(s) shown</span></b><span>{completed_count}/{len(action_tasks)} complete</span></div>', unsafe_allow_html=True)
        for task in visible_tasks:
            task_cols = st.columns([0.075, 0.61, 0.16, 0.155], vertical_alignment="center")
            with task_cols[0]:
                task_done_now = st.checkbox(
                    "Complete task",
                    value=bool(task.get("completed")),
                    key=f"action_done_{task['id']}",
                    on_change=sync_action_task_completion,
                    args=(task["id"],),
                    label_visibility="collapsed"
                )
            task["completed"] = task_done_now
            with task_cols[1]:
                status_class = "action-done" if task_done_now else "action-open"
                st.markdown(
                    f'<div class="action-task-card {status_class}"><div class="action-task-title">{html_escape(task.get("title", "Untitled task"))}</div><div class="action-task-meta">{html_escape(task.get("source_title", "Personal task"))} · {html_escape(task.get("category", "Other"))}</div><div class="action-task-evidence">{html_escape(task.get("evidence", ""))}</div></div>',
                    unsafe_allow_html=True
                )
            with task_cols[2]:
                due_date = task.get("due_date", "")
                priority_class = {"High": "action-priority-high", "Normal": "action-priority-normal", "Low": "action-priority-low"}.get(task.get("priority", "Normal"), "action-priority-normal")
                priority_text = html_escape(task.get("priority", "Normal"))
                due_text = "No due date"
                if due_date:
                    try:
                        parsed_due = date.fromisoformat(due_date)
                        due_delta = (parsed_due - today_action).days
                        if task_done_now:
                            due_text = "Completed"
                        elif due_delta < 0:
                            due_text = f"{abs(due_delta)}d overdue"
                        elif due_delta == 0:
                            due_text = "Due today"
                        elif due_delta == 1:
                            due_text = "Due tomorrow"
                        else:
                            due_text = parsed_due.strftime("%d %b %Y")
                    except (ValueError, TypeError):
                        due_text = due_date
                st.markdown(
                    f'<div class="action-task-status"><span class="action-priority {priority_class}">{priority_text}</span><small>{html_escape(due_text)}</small></div>',
                    unsafe_allow_html=True
                )
            with task_cols[3]:
                if st.button("Delete", key=f"action_delete_{task['id']}", use_container_width=True):
                    st.session_state["action_tasks"] = [item for item in action_tasks if item.get("id") != task.get("id")]
                    st.rerun()

        export_csv_buffer = StringIO()
        csv_writer = csv.writer(export_csv_buffer)
        csv_writer.writerow(["Task", "Status", "Priority", "Due date", "Category", "Notice source", "Evidence / note", "Created at"])
        for task in action_tasks:
            csv_writer.writerow([
                task.get("title", ""),
                "Completed" if task.get("completed") else "Open",
                task.get("priority", "Normal"),
                task.get("due_date", ""),
                task.get("category", "Other"),
                task.get("source_title", "Personal task"),
                task.get("evidence", ""),
                task.get("created_at", "")
            ])
        export_left, export_right = st.columns(2)
        with export_left:
            st.download_button(
                "⬇ Export CSV checklist",
                data=export_csv_buffer.getvalue(),
                file_name="noticebuddy_action_plan.csv",
                mime="text/csv",
                key="action_export_csv",
                use_container_width=True
            )
        with export_right:
            st.download_button(
                "⬇ Export JSON backup",
                data=json.dumps(action_tasks, ensure_ascii=False, indent=2),
                file_name="noticebuddy_action_plan.json",
                mime="application/json",
                key="action_export_json",
                use_container_width=True
            )
    else:
        st.markdown("""
        <div class="action-empty-state">
          <span>✓</span><b>Your action board is ready.</b>
          <p>Generate a checklist from an analyzed notice above, or add your own first task. Your tasks will appear here with deadlines and progress tracking.</p>
        </div>
        """, unsafe_allow_html=True)

    st.caption("Action Center tasks are stored only in this active Streamlit session. Export CSV/JSON to keep a copy. Suggested items come from matching lines/dates in the provided notice; always verify them against the official source.")


# ---------- VOICE ASSISTANT ----------
elif page == "🎙️ Voice Assistant":
    st.markdown("""
    <div class="page-heading">
      <div class="eyebrow">NOTICEBUDDY VOICE STUDIO</div>
      <h1>Talk to your notice. 🎙️</h1>
      <p>Ask in Hindi, English or Hinglish. Record a question, review the transcript, then hear NoticeBuddy's reply.</p>
    </div>
    """, unsafe_allow_html=True)

    voice_left, voice_right = st.columns([1, 1], gap="large")
    with voice_left:
        st.markdown("""
        <div class="workspace-card voice-studio-card">
          <div class="workspace-kicker">01 / Speak naturally</div>
          <div class="workspace-title">Ask NoticeBuddy</div>
          <div class="workspace-copy">Record one short question using your microphone.</div>
        </div>
        """, unsafe_allow_html=True)

        speech_language = st.selectbox(
            "Your speech language",
            ["Auto detect", "Hindi", "English", "Hinglish"],
            key="voice_speech_language"
        )
        reply_language = st.selectbox(
            "Reply language",
            ["Hindi", "English", "Hinglish"],
            key="voice_reply_language"
        )
        voice_recording = st.audio_input(
            "🎙️ Record your question",
            sample_rate=16000,
            key="voice_assistant_audio",
            help="Allow microphone access in your browser. Short questions work best."
        )
        if voice_recording:
            st.caption("Recording ready. You can play it back before transcribing.")
            st.audio(voice_recording, format="audio/wav")

        if st.button("🎧 Transcribe my voice", key="voice_transcribe_button", type="primary", use_container_width=True):
            if not voice_recording:
                st.warning("Pehle microphone se question record kar bhai.")
            else:
                try:
                    with st.spinner("Listening to your recording..."):
                        transcript = transcribe_voice_question(voice_recording.getvalue(), speech_language)
                    if not transcript or transcript == "[unclear]":
                        st.warning("Voice clear nahi aayi. Thoda dheere aur clearly dobara record kar.")
                    else:
                        st.session_state["voice_draft_transcript"] = transcript
                        st.session_state["voice_question_editor"] = transcript
                        st.success("Voice transcribed! Send karne se pehle text edit kar sakta hai.")
                except Exception as exc:
                    st.error("Voice transcription abhi complete nahi ho saki.")
                    st.info("Google AI service busy ho sakti hai. Microphone permission aur GEMMA_API_KEY check karke retry kar.")
                    st.caption(f"Technical details: {exc}")

        question_text = st.text_area(
            "Recognized question (you can edit or type here)",
            key="voice_question_editor",
            placeholder="Your transcript appears here. You can also type a question.",
            height=105
        )
        send_voice_question = st.button(
            "✨ Ask NoticeBuddy",
            key="voice_send_button",
            use_container_width=True
        )

    with voice_right:
        st.markdown("""
        <div class="workspace-card voice-context-card">
          <div class="workspace-kicker">02 / Context aware</div>
          <div class="workspace-title">Choose a notice</div>
          <div class="workspace-copy">Select an analyzed notice to keep answers grounded in the original text.</div>
          <div class="workspace-list">
            <div><span>🎤</span><span><b>Voice input</b><br>Record a spoken question.</span></div>
            <div><span>🧠</span><span><b>Notice-aware answers</b><br>Use the selected notice instead of guessing.</span></div>
            <div><span>🔊</span><span><b>Spoken replies</b><br>Listen using your browser's voice engine.</span></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        voice_records = st.session_state.get("notice_history", [])
        context_labels = ["No notice selected"] + [
            f"{i + 1}. {record['title']}" for i, record in enumerate(voice_records)
        ]
        selected_context = st.selectbox(
            "Answer using this notice",
            context_labels,
            key="voice_notice_context"
        )
        selected_record = None
        if selected_context != "No notice selected":
            selected_index = context_labels.index(selected_context) - 1
            if 0 <= selected_index < len(voice_records):
                selected_record = voice_records[selected_index]
                st.markdown(
                    f'<div class="voice-context-pill">✓ Context selected: {html_escape(selected_record["title"])}</div>',
                    unsafe_allow_html=True
                )
        else:
            st.caption("Without a selected notice, official dates or eligibility won't be guessed.")

        if send_voice_question:
            if not question_text.strip():
                st.warning("Pehle question record ya type kar.")
            else:
                try:
                    with st.spinner("NoticeBuddy is preparing your answer..."):
                        answer = answer_voice_question(question_text.strip(), reply_language, selected_record)
                    entry = {
                        "id": uuid.uuid4().hex[:12],
                        "question": question_text.strip(),
                        "answer": answer,
                        "language": reply_language,
                        "context": selected_record.get("title") if selected_record else "General assistant",
                        "created_at": datetime.now().strftime("%d %b %Y, %I:%M %p")
                    }
                    st.session_state.setdefault("voice_history", []).append(entry)
                    st.session_state["voice_draft_transcript"] = ""
                    st.success("Answer ready! Neeche se sun sakta hai.")
                except Exception as exc:
                    st.warning("AI reply service is temporarily unavailable.")
                    if selected_record:
                        fallback_answer = offline_answer_notice_question(
                            selected_record.get("source_text", ""),
                            question_text.strip(),
                            reply_language
                        )
                        st.markdown("**Notice-based fallback**")
                        st.write(fallback_answer)
                        render_read_aloud(
                            fallback_answer,
                            "Hindi" if reply_language in ("Hindi", "Hinglish") else "English"
                        )
                    else:
                        st.info("Select an analyzed notice for a source-based fallback, or retry when the AI service is available.")
                    st.caption(f"Technical details: {exc}")

    st.markdown('<div class="home-section-title">Recent voice conversations</div>', unsafe_allow_html=True)
    voice_entries = st.session_state.get("voice_history", [])
    if not voice_entries:
        st.info("Successful voice conversations will appear here.")
    for entry in reversed(voice_entries[-6:]):
        with st.container(key=f"voice-entry-{entry['id']}"):
            st.markdown(
                f'<div class="voice-message-card">'
                f'<div class="voice-message-meta">YOU ASKED · {html_escape(entry["created_at"])}</div>'
                f'<div class="voice-question-text">🎙️ {html_escape(entry["question"])}</div>'
                f'<div class="voice-context-text">Context: {html_escape(entry["context"])}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
            st.markdown("**NoticeBuddy replied**")
            st.markdown(entry["answer"])
            render_read_aloud(
                entry["answer"],
                "Hindi" if entry.get("language") in ("Hindi", "Hinglish") else "English"
            )
            st.divider()


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
                st.warning("Google AI is temporarily unavailable. Showing a basic rule-based breakdown of the original notice so you can continue testing dates, history, saving and the calendar.")
                st.caption(f"AI service details: {e}")
                explanation = build_offline_explanation(text, language)
                record = add_analysis_record(text, explanation, language)
                st.info("This is a limited offline breakdown, not an AI-generated interpretation. Verify every detail against the original notice.")
                render_saved_analysis(record)

            else:
                activity_slot.empty()
                record = add_analysis_record(text, explanation, language)
                used_model = st.session_state.get("last_ai_model")
                if used_model:
                    st.caption(f"Answered by {used_model}")
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


# ---------- PREMIUM 3D INTERACTIONS (VISUAL ONLY) ----------
components.html(r"""
<script>
(() => {
  let doc;
  let view;
  try {
    view = window.parent;
    doc = view.document;
  } catch (error) {
    return;
  }
  if (!doc || !doc.documentElement || doc.documentElement.dataset.nbPremium3dBound === "1") return;

  const root = doc.documentElement;
  root.dataset.nbPremium3dBound = "1";
  let reduceMotion = false;
  let finePointer = false;
  try {
    reduceMotion = !!(view.matchMedia && view.matchMedia("(prefers-reduced-motion: reduce)").matches);
    finePointer = !!(view.matchMedia && view.matchMedia("(hover: hover) and (pointer: fine)").matches);
  } catch (error) {
    reduceMotion = false;
    finePointer = false;
  }
  const cardSelector = ".nexus-bento-card, .home-feature-card, .workspace-card, .panel, .metric, .action-kpi, .action-task-card, .deadline-row, .voice-message-card, .voice-studio-card, .voice-context-card";
  const revealSelector = ".nexus-bento-card, .home-feature-card, .workflow-home-step, .process-node, .workspace-card, .panel, .metric, .action-kpi, .action-task-card, .deadline-row, .voice-message-card";
  const clamp = (value, min, max) => Math.max(min, Math.min(max, value));
  let activeHero = null;
  let activeCard = null;
  let activeProcess = null;
  let revealObserver = null;

  function setOrRemove(element, property, value) {
    if (!element) return;
    if (value === null) element.style.removeProperty(property);
    else element.style.setProperty(property, value);
  }
  function resetHero(hero) {
    if (!hero) return;
    [
      "--nb-hero-shift-x","--nb-hero-shift-y","--nb-hero-rotate-x","--nb-hero-rotate-y",
      "--nb-robot-x","--nb-robot-y","--nb-orbit-outer-x","--nb-orbit-outer-y",
      "--nb-orbit-inner-x","--nb-orbit-inner-y","--nb-core-x","--nb-core-y",
      "--nb-hud-top-x","--nb-hud-top-y","--nb-hud-bottom-x","--nb-hud-bottom-y"
    ].forEach(name => hero.style.removeProperty(name));
    const mascot = hero.querySelector(".nb-mascot-model:not(.nb-mascot-compact)");
    if (mascot) {
      ["--nb-head-yaw","--nb-head-pitch","--nb-pupil-x","--nb-pupil-y"].forEach(name => mascot.style.removeProperty(name));
      if (mascot.dataset.state !== "greeting") mascot.dataset.state = "idle";
    }
  }
  function resetCard(card) {
    if (!card) return;
    card.classList.remove("is-nb-3d-active");
    [
      "--nb-card-tilt-x","--nb-card-tilt-y","--nb-card-glow-x","--nb-card-glow-y"
    ].forEach(name => card.style.removeProperty(name));
    card.style.removeProperty("transform-origin");
  }
  function resetProcess(node) {
    if (!node) return;
    node.classList.remove("nb-process-active");
    node.style.removeProperty("--nb-process-tilt-x");
    node.style.removeProperty("--nb-process-tilt-y");
  }
  function pointIn(element, event) {
    const rect = element.getBoundingClientRect();
    const width = Math.max(1, rect.width);
    const height = Math.max(1, rect.height);
    return {
      rect,
      x: clamp((event.clientX - rect.left) / width, 0, 1),
      y: clamp((event.clientY - rect.top) / height, 0, 1)
    };
  }

  if (!reduceMotion && finePointer) {
    doc.addEventListener("pointermove", (event) => {
      const target = event.target && event.target.closest ? event.target : null;

      /* Effect 1: pointer-responsive, layered cinematic hero. */
      const hero = target ? target.closest(".hero.hero-ultimate") : null;
      if (hero) {
        activeHero = hero;
        const p = pointIn(hero, event);
        const x = (p.x - 0.5) * 2;
        const y = (p.y - 0.5) * 2;
        hero.style.setProperty("--nb-hero-shift-x", (x * 7).toFixed(2) + "px");
        hero.style.setProperty("--nb-hero-shift-y", (y * 5).toFixed(2) + "px");
        hero.style.setProperty("--nb-hero-rotate-x", (-y * 2.5).toFixed(2) + "deg");
        hero.style.setProperty("--nb-hero-rotate-y", (x * 4).toFixed(2) + "deg");
        hero.style.setProperty("--nb-robot-x", (x * 8).toFixed(2) + "px");
        hero.style.setProperty("--nb-robot-y", (y * 6).toFixed(2) + "px");
        hero.style.setProperty("--nb-orbit-outer-x", (x * -4).toFixed(2) + "px");
        hero.style.setProperty("--nb-orbit-outer-y", (y * -3).toFixed(2) + "px");
        hero.style.setProperty("--nb-orbit-inner-x", (x * 7).toFixed(2) + "px");
        hero.style.setProperty("--nb-orbit-inner-y", (y * 5).toFixed(2) + "px");
        hero.style.setProperty("--nb-core-x", (x * 10).toFixed(2) + "px");
        hero.style.setProperty("--nb-core-y", (y * 7).toFixed(2) + "px");
        hero.style.setProperty("--nb-hud-top-x", (x * 5).toFixed(2) + "px");
        hero.style.setProperty("--nb-hud-top-y", (y * -3).toFixed(2) + "px");
        hero.style.setProperty("--nb-hud-bottom-x", (x * -5).toFixed(2) + "px");
        hero.style.setProperty("--nb-hud-bottom-y", (y * 4).toFixed(2) + "px");

        const mascot = hero.querySelector(".nb-mascot-model:not(.nb-mascot-compact)");
        if (mascot && mascot.dataset.state !== "greeting") {
          mascot.dataset.state = "looking";
          mascot.style.setProperty("--nb-head-yaw", (x * 8).toFixed(2) + "deg");
          mascot.style.setProperty("--nb-head-pitch", (-y * 5).toFixed(2) + "deg");
          mascot.style.setProperty("--nb-pupil-x", (x * 4.0).toFixed(2) + "px");
          mascot.style.setProperty("--nb-pupil-y", (y * 2.4).toFixed(2) + "px");
        }
      } else if (activeHero) {
        resetHero(activeHero);
        activeHero = null;
      }

      /* Effect 2: magnetic 3D glass-card tilt, tied to the real cursor position. */
      const card = target ? target.closest(cardSelector) : null;
      if (card) {
        if (activeCard && activeCard !== card) resetCard(activeCard);
        activeCard = card;
        card.classList.add("nb-3d-card", "is-nb-3d-active");
        let glint = card.querySelector(".nb-card-glint");
        if (!glint) {
          glint = doc.createElement("span");
          glint.className = "nb-card-glint";
          glint.setAttribute("aria-hidden", "true");
          card.prepend(glint);
        }
        const p = pointIn(card, event);
        card.style.setProperty("--nb-card-glow-x", (p.x * 100).toFixed(1) + "%");
        card.style.setProperty("--nb-card-glow-y", (p.y * 100).toFixed(1) + "%");
        const x = (p.x - 0.5) * 2;
        const y = (p.y - 0.5) * 2;
        card.style.setProperty("--nb-card-tilt-x", (-y * 5.2).toFixed(2) + "deg");
        card.style.setProperty("--nb-card-tilt-y", (x * 7.2).toFixed(2) + "deg");
        card.style.transformOrigin = (p.x * 100).toFixed(1) + "% " + (p.y * 100).toFixed(1) + "%";
      } else if (activeCard) {
        resetCard(activeCard);
        activeCard = null;
      }

      /* Effect 3: raised process step with a subtle 3D orientation. */
      const node = target ? target.closest(".process-node") : null;
      if (node) {
        if (activeProcess && activeProcess !== node) resetProcess(activeProcess);
        activeProcess = node;
        node.classList.add("nb-process-active");
        const p = pointIn(node, event);
        const x = (p.x - 0.5) * 2;
        const y = (p.y - 0.5) * 2;
        node.style.setProperty("--nb-process-tilt-x", (-y * 3.2).toFixed(2) + "deg");
        node.style.setProperty("--nb-process-tilt-y", (x * 4.5).toFixed(2) + "deg");
      } else if (activeProcess) {
        resetProcess(activeProcess);
        activeProcess = null;
      }
    }, { passive: true });
    const clearActiveEffects = () => {
      resetHero(activeHero);
      resetCard(activeCard);
      resetProcess(activeProcess);
      activeHero = activeCard = activeProcess = null;
    };
    view.addEventListener("blur", clearActiveEffects);
    doc.addEventListener("pointerout", (event) => {
      const from = event.target && event.target.closest ? event.target : null;
      const destination = event.relatedTarget;
      if (!destination) {
        clearActiveEffects();
        return;
      }
      if (activeHero && from && from.closest(".hero.hero-ultimate") === activeHero && !activeHero.contains(destination)) {
        resetHero(activeHero);
        activeHero = null;
      }
      if (activeCard && from && from.closest(cardSelector) === activeCard && !activeCard.contains(destination)) {
        resetCard(activeCard);
        activeCard = null;
      }
      if (activeProcess && from && from.closest(".process-node") === activeProcess && !activeProcess.contains(destination)) {
        resetProcess(activeProcess);
        activeProcess = null;
      }
    }, true);
  }

  /* Effect 4: existing content settles into view with perspective, not a new section. */
  function prepareReveal(scope) {
    if (!scope || !scope.querySelectorAll) return;
    const found = [];
    if (scope.matches && scope.matches(revealSelector)) found.push(scope);
    scope.querySelectorAll(revealSelector).forEach(element => found.push(element));
    found.forEach(element => {
      if (element.dataset.nbRevealReady === "1") return;
      element.dataset.nbRevealReady = "1";
      element.classList.add("nb-reveal-ready");
      if (reduceMotion || !revealObserver) {
        element.classList.add("nb-revealed");
      } else {
        revealObserver.observe(element);
      }
    });
  }
  /* The mascot's own accessible button triggers a one-shot, local greeting. */
  doc.addEventListener("click", (event) => {
    const hotspot = event.target && event.target.closest
      ? event.target.closest(".nb-mascot-hotspot")
      : null;
    if (!hotspot) return;
    const hero = hotspot.closest(".hero.hero-ultimate");
    const mascot = hero ? hero.querySelector(".nb-mascot-model:not(.nb-mascot-compact)") : null;
    if (!mascot) return;
    mascot.dataset.state = "greeting";
    mascot.style.setProperty("--nb-head-pitch", "-3deg");
    if (mascot._nbGreetingTimer) view.clearTimeout(mascot._nbGreetingTimer);
    mascot._nbGreetingTimer = view.setTimeout(() => {
      if (!mascot.isConnected) return;
      if (mascot.dataset.state === "greeting") mascot.dataset.state = "idle";
      mascot.style.removeProperty("--nb-head-pitch");
      mascot._nbGreetingTimer = null;
    }, reduceMotion ? 0 : 1050);
  });

  if (!reduceMotion && "IntersectionObserver" in view) {
    revealObserver = new view.IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("nb-revealed");
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -4% 0px" });
  }
  prepareReveal(doc);
  if ("MutationObserver" in view && doc.body) {
    const mutationObserver = new view.MutationObserver((records) => {
      records.forEach(record => record.addedNodes.forEach(node => {
        if (node && node.nodeType === 1) prepareReveal(node);
      }));
    });
    mutationObserver.observe(doc.body, { childList: true, subtree: true });
  }
})();
</script>
""", height=1, scrolling=False)
