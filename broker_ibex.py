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

    
    
       # Formato ultra-compatible (evita el error de antes)
        st.write("### Lista de Cotizaciones")
        for ticker, precio in data.tail(1).T.iloc[:, 0].items():
            st.metric(label=ticker, value=f"{precio:.2f}") 
        
        st.success("Datos actualizados correctamente.")
    else:
        st.error("No se han recibido datos. Prueba a recargar la página.")

except Exception as e:
    st.error(f"Error técnico: {e}")

st.write("---")
st.caption("Datos proporcionados por Yahoo Finance • 2026")
