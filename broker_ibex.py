import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from PIL import Image
import os

# Configuración de página
st.set_page_config(page_title="Miguel - Terminal Financiero Pro", layout="wide")

# Diseño Modo Claro Profesional
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .card { padding: 20px; border-radius: 12px; margin-bottom: 15px; border-left: 8px solid; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .compra { background-color: #f0fdf4; border-left-color: #22c55e; color: #166534; }
    .venta { background-color: #fef2f2; border-left-color: #ef4444; color: #991b1b; }
    .badge { background-color: #1e293b; color: white; padding: 3px 8px; border-radius: 5px; font-size: 11px; margin-right: 5px; }
    h1, h2, h3, h4 { color: #1e293b !important; font-family: 'Segoe UI'; }
    
    /* Centrado de la imagen */
    [data-testid="stImage"] {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. CABECERA CON TU LOGO (TAMAÑO AJUSTADO) ---
if os.path.exists("logo_miguel.png"):
    img = Image.open("logo_miguel.png")
    # Hemos cambiado width=300 por width=150 para reducirlo a la mitad
    st.image(img, width=150)

st.markdown("<h1 style='text-align: center; color: black;'>📡 Scanner IBEX Pro - MIGUEL</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center; color: grey;'>Analizando tendencia, volumen, riesgo (RSI) y dividendos.</p>", unsafe_allow_html=True)

# --- 2. EL SUPER ESCÁNER (RSI + DIVIDENDOS + BACKTESTING) ---
tickers = ["SAN.MC", "BBVA.MC", "TEF.MC", "IBE.MC", "ITX.MC", "REP.MC", "CABK.MC", "SAB.MC", "ENG.MC", "ELE.MC"]

st.markdown("<br>", unsafe_allow_html=True) # Espacio

if st.button('🚀 EJECUTAR ANÁLISIS COMPLETO DEL IBEX', use_container_width=True):
    col1, col2 = st.columns(2)
    with st.spinner('Analizando datos en tiempo real...'):
        for t in tickers:
            try:
                t_obj = yf.Ticker(t)
                # Descargamos datos con 'auto_adjust=False' para evitar avisos
                df = yf.download(t, period="4mo", progress=False, auto_adjust=False)
                if not df.empty:
                    # Datos Actuales
                    cierre = df['Close']
                    actual = float(cierre.iloc[-1])
                    precio_mes = float(cierre.iloc[-21]) if len(cierre) > 21 else actual
                    rent_mes = ((actual / precio_mes) - 1) * 100
                    
                    # Dividendo
                    div_yield = t_obj.info.get('dividendYield', 0)
                    div_p = div_yield * 100 if div_yield else 0
                    
                    # Cálculo RSI (Riesgo)
                    delta = cierre.diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    rsi_val = 100 - (100 / (1 + rs.iloc[-1]))
                    
                    # Semáforo de Riesgo
                    if rsi_val > 70: msg_rsi = "🔴 SOBRECOMPRA"
                    elif rsi_val < 30: msg_rsi = "🟢 SOBREVENTA"
                    else: msg_rsi = "⚖️ NEUTRO"
                    
                    # Columna y Diseño
                    target = col1 if rent_mes > 0 else col2
                    clase = "compra" if rent_mes > 0 else "venta"
                    
                    with target:
                        st.markdown(f"""
                            <div class="card {clase}">
                                <span class="badge">RSI: {rsi_val:.1f} ({msg_rsi})</span>
                                <h3 style="margin:5px 0;">{t}: {actual:.2f}€</h3>
                                <p style="margin:0;"><b>💰 Dividendo Anual: {div_p:.2f}%</b></p>
                                <p style="margin:0; font-size:14px;">Hace 30 días: {precio_mes:.2f}€ ({rent_mes:.2f}%)</p>
                            </div>
                        """, unsafe_allow_html=True)
            except: continue

st.divider()

# --- 3. SIMULADOR DE BENEFICIOS Y PAGA EXTRA ---
st.subheader("💰 Calculadora de Ganancias Futuras")
c1, c2 = st.columns([1, 1.5])

with c1:
    inversion = st.number_input("Dinero a invertir (€):", min_value=100, value=1000, step=100)
    accion_e = st.selectbox("Elegir acción:", tickers)
    objetivo = st.slider("Objetivo de subida (%)", 1, 30, 5)

with c2:
    try:
        t_sim = yf.Ticker(accion_e)
        data_sim = yf.download(accion_e, period="1d", progress=False, auto_adjust=False)
        p_v = float(data_sim['Close'].iloc[-1])
        y_v = t_sim.info.get('dividendYield', 0)
        
        num_acciones = int(inversion / p_v)
        ganancia_subida = (p_v * (objetivo/100)) * num_acciones
        paga_extra_anual = inversion * y_v
        
        st.markdown(f"""
            <div style="background-color:#f0f9ff; padding:20px; border-radius:15px; border:2px solid #0369a1;">
                <h3 style="color:#0369a1; margin-top:0;">Proyección para {accion_e}:</h3>
                <p style="font-size:24px; color:#166534; margin:10px 0;"><b>¡Ganarías {ganancia_subida:.2f}€ por la subida!</b></p>
                <p style="font-size:18px; color:#c2410c;">Y cobrarías <b>{paga_extra_anual:.2f}€ al año</b> de dividendos.</p>
                <p>Comprando {num_acciones} acciones a {p_v:.2f}€.</p>
            </div>
        """, unsafe_allow_html=True)
    except: st.write("Calculando...")
