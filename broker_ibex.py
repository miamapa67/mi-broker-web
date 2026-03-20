import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Configuración de página
st.set_page_config(page_title="IBEX 35 - Inversión Inteligente", layout="wide")

# Estilo CSS (Modo Claro Profesional)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .card { padding: 18px; border-radius: 12px; margin-bottom: 12px; border-left: 6px solid; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .riesgo-bajo { background-color: #f0fdf4; border-left-color: #22c55e; color: #166534; }
    .riesgo-medio { background-color: #fffbeb; border-left-color: #f59e0b; color: #92400e; }
    .riesgo-alto { background-color: #fef2f2; border-left-color: #ef4444; color: #991b1b; }
    .sim-box { background-color: #f8fafc; padding: 25px; border-radius: 20px; border: 1px solid #e2e8f0; margin-top: 20px; }
    h1, h2, h3 { color: #1e293b !important; }
    </style>
    """, unsafe_allow_html=True)

def calcular_rsi(series, periods=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / (loss + 1e-9)
    return 100 - (100 / (1 + rs))

st.title("🏹 Scanner & Simulador de Inversión")

# --- PARTE 1: EL SCANNER ---
tickers = ["SAN.MC", "BBVA.MC", "TEF.MC", "IBE.MC", "ITX.MC", "REP.MC", "CABK.MC", "SAB.MC", "GRF.MC"]

if st.button('🚀 ESCANEAR OPORTUNIDADES'):
    c1, c2 = st.columns(2)
    with st.spinner('Analizando mercado...'):
        for t in tickers:
            try:
                df = yf.download(t, period="3mo", progress=False)
                if not df.empty:
                    cierre = df['Close'].iloc[:, 0] if len(df['Close'].shape) > 1 else df['Close']
                    actual = float(cierre.iloc[-1])
                    media_20 = float(cierre.tail(20).mean())
                    rsi_val = float(calcular_rsi(cierre).iloc[-1])
                    
                    # Lógica de colores por RSI
                    tipo = "riesgo-alto" if rsi_val > 70 else ("riesgo-bajo" if rsi_val < 30 else "riesgo-medio")
                    label = "SOBRECOMPRA" if rsi_val > 70 else ("SOBREVENTA" if rsi_val < 30 else "NEUTRO")
                    
                    with (c1 if actual > media_20 else c2):
                        st.markdown(f"""<div class="card {tipo}">
                            <strong>{t}</strong>: {actual:.2f}€ | RSI: {rsi_val:.1f} ({label})
                        </div>""", unsafe_allow_html=True)
            except: continue

st.divider()

# --- PARTE 2: EL SIMULADOR (LA NOVEDAD) ---
st.header("💰 Simulador de Compra")
st.write("Calcula cuánto puedes ganar con los valores que el scanner ha marcado en **Verde**.")

col_sim1, col_sim2 = st.columns([1, 1])

with col_sim1:
    presupuesto = st.number_input("¿Cuánto dinero quieres invertir? (€)", min_value=100, value=1000, step=100)
    ticker_sim = st.selectbox("Selecciona la acción para el simulacro:", tickers)
    objetivo_ganancia = st.slider("Objetivo de subida (%)", 1, 20, 5)

with col_sim2:
    try:
        datos_sim = yf.Ticker(ticker_sim).history(period="1d")
        precio_sim = float(datos_sim['Close'].iloc[-1])
        
        num_acciones = int(presupuesto / precio_sim)
        inversion_real = num_acciones * precio_sim
        ganancia_esperada = inversion_real * (objetivo_ganancia / 100)
        
        st.markdown(f"""
            <div class="sim-box">
                <h3 style="margin-top:0;">Plan de Inversión para {ticker_sim}</h3>
                <p>Con <b>{presupuesto}€</b> puedes comprar <b>{num_acciones} acciones</b>.</p>
                <p>Inversión exacta: <b>{inversion_real:.2f}€</b></p>
                <hr>
                <h2 style="color:#22c55e !important;">Ganancia estimada: +{ganancia_esperada:.2f}€</h2>
                <small>Si el precio sube un {objetivo_ganancia}% ({precio_sim * (1+objetivo_ganancia/100):.2f}€)</small>
            </div>
        """, unsafe_allow_html=True)
    except:
        st.warning("Selecciona un ticker válido para simular.")
