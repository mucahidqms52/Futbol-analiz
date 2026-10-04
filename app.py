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
import hashlib
import secrets as _secrets
import psycopg2
from psycopg2.extras import Json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess, sys


YASAL_METIN = """
# ⚖️ KULLANIM ŞARTLARI VE SORUMLULUK REDDİ

**Yürürlük Tarihi:** Hizmete kayıt olduğunuz tarih itibariyle geçerlidir.

## 1. TARAFLAR VE KAPSAM
Bu Kullanım Şartları, **"Futbol Analiz Pro"** ile bu hizmete kayıt olan kullanıcı arasında akdedilmiştir.

## 2. HİZMETİN TANIMI
Uygulama, futbol maçlarına ilişkin olarak **geçmiş istatistiklere dayalı matematiksel ve istatistiksel analizler** üreterek kullanıcıya **bilgilendirme amaçlı tahminler** sunar.

## 3. YAŞ SINIRI
18 yaşından büyük olmanız, fiil ehliyetine sahip olmanız ve yasal olarak bahis oynamanın yasak olmadığı bir ülkede bulunmanız gerekmektedir.

## 4. SORUMLULUK REDDİ
Uygulama **"AS IS"** sunulmaktadır. Tahminler **%100 doğru değildir**, garanti içermez.

## 5. YASADIŞI BAHİS UYARISI
Türkiye'de yasadışı bahis **suçtur** (7258 sayılı Kanun).

## 6. ÖDEME VE İADE
Ödemeler **havale / EFT** ile yapılır. Aktivasyon sonrası **iade yapılmaz**.

## 7. KVKK
Veriler yalnızca hizmet için kullanılır, 3. taraflarla paylaşılmaz.

## 8. İLETİŞİM
Bildirim bölümünden iletişime geçebilirsiniz.

**YEDAM: 115**
"""


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
    h1, h2, h3, h4, .fa-score, .fa-big, .mh-stat-num, .login-title, .mh-hero-title { font-family: 'Rajdhani', 'Inter', sans-serif !important; letter-spacing: 0.4px; }
    .block-container { padding-top: 0.8rem !important; padding-bottom: 0.8rem !important; padding-left: 0.8rem !important; padding-right: 0.8rem !important; max-width: 100% !important; }
    :root { --bg-0: #060a14; --bg-1: #0b1220; --card: #131c2e; --border: #1f2c44; --text: #eaf1fb; --muted: #7f92b3; --green: #22c55e; --blue: #3b82f6; --yellow: #f59e0b; --red: #ef4444; }
    .stApp { background: radial-gradient(1200px 600px at 10% -10%, rgba(34,197,94,0.08), transparent 60%), radial-gradient(900px 500px at 100% 0%, rgba(59,130,246,0.07), transparent 60%), linear-gradient(180deg, #060a14 0%, #0b1220 100%) !important; }
    header[data-testid="stHeader"] { background: transparent !important; }
    .stApp, .stApp p, .stApp span, .stApp label, .stApp li, .stApp div[data-testid="stMarkdownContainer"] { color: var(--text) !important; }
    .stApp div[data-testid="stCaptionContainer"], .stApp small { color: var(--muted) !important; }
    hr { border-color: var(--border) !important; margin: 0.5rem 0 !important; }
    h1 { font-size: 1.35rem !important; font-weight: 800 !important; margin: 0.4rem 0 !important; text-align: center; background: linear-gradient(135deg, #eaf1fb 0%, #94a3b8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 0.4px; }
    h2 { font-size: 1rem !important; font-weight: 700 !important; margin: 0.4rem 0 !important; }
    h3 { font-size: 0.88rem !important; font-weight: 700 !important; margin: 0.25rem 0 !important; border-left: 3px solid var(--green); padding-left: 0.5rem; }
    p { font-size: 0.8rem !important; margin: 0.2rem 0 !important; line-height: 1.45; }
    div[data-testid="stNumberInput"] label p { font-size: 0.72rem !important; margin: 0 !important; font-weight: 600; }
    div[data-testid="stNumberInput"] input { font-size: 0.85rem !important; padding: 0.35rem 0.5rem !important; height: 2rem !important; }
    div[data-testid="stNumberInput"] button { height: 2rem !important; }
    div[data-testid="stNumberInput"] > div { margin-bottom: 0.25rem !important; }
    .stTextArea textarea, .stTextInput input, div[data-testid="stNumberInput"] input { background: var(--card) !important; color: var(--text) !important; border: 1.5px solid var(--border) !important; border-radius: 10px !important; transition: all 0.2s ease !important; }
    .stTextArea textarea:focus, .stTextInput input:focus, div[data-testid="stNumberInput"] input:focus { border-color: var(--green) !important; box-shadow: 0 0 0 4px rgba(34,197,94,0.12) !important; }
    div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="base-input"] { background: var(--card) !important; border-radius: 10px !important; }
    .stButton button, div[data-testid="stDownloadButton"] button, div[data-testid="stFormSubmitButton"] button { background: linear-gradient(145deg, #18233a, #131c2e) !important; border: 1.5px solid var(--border) !important; border-radius: 10px !important; font-weight: 700 !important; font-size: 0.8rem !important; color: var(--text) !important; transition: all 0.2s ease !important; box-shadow: 0 2px 8px rgba(0,0,0,0.25) !important; padding: 0.35rem 0.5rem !important; }
    .stButton button p, div[data-testid="stDownloadButton"] button p, div[data-testid="stFormSubmitButton"] button p { color: var(--text) !important; font-weight: 700 !important; font-size: 0.8rem !important; }
    .stButton button:hover, div[data-testid="stDownloadButton"] button:hover { border-color: var(--green) !important; transform: translateY(-1px); box-shadow: 0 6px 20px rgba(34,197,94,0.2) !important; }
    .stButton button[kind="primary"], button[data-testid="stBaseButton-primary"], button[data-testid="stBaseButton-primaryFormSubmit"] { background: linear-gradient(135deg, #16a34a, #22c55e) !important; border: none !important; box-shadow: 0 6px 20px rgba(34,197,94,0.35) !important; color: #04130a !important; }
    .stButton button[kind="primary"] p, button[data-testid="stBaseButton-primary"] p, button[data-testid="stBaseButton-primaryFormSubmit"] p { color: #04130a !important; }
    div[data-testid="stExpander"] { background: linear-gradient(145deg, var(--card), #0f1829) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; overflow: hidden; margin-bottom: 8px !important; }
    div[data-testid="stExpander"] details > summary { display: flex !important; align-items: center !important; gap: 6px !important; padding: 0.5rem 0.8rem !important; font-size: 0.82rem !important; font-weight: 700 !important; line-height: 1.3 !important; min-height: 38px !important; overflow: hidden !important; cursor: pointer !important; list-style: none !important; }
    div[data-testid="stExpander"] details > summary::-webkit-details-marker { display: none !important; }
    div[data-testid="stExpander"] details > summary::marker { display: none !important; content: "" !important; }
    div[data-testid="stExpander"] details > summary:hover { background: rgba(34,197,94,0.05) !important; }
    div[data-testid="stExpander"] details > summary p, div[data-testid="stExpander"] details > summary div[data-testid="stMarkdownContainer"], div[data-testid="stExpander"] details > summary div[data-testid="stMarkdownContainer"] p { font-size: 0.82rem !important; font-weight: 700 !important; margin: 0 !important; line-height: 1.3 !important; color: #eaf1fb !important; white-space: normal !important; display: inline-block !important; }
    div[data-testid="stExpander"] details > summary > div { display: flex !important; align-items: center !important; gap: 6px !important; flex-wrap: nowrap !important; }
    div[data-testid="stExpander"] details > summary svg { flex-shrink: 0 !important; width: 14px !important; height: 14px !important; min-width: 14px !important; transition: transform 0.2s ease !important; }
    div[data-testid="stExpander"] details > div[role="region"] { padding: 0.4rem 0.8rem 0.8rem 0.8rem !important; font-size: 0.82rem !important; }
    div[data-testid="stAlert"] { padding: 0.4rem 0.7rem !important; font-size: 0.8rem !important; border-radius: 10px !important; }
    div[data-testid="stFileUploader"] section { background: var(--card) !important; border: 1.5px dashed var(--border) !important; border-radius: 12px !important; }
    .st-key-fa_nav div[data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: 0.3rem !important; }
    .st-key-fa_nav div[data-testid="stColumn"], .st-key-fa_nav div[data-testid="column"] { min-width: 0 !important; flex: 1 1 0 !important; width: auto !important; }
    .st-key-fa_nav .stButton button { padding: 0.3rem 0.25rem !important; height: 2.1rem !important; background: rgba(19,28,46,0.6) !important; backdrop-filter: blur(8px); border: 1px solid var(--border) !important; }
    .st-key-fa_nav .stButton button p { font-size: 0.72rem !important; white-space: nowrap; font-weight: 700 !important; }
    .st-key-fa_nav .stButton button[kind="primary"] { background: linear-gradient(135deg, #16a34a, #22c55e) !important; box-shadow: 0 4px 16px rgba(34,197,94,0.4) !important; }
    .stApp .fa-hero { position: relative; overflow: hidden; background: linear-gradient(135deg, #14243e 0%, #0d1729 100%); border: 1px solid var(--border); border-radius: 16px; padding: 14px 12px; margin: 6px 0 10px 0; text-align: center; box-shadow: 0 10px 32px rgba(0,0,0,0.4), 0 0 0 1px rgba(34,197,94,0.05) inset; }
    .stApp .fa-hero::before { content: ""; position: absolute; inset: 0; background: radial-gradient(circle at 50% 0%, rgba(34,197,94,0.15), transparent 60%); pointer-events: none; }
    .stApp .fa-teams { display: flex; align-items: center; justify-content: space-between; gap: 6px; position: relative; z-index: 1; }
    .stApp .fa-team { flex: 1; font-weight: 800; font-size: 0.9rem; line-height: 1.2; word-break: break-word; letter-spacing: 0.2px; }
    .stApp .fa-score { font-size: 1.6rem; font-weight: 900; color: var(--green) !important; min-width: 80px; letter-spacing: 0.5px; text-shadow: 0 0 20px rgba(34,197,94,0.5); }
    .stApp .fa-vs { font-size: 0.9rem; font-weight: 800; color: var(--muted) !important; min-width: 50px; letter-spacing: 1px; }
    .stApp .fa-sub { font-size: 0.68rem; color: var(--muted) !important; margin-top: 6px; letter-spacing: 0.2px; }
    .stApp .fa-card { background: linear-gradient(145deg, var(--card), #0f1829); border: 1px solid var(--border); border-radius: 14px; padding: 10px 12px; margin-bottom: 10px; box-shadow: 0 6px 20px rgba(0,0,0,0.25); transition: all 0.25s ease; }
    .stApp .fa-card:hover { border-color: rgba(34,197,94,0.3); transform: translateY(-1px); }
    .stApp .fa-card.fa-pos { border-color: rgba(34,197,94,0.55); box-shadow: 0 8px 28px rgba(34,197,94,0.15), 0 0 0 1px rgba(34,197,94,0.15) inset; }
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
    .stApp .fa-locked { position: relative; overflow: hidden; background: linear-gradient(135deg, #14243e 0%, #0d1729 100%); border: 1px solid var(--border); border-radius: 16px; padding: 14px 12px; margin: 6px 0 10px 0; text-align: center; opacity: 0.7; }
    .stApp .fa-locked::after { content: "🔒"; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 3rem; opacity: 0.15; }
    .stApp .fa-locked-teams { display: flex; align-items: center; justify-content: space-between; gap: 6px; filter: blur(3px); }
    .stApp .fa-locked-overlay { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, rgba(34,197,94,0.08), rgba(59,130,246,0.08)); z-index: 2; }
    .stApp .fa-locked-text { background: linear-gradient(135deg, #16a34a, #22c55e); color: #04130a !important; font-weight: 900; font-size: 0.85rem; padding: 10px 20px; border-radius: 99px; box-shadow: 0 8px 24px rgba(34,197,94,0.4); letter-spacing: 0.5px; }
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
    .mh-stat::after { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #22c55e, #3b82f6); }
    .mh-stat-icon { font-size: 1.3rem; margin-bottom: 4px; }
    .mh-stat-num { font-size: 1.8rem; font-weight: 900; color: var(--green) !important; line-height: 1; letter-spacing: -0.8px; }
    .mh-stat-lbl { font-size: 0.65rem; color: var(--muted) !important; margin-top: 6px; letter-spacing: 0.7px; text-transform: uppercase; font-weight: 800; }
    .mh-info { background: linear-gradient(145deg, rgba(19,28,46,0.7), rgba(11,18,32,0.9)); border: 1px solid var(--border); border-radius: 14px; padding: 12px 14px; margin-top: 14px; font-size: 0.75rem; color: var(--muted) !important; line-height: 1.6; }
    .mh-info b { color: var(--green) !important; }
    ::-webkit-scrollbar { width: 7px; height: 7px; }
    ::-webkit-scrollbar-track { background: var(--bg-1); }
    ::-webkit-scrollbar-thumb { background: #2a3a56; border-radius: 99px; }
    section[data-testid="stSidebar"] { background: var(--bg-1) !important; border-right: 1px solid var(--border); }
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
    .stApp .fa-card, .stApp .fa-hero, .stApp .fa-mk, .mh-stat, .stApp .fa-locked { animation: fadeInUp 0.4s ease-out; }
    .stApp div[data-testid="stCheckbox"] { background: linear-gradient(145deg, rgba(19,28,46,0.6), rgba(11,18,32,0.8)); border: 1.5px solid var(--border); border-radius: 12px; padding: 10px 12px; margin: 10px 0; }
    .stApp div[data-testid="stCheckbox"] label p { font-size: 0.78rem !important; line-height: 1.5 !important; }
    .stApp .fa-bildirim { background: linear-gradient(145deg, var(--card), #0f1829); border-left: 4px solid var(--green); border-radius: 12px; padding: 12px 14px; margin-bottom: 10px; }
    .stApp .fa-bildirim.fa-bildirim-iptal { border-left-color: #ef4444; }
    .stApp .fa-bildirim.fa-bildirim-sikayet { border-left-color: #f59e0b; }
    .stApp .fa-bildirim.fa-bildirim-gorus { border-left-color: #3b82f6; }
    .stApp .fa-bildirim.fa-bildirim-diger { border-left-color: #94a3b8; }
    .stApp .fa-bildirim-ttl { font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
    .stApp .fa-bildirim-msg { font-size: 0.85rem; color: #eaf1fb !important; line-height: 1.5; margin: 6px 0; }
    .stApp .fa-bildirim-meta { font-size: 0.68rem; color: var(--muted) !important; }
    .st-key-fa_nav .stButton button { min-height: 2.9rem !important; padding: 0.55rem 0.4rem !important; }
    .st-key-fa_nav .stButton button p { font-size: 0.88rem !important; font-weight: 800 !important; }
    .stApp .fa-donut-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 16px 0 8px 0; }
    .stApp .fa-donut-kart { background: linear-gradient(145deg, rgba(19,28,46,0.85), rgba(11,18,32,0.95)); border: 1px solid #1d2940; border-radius: 16px; padding: 12px 6px 10px 6px; text-align: center; position: relative; overflow: hidden; transition: all 0.3s ease; box-shadow: 0 4px 16px rgba(0,0,0,0.25); }
    .stApp .fa-donut-kart:hover { border-color: rgba(34,197,94,0.45); transform: translateY(-3px); box-shadow: 0 10px 28px rgba(34,197,94,0.15); }
    .stApp .fa-donut-kart::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--c); }
    .stApp .fa-donut-ttl { font-size: 0.62rem; color: #8fa0bd !important; font-weight: 800; letter-spacing: 0.6px; text-transform: uppercase; margin-bottom: 8px; }
    .stApp .fa-donut-svg { width: 100%; max-width: 82px; height: auto; margin: 0 auto; display: block; }
    .stApp .fa-donut-sub { font-size: 0.62rem; color: #64748b !important; margin-top: 8px; font-weight: 700; }
    .stApp .fa-donut-sub b { color: #eaf1fb !important; }
    .stApp .mh-hero-ust { font-size: 0.7rem; color: #8fa0bd !important; letter-spacing: 2px; text-transform: uppercase; font-weight: 800; margin-bottom: 8px; opacity: 0.7; }
    .stApp .fa-uye-link { text-align: center; font-size: 0.78rem; color: #8fa0bd !important; margin-top: 8px; }
    .stApp .fa-uye-link b { color: #22c55e !important; font-weight: 800; }
    .stApp .fa-ai-kart { background: linear-gradient(145deg, rgba(19,28,46,0.92), rgba(11,18,32,0.98)); border: 1px solid rgba(59,130,246,0.35); border-radius: 16px; padding: 16px 16px 12px 16px; margin-bottom: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.35), 0 0 0 1px rgba(59,130,246,0.06) inset; animation: fadeInUp 0.4s ease-out; }
    .stApp .fa-ai-baslik { font-size: 0.78rem; font-weight: 900; letter-spacing: 1.5px; text-transform: uppercase; color: #3b82f6 !important; margin-bottom: 14px; padding-bottom: 10px; border-bottom: 1px solid rgba(59,130,246,0.3); }
    .stApp .fa-ai-bolum { margin-bottom: 14px; }
    .stApp .fa-ai-bolum:last-child { margin-bottom: 4px; }
    .stApp .fa-ai-bolum-baslik { font-size: 0.72rem; font-weight: 900; letter-spacing: 0.8px; color: #8fa0bd !important; text-transform: uppercase; margin-bottom: 6px; }
    .stApp .fa-ai-bolum-metin { font-size: 0.86rem; line-height: 1.7; color: #eaf1fb !important; text-align: justify; letter-spacing: 0.1px; }
    .stApp .fa-ai-bolum-metin b { color: #22c55e !important; font-weight: 800; }
    .stApp .fa-ai-bolum-metin .ev { color: #3b82f6 !important; font-weight: 800; }
    .stApp .fa-ai-bolum-metin .dep { color: #f59e0b !important; font-weight: 800; }
    .stApp .fa-ai-bolum-metin .vurgu { color: #22c55e !important; font-weight: 800; }
    .stApp .fa-ai-bolum-metin .uyari { color: #f59e0b !important; font-weight: 800; }
    .stApp .fa-ai-bolum-metin .kotu { color: #ef4444 !important; font-weight: 800; }
    .stApp .fa-ai-karar { background: rgba(34,197,94,0.08); border-left: 3px solid #22c55e; border-radius: 8px; padding: 10px 12px; margin-top: 12px; font-size: 0.84rem; line-height: 1.55; color: #eaf1fb !important; }
    .stApp .fa-ai-karar b { color: #22c55e !important; font-weight: 900; }
</style>
""", unsafe_allow_html=True)


# ==========================================
# POSTGRESQL VERİ KATMANI
# ==========================================
ADMIN_KULLANICI_ADI = "admin52"


def _admin_sifre_al():
    try:
        if "ADMIN_SIFRE" in st.secrets:
            return st.secrets["ADMIN_SIFRE"]
    except Exception:
        pass
    return os.environ.get("ADMIN_SIFRE", "Mg153759")

ADMIN_SIFRE = _admin_sifre_al()


def _db_baglanti():
    url = os.environ.get("DATABASE_URL", "")
    if not url:
        raise RuntimeError("DATABASE_URL ortam değişkeni tanımlı değil.")
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return psycopg2.connect(url, sslmode="require")


@st.cache_resource(show_spinner="Veritabanı hazırlanıyor...")
def _init_db():
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS kullanicilar (kullanici_adi TEXT PRIMARY KEY, veri JSONB NOT NULL)")
            cur.execute("CREATE TABLE IF NOT EXISTS bekleyen_odemeler (kullanici_adi TEXT PRIMARY KEY, veri JSONB NOT NULL)")
            cur.execute("CREATE TABLE IF NOT EXISTS bildirimler (id BIGINT PRIMARY KEY, veri JSONB NOT NULL)")
            cur.execute("CREATE TABLE IF NOT EXISTS gecmis (id SERIAL PRIMARY KEY, veri JSONB NOT NULL)")
            cur.execute("CREATE TABLE IF NOT EXISTS gelecek (id SERIAL PRIMARY KEY, veri JSONB NOT NULL)")
            cur.execute("CREATE TABLE IF NOT EXISTS ayarlar (id INT PRIMARY KEY DEFAULT 1, veri JSONB NOT NULL, CONSTRAINT ayarlar_tek_satir CHECK (id = 1))")
        conn.commit()
    finally:
        conn.close()
    return True


try:
    _init_db()
except Exception as _db_hata:
    st.error(f"❌ Veritabanı bağlantı hatası: {_db_hata}")
    st.stop()


def kullanicilar_yukle():
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT kullanici_adi, veri FROM kullanicilar")
            return {row[0]: row[1] for row in cur.fetchall()}
    finally:
        conn.close()


def kullanicilar_kaydet(v):
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM kullanicilar")
            for k, veri in v.items():
                cur.execute("INSERT INTO kullanicilar (kullanici_adi, veri) VALUES (%s, %s)", (k, Json(veri)))
        conn.commit()
    finally:
        conn.close()


def bekleyen_yukle():
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT kullanici_adi, veri FROM bekleyen_odemeler")
            return {row[0]: row[1] for row in cur.fetchall()}
    finally:
        conn.close()


def bekleyen_kaydet(v):
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM bekleyen_odemeler")
            for k, veri in v.items():
                cur.execute("INSERT INTO bekleyen_odemeler (kullanici_adi, veri) VALUES (%s, %s)", (k, Json(veri)))
        conn.commit()
    finally:
        conn.close()


def bildirimler_yukle():
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, veri FROM bildirimler ORDER BY id")
            return [row[1] for row in cur.fetchall()]
    finally:
        conn.close()


def bildirimler_kaydet(v):
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM bildirimler")
            for veri in v:
                bid = veri.get("id") or int(time.time() * 1000)
                cur.execute("INSERT INTO bildirimler (id, veri) VALUES (%s, %s)", (bid, Json(veri)))
        conn.commit()
    finally:
        conn.close()


def otomatik_log_yukle():
    return {}


def otomatik_log_kaydet(v):
    pass


def gecmis_yukle():
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT veri FROM gecmis ORDER BY id")
            return [row[0] for row in cur.fetchall()]
    finally:
        conn.close()


def gecmis_kaydet(v):
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM gecmis")
            for veri in v:
                cur.execute("INSERT INTO gecmis (veri) VALUES (%s)", (Json(veri),))
        conn.commit()
    finally:
        conn.close()


def gelecek_yukle():
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT veri FROM gelecek ORDER BY id")
            return [row[0] for row in cur.fetchall()]
    finally:
        conn.close()


def gelecek_kaydet(v):
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM gelecek")
            for veri in v:
                cur.execute("INSERT INTO gelecek (veri) VALUES (%s)", (Json(veri),))
        conn.commit()
    finally:
        conn.close()


def ayarlar_yukle():
    v = {"ust": 65.0, "alt": 55.0, "kg_var": 57.0, "kg_yok": 72.0, "esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0, "iban": "TR00 0000 0000 0000 0000 0000 00", "hesap_sahibi": "ADINIZ SOYADINIZ", "fiyat_haftalik": 49.0, "fiyat_aylik": 149.0, "fiyat_yillik": 999.0, "ucretsiz_kotasi": 3}
    try:
        conn = _db_baglanti()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT veri FROM ayarlar WHERE id = 1")
                row = cur.fetchone()
                if row and row[0]:
                    v.update(row[0])
        finally:
            conn.close()
    except Exception:
        pass
    return v


def ayarlar_kaydet(v):
    conn = _db_baglanti()
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO ayarlar (id, veri) VALUES (1, %s) ON CONFLICT (id) DO UPDATE SET veri = EXCLUDED.veri", (Json(v),))
        conn.commit()
    finally:
        conn.close()


def sifre_hashle(sifre, salt=None):
    if salt is None:
        salt = _secrets.token_hex(16)
    h = hashlib.sha256((salt + sifre).encode("utf-8")).hexdigest()
    return salt, h


def sifre_dogrula(sifre, salt, kayitli_hash):
    _, h = sifre_hashle(sifre, salt)
    return h == kayitli_hash


def kullanici_ekle(kullanici_adi, sifre):
    kullanicilar = kullanicilar_yukle()
    if kullanici_adi in kullanicilar:
        return False, "Bu kullanıcı adı zaten alınmış."
    salt, s_hash = sifre_hashle(sifre)
    kullanicilar[kullanici_adi] = {
        "salt": salt, "sifre_hash": s_hash,
        "kayit_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "abonelik_bitis": None, "son_odeme": None, "son_odeme_gun": 0,
        "yasal_kabul_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    kullanicilar_kaydet(kullanicilar)
    return True, "Kayıt başarılı."


def kullanici_dogrula(kullanici_adi, sifre):
    kullanicilar = kullanicilar_yukle()
    k = kullanicilar.get(kullanici_adi)
    if not k: return False
    return sifre_dogrula(sifre, k["salt"], k["sifre_hash"])


def abonelik_aktif_mi(kullanici_adi):
    kullanicilar = kullanicilar_yukle()
    k = kullanicilar.get(kullanici_adi)
    if not k: return False
    bitis_str = k.get("abonelik_bitis")
    if not bitis_str: return False
    try:
        return datetime.strptime(bitis_str, "%Y-%m-%d") >= datetime.now()
    except Exception:
        return False


def abonelik_aktif_et(kullanici_adi, gun_sayisi):
    kullanicilar = kullanicilar_yukle()
    if kullanici_adi not in kullanicilar:
        return False, "Kullanıcı bulunamadı."
    k = kullanicilar[kullanici_adi]
    mevcut_bitis = None
    if k.get("abonelik_bitis"):
        try: mevcut_bitis = datetime.strptime(k["abonelik_bitis"], "%Y-%m-%d")
        except Exception: mevcut_bitis = None
    bugun = datetime.now()
    baslangic = mevcut_bitis if (mevcut_bitis and mevcut_bitis > bugun) else bugun
    yeni_bitis = baslangic + timedelta(days=int(gun_sayisi))
    k["abonelik_bitis"] = yeni_bitis.strftime("%Y-%m-%d")
    k["son_odeme"] = bugun.strftime("%Y-%m-%d %H:%M")
    k["son_odeme_gun"] = int(gun_sayisi)
    kullanicilar_kaydet(kullanicilar)
    return True, yeni_bitis.strftime("%Y-%m-%d")


def abonelik_iptal_et(kullanici_adi):
    kullanicilar = kullanicilar_yukle()
    if kullanici_adi not in kullanicilar: return False
    kullanicilar[kullanici_adi]["abonelik_bitis"] = None
    kullanicilar_kaydet(kullanicilar)
    return True


def kullanici_sil(kullanici_adi):
    kullanicilar = kullanicilar_yukle()
    if kullanici_adi in kullanicilar:
        del kullanicilar[kullanici_adi]
        kullanicilar_kaydet(kullanicilar)
        bd = bildirimler_yukle()
        bd = [b for b in bd if b.get("kullanici") != kullanici_adi]
        bildirimler_kaydet(bd)
        return True
    return False


BILDIRIM_TIPLERI = {
    "iptal": {"ikon": "🚫", "isim": "Abonelik İptal Talebi", "sinif": "fa-bildirim-iptal"},
    "sikayet": {"ikon": "⚠️", "isim": "Şikayet", "sinif": "fa-bildirim-sikayet"},
    "gorus": {"ikon": "💬", "isim": "Görüş / Öneri", "sinif": "fa-bildirim-gorus"},
    "diger": {"ikon": "📩", "isim": "Diğer", "sinif": "fa-bildirim-diger"},
}


def bildirim_ekle(kullanici_adi, tip, konu, mesaj):
    bd = bildirimler_yukle()
    yeni = {"id": int(time.time() * 1000), "kullanici": kullanici_adi, "tip": tip, "konu": konu, "mesaj": mesaj, "tarih": datetime.now().strftime("%Y-%m-%d %H:%M"), "durum": "okunmadi", "cevap": ""}
    bd.append(yeni)
    bildirimler_kaydet(bd)
    return yeni["id"]


def bildirim_guncelle(bid, **kwargs):
    bd = bildirimler_yukle()
    for b in bd:
        if b.get("id") == bid:
            b.update(kwargs)
            break
    bildirimler_kaydet(bd)


def bildirim_sil(bid):
    bd = bildirimler_yukle()
    bd = [b for b in bd if b.get("id") != bid]
    bildirimler_kaydet(bd)


def kullanici_bildirimleri(kullanici_adi):
    bd = bildirimler_yukle()
    return [b for b in bd if b.get("kullanici") == kullanici_adi]


def saat_2_saat_ileri(s):
    if not s: return s
    m = re.match(r'^(\d{1,2}):(\d{2})$', str(s).strip())
    if not m: return s
    try: return f"{(int(m.group(1)) + 2) % 24:02d}:{int(m.group(2)):02d}"
    except Exception: return s


def saat_sirala_anahtari(g):
    try:
        v = g.get("veri", {}) if isinstance(g, dict) else {}
        tarih = str(v.get("tarih", "")).strip(); saat = str(v.get("saat", "")).strip()
        gun, ay, yil = 99, 99, 9999
        if tarih:
            m = re.match(r'^(\d{1,2})\.(\d{1,2})\.(\d{2,4})$', tarih)
            if m:
                gun = int(m.group(1)); ay = int(m.group(2)); yr = m.group(3); yil = int(yr) if len(yr) == 4 else 2000 + int(yr)
        sh, sm = 99, 99
        if saat:
            m2 = re.match(r'^(\d{1,2}):(\d{2})$', saat)
            if m2: sh = int(m2.group(1)); sm = int(m2.group(2))
        return (yil, ay, gun, sh, sm)
    except Exception: return (9999, 99, 99, 99, 99)


ESIK_YUKSEK = 65.0; ESIK_ORTA = 55.0; ESIK_BELIRSIZ = 50.0; MONTE_CARLO_N = 10000


VARSAYILAN_VERI = {k: v for k, v in {
    "ppg_ev": 0.0, "mpg_dep": 0.0, "form_str_ev": "", "form_str_dep": "",
    "siralama_ev": 0, "siralama_dep": 0, "puan_ev": 0, "puan_dep": 0,
    "xg_ev": 0.0, "xg_dep": 0.0, "atilan_ev": 0.0, "atilan_dep": 0.0,
    "yenen_ev": 0.0, "yenen_dep": 0.0, "clean_sheets_ev": 0.0, "clean_sheets_dep": 0.0,
    "team_scored_ev": 0.0, "team_scored_dep": 0.0, "team_scored_2_ev": 0.0, "team_scored_2_dep": 0.0,
    "scored_both_halves_ev": 0.0, "scored_both_halves_dep": 0.0,
    "goal_both_halves_ev": 0.0, "goal_both_halves_dep": 0.0,
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
    "lht_lft_ev": 0.0, "lht_lft_dep": 0.0,
    "galibiyet_ev": 30.0, "galibiyet_dep": 30.0, "beraberlik_ev": 30.0, "beraberlik_dep": 30.0,
    "maglubiyet_ev": 30.0, "maglubiyet_dep": 30.0,
    "win_1h_ev": 0.0, "win_1h_dep": 0.0, "draw_ht_ev": 0.0, "draw_ht_dep": 0.0,
    "lose_1h_ev": 0.0, "lose_1h_dep": 0.0, "win_btts_ev": 0.0, "win_btts_dep": 0.0,
    "draw_btts_ev": 0.0, "draw_btts_dep": 0.0, "lose_btts_ev": 0.0, "lose_btts_dep": 0.0,
    "win_over15_ev": 0.0, "win_over15_dep": 0.0, "lose_over15_ev": 0.0, "lose_over15_dep": 0.0,
    "takim_ev": "", "takim_dep": "", "skor_ev": 0, "skor_dep": 0, "skor_belli": False,
    "lig_ort_toplam": 0.0, "lig_ust25": 0.0, "lig_kg": 0.0,
    "saat": "", "tarih": "", "ulke": "", "format": "bilinmiyor", "kaynak_url": "",
    "trends_ev": [], "trends_dep": [],
}.items()}

MAX_GOL = 8; BELIRSIZLIK = 0.20; MAX_MAC_SINIRI = 200
_kilit = threading.Lock(); _ESIK_CACHE = {}


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
if "bt_market_esik" not in st.session_state: st.session_state.bt_market_esik = {"esik_1": 55.0, "esik_x": 55.0, "esik_2": 55.0, "kg_var": 70.0, "kg_yok": 70.0, "ust": 70.0, "alt": 70.0}
if "bt_sonuc" not in st.session_state: st.session_state.bt_sonuc = None
if "bt_detaylar" not in st.session_state: st.session_state.bt_detaylar = []
if "toplu_cek_ozet" not in st.session_state: st.session_state.toplu_cek_ozet = None
if "skor_ozet" not in st.session_state: st.session_state.skor_ozet = None
if "aktif_kullanici" not in st.session_state: st.session_state.aktif_kullanici = None
if "odeme_hedef_kadi" not in st.session_state: st.session_state.odeme_hedef_kadi = None
if "sil_onay_kadi" not in st.session_state: st.session_state.sil_onay_kadi = None
if "kayit_yasal_onay" not in st.session_state: st.session_state.kayit_yasal_onay = False
if "odeme_yasal_onay" not in st.session_state: st.session_state.odeme_yasal_onay = False


def admin_mi(): return st.session_state.get("rol") == "admin"
def uye_mi(): return st.session_state.get("aktif_kullanici") is not None
def uye_adi(): return st.session_state.get("aktif_kullanici", "")
def uye_premium_mu():
    if not uye_mi(): return False
    return abonelik_aktif_mi(uye_adi())


def esik_al(key):
    try:
        v = st.session_state.esikler.get(key)
        if v is not None: return v
    except Exception: pass
    return _ESIK_CACHE.get(key, 50.0)


def esik_1x2_al(secim):
    km = {"1": "esik_1", "X": "esik_x", "2": "esik_2"}; k = km.get(secim, "")
    try:
        v = st.session_state.esikler.get(k)
        if v is not None: return v
    except Exception: pass
    return _ESIK_CACHE.get(k, 55.0)


def ayar_al(key, default=None):
    try: return st.session_state.esikler.get(key, default)
    except Exception: return default


ULKE_BAYRAK = {"switzerland": "🇨🇭", "isviçre": "🇨🇭", "england": "🏴", "ingiltere": "🏴", "spain": "🇪🇸", "ispanya": "🇪🇸", "italy": "🇮🇹", "italya": "🇮🇹", "germany": "🇩🇪", "almanya": "🇩🇪", "france": "🇫🇷", "fransa": "🇫🇷", "netherlands": "🇳🇱", "hollanda": "🇳🇱", "portugal": "🇵🇹", "portekiz": "🇵🇹", "belgium": "🇧🇪", "belçika": "🇧🇪", "turkey": "🇹🇷", "türkiye": "🇹🇷", "turkiye": "🇹🇷", "argentina": "🇦🇷", "arjantin": "🇦🇷", "brazil": "🇧🇷", "brezilya": "🇧🇷", "mexico": "🇲🇽", "meksika": "🇲🇽", "usa": "🇺🇸", "abd": "🇺🇸", "japan": "🇯🇵", "japonya": "🇯🇵", "china": "🇨🇳", "çin": "🇨🇳", "russia": "🇷🇺", "rusya": "🇷🇺", "poland": "🇵🇱", "polonya": "🇵🇱", "greece": "🇬🇷", "yunanistan": "🇬🇷", "romania": "🇷🇴", "romanya": "🇷🇴", "serbia": "🇷🇸", "sırbistan": "🇷🇸", "croatia": "🇭🇷", "hırvatistan": "🇭🇷", "iran": "🇮🇷"}


def ulke_bayrak_bul(ulke_adi):
    if not ulke_adi: return "🌍"
    u = ulke_adi.lower().strip()
    for a in sorted(ULKE_BAYRAK.keys(), key=len, reverse=True):
        if a in u: return ULKE_BAYRAK[a]
    return "🌍"


def _ulke_bul(metin):
    m = re.search(r'Standings\s+([^\n]+)', metin)
    if not m: return ""
    s = m.group(1).strip()
    if not s: return ""
    alt = s.lower()
    for a in sorted(ULKE_BAYRAK.keys(), key=len, reverse=True):
        if a in alt: return a
    p = s.split(); return " ".join(p[:2]) if len(p) >= 2 else (p[0] if p else "")


def clamp(x, lo, hi): return max(lo, min(hi, x))


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


def poisson_matris(lam_ev, lam_dep, mg=MAX_GOL):
    return [[poisson_pmf(i, lam_ev) * poisson_pmf(j, lam_dep) for j in range(mg)] for i in range(mg)]


def hesapla_lambda(v):
    ae = v.get("atilan_ev", 0.0); ye = v.get("yenen_ev", 0.0)
    ad = v.get("atilan_dep", 0.0); yd = v.get("yenen_dep", 0.0)
    xge = v.get("xg_ev", 0.0); xgd = v.get("xg_dep", 0.0)
    he = (xge * 0.60 + ae * 0.40) if xge > 0 else (ae if ae > 0 else 1.2)
    hd = (xgd * 0.60 + ad * 0.40) if xgd > 0 else (ad if ad > 0 else 1.0)
    sd = yd if yd > 0 else 1.2; se = ye if ye > 0 else 1.0
    cse = v.get("clean_sheets_ev", 0.0); csd = v.get("clean_sheets_dep", 0.0)
    def cf(cs):
        if cs <= 0: return 1.0
        if cs < 40.0: return 1.0 - (cs / 250.0)
        return max(0.40, 0.84 - (cs - 40.0) * (0.44 / 60.0))
    df = cf(cse); ef = cf(csd)
    le = he * 0.60 + sd * 0.40; ld = hd * 0.60 + se * 0.40
    fe = clamp(1 + (v.get("ppg_ev", 1.5) - 1.5) / 15, 0.85, 1.15)
    fd = clamp(1 + (v.get("mpg_dep", 1.5) - 1.5) / 15, 0.85, 1.15)
    le = le * 1.05 * fe; ld = ld * 0.95 * fd
    if le > 2.50: le = 2.50 + (le - 2.50) * 0.5
    if ld > 2.50: ld = 2.50 + (ld - 2.50) * 0.5
    return clamp(le, 0.05, 4.5), clamp(ld, 0.05, 4.5), 0.80


def matristen_olasilik(matris, mg=MAX_GOL):
    p1 = px = p2 = u25 = kg = 0.0; tot = 0.0
    for i in range(mg):
        for j in range(mg):
            p = matris[i][j]; tot += p
            if i > j: p1 += p
            elif i == j: px += p
            else: p2 += p
            if i + j > 2.5: u25 += p
            if i > 0 and j > 0: kg += p
    return {"1": p1, "X": px, "2": p2, "ust_25": u25, "kg_var": kg, "toplam": tot}


def monte_carlo_simulasyon(leb, ldb, n=MONTE_CARLO_N):
    seed = int(round(leb * 1_000_000)) * 1_000_003 + int(round(ldb * 1_000_000))
    rng = random.Random(seed)
    s = {"1": 0, "X": 0, "2": 0, "u25": 0, "kg": 0}
    for _ in range(n):
        le = leb * rng.uniform(1 - BELIRSIZLIK, 1 + BELIRSIZLIK)
        ld = ldb * rng.uniform(1 - BELIRSIZLIK, 1 + BELIRSIZLIK)
        eg = min(MAX_GOL - 1, poisson_random(le, rng))
        dg = min(MAX_GOL - 1, poisson_random(ld, rng))
        if eg > dg: s["1"] += 1
        elif eg == dg: s["X"] += 1
        else: s["2"] += 1
        if eg + dg > 2.5: s["u25"] += 1
        if eg > 0 and dg > 0: s["kg"] += 1
    def yz(x): return x / n * 100 if n > 0 else 0
    return {"p1": yz(s["1"]), "px": yz(s["X"]), "p2": yz(s["2"]), "ust25": yz(s["u25"]), "kg_var": yz(s["kg"])}


def analiz_hesapla(v):
    le, ld, gv = hesapla_lambda(v)
    matris = poisson_matris(le, ld, MAX_GOL)
    o = matristen_olasilik(matris, MAX_GOL)
    tot = o["toplam"] or 1
    p1p = o["1"] / tot * 100; pxp = o["X"] / tot * 100; p2p = o["2"] / tot * 100
    u25p = o["ust_25"] / tot * 100; kgp = o["kg_var"] / tot * 100
    mc = monte_carlo_simulasyon(le, ld, MONTE_CARLO_N)
    p1 = p1p * 0.60 + mc["p1"] * 0.40
    px = pxp * 0.60 + mc["px"] * 0.40
    p2 = p2p * 0.60 + mc["p2"] * 0.40
    t = p1 + px + p2
    if t > 0: p1, px, p2 = (p1 / t) * 100, (px / t) * 100, (p2 / t) * 100
    u25 = u25p * 0.65 + mc["ust25"] * 0.35
    kgm = kgp * 0.60 + mc["kg_var"] * 0.40
    kgy = 100.0 - kgm; alt = 100.0 - u25
    eo = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
    return {"lam_ev": le, "lam_dep": ld, "p1": p1, "px": px, "p2": p2, "ust_25": u25, "alt_25": alt, "kg_var_model": kgm, "kg_yok_model": kgy, "en_olasi": eo}


def kayit_olustur(v, a):
    return {"veri": copy.deepcopy(v), "analiz": {"p1": a["p1"], "px": a["px"], "p2": a["p2"], "tahmini_gol": a["lam_ev"] + a["lam_dep"], "kg_var_model": a["kg_var_model"], "ust_25": a["ust_25"]}}


def sonuc_hesapla(kayit):
    v = kayit["veri"]; a = kayit.get("analiz", {})
    if not v.get("skor_belli", False): return None
    se = v.get("skor_ev", 0); sd = v.get("skor_dep", 0)
    tg = se + sd; gu = tg > 2.5; gk = (se > 0 and sd > 0)
    g1 = "1" if se > sd else ("X" if se == sd else "2")
    u25 = a.get("ust_25", 50); alt = 100 - u25
    kgv = a.get("kg_var_model", 50); kgy = 100 - kgv
    p1a = a.get("p1", 33.33); pxa = a.get("px", 33.33); p2a = a.get("p2", 33.34)
    s1, y1 = max([("1", p1a), ("X", pxa), ("2", p2a)], key=lambda x: x[1])
    o1 = s1 if y1 >= esik_1x2_al(s1) else None
    og = None
    if u25 >= esik_al("ust") and u25 >= alt: og = "Üst"
    elif alt >= esik_al("alt") and alt >= u25: og = "Alt"
    okg = None
    if kgv >= esik_al("kg_var") and kgv >= kgy: okg = "Var"
    elif kgy >= esik_al("kg_yok") and kgy >= kgv: okg = "Yok"
    def _t(o, g):
        if o is None: return None, None
        d = "tam" if o == g else "yanlis"; return d == "tam", d
    t1, d1 = _t(o1, g1); tg_, dg_ = _t(og, "Üst" if gu else "Alt"); tk, dk = _t(okg, "Var" if gk else "Yok")
    return {"oneri_1x2": {"tahmin": o1, "tuttu": t1, "durum": d1}, "oneri_gol": {"tahmin": og, "tuttu": tg_, "durum": dg_}, "oneri_kg": {"tahmin": okg, "tuttu": tk, "durum": dk}}


def _form_ppg(s):
    return sum(3 if c == "W" else 1 if c == "D" else 0 for c in s) / max(len(s), 1)


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


MANUEL_ALANLAR = {
    "Sıralama": [("siralama_ev", "Ev Sıralaması", "int", 1), ("siralama_dep", "Dep Sıralaması", "int", 1)],
    "Takım isimleri (Ev)": [("takim_ev", "Ev Takım Adı", "str", "")],
    "Takım isimleri (Dep)": [("takim_dep", "Dep Takım Adı", "str", "")],
}


def _cift_tab(etiket, blok):
    pattern = r'([\d.,]+)%?\s*\t\s*' + re.escape(etiket) + r'\s*\t\s*([\d.,]+)%?'
    m = re.search(pattern, blok, re.IGNORECASE)
    if m:
        try: return float(m.group(1).replace(",", ".")), float(m.group(2).replace(",", "."))
        except ValueError: pass
    return None, None


def sportytrader_veri_cikar(metin):
    veri = {}; okunamayanlar = []
    m = re.search(r'^([A-ZÇĞİÖŞÜ][\w\s\.\-]+?)\s*-\s*([A-ZÇĞİÖŞÜ][\w\s\.\-]+?)\s+Stats', metin, re.MULTILINE)
    if m:
        veri["takim_ev"] = m.group(1).strip(); veri["takim_dep"] = m.group(2).strip()
    m = re.search(r'Time\s*\t\s*(\d{1,2}:\d{2})', metin)
    if m: veri["saat"] = m.group(1).strip()
    veri["ulke"] = _ulke_bul(metin)
    m = re.search(r'FT\s*\r?\n\s*(\d+)\s*-\s*(\d+)', metin)
    if m:
        veri["skor_ev"] = int(m.group(1)); veri["skor_dep"] = int(m.group(2)); veri["skor_belli"] = True
    else: veri["skor_belli"] = False
    idx = metin.find("Main Stats")
    if idx != -1:
        blok = metin[idx:idx+1500]
        v1, v2 = _cift_tab("Goals scored per game", blok)
        if v1 is not None: veri["atilan_ev"] = v1; veri["atilan_dep"] = v2
        v1, v2 = _cift_tab("Goals conceded per game", blok)
        if v1 is not None: veri["yenen_ev"] = v1; veri["yenen_dep"] = v2
    veri["format"] = "sportytrader"
    return veri, okunamayanlar


def metinden_veri_cikar(metin):
    metin = metin.replace(",", ".")
    if "Main Stats" in metin and "Goals scored per game" in metin:
        veri, okunamayanlar = sportytrader_veri_cikar(metin)
        if veri.get("saat"): veri["saat"] = saat_2_saat_ileri(veri["saat"])
        return veri, okunamayanlar
    return {}, []


# ==========================================
# VERİ ÇEKME MOTORU (requests-only)
# ==========================================
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def _scrapingbee_get(url, render_js=True, timeout=30, mac_sec="5", max_retry=3, dogrula=False):
    hata = None
    for d in range(max_retry):
        try:
            r = requests.get(url,
                headers={
                    "User-Agent": UA,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                },
                timeout=timeout)
            if r.status_code == 200 and r.text and len(r.text) > 500:
                return r.text, None
            hata = f"HTTP {r.status_code} • Boyut: {len(r.text) if r.text else 0}"
        except Exception as e:
            hata = f"Bağlantı: {str(e)[:150]}"
        if d < max_retry - 1: time.sleep(1 + d)
    return None, hata or "Sayfa alınamadı."


def _html_metne_cevir(html):
    soup = BeautifulSoup(html, "html.parser")
    for t in soup(["script", "style", "noscript", "svg", "iframe"]): t.decompose()
    for td in soup.find_all(["td", "th"]): td.insert_after("\t")
    for tr in soup.find_all("tr"): tr.insert_after("\n")
    for e in soup.find_all(["div", "p", "li", "h1", "h2", "h3", "h4", "br"]): e.insert_after("\n")
    m = soup.get_text(separator="", strip=False)
    m = re.sub(r'[ \t]+\n', '\n', m); m = re.sub(r'\n{3,}', '\n\n', m)
    return m


def mutating_ana_sayfa_linklerini_al(max_mac=MAX_MAC_SINIRI):
    html, hata = _scrapingbee_get("https://www.mutating.com/football-stats/", render_js=True)
    if hata: return [], [hata]
    if not html: return [], ["Ana sayfa indirilemedi"]
    soup = BeautifulSoup(html, "html.parser")
    maclar = []; gor = set()
    for link in soup.find_all("a", href=True):
        if len(maclar) >= max_mac: break
        href = link.get("href", "")
        if not any(x in href for x in ["match-preview", "match/", "/stats/"]): continue
        if href.startswith("/"): href = "https://www.mutating.com" + href
        elif not href.startswith("http"): continue
        if href in gor: continue
        gor.add(href)
        h2 = link.find_all("h2")
        tev = h2[0].get_text(strip=True) if len(h2) > 0 else ""
        tdep = h2[1].get_text(strip=True) if len(h2) > 1 else ""
        s_el = link.find(class_=re.compile(r"nostart|time|match-time"))
        saat = s_el.get_text(strip=True) if s_el else ""
        # ✅ YENİ: Ana sayfadan gelen saate +2 saat ekle
        if saat: saat = saat_2_saat_ileri(saat)
        maclar.append({"url": href, "takim_ev": tev, "takim_dep": tdep, "saat": saat})
    return maclar, []


def _mac_html_parse(html, url=""):
    soup = BeautifulSoup(html, "html.parser")
    veri = {}; okunamayanlar = []
    h1 = soup.find("h1")
    if h1:
        b = h1.get_text(strip=True)
        if " - " in b:
            p = b.replace(" Stats", "").replace(" stats", "").split(" - ")
            veri["takim_ev"] = p[0].strip()
            if len(p) > 1: veri["takim_dep"] = p[1].strip()
    metin = _html_metne_cevir(html)
    m1 = re.search(r'(\d{1,2}\.\d{1,2}\.\d{4})', metin)
    if m1: veri["tarih"] = m1.group(1)
    m1 = re.search(r'(\d{1,2}:\d{2})', metin)
    # ✅ YENİ: Detay sayfasından gelen saate de +2 saat ekle
    if m1: veri["saat"] = saat_2_saat_ileri(m1.group(1))
    veri["ulke"] = _ulke_bul(metin)

    skor = _skor_parse(html)
    if skor:
        veri["skor_ev"] = skor[0]; veri["skor_dep"] = skor[1]; veri["skor_belli"] = True
    else:
        veri["skor_belli"] = False

    def cf(label):
        for pat in [r'([\d.,]+)\s*%?\s*\t\s*' + re.escape(label) + r'\s*\t\s*([\d.,]+)', r'([\d.,]+)\s*%?\s*\|\s*' + re.escape(label) + r'\s*\|\s*([\d.,]+)', r'([\d.,]+)\s*%?\s+' + re.escape(label) + r'\s+([\d.,]+)\s*%?', r'([\d.,]+)\s*%?\s*\n\s*' + re.escape(label) + r'\s*\n\s*([\d.,]+)']:
            x = re.search(pat, metin, re.IGNORECASE)
            if x:
                try: return float(x.group(1).replace(",", ".")), float(x.group(2).replace(",", "."))
                except ValueError: continue
        return None, None

    for lb, ke, kd in [("Goals scored per game", "atilan_ev", "atilan_dep"), ("Goals conceded per game", "yenen_ev", "yenen_dep"), ("Clean sheets", "clean_sheets_ev", "clean_sheets_dep"), ("Team scored", "team_scored_ev", "team_scored_dep"), ("Both Teams to Score", "kg_siklik_ev", "kg_siklik_dep"), ("Over 2.5 goals", "ust25_ev", "ust25_dep")]:
        a, b = cf(lb)
        if a is not None and veri.get(ke, 0) == 0: veri[ke] = a; veri[kd] = b
    for lb, ke, kd in [("Win", "galibiyet_ev", "galibiyet_dep"), ("Draw", "beraberlik_ev", "beraberlik_dep"), ("Lose", "maglubiyet_ev", "maglubiyet_dep")]:
        x = re.search(r'([\d.,]+)\s*%\s*\t\s*' + lb + r'\s*\t\s*([\d.,]+)\s*%', metin, re.MULTILINE)
        if x:
            try: veri[ke] = float(x.group(1).replace(",", ".")); veri[kd] = float(x.group(2).replace(",", "."))
            except ValueError: pass
    veri["format"] = "mutating"
    if url: veri["kaynak_url"] = url
    return veri, []


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
    except Exception: return False


def mutating_mac_detay_cek(url):
    h, hata = _scrapingbee_get(url, render_js=True, mac_sec="5", dogrula=True)
    if hata: return None, [hata]
    if not h: return None, ["Sayfa indirilemedi"]
    return _mac_html_parse(h, url)


# ==========================================
# DÜZELTİLDİ: Veri kontrolü + thread-safe
# ==========================================
def _gelecek_mac_isle(mac, mevcut):
    try:
        veri, _ = mutating_mac_detay_cek(mac["url"])
        if not veri: return ("hata", mac, "Veri yok", None)
        if not veri.get("takim_ev"): veri["takim_ev"] = mac.get("takim_ev", "")
        if not veri.get("takim_dep"): veri["takim_dep"] = mac.get("takim_dep", "")
        if not veri.get("saat"): veri["saat"] = mac.get("saat", "")
        veri["kaynak_url"] = mac["url"]
        if mac["url"] in mevcut: return ("zaten_var", veri, "Zaten var", None)

        # ✅ YENİ: İstatistik verisi yoksa ATLA
        ae = veri.get("atilan_ev", 0); ye = veri.get("yenen_ev", 0)
        ad = veri.get("atilan_dep", 0); yd = veri.get("yenen_dep", 0)
        if ae == 0 and ye == 0 and ad == 0 and yd == 0:
            return ("veri_yok", veri, "İstatistik yok", None)

        # ✅ YENİ: Takım isimleri yoksa ATLA
        if not veri.get("takim_ev") or not veri.get("takim_dep"):
            return ("veri_yok", veri, "Takım isimleri yok", None)

        try: a = analiz_hesapla(veri)
        except Exception as e: return ("veri_yok", veri, f"Hata: {str(e)[:50]}", None)
        if _mac_tahmin_var_mi(veri):
            kayit = kayit_olustur(veri, a)
            return ("eklendi", veri, "Eklendi", kayit)
        return ("esik_alti", veri, "Eşik altı", None)
    except Exception as e:
        return ("hata", mac, f"İstisna: {str(e)[:80]}", None)


def mutating_toplu_cek(max_mac=MAX_MAC_SINIRI, progress_callback=None, max_workers=3):
    _ESIK_CACHE.clear()
    try: _ESIK_CACHE.update(dict(st.session_state.esikler))
    except Exception: pass
    maclar, hatalar = mutating_ana_sayfa_linklerini_al(max_mac=max_mac)
    if hatalar: return [], hatalar
    if not maclar: return [], ["Maç linki yok"]
    mevcut = set()
    for g in st.session_state.gelecek_analizler:
        u = g.get("veri", {}).get("kaynak_url", "")
        if u: mevcut.add(u)
    ek = 0; ea = 0; vy = 0; zv = 0; ht = 0; ekl = []; log = []; tam = 0
    eklenecekler = []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = {ex.submit(_gelecek_mac_isle, m, mevcut): m for m in maclar}
        for f in as_completed(futs):
            tam += 1; mac = futs[f]
            isim = f"{mac.get('takim_ev', '?')} - {mac.get('takim_dep', '?')}"
            try:
                r = f.result()
                if len(r) == 4: sonuc, veri, mesaj, kayit = r
                else: sonuc, veri, mesaj = r; kayit = None
                if sonuc == "eklendi":
                    ek += 1; ekl.append(veri)
                    if kayit is not None: eklenecekler.append(kayit)
                    log.append(f"✅ {isim} → {mesaj}")
                elif sonuc == "esik_alti": ea += 1; log.append(f"⚠️ {isim} → {mesaj}")
                elif sonuc == "veri_yok": vy += 1; log.append(f"🚫 {isim} → {mesaj}")
                elif sonuc == "zaten_var": zv += 1; log.append(f"↩️ {isim} → Zaten var")
                else: ht += 1; log.append(f"❌ {isim} → {mesaj}")
            except Exception as e:
                ht += 1; log.append(f"❌ {isim} → {str(e)[:80]}")
            if progress_callback:
                try: progress_callback(tam - 1, len(maclar), mac.get("takim_ev", ""))
                except Exception: pass
    if eklenecekler:
        st.session_state.gelecek_analizler.extend(eklenecekler)
        try: gelecek_kaydet(st.session_state.gelecek_analizler)
        except Exception: pass
    st.session_state.toplu_cek_ozet = {"bulunan": len(maclar), "eklenen": ek, "esik_alti": ea, "veri_yok": vy, "zaten_var": zv, "hata": ht, "detay_log": log[:300]}
    return ekl, []


def _lig_son_mac_linklerini_al(lig_url, adet=10):
    html, hata = _scrapingbee_get(lig_url, render_js=True, mac_sec="10")
    if hata: return [], [hata]
    if not html: return [], ["Lig sayfası indirilemedi"]
    soup = BeautifulSoup(html, "html.parser")
    maclar = []; gor = set()
    for link in soup.find_all("a", href=True):
        href = link.get("href", "")
        if "match-preview" not in href: continue
        if href.startswith("/"): href = "https://www.mutating.com" + href
        elif not href.startswith("http"): continue
        if href in gor: continue
        gor.add(href)
        takim_ev = ""; takim_dep = ""
        img = link.find_all("img", alt=True)
        if len(img) >= 2:
            takim_ev = img[0].get("alt", "").strip()
            takim_dep = img[1].get("alt", "").strip()
        maclar.append({"url": href, "takim_ev": takim_ev, "takim_dep": takim_dep})
        if len(maclar) >= adet: break
    return maclar, []


def _gecmis_mac_isle(mac, mevcut_urls):
    try:
        if mac["url"] in mevcut_urls: return ("atlandi", None, "Zaten var", None)
        html, hata = _scrapingbee_get(mac["url"], render_js=True, mac_sec="5", dogrula=True)
        if hata or not html: return ("hata", mac, hata or "HTML yok", None)
        veri, _ = _mac_html_parse(html, mac["url"])
        if not veri.get("skor_belli", False): return ("atlandi", None, "Skor yok", None)
        if veri.get("atilan_ev", 0) == 0 or veri.get("yenen_ev", 0) == 0: return ("atlandi", None, "İstatistik eksik", None)
        if not veri.get("takim_ev"): veri["takim_ev"] = mac.get("takim_ev", "")
        if not veri.get("takim_dep"): veri["takim_dep"] = mac.get("takim_dep", "")
        yv = copy.deepcopy(VARSAYILAN_VERI); yv.update(veri)
        kayit = kayit_olustur(yv, analiz_hesapla(yv))
        kayit["dogruluk"] = sonuc_hesapla(kayit)
        return ("eklendi", veri, f"{veri['skor_ev']}-{veri['skor_dep']}", kayit)
    except Exception as e:
        return ("hata", mac, str(e)[:80], None)


def lig_gecmis_cek(lig_url, adet=10, max_workers=3, progress_callback=None):
    _ESIK_CACHE.clear()
    try: _ESIK_CACHE.update(dict(st.session_state.esikler))
    except Exception: pass
    maclar, hatalar = _lig_son_mac_linklerini_al(lig_url, adet=adet)
    if hatalar: return [], hatalar
    if not maclar: return [], ["Lig sayfasında maç linki bulunamadı"]
    mevcut_urls = set()
    for g in st.session_state.gecmis_analizler:
        u = g.get("veri", {}).get("kaynak_url", "")
        if u: mevcut_urls.add(u)
    bas = []; hat = []; tam = 0
    eklenecekler = []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = {ex.submit(_gecmis_mac_isle, m, mevcut_urls): m for m in maclar}
        for f in as_completed(futs):
            tam += 1; mac = futs[f]
            try:
                r = f.result()
                sonuc, veri, mesaj, kayit = r if len(r) == 4 else (r[0], r[1], r[2], None)
                if sonuc == "eklendi":
                    bas.append(veri)
                    if kayit is not None: eklenecekler.append(kayit)
                elif sonuc == "atlandi": pass
                else: hat.append(f"{mac.get('takim_ev','?')}: {mesaj}")
            except Exception as e:
                hat.append(f"{mac.get('takim_ev','?')}: {e}")
            if progress_callback:
                try: progress_callback(tam - 1, len(maclar), mac.get("takim_ev", ""))
                except Exception: pass
    if eklenecekler:
        st.session_state.gecmis_analizler.extend(eklenecekler)
        try: gecmis_kaydet(st.session_state.gecmis_analizler)
        except Exception: pass
    return bas, hat


# ==========================================
# SKOR ÇEKME (SADECE FT — HT/DOM yok)
# ==========================================
def _skor_parse(html):
    """SADECE FT skorunu okur. HT/standings/DOM HİÇBİR ŞEYE bakmaz."""
    if not html:
        return None
    metin = _html_metne_cevir(html)

    # Ana format: "FT\n1 - 0" (FT tek başına satırda)
    m = re.search(r'(?:^|\n)\s*FT\s*\n+\s*(\d{1,2})\s*[-:]\s*(\d{1,2})', metin)
    if m:
        e, d = int(m.group(1)), int(m.group(2))
        if 0 <= e <= 12 and 0 <= d <= 12:
            return e, d

    # Yedek format: "FT 1-0" aynı satırda
    m = re.search(r'\bFT\s+(\d{1,2})\s*[-:]\s*(\d{1,2})\b', metin)
    if m:
        e, d = int(m.group(1)), int(m.group(2))
        if 0 <= e <= 12 and 0 <= d <= 12:
            return e, d

    return None


def _skor_cek(url, yedek=False):
    h, hata = _scrapingbee_get(url, timeout=30, max_retry=2)
    if not h: return None, f"Sayfa alınamadı: {hata}"
    skor = _skor_parse(h)
    if skor: return skor, None
    return None, None


def sonuclari_isle(max_workers=3, progress_callback=None):
    gel = st.session_state.gelecek_analizler
    isler = [(i, g) for i, g in enumerate(gel) if g.get("veri", {}).get("kaynak_url")]
    sonuc = {}; tam = 0
    if isler:
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futs = {ex.submit(_skor_cek, g["veri"]["kaynak_url"], False): (i, g) for i, g in isler}
            for f in as_completed(futs):
                i, g = futs[f]; tam += 1
                try: sonuc[i] = f.result()
                except Exception as e: sonuc[i] = (None, str(e)[:80])
                if progress_callback:
                    try: progress_callback(tam - 1, len(isler), g["veri"].get("takim_ev", ""))
                    except Exception: pass
    mevcut = {x.get("veri", {}).get("kaynak_url") for x in st.session_state.gecmis_analizler}
    tas = 0; bm = 0; ht = []; kalan = []
    for i, g in enumerate(gel):
        r = sonuc.get(i)
        if r is None: kalan.append(g); continue
        skor, hata = r
        v = g["veri"]; isim = f"{v.get('takim_ev', '?')} - {v.get('takim_dep', '?')}"
        if hata: ht.append(f"{isim}: {hata}"); kalan.append(g); continue
        if skor is None: bm += 1; kalan.append(g); continue
        v["skor_ev"] = skor[0]; v["skor_dep"] = skor[1]; v["skor_belli"] = True
        d = sonuc_hesapla(g)
        if d: g["dogruluk"] = d
        if v.get("kaynak_url") not in mevcut:
            st.session_state.gecmis_analizler.append(g)
            mevcut.add(v.get("kaynak_url"))
        tas += 1
    st.session_state.gelecek_analizler = kalan
    gecmis_kaydet(st.session_state.gecmis_analizler)
    gelecek_kaydet(st.session_state.gelecek_analizler)
    return {"tasinan": tas, "bitmemis": bm, "hatalar": ht, "toplam": len(isler)}


# ==========================================
# TASARIM YARDIMCILARI
# ==========================================
def _e(x): return _html.escape(str(x))


def mac_karti(ev, dep, sb, se, sd, le, ld, saat="", ulke="", tarih=""):
    orta = f'<div class="fa-score">{int(se)} - {int(sd)}</div>' if sb else '<div class="fa-vs">VS</div>'
    br = ulke_bayrak_bul(ulke); ust = ""
    if saat or ulke or tarih:
        p = []
        if br != "🌍" or ulke: p.append(f"{br} {_e((ulke or '').title())}")
        if tarih: p.append(f"📅 {_e(tarih)}")
        if saat: p.append(f"🕐 {_e(saat)}")
        if p: ust = f'<div class="fa-sub" style="margin-bottom:6px;">{" • ".join(p)}</div>'
    alt = f'<div class="fa-sub">Model beklenen gol: {le:.2f} - {ld:.2f}</div>'
    return f'<div class="fa-hero">{ust}<div class="fa-teams"><div class="fa-team">{_e(ev)}</div>{orta}<div class="fa-team">{_e(dep)}</div></div>{alt}</div>'


def mac_tahmin_karti(v_g, g=None):
    try:
        ya = yeniden_analiz(v_g)
        p1 = ya.get("p1", 33.33); px = ya.get("px", 33.33); p2 = ya.get("p2", 33.34)
        u25 = ya.get("ust_25", 50); a25 = 100 - u25
        kgv = ya.get("kg_var_model", 50); kgy = 100 - kgv
        e1 = max([("1", p1), ("X", px), ("2", p2)], key=lambda x: x[1])
        s1, y1 = e1; es1 = esik_1x2_al(s1); poz1 = y1 >= es1
        isim1 = {"1": "1 — Ev Kazanır", "X": "X — Beraberlik", "2": "2 — Dep Kazanır"}[s1]
        if u25 >= a25: gs = "Üst 2.5"; gy = u25; ge_ = esik_al("ust")
        else: gs = "Alt 2.5"; gy = a25; ge_ = esik_al("alt")
        gp = gy >= ge_
        if kgv >= kgy: ks = "KG Var"; ky = kgv; ke = esik_al("kg_var")
        else: ks = "KG Yok"; ky = kgy; ke = esik_al("kg_yok")
        kp = ky >= ke
        def r(p): return "pass" if p else "off"
        def b(p): return "ok" if p else "no"
        def bt(p): return "✅" if p else "⚪"
        return f'''<div class="fa-mk"><div class="fa-mk-row"><span class="fa-mk-lbl">🎯 1X2</span><span class="fa-mk-pick {r(poz1)}">{_e(isim1)}</span><span class="fa-mk-pct">%{y1:.0f} <span class="fa-mk-badge {b(poz1)}">{bt(poz1)} eşik %{es1:.0f}</span></span></div><div class="fa-mk-row"><span class="fa-mk-lbl">⚽ Gol</span><span class="fa-mk-pick {r(gp)}">{_e(gs)}</span><span class="fa-mk-pct">%{gy:.0f} <span class="fa-mk-badge {b(gp)}">{bt(gp)} eşik %{ge_:.0f}</span></span></div><div class="fa-mk-row"><span class="fa-mk-lbl">🤝 KG</span><span class="fa-mk-pick {r(kp)}">{_e(ks)}</span><span class="fa-mk-pct">%{ky:.0f} <span class="fa-mk-badge {b(kp)}">{bt(kp)} eşik %{ke:.0f}</span></span></div></div>'''
    except Exception: return ""


def olasilik_bar(e, y, esik=None, renk="#3b82f6"):
    y = max(0.0, min(100.0, y)); isr = ""
    if esik is not None:
        renk = "#22c55e" if y >= esik else "#475569"
        isr = f'<div class="fa-tick" style="left:{esik:.0f}%"></div>'
    return f'<div class="fa-row"><div class="fa-row-top"><span class="fa-lbl">{_e(e)}</span><span class="fa-val">%{y:.1f}</span></div><div class="fa-bar"><div class="fa-fill" style="width:{y:.1f}%;background:{renk}"></div>{isr}</div></div>'


def olasilik_paneli(a):
    s = ('<div class="fa-ttl">Maç Sonucu</div>'
        + olasilik_bar("Ev (1)", a["p1"], esik_1x2_al("1"), "#3b82f6")
        + olasilik_bar("Beraberlik (X)", a["px"], esik_1x2_al("X"), "#94a3b8")
        + olasilik_bar("Dep (2)", a["p2"], esik_1x2_al("2"), "#f59e0b")
        + '<div class="fa-ttl" style="margin-top:10px">Piyasalar</div>'
        + olasilik_bar("Üst 2.5", a["ust_25"], esik_al("ust"))
        + olasilik_bar("Alt 2.5", a["alt_25"], esik_al("alt"))
        + olasilik_bar("KG Var", a["kg_var_model"], esik_al("kg_var"))
        + olasilik_bar("KG Yok", a["kg_yok_model"], esik_al("kg_yok")))
    return f'<div class="fa-card">{s}</div>'


def yasal_metin_goster():
    with st.expander("📜 Kullanım Şartları", expanded=False):
        st.markdown(YASAL_METIN)


def gecmis_istatistik_hesapla():
    g1x2 = gg = gk = 0
    t1x2 = tg = tk = 0
    for g in st.session_state.gecmis_analizler:
        try:
            v = g["veri"]
            if not v.get("skor_belli"): continue
            d = sonuc_hesapla(g)
            if not d: continue
            o = d["oneri_1x2"]
            if o.get("tuttu") is not None:
                t1x2 += 1
                if o["tuttu"]: g1x2 += 1
            o = d["oneri_gol"]
            if o.get("tuttu") is not None:
                tg += 1
                if o["tuttu"]: gg += 1
            o = d["oneri_kg"]
            if o.get("tuttu") is not None:
                tk += 1
                if o["tuttu"]: gk += 1
        except Exception: continue
    p1 = (g1x2 / t1x2 * 100) if t1x2 else 0
    pg = (gg / tg * 100) if tg else 0
    pk = (gk / tk * 100) if tk else 0
    return p1, g1x2, t1x2, pg, gg, tg, pk, gk, tk


def modern_istatistik_grafik(baslik="📊 İSTATİSTİKLER"):
    p1, t1, s1, pg, tg, sg, pk, tk, sk = gecmis_istatistik_hesapla()
    st.markdown(f"### {baslik}")
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("1X2", f"%{p1:.1f}", f"{t1}/{s1}")
    with c2: st.metric("Gol", f"%{pg:.1f}", f"{tg}/{sg}")
    with c3: st.metric("KG", f"%{pk:.1f}", f"{tk}/{sk}")


def admin_giris_ekrani():
    st.markdown('<h1>🔐 Giriş Yap</h1>', unsafe_allow_html=True)
    with st.form("admin_giris_form"):
        kadi = st.text_input("👤 Kullanıcı Adı")
        sifre = st.text_input("🔐 Şifre", type="password")
        c1, c2 = st.columns(2)
        with c1: giris_btn = st.form_submit_button("✅ Giriş Yap", use_container_width=True, type="primary")
        with c2: iptal_btn = st.form_submit_button("⬅️ Ana Sayfa", use_container_width=True)
        if giris_btn:
            if not kadi.strip() or not sifre: st.error("❌ Kullanıcı adı ve şifre gerekli.")
            elif kadi.strip() == ADMIN_KULLANICI_ADI and sifre == ADMIN_SIFRE:
                st.session_state.rol = "admin"; st.session_state.admin_login_acik = False; st.session_state.sayfa = "giris"; st.rerun()
            elif kullanici_dogrula(kadi.strip(), sifre):
                st.session_state.aktif_kullanici = kadi.strip(); st.session_state.admin_login_acik = False; st.session_state.sayfa = "giris"
                st.success(f"✅ Hoş geldin, {kadi.strip()}!"); time.sleep(1); st.rerun()
            else: st.error("❌ Hatalı giriş.")
        if iptal_btn:
            st.session_state.admin_login_acik = False; st.session_state.sayfa = "giris"; st.rerun()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✨ Üye Ol", use_container_width=True, key="admin_to_kayit", type="primary"):
            st.session_state.admin_login_acik = False; st.session_state.sayfa = "kayit"; st.rerun()
    with c2:
        if st.button("⬅️ Ana Sayfa", use_container_width=True, key="admin_to_main"):
            st.session_state.admin_login_acik = False; st.session_state.sayfa = "giris"; st.rerun()


def ust_bar():
    c1, c2 = st.columns([3, 1])
    with c1:
        if admin_mi(): st.markdown("👑 **Admin Modu**")
        elif uye_mi(): st.markdown(f"👤 **{_e(uye_adi())}**")
        else: st.markdown("👤 Misafir")
    with c2:
        if admin_mi():
            if st.button("🚪 Çıkış", use_container_width=True, key="cikis_btn"):
                st.session_state.rol = "misafir"; st.session_state.sayfa = "giris"; st.rerun()
        elif uye_mi():
            if st.button("🚪 Çıkış", use_container_width=True, key="uye_cikis_btn"):
                st.session_state.aktif_kullanici = None; st.session_state.sayfa = "giris"; st.rerun()


def nav_git(h):
    st.session_state.sayfa = h
    st.session_state.kayit_yapildi = False
    st.rerun()


def nav_bar():
    if st.session_state.sayfa in ("kayit", "uyegirisi", "odeme", "giris_yap"): return
    if admin_mi():
        sec = [("🏠 Ana", "giris"), ("🔮 Gelecek", "gelecek_admin"), ("📊 Geçmiş", "gecmis"), ("💳 Ödemeler", "admin_odemeler"), ("👥 Aboneler", "admin_aboneler"), ("📬 Bildirimler", "admin_bildirimler"), ("⚙️ Ayar", "ayarlar")]
    elif uye_mi():
        sec = [("🏠 Ana", "giris"), ("📊 Geçmiş", "gecmis"), ("📬 Bildirim", "kullanici_bildirim")]
    else:
        sec = [("🏠 Ana", "giris"), ("📊 Geçmiş", "gecmis")]
    kl = st.columns(len(sec))
    for k, (e, h) in zip(kl, sec):
        with k:
            aktif = st.session_state.sayfa == h
            if st.button(e, key=f"nav_{h}", use_container_width=True, type="primary" if aktif else "secondary"):
                if not aktif: nav_git(h)


if st.session_state.admin_login_acik and not admin_mi():
    admin_giris_ekrani()
    st.stop()

ust_bar()
nav_bar()


if st.session_state.sayfa == "giris_yap":
    admin_giris_ekrani()

elif st.session_state.sayfa == "giris":
    if admin_mi():
        st.markdown("<h1>⚽ Futbol Analiz Pro</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:gray;'>Admin Paneli</p>", unsafe_allow_html=True)

        st.divider()
        st.markdown("### 📋 İstatistik Metnini Yapıştır")
        ym = st.text_area("Yapıştırma", height=200, key="yapistir_input", label_visibility="collapsed")
        c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 1])
        with c1: analiz_btn = st.button("🚀 ANALİZ ET", use_container_width=True, type="primary")
        with c2: gecmis_btn = st.button("📊 Geçmiş", use_container_width=True)
        with c3: gelecek_btn = st.button("🔮 Gelecek", use_container_width=True)
        with c4: backtest_btn = st.button("🔬 Test", use_container_width=True)
        with c5: ayarlar_btn = st.button("⚙️ Ayar", use_container_width=True)
        if analiz_btn:
            if not ym.strip(): st.warning("⚠️ Metin yapıştır.")
            else:
                cikan, okunamayanlar = metinden_veri_cikar(ym)
                if not cikan: st.error("❌ Veri çıkarılamadı.")
                else:
                    yv = copy.deepcopy(VARSAYILAN_VERI); yv.update(cikan)
                    st.session_state.form_verileri = yv; st.session_state.kayit_yapildi = False
                    st.session_state.sayfa = "sonuc"; st.rerun()
        if gecmis_btn: nav_git("gecmis")
        if gelecek_btn: nav_git("gelecek_admin")
        if backtest_btn: nav_git("backtest")
        if ayarlar_btn: nav_git("ayarlar")

        st.divider()
        st.markdown("### 🤖 Otomatik Veri Çekme")
        vs1, vs2, vs3 = st.tabs(["🔄 Gelecek Maçlar", "📜 Lig Geçmişi", "🏁 Sonuçları İşle"])
        with vs1:
            if st.session_state.toplu_cek_ozet:
                oz = st.session_state.toplu_cek_ozet
                st.markdown(f"**Son çekim:** Bulunan: **{oz.get('bulunan', 0)}** | Eklendi: **{oz.get('eklenen', 0)}** | Eşik altı: **{oz.get('esik_alti', 0)}** | Veri yok: **{oz.get('veri_yok', 0)}** | Zaten var: **{oz.get('zaten_var', 0)}** | Hata: **{oz.get('hata', 0)}**")
                if oz.get("detay_log"):
                    with st.expander(f"🔎 Detay"):
                        for s in oz["detay_log"]: st.text(s)
            c1, c2 = st.columns(2)
            with c1: w = st.number_input("Paralel", 1, 8, 3, 1, key="fw")
            with c2:
                st.markdown("")
                if st.button("🚀 Bugünün Maçlarını Çek", use_container_width=True, type="primary", key="mbtn"):
                    ph = st.empty()
                    def _p(i, t, n):
                        try: ph.progress(min((i + 1) / t, 1.0), text=f"{i+1}/{t}: {n}")
                        except Exception: pass
                    with st.spinner("Çekiliyor..."):
                        mutating_toplu_cek(max_mac=MAX_MAC_SINIRI, progress_callback=_p, max_workers=int(w))
                    ph.empty(); st.rerun()
        with vs2:
            lurl = st.text_input("Lig URL", key="lig_url_input", placeholder="https://www.mutating.com/football-stats/league-...")
            c1, c2 = st.columns(2)
            with c1: la = st.number_input("Kaç maç?", 5, 30, 10, 1, key="lig_adet")
            with c2: lw = st.number_input("Paralel", 1, 8, 3, 1, key="lig_workers")
            if st.button("📜 Ligi Çek", use_container_width=True, type="primary", key="lig_cek_btn"):
                if not lurl.strip(): st.warning("URL gerekli")
                else:
                    ph = st.empty()
                    def _p2(i, t, n):
                        try: ph.progress(min((i + 1) / t, 1.0), text=f"{i+1}/{t}: {n}")
                        except Exception: pass
                    with st.spinner(f"Son {la} maç..."):
                        bas, hat = lig_gecmis_cek(lurl.strip(), int(la), int(lw), _p2)
                    ph.empty()
                    if hat:
                        with st.expander(f"⚠️ {len(hat)} hata"):
                            for h in hat: st.caption(h)
                    if bas:
                        st.success(f"✅ {len(bas)} maç eklendi!"); time.sleep(2); st.rerun()
                    else: st.error("Hiçbir maç eklenemedi.")
        with vs3:
            if st.session_state.skor_ozet:
                oz = st.session_state.skor_ozet
                st.success(f"✅ {oz['tasinan']} taşındı • {oz['bitmemis']} bitmemiş • {len(oz.get('hatalar', []))} hata")
                if oz.get("hatalar"):
                    with st.expander("⚠️ Hata detayı"):
                        for _h in oz["hatalar"][:50]: st.caption(_h)
            st.markdown(f"Bekleyen: **{len(st.session_state.gelecek_analizler)}**")
            c1, c2 = st.columns(2)
            with c1: sw = st.number_input("Paralel", 1, 8, 3, 1, key="skor_w")
            with c2:
                if st.button("🏁 Skorları Çek", use_container_width=True, type="primary", key="skor_btn"):
                    if not st.session_state.gelecek_analizler: st.warning("Gelecek'te maç yok")
                    else:
                        with st.spinner("Kontrol..."):
                            st.session_state.skor_ozet = sonuclari_isle(int(sw))
                        st.rerun()

    else:
        gelecek = st.session_state.gelecek_analizler
        toplam = len(gelecek)
        premium = uye_premium_mu()
        kota = int(ayar_al("ucretsiz_kotasi", 3))

        if premium:
            st.markdown(f'<div class="mh-hero"><div class="mh-hero-ust">⚽ FUTBOL ANALİZ PRO</div><div class="mh-hero-title">Hoş Geldin, {_e(uye_adi())}</div><div class="mh-hero-sub">Premium aktif</div><div class="mh-hero-badge">🌟 PREMIUM</div></div>', unsafe_allow_html=True)
        elif uye_mi():
            st.markdown(f'<div class="mh-hero"><div class="mh-hero-ust">⚽ FUTBOL ANALİZ PRO</div><div class="mh-hero-title">Hoş Geldin, {_e(uye_adi())}</div><div class="mh-hero-sub">İlk {kota} maç ücretsiz</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="mh-hero"><div class="mh-hero-ust">⚽ FUTBOL ANALİZ PRO</div><div class="mh-hero-title">Bugün {toplam} Maç</div><div class="mh-hero-sub">İlk {kota} maç ücretsiz</div></div>', unsafe_allow_html=True)

        modern_istatistik_grafik()

        if not uye_mi():
            if st.button("💳 Premium / ✨ Üye Ol", use_container_width=True, type="primary", key="mis_prem"):
                st.session_state.sayfa = "kayit"; st.rerun()
            if st.button("🔐 Giriş Yap", use_container_width=True, key="mis_giris_btn"):
                st.session_state.sayfa = "giris_yap"; st.rerun()

        st.divider()
        if not gelecek: st.info("ℹ️ Henüz maç yok.")
        else:
            # ✅ YENİ: Saate göre erkenden gece doğru sırala
            sirali = sorted(enumerate(gelecek), key=lambda x: saat_sirala_anahtari(x[1]))
            acik = 0
            for idx, g in sirali:
                v = g["veri"]; te = v.get("takim_ev", "Ev") or "Ev"; td = v.get("takim_dep", "Dep") or "Dep"
                if premium or acik < kota:
                    try:
                        af = analiz_hesapla(v); le = af["lam_ev"]; ld = af["lam_dep"]
                    except Exception: le = ld = 0
                    st.markdown(mac_karti(te, td, False, 0, 0, le, ld, v.get("saat", ""), v.get("ulke", ""), v.get("tarih", "")), unsafe_allow_html=True)
                    th = mac_tahmin_karti(v, g)
                    if th: st.markdown(th, unsafe_allow_html=True)
                    if st.button("🔍 Detay", use_container_width=True, key=f"gmac_{idx}"):
                        st.session_state.form_verileri = copy.deepcopy(v); st.session_state.kayit_yapildi = True
                        st.session_state.gelecekten_gelindi = True; st.session_state.aktif_gelecek_idx = idx
                        st.session_state.sayfa = "sonuc"; st.rerun()
                    acik += 1
                else:
                    st.markdown(mac_karti(te, td, False, 0, 0, 0, 0, v.get("saat", ""), v.get("ulke", ""), v.get("tarih", "")), unsafe_allow_html=True)
                    st.warning("🔒 Premium'a geç")
                st.divider()
        yasal_metin_goster()


elif st.session_state.sayfa == "kayit":
    st.markdown('<h1>✨ Üye Ol</h1>', unsafe_allow_html=True)
    with st.form("kayit_form"):
        yk = st.text_input("👤 Kullanıcı Adı", max_chars=30)
        ys = st.text_input("🔐 Şifre", type="password")
        yst = st.text_input("🔐 Şifre Tekrar", type="password")
        yasal_onay = st.checkbox("✅ Kullanım Şartlarını kabul ediyorum.")
        c1, c2 = st.columns(2)
        with c1: kb = st.form_submit_button("✅ Kayıt Ol", use_container_width=True, type="primary")
        with c2: gb = st.form_submit_button("⬅️ Geri", use_container_width=True)
        if kb:
            if not yk.strip() or len(yk.strip()) < 3: st.error("❌ En az 3 karakter.")
            elif len(ys) < 4: st.error("❌ Şifre en az 4 karakter.")
            elif ys != yst: st.error("❌ Şifreler uyuşmuyor.")
            elif not yasal_onay: st.error("❌ Şartları kabul et.")
            else:
                b, m = kullanici_ekle(yk.strip(), ys)
                if b:
                    st.session_state["aktif_kullanici"] = yk.strip()
                    st.session_state["odeme_hedef_kadi"] = yk.strip()
                    st.session_state.sayfa = "odeme"; st.rerun()
                else: st.error(f"❌ {m}")
        if gb: st.session_state.sayfa = "giris"; st.rerun()


elif st.session_state.sayfa == "odeme":
    hedef = st.session_state.get("odeme_hedef_kadi") or uye_adi()
    if not hedef:
        st.error("❌ Kullanıcı yok."); st.stop()
    iban = ayar_al("iban", ""); hs = ayar_al("hesap_sahibi", "")
    fh = float(ayar_al("fiyat_haftalik", 49.0)); fa = float(ayar_al("fiyat_aylik", 149.0)); fy = float(ayar_al("fiyat_yillik", 999.0))
    st.markdown(f'<h1>💳 Premium</h1><p>Kullanıcı: <b>{_e(hedef)}</b></p>', unsafe_allow_html=True)
    sec = st.radio("Süre?", ["haftalik", "aylik", "yillik"], format_func=lambda x: {"haftalik": f"Haftalık {fh:.0f} ₺", "aylik": f"Aylık {fa:.0f} ₺", "yillik": f"Yıllık {fy:.0f} ₺"}[x], index=1)
    sg = {"haftalik": 7, "aylik": 30, "yillik": 365}[sec]
    fy_ = {"haftalik": fh, "aylik": fa, "yillik": fy}[sec]
    et = {"haftalik": "Haftalık", "aylik": "Aylık", "yillik": "Yıllık"}[sec]
    st.markdown(f"### 🏦 Havale\n**Alıcı:** {_e(hs)}\n\n**IBAN:** `{_e(iban)}`\n\n**Tutar:** {fy_:.0f} ₺\n\n**Açıklama:** `{_e(hedef)}`")
    st.divider()
    bk = bekleyen_yukle()
    if hedef in bk and bk[hedef].get("durum") == "bekliyor": st.warning("⏳ Bekleyen bildirimin var")
    else:
        iade_onay = st.checkbox("✅ İade kabul etmiyorum")
        if st.button("📤 Ödeme Yaptım", use_container_width=True, type="primary"):
            if not iade_onay: st.error("❌ Kabul et.")
            else:
                bk[hedef] = {"tarih": datetime.now().strftime("%Y-%m-%d %H:%M"), "sure_gun": int(sg), "sure_etiket": et, "fiyat": float(fy_), "durum": "bekliyor"}
                bekleyen_kaydet(bk); st.success("✅ Bildirimin alındı!"); time.sleep(2); st.rerun()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Ana", use_container_width=True): st.session_state.sayfa = "giris"; st.rerun()
    with c2:
        if st.button("🔄 Kontrol", use_container_width=True):
            if abonelik_aktif_mi(hedef): st.success("✅ Aktif!"); time.sleep(1); st.session_state.sayfa = "giris"; st.rerun()
            else: st.info("⏳ Bekleniyor")


elif st.session_state.sayfa == "admin_odemeler":
    if not admin_mi(): st.error("❌"); st.stop()
    st.markdown("<h1>💳 Bekleyen Ödemeler</h1>", unsafe_allow_html=True)
    bk = bekleyen_yukle()
    if not bk: st.info("Yok.")
    else:
        for k, b in list(bk.items()):
            st.markdown(f"**👤 {_e(k)}** — {b.get('sure_etiket')} — {b.get('fiyat', 0):.0f} ₺ — {b.get('tarih')}")
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("✅ Onayla", key=f"o_{k}", type="primary", use_container_width=True):
                    b_, yb = abonelik_aktif_et(k, b.get("sure_gun", 0))
                    if b_:
                        del bk[k]; bekleyen_kaydet(bk); st.success(f"✅ {k} → {yb}"); time.sleep(1); st.rerun()
            with c2:
                if st.button("❌ Reddet", key=f"r_{k}", use_container_width=True):
                    del bk[k]; bekleyen_kaydet(bk); st.rerun()
            with c3:
                if st.button("🗑️", key=f"s_{k}", use_container_width=True):
                    del bk[k]; bekleyen_kaydet(bk); st.rerun()
            st.divider()
    if st.button("⬅️ Ana", type="primary", use_container_width=True): st.session_state.sayfa = "giris"; st.rerun()


elif st.session_state.sayfa == "admin_aboneler":
    if not admin_mi(): st.error("❌"); st.stop()
    st.markdown("<h1>👥 Aboneler</h1>", unsafe_allow_html=True)
    kl = kullanicilar_yukle()
    if not kl: st.info("Kayıt yok.")
    else:
        for k, kd in list(kl.items()):
            aktif = abonelik_aktif_mi(k)
            durum = "🌟 AKTİF" if aktif else "⚪ Pasif"
            st.markdown(f"**👤 {_e(k)}** — {durum} — Bitiş: {kd.get('abonelik_bitis', 'Yok')}")
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                if st.button("+1H", key=f"ph_{k}", use_container_width=True): abonelik_aktif_et(k, 7); st.rerun()
            with c2:
                if st.button("+1A", key=f"p1_{k}", use_container_width=True): abonelik_aktif_et(k, 30); st.rerun()
            with c3:
                if st.button("+1Y", key=f"py_{k}", use_container_width=True): abonelik_aktif_et(k, 365); st.rerun()
            with c4:
                if st.button("İptal", key=f"ip_{k}", use_container_width=True): abonelik_iptal_et(k); st.rerun()
            with c5:
                if st.button("🗑️", key=f"ks_{k}", use_container_width=True): kullanici_sil(k); st.rerun()
            st.divider()
    if st.button("⬅️ Ana", type="primary", use_container_width=True): st.session_state.sayfa = "giris"; st.rerun()


elif st.session_state.sayfa == "admin_bildirimler":
    if not admin_mi(): st.error("❌"); st.stop()
    st.markdown("<h1>📬 Bildirimler</h1>", unsafe_allow_html=True)
    bd = bildirimler_yukle()
    if not bd: st.info("Yok.")
    else:
        for b in sorted(bd, key=lambda x: x.get("tarih", ""), reverse=True):
            bid = b.get("id")
            st.markdown(f"**{b.get('tip')}** — {_e(b.get('kullanici', ''))} — {b.get('tarih')}")
            st.write(f"**Konu:** {_e(b.get('konu', ''))}")
            st.write(_e(b.get('mesaj', '')))
            yanit = st.text_area("Yanıt", value=b.get("cevap", ""), key=f"cy_{bid}")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("💬 Kaydet", key=f"kaydet_{bid}", use_container_width=True, type="primary"):
                    bildirim_guncelle(bid, cevap=yanit, durum="okundu"); st.rerun()
            with c2:
                if st.button("🗑️ Sil", key=f"sil_{bid}", use_container_width=True): bildirim_sil(bid); st.rerun()
            st.divider()
    if st.button("⬅️ Ana", type="primary", use_container_width=True): st.session_state.sayfa = "giris"; st.rerun()


elif st.session_state.sayfa == "kullanici_bildirim":
    if not uye_mi(): st.error("❌"); st.stop()
    st.markdown("<h1>📬 Bildirim Gönder</h1>", unsafe_allow_html=True)
    with st.form("bildirim_form"):
        tip = st.selectbox("Kategori", options=list(BILDIRIM_TIPLERI.keys()), format_func=lambda x: f"{BILDIRIM_TIPLERI[x]['ikon']} {BILDIRIM_TIPLERI[x]['isim']}")
        konu = st.text_input("Konu")
        mesaj = st.text_area("Mesaj", height=150)
        if st.form_submit_button("📤 Gönder", use_container_width=True, type="primary"):
            if not konu.strip() or not mesaj.strip(): st.error("❌")
            else:
                bildirim_ekle(uye_adi(), tip, konu.strip(), mesaj.strip())
                st.success("✅"); time.sleep(1); st.rerun()
    st.divider()
    bl = kullanici_bildirimleri(uye_adi())
    for b in sorted(bl, key=lambda x: x.get("tarih", ""), reverse=True):
        st.markdown(f"**{b.get('tip')}** — {b.get('durum')}")
        st.write(f"**{_e(b.get('konu', ''))}**: {_e(b.get('mesaj', ''))}")
        if b.get("cevap"): st.info(f"💬 {b['cevap']}")
        st.divider()


elif st.session_state.sayfa == "gelecek_admin":
    if not admin_mi(): st.error("❌"); st.stop()
    st.markdown("<h1>🔮 Gelecek Maçlar</h1>", unsafe_allow_html=True)
    gel = st.session_state.gelecek_analizler
    st.caption(f"Toplam: **{len(gel)}** maç")
    if not gel: st.info("Gelecek maç yok.")
    else:
        # ✅ Saate göre sıralı
        sirali = sorted(enumerate(gel), key=lambda x: saat_sirala_anahtari(x[1]))
        for idx, g in sirali:
            v = g["veri"]; te = v.get("takim_ev", "Ev"); td = v.get("takim_dep", "Dep")
            st.markdown(mac_karti(te, td, False, 0, 0, 0, 0, v.get("saat", ""), v.get("ulke", ""), v.get("tarih", "")), unsafe_allow_html=True)
            c1, c2 = st.columns([5, 1])
            with c1:
                if st.button("🔍 Detay", key=f"gmac_{idx}", use_container_width=True):
                    st.session_state.form_verileri = copy.deepcopy(v)
                    st.session_state.kayit_yapildi = True; st.session_state.gelecekten_gelindi = True
                    st.session_state.aktif_gelecek_idx = idx; st.session_state.sayfa = "sonuc"; st.rerun()
            with c2:
                if st.button("🗑️", key=f"gsil_{idx}"):
                    st.session_state.gelecek_analizler.pop(idx)
                    gelecek_kaydet(st.session_state.gelecek_analizler); st.rerun()
            st.divider()
    if st.button("⬅️ Ana", type="primary", use_container_width=True): st.session_state.sayfa = "giris"; st.rerun()


elif st.session_state.sayfa == "gecmis":
    st.markdown("<h1>📊 Geçmiş Maçlar</h1>", unsafe_allow_html=True)
    gc = st.session_state.gecmis_analizler
    st.caption(f"Toplam: **{len(gc)}** maç")
    if not gc: st.info("Kayıt yok.")
    else:
        modern_istatistik_grafik()
        st.divider()
        for i, g in enumerate(reversed(gc)):
            idx = len(gc) - 1 - i; v = g["veri"]
            te = v.get("takim_ev", "Ev"); td = v.get("takim_dep", "Dep")
            se = v.get("skor_ev", 0); sd = v.get("skor_dep", 0)
            st.markdown(mac_karti(te, td, True, se, sd, 0, 0, "", v.get("ulke", ""), ""), unsafe_allow_html=True)
            if admin_mi():
                if st.button("🗑️", key=f"sil_{idx}"):
                    st.session_state.gecmis_analizler.pop(idx)
                    gecmis_kaydet(st.session_state.gecmis_analizler); st.rerun()
            st.divider()
    if admin_mi():
        if st.button("🗑️ Tüm Geçmişi Sil", use_container_width=True):
            st.session_state.gecmis_analizler = []; gecmis_kaydet([]); st.rerun()
    if st.button("⬅️ Ana", type="primary", use_container_width=True): st.session_state.sayfa = "giris"; st.rerun()


elif st.session_state.sayfa == "ayarlar":
    if not admin_mi(): st.error("❌"); st.stop()
    st.markdown("<h1>⚙️ Ayarlar</h1>", unsafe_allow_html=True)
    mv = st.session_state.esikler.copy()
    st.markdown("### 🏦 Ödeme")
    c1, c2 = st.columns(2)
    with c1: yiban = st.text_input("IBAN", value=mv.get("iban", ""))
    with c2: yhs = st.text_input("Hesap Sahibi", value=mv.get("hesap_sahibi", ""))
    st.markdown("### 💰 Fiyatlar")
    c1, c2, c3 = st.columns(3)
    with c1: yfh = st.number_input("Haftalık", min_value=1.0, value=float(mv.get("fiyat_haftalik", 49.0)))
    with c2: yfa = st.number_input("Aylık", min_value=1.0, value=float(mv.get("fiyat_aylik", 149.0)))
    with c3: yfy = st.number_input("Yıllık", min_value=1.0, value=float(mv.get("fiyat_yillik", 999.0)))
    st.markdown("### 🔓 Ücretsiz Kota")
    yk = st.number_input("Kaç maç ücretsiz?", 0, 50, int(mv.get("ucretsiz_kotasi", 3)))
    st.markdown("### 🎯 Eşikler")
    c1, c2, c3 = st.columns(3)
    with c1: ye1 = st.slider("1 %", 0, 100, int(mv.get("esik_1", 55.0)))
    with c2: yex = st.slider("X %", 0, 100, int(mv.get("esik_x", 55.0)))
    with c3: ye2 = st.slider("2 %", 0, 100, int(mv.get("esik_2", 55.0)))
    c4, c5 = st.columns(2)
    with c4: yu = st.slider("Üst %", 0, 100, int(mv.get("ust", 65.0)))
    with c5: ya = st.slider("Alt %", 0, 100, int(mv.get("alt", 55.0)))
    c6, c7 = st.columns(2)
    with c6: ykv = st.slider("KG Var %", 0, 100, int(mv.get("kg_var", 57.0)))
    with c7: yky = st.slider("KG Yok %", 0, 100, int(mv.get("kg_yok", 72.0)))
    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("💾 Kaydet", use_container_width=True, type="primary"):
            y = dict(mv); y.update({"iban": yiban, "hesap_sahibi": yhs, "fiyat_haftalik": float(yfh), "fiyat_aylik": float(yfa), "fiyat_yillik": float(yfy), "ucretsiz_kotasi": int(yk), "esik_1": float(ye1), "esik_x": float(yex), "esik_2": float(ye2), "ust": float(yu), "alt": float(ya), "kg_var": float(ykv), "kg_yok": float(yky)})
            st.session_state.esikler = y; ayarlar_kaydet(y); st.success("✅")
    with c2:
        if st.button("🔄 Sıfırla", use_container_width=True): ayarlar_kaydet({}); st.rerun()
    with c3:
        if st.button("⬅️ Ana", use_container_width=True): st.session_state.sayfa = "giris"; st.rerun()


elif st.session_state.sayfa == "sonuc":
    v = st.session_state.form_verileri; a = analiz_hesapla(v)
    te = v.get("takim_ev", "Ev") or "Ev"; td = v.get("takim_dep", "Dep") or "Dep"
    sb = v.get("skor_belli", False); se = v.get("skor_ev", 0); sd = v.get("skor_dep", 0)
    st.markdown(mac_karti(te, td, sb, se, sd, a["lam_ev"], a["lam_dep"]), unsafe_allow_html=True)
    st.markdown(olasilik_paneli(a), unsafe_allow_html=True)
    s1, y1 = max([("1", a["p1"]), ("X", a["px"]), ("2", a["p2"])], key=lambda x: x[1])
    st.markdown(f"### 🏆 Final: **{s1}** (%{y1:.1f})")
    if st.button("🔄 Yeni", use_container_width=True, type="primary"):
        st.session_state.form_verileri = copy.deepcopy(VARSAYILAN_VERI); st.session_state.sayfa = "giris"; st.rerun()
