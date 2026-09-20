# -*- coding: utf-8 -*-
"""
V11.17 — Streamlit Mobil Uygulama
"""

import streamlit as st
import math, json, os, random, re

st.set_page_config(page_title="Futbol Analiz", page_icon="⚽", layout="centered")

LIG_ORT_GOL = 1.35

def poisson_pmf(k, lam):
    return math.exp(-lam) * (lam ** k) / math.factorial(k)

def dixon_coles_tau(x, y, lam_ev, lam_dep, rho):
    if x == 0 and y == 0: return 1 - lam_ev * lam_dep * rho
    if x == 0 and y == 1: return 1 + lam_ev * rho
    if x == 1 and y == 0: return 1 + lam_dep * rho
    if x == 1 and y == 1: return 1 - rho
    return 1.0

def skor_matrisi(lam_ev, lam_dep, rho, max_gol=6):
    mat = {}
    toplam = 0.0
    for i in range(max_gol + 1):
        for j in range(max_gol + 1):
            p = poisson_pmf(i, lam_ev) * poisson_pmf(j, lam_dep)
            p *= dixon_coles_tau(i, j, lam_ev, lam_dep, rho)
            if p < 0: p = 0.0
            mat[(i, j)] = p
            toplam += p
    for k in mat: mat[k] /= toplam
    return mat

def ozetle(mat):
    P1 = P0 = P2 = 0.0
    kg_var = 0.0
    for (i, j), p in mat.items():
        if i > j: P1 += p
        elif i == j: P0 += p
        else: P2 += p
        if i > 0 and j > 0: kg_var += p
        
    au_kombolar = {"ALT+VAR": 0.0, "ALT+YOK": 0.0, "UST+VAR": 0.0, "UST+YOK": 0.0}
    for (i, j), p in mat.items():
        toplam = i + j
        kg = (i > 0 and j > 0)
        if toplam >= 3:
            au_kombolar["UST+VAR" if kg else "UST+YOK"] += p
        else:
            au_kombolar["ALT+VAR" if kg else "ALT+YOK"] += p
    return P1, P0, P2, kg_var, au_kombolar

def ciftesan_sec(P1, P0, P2):
    taraflar = [("1", P1), ("0", P0), ("2", P2)]
    taraflar.sort(key=lambda x: x[1], reverse=True)
    en_yuksek_1 = taraflar[0][0]
    en_yuksek_2 = taraflar[1][0]
    secili = sorted([en_yuksek_1, en_yuksek_2])
    if secili == ["0", "1"]: cs_kod = "1X"
    elif secili == ["1", "2"]: cs_kod = "12"
    elif secili == ["0", "2"]: cs_kod = "X2"
    else: cs_kod = "?".join(secili)
    cs_olasilik = P1 + P0 + P2 - taraflar[2][1]
    return cs_kod, cs_olasilik

def metin_ayikla_mobile(metin):
    v = {}
    tablo_map = {
        "Ev takım": "ev_takim", "Dep takım": "dep_takim", "Lig": "lig",
        "PPG Ev": "ppg_ev", "MPG Dep": "ppg_dep",
        "Sıralama Ev": "siralama_ev", "Sıralama Dep": "siralama_dep",
        "xG Ev": "xg_ev", "xG Dep": "xg_dep",
        "Atılan Ev": "atilan_ev", "Atılan Dep": "atilan_dep",
        "Yenen Ev": "yenen_ev", "Yenen Dep": "yenen_dep",
        "KG Ev %": "kg_ev", "KG Dep %": "kg_dep",
    }
    for satir in metin.split("\n"):
        satir = satir.strip()
        if not satir: continue
        m = re.match(r'^(?:\d+\s+)?(.+?)\s+([\d.,]+)\s*$', satir)
        if m:
            alan, deger = m.group(1).strip(), m.group(2).strip()
            anahtar = tablo_map.get(alan)
            if anahtar:
                try: v[anahtar] = float(deger.replace(",", "."))
                except: pass
    return v

# STREAMLIT EKRANI
st.title("⚽ Futbol Analiz V11.17")
st.caption("Çifte Şans & Gol Analiz Sistemi")

metin = st.text_area("📋 Maç İstatistiklerini Yapıştırın:", height=180, placeholder="Maç istatistik metnini buraya yapıştırın...")

if st.button("⚡ MAÇI ANALİZ ET", use_container_width=True, type="primary"):
    if not metin.strip():
        st.warning("Lütfen metin girin!")
    else:
        v = metin_ayikla_mobile(metin)
        xg_ev = v.get("xg_ev", 1.2)
        xg_dep = v.get("xg_dep", 1.2)
        at_ev = v.get("atilan_ev", 1.2)
        at_dep = v.get("atilan_dep", 1.2)
        yen_ev = v.get("yenen_ev", 1.2)
        yen_dep = v.get("yenen_dep", 1.2)

        hucum_ev = 0.55 * xg_ev + 0.45 * at_ev
        hucum_dep = 0.55 * xg_dep + 0.45 * at_dep
        def_z_ev = max(0.60, min(1.50, yen_dep / LIG_ORT_GOL))
        def_z_dep = max(0.60, min(1.50, yen_ev / LIG_ORT_GOL))

        lam_ev = max(0.20, hucum_ev * def_z_ev * 1.10)
        lam_dep = max(0.20, hucum_dep * def_z_dep * 0.90)

        mat = skor_matrisi(lam_ev, lam_dep, -0.05)
        P1, P0, P2, kg_var, au_kombolar = ozetle(mat)
        cs_kod, cs_p = ciftesan_sec(P1, P0, P2)

        st.success(f"🎯 **Çifte Şans Tahmini:** {cs_kod} (%{cs_p*100:.1f} Güven)")

        col1, col2, col3 = st.columns(3)
        col1.metric("1 (Ev)", f"%{P1*100:.1f}")
        col2.metric("X (Berabere)", f"%{P0*100:.1f}")
        col3.metric("2 (Dep)", f"%{P2*100:.1f}")

        st.subheader("🎲 ALT/ÜST & KG Paneli")
        for k, p in au_kombolar.items():
            st.write(f"**{k}:** %{p*100:.1f}")
