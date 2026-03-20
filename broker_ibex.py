import streamlit as st
import yfinance as yf
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Radar de Inversión Pro", layout="wide")

# Estilo CSS para que se vea impecable
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 12px; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-size: 28px; }
    h1, h2, h3 { color: white !important; }
    .stDataFrame { background-color: #161b22; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📡 Radar de Oportunidades")

# --- SECCIÓN 1: EL RADAR AUTOMÁTICO ---
st.subheader("Análisis Automático de Favoritos")
favoritos = ["SAN.MC", "BBVA.MC", "TEF.MC", "IBE.MC", "TSLA"]

cols_radar = st.columns(len(favoritos))
resultados_radar = []

for i, f en enumerate(favoritos):
    try:
        # Descarga rápida para el radar
        d = yf.download(f, period="1mo", progress=False)
        if not d.empty:
            p_actual = float(d['Close'].iloc[-1])
            p_media = float(d['Close'].tail(20).mean())
            estado = "🟢 COMPRA" if p_actual > p_media else "🔴 VENTA"
            
            with cols_radar[i]:
                st.metric(label=f, value=f"{p_actual:.2f}€")
                if "COMPRA" in estado:
                    st.caption(f"✅ {estado}")
                else:
                    st.caption(f"⚠️ {estado}")
            
            resultados_radar.append({"Ticker": f, "Precio": f"{p_actual:.2f}€", "Señal": estado})
    except:
        continue

st.divider()

# --- SECCIÓN 2: BUSCADOR INDIVIDUAL (Tu diseño favorito) ---
st.subheader("🔍 Analizador Detallado")
ticker = st.text_input("Introduce cualquier Ticker:", value="SAN.MC").upper().strip()

if ticker:
    try:
        data = yf.download(ticker, period="1y", progress=False)
        if not data.empty:
            precios = data['Close']
            actual = float(precios.iloc[-1])
            media_20 = float(precios.tail(20).mean())
            distancia = ((actual/media_20)-1)*100
            
            c1, c2 = st.columns([1, 3])
            with c1:
                st.metric(label=f"Precio Actual {ticker}", value=f"{actual:.2f}€", delta=f"{distancia:.2f}%")
                if actual > media_20:
                    st.success("🎯 SEÑAL: COMPRA")
                else:
                    st.error("🚨 SEÑAL: VENTA")
                st.info(f"Media 20d: {media_20:.2f}€")
            with c2:
                # Tu línea roja favorita
                st.line_chart(precios, color="#FF4B4B")
    except:
        st.error("Esperando conexión...")
        
