import streamlit as st
import yfinance as yf
import pandas as pd

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Miguel Terminal PRO", layout="wide")

st.title("🚀 Terminal Inteligente IBEX 35 - MIGUEL")

# 2. LISTA ACTUALIZADA (La que ya tienes)
ibex_35 = [
    "ANA.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", 
    "MRL.MC", "BBVA.MC", "BKT.MC", "CABK.MC", "ENG.MC", 
    "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", 
    "IBE.MC", "ITX.MC", "IDR.MC", "COL.MC", "LOG.MC", 
    "MAP.MC", "MEL.MC", "NTGY.MC", "PUIG.MC", "RED.MC", 
    "ROVI.MC", "SAB.MC", "SAN.MC", "SCYR.MC", "TEF.MC", 
    "UNI.MC"
]

# 3. SIDEBAR
with st.sidebar:
    st.header("💰 CALCULADORA")
    capital = st.number_input("Inversión (€):", value=1000)
    st.divider()
    st.success("🟢 COMPRA: RSI < 35")
    st.error("🔴 RIESGO: RSI > 65")

# 4. MOTOR DE ANÁLISIS (Simplificado para que no se cuelgue)
st.subheader("Estado del Mercado")

@st.cache_data(ttl=600) # Guarda los datos 10 minutos para que vaya rápido
def cargar_datos():
    # Descarga solo el precio de cierre del último mes
    df = yf.download(ibex_35, period="1mo")['Close']
    return df

try:
    datos = cargar_datos()
    st.write("Datos actualizados correctamente.")
    st.dataframe(datos.tail()) # Muestra las últimas filas para probar
except Exception as e:
    st.error(f"Error al conectar con Yahoo Finance: {e}")
