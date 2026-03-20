import streamlit as st
import yfinance as yf
import pandas as pd

# Configuración básica
st.set_page_config(page_title="Analista Robot Pro", layout="wide")

st.title("🤖 Analista Robot Pro")
st.write("Si ves esto, ¡el robot por fin ha despertado!")

# Buscador ultra simple para probar
ticker = st.text_input("Introduce un Ticker (ej: SAN.MC):", value="SAN.MC").upper()

if ticker:
    try:
        data = yf.download(ticker, period="1mo")['Close']
        if not data.empty:
            st.metric("Precio Actual", f"{data.iloc[-1]:.2f}€")
            st.line_chart(data)
        else:
            st.warning("No hay datos para ese símbolo.")
    except Exception as e:
        st.error(f"Error: {e}")
