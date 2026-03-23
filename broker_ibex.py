import streamlit as st
import pandas as pd

st.set_page_config(page_title="Miguel Terminal PRO", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal Inteligente IBEX 35 - MIGUEL")

# --- 1. CALCULADORA (ACTIVA Y FIABLE) ---
with st.expander("💰 CALCULADORA DE OPERACIÓN RÁPIDA", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1: inv = st.number_input("Inversión (€):", value=1000, step=100)
    with c2: pre = st.number_input("Precio Acción (€):", value=10.0, step=0.1)
    with c3:
        obj = st.slider("Objetivo (%)", 1, 30, 10)
        st.metric("Beneficio Estimado", f"+{inv * (obj/100):.2f}€", f"{obj}%")

st.divider()

# --- 2. DICCIONARIO DE SECTORES (LOS 35) ---
sectores = {
    "🏦 BANCA": ["SAN", "BBVA", "CABK", "SAB", "BKT", "UNI"],
    "⚡ ENERGÍA": ["IBE", "REP", "NTGY", "ELE", "ENG", "REE", "SLBA"],
    "🏗️ IND/CONS": ["ITX", "ANA", "ACS", "FER", "ACX", "MTS", "IAG", "PUIG"],
    "📡 TECNOLOGÍA": ["TEF", "CLNX", "IDR", "AMS"],
    "🧬 OTROS": ["GRF", "ROVI", "COL", "MRL", "LOG", "AENA", "SCYR", "FDR", "MEL"]
}

st.sidebar.header("🎯 FILTROS DE MERCADO")
sector_sel = st.sidebar.multiselect("Elegir Sectores:", list(sectores.keys()), default=["🏦 BANCA"])

st.info("🚀 Sistema 'Anti-Bloqueo' activado. Haz clic en 'VER ANÁLISIS' para abrir el gráfico profesional de cada valor.")

# --- 3. PANEL DE CONTROL Y ANÁLISIS ---
for s in sector_sel:
    st.subheader(f"📂 Sector: {s}")
    cols = st.columns(3)
    for i, t in enumerate(sectores[s]):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"### {t}.MC")
                
                # Links de Inteligencia Directa
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    # Link a Google Finance (Gráfico, RSI y Previsiones)
                    url_g = f"https://www.google.com/finance/quote/{t}:BME"
                    st.link_button("📊 VER ANÁLISIS", url_g, use_container_width=True)
                with col_btn2:
                    # Link a Noticias de Bolsa
                    url_n = f"https://www.google.com/search?q={t}+noticias+bolsa&tbm=nws"
                    st.link_button("📰 NOTICIAS", url_n, use_container_width=True)
                
                # Semáforo Manual (Tu decisión final)
                st.selectbox("Tu Semáforo:", ["⚪ Pendiente", "🟢 COMPRA", "🔴 RIESGO"], key=f"sem_{t}")

st.divider()
st.caption("Terminal optimizada para Miguel. Datos de Google Finance sin bloqueos.")
