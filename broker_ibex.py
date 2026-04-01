import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="Miguel Terminal PRO", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal Inteligente IBEX 35 - MIGUEL")

# --- 1. CALCULADORA ---
with st.sidebar:
    st.header("💰 CALCULADORA")
    capital = st.number_input("Inversión (€):", value=1000)
    st.divider()
    st.success("🟢 COMPRA: RSI < 35")
    st.error("🔴 RIESGO: RSI > 65")

# --- 2. LISTA TOTAL IBEX 35 ---
ibex_35 = [
    "SAN.MC", "BBVA.MC", "CABK.MC", "SAB.MC", "BKT.MC", "UNI.MC",
    "IBE.MC", "REP.MC", "NTGY.MC", "ELE.MC", "ENG.MC", "REE.MC", "SLBA.MC",
    "ITX.MC", "ANA.MC", "ACS.MC", "FER.MC", "ACX.MC", "MTS.MC", "IAG.MC", "PUIG.MC",
    "TEF.MC", "CLNX.MC", "IDR.MC", "AMS.MC", "GRF.MC", "ROVI.MC", "COL.MC", 
    "MRL.MC", "LOG.MC", "AENA.MC", "SCYR.MC", "FDR.MC", "MEL.MC", "MAP.MC"
]

# --- 3. MOTOR DE ANÁLISIS ---
if st.button('🚀 LANZAR ANÁLISIS TOTAL (PRECIOS Y SEMÁFOROS)', use_container_width=True):
    resultados = []
    progreso = st.progress(0)
    status = st.empty()
    
    with st.spinner('Forzando conexión con el mercado...'):
        for i, t in enumerate(ibex_35):
            try:
                status.text(f"Capturando datos de {t}...")
                # Usamos un periodo muy corto para que Yahoo no nos bloquee
                data = yf.download(t, period="1mo", interval="1d", progress=False)
                
                if not data.empty:
                    precio = float(data['Close'].iloc[-1])
                    # RSI Manual
                    delta = data['Close'].diff()
                    up = delta.clip(lower=0).rolling(window=14).mean()
                    down = -1 * delta.clip(upper=0).rolling(window=14).mean()
                    rsi = 100 - (100 / (1 + (up.iloc[-1] / (down.iloc[-1] + 0.0001))))
                    
                    if rsi < 35: sem, col, txt = "🟢", "#d4edda", "COMPRA"
                    elif rsi > 65: sem, col, txt = "🔴", "#f8d7da", "RIESGO"
                    else: sem, col, txt = "⚪", "#f8f9fa", "NEUTRO"
                    
                    resultados.append({
                        "t": t, "p": precio, "r": rsi, "s": sem, "c": col, "txt": txt
                    })
                time.sleep(0.1) # Pausa mínima
                progreso.progress((i + 1) / len(ibex_35))
            except: continue

    status.empty()

    if resultados:
        # --- PANEL VISUAL ---
        cols = st.columns(3)
        for idx, item in enumerate(resultados):
            with cols[idx % 3]:
                st.markdown(f"""
                <div style="background-color:{item['c']}; padding:15px; border-radius:10px; border:2px solid #eee; text-align:center; margin-bottom:10px;">
                    <h2 style="margin:0;">{item['t']}</h2>
                    <h1 style="margin:5px 0;">{item['p']:.2f}€</h1>
                    <p style="font-size:1.1em; margin:0;">RSI: <b>{item['r']:.1f}</b></p>
                    <h3 style="margin:5px 0;">{item['s']} {item['txt']}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                with c1: st.link_button("📊 Gráfico", f"https://www.google.com/finance/quote/{item['t'].replace('.MC','')}:BME", use_container_width=True)
                with c2: st.link_button("📰 Noticias", f"https://www.google.com/search?q={item['t']}+noticias&tbm=nws", use_container_width=True)
    else:
        st.error("❌ El bloqueo de Yahoo persiste. Prueba a abrir la app desde tu móvil SIN WIFI (usando datos 5G).")

st.divider()
st.caption("Miguel Terminal PRO - Sistema de Análisis de Fuerza (RSI)")
