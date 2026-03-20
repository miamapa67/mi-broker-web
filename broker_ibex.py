import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from PIL import Image
import os

st.set_page_config(page_title="Scanner Miguel Pro", layout="wide")

# Estilo blanco limpio
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

# --- CABECERA CON LOGO (CORREGIDO) ---
if os.path.exists("logo_miguel.png"):
    img = Image.open("logo_miguel.png")
    # Usamos 'use_column_width' que es la versión más estable
    st.image(img, use_column_width=True)
else:
    st.info("Configurando el entorno de Miguel...")

st.title("🏹 Scanner & Simulador de Inversión")

# --- EL RESTO DEL CÓDIGO (FUNCIONANDO) ---
tickers = ["SAN.MC", "BBVA.MC", "TEF.MC", "IBE.MC", "ITX.MC", "REP.MC", "CABK.MC", "SAB.MC", "GRF.MC"]

if st.button('🚀 ESCANEAR OPORTUNIDADES'):
    col1, col2 = st.columns(2)
    with st.spinner('Analizando el IBEX 35...'):
        for t in tickers:
            try:
                df = yf.download(t, period="3mo", progress=False)
                if not df.empty:
                    cierre = df['Close'].iloc[:, 0] if len(df['Close'].shape) > 1 else df['Close']
                    actual = float(cierre.iloc[-1])
                    # Cálculo rápido de RSI para el semáforo
                    delta = cierre.diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    rsi = 100 - (100 / (1 + rs))
                    rsi_val = float(rsi.iloc[-1])
                    
                    # Semáforo de colores
                    color = "#fef2f2" if rsi_val > 70 else "#f0fdf4" if rsi_val < 30 else "#fffbeb"
                    texto = "SOBRECOMPRA" if rsi_val > 70 else "SOBREVENTA" if rsi_val < 30 else "NEUTRO"
                    
                    st.markdown(f"""
                        <div style="background-color:{color}; padding:15px; border-radius:10px; border:1px solid #ddd; margin-bottom:10px;">
                            <strong>{t}</strong>: {actual:.2f}€ | RSI: {rsi_val:.1f} ({texto})
                        </div>
                    """, unsafe_allow_html=True)
            except: continue
