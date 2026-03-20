import streamlit as st
import yfinance as yf
import pandas as pd
from PIL import Image
import os

st.set_page_config(page_title="Miguel Terminal Dividendos", layout="wide")

# Estilo Blanco Nítido
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

# --- 1. CABECERA CON TU LOGO ---
if os.path.exists("logo_miguel.png"):
    img = Image.open("logo_miguel.png")
    st.image(img, use_column_width=True)

st.title("🏹 Scanner & Dividendos - MIGUEL")
st.write("Analizando tendencia, RSI y rentabilidad por dividendo.")

# --- 2. MOTOR DEL ESCÁNER CON DIVIDENDOS ---
tickers = ["SAN.MC", "BBVA.MC", "TEF.MC", "IBE.MC", "ITX.MC", "REP.MC", "CABK.MC", "SAB.MC", "GRF.MC"]

if st.button('🚀 EJECUTAR ANÁLISIS COMPLETO (PRECIO + DIVIDENDOS)', use_container_width=True):
    st.subheader("📊 Radiografía del IBEX 35")
    cols = st.columns(3)
    
    with st.spinner('Calculando dividendos y señales...'):
        for i, t in enumerate(tickers):
            try:
                # Bajamos info completa del ticker para sacar el dividendo
                tk = yf.Ticker(t)
                df = tk.history(period="3mo")
                
                if not df.empty:
                    actual = float(df['Close'].iloc[-1])
                    
                    # Intentamos sacar el dividendo anualizado
                    div_yield = tk.info.get('dividendYield', 0)
                    if div_yield is None: div_yield = 0
                    div_porcentaje = div_yield * 100
                    
                    # Cálculo RSI
                    delta = df['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    rsi_val = 100 - (100 / (1 + rs.iloc[-1]))
                    
                    # Colores
                    if rsi_val > 70: color = "#fef2f2"
                    elif rsi_val < 30: color = "#f0fdf4"
                    else: color = "#f8fafc"
                    
                    with cols[i % 3]:
                        st.markdown(f"""
                            <div style="background-color:{color}; padding:15px; border-radius:10px; border:1px solid #e2e8f0; margin-bottom:15px;">
                                <h4 style="margin:0;">{t}</h4>
                                <p style="font-size:22px; font-weight:bold; margin:5px 0;">{actual:.2f}€</p>
                                <div style="color:#166534; font-weight:bold;">💰 Div: {div_porcentaje:.2f}% anual</div>
                                <small>RSI: {rsi_val:.1f}</small>
                            </div>
                        """, unsafe_allow_html=True)
            except: continue

st.divider()

# --- 3. CALCULADORA DE GANANCIAS TOTALES ---
st.subheader("💰 Calculadora de Ganancias Futuras (Subida + Dividendos)")
c1, c2 = st.columns([1, 1.5])

with c1:
    inv = st.number_input("Dinero a invertir (€):", value=1000, step=100)
    tick_sim = st.selectbox("Elegir acción:", tickers)
    subida = st.slider("Objetivo de subida (%)", 1, 30, 5)

with c2:
    try:
        t_sim = yf.Ticker(tick_sim)
        p_v = float(t_sim.history(period="1d")['Close'].iloc[-1])
        
        # Sacamos el dividendo para la simulación
        d_yield_sim = t_sim.info.get('dividendYield', 0)
        if d_yield_sim is None: d_yield_sim = 0
        
        n_acc = int(inv / p_v)
        gan_subida = (p_v * (subida/100)) * n_acc
        gan_dividendos = (inv * d_yield_sim)
        
        st.markdown(f"""
            <div style="background-color:#f0f9ff; padding:20px; border-radius:15px; border:2px solid #0369a1;">
                <h3 style="color:#0369a1; margin:0;">Proyección para {tick_sim}:</h3>
                <p style="font-size:24px; color:#166534; margin:10px 0;"><b>Ganarías {gan_subida:.2f}€ por la subida</b></p>
                <p style="font-size:18px; color:#1e293b; margin:0;"><b>+ Cobrarías {gan_dividendos:.2f}€ al año en dividendos</b></p>
                <hr>
                <p>Inversión: {n_acc * p_v:.2f}€ en {n_acc} acciones.</p>
            </div>
        """, unsafe_allow_html=True)
    except: st.write("Calculando datos...")
