import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Miguel Terminal ELITE", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal Inteligente IBEX 35 - MIGUEL")
st.caption(f"Acceso Directo a Mercados • {datetime.datetime.now().strftime('%d/%m/%Y')}")

# --- 1. CALCULADORA RÁPIDA (SIEMPRE ACTIVA) ---
with st.sidebar:
    st.header("💰 CALCULADORA")
    capital = st.number_input("Capital a invertir (€):", value=1000, step=100)
    st.divider()
    st.info("Estrategia: Al hacer clic en un valor, revisa el RSI en Google. Si está por debajo de 30, es una oportunidad de compra.")

# --- 2. DICCIONARIO DE LOS 35 POR SECTORES ---
sectores = {
    "🏦 BANCA": ["SAN", "BBVA", "CABK", "SAB", "BKT", "UNI"],
    "⚡ ENERGÍA": ["IBE", "REP", "NTGY", "ELE", "ENG", "REE", "SLBA"],
    "🏗️ IND/CONS": ["ITX", "ANA", "ACS", "FER", "ACX", "MTS", "IAG", "PUIG"],
    "📡 TECNO": ["TEF", "CLNX", "IDR", "AMS"],
    "🧬 OTROS": ["GRF", "ROVI", "COL", "MRL", "LOG", "AENA", "SCYR", "FDR", "MEL"]
}

# --- 3. PANEL DE CONTROL ---
st.subheader("📊 Radar de Oportunidades (35 Valores)")

# Creamos pestañas para que no sea una lista infinita
tabs = st.tabs(list(sectores.keys()))

for i, sector in enumerate(sectores.keys()):
    with tabs[i]:
        cols = st.columns(3)
        for idx, ticker in enumerate(sectores[sector]):
            with cols[idx % 3]:
                with st.container(border=True):
                    st.markdown(f"### {ticker}.MC")
                    
                    # Botón de Oro: Análisis en Google Finance
                    # Esto abre el gráfico profesional, RSI y noticias sin bloqueos
                    url_google = f"https://www.google.com/finance/quote/{ticker}:BME"
                    st.link_button(f"🔍 ANALIZAR {ticker}", url_google, use_container_width=True, type="primary")
                    
                    # Botón de Noticias
                    url_news = f"https://www.google.com/search?q={ticker}+noticias+bolsa&tbm=nws"
                    st.link_button("📰 NOTICIAS", url_news, use_container_width=True)
                    
                    # Semáforo de Usuario
                    st.radio("Tu veredicto:", ["⚪ Neutro", "🟢 COMPRA", "🔴 RIESGO"], key=f"v_{ticker}", horizontal=True)

st.divider()
st.warning("⚠️ Nota: Debido a los bloqueos de Yahoo, esta terminal te conecta directamente a Google Finance para garantizar datos en tiempo real sin errores.")
