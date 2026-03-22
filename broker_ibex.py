import streamlit as st
import yfinance as yf
import pandas as pd
from PIL import Image
import os

st.set_page_config(page_title="Miguel Terminal IBEX 35", layout="wide")

# Estilo Blanco Nítido
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

# --- 1. CABECERA ---
if os.path.exists("logo_miguel.png"):
    img = Image.open("logo_miguel.png")
    st.image(img, use_column_width=True)

st.title("🏹 Terminal IBEX 35 Completa - MIGUEL")
st.write("Análisis de los 35 valores: Semáforo RSI, Dividendos y Radar de Prensa.")

# --- 2. LISTA COMPLETA IBEX 35 ---
ibex_35 = [
    "ANA.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", "BKT.MC", "BBVA.MC",
    "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC",
    "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC",
    "ROVI.MC", "SCYR.MC", "SLBA.MC", "TEF.MC", "UNI.MC"
]

if st.button('🚀 ESCANEAR LOS 35 VALORES Y NOTICIAS', use_container_width=True):
    st.subheader("📊 Mapa del Mercado en Tiempo Real")
    cols = st.columns(3) # Dividimos en 3 columnas para que quepa todo bien
    
    with st.spinner('Conectando con la Bolsa de Madrid...'):
        for i, t in enumerate(ibex_35):
            try:
                tk = yf.Ticker(t)
                hist = tk.history(period="3mo")
                if hist.empty: continue
                
                precio_actual = float(hist['Close'].iloc[-1])
                
                # --- SEMÁFORO (RSI) ---
                delta = hist['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi_val = 100 - (100 / (1 + rs.iloc[-1]))
                
                if rsi_val > 70: est = "🔴 CARO"
                elif rsi_val < 30: est = "🟢 COMPRA"
                else: est = "⚪ NEUTRO"

                # --- DIVIDENDO ---
                div_yield = tk.info.get('dividendYield', 0)
                if not div_yield:
                    divs = tk.dividends
                    if not divs.empty: div_yield = (divs.iloc[-1] * 2) / precio_actual 
                div_final = (div_yield * 100) if div_yield else 0

                # --- MOSTRAR EN COLUMNAS ---
                with cols[i % 3]:
                    with st.expander(f"{t}: {precio_actual:.2f}€ | {est}"):
                        st.write(f"**RSI:** {rsi_val:.1f}")
                        if div_final > 0:
                            st.markdown(f"<span style='color:green;'>💰 <b>Div: {div_final:.2f}%</b></span>", unsafe_allow_html=True)
                        
                        # --- RADAR DE NOTICIAS (CORREGIDO) ---
                        nombre_n = t.split('.')[0]
                        url_news = f"https://www.google.com/search?q={nombre_n}+noticias+bolsa&tbm=nws"
                        url_grafico = f"https://www.google.com/finance/quote/{t.replace('.MC', ':BME')}"
                        
                        st.markdown(f"**📰 Radar de Noticias:**")
                        st.markdown(f"[👉 Leer últimas noticias de {nombre_n}]({url_news})")
                        st.markdown(f"[📊 Ver gráfico interactivo]({url_grafico})")

            except: continue
    st.success("¡Análisis de los 35 valores finalizado!")

st.divider()

# --- 3. CALCULADORA ---
st.subheader("💰 Simulador de Inversión")
c1, c2 = st.columns(2)
with c1:
    inver = st.number_input("Capital (€):", value=1000, step=500)
    acc_elegida = st.selectbox("Selecciona valor:", ibex_35)
    sub_obj = st.slider("Subida objetivo (%)", 1, 30, 5)
with c2:
    try:
        p_v = float(yf.Ticker(acc_elegida).history(period="1d")['Close'].iloc[-1])
        n_acc = int(inver / p_v)
        gan = (p_v * (sub_obj/100)) * n_acc
        st.success(f"**Ganancia estimada: +{gan:.2f}€**")
    except: st.info("Selecciona un valor del IBEX")
