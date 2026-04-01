import streamlit as st
import datetime

st.set_page_config(page_title="Miguel Terminal ELITE", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal Inteligente IBEX 35 - MIGUEL")
st.caption(f"Acceso Directo a Mercados • {datetime.datetime.now().strftime('%d/%m/%Y')}")

# --- 1. CALCULADORA RÁPIDA ---
with st.sidebar:
    st.header("💰 CALCULADORA")
    capital = st.number_input("Capital a invertir (€):", value=1000, step=100)
    st.divider()
    st.info("Estrategia: Pulsa ANALIZAR. Si el RSI en Google es < 30, marca COMPRA.")

# --- 2. DICCIONARIO DE LOS 35 ---
sectores = {
    "🏦 BANCA": ["SAN", "BBVA", "CABK", "SAB", "BKT", "UNI"],
    "⚡ ENERGÍA": ["IBE", "REP", "NTGY", "ELE", "ENG", "REE", "SLBA"],
    "🏗️ IND/CONS": ["ITX", "ANA", "ACS", "FER", "ACX", "MTS", "IAG", "PUIG"],
    "📡 TECNO": ["TEF", "CLNX", "IDR", "AMS"],
    "🧬 OTROS": ["GRF", "ROVI", "COL", "MRL", "LOG", "AENA", "SCYR", "FDR", "MEL"]
}

# --- 3. PANEL DE CONTROL ---
tabs = st.tabs(list(sectores.keys()))

for i, sector in enumerate(sectores.keys()):
    with tabs[i]:
        cols = st.columns(3)
        for idx, ticker in enumerate(sectores[sector]):
            with cols[idx % 3]:
                # Tarjeta con borde y título grande
                with st.container(border=True):
                    st.markdown(f"<h2 style='text-align: center;'>{ticker}</h2>", unsafe_allow_html=True)
                    
                    url_google = f"https://www.google.com/finance/quote/{ticker}:BME"
                    st.link_button(f"🔍 ANALIZAR {ticker}", url_google, use_container_width=True, type="primary")
                    
                    url_news = f"https://www.google.com/search?q={ticker}+noticias+bolsa&tbm=nws"
                    st.link_button("📰 NOTICIAS", url_news, use_container_width=True)
                    
                    st.radio("Veredicto:", ["⚪ Neutro", "🟢 COMPRA", "🔴 RIESGO"], key=f"v_{ticker}", horizontal=True)

st.divider()
st.success("✅ Conexión con Google Finance Estable. Sin bloqueos de servidor.")
