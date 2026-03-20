import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from PIL import Image
import os

st.set_page_config(page_title="Miguel - Radar de Dividendos", layout="wide")

# Estilo blanco limpio
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

# --- 1. CABECERA CON TU LOGO ---
if os.path.exists("logo_miguel.png"):
    img = Image.open("logo_miguel.png")
    st.image(img, use_column_width=True)

st.title("🏹 Scanner de Dividendos e Inversión")

# --- 2. EL RADAR DE DIVIDENDOS Y TENDENCIA ---
tickers = ["SAN.MC", "BBVA.MC", "TEF.MC", "IBE.MC", "ITX.MC", "REP.MC", "CABK.MC", "SAB.MC", "ENG.MC", "ELE.MC"]

if st.button('🚀 ESCANEAR RENTABILIDAD POR DIVIDENDO', use_container_width=True):
    st.subheader("📊 Análisis de Rentas y Tendencia")
    col1, col2 = st.columns(2)
    
    with st.spinner('Calculando dividendos y salud financiera...'):
        for t in tickers:
            try:
                # Descargamos info y datos históricos
                ticker_obj = yf.Ticker(t)
                info = ticker_obj.info
                df = ticker_obj.history(period="3mo")
                
                if not df.empty:
                    actual = float(df['Close'].iloc[-1])
                    # Sacamos el dividendo (Yield)
                    div_yield = info.get('dividendYield', 0)
                    div_porcentaje = div_yield * 100 if div_yield else 0
                    
                    # Backtesting rápido (30 días)
                    precio_mes = float(df['Close'].iloc[-21]) if len(df) > 21 else actual
                    rent_mes = ((actual / precio_mes) - 1) * 100
                    
                    # Colores: Verde si paga > 4% de dividendo (buena renta)
                    color_div = "#f0fdf4" if div_porcentaje > 4 else "#f8fafc"
                    estrella = "⭐" if div_porcentaje > 5 else ""
                    
                    target = col1 if rent_mes > 0 else col2
                    
                    with target:
                        st.markdown(f"""
                            <div style="background-color:{color_div}; padding:15px; border-radius:10px; border:1px solid #ddd; margin-bottom:10px;">
                                <h4 style="margin:0;">{t}: {actual:.2f}€ {estrella}</h4>
                                <p style="margin:5px 0; color:#166534; font-weight:bold;">💰 Dividendo Anual: {div_porcentaje:.2f}%</p>
                                <p style="margin:0; font-size:14px;">Evolución mes: {rent_mes:.2f}%</p>
                            </div>
                        """, unsafe_allow_html=True)
            except: continue

st.divider()

# --- 3. SIMULADOR DE "PAGA EXTRA" ---
st.subheader("💵 Simulador de Paga Extra (Dividendos)")
c1, c2 = st.columns([1, 1.5])

with c1:
    inv_div = st.number_input("Dinero para invertir (€):", min_value=500, value=5000, step=500)
    accion_div = st.selectbox("Elegir para dividendos:", tickers)

with c2:
    try:
        t_obj = yf.Ticker(accion_div)
        y_div = t_obj.info.get('dividendYield', 0)
        p_div = float(t_obj.history(period="1d")['Close'].iloc[-1])
        
        cobro_anual = inv_div * y_div
        cobro_mensual = cobro_anual / 12
        
        st.markdown(f"""
            <div style="background-color:#fff7ed; padding:20px; border-radius:15px; border:2px solid #ea580c;">
                <h3 style="color:#ea580c; margin-top:0;">Tu Renta Pasiva con {accion_div}:</h3>
                <p style="font-size:24px; color:#c2410c; margin:10px 0;"><b>Cobrarías {cobro_anual:.2f}€ al año</b></p>
                <p style="font-size:18px;">Equivale a una "paga" de <b>{cobro_mensual:.2f}€ al mes</b> sin trabajar.</p>
                <hr style="border-top: 1px solid #ea580c;">
                <small>Basado en un dividendo del {(y_div*100):.2f}%</small>
            </div>
        """, unsafe_allow_html=True)
    except: st.write("Calculando renta...")
