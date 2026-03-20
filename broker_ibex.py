import streamlit as st
import yfinance as yf
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Radar de Inversión Pro", layout="wide")

# --- ESTILO MEJORADO (TARJETAS CLARAS Y LEGIBLES) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    h1, h2, h3 { color: #ffffff !important; }
    
    /* Tarjetas del Radar (Fondo claro, texto negro) */
    [data-testid="stMetric"] {
        background-color: #f0f2f6; 
        border-radius: 15px;
        padding: 15px;
    }
    [data-testid="stMetricLabel"] { color: #111827 !important; font-weight: bold; }
    [data-testid="stMetricValue"] { color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📡 Radar de Oportunidades")

# --- SECCIÓN 1: EL RADAR ---
st.subheader("Análisis Automático de Favoritos")
favoritos = ["SAN.MC", "BBVA.MC", "TEF.MC", "IBE.MC", "TSLA"]
cols = st.columns(len(favoritos))

for i, f in enumerate(favoritos):
    try:
        d = yf.download(f, period="1mo", progress=False)
        if not d.empty:
            p_actual = float(d['Close'].iloc[-1])
            p_media = float(d['Close'].tail(20).mean())
            with cols[i]:
                st.metric(label=f, value=f"{p_actual:.2f}€")
                if p_actual > p_media: st.success("🟢 COMPRA")
                else: st.error("🔴 VENTA")
    except: continue

st.divider()

# --- SECCIÓN 2: BUSCADOR CON GRÁFICA CORREGIDA ---
st.subheader("🔍 Analizador Detallado")
ticker = st.text_input("Introduce un Ticker:", value="BBVA.MC").upper().strip()

if ticker:
    try:
        # Descargamos los datos
        data = yf.download(ticker, period="1y", progress=False)
        if not data.empty:
            precios = data['Close']
            actual = float(precios.iloc[-1])
            
            c1, c2 = st.columns([1, 3])
            with c1:
                st.metric(label=f"Precio {ticker}", value=f"{actual:.2f}€")
                # Botón de señal
                p_media = float(precios.tail(20).mean())
                if actual > p_media: st.success("🎯 SEÑAL: COMPRA")
                else: st.error("🚨 SEÑAL: VENTA")
            
            with c2:
                # --- AQUÍ ESTÁ EL CAMBIO CLAVE ---
                # Forzamos a que la gráfica no empiece en 0
                st.line_chart(precios, color="#FF4B4B")
                st.caption("Evolución últimos 12 meses (Datos ajustados)")
    except:
        st.error("Conectando...")
