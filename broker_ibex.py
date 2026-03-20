import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from PIL import Image
import os

st.set_page_config(page_title="Scanner Miguel Pro", layout="wide")

# Estilo blanco limpio
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

# --- 1. CABECERA CON TU LOGO ---
if os.path.exists("logo_miguel.png"):
    img = Image.open("logo_miguel.png")
    st.image(img, use_column_width=True)

st.title("🏹 Scanner & Simulador de Inversión")

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
                    
                    # Colores de riesgo
                    if rsi_val > 70: color, texto = "#fef2f2", "SOBRECOMPRA (CARO)"
                    elif rsi_val < 30: color, texto = "#f0fdf4", "SOBREVENTA (BARATO)"
                    else: color, texto = "#f8fafc", "NEUTRO"
                    
                    st.markdown(f"""
                        <div style="background-color:{color}; padding:15px; border-radius:10px; border:1px solid #e2e8f0; margin-bottom:10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                            <strong style="color:#1e293b; font-size:18px;">{t}</strong>: 
                            <span style="color:#0f172a; font-weight:bold;">{actual:.2f}€</span> | 
                            <span style="color:#475569;">RSI: {rsi_val:.1f} ({texto})</span>
                        </div>
                    """, unsafe_allow_html=True)
            except: continue

st.divider()

# --- 3. EL SIMULADOR DE INVERSIÓN ---
st.subheader("💰 Simulador de Compra")
col_sim1, col_sim2 = st.columns(2)

with col_sim1:
    capital = st.number_input("¿Cuánto dinero quieres invertir? (€)", min_value=100, value=1000, step=100)
    ticket_sim = st.selectbox("Selecciona una acción para simular:", tickers)

with col_sim2:
    try:
        data_sim = yf.download(ticket_sim, period="1d", progress=False)
        precio_sim = float(data_sim['Close'].iloc[-1])
        cantidad = int(capital / precio_sim)
        inversion_real = cantidad * precio_sim
        sobrante = capital - inversion_real
        
        st.markdown(f"""
            <div style="background-color:#f8fafc; padding:20px; border-radius:12px; border:2px solid #2563eb;">
                <h4 style="margin:0; color:#2563eb;">Resultado para {ticket_sim}:</h4>
                <p style="font-size:24px; margin:10px 0;">Puedes comprar <strong>{cantidad}</strong> acciones.</p>
                <small>Inversión real: {inversion_real:.2f}€ | Te sobran: {sobrante:.2f}€</small>
            </div>
        """, unsafe_allow_html=True)
    except:
        st.write("Cargando datos del simulador...")
