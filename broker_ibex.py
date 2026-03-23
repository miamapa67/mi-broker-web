import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Miguel Terminal Inmune", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal Inteligente IBEX 35 - MIGUEL")

# --- LISTA COMPLETA CON SECTORES ---
sectores = {
    "Banca": ["SAN", "BBVA", "CABK", "SAB", "BKT", "UNI"],
    "Energía": ["IBE", "REP", "NTGY", "ELE", "ENG", "REE", "SLBA"],
    "Ind. y Consumo": ["ITX", "ANA", "ACS", "FER", "ACX", "MTS", "IAG", "PUIG"],
    "Tecno y Telco": ["TEF", "CLNX", "IDR", "AMS"],
    "Otros": ["GRF", "ROVI", "COL", "MRL", "LOG", "AENA", "SCYR", "FDR", "MEL"]
}

# Sidebar con filtros
st.sidebar.header("🎯 Filtros de Mercado")
sector_sel = st.sidebar.multiselect("Filtrar Sectores:", list(sectores.keys()), default=list(sectores.keys()))

st.info("💡 Debido a los bloqueos de Yahoo, hemos activado el Panel de Análisis Directo de Google Finance. ¡Cero errores!")

# --- GENERAR PANEL POR SECTORES ---
for sec in sector_sel:
    st.subheader(f"📂 Sector: {sec}")
    cols = st.columns(3)
    for i, t in enumerate(sectores[sec]):
        with cols[i % 3]:
            # Creamos un diseño tipo "Tarjeta de Trader"
            with st.container(border=True):
                st.markdown(f"### {t}.MC")
                # Enlaces de inteligencia directa
                c1, c2 = st.columns(2)
                with c1:
                    # Enlace a Google Finance (Gráfico de velas + RSI + Noticias)
                    url_g = f"https://www.google.com/finance/quote/{t}:BME"
                    st.link_button("📊 Ver Gráfico/RSI", url_g, use_container_width=True)
                with c2:
                    # Enlace a Noticias
                    url_n = f"https://www.google.com/search?q={t}+noticias+bolsa&tbm=nws"
                    st.link_button("📰 Noticias", url_n, use_container_width=True)
                
                # Semáforo Manual (Para que tú decidas según lo que ves en el gráfico)
                st.selectbox(f"Semáforo {t}", ["⚪ Neutro", "🟢 OPORTUNIDAD", "🔴 RIESGO"], key=f"sem_{t}")

st.divider()

# --- CALCULADORA QUE NUNCA FALLA ---
st.subheader("💰 Calculadora Operativa")
col_c1, col_c2 = st.columns(2)
with col_c1:
    inv = st.number_input("Inversión (€):", value=1000, step=100)
    ent = st.number_input("Precio de entrada (€):", value=10.0, step=0.1)
with col_c2:
    obj = st.slider("Objetivo de subida (%)", 1, 30, 10)
    gan = inv * (obj / 100)
    st.metric("Beneficio Estimado", f"+{gan:.2f}€", f"{obj}%")
