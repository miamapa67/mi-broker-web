import streamlit as st
import yfinance as yf
import pandas as pd
from PIL import Image
import os

st.set_page_config(page_title="Miguel Terminal Pro", layout="wide")

# Estilo Blanco Nítido
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

# --- 1. CABECERA CON TU LOGO ---
if os.path.exists("logo_miguel.png"):
    img = Image.open("logo_miguel.png")
    st.image(img, use_column_width=True)

st.title("🏹 Scanner IBEX Pro - MIGUEL")
st.write("Analizando tendencia, volumen y riesgo (RSI) en tiempo real.")

# --- 2. EL MOTOR DEL ESCÁNER (CORREGIDO) ---
tickers = ["SAN.MC", "BBVA.MC", "TEF.MC", "IBE.MC", "ITX.MC", "REP.MC", "CABK.MC", "SAB.MC", "GRF.MC"]

# Usamos un contenedor para que los resultados no desaparezcan
if st.button('🚀 EJECUTAR ANÁLISIS COMPLETO DEL IBEX', use_container_width=True):
    st.subheader("📊 Resultados del Mercado")
    
    # Creamos 3 columnas para que las tarjetas queden ordenadas
    cols = st.columns(3)
    
    with st.spinner('Conectando con la Bolsa de Madrid...'):
        for i, t in enumerate(tickers):
            try:
                df = yf.download(t, period="3mo", progress=False)
                if not df.empty:
                    cierre = df['Close'].iloc[:, 0] if len(df['Close'].shape) > 1 else df['Close']
                    actual = float(cierre.iloc[-1])
                    
                    # Cálculo RSI rápido
                    delta = cierre.diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    rsi_val = 100 - (100 / (1 + rs.iloc[-1]))
                    
                    # Semáforo
                    if rsi_val > 70: color, txt = "#fef2f2", "CARO (Vender)"
                    elif rsi_val < 30: color, txt = "#f0fdf4", "BARATO (Comprar)"
                    else: color, txt = "#f8fafc", "NEUTRO"
                    
                    # Repartimos en las 3 columnas
                    with cols[i % 3]:
                        st.markdown(f"""
                            <div style="background-color:{color}; padding:15px; border-radius:10px; border:1px solid #e2e8f0; margin-bottom:15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                                <h4 style="margin:0; color:#1e293b;">{t}</h4>
                                <p style="font-size:20px; font-weight:bold; margin:5px 0;">{actual:.2f}€</p>
                                <small>RSI: {rsi_val:.1f} ({txt})</small>
                            </div>
                        """, unsafe_allow_html=True)
            except: continue
    st.success("Análisis finalizado.")

st.divider()

# --- 3. CALCULADORA (SE MANTIENE IGUAL) ---
st.subheader("💰 Calculadora de Ganancias Futuras")
c1, c2 = st.columns([1, 1.5])

with c1:
    inv = st.number_input("Dinero a invertir (€):", value=1000)
    tick_sim = st.selectbox("Elegir acción:", tickers)
    subida = st.slider("Objetivo de subida (%)", 1, 30, 5)

with c2:
    try:
        d_sim = yf.download(tick_sim, period="1d", progress=False)
        p_v = float(d_sim['Close'].iloc[-1])
        n_acc = int(inv / p_v)
        gan_b = (p_v * (subida/100)) * n_acc
        st.markdown(f"""
            <div style="background-color:#f0f9ff; padding:20px; border-radius:15px; border:2px solid #0369a1;">
                <h3 style="color:#0369a1; margin:0;">Proyección para {tick_sim}:</h3>
                <p style="font-size:24px; color:#166534; margin:10px 0;"><b>¡Ganarías {gan_b:.2f}€!</b></p>
                <p>Comprando {n_acc} acciones a {p_v:.2f}€</p>
            </div>
        """, unsafe_allow_html=True)
    except: st.write("Calculando...")
