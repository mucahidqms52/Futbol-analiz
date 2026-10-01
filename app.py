import streamlit as st
import math
import copy
import re
import random
import json
import os
import html as _html
from datetime import datetime, timedelta

st.set_page_config(page_title="Futbol Analiz Pro", page_icon="⚽", layout="centered")

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
        padding-top: 0.8rem !important;
        padding-bottom: 0.8rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        max-width: 100% !important;
    }

    :root {
        --bg-0: #060a14;
        --bg-1: #0b1220;
        --bg-2: #101a2e;
        --card: #131c2e;
        --card-2: #16223a;
        --border: #1f2c44;
        --border-glow: rgba(34,197,94,0.35);
        --text: #eaf1fb;
        --muted: #7f92b3;
        --green: #22c55e;
        --green-dark: #15803d;
        --blue: #3b82f6;
        --yellow: #f59e0b;
        --red: #ef4444;
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
    div[data-testid="stNumberInput"] input {
        font-size: 0.85rem !important; padding: 0.35rem 0.5rem !important;
        height: 2rem !important;
    }
    div[data-testid="stNumberInput"] button { height: 2rem !important; }
    div[data-testid="stNumberInput"] > div { margin-bottom: 0.25rem !important; }

    .stTextArea textarea, .stTextInput input, div[data-testid="stNumberInput"] input {
        background: var(--card) !important;
        color: var(--text) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 10px !important;
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
        font-weight: 700 !important;
        font-size: 0.8rem !important;
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

    div[data-testid="stMetric"] {
        padding: 0.4rem !important;
        background: var(--card); border: 1px solid var(--border); border-radius: 10px;
    }
    div[data-testid="stMetricValue"] { font-size: 1rem !important; font-weight: 800 !important; }
    div[data-testid="stMetricLabel"] { font-size: 0.68rem !important; }

    div[data-testid="stExpander"] {
        background: linear-gradient(145deg, var(--card), #0f1829) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        overflow: hidden;
        margin-bottom: 8px !important;
    }

    div[data-testid="stExpander"] details > summary {
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
        padding: 0.5rem 0.8rem !important;
        font-size: 0.82rem !important;
        font-weight: 700 !important;
        line-height: 1.3 !important;
        min-height: 38px !important;
        overflow: hidden !important;
        cursor: pointer !important;
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
        display: none !important; visibility: hidden !important; width: 0 !important; height: 0 !important;
        font-size: 0 !important; overflow: hidden !important; position: absolute !important; left: -9999px !important; opacity: 0 !important; pointer-events: none !important;
    }

    div[data-testid="stExpander"] details > summary p,
    div[data-testid="stExpander"] details > summary div[data-testid="stMarkdownContainer"],
    div[data-testid="stExpander"] details > summary div[data-testid="stMarkdownContainer"] p {
        font-size: 0.82rem !important; font-weight: 700 !important; margin: 0 !important; line-height: 1.3 !important; color: #eaf1fb !important; white-space: normal !important; display: inline-block !important;
    }

    div[data-testid="stExpander"] details > summary > div { display: flex !important; align-items: center !important; gap: 6px !important; flex-wrap: nowrap !important; }
    div[data-testid="stExpander"] details > summary svg { flex-shrink: 0 !important; width: 14px !important; height: 14px !important; min-width: 14px !important; transition: transform 0.2s ease !important; }
    div[data-testid="stExpander"] details > div[role="region"] { padding: 0.4rem 0.8rem 0.8rem 0.8rem !important; font-size: 0.82rem !important; }

    div[data-testid="stAlert"] { padding: 0.4rem 0.7rem !important; font-size: 0.8rem !important; border-radius: 10px !important; }
    div[data-testid="stFileUploader"] section { background: var(--card) !important; border: 1.5px dashed var(--border) !important; border-radius: 12px !important; }

    .st-key-fa_nav div[data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: 0.3rem !important; }
    .st-key-fa_nav div[data-testid="stColumn"], .st-key-fa_nav div[data-testid="column"] { min-width: 0 !important; flex: 1 1 0 !important; width: auto !important; }
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
        border: 1px solid var(--border); border-radius: 16px; padding: 14px 12px; margin: 6px 0 10px 0;
        text-align: center; box-shadow: 0 10px 32px rgba(0,0,0,0.4), 0 0 0 1px rgba(34,197,94,0.05) inset;
    }
    .stApp .fa-hero::before {
        content: ""; position: absolute; inset: 0;
        background: radial-gradient(circle at 50% 0%, rgba(34,197,94,0.15), transparent 60%);
        pointer-events: none;
    }
    .stApp .fa-teams { display: flex; align-items: center; justify-content: space-between; gap: 6px; position: relative; z-index: 1; }
    .stApp .fa-team { flex: 1; font-weight: 800; font-size: 0.9rem; line-height: 1.2; word-break: break-word; letter-spacing: 0.2px; }
    .stApp .fa-score { font-size: 1.6rem; font-weight: 900; color: var(--green) !important; min-width: 80px; letter-spacing: 0.5px; text-shadow: 0 0 20px rgba(34,197,94,0.5); }
    .stApp .fa-vs { font-size: 0.9rem; font-weight: 800; color: var(--muted) !important; min-width: 50px; letter-spacing: 1px; }
    .stApp .fa-sub { font-size: 0.68rem; color: var(--muted) !important; margin-top: 6px; letter-spacing: 0.2px; }

    .stApp .fa-card {
        background: linear-gradient(145deg, var(--card), #0f1829);
        border: 1px solid var(--border); border-radius: 14px; padding: 10px 12px; margin-bottom: 10px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.25); transition: all 0.25s ease;
    }
    .stApp .fa-card:hover { border-color: rgba(34,197,94,0.3); transform: translateY(-1px); }
    .stApp .fa-card.fa-pos {
        border-color: rgba(34,197,94,0.55);
        box-shadow: 0 8px 28px rgba(34,197,94,0.15), 0 0 0 1px rgba(34,197,94,0.15) inset;
    }
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

    .login-hero { text-align: center; padding: 40px 10px 24px 10px; position: relative; }
    .login-logo { font-size: 4.2rem; line-height: 1; margin-bottom: 14px; display: inline-block; filter: drop-shadow(0 0 30px rgba(34,197,94,0.6)); animation: logoPulse 3s ease-in-out infinite; }
    @keyframes logoPulse {
        0%, 100% { transform: scale(1) rotate(0deg); filter: drop-shadow(0 0 20px rgba(34,197,94,0.5)); }
        50% { transform: scale(1.08) rotate(-3deg); filter: drop-shadow(0 0 40px rgba(34,197,94,0.9)); }
    }
    .login-title {
        font-size: 2rem !important; font-weight: 900 !important;
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 45%, #3b82f6 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; margin: 0 !important; padding: 0 !important;
        letter-spacing: 1.2px; border: none !important; text-align: center !important;
    }
    .login-subtitle { font-size: 0.82rem; color: var(--muted) !important; margin-top: 8px; letter-spacing: 0.5px; font-weight: 500; }

    div[data-testid="stForm"] {
        background: linear-gradient(145deg, rgba(19,28,46,0.9), rgba(11,18,32,0.98)) !important;
        border: 1.5px solid rgba(34,197,94,0.2) !important; border-radius: 20px !important;
        padding: 22px 18px !important; box-shadow: 0 20px 60px rgba(0,0,0,0.55), 0 0 0 1px rgba(34,197,94,0.05) inset !important;
        backdrop-filter: blur(16px);
    }
    div[data-testid="stForm"] label p { font-size: 0.78rem !important; font-weight: 700 !important; color: #cbd5e1 !important; letter-spacing: 0.3px; margin-bottom: 5px !important; }
    div[data-testid="stForm"] input { height: 42px !important; font-size: 0.9rem !important; padding: 0 14px !important; background: rgba(11,18,32,0.9) !important; border: 1.5px solid var(--border) !important; border-radius: 10px !important; transition: all 0.2s ease; }
    div[data-testid="stForm"] input:focus { border-color: var(--green) !important; box-shadow: 0 0 0 4px rgba(34,197,94,0.15) !important; outline: none !important; }
    div[data-testid="stForm"] button { height: 42px !important; font-size: 0.9rem !important; font-weight: 800 !important; border-radius: 10px !important; letter-spacing: 0.3px; transition: all 0.2s ease; }
    div[data-testid="stForm"] button[kind="primary"] { background: linear-gradient(135deg, #16a34a, #22c55e) !important; box-shadow: 0 8px 24px rgba(34,197,94,0.4) !important; border: none !important; }
    div[data-testid="stForm"] button[kind="primary"]:hover { box-shadow: 0 12px 32px rgba(34,197,94,0.55) !important; transform: translateY(-2px); }

    .mh-hero {
        position: relative; overflow: hidden; text-align: center; padding: 28px 14px 22px 14px;
        background: linear-gradient(135deg, rgba(22,35,61,0.9), rgba(15,26,46,0.95));
        border: 1.5px solid rgba(34,197,94,0.25); border-radius: 20px; margin: 6px 0 16px 0;
        box-shadow: 0 16px 48px rgba(0,0,0,0.45), 0 0 0 1px rgba(34,197,94,0.06) inset;
    }
    .mh-hero-icon { font-size: 3rem; line-height: 1; margin-bottom: 10px; display: inline-block; filter: drop-shadow(0 0 24px rgba(34,197,94,0.65)); animation: logoPulse 3s ease-in-out infinite; position: relative; z-index: 1; }
    .mh-hero-title {
        font-size: 1.7rem; font-weight: 900;
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 45%, #3b82f6 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
        letter-spacing: 1px; position: relative; z-index: 1; margin: 0;
    }
    .mh-hero-sub { font-size: 0.8rem; color: var(--muted); margin-top: 8px; letter-spacing: 0.4px; position: relative; z-index: 1; }
    .mh-hero-badge { display: inline-block; margin-top: 12px; padding: 4px 14px; background: rgba(34,197,94,0.12); border: 1px solid rgba(34,197,94,0.45); border-radius: 99px; font-size: 0.7rem; font-weight: 800; color: var(--green) !important; letter-spacing: 0.8px; position: relative; z-index: 1; }

    .mh-stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 0 0 16px 0; }
    .mh-stat {
        position: relative; background: linear-gradient(145deg, #16233d, #0f1a2e);
        border: 1px solid var(--border); border-radius: 16px; padding: 14px 10px 12px 10px;
        text-align: center; overflow: hidden; transition: all 0.25s ease; box-shadow: 0 6px 20px rgba(0,0,0,0.25);
    }
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
</style>
""", unsafe_allow_html=True)

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

def saat_2_saat_ileri(saat_str):
    if not saat_str: return saat_str
    m = re.match(r'^(\d{1,2}):(\d{2})$', str(saat_str).strip())
    if not m: return saat_str
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
                gun = int(m.group(1)); ay = int(m.group(2))
                y_raw = m.group(3)
                yil = int(y_raw) if len(y_raw) == 4 else 2000 + int(y_raw)
        sa_h, sa_m = 99, 99
        if saat:
            m2 = re.match(r'^(\d{1,2}):(\d{2})$', saat)
            if m2:
                sa_h = int(m2.group(1)); sa_m = int(m2.group(2))
        return (yil, ay, gun, sa_h, sa_m)
    except Exception:
        return (9999, 99, 99, 99, 99)

ESIK_YUKSEK = 65.0
ESIK_ORTA = 55.0
ESIK_BELIRSIZ = 50.0
MONTE_CARLO_N = 10000

VARSAYILAN_VERI = {
    "ppg_ev": 0.0, "mpg_dep": 0.0, "form_str_ev": "", "form_str_dep": "",
    "siralama_ev": 0, "siralama_dep": 0, "puan_ev": 0, "puan_dep": 0,
    "xg_ev": 0.0, "xg_dep": 0.0, "atilan_ev": 0.0, "atilan_dep": 0.0,
    "yenen_ev": 0.0, "yenen_dep": 0.0, "clean_sheets_ev": 0.0, "clean_sheets_dep": 0.0,
    "team_scored_ev": 0.0, "team_scored_dep": 0.0, "team_scored_2_ev": 0.0, "team_scored_2_dep": 0.0,
    "scored_both_halves_ev": 0.0, "scored_both_halves_dep": 0.0, "goal_both_halves_ev": 0.0, "goal_both_halves_dep": 0.0,
    "ust05_ev": 80.0, "ust05_dep": 80.0, "ust15_ev": 50.0, "ust15_dep": 50.0,
    "ust25_ev": 30.0, "ust25_dep": 30.0, "ust35_ev": 20.0, "ust35_dep": 20.0,
    "kg_siklik_ev": 50.0, "kg_siklik_dep": 50.0, "btts_1h_ev": 0.0, "btts_1h_dep": 0.0,
    "btts_2h_ev": 0.0, "btts_2h_dep": 0.0, "btts_over15_ev": 0.0, "btts_over15_dep": 0.0,
    "btts_over25_ev": 0.0, "btts_over25_dep": 0.0, "tg_0_ev": 0.0, "tg_0_dep": 0.0,
    "tg_1_ev": 0.0, "tg_1_dep": 0.0, "tg_2_ev": 0.0, "tg_2_dep": 0.0,
    "tg_3_ev": 0.0, "tg_3_dep": 0.0, "tg_4_ev": 0.0, "tg_4_dep": 0.0,
    "tg_01_ev": 0.0, "tg_01_dep": 0.0, "tg_23_ev": 0.0, "tg_23_dep": 0.0,
    "tg_4p_ev": 0.0, "tg_4p_dep": 0.0, "ht_ust05_ev": 0.0, "ht_ust05_dep": 0.0,
    "ht_ust15_ev": 0.0, "ht_ust15_dep": 0.0, "ht_ust25_ev": 0.0, "ht_ust25_dep": 0.0,
    "wht_wft_ev": 0.0, "wht_wft_dep": 0.0, "wht_dft_ev": 0.0, "wht_dft_dep": 0.0,
    "wht_lft_ev": 0.0, "wht_lft_dep": 0.0, "dht_wft_ev": 0.0, "dht_wft_dep": 0.0,
    "dht_dft_ev": 0.0, "dht_dft_dep": 0.0, "dht_lft_ev": 0.0, "dht_lft_dep": 0.0,
    "lht_wft_ev": 0.0, "lht_wft_dep": 0.0, "lht_dft_ev": 0.0, "lht_dft_dep": 0.0,
    "lht_lft_ev": 0.0, "lht_lft_dep": 0.0, "galibiyet_ev": 30.0, "galibiyet_dep": 30.0,
    "beraberlik_ev": 30.0, "beraberlik_dep": 30.0, "maglubiyet_ev": 30.0, "maglubiyet_dep": 30.0,
    "win_1h_ev": 0.0, "win_1h_dep": 0.0, "draw_ht_ev": 0.0, "draw_ht_dep": 0.0,
    "lose_1h_ev": 0.0, "lose_1h_dep": 0.0, "win_btts_ev": 0.0, "win_btts_dep": 0.0,
    "draw_btts_ev": 0.0, "draw_btts_dep": 0.0, "lose_btts_ev": 0.0, "lose_btts_dep": 0.0,
    "win_over15_ev": 0.0, "win_over15_dep": 0.0, "lose_over15_ev": 0.0, "lose_over15_dep": 0.0,
    "takim_ev": "", "takim_dep": "", "skor_ev": 0, "skor_dep": 0, "skor_belli": False,
    "lig_ort_toplam": 0.0, "lig_ust25": 0.0, "lig_kg": 0.0, "saat": "", "tarih": "", "ulke": "", "format": "bilinmiyor",
}

MAX_GOL = 8
BELIRSIZLIK = 0.20

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

if "bt_market" not in st.session_state: st.session_state.bt_market = {"1x2": False, "kg_var": False, "kg_yok": False, "ust": False, "alt": False}
if "bt_market_esik" not in st.session_state:
    st.session_state.bt_market_esik = {"esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0, "kg_var": 70.0, "kg_yok": 70.0, "ust": 70.0, "alt": 70.0}
if "bt_sonuc" not in st.session_state: st.session_state.bt_sonuc = None
if "bt_detaylar" not in st.session_state: st.session_state.bt_detaylar = []

def admin_mi(): return st.session_state.get("rol") == "admin"
def esik_al(key): return st.session_state.esikler.get(key, 50.0)
def esik_1x2_al(secim):
    key_map = {"1": "esik_1", "X": "esik_x", "2": "esik_2"}
    return st.session_state.esikler.get(key_map.get(secim, ""), 55.0)

ULKE_BAYRAK = {
    "switzerland": "🇨🇭", "isviçre": "🇨🇭", "i̇sviçre": "🇨🇭", "england": "🏴", "ingiltere": "🏴", "i̇ngiltere": "🏴",
    "spain": "🇪🇸", "ispanya": "🇪🇸", "i̇spanya": "🇪🇸", "italy": "🇮🇹", "italya": "🇮🇹", "i̇talya": "🇮🇹",
    "germany": "🇩🇪", "almanya": "🇩🇪", "france": "🇫🇷", "fransa": "🇫🇷", "netherlands": "🇳🇱", "hollanda": "🇳🇱",
    "portugal": "🇵🇹", "portekiz": "🇵🇹", "belgium": "🇧🇪", "belçika": "🇧🇪", "turkey": "🇹🇷", "türkiye": "🇹🇷", "turkiye": "🇹🇷",
    "argentina": "🇦🇷", "arjantin": "🇦🇷", "brazil": "🇧🇷", "brezilya": "🇧🇷", "mexico": "🇲🇽", "meksika": "🇲🇽",
    "usa": "🇺🇸", "japan": "🇯🇵", "japonya": "🇯🇵", "south korea": "🇰🇷", "güney kore": "🇰🇷", "china": "🇨🇳", "çin": "🇨🇳",
    "russia": "🇷🇺", "rusya": "🇷🇺", "ukraine": "🇺🇦", "ukrayna": "🇺🇦", "poland": "🇵🇱", "polonya": "🇵🇱",
    "greece": "🇬🇷", "yunanistan": "🇬🇷", "scotland": "🏴", "i̇skoçya": "🏴", "austria": "🇦🇹", "avusturya": "🇦🇹",
    "croatia": "🇭🇷", "hırvatistan": "🇭🇷", "serbia": "🇷🇸", "sırbistan": "🇷🇸", "romania": "🇷🇴", "romanya": "🇷🇴",
    "denmark": "🇩🇰", "danimarka": "🇩🇰", "sweden": "🇸🇪", "i̇sveç": "🇸🇪", "norway": "🇳🇴", "norveç": "🇳🇴",
}

def ulke_bayrak_bul(ulke_adi):
    if not ulke_adi: return "🌍"
    u = ulke_adi.lower().strip()
    for anahtar in sorted(ULKE_BAYRAK.keys(), key=len, reverse=True):
        if anahtar in u: return ULKE_BAYRAK[anahtar]
    return "🌍"

def _ulke_bul(metin):
    m = re.search(r'Standings\s+([^\n]+)', metin)
    if not m: return ""
    satir = m.group(1).strip()
    if not satir: return ""
    alt = satir.lower()
    for anahtar in sorted(ULKE_BAYRAK.keys(), key=len, reverse=True):
        if anahtar in alt: return anahtar
    parcalar = satir.split()
    return " ".join(parcalar[:2]) if len(parcalar) >= 2 else (parcalar[0] if parcalar else "")

def clamp(x, lo, hi): return max(lo, min(hi, x))
def ort_iki(a, b):
    vals = [x for x in [a, b] if x is not None and x > 0]
    return sum(vals) / len(vals) if vals else 0

def guven_seviyesi_bul(olasilik):
    if olasilik >= ESIK_YUKSEK: return ("yuksek", "🟢", "success", "Yüksek")
    if olasilik >= ESIK_ORTA:   return ("orta", "🟡", "warning", "Orta")
    if olasilik >= ESIK_BELIRSIZ: return ("belirsiz", "🔴", "error", "Belirsiz")
    return ("cok_dusuk", "⚫", "error", "Düşük")

def oneri_istatistik_guncel(gecmis):
    ist = {"1x2": {"tam": 0, "yakin": 0, "yanlis": 0}, "gol": {"tam": 0, "yakin": 0, "yanlis": 0}, "kg": {"tam": 0, "yakin": 0, "yanlis": 0}}
    for g in gecmis:
        try:
            v = g["veri"]
            if not v.get("skor_belli", False): continue
            try: ya = yeniden_analiz(v)
            except Exception: ya = g.get("analiz", {})
            d = sonuc_hesapla({"veri": v, "analiz": ya})
            if not d: continue
            for key in ["oneri_1x2", "oneri_gol", "oneri_kg"]:
                kisa = key.replace("oneri_", "")
                durum = d[key].get("durum")
                if durum == "tam": ist[kisa]["tam"] += 1
                elif durum == "yanlis": ist[kisa]["yanlis"] += 1
        except Exception: continue
    return ist

def wilson_aralik(dogru, toplam, z=1.96):
    if toplam <= 0: return 0.0, 0.0
    p = dogru / toplam
    payda = 1 + z * z / toplam
    merkez = (p + z * z / (2 * toplam)) / payda
    yari = z * math.sqrt(p * (1 - p) / toplam + z * z / (4 * toplam * toplam)) / payda
    return max(0.0, (merkez - yari) * 100), min(100.0, (merkez + yari) * 100)

def _form_ppg(s): return sum(3 if c == "W" else 1 if c == "D" else 0 for c in s) / max(len(s), 1)

def yeniden_analiz(v):
    v2 = copy.deepcopy(v)
    if v2.get("form_str_ev"): v2["ppg_ev"] = _form_ppg(v2["form_str_ev"])
    if v2.get("form_str_dep"): v2["mpg_dep"] = _form_ppg(v2["form_str_dep"])
    anahtar = json.dumps(v2, sort_keys=True, ensure_ascii=False)
    if "bt_analiz_cache" not in st.session_state: st.session_state.bt_analiz_cache = {}
    cache = st.session_state.bt_analiz_cache
    if anahtar not in cache:
        a = analiz_hesapla(v2)
        cache[anahtar] = {"ust_25": a["ust_25"], "kg_var_model": a["kg_var_model"], "p1": a["p1"], "px": a["px"], "p2": a["p2"]}
    return cache[anahtar]

def backtest_hesapla(gecmis, market_sec, market_esik):
    sonuc = {"1x2": {"dogru": 0, "yanlis": 0}, "kg_var": {"dogru": 0, "yanlis": 0}, "kg_yok": {"dogru": 0, "yanlis": 0}, "ust": {"dogru": 0, "yanlis": 0}, "alt": {"dogru": 0, "yanlis": 0}}
    mac_detaylari = []
    for g in gecmis:
        try:
            v = g["veri"]
            analiz = g.get("analiz", {})
            if not v.get("skor_belli", False): continue
            skor_ev = int(v.get("skor_ev", 0)); skor_dep = int(v.get("skor_dep", 0))
            toplam_gol = skor_ev + skor_dep
            gercek_kg_var = (skor_ev > 0 and skor_dep > 0)
            gercek_ust = toplam_gol > 2.5
            gercek_1x2 = "1" if skor_ev > skor_dep else ("X" if skor_ev == skor_dep else "2")
            yeni_analiz = yeniden_analiz(v)
            ust_25 = yeni_analiz["ust_25"]; kg_var = yeni_analiz["kg_var_model"]
            p1_y = yeni_analiz["p1"]; px_y = yeni_analiz["px"]; p2_y = yeni_analiz["p2"]
            alt_25 = 100 - ust_25; kg_yok = 100 - kg_var
            mac_kayit = {"takim_ev": v.get("takim_ev", "Ev"), "takim_dep": v.get("takim_dep", "Dep"), "skor": f"{skor_ev}-{skor_dep}", "gercek_1x2": gercek_1x2, "detaylar": []}
            if market_sec.get("1x2", False):
                secim, yuzde = max([("1", p1_y), ("X", px_y), ("2", p2_y)], key=lambda x: x[1])
                esik_secim = market_esik.get({"1": "esik_1", "X": "esik_x", "2": "esik_2"}[secim], 55.0)
                if yuzde >= esik_secim:
                    if secim == gercek_1x2: sonuc["1x2"]["dogru"] += 1; mac_kayit["detaylar"].append(f"1X2: {secim} ✅")
                    else: sonuc["1x2"]["yanlis"] += 1; mac_kayit["detaylar"].append(f"1X2: {secim} ❌")
            if market_sec.get("kg_var", False) and kg_var >= market_esik["kg_var"] and kg_var >= kg_yok:
                if gercek_kg_var: sonuc["kg_var"]["dogru"] += 1; mac_kayit["detaylar"].append("KG Var ✅")
                else: sonuc["kg_var"]["yanlis"] += 1; mac_kayit["detaylar"].append("KG Var ❌")
            if market_sec.get("kg_yok", False) and kg_yok >= market_esik["kg_yok"] and kg_yok >= kg_var:
                if not gercek_kg_var: sonuc["kg_yok"]["dogru"] += 1; mac_kayit["detaylar"].append("KG Yok ✅")
                else: sonuc["kg_yok"]["yanlis"] += 1; mac_kayit["detaylar"].append("KG Yok ❌")
            if market_sec.get("ust", False) and ust_25 >= market_esik["ust"] and ust_25 >= alt_25:
                if gercek_ust: sonuc["ust"]["dogru"] += 1; mac_kayit["detaylar"].append("Üst ✅")
                else: sonuc["ust"]["yanlis"] += 1; mac_kayit["detaylar"].append("Üst ❌")
            if market_sec.get("alt", False) and alt_25 >= market_esik["alt"] and alt_25 >= ust_25:
                if not gercek_ust: sonuc["alt"]["dogru"] += 1; mac_kayit["detaylar"].append("Alt ✅")
                else: sonuc["alt"]["yanlis"] += 1; mac_kayit["detaylar"].append("Alt ❌")
            if mac_kayit["detaylar"]: mac_detaylari.append(mac_kayit)
        except Exception: continue
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
    return None, None

def _sira_bul(metin, takim_adi):
    if not takim_adi: return None, None
    pattern = r'(?:^|\n)\s*(\d{1,2})\s*\r?\n\s*' + re.escape(takim_adi) + r'\s*\r?\n\s*' + re.escape(takim_adi) + r'\s*\r?\n\s*(\d+)\s*\t'
    m = re.search(pattern, metin, re.MULTILINE)
    if m:
        try: return int(m.group(1)), int(m.group(2))
        except (ValueError, AttributeError): pass
    return None, None

def sportytrader_veri_cikar(metin):
    veri = {}; okunamayanlar = []
    m = re.search(r'^([A-ZÇĞİÖŞÜ][\w\s\.\-]+?)\s*-\s*([A-ZÇĞİÖŞÜ][\w\s\.\-]+?)\s+Stats', metin, re.MULTILINE)
    if m: veri["takim_ev"] = m.group(1).strip(); veri["takim_dep"] = m.group(2).strip()

    m = re.search(r'Time\s*\t\s*(\d{1,2}:\d{2})', metin)
    if m: veri["saat"] = m.group(1).strip()
    m = re.search(r'Date\s*\t\s*(\d{1,2}\.\d{1,2}\.\d{2,4})', metin)
    if m: veri["tarih"] = m.group(1).strip()

    veri["ulke"] = _ulke_bul(metin)
    m = re.search(r'FT\s*\r?\n\s*(\d+)\s*-\s*(\d+)', metin)
    if m: veri["skor_ev"] = int(m.group(1)); veri["skor_dep"] = int(m.group(2)); veri["skor_belli"] = True
    else: veri["skor_belli"] = False

    takim_ev, takim_dep = veri.get("takim_ev", ""), veri.get("takim_dep", "")
    idx = metin.find("Main Stats")
    if idx != -1:
        blok = metin[idx:idx+1500]
        v1, v2 = _cift_tab("Goals scored per game", blok)
        if v1 is not None: veri["atilan_ev"] = v1; veri["atilan_dep"] = v2
        v1, v2 = _cift_tab("Goals conceded per game", blok)
        if v1 is not None: veri["yenen_ev"] = v1; veri["yenen_dep"] = v2
        v1, v2 = _cift_tab("Clean sheets", blok)
        if v1 is not None: veri["clean_sheets_ev"] = v1; veri["clean_sheets_dep"] = v2

    if takim_ev:
        s, p = _sira_bul(metin, takim_ev)
        if s is not None: veri["siralama_ev"] = s; veri["puan_ev"] = p or 0
    if takim_dep:
        s, p = _sira_bul(metin, takim_dep)
        if s is not None: veri["siralama_dep"] = s; veri["puan_dep"] = p or 0

    if veri.get("siralama_ev", 0) == 0: okunamayanlar.append("Sıralama (Ev)")
    if veri.get("siralama_dep", 0) == 0: okunamayanlar.append("Sıralama (Dep)")

    m = re.search(r'\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\nForm\s*\t?\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])\s*\r?\n([WDL])', metin)
    if m:
        form_ev = m.group(1)+m.group(2)+m.group(3)+m.group(4)+m.group(5)
        form_dep = m.group(6)+m.group(7)+m.group(8)+m.group(9)+m.group(10)
        veri["form_str_ev"] = form_ev; veri["form_str_dep"] = form_dep
        veri["ppg_ev"] = _form_ppg(form_ev); veri["mpg_dep"] = _form_ppg(form_dep)

    veri["format"] = "sportytrader"
    return veri, okunamayanlar

def metinden_veri_cikar(metin):
    metin = metin.replace(",", ".")
    if "Main Stats" in metin and "Goals scored per game" in metin:
        veri, okunamayanlar = sportytrader_veri_cikar(metin)
        if not veri.get("takim_ev"): okunamayanlar.append("Takım isimleri (Ev)")
        if not veri.get("takim_dep"): okunamayanlar.append("Takım isimleri (Dep)")
        if veri.get("saat"): veri["saat"] = saat_2_saat_ileri(veri["saat"])
        return veri, okunamayanlar
    return {"format": "genel"}, []

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
    hucum_ev_baz = (xg_e * 0.60) + (atilan_e * 0.40) if xg_e > 0 else (atilan_e if atilan_e > 0 else 1.2)
    hucum_dep_baz = (xg_d * 0.60) + (atilan_d * 0.40) if xg_d > 0 else (atilan_d if atilan_d > 0 else 1.0)
    savunma_dep_zaaf = yenen_d if yenen_d > 0 else 1.2
    savunma_ev_zaaf = yenen_e if yenen_e > 0 else 1.0

    lam_ev_ham = (hucum_ev_baz * 0.60) + (savunma_dep_zaaf * 0.40)
    lam_dep_ham = (hucum_dep_baz * 0.60) + (savunma_ev_zaaf * 0.40)
    form_ev = clamp(1 + (v.get("ppg_ev", 1.5) - 1.5) / 15, 0.85, 1.15)
    form_dep = clamp(1 + (v.get("mpg_dep", 1.5) - 1.5) / 15, 0.85, 1.15)
    lam_ev = lam_ev_ham * 1.05 * form_ev
    lam_dep = lam_dep_ham * 0.95 * form_dep
    return clamp(lam_ev, 0.05, 4.5), clamp(lam_dep, 0.05, 4.5), 0.80

def matristen_olasilik(matris, max_gol=MAX_GOL):
    p1 = px = p2 = ust_25 = kg_var = toplam = 0.0
    for i in range(max_gol):
        for j in range(max_gol):
            p = matris[i][j]; toplam += p
            if i > j: p1 += p
            elif i == j: px += p
            else: p2 += p
            if i + j > 2.5: ust_25 += p
            if i > 0 and j > 0: kg_var += p
    return {"1": p1, "X": px, "2": p2, "ust_25": ust_25, "kg_var": kg_var, "toplam": toplam}

def veri_yeterli_mi(v):
    return sum(1 for x in [v.get("atilan_ev", 0), v.get("atilan_dep", 0), v.get("yenen_ev", 0), v.get("yenen_dep", 0)] if x > 0) >= 2

def monte_carlo_simulasyon(lam_ev_base, lam_dep_base, n=MONTE_CARLO_N):
    rng = random.Random(int(round(lam_ev_base * 1_000_000)))
    sayac = {"1": 0, "X": 0, "2": 0, "ust25": 0, "kg_var": 0}
    for _ in range(n):
        ev_gol = min(MAX_GOL - 1, poisson_random(lam_ev_base * rng.uniform(0.8, 1.2), rng))
        dep_gol = min(MAX_GOL - 1, poisson_random(lam_dep_base * rng.uniform(0.8, 1.2), rng))
        if ev_gol > dep_gol: sayac["1"] += 1
        elif ev_gol == dep_gol: sayac["X"] += 1
        else: sayac["2"] += 1
        if ev_gol + dep_gol > 2.5: sayac["ust25"] += 1
        if ev_gol > 0 and dep_gol > 0: sayac["kg_var"] += 1
    return {k: v / n * 100 for k, v in sayac.items()}

def analiz_hesapla(v):
    lam_ev, lam_dep, guven = hesapla_lambda(v)
    matris = poisson_matris(lam_ev, lam_dep, MAX_GOL)
    olas = matristen_olasilik(matris, MAX_GOL)
    toplam = olas["toplam"] or 1
    mc = monte_carlo_simulasyon(lam_ev, lam_dep, 1000)
    p1 = (olas["1"] / toplam * 100 * 0.6) + (mc["1"] * 0.4)
    px = (olas["X"] / toplam * 100 * 0.6) + (mc["X"] * 0.4)
    p2 = (olas["2"] / toplam * 100 * 0.6) + (mc["2"] * 0.4)
    t = p1 + px + p2
    if t > 0: p1, px, p2 = (p1/t)*100, (px/t)*100, (p2/t)*100
    ust_25 = (olas["ust_25"] / toplam * 100 * 0.6) + (mc["ust25"] * 0.4)
    kg_var_model = (olas["kg_var"] / toplam * 100 * 0.6) + (mc["kg_var"] * 0.4)
    return {
        "lam_ev": lam_ev, "lam_dep": lam_dep, "p1": p1, "px": px, "p2": p2,
        "ust_25": ust_25, "alt_25": 100 - ust_25, "kg_var_model": kg_var_model, "kg_yok_model": 100 - kg_var_model,
        "tahmini_gol": lam_ev + lam_dep, "en_olasi": max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1]),
        "en_guvenli": max([("1X", p1+px), ("X2", p2+px)], key=lambda x: x[1]),
        "en_olasi_gol": "Üst" if ust_25 > 50 else "Alt", "en_olasi_kg": "Var" if kg_var_model > 50 else "Yok"
    }

def kayit_olustur(v, a):
    return {"veri": copy.deepcopy(v), "analiz": {"p1": a["p1"], "px": a["px"], "p2": a["p2"], "tahmini_gol": a["tahmini_gol"], "kg_var_model": a["kg_var_model"], "ust_25": a["ust_25"]}}

def sonuc_hesapla(kayit):
    v = kayit["veri"]; analiz = kayit.get("analiz", {})
    if not v.get("skor_belli", False): return None
    skor_ev = v.get("skor_ev", 0); skor_dep = v.get("skor_dep", 0)
    gercek_1x2 = "1" if skor_ev > skor_dep else ("X" if skor_ev == skor_dep else "2")
    gercek_ust = (skor_ev + skor_dep) > 2.5
    gercek_kg_var = (skor_ev > 0 and skor_dep > 0)
    p1_a, px_a, p2_a = analiz.get("p1", 33.3), analiz.get("px", 33.3), analiz.get("p2", 33.4)
    secim_1x2, yuzde_1x2 = max([("1", p1_a), ("X", px_a), ("2", p2_a)], key=lambda x: x[1])
    oneri_1x2 = secim_1x2 if yuzde_1x2 >= esik_1x2_al(secim_1x2) else None
    ust_25 = analiz.get("ust_25", 50)
    oneri_gol = "Üst" if ust_25 >= esik_al("ust") else ("Alt" if (100 - ust_25) >= esik_al("alt") else None)
    kg_var = analiz.get("kg_var_model", 50)
    oneri_kg = "Var" if kg_var >= esik_al("kg_var") else ("Yok" if (100 - kg_var) >= esik_al("kg_yok") else None)
    return {
        "oneri_1x2": {"tahmin": oneri_1x2, "tuttu": (oneri_1x2 == gercek_1x2) if oneri_1x2 else None},
        "oneri_gol": {"tahmin": oneri_gol, "tuttu": ((oneri_gol == "Üst") == gercek_ust) if oneri_gol else None},
        "oneri_kg": {"tahmin": oneri_kg, "tuttu": ((oneri_kg == "Var") == gercek_kg_var) if oneri_kg else None},
        "gercek_1x2": gercek_1x2, "gercek_gol": "Üst" if gercek_ust else "Alt", "gercek_kg": "Var" if gercek_kg_var else "Yok"
    }

def detayli_analiz_yorumu(v):
    yorumlar = []
    ppg, mpg = v.get("ppg_ev", 0.0), v.get("mpg_dep", 0.0)
    if ppg > 0 or mpg > 0:
        yorumlar.append(("📈 FORM", f"Ev sahibi form: **{ppg:.2f}** • Deplasman form: **{mpg:.2f}**"))
    s_ev, s_dep = v.get("siralama_ev", 0), v.get("siralama_dep", 0)
    if s_ev > 0 and s_dep > 0:
        yorumlar.append(("🏆 SIRALAMA", f"Ev sahibi: **{s_ev}.** • Deplasman: **{s_dep}.**"))
    return yorumlar

def okunan_veriler_paneli(v):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**{v.get('takim_ev', 'Ev')}**")
        st.markdown(f"- Atılan: **{v.get('atilan_ev', 0):.2f}**")
        st.markdown(f"- Yenen: **{v.get('yenen_ev', 0):.2f}**")
        st.markdown(f"- Sıralama: **{v.get('siralama_ev', 0)}**")
    with c2:
        st.markdown(f"**{v.get('takim_dep', 'Dep')}**")
        st.markdown(f"- Atılan: **{v.get('atilan_dep', 0):.2f}**")
        st.markdown(f"- Yenen: **{v.get('yenen_dep', 0):.2f}**")
        st.markdown(f"- Sıralama: **{v.get('siralama_dep', 0)}**")

def rozet(metin, tip="gray"): return f'<span class="fa-badge fa-b-{tip}">{metin}</span>'

def mac_karti(ev, dep, skor_belli, skor_ev, skor_dep, lam_ev, lam_dep, saat="", ulke="", tarih=""):
    orta = f'<div class="fa-score">{int(skor_ev)} - {int(skor_dep)}</div>' if skor_belli else '<div class="fa-vs">VS</div>'
    bayrak = ulke_bayrak_bul(ulke)
    ust_bilgi = f'<div class="fa-sub" style="margin-bottom:6px;">{bayrak} {ulke.title()} • 📅 {tarih} • 🕐 {saat}</div>' if (saat or ulke or tarih) else ""
    return f'<div class="fa-hero">{ust_bilgi}<div class="fa-teams"><div class="fa-team">{ev}</div>{orta}<div class="fa-team">{dep}</div></div><div class="fa-sub">Beklenen gol: {lam_ev:.2f} - {lam_dep:.2f}</div></div>'

def mac_tahmin_karti(v_g, g=None):
    try:
        ya = yeniden_analiz(v_g)
        p1, px, p2 = ya["p1"], ya["px"], ya["p2"]
        ust_25 = ya["ust_25"]; kg_var = ya["kg_var_model"]
        sec1x2, y1x2 = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
        return f'''
        <div class="fa-mk">
            <div class="fa-mk-row"><span class="fa-mk-lbl">🎯 1X2</span><span class="fa-mk-pick">{sec1x2}</span><span class="fa-mk-pct">%{y1x2:.0f}</span></div>
            <div class="fa-mk-row"><span class="fa-mk-lbl">⚽ Gol</span><span class="fa-mk-pick">{"Üst" if ust_25>=50 else "Alt"}</span><span class="fa-mk-pct">%{ust_25:.0f}</span></div>
            <div class="fa-mk-row"><span class="fa-mk-lbl">🤝 KG</span><span class="fa-mk-pick">{"Var" if kg_var>=50 else "Yok"}</span><span class="fa-mk-pct">%{kg_var:.0f}</span></div>
        </div>
        '''
    except Exception: return ""

def olasilik_bar(etiket, yuzde, esik=None, renk="#3b82f6"):
    y = max(0.0, min(100.0, yuzde))
    isaret = f'<div class="fa-tick" style="left:{esik:.0f}%"></div>' if esik is not None else ""
    if esik is not None: renk = "#22c55e" if yuzde >= esik else "#475569"
    return f'<div class="fa-row"><div class="fa-row-top"><span class="fa-lbl">{etiket}</span><span class="fa-val">%{yuzde:.1f}</span></div><div class="fa-bar"><div class="fa-fill" style="width:{y:.1f}%;background:{renk}"></div>{isaret}</div></div>'

def olasilik_paneli(a):
    return f'<div class="fa-card"><div class="fa-ttl">Maç Sonucu</div>' + olasilik_bar("Ev (1)", a["p1"], esik_1x2_al("1")) + olasilik_bar("X", a["px"], esik_1x2_al("X")) + olasilik_bar("Dep (2)", a["p2"], esik_1x2_al("2")) + '<div class="fa-ttl" style="margin-top:10px">Piyasalar</div>' + olasilik_bar("Üst 2.5", a["ust_25"], esik_al("ust")) + olasilik_bar("KG Var", a["kg_var_model"], esik_al("kg_var")) + '</div>'

def oneri_karti(baslik, secim, yuzde, esik, poz, alt_satir):
    sinif, pct_sinif, durum = ("fa-card fa-pos", "fa-pct", rozet("Uygun", "green")) if poz else ("fa-card fa-neg", "fa-pct fa-off", rozet("Eşik altı", "gray"))
    return f'<div class="{sinif}"><div class="fa-ttl">{baslik}</div><div class="fa-pickrow"><div><div class="fa-pick">{secim}</div>{durum}</div><div class="{pct_sinif}">%{yuzde:.1f}</div></div>{olasilik_bar("", yuzde, esik)}<div class="fa-mut">{alt_satir}</div></div>'

def istat_karti(baslik, ist, esik_metni):
    t, y, yl = ist["tam"], ist["yakin"], ist["yanlis"]
    top = t + y + yl
    isabet = (t + y) / top * 100 if top > 0 else 0
    return f'<div class="fa-card"><div class="fa-ttl">{baslik}</div><div class="fa-big fa-g">%{isabet:.0f}</div><div class="fa-mut">✅ {t+y} doğru • ❌ {yl} yanlış • {top} bahis</div><div class="fa-mut">{esik_metni}</div></div>'

def backtest_karti(baslik, dogru, yanlis):
    top = dogru + yanlis
    yuzde = dogru / top * 100 if top > 0 else 0
    alt_s, ust_s = wilson_aralik(dogru, top)
    return f'<div class="fa-card"><div class="fa-ttl">{baslik}</div><div class="fa-pickrow"><div class="fa-big fa-g">%{yuzde:.1f}</div><div style="text-align:right"><div class="fa-val">✅ {dogru} &nbsp; ❌ {yanlis}</div><div class="fa-mut">{top} bahis</div></div></div><div class="fa-ci"><div class="fa-ci-fill" style="left:{alt_s:.1f}%;width:{max(ust_s - alt_s, 0.5):.1f}%"></div><div class="fa-ci-dot" style="left:{yuzde:.1f}%;background:#22c55e"></div></div><div class="fa-mut">%95 Güven: %{alt_s:.0f} – %{ust_s:.0f}</div></div>'

def mac_sonuc_ikon(g):
    try:
        d = sonuc_hesapla({"veri": g["veri"], "analiz": yeniden_analiz(g["veri"])})
        if not d: return "⚫"
        verilen = [x["tuttu"] for x in [d["oneri_1x2"], d["oneri_gol"], d["oneri_kg"]] if x["tuttu"] is not None]
        if not verilen: return "⚫"
        return "✅" if all(verilen) else ("❌" if not any(verilen) else "🟡")
    except Exception: return "⚫"

def nav_bar():
    secenekler = [("🏠", "giris"), ("📊 Geçmiş", "gecmis"), ("🔮 Gelecek", "gelecek")]
    if admin_mi(): secenekler.extend([("🔬 Test", "backtest"), ("⚙️ Ayar", "ayarlar")])
    try: kutu = st.container(key="fa_nav")
    except TypeError: kutu = st.container()
    with kutu:
        cols = st.columns(len(secenekler))
        for kol, (etiket, hedef) in zip(cols, secenekler):
            with kol:
                if st.button(etiket, key=f"nav_{hedef}", use_container_width=True, type="primary" if st.session_state.sayfa == hedef else "secondary"):
                    st.session_state.sayfa = hedef
                    st.rerun()

def ust_bar():
    c1, c2 = st.columns([4, 1])
    with c1:
        st.markdown(f'<div style="padding:6px 0; font-size:0.8rem; color:{"#22c55e" if admin_mi() else "#8fa0bd"}; font-weight:700;">{"👑 Admin Modu" if admin_mi() else "👤 Misafir Modu"}</div>', unsafe_allow_html=True)
    with c2:
        if admin_mi():
            if st.button("🚪 Çıkış", use_container_width=True):
                st.session_state.rol = "misafir"
                st.session_state.admin_login_acik = False
                st.session_state.sayfa = "giris"
                st.rerun()
        else:
            if st.button("🔐 Giriş", use_container_width=True, type="primary"):
                st.session_state.admin_login_acik = True
                st.rerun()

if st.session_state.admin_login_acik and not admin_mi():
    st.markdown("""<div class="login-hero"><div class="login-logo">👑</div><h1 class="login-title">Admin Girişi</h1></div>""", unsafe_allow_html=True)
    with st.form("admin_giris_form"):
        sifre = st.text_input("🔐 Admin Şifresi", type="password")
        c1, c2 = st.columns(2)
        with c1: giris_btn = st.form_submit_button("✅ Giriş Yap", type="primary", use_container_width=True)
        with c2: iptal_btn = st.form_submit_button("⬅ İptal", use_container_width=True)
        if giris_btn:
            if sifre == ADMIN_SIFRE:
                st.session_state.rol = "admin"
                st.session_state.admin_login_acik = False
                st.rerun()
            else: st.error("❌ Yanlış şifre!")
        if iptal_btn:
            st.session_state.admin_login_acik = False
            st.rerun()
    st.stop()

ust_bar()
nav_bar()

if st.session_state.sayfa == "giris":
    if admin_mi():
        st.markdown("<h1>⚽ Futbol Analiz Pro</h1>", unsafe_allow_html=True)
        yapistir_metni = st.text_area("Metin Yapıştır", height=200, placeholder="Sportytrader maç verilerini buraya yapıştır...")
        if st.button("🚀 ANALİZ ET", type="primary", use_container_width=True):
            if yapistir_metni.strip():
                cikan, okunamayanlar = metinden_veri_cikar(yapistir_metni)
                st.session_state.form_verileri.update(cikan)
                st.session_state.sayfa = "sonuc"
                st.rerun()
    else:
        st.markdown('<div class="mh-hero"><div class="mh-hero-icon">⚽</div><div class="mh-hero-title">Futbol Analiz Pro</div><div class="mh-hero-sub">Akıllı Maç Analizi</div></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📊 Geçmiş Maçlar", use_container_width=True, type="primary"):
                st.session_state.sayfa = "gecmis"; st.rerun()
        with c2:
            if st.button("🔮 Gelecek Maçlar", use_container_width=True, type="primary"):
                st.session_state.sayfa = "gelecek"; st.rerun()

elif st.session_state.sayfa == "gecmis":
    st.markdown("<h1>📊 Geçmiş Maçlar</h1>", unsafe_allow_html=True)
    gecmis = st.session_state.gecmis_analizler
    if not gecmis:
        st.info("ℹ️ Henüz geçmiş maç yok.")
    else:
        for i, g in enumerate(reversed(gecmis)):
            v = g["veri"]
            st.markdown(f"### {mac_sonuc_ikon(g)}")
            st.markdown(mac_karti(v.get('takim_ev','Ev'), v.get('takim_dep','Dep'), True, v.get('skor_ev',0), v.get('skor_dep',0), 0, 0, v.get('saat',''), v.get('ulke',''), v.get('tarih','')), unsafe_allow_html=True)
            st.markdown(mac_tahmin_karti(v, g), unsafe_allow_html=True)
            st.divider()

    # 📥 VERİ İNDİRME VE YÜKLEME BÖLÜMÜ (Burada açıkça yer alıyor)
    if admin_mi():
        st.markdown("### 💾 Veri Yedekleme ve Yönetimi")
        c_ind, c_yuk = st.columns(2)
        with c_ind:
            st.download_button("📥 Geçmişi İndir (JSON)", data=json.dumps(gecmis, ensure_ascii=False, indent=2), file_name="gecmis.json", mime="application/json", use_container_width=True)
        with c_yuk:
            yuklenen = st.file_uploader("📤 Geçmiş Yükle", type=["json"], key="yuk_gecmis_main")
            if yuklenen is not None:
                try:
                    veri = json.loads(yuklenen.read().decode("utf-8"))
                    if isinstance(veri, list):
                        st.session_state.gecmis_analizler = veri
                        gecmis_kaydet(veri)
                        st.success("✅ Geçmiş yüklendi!")
                        st.rerun()
                except Exception as e: st.error(f"Hata: {e}")
        if st.button("🗑️ Tüm Geçmişi Temizle", type="primary", use_container_width=True):
            st.session_state.gecmis_analizler = []
            if os.path.exists(GECMIS_DOSYA): os.remove(GECMIS_DOSYA)
            st.rerun()

elif st.session_state.sayfa == "gelecek":
    st.markdown("<h1>🔮 Gelecek Maçlar</h1>", unsafe_allow_html=True)
    gelecek = st.session_state.gelecek_analizler
    if not gelecek:
        st.info("ℹ️ Gelecek maç yok.")
    else:
        for g in gelecek:
            v = g["veri"]
            st.markdown(mac_karti(v.get('takim_ev','Ev'), v.get('takim_dep','Dep'), False, 0, 0, 1.5, 1.2, v.get('saat',''), v.get('ulke',''), v.get('tarih','')), unsafe_allow_html=True)
            st.markdown(mac_tahmin_karti(v, g), unsafe_allow_html=True)
            st.divider()
    
    if admin_mi():
        st.markdown("### 💾 Gelecek Verilerini Yedekle")
        st.download_button("📥 Geleceği İndir (JSON)", data=json.dumps(gelecek, ensure_ascii=False, indent=2), file_name="gelecek.json", mime="application/json", use_container_width=True)

elif st.session_state.sayfa == "sonuc":
    v = st.session_state.form_verileri
    a = analiz_hesapla(v)
    st.markdown(mac_karti(v.get('takim_ev',''), v.get('takim_dep',''), v.get('skor_belli',False), v.get('skor_ev',0), v.get('skor_dep',0), a["lam_ev"], a["lam_dep"], v.get('saat',''), v.get('ulke',''), v.get('tarih','')), unsafe_allow_html=True)
    st.markdown(olasilik_paneli(a), unsafe_allow_html=True)
    if st.button("⬅️ Geri Dön", type="primary", use_container_width=True):
        st.session_state.sayfa = "giris"
        st.rerun()

elif st.session_state.sayfa == "ayarlar" and admin_mi():
    st.markdown("<h1>⚙️ Eşik Ayarları</h1>", unsafe_allow_html=True)
    mevcut = st.session_state.esikler
    yeni_ust = st.slider("Üst 2.5 eşiği (%)", 0, 100, int(mevcut.get("ust", 65.0)))
    yeni_kg_var = st.slider("KG Var eşiği (%)", 0, 100, int(mevcut.get("kg_var", 57.0)))
    if st.button("💾 Kaydet", type="primary", use_container_width=True):
        st.session_state.esikler["ust"] = float(yeni_ust)
        st.session_state.esikler["kg_var"] = float(yeni_kg_var)
        ayarlar_kaydet(st.session_state.esikler)
        st.success("✅ Ayarlar kaydedildi!")

elif st.session_state.sayfa == "backtest" and admin_mi():
    st.markdown("<h1>🔬 Backtest</h1>", unsafe_allow_html=True)
    st.info("Geçmiş maçlar üzerinden test yapabilirsiniz.")
