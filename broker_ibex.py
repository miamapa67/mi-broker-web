import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Configuración de página
st.set_page_config(page_title="IBEX 35 - Semáforo de Riesgo", layout="wide")

# Estilo CSS Avanzado
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .card { padding: 20px; border-radius: 12px; margin-bottom: 15px; border-left: 8px solid; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .riesgo-bajo { background-color: #f0fdf4; border-left-color: #22c55e; color: #166534; }
    .riesgo-medio { background-color: #fffbeb; border-left-color: #f59e0b; color: #92400e; }
    .riesgo-alto { background-color: #fef2f2; border-left-color: #ef4444; color: #991b1b; }
    .badge { background-color: #1e293b; color: white; padding: 3px 8px; border-radius: 5px; font-size: 11px; margin-right: 5px; }
    h1, h2, h3 { color: #1e293b !important; }
    </style>
    """, unsafe_allow_html=True)

def calcular_rsi(series, periods=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    return 100 - (100 / (1 * rs + 1))

st.title("🏹 Scanner con Semáforo de Riesgo")
st.write("Analizando tendencia, volumen y fatiga del precio (RSI).")

tickers = ["SAN.MC", "BBVA.MC", "TEF.MC", "IBE.MC", "ITX.MC", "REP.MC", "CABK.MC", "SAB.MC", "ACS.MC", "GRF.MC", "FER.MC"]

if st.button('🚀 ESCANEAR RIESGO DEL IBEX'):
    col1, col2 = st.columns(2)
    
    with st.spinner('Analizando osciladores de mercado...'):
        for t in tickers:
            try:
                df = yf.download(t, period="3mo", progress=False)
                if not df.empty:
                    # Datos de precio
                    cierre = df['Close'].iloc[:, 0] if len(df['Close'].shape) > 1 else df['Close']
                    actual = float(cierre.iloc[-1])
                    media_20 = float(cierre.tail(20).mean())
                    
                    # Cálculo RSI
                    rsi_val = float(calcular_rsi(cierre).iloc[-1])
                    
                    # Determinación de Riesgo
                    if rsi_val > 70:
                        clase_riesgo = "riesgo-alto"
                        msg_riesgo = "🔥 SOBRECOMPRADO (Riesgo de caída)"
                    elif rsi_val < 30:
                        clase_riesgo = "riesgo-bajo"
                        msg_riesgo = "❄️ SOBREVENDIDO (Oportunidad rebote)"
                    else:
                        clase_riesgo = "riesgo-medio"
                        msg_riesgo = "⚖️ NEUTRO"

                    # Mostrar según tendencia
                    target_col = col1 if actual > media_20 else col2
                    
                    with target_col:
                        st.markdown(f"""
                            <div class="card {clase_riesgo}">
                                <span class="badge">RSI: {rsi_val:.1f}</span>
                                <h3 style="margin:5px 0;">{t} - {actual:.2f}€</h3>
                                <strong>{msg_riesgo}</strong><br>
                                <small>Tendencia: {"Alcista" if actual > media_20 else "Bajista"}</small>
                            </div>
                        """, unsafe_allow_html=True)
            except: continue
    st.success("¡Análisis de riesgo completado!")
