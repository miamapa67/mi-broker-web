import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Miguel Terminal PRO", layout="wide")

# --- 1. LISTA Y DATOS ---
ibex_35 = ["ANA.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", "MRL.MC", "BBVA.MC", "BKT.MC", "CABK.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC", "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "NTGY.MC", "PUIG.MC", "RED.MC", "ROVI.MC", "SAB.MC", "SAN.MC", "SCYR.MC", "TEF.MC", "UNI.MC"]

@st.cache_data(ttl=600)
def cargar_datos_totales(tickers):
    return yf.download(tickers, period="6mo")['Close']

# --- INTERFAZ PRINCIPAL ---
st.title("🚀 Terminal Inteligente IBEX 35")

# Selector de Acción (El motor que cambia todo)
ticker_seleccionado = st.selectbox("🔍 SELECCIONA UNA EMPRESA PARA ANALIZAR:", ibex_35)

try:
    # Obtener datos de la empresa seleccionada
    datos_completos = cargar_datos_totales(ibex_35)
    precios_ticker = datos_completos[ticker_seleccionado].dropna()
    
    # 2. CÁLCULO DE RSI
    delta = precios_ticker.diff()
    ganancia = (delta.where(delta > 0, 0)).rolling(14).mean()
    perdida = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rsi = 100 - (100 / (1 + ganancia/perdida))
    u_rsi = rsi.iloc[-1]
    u_precio = precios_ticker.iloc[-1]

    # --- 3. DISEÑO DE FICHA INDIVIDUAL ---
    st.divider()
    
    # Fila de Cabecera: Precio y Riesgo
    c1, c2, c3 = st.columns(3)
    c1.metric("Precio Actual", f"{u_precio:.2f} €")
    c2.metric("RSI (14d)", f"{u_rsi:.2f}")
    
    if u_rsi < 35:
        c3.success("VALORACIÓN: COMPRA ✅")
    elif u_rsi > 65:
        c3.error("VALORACIÓN: RIESGO ⚠️")
    else:
        c3.info("VALORACIÓN: NEUTRO ⚪")

    # Fila de Gráfico y Noticias
    col_grafico, col_noticias = st.columns([2, 1])

    with col_grafico:
        st.subheader(f"📈 Evolución de {ticker_seleccionado}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=precios_ticker.index, y=precios_ticker, mode='lines', name='Precio', line=dict(color='#007bff')))
        fig.update_layout(template="plotly_white", height=400, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_noticias:
        st.subheader("📰 Noticias Recientes")
        obj_ticker = yf.Ticker(ticker_seleccionado)
        noticias = obj_ticker.news[:4] # 4 noticias principales
        if noticias:
            for n in noticias:
                st.markdown(f"**[{n['title']}]({n['link']})**")
                st.caption(f"Fuente: {n['publisher']}")
                st.write("---")
        else:
            st.write("No hay noticias recientes para este valor.")

except Exception as e:
    st.error(f"Error cargando ficha: {e}")

# Sidebar con resumen rápido
with st.sidebar:
    st.header("📊 Resumen del Mercado")
    st.write("Usa el buscador central para ver el análisis detallado de cada empresa.")
