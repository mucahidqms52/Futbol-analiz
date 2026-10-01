import streamlit as st
import math
import copy
import re
import random
import json
import os
import html as _html
import time
import threading
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess, sys


st.set_page_config(page_title="Futbol Analiz Pro", page_icon="⚽", layout="centered")


@st.cache_resource(show_spinner="Tarayıcı kuruluyor (ilk açılışta 1-2 dk sürer)...")
def _tarayici_kur():
    try:
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=False, timeout=600)
    except Exception:
        pass
    return True


_tarayici_kur()


st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Rajdhani:wght@600;700&display=swap" rel="stylesheet">
<style>
    html { font-size: 13px !important; }
    body, .stApp { font-size: 0.85rem !important; }
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important; }
    h1, h2, h3, h4, .fa-score, .fa-big, .mh-stat-num, .login-title, .mh-hero-title {
        font-family: 'Rajdhani', 'Inter', sans-serif !important;
        letter-spacing: 0.4px;
    }
    .block-container {
        padding-top: 0.8rem !important; padding-bottom: 0.8rem !important;
        padding-left: 0.8rem !important; padding-right: 0.8rem !important;
        max-width: 100% !important;
    }
    :root {
        --bg-0: #060a14; --bg-1: #0b1220; --bg-2: #101a2e;
        --card: #131c2e; --card-2: #16223a; --border: #1f2c44;
        --text: #eaf1fb; --muted: #7f92b3;
        --green: #22c55e; --blue: #3b82f6; --yellow: #f59e0b; --red: #ef4444;
    }
    .stApp {
        background:
            radial-gradient(1200px 600px at 10% -10%, rgba(34,197,94,0.08), transparent 60%),
            radial-gradient(900px 500px at 100% 0%, rgba(59,130,246,0.07), transparent 60%),
            linear-gradient(180deg, #060a14 0%, #0b1220 100%) !important;
    }
    header[data-testid="stHeader"] { background: transparent !important; }
    .stApp, .stApp p, .stApp span, .stApp label, .stApp li,
    .stApp div[data-testid="stMarkdownContainer"] { color: var(--text) !important; }
    .stApp div[data-testid="stCaptionContainer"], .stApp small { color: var(--muted) !important; }
    hr { border-color: var(--border) !important; margin: 0.5rem 0 !important; }
    h1 {
        font-size: 1.35rem !important; font-weight: 800 !important;
        margin: 0.4rem 0 !important; text-align: center;
        background: linear-gradient(135deg, #eaf1fb 0%, #94a3b8 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: 0.4px;
    }
    h2 { font-size: 1rem !important; font-weight: 700 !important; margin: 0.4rem 0 !important; }
    h3 {
        font-size: 0.88rem !important; font-weight: 700 !important;
        margin: 0.25rem 0 !important; border-left: 3px solid var(--green);
        padding-left: 0.5rem;
    }
    p { font-size: 0.8rem !important; margin: 0.2rem 0 !important; line-height: 1.45; }
    div[data-testid="stNumberInput"] label p { font-size: 0.72rem !important; margin: 0 !important; font-weight: 600; }
    div[data-testid="stNumberInput"] input { font-size: 0.85rem !important; padding: 0.35rem 0.5rem !important; height: 2rem !important; }
    div[data-testid="stNumberInput"] button { height: 2rem !important; }
    div[data-testid="stNumberInput"] > div { margin-bottom: 0.25rem !important; }
    .stTextArea textarea, .stTextInput input, div[data-testid="stNumberInput"] input {
        background: var(--card) !important; color: var(--text) !important;
        border: 1.5px solid var(--border) !important; border-radius: 10px !important;
        transition: all 0.2s ease !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus,
    div[data-testid="stNumberInput"] input:focus {
        border-color: var(--green) !important;
        box-shadow: 0 0 0 4px rgba(34,197,94,0.12) !important;
    }
    div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="base-input"] {
        background: var(--card) !important; border-radius: 10px !important;
    }
    .stButton button, div[data-testid="stDownloadButton"] button,
    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(145deg, #18233a, #131c2e) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 10px !important;
        font-weight: 700 !important; font-size: 0.8rem !important;
        color: var(--text) !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.25) !important;
        padding: 0.35rem 0.5rem !important;
    }
    .stButton button p, div[data-testid="stDownloadButton"] button p,
    div[data-testid="stFormSubmitButton"] button p { color: var(--text) !important; font-weight: 700 !important; font-size: 0.8rem !important; }
    .stButton button:hover, div[data-testid="stDownloadButton"] button:hover {
        border-color: var(--green) !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(34,197,94,0.2) !important;
    }
    .stButton button[kind="primary"],
    button[data-testid="stBaseButton-primary"],
    button[data-testid="stBaseButton-primaryFormSubmit"] {
        background: linear-gradient(135deg, #16a34a, #22c55e) !important;
        border: none !important;
        box-shadow: 0 6px 20px rgba(34,197,94,0.35) !important;
        color: #04130a !important;
    }
    .stButton button[kind="primary"] p,
    button[data-testid="stBaseButton-primary"] p,
    button[data-testid="stBaseButton-primaryFormSubmit"] p { color: #04130a !important; }
    div[data-testid="stMetric"] { padding: 0.4rem !important; background: var(--card); border: 1px solid var(--border); border-radius: 10px; }
    div[data-testid="stMetricValue"] { font-size: 1rem !important; font-weight: 800 !important; }
    div[data-testid="stMetricLabel"] { font-size: 0.68rem !important; }
    div[data-testid="stExpander"] {
        background: linear-gradient(145deg, var(--card), #0f1829) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important; overflow: hidden;
        margin-bottom: 8px !important;
    }
    div[data-testid="stExpander"] details > summary {
        display: flex !important; align-items: center !important;
        gap: 6px !important; padding: 0.5rem 0.8rem !important;
        font-size: 0.82rem !important; font-weight: 700 !important;
        line-height: 1.3 !important; min-height: 38px !important;
        overflow: hidden !important; cursor: pointer !important;
        list-style: none !important;
    }
    div[data-testid="stExpander"] details > summary::-webkit-details-marker { display: none !important; }
    div[data-testid="stExpander"] details > summary::marker { display: none !important; content: "" !important; }
    div[data-testid="stExpander"] details > summary:hover { background: rgba(34,197,94,0.05) !important; }
    div[data-testid="stExpander"] details > summary > span[data-testid="stIconMaterial"],
    div[data-testid="stExpander"] details > summary > span.material-icons,
    div[data-testid="stExpander"] details > summary [data-testid="stIconMaterial"],
    div[data-testid="stExpander"] details > summary .material-icons,
    div[data-testid="stExpander"] details > summary [class*="material-symbols"],
    div[data-testid="stExpander"] details > summary [class*="Material"],
    div[data-testid="stExpander"] details > summary > svg + span,
    div[data-testid="stExpander"] details > summary > span[aria-hidden="true"] {
        display: none !important; visibility: hidden !important;
        width: 0 !important; height: 0 !important;
        font-size: 0 !important; overflow: hidden !important;
        position: absolute !important; left: -9999px !important;
        opacity: 0 !important; pointer-events: none !important;
    }
    div[data-testid="stExpander"] details > summary p,
    div[data-testid="stExpander"] details > summary div[data-testid="stMarkdownContainer"],
    div[data-testid="stExpander"] details > summary div[data-testid="stMarkdownContainer"] p {
        font-size: 0.82rem !important; font-weight: 700 !important;
        margin: 0 !important; line-height: 1.3 !important;
        color: #eaf1fb !important; white-space: normal !important;
        display: inline-block !important;
    }
    div[data-testid="stExpander"] details > summary > div {
        display: flex !important; align-items: center !important;
        gap: 6px !important; flex-wrap: nowrap !important;
    }
    div[data-testid="stExpander"] details > summary svg {
        flex-shrink: 0 !important; width: 14px !important; height: 14px !important;
        min-width: 14px !important; transition: transform 0.2s ease !important;
    }
    div[data-testid="stExpander"] details > div[role="region"] {
        padding: 0.4rem 0.8rem 0.8rem 0.8rem !important; font-size: 0.82rem !important;
    }
    div[data-testid="stAlert"] { padding: 0.4rem 0.7rem !important; font-size: 0.8rem !important; border-radius: 10px !important; }
    div[data-testid="stFileUploader"] section {
        background: var(--card) !important;
        border: 1.5px dashed var(--border) !important;
        border-radius: 12px !important;
    }
    .st-key-fa_nav div[data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: 0.3rem !important; }
    .st-key-fa_nav div[data-testid="stColumn"], .st-key-fa_nav div[data-testid="column"] {
        min-width: 0 !important; flex: 1 1 0 !important; width: auto !important;
    }
    .st-key-fa_nav .stButton button {
        padding: 0.3rem 0.25rem !important; height: 2.1rem !important;
        background: rgba(19,28,46,0.6) !important; backdrop-filter: blur(8px);
        border: 1px solid var(--border) !important;
    }
    .st-key-fa_nav .stButton button p { font-size: 0.72rem !important; white-space: nowrap; font-weight: 700 !important; }
    .st-key-fa_nav .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #16a34a, #22c55e) !important;
        box-shadow: 0 4px 16px rgba(34,197,94,0.4) !important;
    }
    .stApp .fa-hero {
        position: relative; overflow: hidden;
        background: linear-gradient(135deg, #14243e 0%, #0d1729 100%);
        border: 1px solid var(--border); border-radius: 16px;
        padding: 14px 12px; margin: 6px 0 10px 0; text-align: center;
        box-shadow: 0 10px 32px rgba(0,0,0,0.4), 0 0 0 1px rgba(34,197,94,0.05) inset;
    }
    .stApp .fa-hero::before {
        content: ""; position: absolute; inset: 0;
        background: radial-gradient(circle at 50% 0%, rgba(34,197,94,0.15), transparent 60%);
        pointer-events: none;
    }
    .stApp .fa-teams { display: flex; align-items: center; justify-content: space-between; gap: 6px; position: relative; z-index: 1; }
    .stApp .fa-team { flex: 1; font-weight: 800; font-size: 0.9rem; line-height: 1.2; word-break: break-word; letter-spacing: 0.2px; }
    .stApp .fa-score {
        font-size: 1.6rem; font-weight: 900; color: var(--green) !important;
        min-width: 80px; letter-spacing: 0.5px; text-shadow: 0 0 20px rgba(34,197,94,0.5);
    }
    .stApp .fa-vs { font-size: 0.9rem; font-weight: 800; color: var(--muted) !important; min-width: 50px; letter-spacing: 1px; }
    .stApp .fa-sub { font-size: 0.68rem; color: var(--muted) !important; margin-top: 6px; letter-spacing: 0.2px; }
    .stApp .fa-card {
        background: linear-gradient(145deg, var(--card), #0f1829);
        border: 1px solid var(--border); border-radius: 14px;
        padding: 10px 12px; margin-bottom: 10px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.25); transition: all 0.25s ease;
    }
    .stApp .fa-card:hover { border-color: rgba(34,197,94,0.3); transform: translateY(-1px); }
    .stApp .fa-card.fa-pos { border-color: rgba(34,197,94,0.55); box-shadow: 0 8px 28px rgba(34,197,94,0.15), 0 0 0 1px rgba(34,197,94,0.15) inset; }
    .stApp .fa-card.fa-neg { opacity: 0.9; }
    .stApp .fa-ttl { font-size: 0.68rem; font-weight: 800; color: var(--muted) !important; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; }
    .stApp .fa-pickrow { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
    .stApp .fa-pick { font-size: 1rem; font-weight: 800; letter-spacing: 0.2px; }
    .stApp .fa-pct { font-size: 1.35rem; font-weight: 900; color: var(--green) !important; text-shadow: 0 0 16px rgba(34,197,94,0.4); }
    .stApp .fa-pct.fa-off { color: var(--muted) !important; text-shadow: none; }
    .stApp .fa-mut { font-size: 0.68rem; color: var(--muted) !important; margin-top: 6px; letter-spacing: 0.15px; }
    .stApp .fa-row { margin: 7px 0; }
    .stApp .fa-row-top { display: flex; justify-content: space-between; font-size: 0.76rem; margin-bottom: 3px; }
    .stApp .fa-lbl { color: #cbd5e1 !important; font-weight: 500; }
    .stApp .fa-val { font-weight: 800; }
    .stApp .fa-bar { position: relative; height: 8px; background: #1a2438; border-radius: 99px; overflow: hidden; box-shadow: inset 0 1px 3px rgba(0,0,0,0.4); }
    .stApp .fa-fill { height: 100%; border-radius: 99px; transition: width 0.6s ease; }
    .stApp .fa-tick { position: absolute; top: 0; bottom: 0; width: 2px; background: #eaf1fb; opacity: 0.8; }
    .stApp .fa-badge { display: inline-block; padding: 3px 9px; border-radius: 99px; font-size: 0.65rem; font-weight: 800; white-space: nowrap; letter-spacing: 0.3px; text-transform: uppercase; }
    .stApp .fa-b-green { background: rgba(34,197,94,0.15); color: var(--green) !important; border: 1px solid rgba(34,197,94,0.5); }
    .stApp .fa-b-yellow { background: rgba(245,158,11,0.15); color: var(--yellow) !important; border: 1px solid rgba(245,158,11,0.5); }
    .stApp .fa-b-red { background: rgba(239,68,68,0.15); color: var(--red) !important; border: 1px solid rgba(239,68,68,0.5); }
    .stApp .fa-b-gray { background: rgba(148,163,184,0.12); color: #94a3b8 !important; border: 1px solid rgba(148,163,184,0.35); }
    .stApp .fa-big { font-size: 1.6rem; font-weight: 900; line-height: 1.05; letter-spacing: -0.4px; }
    .stApp .fa-g { color: var(--green) !important; }
    .stApp .fa-y { color: var(--yellow) !important; }
    .stApp .fa-r { color: var(--red) !important; }
    .stApp .fa-ci { position: relative; height: 8px; background: #1a2438; border-radius: 99px; margin-top: 8px; }
    .stApp .fa-ci-fill { position: absolute; top: 0; bottom: 0; background: rgba(148,163,184,0.4); border-radius: 99px; }
    .stApp .fa-ci-dot { position: absolute; top: -3px; width: 14px; height: 14px; border-radius: 50%; border: 2.5px solid #0b1220; margin-left: -7px; box-shadow: 0 0 12px currentColor; }
    .stApp .fa-mk { background: linear-gradient(145deg, var(--card), #0f1829); border: 1px solid var(--border); border-radius: 12px; padding: 8px 12px; margin: -4px 0 8px 0; box-shadow: 0 4px 16px rgba(0,0,0,0.2); }
    .stApp .fa-mk-row { display: flex; align-items: center; justify-content: space-between; padding: 6px 0; border-bottom: 1px dashed #1d2940; gap: 6px; flex-wrap: wrap; }
    .stApp .fa-mk-row:last-child { border-bottom: none; }
    .stApp .fa-mk-lbl { font-size: 0.75rem; font-weight: 800; color: #cbd5e1 !important; min-width: 55px; }
    .stApp .fa-mk-pick { font-size: 0.86rem; font-weight: 800; }
    .stApp .fa-mk-pick.pass { color: var(--green) !important; }
    .stApp .fa-mk-pick.off { color: #94a3b8 !important; }
    .stApp .fa-mk-pct { font-size: 0.78rem; font-weight: 800; color: var(--text) !important; }
    .stApp .fa-mk-badge { font-size: 0.6rem; font-weight: 800; padding: 2px 7px; border-radius: 99px; margin-left: 4px; letter-spacing: 0.2px; }
    .stApp .fa-mk-badge.ok { background: rgba(34,197,94,0.15); color: var(--green) !important; border: 1px solid rgba(34,197,94,0.5); }
    .stApp .fa-mk-badge.no { background: rgba(148,163,184,0.12); color: #94a3b8 !important; border: 1px solid rgba(148,163,184,0.35); }
    .stApp .fa-mk-info { font-size: 0.66rem; color: var(--muted) !important; }
    .login-hero { text-align: center; padding: 40px 10px 24px 10px; position: relative; }
    .login-logo { font-size: 4.2rem; line-height: 1; margin-bottom: 14px; display: inline-block; filter: drop-shadow(0 0 30px rgba(34,197,94,0.6)); animation: logoPulse 3s ease-in-out infinite; }
    @keyframes logoPulse { 0%, 100% { transform: scale(1) rotate(0deg); filter: drop-shadow(0 0 20px rgba(34,197,94,0.5)); } 50% { transform: scale(1.08) rotate(-3deg); filter: drop-shadow(0 0 40px rgba(34,197,94,0.9)); } }
    .login-title { font-size: 2rem !important; font-weight: 900 !important; background: linear-gradient(135deg, #22c55e 0%, #16a34a 45%, #3b82f6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin: 0 !important; padding: 0 !important; letter-spacing: 1.2px; border: none !important; text-align: center !important; }
    .login-subtitle { font-size: 0.82rem; color: var(--muted) !important; margin-top: 8px; letter-spacing: 0.5px; font-weight: 500; }
    div[data-testid="stForm"] { background: linear-gradient(145deg, rgba(19,28,46,0.9), rgba(11,18,32,0.98)) !important; border: 1.5px solid rgba(34,197,94,0.2) !important; border-radius: 20px !important; padding: 22px 18px !important; box-shadow: 0 20px 60px rgba(0,0,0,0.55), 0 0 0 1px rgba(34,197,94,0.05) inset !important; backdrop-filter: blur(16px); }
    div[data-testid="stForm"] label p { font-size: 0.78rem !important; font-weight: 700 !important; color: #cbd5e1 !important; letter-spacing: 0.3px; margin-bottom: 5px !important; }
    div[data-testid="stForm"] input { height: 42px !important; font-size: 0.9rem !important; padding: 0 14px !important; background: rgba(11,18,32,0.9) !important; border: 1.5px solid var(--border) !important; border-radius: 10px !important; transition: all 0.2s ease; }
    div[data-testid="stForm"] input:focus { border-color: var(--green) !important; box-shadow: 0 0 0 4px rgba(34,197,94,0.15) !important; outline: none !important; }
    div[data-testid="stForm"] button { height: 42px !important; font-size: 0.9rem !important; font-weight: 800 !important; border-radius: 10px !important; letter-spacing: 0.3px; transition: all 0.2s ease; }
    div[data-testid="stForm"] button[kind="primary"] { background: linear-gradient(135deg, #16a34a, #22c55e) !important; box-shadow: 0 8px 24px rgba(34,197,94,0.4) !important; border: none !important; }
    div[data-testid="stForm"] button[kind="primary"]:hover { box-shadow: 0 12px 32px rgba(34,197,94,0.55) !important; transform: translateY(-2px); }
    div[data-testid="stForm"] button[kind="secondary"] { background: rgba(30,41,59,0.6) !important; border: 1.5px solid var(--border) !important; }
    div[data-testid="stForm"] button[kind="secondary"]:hover { border-color: var(--blue) !important; background: rgba(59,130,246,0.1) !important; }
    .login-divider { display: flex; align-items: center; gap: 12px; margin: 12px 0 8px 0; color: #64748b !important; font-size: 0.68rem; font-weight: 800; letter-spacing: 4px; justify-content: center; }
    .login-divider::before, .login-divider::after { content: ""; flex: 1; height: 1px; background: linear-gradient(90deg, transparent, var(--border) 50%, transparent); }
    .login-features { display: flex; flex-wrap: wrap; justify-content: center; gap: 6px; margin-top: 20px; padding: 0 8px; }
    .lf-chip { display: inline-block; padding: 5px 12px; background: rgba(34,197,94,0.08); border: 1px solid rgba(34,197,94,0.3); border-radius: 99px; font-size: 0.7rem; font-weight: 700; color: #cbd5e1 !important; letter-spacing: 0.3px; transition: all 0.2s ease; }
    .lf-chip:hover { background: rgba(34,197,94,0.15); border-color: var(--green); transform: translateY(-2px); }
    .login-footer { text-align: center; margin-top: 24px; font-size: 0.7rem; color: #64748b !important; letter-spacing: 0.5px; }
    .login-footer b { color: var(--green) !important; font-weight: 800; }
    .mh-hero { position: relative; overflow: hidden; text-align: center; padding: 28px 14px 22px 14px; background: linear-gradient(135deg, rgba(22,35,61,0.9), rgba(15,26,46,0.95)); border: 1.5px solid rgba(34,197,94,0.25); border-radius: 20px; margin: 6px 0 16px 0; box-shadow: 0 16px 48px rgba(0,0,0,0.45), 0 0 0 1px rgba(34,197,94,0.06) inset; }
    .mh-hero::before { content: ""; position: absolute; top: -60%; left: -60%; width: 220%; height: 220%; background: radial-gradient(circle at 50% 50%, rgba(34,197,94,0.18), transparent 55%); animation: mhGlow 6s ease-in-out infinite; pointer-events: none; }
    @keyframes mhGlow { 0%, 100% { opacity: 0.5; transform: scale(1) rotate(0deg); } 50% { opacity: 1; transform: scale(1.2) rotate(25deg); } }
    .mh-hero-icon { font-size: 3rem; line-height: 1; margin-bottom: 10px; display: inline-block; filter: drop-shadow(0 0 24px rgba(34,197,94,0.65)); animation: logoPulse 3s ease-in-out infinite; position: relative; z-index: 1; }
    .mh-hero-title { font-size: 1.7rem; font-weight: 900; background: linear-gradient(135deg, #22c55e 0%, #16a34a 45%, #3b82f6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; letter-spacing: 1px; position: relative; z-index: 1; margin: 0; }
    .mh-hero-sub { font-size: 0.8rem; color: var(--muted); margin-top: 8px; letter-spacing: 0.4px; position: relative; z-index: 1; }
    .mh-hero-badge { display: inline-block; margin-top: 12px; padding: 4px 14px; background: rgba(34,197,94,0.12); border: 1px solid rgba(34,197,94,0.45); border-radius: 99px; font-size: 0.7rem; font-weight: 800; color: var(--green) !important; letter-spacing: 0.8px; position: relative; z-index: 1; }
    .mh-stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 0 0 16px 0; }
    .mh-stat { position: relative; background: linear-gradient(145deg, #16233d, #0f1a2e); border: 1px solid var(--border); border-radius: 16px; padding: 14px 10px 12px 10px; text-align: center; overflow: hidden; transition: all 0.25s ease; box-shadow: 0 6px 20px rgba(0,0,0,0.25); }
    .mh-stat:hover { transform: translateY(-3px); border-color: rgba(34,197,94,0.4); box-shadow: 0 12px 32px rgba(34,197,94,0.15); }
    .mh-stat::after { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #22c55e, #3b82f6); }
    .mh-stat-icon { font-size: 1.3rem; margin-bottom: 4px; }
    .mh-stat-num { font-size: 1.8rem; font-weight: 900; color: var(--green) !important; line-height: 1; letter-spacing: -0.8px; text-shadow: 0 0 20px rgba(34,197,94,0.4); }
    .mh-stat-lbl { font-size: 0.65rem; color: var(--muted) !important; margin-top: 6px; letter-spacing: 0.7px; text-transform: uppercase; font-weight: 800; }
    .mh-section-title { font-size: 0.75rem; color: var(--muted) !important; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 800; margin: 4px 0 8px 2px; text-align: left; border-left: 3px solid var(--green); padding-left: 8px; }
    .st-key-fa_misafir_nav .stButton button { height: 68px !important; font-size: 0.95rem !important; font-weight: 900 !important; border-radius: 16px !important; letter-spacing: 0.4px; box-shadow: 0 10px 28px rgba(34,197,94,0.3) !important; transition: all 0.25s ease; }
    .st-key-fa_misafir_nav .stButton button:hover { transform: translateY(-3px); box-shadow: 0 16px 40px rgba(34,197,94,0.5) !important; }
    .st-key-fa_misafir_nav .stButton button p { font-size: 0.95rem !important; font-weight: 900 !important; }
    .mh-info { background: linear-gradient(145deg, rgba(19,28,46,0.7), rgba(11,18,32,0.9)); border: 1px solid var(--border); border-radius: 14px; padding: 12px 14px; margin-top: 14px; font-size: 0.75rem; color: var(--muted) !important; line-height: 1.6; }
    .mh-info b { color: var(--green) !important; }
    ::-webkit-scrollbar { width: 7px; height: 7px; }
    ::-webkit-scrollbar-track { background: var(--bg-1); }
    ::-webkit-scrollbar-thumb { background: #2a3a56; border-radius: 99px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--green); }
    section[data-testid="stSidebar"] { background: var(--bg-1) !important; border-right: 1px solid var(--border); }
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
    .stApp .fa-card, .stApp .fa-hero, .stApp .fa-mk, .mh-stat { animation: fadeInUp 0.4s ease-out; }
</style>
""", unsafe_allow_html=True)


# ==========================================
# DOSYALAR
# ==========================================
GECMIS_DOSYA = "gecmis.json"
GELECEK_DOSYA = "gelecek.json"
AYARLAR_DOSYA = "ayarlar.json"
ADMIN_SIFRE = "Mg153759"


def _yukle(dosya):
    try:
        if os.path.exists(dosya):
            with open(dosya, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return []


def _kaydet(dosya, veri):
    try:
        with open(dosya, "w", encoding="utf-8") as f:
            json.dump(veri, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def gecmis_yukle(): return _yukle(GECMIS_DOSYA)
def gecmis_kaydet(v): _kaydet(GECMIS_DOSYA, v)
def gelecek_yukle(): return _yukle(GELECEK_DOSYA)
def gelecek_kaydet(v): _kaydet(GELECEK_DOSYA, v)


def ayarlar_yukle():
    varsayilan = {
        "ust": 65.0, "alt": 55.0, "kg_var": 57.0, "kg_yok": 72.0,
        "esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0,
    }
    try:
        if os.path.exists(AYARLAR_DOSYA):
            with open(AYARLAR_DOSYA, "r", encoding="utf-8") as f:
                yuklenen = json.load(f)
                if "1x2" in yuklenen and "esik_1" not in yuklenen:
                    eski = float(yuklenen["1x2"])
                    yuklenen["esik_1"] = eski
                    yuklenen["esik_x"] = eski
                    yuklenen["esik_2"] = eski
                varsayilan.update(yuklenen)
    except Exception:
        pass
    return varsayilan


def ayarlar_kaydet(esikler):
    try:
        with open(AYARLAR_DOSYA, "w", encoding="utf-8") as f:
            json.dump(esikler, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# ==========================================
# SAAT İŞLEMLERİ
# ==========================================
def saat_2_saat_ileri(saat_str):
    if not saat_str:
        return saat_str
    m = re.match(r'^(\d{1,2}):(\d{2})$', str(saat_str).strip())
    if not m:
        return saat_str
    try:
        saat = int(m.group(1))
        dakika = int(m.group(2))
        yeni_saat = (saat + 2) % 24
        return f"{yeni_saat:02d}:{dakika:02d}"
    except Exception:
        return saat_str


def saat_sirala_anahtari(g):
    try:
        v = g.get("veri", {}) if isinstance(g, dict) else {}
        tarih = str(v.get("tarih", "")).strip()
        saat = str(v.get("saat", "")).strip()
        gun, ay, yil = 99, 99, 9999
        if tarih:
            m = re.match(r'^(\d{1,2})\.(\d{1,2})\.(\d{2,4})$', tarih)
            if m:
                gun = int(m.group(1))
                ay = int(m.group(2))
                y_raw = m.group(3)
                yil = int(y_raw) if len(y_raw) == 4 else 2000 + int(y_raw)
        sa_h, sa_m = 99, 99
        if saat:
            m2 = re.match(r'^(\d{1,2}):(\d{2})$', saat)
            if m2:
                sa_h = int(m2.group(1))
                sa_m = int(m2.group(2))
        return (yil, ay, gun, sa_h, sa_m)
    except Exception:
        return (9999, 99, 99, 99, 99)


# ==========================================
# EŞİKLER
# ==========================================
ESIK_YUKSEK = 65.0
ESIK_ORTA = 55.0
ESIK_BELIRSIZ = 50.0
MONTE_CARLO_N = 10000


# ==========================================
# VARSAYILAN VERİ
# ==========================================
VARSAYILAN_VERI = {
    "ppg_ev": 0.0, "mpg_dep": 0.0,
    "form_str_ev": "", "form_str_dep": "",
    "siralama_ev": 0, "siralama_dep": 0,
    "puan_ev": 0, "puan_dep": 0,
    "xg_ev": 0.0, "xg_dep": 0.0,
    "atilan_ev": 0.0, "atilan_dep": 0.0,
    "yenen_ev": 0.0, "yenen_dep": 0.0,
    "clean_sheets_ev": 0.0, "clean_sheets_dep": 0.0,
    "team_scored_ev": 0.0, "team_scored_dep": 0.0,
    "team_scored_2_ev": 0.0, "team_scored_2_dep": 0.0,
    "scored_both_halves_ev": 0.0, "scored_both_halves_dep": 0.0,
    "goal_both_halves_ev": 0.0, "goal_both_halves_dep": 0.0,
    "ust05_ev": 80.0, "ust05_dep": 80.0,
    "ust15_ev": 50.0, "ust15_dep": 50.0,
    "ust25_ev": 30.0, "ust25_dep": 30.0,
    "ust35_ev": 20.0, "ust35_dep": 20.0,
    "kg_siklik_ev": 50.0, "kg_siklik_dep": 50.0,
    "btts_1h_ev": 0.0, "btts_1h_dep": 0.0,
    "btts_2h_ev": 0.0, "btts_2h_dep": 0.0,
    "btts_over15_ev": 0.0, "btts_over15_dep": 0.0,
    "btts_over25_ev": 0.0, "btts_over25_dep": 0.0,
    "tg_0_ev": 0.0, "tg_0_dep": 0.0,
    "tg_1_ev": 0.0, "tg_1_dep": 0.0,
    "tg_2_ev": 0.0, "tg_2_dep": 0.0,
    "tg_3_ev": 0.0, "tg_3_dep": 0.0,
    "tg_4_ev": 0.0, "tg_4_dep": 0.0,
    "tg_01_ev": 0.0, "tg_01_dep": 0.0,
    "tg_23_ev": 0.0, "tg_23_dep": 0.0,
    "tg_4p_ev": 0.0, "tg_4p_dep": 0.0,
    "ht_ust05_ev": 0.0, "ht_ust05_dep": 0.0,
    "ht_ust15_ev": 0.0, "ht_ust15_dep": 0.0,
    "ht_ust25_ev": 0.0, "ht_ust25_dep": 0.0,
    "wht_wft_ev": 0.0, "wht_wft_dep": 0.0,
    "wht_dft_ev": 0.0, "wht_dft_dep": 0.0,
    "wht_lft_ev": 0.0, "wht_lft_dep": 0.0,
    "dht_wft_ev": 0.0, "dht_wft_dep": 0.0,
    "dht_dft_ev": 0.0, "dht_dft_dep": 0.0,
    "dht_lft_ev": 0.0, "dht_lft_dep": 0.0,
    "lht_wft_ev": 0.0, "lht_wft_dep": 0.0,
    "lht_dft_ev": 0.0, "lht_dft_dep": 0.0,
    "lht_lft_ev": 0.0, "lht_lft_dep": 0.0,
    "galibiyet_ev": 30.0, "galibiyet_dep": 30.0,
    "beraberlik_ev": 30.0, "beraberlik_dep": 30.0,
    "maglubiyet_ev": 30.0, "maglubiyet_dep": 30.0,
    "win_1h_ev": 0.0, "win_1h_dep": 0.0,
    "draw_ht_ev": 0.0, "draw_ht_dep": 0.0,
    "lose_1h_ev": 0.0, "lose_1h_dep": 0.0,
    "win_btts_ev": 0.0, "win_btts_dep": 0.0,
    "draw_btts_ev": 0.0, "draw_btts_dep": 0.0,
    "lose_btts_ev": 0.0, "lose_btts_dep": 0.0,
    "win_over15_ev": 0.0, "win_over15_dep": 0.0,
    "lose_over15_ev": 0.0, "lose_over15_dep": 0.0,
    "takim_ev": "", "takim_dep": "",
    "skor_ev": 0, "skor_dep": 0,
    "skor_belli": False,
    "lig_ort_toplam": 0.0, "lig_ust25": 0.0, "lig_kg": 0.0,
    "saat": "", "tarih": "", "ulke": "",
    "format": "bilinmiyor", "kaynak_url": "",
}

MAX_GOL = 8
BELIRSIZLIK = 0.20
MAX_MAC_SINIRI = 200
_kilit = threading.Lock()
_ESIK_CACHE = {}


# ==========================================
# SESSION STATE
# ==========================================
if "sayfa" not in st.session_state: st.session_state.sayfa = "giris"
if "form_verileri" not in st.session_state: st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
if "gecmis_analizler" not in st.session_state: st.session_state.gecmis_analizler = gecmis_yukle()
if "gelecek_analizler" not in st.session_state: st.session_state.gelecek_analizler = gelecek_yukle()
if "kayit_yapildi" not in st.session_state: st.session_state.kayit_yapildi = False
if "gecmisten_gelindi" not in st.session_state: st.session_state.gecmisten_gelindi = False
if "gelecekten_gelindi" not in st.session_state: st.session_state.gelecekten_gelindi = False
if "silme_onay" not in st.session_state: st.session_state.silme_onay = False
if "aktif_kayit_idx" not in st.session_state: st.session_state.aktif_kayit_idx = None
if "aktif_gelecek_idx" not in st.session_state: st.session_state.aktif_gelecek_idx = None
if "okunamayan_alanlar" not in st.session_state: st.session_state.okunamayan_alanlar = []
if "manuel_bekleyen" not in st.session_state: st.session_state.manuel_bekleyen = []
if "tek_silme_onay" not in st.session_state: st.session_state.tek_silme_onay = None
if "tek_silme_gelecek" not in st.session_state: st.session_state.tek_silme_gelecek = None
if "giris_yapildi" not in st.session_state: st.session_state.giris_yapildi = True
if "rol" not in st.session_state: st.session_state.rol = "misafir"
if "admin_login_acik" not in st.session_state: st.session_state.admin_login_acik = False
if "esikler" not in st.session_state: st.session_state.esikler = ayarlar_yukle()
if "bt_market" not in st.session_state:
    st.session_state.bt_market = {"1x2": False, "kg_var": False, "kg_yok": False, "ust": False, "alt": False}
if "bt_market_esik" not in st.session_state:
    st.session_state.bt_market_esik = {
        "esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0,
        "kg_var": 70.0, "kg_yok": 70.0, "ust": 70.0, "alt": 70.0,
    }
if "bt_sonuc" not in st.session_state: st.session_state.bt_sonuc = None
if "bt_detaylar" not in st.session_state: st.session_state.bt_detaylar = []
if "toplu_cek_ozet" not in st.session_state: st.session_state.toplu_cek_ozet = None
if "gecmis_cek_ozet" not in st.session_state: st.session_state.gecmis_cek_ozet = None
if "skor_ozet" not in st.session_state: st.session_state.skor_ozet = None


def admin_mi():
    return st.session_state.get("rol") == "admin"


def esik_al(key):
    try:
        v = st.session_state.esikler.get(key)
        if v is not None: return v
    except Exception:
        pass
    return _ESIK_CACHE.get(key, 50.0)


def esik_1x2_al(secim):
    key_map = {"1": "esik_1", "X": "esik_x", "2": "esik_2"}
    k = key_map.get(secim, "")
    try:
        v = st.session_state.esikler.get(k)
        if v is not None: return v
    except Exception:
        pass
    return _ESIK_CACHE.get(k, 55.0)


# ==========================================
# ÜLKE → BAYRAK
# ==========================================
ULKE_BAYRAK = {
    "switzerland": "🇨🇭", "isviçre": "🇨🇭", "i̇sviçre": "🇨🇭",
    "england": "🏴", "ingiltere": "🏴", "i̇ngiltere": "🏴",
    "spain": "🇪🇸", "ispanya": "🇪🇸", "i̇spanya": "🇪🇸",
    "italy": "🇮🇹", "italya": "🇮🇹", "i̇talya": "🇮🇹",
    "germany": "🇩🇪", "almanya": "🇩🇪",
    "france": "🇫🇷", "fransa": "🇫🇷",
    "netherlands": "🇳🇱", "hollanda": "🇳🇱",
    "portugal": "🇵🇹", "portekiz": "🇵🇹",
    "belgium": "🇧🇪", "belçika": "🇧🇪",
    "turkey": "🇹🇷", "türkiye": "🇹🇷", "turkiye": "🇹🇷",
    "argentina": "🇦🇷", "arjantin": "🇦🇷",
    "brazil": "🇧🇷", "brezilya": "🇧🇷",
    "mexico": "🇲🇽", "meksika": "🇲🇽",
    "usa": "🇺🇸", "united states": "🇺🇸", "abd": "🇺🇸",
    "japan": "🇯🇵", "japonya": "🇯🇵",
    "south korea": "🇰🇷", "korea": "🇰🇷", "güney kore": "🇰🇷",
    "china": "🇨🇳", "çin": "🇨🇳",
    "russia": "🇷🇺", "rusya": "🇷🇺",
    "ukraine": "🇺🇦", "ukrayna": "🇺🇦",
    "poland": "🇵🇱", "polonya": "🇵🇱",
    "greece": "🇬🇷", "yunanistan": "🇬🇷",
    "scotland": "🏴", "i̇skoçya": "🏴",
    "wales": "🏴", "galler": "🏴",
    "ireland": "🇮🇪", "i̇rlanda": "🇮🇪",
    "austria": "🇦🇹", "avusturya": "🇦🇹",
    "croatia": "🇭🇷", "hırvatistan": "🇭🇷",
    "serbia": "🇷🇸", "sırbistan": "🇷🇸",
    "romania": "🇷🇴", "romanya": "🇷🇴",
    "bulgaria": "🇧🇬", "bulgaristan": "🇧🇬",
    "denmark": "🇩🇰", "danimarka": "🇩🇰",
    "sweden": "🇸🇪", "i̇sveç": "🇸🇪",
    "norway": "🇳🇴", "norveç": "🇳🇴",
    "finland": "🇫🇮", "finlandiya": "🇫🇮",
    "iceland": "🇮🇸", "i̇zlanda": "🇮🇸",
    "hungary": "🇭🇺", "macaristan": "🇭🇺",
    "czech": "🇨🇿", "çekya": "🇨🇿",
    "slovakia": "🇸🇰", "slovakya": "🇸🇰",
    "slovenia": "🇸🇮", "slovenya": "🇸🇮",
    "saudi": "🇸🇦", "suudi arabistan": "🇸🇦",
    "uae": "🇦🇪", "qatar": "🇶🇦", "katar": "🇶🇦",
    "egypt": "🇪🇬", "mısır": "🇪🇬",
    "morocco": "🇲🇦", "fas": "🇲🇦",
    "algeria": "🇩🇿", "cezayir": "🇩🇿",
    "tunisia": "🇹🇳", "tunus": "🇹🇳",
    "nigeria": "🇳🇬", "nijerya": "🇳🇬",
    "south africa": "🇿🇦", "güney afrika": "🇿🇦",
    "australia": "🇦🇺", "avustralya": "🇦🇺",
    "new zealand": "🇳🇿", "yeni zelanda": "🇳🇿",
    "india": "🇮🇳", "hindistan": "🇮🇳",
    "iran": "🇮🇷", "iraq": "🇮🇶", "irak": "🇮🇶",
    "israel": "🇮🇱", "i̇srail": "🇮🇱",
    "colombia": "🇨🇴", "kolombiya": "🇨🇴",
    "chile": "🇨🇱", "şili": "🇨🇱",
    "peru": "🇵🇪", "uruguay": "🇺🇾",
    "ecuador": "🇪🇨", "ekvador": "🇪🇨",
    "paraguay": "🇵🇾",
    "bolivia": "🇧🇴", "bolivya": "🇧🇴",
    "venezuela": "🇻🇪",
    "costa rica": "🇨🇷", "panama": "🇵🇦", "jamaica": "🇯🇲",
    "canada": "🇨🇦", "kanada": "🇨🇦",
    "kosovo": "🇽🇰", "kosova": "🇽🇰",
    "albania": "🇦🇱", "arnavutluk": "🇦🇱",
    "moldova": "🇲🇩",
    "georgia": "🇬🇪", "gürcistan": "🇬🇪",
    "armenia": "🇦🇲", "ermenistan": "🇦🇲",
    "azerbaijan": "🇦🇿", "azerbaycan": "🇦🇿",
    "kazakhstan": "🇰🇿", "kazakistan": "🇰🇿",
    "uzbekistan": "🇺🇿", "özbekistan": "🇺🇿",
    "belarus": "🇧🇾",
    "latvia": "🇱🇻", "letonya": "🇱🇻",
    "lithuania": "🇱🇹", "litvanya": "🇱🇹",
    "estonia": "🇪🇪", "estonya": "🇪🇪",
    "luxembourg": "🇱🇺", "lüksemburg": "🇱🇺",
    "malta": "🇲🇹", "cyprus": "🇨🇾", "kıbrıs": "🇨🇾",
    "montenegro": "🇲🇪", "karadağ": "🇲🇪",
    "north macedonia": "🇲🇰", "kuzey makedonya": "🇲🇰",
    "bosnia": "🇧🇦", "bosna": "🇧🇦",
    "liechtenstein": "🇱🇮", "andorra": "🇦🇩",
    "san marino": "🇸🇲", "gibraltar": "🇬🇮", "faroe": "🇫🇴",
}


def ulke_bayrak_bul(ulke_adi):
    if not ulke_adi:
        return "🌍"
    u = ulke_adi.lower().strip()
    for anahtar in sorted(ULKE_BAYRAK.keys(), key=len, reverse=True):
        if anahtar in u:
            return ULKE_BAYRAK[anahtar]
    return "🌍"


def _ulke_bul(metin):
    m = re.search(r'Standings\s+([^\n]+)', metin)
    if not m:
        return ""
    satir = m.group(1).strip()
    if not satir:
        return ""
    alt = satir.lower()
    for anahtar in sorted(ULKE_BAYRAK.keys(), key=len, reverse=True):
        if anahtar in alt:
            return anahtar
    parcalar = satir.split()
    return " ".join(parcalar[:2]) if len(parcalar) >= 2 else (parcalar[0] if parcalar else "")


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def ort_iki(a, b):
    vals = [x for x in [a, b] if x is not None and x > 0]
    if not vals: return 0
    return sum(vals) / len(vals)


def guven_seviyesi_bul(olasilik):
    if olasilik >= ESIK_YUKSEK: return ("yuksek", "🟢", "success", "Yüksek")
    if olasilik >= ESIK_ORTA:   return ("orta", "🟡", "warning", "Orta")
    if olasilik >= ESIK_BELIRSIZ: return ("belirsiz", "🔴", "error", "Belirsiz")
    return ("cok_dusuk", "⚫", "error", "Düşük")


def oneri_istatistik_guncel(gecmis):
    ist = {"1x2": {"tam": 0, "yakin": 0, "yanlis": 0},
           "gol": {"tam": 0, "yakin": 0, "yanlis": 0},
           "kg": {"tam": 0, "yakin": 0, "yanlis": 0}}
    for g in gecmis:
        try:
            v = g["veri"]
            if not v.get("skor_belli", False):
                continue
            try:
                ya = yeniden_analiz(v)
            except Exception:
                ya = g.get("analiz", {})
            d = sonuc_hesapla({"veri": v, "analiz": ya})
            if not d:
                continue
            for key in ["oneri_1x2", "oneri_gol", "oneri_kg"]:
                kisa = key.replace("oneri_", "")
                durum = d[key].get("durum")
                if durum == "tam": ist[kisa]["tam"] += 1
                elif durum == "yanlis": ist[kisa]["yanlis"] += 1
        except Exception:
            continue
    return ist


def wilson_aralik(dogru, toplam, z=1.96):
    if toplam <= 0:
        return 0.0, 0.0
    p = dogru / toplam
    payda = 1 + z * z / toplam
    merkez = (p + z * z / (2 * toplam)) / payda
    yari = z * math.sqrt(p * (1 - p) / toplam + z * z / (4 * toplam * toplam)) / payda
    return max(0.0, (merkez - yari) * 100), min(100.0, (merkez + yari) * 100)


def _form_ppg(s):
    return sum(3 if c == "W" else 1 if c == "D" else 0 for c in s) / max(len(s), 1)


def yeniden_analiz(v):
    v2 = copy.deepcopy(v)
    if v2.get("form_str_ev"):
        v2["ppg_ev"] = _form_ppg(v2["form_str_ev"])
    if v2.get("form_str_dep"):
        v2["mpg_dep"] = _form_ppg(v2["form_str_dep"])
    anahtar = json.dumps(v2, sort_keys=True, ensure_ascii=False)
    if "bt_analiz_cache" not in st.session_state:
        st.session_state.bt_analiz_cache = {}
    cache = st.session_state.bt_analiz_cache
    if anahtar not in cache:
        a = analiz_hesapla(v2)
        cache[anahtar] = {
            "ust_25": a["ust_25"], "kg_var_model": a["kg_var_model"],
            "p1": a["p1"], "px": a["px"], "p2": a["p2"],
        }
    return cache[anahtar]


def backtest_hesapla(gecmis, market_sec, market_esik):
    sonuc = {"1x2": {"dogru": 0, "yanlis": 0}, "kg_var": {"dogru": 0, "yanlis": 0},
             "kg_yok": {"dogru": 0, "yanlis": 0}, "ust": {"dogru": 0, "yanlis": 0},
             "alt": {"dogru": 0, "yanlis": 0}}
    mac_detaylari = []
    for g in gecmis:
        try:
            v = g["veri"]; analiz = g.get("analiz", {})
            if not v.get("skor_belli", False): continue
            skor_ev = int(v.get("skor_ev", 0)); skor_dep = int(v.get("skor_dep", 0))
            toplam_gol = skor_ev + skor_dep
            gercek_kg_var = (skor_ev > 0 and skor_dep > 0)
            gercek_ust = toplam_gol > 2.5
            if skor_ev > skor_dep: gercek_1x2 = "1"
            elif skor_ev == skor_dep: gercek_1x2 = "X"
            else: gercek_1x2 = "2"
            try:
                yeni_analiz = yeniden_analiz(v)
                ust_25 = yeni_analiz["ust_25"]; kg_var = yeni_analiz["kg_var_model"]
                p1_y = yeni_analiz["p1"]; px_y = yeni_analiz["px"]; p2_y = yeni_analiz["p2"]
            except Exception:
                ust_25 = analiz.get("ust_25", 50); kg_var = analiz.get("kg_var_model", 50)
                p1_y = analiz.get("p1", 33.33); px_y = analiz.get("px", 33.33); p2_y = analiz.get("p2", 33.34)
            alt_25 = 100 - ust_25; kg_yok = 100 - kg_var
            mac_kayit = {"takim_ev": v.get("takim_ev", "Ev"), "takim_dep": v.get("takim_dep", "Dep"),
                         "skor": f"{skor_ev}-{skor_dep}",
                         "gercek_kg": "Var" if gercek_kg_var else "Yok",
                         "gercek_gol": "Üst" if gercek_ust else "Alt",
                         "gercek_1x2": gercek_1x2, "detaylar": []}
            if market_sec.get("1x2", False):
                en_yuksek = max([("1", p1_y), ("X", px_y), ("2", p2_y)], key=lambda x: x[1])
                secim, yuzde = en_yuksek
                esik_key = {"1": "esik_1", "X": "esik_x", "2": "esik_2"}[secim]
                esik_secim = market_esik.get(esik_key, 55.0)
                if yuzde >= esik_secim:
                    if secim == gercek_1x2:
                        sonuc["1x2"]["dogru"] += 1
                        mac_kayit["detaylar"].append(f"1X2: {secim} ✅ (%{yuzde:.1f} ≥ %{esik_secim:.0f})")
                    else:
                        sonuc["1x2"]["yanlis"] += 1
                        mac_kayit["detaylar"].append(f"1X2: {secim} ❌ (gerçek: {gercek_1x2}, %{yuzde:.1f} ≥ %{esik_secim:.0f})")
            if market_sec.get("kg_var", False):
                if kg_var >= market_esik["kg_var"] and kg_var >= kg_yok:
                    if gercek_kg_var:
                        sonuc["kg_var"]["dogru"] += 1; mac_kayit["detaylar"].append("KG Var ✅")
                    else:
                        sonuc["kg_var"]["yanlis"] += 1; mac_kayit["detaylar"].append("KG Var ❌")
            if market_sec.get("kg_yok", False):
                if kg_yok >= market_esik["kg_yok"] and kg_yok >= kg_var:
                    if not gercek_kg_var:
                        sonuc["kg_yok"]["dogru"] += 1; mac_kayit["detaylar"].append("KG Yok ✅")
                    else:
                        sonuc["kg_yok"]["yanlis"] += 1; mac_kayit["detaylar"].append("KG Yok ❌")
            if market_sec.get("ust", False):
                if ust_25 >= market_esik["ust"] and ust_25 >= alt_25:
                    if gercek_ust:
                        sonuc["ust"]["dogru"] += 1; mac_kayit["detaylar"].append("Üst ✅")
                    else:
                        sonuc["ust"]["yanlis"] += 1; mac_kayit["detaylar"].append("Üst ❌")
            if market_sec.get("alt", False):
                if alt_25 >= market_esik["alt"] and alt_25 >= ust_25:
                    if not gercek_ust:
                        sonuc["alt"]["dogru"] += 1; mac_kayit["detaylar"].append("Alt ✅")
                    else:
                        sonuc["alt"]["yanlis"] += 1; mac_kayit["detaylar"].append("Alt ❌")
            if mac_kayit["detaylar"]:
                mac_detaylari.append(mac_kayit)
        except Exception:
            continue
    return sonuc, mac_detaylari


MANUEL_ALANLAR = {
    "Sıralama": [("siralama_ev", "Ev Sıralaması", "int", 1), ("siralama_dep", "Dep Sıralaması", "int", 1)],
    "Takım isimleri (Ev)": [("takim_ev", "Ev Takım Adı", "str", "")],
    "Takım isimleri (Dep)": [("takim_dep", "Dep Takım Adı", "str", "")],
    "PPG (Ev Form)": [("ppg_ev", "PPG (Ev)", "float", 0.0)],
    "MPG (Dep Form)": [("mpg_dep", "MPG (Dep)", "float", 0.0)],
    "xG": [("xg_ev", "xG (Ev)", "float", 0.0), ("xg_dep", "xG (Dep)", "float", 0.0)],
    "Atılan Gol": [("atilan_ev", "Atılan Gol (Ev)", "float", 0.0), ("atilan_dep", "Atılan Gol (Dep)", "float", 0.0)],
    "Yenen Gol": [("yenen_ev", "Yenen Gol (Ev)", "float", 0.0), ("yenen_dep", "Yenen Gol (Dep)", "float", 0.0)],
}


def _cift_tab(etiket, blok):
    pattern = r'([\d.,]+)%?\s*\t\s*' + re.escape(etiket) + r'\s*\t\s*([\d.,]+)%?'
    m = re.search(pattern, blok, re.IGNORECASE)
    if m:
        try: return float(m.group(1).replace(",", ".")), float(m.group(2).replace(",", "."))
        except ValueError: pass
    pattern2 = r'([\d.,]+)%?\s{1,4}' + re.escape(etiket) + r'\s{1,4}([\d.,]+)%?'
    m = re.search(pattern2, blok, re.IGNORECASE)
    if m:
        try: return float(m.group(1).replace(",", ".")), float(m.group(2).replace(",", "."))
        except ValueError: pass
    return None, None


def _sira_bul(metin, takim_adi):
    if not takim_adi: return None, None
    pattern = (r'(?:^|\n)\s*(\d{1,2})\s*\r?\n\s*' + re.escape(takim_adi) + r'\s*\r?\n\s*'
               + re.escape(takim_adi) + r'\s*\r?\n' r'\s*(\d+)\s*\t')
    m = re.search(pattern, metin, re.MULTILINE)
    if m:
        try:
            sira = int(m.group(1))
            if 1 <= sira <= 30:
                devam = metin[m.end()-1:]
                m_puan = re.match(r'[\s\S]{0,80}?\r?\n\s*(\d{1,2})\s*\r?\n', devam)
                puan = int(m_puan.group(1)) if m_puan else 0
                return sira, puan
        except (ValueError, AttributeError): pass
    pattern2 = (r'(?:^|\n)\s*(\d{1,2})\s*\r?\n\s*\r?\n\s*'
                + re.escape(takim_adi) + r'\s*\r?\n\s*' + re.escape(takim_adi))
    m = re.search(pattern2, metin, re.MULTILINE)
    if m:
        try:
            sira = int(m.group(1))
            if 1 <= sira <= 30: return sira, 0
        except ValueError: pass
    return None, None


def sportytrader_veri_cikar(metin):
    veri = {}; okunamayanlar = []
    m = re.search(r'^([A-ZÇĞİÖŞÜ][\w\s\.\-]+?)\s*-\s*([A-ZÇĞİÖŞÜ][\w\s\.\-]+?)\s+Stats', metin, re.MULTILINE)
    if m:
        veri["takim_ev"] = m.group(1).strip(); veri["takim_dep"] = m.group(2).strip()
    m = re.search(r'Time\s*\t\s*(\d{1,2}:\d{2})', metin)
    if m: veri["saat"] = m.group(1).strip()
    else:
        m = re.search(r'\d{1,2}\.\d{1,2}\.\d{2,4}\s+(\d{1,2}:\d{2})', metin)
        if m: veri["saat"] = m.group(1).strip()
    m = re.search(r'Date\s*\t\s*(\d{1,2}\.\d{1,2}\.\d{2,4})', metin)
    if m: veri["tarih"] = m.group(1).strip()
    else:
        m = re.search(r'(\d{1,2}\.\d{1,2}\.\d{2,4})\s+\d{1,2}:\d{2}', metin)
        if m: veri["tarih"] = m.group(1).strip()
    veri["ulke"] = _ulke_bul(metin)
    m = re.search(r'FT\s*\r?\n\s*(\d+)\s*-\s*(\d+)', metin)
    if m:
        veri["skor_ev"] = int(m.group(1)); veri["skor_dep"] = int(m.group(2)); veri["skor_belli"] = True
    else:
        veri["skor_belli"] = False
    takim_ev = veri.get("takim_ev", ""); takim_dep = veri.get("takim_dep", "")
    idx = metin.find("Main Stats")
    if idx != -1:
        blok = metin[idx:idx+1500]
        v1, v2 = _cift_tab("Goals scored per game", blok)
        if v1 is not None: veri["atilan_ev"] = v1; veri["atilan_dep"] = v2
        v1, v2 = _cift_tab("Goals conceded per game", blok)
        if v1 is not None: veri["yenen_ev"] = v1; veri["yenen_dep"] = v2
        v1, v2 = _cift_tab("Clean sheets", blok)
        if v1 is not None: veri["clean_sheets_ev"] = v1; veri["clean_sheets_dep"] = v2
        v1, v2 = _cift_tab("Team scored", blok)
        if v1 is not None: veri["team_scored_ev"] = v1; veri["team_scored_dep"] = v2
    idx = metin.find("Win Draw Lose")
    if idx != -1:
        blok = metin[idx:idx+1500]
        for etiket, key_ev, key_dep in [("Win", "galibiyet_ev", "galibiyet_dep"),
                                        ("Draw", "beraberlik_ev", "beraberlik_dep"),
                                        ("Lose", "maglubiyet_ev", "maglubiyet_dep")]:
            pattern = r'(?:^|\n)\s*([\d.,]+)%\s*\t\s*' + etiket + r'\s*\t\s*([\d.,]+)%'
            mm = re.search(pattern, blok, re.MULTILINE)
            if mm:
                try:
                    veri[key_ev] = float(mm.group(1).replace(",", "."))
                    veri[key_dep] = float(mm.group(2).replace(",", "."))
                except ValueError: pass
    idx = metin.find("Both Teams to Score")
    if idx != -1:
        blok = metin[idx:idx+1500]
        m = re.search(r'(?:^|\n)\s*([\d.,]+)%\s*\t\s*Both Teams to Score\s*\t\s*([\d.,]+)%', blok, re.MULTILINE)
        if m:
            try:
                veri["kg_siklik_ev"] = float(m.group(1).replace(",", "."))
                veri["kg_siklik_dep"] = float(m.group(2).replace(",", "."))
            except ValueError: pass
    idx = metin.find("Over Under Goals")
    if idx != -1:
        blok = metin[idx:idx+1500]
        v1, v2 = _cift_tab("Over 1.5 goals", blok)
        if v1 is not None: veri["ust15_ev"] = v1; veri["ust15_dep"] = v2
        v1, v2 = _cift_tab("Over 2.5 goals", blok)
        if v1 is not None: veri["ust25_ev"] = v1; veri["ust25_dep"] = v2
        v1, v2 = _cift_tab("Over 3.5 goals", blok)
        if v1 is not None: veri["ust35_ev"] = v1; veri["ust35_dep"] = v2
    if takim_ev:
        s, p = _sira_bul(metin, takim_ev)
        if s is not None: veri["siralama_ev"] = s
    if takim_dep:
        s, p = _sira_bul(metin, takim_dep)
        if s is not None: veri["siralama_dep"] = s
    if veri.get("siralama_ev", 0) == 0: okunamayanlar.append("Sıralama (Ev)")
    if veri.get("siralama_dep", 0) == 0: okunamayanlar.append("Sıralama (Dep)")
    if veri.get("atilan_ev", 0) > 0 and veri.get("yenen_ev", 0) > 0:
        veri["lig_ort_toplam"] = (veri.get("atilan_ev", 0) + veri.get("atilan_dep", 0) +
                                  veri.get("yenen_ev", 0) + veri.get("yenen_dep", 0)) / 2
    if veri.get("ust25_ev", 0) > 0 and veri.get("ust25_dep", 0) > 0:
        veri["lig_ust25"] = (veri["ust25_ev"] + veri["ust25_dep"]) / 2
    if veri.get("kg_siklik_ev", 0) > 0 and veri.get("kg_siklik_dep", 0) > 0:
        veri["lig_kg"] = (veri["kg_siklik_ev"] + veri["kg_siklik_dep"]) / 2
    veri["format"] = "sportytrader"
    return veri, okunamayanlar


def metinden_veri_cikar(metin):
    metin = metin.replace(",", ".")
    if "Main Stats" in metin and "Goals scored per game" in metin:
        veri, okunamayanlar = sportytrader_veri_cikar(metin)
        if not veri.get("takim_ev"): okunamayanlar.append("Takım isimleri (Ev)")
        if not veri.get("takim_dep"): okunamayanlar.append("Takım isimleri (Dep)")
        if veri.get("saat"):
            veri["saat"] = saat_2_saat_ileri(veri["saat"])
        return veri, okunamayanlar
    veri = {}; okunamayanlar = []
    veri["format"] = "genel"
    return veri, okunamayanlar


def poisson_pmf(k, lam):
    if lam <= 0: return 1.0 if k == 0 else 0.0
    return (math.exp(-lam) * (lam ** k)) / math.factorial(k)


def poisson_random(lam, rng=None):
    r = rng if rng is not None else random
    if lam <= 0: return 0
    L = math.exp(-lam); k = 0; p = 1.0
    while True:
        k += 1; p *= r.random()
        if p <= L: return k - 1


def poisson_matris(lam_ev, lam_dep, max_gol=MAX_GOL):
    return [[poisson_pmf(i, lam_ev) * poisson_pmf(j, lam_dep) for j in range(max_gol)] for i in range(max_gol)]


def hesapla_lambda(v):
    atilan_e = v.get("atilan_ev", 0.0); yenen_e = v.get("yenen_ev", 0.0)
    atilan_d = v.get("atilan_dep", 0.0); yenen_d = v.get("yenen_dep", 0.0)
    xg_e = v.get("xg_ev", 0.0); xg_d = v.get("xg_dep", 0.0)
    if xg_e > 0: hucum_ev_baz = (xg_e * 0.60) + (atilan_e * 0.40)
    else: hucum_ev_baz = atilan_e if atilan_e > 0 else 1.2
    if xg_d > 0: hucum_dep_baz = (xg_d * 0.60) + (atilan_d * 0.40)
    else: hucum_dep_baz = atilan_d if atilan_d > 0 else 1.0
    ts_ev = v.get("team_scored_ev", 0); ts_dep = v.get("team_scored_dep", 0)
    if ts_ev > 0: hucum_ev_baz *= clamp(ts_ev / 60, 0.7, 1.3)
    if ts_dep > 0: hucum_dep_baz *= clamp(ts_dep / 60, 0.7, 1.3)
    savunma_dep_zaaf = yenen_d if yenen_d > 0 else 1.2
    savunma_ev_zaaf = yenen_e if yenen_e > 0 else 1.0
    cs_ev = v.get("clean_sheets_ev", 0.0); cs_dep = v.get("clean_sheets_dep", 0.0)
    def clean_sheet_freni(cs_orani):
        if cs_orani <= 0: return 1.0
        if cs_orani < 40.0: return 1.0 - (cs_orani / 250.0)
        return max(0.40, 0.84 - (cs_orani - 40.0) * (0.44 / 60.0))
    dep_freni = clean_sheet_freni(cs_ev); ev_freni = clean_sheet_freni(cs_dep)
    lam_ev_ham = (hucum_ev_baz * 0.60) + (savunma_dep_zaaf * 0.40)
    lam_dep_ham = (hucum_dep_baz * 0.60) + (savunma_ev_zaaf * 0.40)
    ust25_e = v.get("ust25_ev", 0); ust25_d = v.get("ust25_dep", 0)
    if ust25_e > 0: lam_ev_ham *= clamp(ust25_e / 50, 0.85, 1.15)
    if ust25_d > 0: lam_dep_ham *= clamp(ust25_d / 50, 0.85, 1.15)
    kg_e = v.get("kg_siklik_ev", 0); kg_d = v.get("kg_siklik_dep", 0)
    if kg_e > 0 and kg_d > 0:
        kg_ort = (kg_e + kg_d) / 2
        if kg_ort >= 60: lam_ev_ham *= 1.05; lam_dep_ham *= 1.05
        elif kg_ort <= 35: lam_ev_ham *= 0.95; lam_dep_ham *= 0.95
    form_ev = clamp(1 + (v.get("ppg_ev", 1.5) - 1.5) / 15, 0.85, 1.15)
    form_dep = clamp(1 + (v.get("mpg_dep", 1.5) - 1.5) / 15, 0.85, 1.15)
    sira_e = v.get("siralama_ev", 10); sira_d = v.get("siralama_dep", 10)
    dominasyon_bonus_ev = 1.0
    if 1 <= sira_e <= 5 and sira_d >= 10: dominasyon_bonus_ev = 1.20
    gal_ev = v.get("galibiyet_ev", 0); gal_dep = v.get("galibiyet_dep", 0)
    if gal_ev > 0 and gal_dep > 0:
        if gal_ev - gal_dep >= 25: lam_ev_ham *= 1.08; lam_dep_ham *= 0.95
        elif gal_dep - gal_ev >= 25: lam_ev_ham *= 0.95; lam_dep_ham *= 1.08
    lam_ev = lam_ev_ham * 1.05 * form_ev * ev_freni * dominasyon_bonus_ev
    lam_dep = lam_dep_ham * 0.95 * form_dep * dep_freni
    if lam_ev > 2.50: lam_ev = 2.50 + (lam_ev - 2.50) * 0.5
    if lam_dep > 2.50: lam_dep = 2.50 + (lam_dep - 2.50) * 0.5
    return clamp(lam_ev, 0.05, 4.5), clamp(lam_dep, 0.05, 4.5), 0.80


def matristen_olasilik(matris, max_gol=MAX_GOL):
    p1 = px = p2 = 0.0
    ust_05 = ust_15 = ust_25 = ust_35 = 0.0
    kg_var = 0.0; skorlar = {}; toplam = 0.0
    for i in range(max_gol):
        for j in range(max_gol):
            p = matris[i][j]; toplam += p
            if i > j: p1 += p
            elif i == j: px += p
            else: p2 += p
            tg = i + j
            if tg > 0.5: ust_05 += p
            if tg > 1.5: ust_15 += p
            if tg > 2.5: ust_25 += p
            if tg > 3.5: ust_35 += p
            if i > 0 and j > 0: kg_var += p
            skorlar[f"{i}-{j}"] = p
    return {"1": p1, "X": px, "2": p2, "ust_05": ust_05, "ust_15": ust_15,
            "ust_25": ust_25, "ust_35": ust_35, "kg_var": kg_var, "skorlar": skorlar, "toplam": toplam}


def veri_yeterli_mi(v):
    onemli = [v.get("atilan_ev", 0), v.get("atilan_dep", 0), v.get("yenen_ev", 0), v.get("yenen_dep", 0)]
    return sum(1 for x in onemli if x > 0) >= 2


def mac_ici_sok(lam_ev, lam_dep, rng=None):
    r = rng if rng is not None else random
    if r.random() < 0.03:
        if r.random() < 0.5: lam_ev *= 0.70
        else: lam_dep *= 0.70
    return lam_ev, lam_dep


def monte_carlo_simulasyon(lam_ev_base, lam_dep_base, n=MONTE_CARLO_N):
    seed = int(round(lam_ev_base * 1_000_000)) * 1_000_003 + int(round(lam_dep_base * 1_000_000))
    rng = random.Random(seed)
    sayac = {"1": 0, "X": 0, "2": 0, "ust25": 0, "kg_var": 0}
    for _ in range(n):
        sapma_ev = rng.uniform(1 - BELIRSIZLIK, 1 + BELIRSIZLIK)
        sapma_dep = rng.uniform(1 - BELIRSIZLIK, 1 + BELIRSIZLIK)
        lam_ev = lam_ev_base * sapma_ev; lam_dep = lam_dep_base * sapma_dep
        lam_ev, lam_dep = mac_ici_sok(lam_ev, lam_dep, rng)
        ev_gol = min(MAX_GOL - 1, poisson_random(lam_ev, rng))
        dep_gol = min(MAX_GOL - 1, poisson_random(lam_dep, rng))
        if ev_gol > dep_gol: sayac["1"] += 1
        elif ev_gol == dep_gol: sayac["X"] += 1
        else: sayac["2"] += 1
        if ev_gol + dep_gol > 2.5: sayac["ust25"] += 1
        if ev_gol > 0 and dep_gol > 0: sayac["kg_var"] += 1
    def yuzde(s): return s / n * 100 if n > 0 else 0
    return {"p1": yuzde(sayac["1"]), "px": yuzde(sayac["X"]), "p2": yuzde(sayac["2"]),
            "ust25": yuzde(sayac["ust25"]), "alt25": 100 - yuzde(sayac["ust25"]),
            "kg_var": yuzde(sayac["kg_var"]), "kg_yok": 100 - yuzde(sayac["kg_var"]), "n": n}


def analiz_hesapla(v):
    lam_ev, lam_dep, guven = hesapla_lambda(v)
    matris = poisson_matris(lam_ev, lam_dep, MAX_GOL)
    olas = matristen_olasilik(matris, MAX_GOL)
    toplam = olas["toplam"] or 1
    p1_po = olas["1"] / toplam * 100
    px_po = olas["X"] / toplam * 100
    p2_po = olas["2"] / toplam * 100
    ust25_po = olas["ust_25"] / toplam * 100
    kg_var_po = olas["kg_var"] / toplam * 100
    mc = monte_carlo_simulasyon(lam_ev, lam_dep, MONTE_CARLO_N)
    p1_mc = mc["p1"]; px_mc = mc["px"]; p2_mc = mc["p2"]
    ust25_mc = mc["ust25"]; kg_var_mc = mc["kg_var"]
    lig_ust25 = v.get("lig_ust25", 0.0); lig_kg = v.get("lig_kg", 0.0)
    ust15_e = v.get("ust15_ev", 0); ust15_d = v.get("ust15_dep", 0)
    ust35_e = v.get("ust35_ev", 0); ust35_d = v.get("ust35_dep", 0)
    kg_sik_e = v.get("kg_siklik_ev", 0); kg_sik_d = v.get("kg_siklik_dep", 0)
    btts_1h_e = v.get("btts_1h_ev", 0); btts_1h_d = v.get("btts_1h_dep", 0)
    btts_2h_e = v.get("btts_2h_ev", 0); btts_2h_d = v.get("btts_2h_dep", 0)
    tg_0_e = v.get("tg_0_ev", 0); tg_0_d = v.get("tg_0_dep", 0)
    tg_1_e = v.get("tg_1_ev", 0); tg_1_d = v.get("tg_1_dep", 0)
    tg_2_e = v.get("tg_2_ev", 0); tg_2_d = v.get("tg_2_dep", 0)
    tg_3_e = v.get("tg_3_ev", 0); tg_3_d = v.get("tg_3_dep", 0)
    tg_4_e = v.get("tg_4_ev", 0); tg_4_d = v.get("tg_4_dep", 0)
    gal_e = v.get("galibiyet_ev", 0); gal_d = v.get("galibiyet_dep", 0)
    ber_e = v.get("beraberlik_ev", 0); ber_d = v.get("beraberlik_dep", 0)
    p1 = (p1_po * 0.60) + (p1_mc * 0.40)
    px = (px_po * 0.60) + (px_mc * 0.40)
    p2 = (p2_po * 0.60) + (p2_mc * 0.40)
    if gal_e > 0 and gal_d > 0:
        p1 = (p1 * 0.85) + (gal_e * 0.15)
        p2 = (p2 * 0.85) + (gal_d * 0.15)
    if ber_e > 0 and ber_d > 0:
        ber_ort = (ber_e + ber_d) / 2
        px = (px * 0.85) + (ber_ort * 0.15)
    t = p1 + px + p2
    if t > 0: p1, px, p2 = (p1 / t) * 100, (px / t) * 100, (p2 / t) * 100
    if lig_ust25 > 0:
        ust_25 = (ust25_po * 0.60) + (lig_ust25 * 0.10) + (ust25_mc * 0.30)
    else:
        ust_25 = (ust25_po * 0.65) + (ust25_mc * 0.35)
    if ust15_e > 0 and ust15_d > 0:
        u15_ort = (ust15_e + ust15_d) / 2
        if u15_ort >= 70: ust_25 = (ust_25 * 0.90) + (u15_ort * 0.10)
    if ust35_e > 0 and ust35_d > 0:
        u35_ort = (ust35_e + ust35_d) / 2
        if u35_ort >= 40: ust_25 = (ust_25 * 0.92) + (u35_ort * 0.08)
    tg_3p = ort_iki((tg_3_e + tg_4_e) if (tg_3_e > 0 or tg_4_e > 0) else 0,
                    (tg_3_d + tg_4_d) if (tg_3_d > 0 or tg_4_d > 0) else 0)
    if tg_3p > 0:
        ust_egilim = tg_3p
        if ust_egilim >= 50: ust_25 = (ust_25 * 0.93) + (ust_egilim * 0.07)
    if lig_kg > 0:
        kg_var_model = (kg_var_po * 0.40) + (lig_kg * 0.30) + (kg_var_mc * 0.30)
    else:
        kg_var_model = (kg_var_po * 0.60) + (kg_var_mc * 0.40)
    if kg_sik_e > 0 and kg_sik_d > 0:
        kg_ort = (kg_sik_e + kg_sik_d) / 2
        kg_var_model = (kg_var_model * 0.85) + (kg_ort * 0.15)
    if btts_1h_e > 0 and btts_1h_d > 0:
        btts_1h_ort = (btts_1h_e + btts_1h_d) / 2
        if btts_1h_ort >= 30: kg_var_model = (kg_var_model * 0.95) + (btts_1h_ort * 0.05)
    if btts_2h_e > 0 and btts_2h_d > 0:
        btts_2h_ort = (btts_2h_e + btts_2h_d) / 2
        if btts_2h_ort >= 30: kg_var_model = (kg_var_model * 0.95) + (btts_2h_ort * 0.05)
    tg_0_ort = ort_iki(tg_0_e, tg_0_d); tg_1_ort = ort_iki(tg_1_e, tg_1_d)
    if tg_0_ort >= 15 or tg_1_ort >= 15:
        kg_yoklama = tg_0_ort + tg_1_ort
        if kg_yoklama >= 30: kg_var_model = (kg_var_model * 0.90) + ((100 - kg_yoklama) * 0.10)
    toplam_beklenen_gol = lam_ev + lam_dep
    if toplam_beklenen_gol < 1.80:
        baski_faktoru = (1.80 - toplam_beklenen_gol) / 1.80
        ust_25 = max(10.0, ust_25 * (1.0 - baski_faktoru * 0.8))
        kg_var_model = max(15.0, kg_var_model * (1.0 - baski_faktoru * 0.9))
    cs_ev = v.get("clean_sheets_ev", 0.0); cs_dep = v.get("clean_sheets_dep", 0.0)
    if cs_ev >= 50.0 and lam_dep < 1.0: kg_var_model *= 0.80
    if cs_dep >= 50.0 and lam_ev < 1.0: kg_var_model *= 0.80
    kg_yok_model = 100.0 - kg_var_model
    if kg_yok_model > 68.0 and p1 > 55.0 and lam_ev >= 1.70:
        ust_25 = min(68.0, ust_25 * 1.35)
    alt_25 = 100.0 - ust_25
    tahmini_gol = lam_ev + lam_dep
    en_olasi = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
    en_guvenli = max([("1X", p1+px), ("X2", p2+px), ("12", p1+p2)], key=lambda x: x[1])
    en_olasi_gol = "Üst" if ust_25 > alt_25 else "Alt"
    en_olasi_kg = "Var" if kg_var_model > kg_yok_model else "Yok"
    return {
        "lam_ev": lam_ev, "lam_dep": lam_dep, "guven": guven, "matris": matris, "olas": olas,
        "p1": p1, "px": px, "p2": p2,
        "cifte_1x": p1 + px, "cifte_x2": p2 + px, "cifte_12": p1 + p2,
        "tahmini_gol": tahmini_gol, "ust_25": ust_25, "alt_25": alt_25,
        "kg_var_model": kg_var_model, "kg_yok_model": kg_yok_model,
        "en_olasi": en_olasi, "en_guvenli": en_guvenli,
        "en_olasi_gol": en_olasi_gol, "en_olasi_kg": en_olasi_kg,
        "p1_po": p1_po, "px_po": px_po, "p2_po": p2_po, "ust25_po": ust25_po, "kg_var_po": kg_var_po,
        "p1_lig": 0, "px_lig": 0, "p2_lig": 0,
        "ust25_lig": lig_ust25, "kg_var_lig": lig_kg,
        "p1_mc": p1_mc, "px_mc": px_mc, "p2_mc": p2_mc, "ust25_mc": ust25_mc, "kg_var_mc": kg_var_mc,
        "mc_n": mc["n"]
    }


def kayit_olustur(v, a):
    return {"veri": copy.deepcopy(v), "analiz": {
        "p1": a["p1"], "px": a["px"], "p2": a["p2"],
        "tahmini_gol": a["tahmini_gol"], "kg_var_model": a["kg_var_model"], "ust_25": a["ust_25"],
        "en_olasi_1x2": a["en_olasi"][0], "en_guvenli_cifte": a["en_guvenli"][0],
        "en_olasi_gol": a["en_olasi_gol"], "en_olasi_kg": a["en_olasi_kg"]}}


def sonuc_hesapla(kayit):
    v = kayit["veri"]; analiz = kayit.get("analiz", {})
    if not v.get("skor_belli", False): return None
    skor_ev = v.get("skor_ev", 0); skor_dep = v.get("skor_dep", 0)
    toplam_gol = skor_ev + skor_dep
    gercek_ust = toplam_gol > 2.5
    gercek_kg_var = (skor_ev > 0 and skor_dep > 0)
    if skor_ev > skor_dep: gercek_1x2 = "1"
    elif skor_ev == skor_dep: gercek_1x2 = "X"
    else: gercek_1x2 = "2"
    ust_25 = analiz.get("ust_25", 50); alt_25 = 100 - ust_25
    kg_var = analiz.get("kg_var_model", 50); kg_yok = 100 - kg_var
    p1_a = analiz.get("p1", 33.33); px_a = analiz.get("px", 33.33); p2_a = analiz.get("p2", 33.34)
    en_yuksek_1x2 = max([("1", p1_a), ("X", px_a), ("2", p2_a)], key=lambda x: x[1])
    secim_1x2, yuzde_1x2 = en_yuksek_1x2
    oneri_1x2 = None
    if yuzde_1x2 >= esik_1x2_al(secim_1x2): oneri_1x2 = secim_1x2
    oneri_gol = None
    if ust_25 >= esik_al("ust") and ust_25 >= alt_25: oneri_gol = "Üst"
    elif alt_25 >= esik_al("alt") and alt_25 >= ust_25: oneri_gol = "Alt"
    oneri_kg = None
    if kg_var >= esik_al("kg_var") and kg_var >= kg_yok: oneri_kg = "Var"
    elif kg_yok >= esik_al("kg_yok") and kg_yok >= kg_var: oneri_kg = "Yok"
    if oneri_1x2 is None: d_o1 = None
    else: d_o1 = "tam" if oneri_1x2 == gercek_1x2 else "yanlis"
    if oneri_gol is None: d_og = None
    else:
        gy = "Üst" if gercek_ust else "Alt"
        d_og = "tam" if oneri_gol == gy else "yanlis"
    if oneri_kg is None: d_ok = None
    else:
        gy = "Var" if gercek_kg_var else "Yok"
        d_ok = "tam" if oneri_kg == gy else "yanlis"
    def _t(d): return None if d is None else (d == "tam")
    return {
        "oneri_1x2": {"tahmin": oneri_1x2, "tuttu": _t(d_o1), "durum": d_o1},
        "oneri_gol": {"tahmin": oneri_gol, "tuttu": _t(d_og), "durum": d_og},
        "oneri_kg": {"tahmin": oneri_kg, "tuttu": _t(d_ok), "durum": d_ok},
        "gercek_1x2": gercek_1x2,
        "gercek_gol": "Üst" if gercek_ust else "Alt",
        "gercek_kg": "Var" if gercek_kg_var else "Yok",
    }


def detayli_analiz_yorumu(v):
    yorumlar = []
    ppg = v.get("ppg_ev", 0.0); mpg = v.get("mpg_dep", 0.0)
    if ppg > 0 or mpg > 0:
        fark = ppg - mpg
        if ppg >= 2.0 and mpg <= 1.0:
            txt = f"Ev sahibi evinde mükemmel form (**PPG {ppg:.2f}**), deplasman zayıf (**MPG {mpg:.2f}**)."
        elif fark >= 0.7: txt = f"Ev sahibi form olarak önde (**PPG {ppg:.2f}** vs **{mpg:.2f}**)."
        elif fark <= -0.7: txt = f"Deplasman form olarak önde (**MPG {mpg:.2f}** vs **{ppg:.2f}**)."
        else: txt = f"Form dengeli (**PPG {ppg:.2f}** vs **MPG {mpg:.2f}**)."
        yorumlar.append(("📈 FORM", txt))
    s_ev = v.get("siralama_ev", 0); s_dep = v.get("siralama_dep", 0)
    if s_ev > 0 and s_dep > 0:
        fark_sira = s_dep - s_ev
        if fark_sira >= 8: txt = f"Ev sahibi **{s_ev}.**, deplasman **{s_dep}.** sırada. **{fark_sira} basamak** ciddi fark."
        elif fark_sira >= 3: txt = f"Ev sahibi **{s_ev}.**, deplasman **{s_dep}.** sırada. Ev sahibi üstün."
        elif fark_sira <= -8: txt = f"Deplasman **{s_dep}.**, ev sahibi **{s_ev}.** sırada. Deplasman **{abs(fark_sira)} basamak** yukarıda."
        else: txt = f"Sıralamalar yakın (Ev **{s_ev}.** / Dep **{s_dep}.**)."
        yorumlar.append(("🏆 SIRALAMA", txt))
    at_ev = v.get("atilan_ev", 0.0); at_dep = v.get("atilan_dep", 0.0)
    if at_ev > 0 or at_dep > 0:
        if at_ev - at_dep >= 0.6: txt = f"Ev sahibi maç başına **{at_ev:.1f}** gol atıyor, deplasman **{at_dep:.1f}**."
        elif at_ev - at_dep <= -0.6: txt = f"Deplasman maç başına **{at_dep:.1f}** gol atıyor, ev sahibi **{at_ev:.1f}**."
        else: txt = f"Atılan goller benzer (Ev **{at_ev:.1f}** / Dep **{at_dep:.1f}**)."
        yorumlar.append(("⚽ ATILAN GOL", txt))
    y_ev = v.get("yenen_ev", 0.0); y_dep = v.get("yenen_dep", 0.0)
    if y_ev > 0 or y_dep > 0:
        if y_dep - y_ev >= 0.7: txt = f"Ev sahibi savunması sağlam (**{y_ev:.1f}**), deplasman zayıf (**{y_dep:.1f}**)."
        elif y_dep - y_ev <= -0.7: txt = f"Deplasman savunması sağlam (**{y_dep:.1f}**), ev sahibi zayıf (**{y_ev:.1f}**)."
        else: txt = f"Savunmalar benzer (Ev **{y_ev:.1f}** / Dep **{y_dep:.1f}**)."
        yorumlar.append(("🛡️ YENEN GOL", txt))
    return yorumlar


def gol_detayli_aciklama(v, a):
    ust_25 = a["ust_25"]; alt_25 = a["alt_25"]
    lam_ev = a["lam_ev"]; lam_dep = a["lam_dep"]; toplam_lambda = lam_ev + lam_dep
    at_ev = v.get("atilan_ev", 0); at_dep = v.get("atilan_dep", 0)
    y_ev = v.get("yenen_ev", 0); y_dep = v.get("yenen_dep", 0)
    lig_ort = v.get("lig_ort_toplam", 0)
    u15 = ort_iki(v.get("ust15_ev", 0), v.get("ust15_dep", 0))
    u35 = ort_iki(v.get("ust35_ev", 0), v.get("ust35_dep", 0))
    yorumlar = []
    if ust_25 >= esik_al("ust"):
        yorumlar.append(f"🎯 **ÜST 2.5 NEDEN POZİTİF? (%{ust_25:.1f})**")
        yorumlar.append(f"- Toplam beklenen gol: **{toplam_lambda:.2f}**")
        yorumlar.append(f"- Ev sahibi atak gücü: **{at_ev:.2f}** gol/maç")
        yorumlar.append(f"- Deplasman atak gücü: **{at_dep:.2f}** gol/maç")
        if lig_ort > 0: yorumlar.append(f"- Lig ortalaması: **{lig_ort:.2f}** gol/maç")
        yorumlar.append(f"- **Sonuç:** Toplam gol beklentisi **2.5 üstü** → Üst 2.5 mantıklı")
    elif alt_25 >= esik_al("alt"):
        yorumlar.append(f"🎯 **ALT 2.5 NEDEN POZİTİF? (%{alt_25:.1f})**")
        yorumlar.append(f"- Toplam beklenen gol: **{toplam_lambda:.2f}**")
        cs_ev = v.get("clean_sheets_ev", 0); cs_dep = v.get("clean_sheets_dep", 0)
        if cs_ev >= 40: yorumlar.append(f"- ✅ Ev sahibi clean sheet: **%{cs_ev:.0f}**")
        if cs_dep >= 40: yorumlar.append(f"- ✅ Deplasman clean sheet: **%{cs_dep:.0f}**")
        yorumlar.append(f"- **Sonuç:** Toplam gol beklentisi **2.5 altı** → Alt 2.5 mantıklı")
    return yorumlar


def kg_detayli_aciklama(v, a):
    kg_var = a["kg_var_model"]; kg_yok = a["kg_yok_model"]
    lam_ev = a["lam_ev"]; lam_dep = a["lam_dep"]
    kg_ev = v.get("kg_siklik_ev", 0); kg_dep = v.get("kg_siklik_dep", 0)
    cs_ev = v.get("clean_sheets_ev", 0); cs_dep = v.get("clean_sheets_dep", 0)
    yorumlar = []
    if kg_var >= esik_al("kg_var"):
        yorumlar.append(f"🤝 **KG VAR NEDEN POZİTİF? (%{kg_var:.1f})**")
        if kg_ev > 0: yorumlar.append(f"- Ev sahibi KG Var oranı: **%{kg_ev:.1f}**")
        if kg_dep > 0: yorumlar.append(f"- Deplasman KG Var oranı: **%{kg_dep:.1f}**")
        yorumlar.append(f"- **Sonuç:** İki takım da gol atabilir → KG Var mantıklı")
    elif kg_yok >= esik_al("kg_yok"):
        yorumlar.append(f"🤝 **KG YOK NEDEN POZİTİF? (%{kg_yok:.1f})**")
        if cs_ev > 0: yorumlar.append(f"- Ev sahibi clean sheet: **%{cs_ev:.0f}**")
        if cs_dep > 0: yorumlar.append(f"- Deplasman clean sheet: **%{cs_dep:.0f}**")
        yorumlar.append(f"- **Sonuç:** En az bir takım gol atmayabilir → KG Yok mantıklı")
    return yorumlar


def birx_iki_detayli_aciklama(v, a):
    p1 = a["p1"]; px = a["px"]; p2 = a["p2"]
    en = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
    secim, yuzde = en; esik_secim = esik_1x2_al(secim)
    isim = {"1": "Ev Sahibi Kazanır (1)", "X": "Beraberlik (X)", "2": "Deplasman Kazanır (2)"}[secim]
    s_ev = v.get("siralama_ev", 0); s_dep = v.get("siralama_dep", 0)
    at_ev = v.get("atilan_ev", 0); at_dep = v.get("atilan_dep", 0)
    y_ev = v.get("yenen_ev", 0); y_dep = v.get("yenen_dep", 0)
    ppg = v.get("ppg_ev", 0); mpg = v.get("mpg_dep", 0)
    gal_e = v.get("galibiyet_ev", 0); gal_d = v.get("galibiyet_dep", 0)
    ber_e = v.get("beraberlik_ev", 0); ber_d = v.get("beraberlik_dep", 0)
    yorumlar = []
    yorumlar.append(f"🎯 **1X2 NEDEN {secim}? (Ev %{p1:.1f} • X %{px:.1f} • Dep %{p2:.1f})**")
    if ppg > 0 and mpg > 0:
        fark = ppg - mpg
        if fark >= 0.5: yorumlar.append(f"- ✅ **Form:** Ev PPG **{ppg:.2f}** vs Dep MPG **{mpg:.2f}**")
        elif fark <= -0.5: yorumlar.append(f"- ✅ **Form:** Dep MPG **{mpg:.2f}** vs Ev PPG **{ppg:.2f}**")
        else: yorumlar.append(f"- Form dengeli (Ev PPG {ppg:.2f} / Dep MPG {mpg:.2f})")
    if s_ev > 0 and s_dep > 0:
        fark_sira = s_dep - s_ev
        if fark_sira >= 5: yorumlar.append(f"- ✅ **Sıralama:** Ev **{s_ev}.** vs Dep **{s_dep}.** → Ev **{fark_sira}** basamak önde")
        elif fark_sira <= -5: yorumlar.append(f"- ✅ **Sıralama:** Dep **{s_dep}.** vs Ev **{s_ev}.** → Dep **{abs(fark_sira)}** basamak önde")
        else: yorumlar.append(f"- Sıralamalar yakın (Ev **{s_ev}.** / Dep **{s_dep}.**)")
    if yuzde >= esik_secim: yorumlar.append(f"- **Sonuç:** En yüksek olasılık **{isim}** (%{yuzde:.1f}) ≥ eşik %{esik_secim:.0f} → **POZİTİF ✅**")
    else: yorumlar.append(f"- **Sonuç:** En yüksek olasılık **{isim}** (%{yuzde:.1f}) < eşik %{esik_secim:.0f} → **EŞİK ALTI**")
    return yorumlar


def okunan_veriler_paneli(v):
    format_tip = v.get("format", "bilinmiyor")
    if format_tip in ("sportytrader", "mutating"):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**{v.get('takim_ev', 'Ev')}**")
            st.markdown(f"- Atılan: **{v.get('atilan_ev', 0):.2f}**")
            st.markdown(f"- Yenen: **{v.get('yenen_ev', 0):.2f}**")
            st.markdown(f"- Clean sheets: **{v.get('clean_sheets_ev', 0):.1f}%**")
            st.markdown(f"- Team scored: **{v.get('team_scored_ev', 0):.1f}%**")
            st.markdown(f"- KG Var: **{v.get('kg_siklik_ev', 0):.1f}%**")
            st.markdown(f"- Üst 2.5: **{v.get('ust25_ev', 0):.1f}%**")
            st.markdown(f"- Sıralama: **{v.get('siralama_ev', 0)}**")
        with c2:
            st.markdown(f"**{v.get('takim_dep', 'Dep')}**")
            st.markdown(f"- Atılan: **{v.get('atilan_dep', 0):.2f}**")
            st.markdown(f"- Yenen: **{v.get('yenen_dep', 0):.2f}**")
            st.markdown(f"- Clean sheets: **{v.get('clean_sheets_dep', 0):.1f}%**")
            st.markdown(f"- Team scored: **{v.get('team_scored_dep', 0):.1f}%**")
            st.markdown(f"- KG Var: **{v.get('kg_siklik_dep', 0):.1f}%**")
            st.markdown(f"- Üst 2.5: **{v.get('ust25_dep', 0):.1f}%**")
            st.markdown(f"- Sıralama: **{v.get('siralama_dep', 0)}**")


# ==========================================
# VERİ ÇEKME MOTORU
# ==========================================
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def _son_n_oku(metin):
    m = re.search(r'Last\s+(\d+)\s+games', metin or "")
    return int(m.group(1)) if m else None


def _tikla_mac_sayisi(pg, mac_sec):
    hedef = str(mac_sec)
    try:
        els = pg.locator(f'xpath=//*[normalize-space(text())="{hedef}"]').all()
        for el in els[:20]:
            try:
                if el.evaluate("e => !!e.closest('table')"): continue
                if el.evaluate("e => e.children.length > 1"): continue
                el.click(timeout=1500)
                return True
            except Exception: continue
    except Exception: pass
    js = """
    (function(hedef) {
        var tum = document.querySelectorAll('label, span, div, button, a, li');
        for (var i = 0; i < tum.length; i++) {
            var el = tum[i];
            if (el.children.length > 1) continue;
            if (el.closest('table')) continue;
            var t = (el.textContent || '').trim();
            if (t === hedef) {
                try { el.click(); } catch(e) {}
                var inp = el.querySelector('input[type=radio], input[type=checkbox]');
                if (inp && !inp.checked) { try { inp.click(); } catch(e) {} }
                return true;
            }
        }
        return false;
    })("%s")
    """ % hedef
    try: return bool(pg.evaluate(js))
    except Exception: return False


def _tikla_takim_sekmesi(pg, takim_adi, sekme):
    if not takim_adi: return False
    js = r"""
    (function(takimAdi, sekmeAdi) {
        var tum = document.querySelectorAll('h1, h2, h3, h4, h5, strong, b, span, div, a, p');
        var teamEl = null;
        for (var i = 0; i < tum.length; i++) {
            var el = tum[i];
            if (el.children.length > 1) continue;
            var t = (el.textContent || '').trim();
            if (t === takimAdi) { teamEl = el; break; }
        }
        if (!teamEl) {
            for (var i = 0; i < tum.length; i++) {
                var el = tum[i];
                if (el.children.length > 1) continue;
                var t = (el.textContent || '').trim();
                if (t.indexOf(takimAdi) === 0 && t.length < takimAdi.length + 5) {
                    teamEl = el; break;
                }
            }
        }
        if (!teamEl) return false;
        var cur = teamEl;
        for (var k = 0; k < 12 && cur.parentElement; k++) {
            cur = cur.parentElement;
            var sekmeler = cur.querySelectorAll('label, span, div, a, button, li');
            for (var j = 0; j < sekmeler.length; j++) {
                var s = sekmeler[j];
                if (s.children.length > 1) continue;
                if (s.closest('table')) continue;
                var ts = (s.textContent || '').trim();
                if (ts === sekmeAdi) {
                    try { s.click(); } catch(e) {}
                    var inp = s.querySelector('input[type=radio], input[type=checkbox]');
                    if (inp && !inp.checked) { try { inp.click(); } catch(e) {} }
                    return true;
                }
            }
        }
        return false;
    })("%s", "%s")
    """ % (takim_adi.replace('"', '\\"'), sekme)
    try: return bool(pg.evaluate(js))
    except Exception: return False


def _playwright_html(url, mac_sec, timeout, dogrula=False, takim_ev="", takim_dep=""):
    from playwright.sync_api import sync_playwright
    hedef = int(mac_sec) if str(mac_sec).isdigit() else None
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=[
            "--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"
        ])
        try:
            ctx = b.new_context(user_agent=UA, locale="en-US")
            pg = ctx.new_page()
            pg.route("**/*", lambda route: route.abort()
                     if route.request.resource_type in ("image", "media", "font")
                     else route.continue_())
            pg.goto(url, wait_until="domcontentloaded", timeout=timeout * 1000)
            try: pg.wait_for_load_state("networkidle", timeout=15000)
            except Exception: pass
            pg.wait_for_timeout(2500)
            _tikla_mac_sayisi(pg, mac_sec)
            pg.wait_for_timeout(3500)
            if takim_ev:
                _tikla_takim_sekmesi(pg, takim_ev, "Home")
                pg.wait_for_timeout(3500)
            if takim_dep:
                _tikla_takim_sekmesi(pg, takim_dep, "Away")
                pg.wait_for_timeout(3500)
            if dogrula and hedef:
                try: metin = pg.inner_text("body")
                except Exception: metin = ""
                n = _son_n_oku(metin)
                if n is not None and n != hedef:
                    _tikla_mac_sayisi(pg, mac_sec)
                    pg.wait_for_timeout(3000)
                    try: metin = pg.inner_text("body")
                    except Exception: metin = ""
                    n = _son_n_oku(metin)
                    if n is not None and n != hedef:
                        raise RuntimeError(f"{hedef} filtresi uygulanamadı (sayfa: Last {n} games)")
            return pg.content()
        finally:
            try: b.close()
            except Exception: pass


def _scrapingbee_get(url, render_js=True, timeout=90, mac_sec="5", max_retry=3,
                    dogrula=False, takim_ev="", takim_dep=""):
    son_hata = None
    try:
        import playwright  # noqa: F401
        playwright_var = True
    except ImportError:
        playwright_var = False; son_hata = "playwright kurulu değil"
    if playwright_var:
        for deneme in range(max_retry):
            try:
                html = _playwright_html(url, mac_sec, timeout, dogrula,
                                        takim_ev=takim_ev, takim_dep=takim_dep)
                if html and len(html) > 500: return html, None
                son_hata = "Boş sayfa"
            except Exception as e:
                son_hata = f"Tarayıcı hatası: {str(e)[:150]}"
            if deneme < max_retry - 1: time.sleep(2 + deneme * 2)
    if dogrula: return None, son_hata or "Filtre uygulanamadı"
    try:
        r = requests.get(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}, timeout=30)
        if r.status_code == 200 and r.text: return r.text, None
        son_hata = f"HTTP {r.status_code}" + (f" | {son_hata}" if son_hata else "")
    except Exception as e:
        son_hata = f"Bağlantı hatası: {str(e)[:100]}" + (f" | {son_hata}" if son_hata else "")
    return None, son_hata or "Sayfa alınamadı."


def _html_metne_cevir(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "iframe"]): tag.decompose()
    for td in soup.find_all(["td", "th"]): td.insert_after("\t")
    for tr in soup.find_all("tr"): tr.insert_after("\n")
    for e in soup.find_all(["div", "p", "li", "h1", "h2", "h3", "h4", "br"]): e.insert_after("\n")
    metin = soup.get_text(separator="", strip=False)
    metin = re.sub(r'[ \t]+\n', '\n', metin)
    metin = re.sub(r'\n{3,}', '\n\n', metin)
    return metin


def mutating_ana_sayfa_linklerini_al(max_mac=MAX_MAC_SINIRI):
    html, hata = _scrapingbee_get("https://www.mutating.com/football-stats/", render_js=True)
    if hata: return [], [hata]
    if not html: return [], ["Ana sayfa indirilemedi."]
    soup = BeautifulSoup(html, "html.parser")
    maclar = []; gorulen = set()
    for link in soup.find_all("a", href=True):
        if len(maclar) >= max_mac: break
        href = link.get("href", "")
        if not any(x in href for x in ["match-preview", "match/", "/stats/"]): continue
        if href.startswith("/"): href = "https://www.mutating.com" + href
        elif not href.startswith("http"): continue
        if href in gorulen: continue
        gorulen.add(href)
        h2_list = link.find_all("h2")
        takim_ev = h2_list[0].get_text(strip=True) if len(h2_list) > 0 else ""
        takim_dep = h2_list[1].get_text(strip=True) if len(h2_list) > 1 else ""
        saat_el = link.find(class_=re.compile(r"nostart|time|match-time"))
        saat = saat_el.get_text(strip=True) if saat_el else ""
        maclar.append({"url": href, "takim_ev": takim_ev, "takim_dep": takim_dep, "saat": saat})
    return maclar, []


def mutating_mac_detay_cek(url, takim_ev="", takim_dep=""):
    html, hata = _scrapingbee_get(url, render_js=True, mac_sec="5",
                                   dogrula=True, takim_ev=takim_ev, takim_dep=takim_dep)
    if hata: return None, [hata]
    if not html: return None, ["Sayfa indirilemedi."]
    return _mac_html_parse(html, url)


def _mac_html_parse(html, url=""):
    soup = BeautifulSoup(html, "html.parser")
    veri = {}; okunamayanlar = []
    h1 = soup.find("h1")
    if h1:
        baslik = h1.get_text(strip=True)
        if " - " in baslik:
            p = baslik.replace(" Stats", "").replace(" stats", "").split(" - ")
            veri["takim_ev"] = p[0].strip()
            if len(p) > 1: veri["takim_dep"] = p[1].strip()
    metin = _html_metne_cevir(html)
    m = re.search(r'(\d{1,2}\.\d{1,2}\.\d{4})', metin)
    if m: veri["tarih"] = m.group(1)
    m = re.search(r'(\d{1,2}:\d{2})', metin)
    if m: veri["saat"] = m.group(1)
    veri["ulke"] = _ulke_bul(metin)
    skor_ev = skor_dep = None
    m = re.search(r'FT\s*\n+\s*(\d{1,2})\s*[-:]\s*(\d{1,2})', metin)
    if m:
        skor_ev = int(m.group(1)); skor_dep = int(m.group(2))
    if skor_ev is not None:
        veri["skor_ev"] = skor_ev; veri["skor_dep"] = skor_dep; veri["skor_belli"] = True
    else:
        veri["skor_belli"] = False

    def _cift(label):
        for pat in [
            r'([\d.,]+)\s*%?\s*\t\s*' + re.escape(label) + r'\s*\t\s*([\d.,]+)',
            r'([\d.,]+)\s*%?\s*\|\s*' + re.escape(label) + r'\s*\|\s*([\d.,]+)',
            r'([\d.,]+)\s*%?\s+' + re.escape(label) + r'\s+([\d.,]+)\s*%?',
            r'([\d.,]+)\s*%?\s*\n\s*' + re.escape(label) + r'\s*\n\s*([\d.,]+)',
        ]:
            mm = re.search(pat, metin, re.IGNORECASE)
            if mm:
                try: return float(mm.group(1).replace(",", ".")), float(mm.group(2).replace(",", "."))
                except ValueError: continue
        return None, None

    for label, k_ev, k_dep in [
        ("Goals scored per game", "atilan_ev", "atilan_dep"),
        ("Goals conceded per game", "yenen_ev", "yenen_dep"),
        ("Clean sheets", "clean_sheets_ev", "clean_sheets_dep"),
        ("Team scored", "team_scored_ev", "team_scored_dep"),
        ("Both Teams to Score", "kg_siklik_ev", "kg_siklik_dep"),
        ("Over 2.5 goals", "ust25_ev", "ust25_dep"),
        ("Over 1.5 goals", "ust15_ev", "ust15_dep"),
        ("Over 3.5 goals", "ust35_ev", "ust35_dep"),
    ]:
        a, b = _cift(label)
        if a is not None and veri.get(k_ev, 0) == 0:
            veri[k_ev] = a; veri[k_dep] = b
    for label, k_ev, k_dep in [("Win", "galibiyet_ev", "galibiyet_dep"),
                                ("Draw", "beraberlik_ev", "beraberlik_dep"),
                                ("Lose", "maglubiyet_ev", "maglubiyet_dep")]:
        mm = re.search(r'([\d.,]+)\s*%\s*\t\s*' + label + r'\s*\t\s*([\d.,]+)\s*%', metin, re.MULTILINE)
        if mm:
            try:
                veri[k_ev] = float(mm.group(1).replace(",", "."))
                veri[k_dep] = float(mm.group(2).replace(",", "."))
            except ValueError: pass
    if veri.get("atilan_ev", 0) > 0 and veri.get("yenen_ev", 0) > 0:
        veri["lig_ort_toplam"] = (veri.get("atilan_ev", 0) + veri.get("atilan_dep", 0) +
                                   veri.get("yenen_ev", 0) + veri.get("yenen_dep", 0)) / 2
    if veri.get("ust25_ev", 0) > 0 and veri.get("ust25_dep", 0) > 0:
        veri["lig_ust25"] = (veri["ust25_ev"] + veri["ust25_dep"]) / 2
    if veri.get("kg_siklik_ev", 0) > 0 and veri.get("kg_siklik_dep", 0) > 0:
        veri["lig_kg"] = (veri["kg_siklik_ev"] + veri["kg_siklik_dep"]) / 2
    veri["format"] = "mutating"
    if url: veri["kaynak_url"] = url
    return veri, okunamayanlar


def _mac_tahmin_var_mi(v):
    try:
        a = analiz_hesapla(v)
        s1, y1 = max([("1", a["p1"]), ("X", a["px"]), ("2", a["p2"])], key=lambda x: x[1])
        if y1 >= esik_1x2_al(s1): return True
        if a["ust_25"] >= esik_al("ust") and a["ust_25"] >= a["alt_25"]: return True
        if a["alt_25"] >= esik_al("alt") and a["alt_25"] >= a["ust_25"]: return True
        if a["kg_var_model"] >= esik_al("kg_var") and a["kg_var_model"] >= a["kg_yok_model"]: return True
        if a["kg_yok_model"] >= esik_al("kg_yok") and a["kg_yok_model"] >= a["kg_var_model"]: return True
        return False
    except Exception:
        return False


def _gelecek_mac_isle(mac, mevcut_urls):
    try:
        veri, _ = mutating_mac_detay_cek(mac["url"], takim_ev=mac.get("takim_ev", ""),
                                          takim_dep=mac.get("takim_dep", ""))
        if not veri:
            return ("hata", mac, "Sayfa çekilemedi", None)
        if not veri.get("takim_ev"): veri["takim_ev"] = mac.get("takim_ev", "")
        if not veri.get("takim_dep"): veri["takim_dep"] = mac.get("takim_dep", "")
        if not veri.get("saat"): veri["saat"] = mac.get("saat", "")
        veri["kaynak_url"] = mac["url"]
        if mac["url"] in mevcut_urls:
            return ("zaten_var", veri, "Zaten var", None)
        at_e = veri.get("atilan_ev", 0); ye_e = veri.get("yenen_ev", 0)
        at_d = veri.get("atilan_dep", 0); ye_d = veri.get("yenen_dep", 0)
        if at_e == 0 and ye_e == 0 and at_d == 0 and ye_d == 0:
            return ("veri_yok", veri, "İstatistik boş (0-0-0-0)", None)
        try:
            a = analiz_hesapla(veri)
        except Exception as e:
            return ("veri_yok", veri, f"Analiz hatası: {str(e)[:50]}", None)
        s1, y1 = max([("1", a["p1"]), ("X", a["px"]), ("2", a["p2"])], key=lambda x: x[1])
        e1 = esik_1x2_al(s1)
        gs = "Üst" if a["ust_25"] >= a["alt_25"] else "Alt"
        gy = a["ust_25"] if gs == "Üst" else a["alt_25"]
        ge_ = esik_al("ust") if gs == "Üst" else esik_al("alt")
        ks = "Var" if a["kg_var_model"] >= a["kg_yok_model"] else "Yok"
        ky = a["kg_var_model"] if ks == "Var" else a["kg_yok_model"]
        ke = esik_al("kg_var") if ks == "Var" else esik_al("kg_yok")
        ozet = f"1X2:%{y1:.0f}(eşik {e1:.0f}) • {gs}:%{gy:.0f}(eşik {ge_:.0f}) • KG {ks}:%{ky:.0f}(eşik {ke:.0f})"
        if _mac_tahmin_var_mi(veri):
            kayit = kayit_olustur(veri, a)
            return ("eklendi", veri, f"Eklendi • {ozet}", kayit)
        return ("esik_alti", veri, f"Eşik altı • {ozet}", None)
    except Exception as e:
        return ("hata", mac, f"İstisna: {str(e)[:80]}", None)


def mutating_toplu_cek(max_mac=MAX_MAC_SINIRI, progress_callback=None, max_workers=3):
    _ESIK_CACHE.clear()
    try: _ESIK_CACHE.update(dict(st.session_state.esikler))
    except Exception: pass
    maclar, hatalar = mutating_ana_sayfa_linklerini_al(max_mac=max_mac)
    if hatalar: return [], hatalar
    if not maclar: return [], ["Ana sayfada maç linki bulunamadı."]
    mevcut_urls = set()
    for g in st.session_state.gelecek_analizler:
        u = g.get("veri", {}).get("kaynak_url", "")
        if u: mevcut_urls.add(u)
    eklenen = 0; esik_alti = 0; veri_yok = 0; zaten_var = 0; hata_sayisi = 0
    eklenen_liste = []; detay_log = []; tamamlanan = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_gelecek_mac_isle, m, mevcut_urls): m for m in maclar}
        for fut in as_completed(futures):
            tamamlanan += 1
            mac = futures[fut]
            isim = f"{mac.get('takim_ev','?')} - {mac.get('takim_dep','?')}"
            try:
                r = fut.result()
                if len(r) == 4:
                    sonuc, veri, mesaj, kayit = r
                else:
                    sonuc, veri, mesaj = r; kayit = None
                if sonuc == "eklendi":
                    eklenen += 1; eklenen_liste.append(veri)
                    if kayit is not None:
                        try: st.session_state.gelecek_analizler.append(kayit)
                        except Exception: pass
                    detay_log.append(f"✅ {isim} → {mesaj}")
                elif sonuc == "esik_alti":
                    esik_alti += 1
                    detay_log.append(f"⚠️ {isim} → {mesaj}")
                elif sonuc == "veri_yok":
                    veri_yok += 1
                    detay_log.append(f"🚫 {isim} → {mesaj}")
                elif sonuc == "zaten_var":
                    zaten_var += 1
                    detay_log.append(f"↩️ {isim} → Zaten var")
                else:
                    hata_sayisi += 1
                    detay_log.append(f"❌ {isim} → {mesaj}")
            except Exception as e:
                hata_sayisi += 1
                detay_log.append(f"❌ {isim} → {str(e)[:80]}")
            if progress_callback:
                try: progress_callback(tamamlanan - 1, len(maclar), mac.get("takim_ev", ""))
                except Exception: pass
    try: gelecek_kaydet(st.session_state.gelecek_analizler)
    except Exception: pass
    st.session_state.toplu_cek_ozet = {
        "bulunan": len(maclar), "eklenen": eklenen, "esik_alti": esik_alti,
        "veri_yok": veri_yok, "zaten_var": zaten_var, "hata": hata_sayisi,
        "detay_log": detay_log[:300],
    }
    return eklenen_liste, []


def _lig_son_mac_linklerini_al(lig_url, adet=10):
    html, hata = _scrapingbee_get(lig_url, render_js=True, mac_sec="10")
    if hata: return [], [hata]
    if not html: return [], ["Lig sayfası indirilemedi."]
    soup = BeautifulSoup(html, "html.parser")
    maclar = []; gorulen = set()
    for link in soup.find_all("a", href=True):
        href = link.get("href", "")
        if "match-preview" not in href: continue
        if href.startswith("/"): href = "https://www.mutating.com" + href
        elif not href.startswith("http"): continue
        if href in gorulen: continue
        gorulen.add(href)
        takim_ev = ""; takim_dep = ""
        img = link.find_all("img", alt=True)
        if len(img) >= 2:
            takim_ev = img[0].get("alt", "").strip()
            takim_dep = img[1].get("alt", "").strip()
        if not takim_ev:
            txt = link.get_text(" ", strip=True)
            if " - " in txt:
                p = txt.split(" - ")
                takim_ev = p[0].strip(); takim_dep = p[1].strip() if len(p) > 1 else ""
        maclar.append({"url": href, "takim_ev": takim_ev, "takim_dep": takim_dep})
        if len(maclar) >= adet: break
    return maclar, []


def _gecmis_mac_isle(mac, mevcut_urls):
    try:
        if mac["url"] in mevcut_urls:
            return ("atlandi", None, "Zaten var", None)
        html, hata = _scrapingbee_get(mac["url"], render_js=True, mac_sec="5",
                                       dogrula=True, takim_ev=mac.get("takim_ev", ""),
                                       takim_dep=mac.get("takim_dep", ""))
        if hata or not html:
            return ("hata", mac, hata or "HTML yok", None)
        veri, _ = _mac_html_parse(html, mac["url"])
        if not veri.get("skor_belli", False):
            return ("atlandi", None, "Skor yok (bitmemiş maç)", None)
        if veri.get("atilan_ev", 0) == 0 or veri.get("yenen_ev", 0) == 0:
            return ("atlandi", None, "İstatistik eksik", None)
        if not veri.get("takim_ev"): veri["takim_ev"] = mac.get("takim_ev", "")
        if not veri.get("takim_dep"): veri["takim_dep"] = mac.get("takim_dep", "")
        yv = copy.deepcopy(VARSAYILAN_VERI); yv.update(veri)
        kayit = kayit_olustur(yv, analiz_hesapla(yv))
        kayit["dogruluk"] = sonuc_hesapla(kayit)
        return ("eklendi", veri, f"{veri['skor_ev']}-{veri['skor_dep']}", kayit)
    except Exception as e:
        return ("hata", mac, str(e), None)


def lig_gecmis_cek(lig_url, adet=10, max_workers=3, progress_callback=None):
    _ESIK_CACHE.clear()
    try: _ESIK_CACHE.update(dict(st.session_state.esikler))
    except Exception: pass
    maclar, hatalar = _lig_son_mac_linklerini_al(lig_url, adet=adet)
    if hatalar: return [], hatalar
    if not maclar: return [], ["Lig sayfasında maç linki bulunamadı."]
    mevcut_urls = set()
    for g in st.session_state.gecmis_analizler:
        u = g.get("veri", {}).get("kaynak_url", "")
        if u: mevcut_urls.add(u)
    basarili = []; hatali = []; eklenen = 0; atlanan = 0; tamamlanan = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_gecmis_mac_isle, m, mevcut_urls): m for m in maclar}
        for fut in as_completed(futures):
            tamamlanan += 1
            mac = futures[fut]
            try:
                r = fut.result()
                if len(r) == 4:
                    sonuc, veri, mesaj, kayit = r
                else:
                    sonuc, veri, mesaj = r; kayit = None
                if sonuc == "eklendi":
                    eklenen += 1; basarili.append(veri)
                    if kayit is not None:
                        try: st.session_state.gecmis_analizler.append(kayit)
                        except Exception: pass
                elif sonuc == "atlandi":
                    atlanan += 1
                else:
                    hatali.append(f"{mac.get('takim_ev','?')}: {mesaj}")
            except Exception as e:
                hatali.append(f"{mac.get('takim_ev','?')}: {e}")
            if progress_callback:
                try: progress_callback(tamamlanan - 1, len(maclar), mac.get("takim_ev", ""))
                except Exception: pass
    try: gecmis_kaydet(st.session_state.gecmis_analizler)
    except Exception: pass
    st.session_state.gecmis_cek_ozet = {"eklenen": eklenen, "atlanan": atlanan}
    return basarili, hatali


def _skor_parse(html):
    metin = _html_metne_cevir(html)
    m = re.search(r'(?<![A-Za-z])FT\s*\n+\s*(\d{1,2})\s*[-:]\s*(\d{1,2})', metin)
    if m: return int(m.group(1)), int(m.group(2))
    return None


def _skor_cek(url, tarayici_yedek=False):
    html = None; hata = None
    try:
        r = requests.get(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}, timeout=30)
        if r.status_code == 200 and r.text: html = r.text
        else: hata = f"HTTP {r.status_code}"
    except Exception as e:
        hata = f"Bağlantı: {str(e)[:80]}"
    skor = _skor_parse(html) if html else None
    if skor is None and tarayici_yedek:
        h2, hata2 = _scrapingbee_get(url, render_js=True, mac_sec="5")
        if h2: skor = _skor_parse(h2); hata = None
        elif hata2: hata = hata2
    if skor is None and html: hata = None
    return skor, hata


def sonuclari_isle(tarayici_yedek=False, max_workers=3, progress_callback=None):
    gel = st.session_state.gelecek_analizler
    isler = [(i, g) for i, g in enumerate(gel) if g.get("veri", {}).get("kaynak_url")]
    sonuc = {}; tamam = 0
    if isler:
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            fut = {ex.submit(_skor_cek, g["veri"]["kaynak_url"], tarayici_yedek): (i, g) for i, g in isler}
            for f in as_completed(fut):
                i, g = fut[f]; tamam += 1
                try: sonuc[i] = f.result()
                except Exception as e: sonuc[i] = (None, str(e)[:80])
                if progress_callback:
                    try: progress_callback(tamam - 1, len(isler), g["veri"].get("takim_ev", ""))
                    except Exception: pass
    mevcut = {x.get("veri", {}).get("kaynak_url") for x in st.session_state.gecmis_analizler}
    tasinan = 0; bitmemis = 0; hatalar = []; kalan = []
    for i, g in enumerate(gel):
        r = sonuc.get(i)
        if r is None: kalan.append(g); continue
        skor, hata = r
        v = g["veri"]; isim = f"{v.get('takim_ev', '?')} - {v.get('takim_dep', '?')}"
        if hata: hatalar.append(f"{isim}: {hata}"); kalan.append(g); continue
        if skor is None: bitmemis += 1; kalan.append(g); continue
        v["skor_ev"], v["skor_dep"], v["skor_belli"] = skor[0], skor[1], True
        d = sonuc_hesapla(g)
        if d: g["dogruluk"] = d
        if v.get("kaynak_url") not in mevcut:
            st.session_state.gecmis_analizler.append(g)
            mevcut.add(v.get("kaynak_url"))
        tasinan += 1
    st.session_state.gelecek_analizler = kalan
    st.session_state.aktif_gelecek_idx = None
    st.session_state.gelecekten_gelindi = False
    gecmis_kaydet(st.session_state.gecmis_analizler)
    gelecek_kaydet(st.session_state.gelecek_analizler)
    return {"tasinan": tasinan, "bitmemis": bitmemis, "hatalar": hatalar, "toplam": len(isler)}


# ==========================================
# TASARIM YARDIMCILARI
# ==========================================
def _e(x): return _html.escape(str(x))


def rozet(metin, tip="gray"):
    return f'<span class="fa-badge fa-b-{tip}">{_e(metin)}</span>'


def mac_karti(ev, dep, skor_belli, skor_ev, skor_dep, lam_ev, lam_dep, saat="", ulke="", tarih=""):
    orta = (f'<div class="fa-score">{int(skor_ev)} - {int(skor_dep)}</div>' if skor_belli
            else '<div class="fa-vs">VS</div>')
    bayrak = ulke_bayrak_bul(ulke)
    ust_bilgi = ""
    if saat or ulke or tarih:
        parcalar = []
        if bayrak != "🌍" or ulke: parcalar.append(f"{bayrak} {_e((ulke or '').title())}")
        if tarih: parcalar.append(f"📅 {_e(tarih)}")
        if saat: parcalar.append(f"🕐 {_e(saat)}")
        if parcalar:
            ust_bilgi = f'<div class="fa-sub" style="margin-bottom:6px;">{" • ".join(parcalar)}</div>'
    alt = f'<div class="fa-sub">Model beklenen gol: {lam_ev:.2f} - {lam_dep:.2f}</div>'
    return (f'<div class="fa-hero">{ust_bilgi}<div class="fa-teams"><div class="fa-team">{_e(ev)}</div>'
            f'{orta}<div class="fa-team">{_e(dep)}</div></div>{alt}</div>')


def mac_tahmin_karti(v_g, g=None):
    try:
        try: ya = yeniden_analiz(v_g)
        except Exception: ya = (g or {}).get("analiz", {})
        p1 = ya.get("p1", 33.33); px = ya.get("px", 33.33); p2 = ya.get("p2", 33.34)
        ust_25 = ya.get("ust_25", 50); alt_25 = 100 - ust_25
        kg_var = ya.get("kg_var_model", 50); kg_yok = 100 - kg_var
        en1x2 = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
        sec1x2, y1x2 = en1x2; e1x2 = esik_1x2_al(sec1x2); p1x2_poz = y1x2 >= e1x2
        isim1x2 = {"1": "1 — Ev Kazanır", "X": "X — Beraberlik", "2": "2 — Dep Kazanır"}[sec1x2]
        if ust_25 >= alt_25: gol_s = "Üst 2.5"; gol_y = ust_25; gol_e = esik_al("ust")
        else: gol_s = "Alt 2.5"; gol_y = alt_25; gol_e = esik_al("alt")
        gol_poz = gol_y >= gol_e
        if kg_var >= kg_yok: kg_s = "KG Var"; kg_y = kg_var; kg_e = esik_al("kg_var")
        else: kg_s = "KG Yok"; kg_y = kg_yok; kg_e = esik_al("kg_yok")
        kg_poz = kg_y >= kg_e
        def r(p): return "pass" if p else "off"
        def b(p): return "ok" if p else "no"
        def bt(p): return "✅" if p else "⚪"
        return f'''
        <div class="fa-mk">
            <div class="fa-mk-row">
                <span class="fa-mk-lbl">🎯 1X2</span>
                <span class="fa-mk-pick {r(p1x2_poz)}">{_e(isim1x2)}</span>
                <span class="fa-mk-pct">%{y1x2:.0f} <span class="fa-mk-badge {b(p1x2_poz)}">{bt(p1x2_poz)} eşik %{e1x2:.0f}</span></span>
            </div>
            <div class="fa-mk-row">
                <span class="fa-mk-lbl">⚽ Gol</span>
                <span class="fa-mk-pick {r(gol_poz)}">{_e(gol_s)}</span>
                <span class="fa-mk-pct">%{gol_y:.0f} <span class="fa-mk-badge {b(gol_poz)}">{bt(gol_poz)} eşik %{gol_e:.0f}</span></span>
            </div>
            <div class="fa-mk-row">
                <span class="fa-mk-lbl">🤝 KG</span>
                <span class="fa-mk-pick {r(kg_poz)}">{_e(kg_s)}</span>
                <span class="fa-mk-pct">%{kg_y:.0f} <span class="fa-mk-badge {b(kg_poz)}">{bt(kg_poz)} eşik %{kg_e:.0f}</span></span>
            </div>
        </div>
        '''
    except Exception:
        return ""


def olasilik_bar(etiket, yuzde, esik=None, renk="#3b82f6"):
    y = max(0.0, min(100.0, yuzde)); isaret = ""
    if esik is not None:
        renk = "#22c55e" if yuzde >= esik else "#475569"
        isaret = f'<div class="fa-tick" style="left:{esik:.0f}%"></div>'
    return (f'<div class="fa-row"><div class="fa-row-top"><span class="fa-lbl">{_e(etiket)}</span>'
            f'<span class="fa-val">%{yuzde:.1f}</span></div>'
            f'<div class="fa-bar"><div class="fa-fill" style="width:{y:.1f}%;background:{renk}"></div>{isaret}</div></div>')


def olasilik_paneli(a):
    satirlar = (
        '<div class="fa-ttl">Maç Sonucu (her seçimin kendi eşiği)</div>'
        + olasilik_bar("Ev Sahibi (1)", a["p1"], esik_1x2_al("1"), "#3b82f6")
        + olasilik_bar("Beraberlik (X)", a["px"], esik_1x2_al("X"), "#94a3b8")
        + olasilik_bar("Deplasman (2)", a["p2"], esik_1x2_al("2"), "#f59e0b")
        + '<div class="fa-ttl" style="margin-top:10px">Piyasalar (çizgi = eşik)</div>'
        + olasilik_bar("Üst 2.5", a["ust_25"], esik_al("ust"))
        + olasilik_bar("Alt 2.5", a["alt_25"], esik_al("alt"))
        + olasilik_bar("KG Var", a["kg_var_model"], esik_al("kg_var"))
        + olasilik_bar("KG Yok", a["kg_yok_model"], esik_al("kg_yok"))
    )
    return f'<div class="fa-card">{satirlar}</div>'


def oneri_karti(baslik, secim, yuzde, esik, poz, alt_satir):
    if poz:
        seviye, emoji, _k, etiket = guven_seviyesi_bul(yuzde)
        tip = "green" if seviye == "yuksek" else "yellow" if seviye == "orta" else "gray"
        durum = rozet(f"{etiket} güven", tip); sinif = "fa-card fa-pos"; pct_sinif = "fa-pct"
        not_satiri = f'<div class="fa-mut">{_e(alt_satir)}</div>'
    else:
        durum = rozet("Eşik altı", "gray"); sinif = "fa-card fa-neg"; pct_sinif = "fa-pct fa-off"
        not_satiri = f'<div class="fa-mut">{_e(alt_satir)} • Gerekli: %{esik:.0f}</div>'
    bar = olasilik_bar("", yuzde, esik)
    return (f'<div class="{sinif}"><div class="fa-ttl">{_e(baslik)}</div>'
            f'<div class="fa-pickrow"><div><div class="fa-pick">{_e(secim)}</div>{durum}</div>'
            f'<div class="{pct_sinif}">%{yuzde:.1f}</div></div>{bar}{not_satiri}</div>')


def istat_karti(baslik, ist, esik_metni):
    t = ist["tam"]; y = ist["yakin"]; yl = ist["yanlis"]; top = t + y + yl
    if top == 0:
        govde = '<div class="fa-big fa-off">—</div><div class="fa-mut">Henüz bahis yok</div>'
    else:
        isabet = (t + y) / top * 100
        sinif = "fa-g" if isabet >= 85 else "fa-y" if isabet >= 70 else "fa-r"
        govde = (f'<div class="fa-big {sinif}">%{isabet:.0f}</div>'
                 f'<div class="fa-mut">✅ {t + y} doğru • ❌ {yl} yanlış • {top} bahis</div>')
    return (f'<div class="fa-card"><div class="fa-ttl">{_e(baslik)}</div>{govde}'
            f'<div class="fa-mut">{_e(esik_metni)}</div></div>')


def backtest_karti(baslik, dogru, yanlis):
    top = dogru + yanlis
    if top == 0:
        return (f'<div class="fa-card"><div class="fa-ttl">{_e(baslik)}</div>'
                f'<div class="fa-mut">Eşiği geçen maç yok.</div></div>')
    yuzde = dogru / top * 100
    alt_s, ust_s = wilson_aralik(dogru, top)
    sinif = "fa-g" if yuzde >= 85 else "fa-y" if yuzde >= 70 else "fa-r"
    renk = "#22c55e" if yuzde >= 85 else "#f59e0b" if yuzde >= 70 else "#ef4444"
    return (f'<div class="fa-card"><div class="fa-ttl">{_e(baslik)}</div>'
            f'<div class="fa-pickrow"><div class="fa-big {sinif}">%{yuzde:.1f}</div>'
            f'<div style="text-align:right"><div class="fa-val">✅ {dogru} &nbsp; ❌ {yanlis}</div>'
            f'<div class="fa-mut">{top} bahis</div></div></div>'
            f'<div class="fa-ci"><div class="fa-ci-fill" style="left:{alt_s:.1f}%;width:{max(ust_s - alt_s, 0.5):.1f}%"></div>'
            f'<div class="fa-ci-dot" style="left:{yuzde:.1f}%;background:{renk}"></div></div>'
            f'<div class="fa-mut">%95 güven aralığı: %{alt_s:.0f} – %{ust_s:.0f}</div></div>')


def mac_sonuc_ikon(g):
    try:
        v = g["veri"]
        if not v.get("skor_belli", False): return "⚫"
        try: ya = yeniden_analiz(v)
        except Exception: ya = g.get("analiz", {})
        d = sonuc_hesapla({"veri": v, "analiz": ya})
        if not d: return "⚫"
        verilen = [x for x in [d["oneri_1x2"]["tuttu"], d["oneri_gol"]["tuttu"], d["oneri_kg"]["tuttu"]] if x is not None]
        if not verilen: return "⚫"
        if all(verilen): return "✅"
        if not any(verilen): return "❌"
        return "🟡"
    except Exception:
        return "⚫"


def nav_git(hedef):
    st.session_state.sayfa = hedef
    st.session_state.kayit_yapildi = False
    st.session_state.gecmisten_gelindi = False
    st.session_state.gelecekten_gelindi = False
    st.session_state.aktif_kayit_idx = None
    st.session_state.aktif_gelecek_idx = None
    st.session_state.okunamayan_alanlar = []
    st.session_state.manuel_bekleyen = []
    st.session_state.tek_silme_onay = None
    st.session_state.tek_silme_gelecek = None
    st.session_state.silme_onay = False
    if hedef == "backtest":
        st.session_state.bt_sonuc = None
        st.session_state.bt_detaylar = []
    st.rerun()


def nav_bar():
    try: kutu = st.container(key="fa_nav")
    except TypeError: kutu = st.container()
    with kutu:
        if admin_mi():
            secenekler = [("🏠", "giris"), ("📊 Geçmiş", "gecmis"), ("🔮 Gelecek", "gelecek"),
                          ("🔬 Test", "backtest"), ("⚙️ Ayar", "ayarlar")]
        else:
            secenekler = [("🏠 Ana", "giris"), ("📊 Geçmiş", "gecmis"), ("🔮 Gelecek", "gelecek")]
        kolonlar = st.columns(len(secenekler))
        for kol, (etiket, hedef) in zip(kolonlar, secenekler):
            with kol:
                aktif = st.session_state.sayfa == hedef
                if st.button(etiket, key=f"nav_{hedef}", use_container_width=True,
                             type="primary" if aktif else "secondary"):
                    if not aktif: nav_git(hedef)


def admin_giris_ekrani():
    st.markdown("""
        <div class="login-hero">
            <div class="login-logo">👑</div>
            <h1 class="login-title">Admin Girişi</h1>
            <p class="login-subtitle">Yönetici paneline erişim</p>
        </div>
    """, unsafe_allow_html=True)
    with st.form("admin_giris_form"):
        sifre = st.text_input("🔐 Admin Şifresi", type="password",
                              key="admin_sifre_input", placeholder="Şifreni gir...")
        col_a, col_b = st.columns(2)
        with col_a:
            giris_btn = st.form_submit_button("✅ Giriş Yap", use_container_width=True, type="primary")
        with col_b:
            iptal_btn = st.form_submit_button("⬅️ Geri Dön", use_container_width=True)
        if giris_btn:
            if sifre == ADMIN_SIFRE:
                st.session_state.rol = "admin"
                st.session_state.admin_login_acik = False
                st.session_state.sayfa = "giris"
                st.rerun()
            else:
                st.error("❌ Yanlış şifre. Tekrar deneyin.")
        if iptal_btn:
            st.session_state.admin_login_acik = False
            st.rerun()
    st.markdown('<div class="login-footer">© <b>Futbol Analiz Pro</b> • Yönetici Erişimi</div>',
                unsafe_allow_html=True)


def ust_bar():
    c1, c2 = st.columns([4, 1])
    with c1:
        if admin_mi():
            st.markdown('<div style="padding:6px 0; font-size:0.8rem; color:#22c55e; font-weight:700;">👑 Admin Modu</div>',
                        unsafe_allow_html=True)
        else:
            st.markdown('<div style="padding:6px 0; font-size:0.8rem; color:#8fa0bd; font-weight:600;">👤 Misafir Modu</div>',
                        unsafe_allow_html=True)
    with c2:
        if admin_mi():
            if st.button("🚪 Çıkış", use_container_width=True, key="cikis_btn"):
                st.session_state.rol = "misafir"
                st.session_state.admin_login_acik = False
                st.session_state.sayfa = "giris"
                st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
                st.session_state.tek_silme_onay = None
                st.session_state.tek_silme_gelecek = None
                st.session_state.silme_onay = False
                st.session_state.aktif_kayit_idx = None
                st.session_state.aktif_gelecek_idx = None
                st.session_state.bt_sonuc = None
                st.session_state.bt_detaylar = []
                st.rerun()
        else:
            if st.button("🔐 Giriş", use_container_width=True, key="giris_btn", type="primary"):
                st.session_state.admin_login_acik = True
                st.rerun()


def misafir_aciklama():
    with st.expander("📖 Uygulamayı Tanı ve Kuralları Oku", expanded=False):
        st.markdown("""
### ⚽ Futbol Analiz Pro Nedir?

Bu uygulama, futbol maçlarının **geçmiş istatistiklerini** analiz ederek 
**1X2 (Maç Sonucu)**, **Üst/Alt 2.5** ve **Karşılıklı Gol (KG)** tahminleri üretir. 
Sadece **bilgilendirme amaçlıdır.** Kesin sonuç garantisi **YOKTUR.**

---

### 🎯 EŞİKLER NEDİR?

**Eşik** = Bir tahminin "oynanabilir" sayılması için geçmesi gereken minimum yüzde.

---

### ⚠️ DİKKATLİ BAHİS KURALLARI

**1. KAYBETMEYİ KABUL ET** — Hiçbir sistem %100 değildir.

**2. BANKANI KORU** — Her bahis, bankanın %2-5'ini geçmesin.

**3. KAYIPTAN SONRA ARTTIRMA** — Her zaman sabit miktar.

**4. SADECE ÖNERİLERE OYNA** — Eşiği geçmeyen maçlara oynama.

**5. HAFTALIK LİMİT KOY**

**6. KAYIP SERİSİNDE ARA VER**

**7. KAZANCI ÇEK**

**8. ALKOL/SİNİR/AÇLIK DURUMUNDA OYNAMA**

---

### 🚫 SORUMLULUK REDDİ

- Bu uygulama **SADECE bilgi amaçlıdır.**
- Hiçbir kayıptan **sorumlu değiliz.**
- **18 yaşından küçükler** bahis oynayamaz.
- **Yeşilay Danışma: 115**

**Bol şans! 🍀**
        """)


# ==========================================
# UYGULAMA BAŞLANGIÇ
# ==========================================
if st.session_state.admin_login_acik and not admin_mi():
    admin_giris_ekrani()
    st.stop()

ust_bar()
nav_bar()


# ==========================================
# SAYFA: ANA SAYFA
# ==========================================
if st.session_state.sayfa == "giris":
    if admin_mi():
        st.markdown("<h1>⚽ Futbol Analiz Pro</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:gray;'>İstatistik metnini kopyala → yapıştır → analiz et.</p>", unsafe_allow_html=True)
        st.markdown("### 📋 İstatistik Metnini Yapıştır")

        yapistir_metni = st.text_area("Yapıştırma alanı", height=240, key="yapistir_input", label_visibility="collapsed", placeholder="İstatistik metnini buraya yapıştır.")
        st.divider()

        col_bt1, col_bt2, col_bt3, col_bt4, col_bt5 = st.columns([2, 1, 1, 1, 1])
        with col_bt1:
            analiz_btn = st.button("🚀 ANALİZ ET", use_container_width=True, type="primary")
        with col_bt2:
            gecmis_btn = st.button("📊 Geçmiş", use_container_width=True)
        with col_bt3:
            gelecek_btn = st.button("🔮 Gelecek", use_container_width=True)
        with col_bt4:
            backtest_btn = st.button("🔬 Backtest", use_container_width=True)
        with col_bt5:
            ayarlar_btn = st.button("⚙️ Ayarlar", use_container_width=True)

        if analiz_btn:
            if not yapistir_metni.strip():
                st.warning("⚠️ Önce metni yapıştır.")
            else:
                cikan, okunamayanlar = metinden_veri_cikar(yapistir_metni)
                if not cikan:
                    st.error("❌ Metinden hiçbir veri çıkarılamadı.")
                else:
                    yeni_veri = copy.deepcopy(VARSAYILAN_VERI)
                    yeni_veri.update(cikan)
                    st.session_state.form_verileri = yeni_veri
                    st.session_state.kayit_yapildi = False
                    st.session_state.gecmisten_gelindi = False
                    st.session_state.gelecekten_gelindi = False
                    st.session_state.aktif_kayit_idx = None
                    st.session_state.aktif_gelecek_idx = None
                    st.session_state.okunamayan_alanlar = okunamayanlar
                    st.session_state.manuel_bekleyen = okunamayanlar.copy()
                    if not veri_yeterli_mi(yeni_veri):
                        st.error(f"⚠️ Analiz için yeterli veri yok.")
                    else:
                        if okunamayanlar: st.session_state.sayfa = "manuel_giris"
                        else: st.session_state.sayfa = "sonuc"
                        st.rerun()

        if gecmis_btn:
            st.session_state.sayfa = "gecmis"
            st.session_state.kayit_yapildi = False
            st.session_state.gecmisten_gelindi = False
            st.session_state.gelecekten_gelindi = False
            st.session_state.aktif_kayit_idx = None
            st.session_state.aktif_gelecek_idx = None
            st.session_state.okunamayan_alanlar = []
            st.session_state.manuel_bekleyen = []
            st.session_state.tek_silme_onay = None
            st.session_state.silme_onay = False
            st.rerun()

        if gelecek_btn:
            st.session_state.sayfa = "gelecek"
            st.session_state.kayit_yapildi = False
            st.session_state.gecmisten_gelindi = False
            st.session_state.gelecekten_gelindi = False
            st.session_state.aktif_kayit_idx = None
            st.session_state.aktif_gelecek_idx = None
            st.session_state.okunamayan_alanlar = []
            st.session_state.manuel_bekleyen = []
            st.session_state.tek_silme_gelecek = None
            st.rerun()

        if backtest_btn:
            st.session_state.sayfa = "backtest"
            st.session_state.bt_sonuc = None
            st.session_state.bt_detaylar = []
            st.rerun()

        if ayarlar_btn:
            st.session_state.sayfa = "ayarlar"
            st.rerun()

        st.divider()
        st.markdown("### 🤖 Otomatik Veri Çekme")
        st.caption("Mutating.com'dan maç verilerini otomatik çek. 5 maçlık veri, Ev=Home / Dep=Away.")

        veri_sekme1, veri_sekme2, veri_sekme3 = st.tabs([
            "🔄 Bugünün Maçları", "📜 Lig Geçmişi", "🏁 Sonuçları İşle"
        ])

        with veri_sekme1:
            st.caption("✅ Bugünün maçları çekilir, **eşiği geçenler Gelecek'e** eklenir.")

            if st.session_state.toplu_cek_ozet:
                oz = st.session_state.toplu_cek_ozet
                st.markdown(
                    f"**Son çekim özeti:**\n"
                    f"- 📋 Bulunan maç: **{oz.get('bulunan', 0)}**\n"
                    f"- ✅ Gelecek'e eklenen: **{oz.get('eklenen', 0)}**\n"
                    f"- ⚠️ Eşik altı (eklenmedi): **{oz.get('esik_alti', 0)}**\n"
                    f"- 🚫 Veri çekilemedi: **{oz.get('veri_yok', 0)}**\n"
                    f"- ↩️ Zaten vardı: **{oz.get('zaten_var', 0)}**\n"
                    f"- ❌ Hata: **{oz.get('hata', 0)}**"
                )
                if oz.get("eklenen", 0) == 0 and oz.get("bulunan", 0) > 0:
                    st.warning("⚠️ Hiçbir maç eklenmedi. Detay için aşağıya bak.")
                if oz.get("detay_log"):
                    with st.expander(f"🔎 Maç maç detay ({len(oz['detay_log'])} satır)"):
                        for satir in oz["detay_log"]:
                            st.text(satir)

            c_w, c_b = st.columns(2)
            with c_w:
                workers = st.number_input("Paralel işlem", 1, 8, 3, 1, key="fw")
            with c_b:
                st.markdown("")
                if st.button("🚀 Bugünün Maçlarını Çek", use_container_width=True, type="primary", key="mbtn"):
                    prog_ph = st.empty()
                    def _prog(i, total, isim):
                        try: prog_ph.progress(min((i + 1) / total, 1.0), text=f"{i+1}/{total}: {isim}")
                        except Exception: pass
                    with st.spinner("Çekiliyor..."):
                        mutating_toplu_cek(max_mac=MAX_MAC_SINIRI, progress_callback=_prog, max_workers=int(workers))
                    prog_ph.empty()
                    st.rerun()

        with veri_sekme2:
            st.caption("Lig URL'i yapıştır → son N maç çekilir, skorla **Geçmiş'e** eklenir.")
            lig_url = st.text_input(
                "Lig URL",
                placeholder="https://www.mutating.com/football-stats/league-uefa-champions-league-country-world-tables-stats-h2h-2/",
                key="lig_url_input",
            )
            c_a, c_b = st.columns(2)
            with c_a:
                lig_adet = st.number_input("Kaç maç?", 5, 30, 10, 1, key="lig_adet")
            with c_b:
                lig_workers = st.number_input("Paralel işlem", 1, 8, 3, 1, key="lig_workers")
            if st.button("📜 Ligi Çek", use_container_width=True, type="primary", key="lig_cek_btn"):
                if not lig_url.strip():
                    st.warning("⚠️ Lig URL gir.")
                else:
                    prog_ph = st.empty()
                    def _prog2(i, total, isim):
                        try: prog_ph.progress(min((i + 1) / total, 1.0), text=f"{i+1}/{total}: {isim}")
                        except Exception: pass
                    with st.spinner(f"Son {lig_adet} maç çekiliyor..."):
                        bas, hat = lig_gecmis_cek(lig_url.strip(), adet=int(lig_adet), max_workers=int(lig_workers), progress_callback=_prog2)
                    prog_ph.empty()
                    if hat:
                        with st.expander(f"⚠️ {len(hat)} hata"):
                            for h in hat: st.caption(h)
                    if not bas:
                        st.error("❌ Hiçbir maç eklenemedi.")
                    else:
                        st.success(f"✅ {len(bas)} maç Geçmiş'e eklendi!")
                        time.sleep(2)
                        st.rerun()

        with veri_sekme3:
            st.caption("Maçlar bitince: Gelecek'teki maçların skorları siteden okunur, **biten maçlar skoruyla Geçmiş'e taşınır**.")
            if st.session_state.skor_ozet:
                oz4 = st.session_state.skor_ozet
                st.success(f"✅ {oz4['tasinan']} maç Geçmiş'e taşındı • {oz4['bitmemis']} maç henüz bitmemiş/skor yok")
                if oz4["hatalar"]:
                    with st.expander(f"⚠️ {len(oz4['hatalar'])} hata"):
                        for h in oz4["hatalar"]: st.caption(h)
            st.markdown(f"Bekleyen maç: **{len(st.session_state.gelecek_analizler)}**")
            skor_yedek = st.checkbox("Skor bulunamazsa tarayıcıyla da dene (yavaş, belleği zorlar)", value=False, key="skor_yedek")
            skor_w = st.number_input("Paralel işlem", 1, 8, 3, 1, key="skor_w")
            if st.button("🏁 Biten Maçları Geçmişe Aktar", use_container_width=True, type="primary", key="skor_btn"):
                if not st.session_state.gelecek_analizler:
                    st.warning("⚠️ Gelecek'te maç yok.")
                else:
                    prog4 = st.empty()
                    def _prog4(i, total, isim):
                        try: prog4.progress(min((i + 1) / total, 1.0), text=f"{i+1}/{total}: {isim}")
                        except Exception: pass
                    with st.spinner("Skorlar kontrol ediliyor..."):
                        st.session_state.skor_ozet = sonuclari_isle(tarayici_yedek=bool(skor_yedek), max_workers=int(skor_w), progress_callback=_prog4)
                    prog4.empty()
                    st.rerun()

    else:
        gecmis_sayi = len(st.session_state.gecmis_analizler)
        gelecek_sayi = len(st.session_state.gelecek_analizler)

        st.markdown(f"""
            <div class="mh-hero">
                <div class="mh-hero-icon">⚽</div>
                <div class="mh-hero-title">Futbol Analiz Pro</div>
                <div class="mh-hero-sub">Akıllı maç analizi ve tahmin motoru</div>
                <div class="mh-hero-badge">● CANLI VERİ</div>
            </div>
            <div class="mh-stat-grid">
                <div class="mh-stat">
                    <div class="mh-stat-icon">📊</div>
                    <div class="mh-stat-num">{gecmis_sayi}</div>
                    <div class="mh-stat-lbl">Geçmiş Maç</div>
                </div>
                <div class="mh-stat">
                    <div class="mh-stat-icon">🔮</div>
                    <div class="mh-stat-num">{gelecek_sayi}</div>
                    <div class="mh-stat-lbl">Gelecek Maç</div>
                </div>
            </div>
            <div class="mh-section-title">HIZLI ERİŞİM</div>
        """, unsafe_allow_html=True)

        try: kutu = st.container(key="fa_misafir_nav")
        except TypeError: kutu = st.container()
        with kutu:
            col_bt2, col_bt3 = st.columns(2)
            with col_bt2:
                gecmis_btn = st.button("📊  Geçmiş Maçlar", use_container_width=True, type="primary", key="m_gecmis")
            with col_bt3:
                gelecek_btn = st.button("🔮  Gelecek Maçlar", use_container_width=True, type="primary", key="m_gelecek")

        if gecmis_btn:
            st.session_state.sayfa = "gecmis"
            st.session_state.kayit_yapildi = False
            st.session_state.aktif_kayit_idx = None
            st.session_state.aktif_gelecek_idx = None
            st.session_state.tek_silme_onay = None
            st.rerun()
        if gelecek_btn:
            st.session_state.sayfa = "gelecek"
            st.session_state.kayit_yapildi = False
            st.session_state.aktif_kayit_idx = None
            st.session_state.aktif_gelecek_idx = None
            st.session_state.tek_silme_gelecek = None
            st.rerun()

        st.markdown("""
            <div class="mh-info">
                💡 <b>İpucu:</b> Geçmiş maçlarda isabet oranlarını incele, gelecek maçlarda
                yüksek güvenli tahminleri filtreleyerek kombine oluştur.
            </div>
            <div class="mh-section-title" style="margin-top:16px;">BİLGİLENDİRME</div>
        """, unsafe_allow_html=True)

        misafir_aciklama()

        st.markdown("""
            <div class="login-footer" style="margin-top:20px;">
                © <b>Futbol Analiz Pro</b> • Bilgi amaçlıdır • Kesin sonuç garantisi yoktur
            </div>
        """, unsafe_allow_html=True)


# ==========================================
# MANUEL GİRİŞ
# ==========================================
elif st.session_state.sayfa == "manuel_giris":
    st.markdown("<h1>📝 Eksik Alanları Doldur</h1>", unsafe_allow_html=True)
    st.warning(f"Aşağıdaki **{len(st.session_state.manuel_bekleyen)}** alan metinden çıkarılamadı:")
    v = st.session_state.form_verileri
    with st.form("manuel_form"):
        yeni_degerler = {}
        for alan_basligi in st.session_state.manuel_bekleyen:
            if alan_basligi in MANUEL_ALANLAR:
                st.markdown(f"**{alan_basligi}**")
                for (key, etiket, tip, varsayilan) in MANUEL_ALANLAR[alan_basligi]:
                    mevcut = v.get(key, varsayilan)
                    if tip == "int":
                        val = st.number_input(etiket, value=int(mevcut) if mevcut else int(varsayilan), min_value=1, max_value=100, step=1, key=f"manuel_{key}")
                        yeni_degerler[key] = int(val)
                    elif tip == "float":
                        val = st.number_input(etiket, value=float(mevcut) if mevcut else float(varsayilan), min_value=0.0, step=0.1, key=f"manuel_{key}")
                        yeni_degerler[key] = float(val)
                    else:
                        val = st.text_input(etiket, value=str(mevcut) if mevcut else "", key=f"manuel_{key}")
                        yeni_degerler[key] = val
                st.markdown("")
        col_a, col_b = st.columns(2)
        with col_a:
            kaydet = st.form_submit_button("✅ Kaydet ve Analiz Et", use_container_width=True, type="primary")
        with col_b:
            atla = st.form_submit_button("⏭️ Atla (Varsayılan)", use_container_width=True)
        if kaydet or atla:
            if kaydet: st.session_state.form_verileri.update(yeni_degerler)
            st.session_state.manuel_bekleyen = []
            st.session_state.sayfa = "sonuc"
            st.rerun()
    if st.button("⬅️ Metni Yeniden Yapıştır"):
        st.session_state.sayfa = "giris"
        st.rerun()


# ==========================================
# GEÇMİŞ
# ==========================================
elif st.session_state.sayfa == "gecmis":
    st.markdown("<h1>📊 Geçmiş Maçlar</h1>", unsafe_allow_html=True)
    gecmis = st.session_state.gecmis_analizler
    toplam = len(gecmis)
    with st.spinner("İstatistikler güncel eşiklerle hesaplanıyor..."):
        oneri_ist = oneri_istatistik_guncel(gecmis)
    if toplam == 0:
        st.info("ℹ️ Henüz kayıtlı maç yok.")
    else:
        st.markdown("### 🎯 ÖNERİ İSTATİSTİKLERİ")
        st.caption("Ayarlar'daki güncel eşiklerle ve güncel hesaplamayla yeniden hesaplanır.")
        col_1, col_2, col_3 = st.columns(3)
        with col_1:
            st.markdown(istat_karti("🎯 1X2 (Maç Sonucu)", oneri_ist["1x2"],
                                    f"Eşikler: 1 %{esik_1x2_al('1'):.0f} • X %{esik_1x2_al('X'):.0f} • 2 %{esik_1x2_al('2'):.0f}"), unsafe_allow_html=True)
        with col_2:
            st.markdown(istat_karti("⚽ Üst / Alt 2.5", oneri_ist["gol"],
                                    f"Eşikler: Üst %{esik_al('ust'):.0f} • Alt %{esik_al('alt'):.0f}"), unsafe_allow_html=True)
        with col_3:
            st.markdown(istat_karti("🤝 KG Var / Yok", oneri_ist["kg"],
                                    f"Eşikler: Var %{esik_al('kg_var'):.0f} • Yok %{esik_al('kg_yok'):.0f}"), unsafe_allow_html=True)
    st.divider()
    st.markdown(f"### ⚽ Skoru Belli Maçlar ({toplam})")
    if toplam > 0:
        for i, g in enumerate(reversed(gecmis)):
            idx_gercek = len(gecmis) - 1 - i
            v_g = g["veri"]
            takim_ev = v_g.get("takim_ev", "Ev") or "Ev"
            takim_dep = v_g.get("takim_dep", "Dep") or "Dep"
            skor_ev = v_g.get("skor_ev", 0); skor_dep = v_g.get("skor_dep", 0)
            ulke = v_g.get("ulke", ""); saat = v_g.get("saat", ""); tarih = v_g.get("tarih", "")
            ikon = mac_sonuc_ikon(g)
            st.markdown(f"### {ikon}", unsafe_allow_html=False)
            header_html = mac_karti(takim_ev, takim_dep, True, skor_ev, skor_dep, 0, 0,
                                    saat=saat, ulke=ulke, tarih=tarih)
            st.markdown(header_html, unsafe_allow_html=True)
            tahmin_html = mac_tahmin_karti(v_g, g)
            if tahmin_html: st.markdown(tahmin_html, unsafe_allow_html=True)
            try:
                try: ya2 = yeniden_analiz(v_g)
                except Exception: ya2 = g.get("analiz", {})
                d2 = sonuc_hesapla({"veri": v_g, "analiz": ya2})
                if d2:
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        o = d2["oneri_1x2"]
                        if o["tuttu"] is None: st.caption("⚫ 1X2 — öneri yok")
                        else:
                            ik = "✅" if o["tuttu"] else "❌"
                            st.caption(f"{ik} 1X2: **{o['tahmin']}** (gerçek: {d2.get('gercek_1x2','?')})")
                    with c2:
                        o = d2["oneri_gol"]
                        if o["tuttu"] is None: st.caption("⚫ Gol — öneri yok")
                        else:
                            ik = "✅" if o["tuttu"] else "❌"
                            st.caption(f"{ik} Gol: **{o['tahmin']}**")
                    with c3:
                        o = d2["oneri_kg"]
                        if o["tuttu"] is None: st.caption("⚫ KG — öneri yok")
                        else:
                            ik = "✅" if o["tuttu"] else "❌"
                            st.caption(f"{ik} KG: **{o['tahmin']}**")
            except Exception: pass
            if admin_mi():
                col_detay, col_sil = st.columns([5, 1])
                with col_detay:
                    if st.button("🔍 Detaylı Analiz", use_container_width=True, key=f"mac_{idx_gercek}"):
                        st.session_state.form_verileri = copy.deepcopy(v_g)
                        st.session_state.kayit_yapildi = True
                        st.session_state.gecmisten_gelindi = True
                        st.session_state.gelecekten_gelindi = False
                        st.session_state.aktif_kayit_idx = idx_gercek
                        st.session_state.aktif_gelecek_idx = None
                        st.session_state.okunamayan_alanlar = []
                        st.session_state.sayfa = "sonuc"
                        st.rerun()
                with col_sil:
                    if st.button("🗑️", key=f"sil_{idx_gercek}"):
                        if st.session_state.tek_silme_onay == idx_gercek:
                            st.session_state.tek_silme_onay = None
                        else:
                            st.session_state.tek_silme_onay = idx_gercek
                        st.rerun()
                if st.session_state.tek_silme_onay == idx_gercek:
                    st.warning(f"⚠️ **{takim_ev} vs {takim_dep}** silinsin mi?")
                    col_e, col_h = st.columns(2)
                    with col_e:
                        if st.button("✅ Sil", key=f"evet_{idx_gercek}", use_container_width=True, type="primary"):
                            if 0 <= idx_gercek < len(st.session_state.gecmis_analizler):
                                st.session_state.gecmis_analizler.pop(idx_gercek)
                                gecmis_kaydet(st.session_state.gecmis_analizler)
                            st.session_state.tek_silme_onay = None
                            st.rerun()
                    with col_h:
                        if st.button("❌ İptal", key=f"hayir_{idx_gercek}", use_container_width=True):
                            st.session_state.tek_silme_onay = None
                            st.rerun()
            else:
                if st.button("🔍 Detaylı Analiz", use_container_width=True, key=f"mac_{idx_gercek}"):
                    st.session_state.form_verileri = copy.deepcopy(v_g)
                    st.session_state.kayit_yapildi = True
                    st.session_state.gecmisten_gelindi = True
                    st.session_state.gelecekten_gelindi = False
                    st.session_state.aktif_kayit_idx = idx_gercek
                    st.session_state.aktif_gelecek_idx = None
                    st.session_state.okunamayan_alanlar = []
                    st.session_state.sayfa = "sonuc"
                    st.rerun()
            st.divider()
    st.markdown("### 💾 Yedekleme (Geçmiş Maçlar)")
    if admin_mi():
        c_ind, c_yuk = st.columns(2)
        with c_ind:
            json_str = json.dumps(st.session_state.gecmis_analizler, ensure_ascii=False, indent=2)
            st.download_button(label=f"📥 Geçmişi İndir ({toplam} maç)", data=json_str,
                               file_name=f"gecmis_{toplam}mac.json", mime="application/json",
                               use_container_width=True, key="ind_gecmis")
        with c_yuk:
            yuklenen = st.file_uploader("📤 Geçmişi Yükle (JSON)", type=["json"], key="yuk_gecmis")
            if yuklenen is not None:
                try:
                    veri = json.loads(yuklenen.read().decode("utf-8"))
                    if isinstance(veri, list):
                        st.session_state.gecmis_analizler = veri
                        gecmis_kaydet(veri)
                        st.success(f"✅ {len(veri)} maç yüklendi! Sayfa yenileniyor...")
                        st.rerun()
                    else:
                        st.error("❌ Dosya formatı hatalı. Liste bekleniyordu.")
                except Exception as e:
                    st.error(f"❌ Yükleme hatası: {e}")
    st.divider()
    if admin_mi():
        c_temizle, c_geri = st.columns(2)
        with c_temizle:
            if st.button("🗑️ Tüm Geçmişi Temizle", use_container_width=True, key="temizle_btn"):
                st.session_state.silme_onay = True
                st.rerun()
        with c_geri:
            if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="gecmis_geri"):
                st.session_state.sayfa = "giris"
                st.session_state.silme_onay = False
                st.session_state.tek_silme_onay = None
                st.rerun()
        if st.session_state.silme_onay:
            st.warning("⚠️ Tüm geçmiş silinecek. Emin misin?")
            c_e, c_h = st.columns(2)
            with c_e:
                if st.button("✅ Evet, Sil", use_container_width=True, type="primary", key="sil_hepsi_evet"):
                    st.session_state.gecmis_analizler = []
                    try:
                        if os.path.exists(GECMIS_DOSYA): os.remove(GECMIS_DOSYA)
                    except Exception: pass
                    st.session_state.silme_onay = False
                    st.session_state.tek_silme_onay = None
                    st.rerun()
            with c_h:
                if st.button("❌ İptal", use_container_width=True, key="sil_hepsi_iptal"):
                    st.session_state.silme_onay = False
                    st.rerun()
    else:
        if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="gecmis_geri_misafir"):
            st.session_state.sayfa = "giris"
            st.session_state.tek_silme_onay = None
            st.rerun()


# ==========================================
# GELECEK
# ==========================================
elif st.session_state.sayfa == "gelecek":
    st.markdown("<h1>🔮 Gelecek Maçlar</h1>", unsafe_allow_html=True)
    gelecek = st.session_state.gelecek_analizler
    toplam_g = len(gelecek)
    if not gelecek:
        st.info("ℹ️ Gelecek maç yok.")
    else:
        sirali = sorted(enumerate(gelecek), key=lambda x: saat_sirala_anahtari(x[1]))
        for idx_gercek, g in sirali:
            v_g = g["veri"]
            takim_ev = v_g.get("takim_ev", "Ev") or "Ev"
            takim_dep = v_g.get("takim_dep", "Dep") or "Dep"
            ulke = v_g.get("ulke", ""); saat = v_g.get("saat", ""); tarih = v_g.get("tarih", "")
            try:
                analiz_full = analiz_hesapla(v_g)
                lam_ev_h = analiz_full["lam_ev"]; lam_dep_h = analiz_full["lam_dep"]
            except Exception:
                lam_ev_h = lam_dep_h = 0
            hero = mac_karti(takim_ev, takim_dep, False, 0, 0, lam_ev_h, lam_dep_h,
                             saat=saat, ulke=ulke, tarih=tarih)
            st.markdown(hero, unsafe_allow_html=True)
            tahmin_html = mac_tahmin_karti(v_g, g)
            if tahmin_html: st.markdown(tahmin_html, unsafe_allow_html=True)
            if admin_mi():
                col_detay, col_sil = st.columns([5, 1])
                with col_detay:
                    if st.button("🔍 Detaylı Analiz", use_container_width=True, key=f"gmac_{idx_gercek}"):
                        st.session_state.form_verileri = copy.deepcopy(v_g)
                        st.session_state.kayit_yapildi = True
                        st.session_state.gecmisten_gelindi = False
                        st.session_state.gelecekten_gelindi = True
                        st.session_state.aktif_kayit_idx = None
                        st.session_state.aktif_gelecek_idx = idx_gercek
                        st.session_state.okunamayan_alanlar = []
                        st.session_state.sayfa = "sonuc"
                        st.rerun()
                with col_sil:
                    if st.button("🗑️", key=f"gsil_{idx_gercek}"):
                        if st.session_state.tek_silme_gelecek == idx_gercek:
                            st.session_state.tek_silme_gelecek = None
                        else:
                            st.session_state.tek_silme_gelecek = idx_gercek
                        st.rerun()
                if st.session_state.tek_silme_gelecek == idx_gercek:
                    st.warning(f"⚠️ **{takim_ev} vs {takim_dep}** silinsin mi?")
                    c_e, c_h = st.columns(2)
                    with c_e:
                        if st.button("✅ Sil", key=f"evet_g_{idx_gercek}", use_container_width=True, type="primary"):
                            if 0 <= idx_gercek < len(st.session_state.gelecek_analizler):
                                st.session_state.gelecek_analizler.pop(idx_gercek)
                                gelecek_kaydet(st.session_state.gelecek_analizler)
                            st.session_state.tek_silme_gelecek = None
                            st.rerun()
                    with c_h:
                        if st.button("❌ İptal", key=f"hayir_g_{idx_gercek}", use_container_width=True):
                            st.session_state.tek_silme_gelecek = None
                            st.rerun()
            else:
                if st.button("🔍 Detaylı Analiz", use_container_width=True, key=f"gmac_{idx_gercek}"):
                    st.session_state.form_verileri = copy.deepcopy(v_g)
                    st.session_state.kayit_yapildi = True
                    st.session_state.gecmisten_gelindi = False
                    st.session_state.gelecekten_gelindi = True
                    st.session_state.aktif_kayit_idx = None
                    st.session_state.aktif_gelecek_idx = idx_gercek
                    st.session_state.okunamayan_alanlar = []
                    st.session_state.sayfa = "sonuc"
                    st.rerun()
            st.divider()
    if admin_mi():
        st.markdown("### 💾 Yedekleme (Gelecek Maçlar)")
        c_ind2, c_yuk2 = st.columns(2)
        with c_ind2:
            json_str2 = json.dumps(st.session_state.gelecek_analizler, ensure_ascii=False, indent=2)
            st.download_button(label=f"📥 Geleceği İndir ({toplam_g} maç)", data=json_str2,
                               file_name=f"gelecek_{toplam_g}mac.json", mime="application/json",
                               use_container_width=True, key="ind_gelecek")
        with c_yuk2:
            yuklenen2 = st.file_uploader("📤 Geleceği Yükle (JSON)", type=["json"], key="yuk_gelecek")
            if yuklenen2 is not None:
                try:
                    veri2 = json.loads(yuklenen2.read().decode("utf-8"))
                    if isinstance(veri2, list):
                        st.session_state.gelecek_analizler = veri2
                        gelecek_kaydet(veri2)
                        st.success(f"✅ {len(veri2)} maç yüklendi! Sayfa yenileniyor...")
                        st.rerun()
                    else:
                        st.error("❌ Dosya formatı hatalı.")
                except Exception as e:
                    st.error(f"❌ Yükleme hatası: {e}")
        st.divider()
    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="g_geri"):
        st.session_state.sayfa = "giris"
        st.session_state.tek_silme_gelecek = None
        st.rerun()


# ==========================================
# BACKTEST
# ==========================================
elif st.session_state.sayfa == "backtest":
    if not admin_mi():
        st.error("❌ Bu sayfa sadece admin içindir.")
        if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary"):
            st.session_state.sayfa = "giris"; st.rerun()
        st.stop()
    st.markdown("<h1>🔬 Geçmiş Backtest</h1>", unsafe_allow_html=True)
    st.caption("Test etmek istediğin marketleri seç ve eşikleri ayarla.")
    st.divider()
    st.markdown("### ⚙️ Test Seçenekleri ve Eşikler")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**🎯 Maç Sonucu**")
        sec_1x2 = st.checkbox("1X2", value=st.session_state.bt_market.get("1x2", False), key="bt_1x2")
        esik_bt_1 = st.slider("1 (Ev) eşiği (%)", 0, 100, int(st.session_state.bt_market_esik.get("esik_1", 55.0)), 1, key="sl_bt_1", disabled=not sec_1x2)
        esik_bt_x = st.slider("X eşiği (%)", 0, 100, int(st.session_state.bt_market_esik.get("esik_x", 55.0)), 1, key="sl_bt_x", disabled=not sec_1x2)
        esik_bt_2 = st.slider("2 (Dep) eşiği (%)", 0, 100, int(st.session_state.bt_market_esik.get("esik_2", 55.0)), 1, key="sl_bt_2", disabled=not sec_1x2)
    with c2:
        st.markdown("**🤝 KG**")
        sec_kg_var = st.checkbox("KG Var", value=st.session_state.bt_market["kg_var"], key="bt_kg_var")
        esik_kg_var = st.slider("KG Var eşiği (%)", 0, 100, int(st.session_state.bt_market_esik["kg_var"]), 1, key="sl_kg_var", disabled=not sec_kg_var)
        sec_kg_yok = st.checkbox("KG Yok", value=st.session_state.bt_market["kg_yok"], key="bt_kg_yok")
        esik_kg_yok = st.slider("KG Yok eşiği (%)", 0, 100, int(st.session_state.bt_market_esik["kg_yok"]), 1, key="sl_kg_yok", disabled=not sec_kg_yok)
    with c3:
        st.markdown("**⚽ Gol**")
        sec_ust = st.checkbox("Üst 2.5", value=st.session_state.bt_market["ust"], key="bt_ust")
        esik_ust = st.slider("Üst 2.5 eşiği (%)", 0, 100, int(st.session_state.bt_market_esik["ust"]), 1, key="sl_ust", disabled=not sec_ust)
        sec_alt = st.checkbox("Alt 2.5", value=st.session_state.bt_market["alt"], key="bt_alt")
        esik_alt = st.slider("Alt 2.5 eşiği (%)", 0, 100, int(st.session_state.bt_market_esik["alt"]), 1, key="sl_alt", disabled=not sec_alt)
    secenekler = {"1x2": sec_1x2, "kg_var": sec_kg_var, "kg_yok": sec_kg_yok, "ust": sec_ust, "alt": sec_alt}
    esikler = {
        "esik_1": float(esik_bt_1), "esik_x": float(esik_bt_x), "esik_2": float(esik_bt_2),
        "kg_var": float(esik_kg_var), "kg_yok": float(esik_kg_yok),
        "ust": float(esik_ust), "alt": float(esik_alt)
    }
    st.divider()
    st.markdown("### 📅 Maç Aralığı")
    tum_gecmis = st.session_state.gecmis_analizler
    toplam_mac = len(tum_gecmis)
    mod = st.radio("Hangi maçlarda test edilsin?",
                   ["Tümü", "Ayar seti (ilk N maç)", "Test seti (N'den sonrası)"],
                   key="bt_mod")
    bolme = toplam_mac // 2
    if mod != "Tümü" and toplam_mac >= 4:
        bolme = st.slider("N", 1, toplam_mac - 1, max(1, toplam_mac // 2), 1, key="bt_bolme")
        if mod.startswith("Ayar"):
            st.caption(f"Test edilecek: ilk **{bolme}** maç")
        else:
            st.caption(f"Test edilecek: **{bolme + 1}.** maçtan sonuncuya, **{toplam_mac - bolme}** maç")
    else:
        st.caption(f"Test edilecek: tüm **{toplam_mac}** maç")
    if mod == "Tümü" or toplam_mac < 4:
        secili_gecmis = tum_gecmis; mod_etiket = f"Tümü ({toplam_mac} maç)"
    elif mod.startswith("Ayar"):
        secili_gecmis = tum_gecmis[:bolme]; mod_etiket = f"Ayar seti: ilk {bolme} maç"
    else:
        secili_gecmis = tum_gecmis[bolme:]; mod_etiket = f"Test seti: {bolme + 1}. maçtan sonrası ({toplam_mac - bolme} maç)"
    st.divider()
    if st.button("🚀 TEST ET", use_container_width=True, type="primary"):
        if not any(secenekler.values()):
            st.warning("⚠️ En az bir market seç.")
        else:
            with st.spinner("Test ediliyor..."):
                st.session_state.bt_mod_etiket = mod_etiket
                sonuc, detaylar = backtest_hesapla(secili_gecmis, secenekler, esikler)
                st.session_state.bt_sonuc = sonuc
                st.session_state.bt_detaylar = detaylar
                st.session_state.bt_market = secenekler
                st.session_state.bt_market_esik = esikler
    if st.session_state.bt_sonuc:
        sonuc = st.session_state.bt_sonuc
        st.divider()
        st.markdown("## 📊 BACKTEST SONUCU")
        st.caption(f"📅 {st.session_state.get('bt_mod_etiket', '')}")
        for key, baslik in [
            ("1x2", "🎯 1X2 (Maç Sonucu)"),
            ("kg_var", "🤝 KG Var"), ("kg_yok", "🤝 KG Yok"),
            ("ust", "⚽ Üst 2.5"), ("alt", "⚽ Alt 2.5"),
        ]:
            if secenekler[key]:
                d = sonuc[key]
                st.markdown(backtest_karti(baslik, d["dogru"], d["yanlis"]), unsafe_allow_html=True)
        st.divider()
        with st.expander(f"📋 Maç Detayları ({len(st.session_state.bt_detaylar)} maç)"):
            for m in st.session_state.bt_detaylar:
                st.markdown(f"**{m['takim_ev']} {m['skor']} {m['takim_dep']}**")
                gercek_1x2 = m.get("gercek_1x2", "?")
                st.caption(f"Gerçek: 1X2={gercek_1x2} / Gol={m['gercek_gol']} / KG={m['gercek_kg']}")
                for dd in m["detaylar"]:
                    st.markdown(f" • {dd}")
                st.markdown("")
    st.divider()
    if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary", key="bt_geri"):
        st.session_state.sayfa = "giris"; st.rerun()


# ==========================================
# AYARLAR
# ==========================================
elif st.session_state.sayfa == "ayarlar":
    if not admin_mi():
        st.error("❌ Bu sayfa sadece admin içindir.")
        if st.button("⬅️ Ana Sayfa", use_container_width=True, type="primary"):
            st.session_state.sayfa = "giris"; st.rerun()
        st.stop()
    st.markdown("<h1>⚙️ Eşik Ayarları</h1>", unsafe_allow_html=True)
    st.caption("Ana analiz için eşikleri buradan değiştirebilirsin.")
    st.divider()
    mevcut = st.session_state.esikler.copy()
    st.markdown("### 🎯 Maç Sonucu Eşikleri (1 / X / 2)")
    st.caption("Her seçim için ayrı eşik. En yüksek olasılıklı sonuç, kendi eşiğini geçerse öneri verilir.")
    c1x2_a, c1x2_b, c1x2_c = st.columns(3)
    with c1x2_a:
        yeni_esik_1 = st.slider("1 (Ev Sahibi) eşiği (%)", 0, 100, int(mevcut.get("esik_1", 55.0)), 1, key="ay_esik_1")
    with c1x2_b:
        yeni_esik_x = st.slider("X (Beraberlik) eşiği (%)", 0, 100, int(mevcut.get("esik_x", 55.0)), 1, key="ay_esik_x")
    with c1x2_c:
        yeni_esik_2 = st.slider("2 (Deplasman) eşiği (%)", 0, 100, int(mevcut.get("esik_2", 55.0)), 1, key="ay_esik_2")
    st.markdown("### ⚽ Gol Eşikleri")
    c1, c2 = st.columns(2)
    with c1:
        yeni_ust = st.slider("Üst 2.5 eşiği (%)", 0, 100, int(mevcut["ust"]), 1, key="ay_ust")
    with c2:
        yeni_alt = st.slider("Alt 2.5 eşiği (%)", 0, 100, int(mevcut["alt"]), 1, key="ay_alt")
    st.markdown("### 🤝 KG Eşikleri")
    c3, c4 = st.columns(2)
    with c3:
        yeni_kg_var = st.slider("KG Var eşiği (%)", 0, 100, int(mevcut["kg_var"]), 1, key="ay_kg_var")
    with c4:
        yeni_kg_yok = st.slider("KG Yok eşiği (%)", 0, 100, int(mevcut["kg_yok"]), 1, key="ay_kg_yok")
    st.divider()
    c_kaydet, c_sifirla, c_geri = st.columns(3)
    with c_kaydet:
        if st.button("💾 Kaydet", use_container_width=True, type="primary"):
            yeni_esikler = {
                "esik_1": float(yeni_esik_1), "esik_x": float(yeni_esik_x), "esik_2": float(yeni_esik_2),
                "ust": float(yeni_ust), "alt": float(yeni_alt),
                "kg_var": float(yeni_kg_var), "kg_yok": float(yeni_kg_yok),
            }
            st.session_state.esikler = yeni_esikler
            ayarlar_kaydet(yeni_esikler)
            st.success("✅ Eşikler kaydedildi!")
    with c_sifirla:
        if st.button("🔄 Sıfırla", use_container_width=True):
            varsayilan = {"ust": 65.0, "alt": 55.0, "kg_var": 57.0, "kg_yok": 72.0,
                          "esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0}
            st.session_state.esikler = varsayilan
            ayarlar_kaydet(varsayilan)
            st.success("✅ Varsayılan eşiklere dönüldü!")
            st.rerun()
    with c_geri:
        if st.button("⬅️ Ana Sayfa", use_container_width=True, key="ay_geri"):
            st.session_state.sayfa = "giris"; st.rerun()
    st.divider()
    st.info(f"""
    **Şu anki aktif eşikler:**
    - 1X2 → 1: **%{st.session_state.esikler.get('esik_1', 55.0):.0f}** • X: **%{st.session_state.esikler.get('esik_x', 55.0):.0f}** • 2: **%{st.session_state.esikler.get('esik_2', 55.0):.0f}**
    - Üst 2.5: **%{st.session_state.esikler['ust']:.0f}**
    - Alt 2.5: **%{st.session_state.esikler['alt']:.0f}**
    - KG Var: **%{st.session_state.esikler['kg_var']:.0f}**
    - KG Yok: **%{st.session_state.esikler['kg_yok']:.0f}**
    """)


# ==========================================
# ANALİZ SONUÇ
# ==========================================
elif st.session_state.sayfa == "sonuc":
    v = st.session_state.form_verileri
    a = analiz_hesapla(v)
    ust_25 = a["ust_25"]; alt_25 = a["alt_25"]
    kg_var_model = a["kg_var_model"]; kg_yok_model = a["kg_yok_model"]
    takim_ev = v.get("takim_ev", "") or "Ev Sahibi"
    takim_dep = v.get("takim_dep", "") or "Deplasman"
    skor_belli = v.get("skor_belli", False)
    skor_ev = v.get("skor_ev", 0); skor_dep = v.get("skor_dep", 0)
    st.markdown(mac_karti(takim_ev, takim_dep, skor_belli, skor_ev, skor_dep,
                          a["lam_ev"], a["lam_dep"],
                          saat=v.get("saat", ""), ulke=v.get("ulke", ""), tarih=v.get("tarih", "")),
                unsafe_allow_html=True)
    st.markdown(olasilik_paneli(a), unsafe_allow_html=True)
    with st.expander("📋 Okunan Tüm Veriler", expanded=False):
        okunan_veriler_paneli(v)
    if skor_belli:
        d = sonuc_hesapla({"veri": v, "analiz": a})
        with st.expander("✅ Tahmin Doğruluğu", expanded=True):
            st.markdown("**🎯 Öneri Tahminleri**")
            st.caption(f"1X2: 1=%{esik_1x2_al('1'):.0f} • X=%{esik_1x2_al('X'):.0f} • 2=%{esik_1x2_al('2'):.0f} | Üst %{esik_al('ust'):.0f} • Alt %{esik_al('alt'):.0f} • KG Var %{esik_al('kg_var'):.0f} • KG Yok %{esik_al('kg_yok'):.0f}")
            c1, c2, c3 = st.columns(3)
            for col, key in zip([c1, c2, c3], ["oneri_1x2", "oneri_gol", "oneri_kg"]):
                o = d[key]
                etiket = {"oneri_1x2": "1X2", "oneri_gol": "Gol", "oneri_kg": "KG"}[key]
                with col:
                    if o["tuttu"] is None:
                        st.markdown(f"⚫ **{etiket}**"); st.markdown("Öneri yok")
                    else:
                        ikon = "✅" if o["tuttu"] else "❌"
                        st.markdown(rozet(f"{ikon} {etiket}", "green" if o["tuttu"] else "red"), unsafe_allow_html=True)
                        st.markdown(f"{o['tahmin']}")
            gercek_1x2 = d.get("gercek_1x2", "?")
            st.caption(f"Gerçek sonuç: **{gercek_1x2}**")
    else:
        d = None
    with st.expander("🔍 Geniş Kapsamlı Analiz", expanded=False):
        genel_yorumlar = detayli_analiz_yorumu(v)
        if genel_yorumlar:
            for baslik, metin in genel_yorumlar:
                st.markdown(f"**{baslik}**"); st.markdown(metin); st.markdown("")
        else:
            st.caption("ℹ️ Genel form/sıralama verisi yok.")
        y1x2 = birx_iki_detayli_aciklama(v, a)
        if y1x2:
            st.markdown("---")
            for satir in y1x2:
                if satir.startswith("🎯"): st.markdown(f"**{satir}**"); st.markdown("")
                else: st.markdown(satir)
        gol_aciklama = gol_detayli_aciklama(v, a)
        if gol_aciklama:
            st.markdown("---")
            for satir in gol_aciklama:
                if satir.startswith("🎯"): st.markdown(f"**{satir}**"); st.markdown("")
                else: st.markdown(satir)
        kg_aciklama = kg_detayli_aciklama(v, a)
        if kg_aciklama:
            st.markdown("---")
            for satir in kg_aciklama:
                if satir.startswith("🤝"): st.markdown(f"**{satir}**"); st.markdown("")
                else: st.markdown(satir)
        if not y1x2 and not gol_aciklama and not kg_aciklama and not genel_yorumlar:
            st.info("ℹ️ Gösterilecek analiz yorumu yok.")
    st.divider()
    st.markdown("## 🏆 FİNAL ÖNERİ")
    en_yuksek_1x2 = max([("1", a["p1"]), ("X", a["px"]), ("2", a["p2"])], key=lambda x: x[1])
    secim_1x2, yuzde_1x2 = en_yuksek_1x2
    esik_1x2_secim = esik_1x2_al(secim_1x2)
    poz_1x2 = yuzde_1x2 >= esik_1x2_secim
    isim_map = {"1": "1 (Ev Sahibi)", "X": "X (Beraberlik)", "2": "2 (Deplasman)"}
    st.markdown(oneri_karti("🎯 Maç Sonucu (1X2)", isim_map[secim_1x2], yuzde_1x2, esik_1x2_secim, poz_1x2,
                            f"1: %{a['p1']:.1f} • X: %{a['px']:.1f} • 2: %{a['p2']:.1f}"), unsafe_allow_html=True)
    if ust_25 >= alt_25:
        gol_secim, gol_yuzde, gol_esik = "Üst 2.5", ust_25, esik_al("ust")
    else:
        gol_secim, gol_yuzde, gol_esik = "Alt 2.5", alt_25, esik_al("alt")
    gol_poz = gol_yuzde >= gol_esik
    st.markdown(oneri_karti("⚽ Gol", gol_secim, gol_yuzde, gol_esik, gol_poz,
                            f"Üst %{ust_25:.1f} • Alt %{alt_25:.1f}"), unsafe_allow_html=True)
    if kg_var_model >= kg_yok_model:
        kg_secim, kg_yuzde, kg_esik = "KG Var", kg_var_model, esik_al("kg_var")
    else:
        kg_secim, kg_yuzde, kg_esik = "KG Yok", kg_yok_model, esik_al("kg_yok")
    kg_poz = kg_yuzde >= kg_esik
    st.markdown(oneri_karti("🤝 Karşılıklı Gol", kg_secim, kg_yuzde, kg_esik, kg_poz,
                            f"Var %{kg_var_model:.1f} • Yok %{kg_yok_model:.1f}"), unsafe_allow_html=True)
    if st.session_state.gelecekten_gelindi and admin_mi():
        idx_g = st.session_state.aktif_gelecek_idx
        if idx_g is not None and 0 <= idx_g < len(st.session_state.gelecek_analizler):
            st.divider()
            st.markdown("### 📥 Sonucu Gir ve Geçmişe Taşı")
            sc1, sc2, sc3 = st.columns([1, 1, 1])
            with sc1:
                yeni_skor_ev = st.number_input("Ev Gol", min_value=0, max_value=20, value=int(v.get("skor_ev", 0)), step=1, key=f"gskor_ev_{idx_g}")
            with sc2:
                yeni_skor_dep = st.number_input("Dep Gol", min_value=0, max_value=20, value=int(v.get("skor_dep", 0)), step=1, key=f"gskor_dep_{idx_g}")
            with sc3:
                st.markdown(""); st.markdown("")
                if st.button("📥 Taşı", key=f"tasi_{idx_g}", use_container_width=True, type="primary"):
                    kayit = st.session_state.gelecek_analizler[idx_g]
                    kayit["veri"]["skor_ev"] = int(yeni_skor_ev)
                    kayit["veri"]["skor_dep"] = int(yeni_skor_dep)
                    kayit["veri"]["skor_belli"] = True
                    yeni_d = sonuc_hesapla(kayit)
                    if yeni_d: kayit["dogruluk"] = yeni_d
                    st.session_state.gecmis_analizler.append(kayit)
                    st.session_state.gelecek_analizler.pop(idx_g)
                    gecmis_kaydet(st.session_state.gecmis_analizler)
                    gelecek_kaydet(st.session_state.gelecek_analizler)
                    st.session_state.gelecekten_gelindi = False
                    st.session_state.aktif_gelecek_idx = None
                    st.session_state.sayfa = "gelecek"
                    st.rerun()
    kaydet_mi = gol_poz or kg_poz or poz_1x2
    if not st.session_state.kayit_yapildi and admin_mi():
        yeni_kayit = kayit_olustur(v, a)
        if d is not None: yeni_kayit["dogruluk"] = d
        if skor_belli:
            st.session_state.gecmis_analizler.append(yeni_kayit)
            gecmis_kaydet(st.session_state.gecmis_analizler)
            if kaydet_mi: st.success("📊 Geçmişe kaydedildi. (öneri vardı)")
            else: st.info("📊 Geçmişe kaydedildi. (öneri yoktu ama backtest için kaydedildi)")
        else:
            if kaydet_mi:
                st.session_state.gelecek_analizler.append(yeni_kayit)
                gelecek_kaydet(st.session_state.gelecek_analizler)
                st.info("🔮 Gelecek Maçlar'a kaydedildi.")
            else:
                st.warning("⚠️ Hiçbir market pozitif değil. Bu maç geleceğe **kaydedilmedi**.")
        st.session_state.kayit_yapildi = True
    st.divider()
    if st.button("🔄 Yeni Maç Analizi", use_container_width=True, type="primary"):
        st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI)
        st.session_state.sayfa = "giris"
        st.rerun()
