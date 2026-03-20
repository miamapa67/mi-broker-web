import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from PIL import Image
import os

st.set_page_config(page_title="Miguel Inversor Pro", layout="wide")

# Estilo blanco limpio
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

# --- 1. CABECERA CON TU LOGO ---
if os.path.exists("logo_miguel.png"):
    img = Image.open("logo_miguel.png")
    st.image(img, use_column_width=True)

st.title("🏹 Scanner & Proyección de Ganancias")

# --- 2. ESCÁNER DE OPORTUNIDADES ---
tickers = ["SAN.MC", "BBVA.MC", "TEF.MC", "IBE.MC", "ITX.MC", "REP.MC", "CABK.MC", "SAB.MC", "GRF.MC"]

if st.button('🚀 ESCANEAR OPORTUNIDADES AHORA', use_container_width=True):
    col1, col2 = st.columns(2)
    with st.spinner('Analizando el IBEX 35...'):
        for t in tickers:
            try:
                df = yf.download(t, period="3mo", progress=False)
                if not df.empty:
                    cierre = df['Close'].iloc[:, 0] if len(df['Close'].shape) > 1 else df['Close']
                    actual = float(cierre.iloc[-1])
                    
                    # Cálculo RSI
                    delta = cierre.diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    rsi_val = 100 - (100 / (1 + rs.iloc[-1]))
                    
                    if rsi_val > 70: color, texto = "#fef2f2", "SOBRECOMPRA (CARO)"
                    elif rsi_val < 30: color, texto = "#f0fdf4", "SOBREVENTA (BARATO)"
                    else: color, texto = "#f8fafc", "NEUTRO"
                    
                    st.markdown(f"""
                        <div style="background-color:{color}; padding:15px; border-radius:10px; border:1px solid #e2e8f0; margin-bottom:10px;">
                            <strong style="color:#1e293b;">{t}</strong>: <b>{actual:.2f}€</b> | RSI: {rsi_val:.1f} ({texto})
                        </div>
                    """, unsafe_allow_html=True)
            except: continue

st.divider()

# --- 3. SIMULADOR DE GANANCIAS (EL QUE TÚ QUERÍAS) ---
st.subheader("💰 Simulador de Beneficios Reales")
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
        
        # Cálculo de beneficio
        precio_objetivo = precio_v * (1 + objetivo/100)
        ganancia_bruta = (precio_objetivo - precio_v) * num_acciones
        total_final = total_invertido + ganancia_bruta
        
        st.markdown(f"""
            <div style="background-color:#f0f9ff; padding:20px; border-radius:15px; border:2px solid #0369a1;">
                <h3 style="color:#0369a1; margin-top:0;">Si {accion_elegida} sube un {objetivo}%:</h3>
                <p style="font-size:20px; margin:5px 0;">Comprarías <b>{num_acciones}</b> acciones a {precio_v:.2f}€</p>
                <hr style="border-top: 1px solid #0369a1;">
                <p style="font-size:28px; color:#166534; margin:10px 0;"><b>¡Ganarías {ganancia_bruta:.2f}€!</b></p>
                <p style="font-size:16px; color:#475569;">Tendrías un total de <b>{total_final:.2f}€</b> en tu cuenta.</p>
            </div>
        """, unsafe_allow_html=True)
    except:
        st.write("Selecciona una acción para calcular...")
