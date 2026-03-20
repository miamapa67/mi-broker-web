import streamlit as st
import yfinance as yf
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Mi Analista Robot", layout="wide")

st.title("🤖 Mi Analista Robot - IBEX & Wall Street")
st.write("Analizando los mercados en tiempo real...")

# Lista de acciones
tickers = ["SAN.MC", "TEF.MC", "ITX.MC", "BBVA.MC", "AAPL", "MSFT", "TSLA"]

try:
    # Descargamos datos
    with st.spinner('Consultando a la bolsa...'):
        data = yf.download(tickers, period="1d")['Close']
    
    if not data.empty:
        st.subheader("📊 Resumen de Precios")
        # Mostramos una tabla bonita
        df_precios = data.tail(1).T
        df_precios.columns = ['Precio Actual']
        st.dataframe(df_precios, use_container_width=True)
        
        st.success("Datos actualizados correctamente.")
    else:
        st.error("No se han recibido datos. Prueba a recargar la página.")

except Exception as e:
    st.error(f"Error técnico: {e}")

st.write("---")
st.caption("Datos proporcionados por Yahoo Finance • 2026")
