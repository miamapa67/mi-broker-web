import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Monitor Financiero", layout="wide")

# --- BARRA LATERAL (Buscador) ---
with st.sidebar:
    st.header("🔎 Buscador de Acciones")
    ticker_buscado = st.text_input("Símbolo (ej: BBVA.MC, AAPL):", value="").upper().strip()
    btn_buscar = st.button("Analizar Acción")

st.title("🤖 Tu Analista Robot Inteligente")

# --- LÓGICA DEL BUSCADOR ---
if btn_buscar and ticker_buscado:
    st.write("---")
    st.subheader(f"📊 Análisis Detallado: {ticker_buscado}")
    try:
        # Descargamos datos
        data_buscada = yf.download(ticker_buscado, period="60d")['Close']
        if not data_buscada.empty:
            actual = data_buscada.iloc[-1]
            media = data_buscada.tail(20).mean()
            es_alcista = actual > media
            
            # Mostrar resultado
            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric(label="Precio Actual", value=f"{actual:.2f}", delta=f"{((actual/media)-1)*100:.2f}% vs media")
                status = "COMPRA ✅" if es_alcista else "VENTA ❌"
                color = "green" if es_alcista else "red"
                st.markdown(f"### Recomendación:")
                st.markdown(f"### **<span style='color:{color}'>{status}</span>**", unsafe_allow_html=True)
            with col2:
                st.line_chart(data_buscada)
        else:
            st.error("No se encontró el símbolo. Recuerda el .MC para España.")
    except Exception as e:
        st.error(f"Error: {e}")

st.write("---")
st.subheader("🇪🇸 Resumen Semáforo IBEX 35")

# Lista de los 35 para el monitor de abajo
ibex_35 = ["ANA.MC", "ACS.MC", "ACG.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", "BKT.MC", "BBVA.MC", "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC", "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC", "ROVI.MC", "SCYR.MC", "SLR.MC", "TEF.MC", "UNI.MC"]

try:
    data_ibex = yf.download(ibex_35, period="40d")['Close']
    if not data_ibex.empty:
        cols = st.columns(5)
        for i, ticker in enumerate(ibex_35):
            with cols[i % 5]:
                serie = data_ibex[ticker].dropna()
                if not serie.empty:
                    act = serie.iloc[-1]
                    med = serie.tail(20).mean()
                    alc = act > med
                    st.markdown(f"**{ticker.replace('.MC','')}**: <span style='color:{'green' if alc else 'red'}'>{'COMPRA' if alc else 'VENTA'}</span>", unsafe_allow_html=True)
                    st.metric(label="Precio", value=f"{act:.2f}€", delta=f"{((act/med)-1)*100:.1f}%")
except:
    st.write("Cargando monitor...")
