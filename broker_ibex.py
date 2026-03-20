import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from PIL import Image
import os

st.set_page_config(page_title="Miguel - Backtesting Pro", layout="wide")

# Estilo blanco limpio
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

# --- 1. CABECERA CON TU LOGO ---
if os.path.exists("logo_miguel.png"):
    img = Image.open("logo_miguel.png")
    st.image(img, use_column_width=True)

st.title("🏹 Scanner & Prueba de Estrategia (Backtesting)")

# --- 2. ESCÁNER CON BACKTESTING DE 30 DÍAS ---
tickers = ["SAN.MC", "BBVA.MC", "TEF.MC", "IBE.MC", "ITX.MC", "REP.MC", "CABK.MC", "SAB.MC", "GRF.MC"]

if st.button('🚀 ESCANEAR Y PROBAR ESTRATEGIA', use_container_width=True):
    st.subheader("📊 Resultados de los últimos 30 días")
    col1, col2 = st.columns(2)
    
    with st.spinner('Viajando al pasado para calcular rentabilidad...'):
        for t in tickers:
            try:
                # Descargamos datos de 4 meses para tener perspectiva
                df = yf.download(t, period="4mo", progress=False)
                if not df.empty:
                    cierre = df['Close'].iloc[:, 0] if len(df['Close'].shape) > 1 else df['Close']
                    
                    # Datos HOY
                    precio_hoy = float(cierre.iloc[-1])
                    
                    # Datos HACE 30 DÍAS (Aproximadamente 20 sesiones de bolsa)
                    precio_hace_mes = float(cierre.iloc[-21])
                    rentabilidad_mes = ((precio_hoy / precio_hace_mes) - 1) * 100
                    
                    # Cálculo RSI actual para el semáforo
                    delta = cierre.diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    rsi_val = 100 - (100 / (1 + rs.iloc[-1]))
                    
                    # Color según si habríamos ganado dinero
                    color_backtest = "#dcfce7" if rentabilidad_mes > 0 else "#fee2e2"
                    emoji = "📈" if rentabilidad_mes > 0 else "📉"
                    
                    with (col1 if rentabilidad_mes > 0 else col2):
                        st.markdown(f"""
                            <div style="background-color:{color_backtest}; padding:15px; border-radius:10px; border:1px solid #ddd; margin-bottom:10px;">
                                <h4 style="margin:0;">{t}: {precio_hoy:.2f}€</h4>
                                <p style="margin:5px 0;">Hace 30 días: {precio_hace_mes:.2f}€</p>
                                <strong style="font-size:18px;">{emoji} Rentabilidad: {rentabilidad_mes:.2f}%</strong><br>
                                <small>Estado actual RSI: {rsi_val:.1f}</small>
                            </div>
                        """, unsafe_allow_html=True)
            except: continue

st.divider()

# --- 3. SIMULADOR DE GANANCIAS ---
st.subheader("💰 Calculadora de Beneficios Futuros")
c1, c2 = st.columns([1, 1.5])

with c1:
    inversion = st.number_input("Dinero a invertir (€):", min_value=100, value=1000, step=100)
    accion_elegida = st.selectbox("Valor elegido:", tickers)
    objetivo = st.slider("Objetivo de subida (%)", 1, 30, 5)

with c2:
    try:
        data_s = yf.download(accion_elegida, period="1d", progress=False)
        precio_v = float(data_s['Close'].iloc[-1])
        num_acciones = int(inversion / precio_v)
        total_invertido = num_acciones * precio_v
        ganancia_bruta = (precio_v * (objetivo/100)) * num_acciones
        
        st.markdown(f"""
            <div style="background-color:#f0f9ff; padding:20px; border-radius:15px; border:2px solid #0369a1;">
                <h3 style="color:#0369a1; margin-top:0;">Proyección para {accion_elegida}:</h3>
                <p style="font-size:28px; color:#166534; margin:10px 0;"><b>¡Ganarías {ganancia_bruta:.2f}€!</b></p>
                <p>Comprando {num_acciones} acciones.</p>
            </div>
        """, unsafe_allow_html=True)
    except: st.write("Seleccionando datos...")
