import streamlit as st
import yfinance as yf
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Radar de Inversión Pro", layout="wide")

# --- NUEVO ESTILO CSS PARA MÁXIMA LEGIBILIDAD ---
st.markdown("""
    <style>
    /* Fondo general oscuro para que resalten las tarjetas */
    .stApp { background-color: #0e1117; }
    
    /* Títulos principales en blanco puro */
    h1, h2, h3 { color: #ffffff !important; font-weight: 700; }
    
    /* --- ESTILO DE LAS TARJETAS DEL RADAR (CLARAS) --- */
    [data-testid="stMetric"] {
        background-color: #f0f2f6; /* Fondo gris muy claro */
        border: 1px solid #d1d5db;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Texto de la etiqueta (Ticker) en negro */
    [data-testid="stMetricLabel"] {
        color: #111827 !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    
    /* Texto del valor (Precio) en negro */
    [data-testid="stMetricValue"] {
        color: #000000 !important;
        font-size: 32px !important;
        font-weight: 800 !important;
    }
    
    /* Ajuste para el delta (porcentaje) si lo hubiera */
    [data-testid="stMetricDelta"] {
        font-weight: 700 !important;
    }

    /* Estilo para el buscador individual (mantenemos oscuro para contraste) */
    .stTextInput>div>div>input { background-color: #161b22; color: white; border: 1px solid #30363d; }
    
    </style>
    """, unsafe_allow_html=True)

st.title("📡 Radar de Oportunidades")

# --- SECCIÓN 1: EL RADAR AUTOMÁTICO (Súper Legible) ---
st.subheader("Análisis Automático de Favoritos")
favoritos = ["SAN.MC", "BBVA.MC", "TEF.MC", "IBE.MC", "TSLA"]

cols_radar = st.columns(len(favoritos))

for i, f in enumerate(favoritos):
    try:
        # Descarga rápida
        d = yf.download(f, period="1mo", progress=False)
        if not d.empty:
            p_actual = float(d['Close'].iloc[-1])
            p_media = float(d['Close'].tail(20).mean())
            
            with cols_radar[i]:
                # Mostramos la métrica con el nuevo estilo claro
                st.metric(label=f"Ticker: {f}", value=f"{p_actual:.2f}€")
                
                # Semáforo visual debajo de la tarjeta
                if p_actual > p_media:
                    st.success("🟢 COMPRA")
                else:
                    st.error("🔴 VENTA")
    except:
        continue

st.divider()

# --- SECCIÓN 2: BUSCADOR INDIVIDUAL ---
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
                # Métrica individual (mantenemos estilo claro aquí también para consistencia)
                st.metric(label=f"Precio Actual {ticker}", value=f"{actual:.2f}€", delta=f"{distancia:.2f}%")
                
                if actual > media_20:
                    st.success("🎯 SEÑAL: COMPRA")
                else:
                    st.error("🚨 SEÑAL: VENTA")
            with c2:
                # Tu línea roja favorita
                st.line_chart(precios, color="#FF4B4B")
    except:
        st.error("Conectando con Yahoo...")
