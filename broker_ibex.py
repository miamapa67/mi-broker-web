import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go # Para gráficos más profesionales

st.set_page_config(page_title="Miguel Terminal PRO", layout="wide")

# --- ESTILOS ---
st.markdown("""<style>.main { background-color: #f5f7f9; }</style>""", unsafe_allow_html=True)

st.title("🚀 Terminal Inteligente IBEX 35 - MIGUEL")

# --- 1. LISTA Y DATOS ---
ibex_35 = ["ANA.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", "MRL.MC", "BBVA.MC", "BKT.MC", "CABK.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC", "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "NTGY.MC", "PUIG.MC", "RED.MC", "ROVI.MC", "SAB.MC", "SAN.MC", "SCYR.MC", "TEF.MC", "UNI.MC"]

@st.cache_data(ttl=600)
def cargar_datos(tickers):
    return yf.download(tickers, period="6mo")['Close']

try:
    df_precios = cargar_datos(ibex_35)
    
    # --- 2. CÁLCULO DE RSI Y SEÑALES ---
    resumen = []
    for ticker in ibex_35:
        if ticker in df_precios.columns:
            p = df_precios[ticker].dropna()
            if len(p) > 14:
                delta = p.diff(); g = (delta.where(delta > 0, 0)).rolling(14).mean(); l = (-delta.where(delta < 0, 0)).rolling(14).mean()
                rsi = 100 - (100 / (1 + g/l))
                u_p = p.iloc[-1]; u_r = rsi.iloc[-1]
                est = "🟢 COMPRA" if u_r < 35 else ("🔴 RIESGO" if u_r > 65 else "⚪ NEUTRO")
                resumen.append({"Ticker": ticker, "Precio": u_p, "RSI": u_r, "Estado": est})
    
    df_resumen = pd.DataFrame(resumen)

    # --- 3. DISEÑO DE LA APP (COLUMNAS) ---
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("💡 Señales Actuales")
        st.dataframe(df_resumen, use_container_width=True, height=400)
        
        # --- ESTADO DE RIESGO GLOBAL ---
        riesgo_medio = df_resumen['RSI'].mean()
        st.metric("RSI Medio IBEX", f"{riesgo_medio:.2f}", delta_color="inverse")
        if riesgo_medio > 60: st.error("⚠️ MERCADO SOBRECALENTADO")
        elif riesgo_medio < 40: st.success("📉 OPORTUNIDAD GENERAL")

    with col2:
        # --- ESQUEMA GRÁFICO ANIMADO (Selector) ---
        st.subheader("📈 Análisis Gráfico")
        seleccionado = st.selectbox("Selecciona acción para gráfico:", ibex_35)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_precios.index, y=df_precios[seleccionado], mode='lines', name='Precio'))
        fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=20, b=20), height=300)
        st.plotly_chart(fig, use_container_width=True)

        # --- SECCIÓN DE NOTICIAS ---
        st.subheader("📰 Últimas Noticias")
        ticker_news = yf.Ticker(seleccionado)
        news = ticker_news.news[:3] # Cogemos las 3 últimas
        for n in news:
            with st.expander(n['title']):
                st.write(f"Fuente: {n['publisher']}")
                st.markdown(f"[Leer noticia completa]({n['link']})")

except Exception as e:
    st.error(f"Error: {e}")

# --- SIDEBAR ---
with st.sidebar:
    st.header("💰 CALCULADORA")
    capital = st.number_input("Inversión (€):", value=1000)
    st.info(f"Con {capital}€ podrías diversificar en las 🟢 COMPRA.")
