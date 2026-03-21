import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Miguel Terminal", layout="wide")
st.title("🏹 Terminal IBEX - MIGUEL")

# Solo 3 valores para no despertar al servidor
test_tickers = ["SAN.MC", "ITX.MC", "TEF.MC"]

if st.button('🚀 INTENTO DE CONEXIÓN RÁPIDA'):
    with st.spinner('Pidiendo datos mínimos...'):
        for t in test_tickers:
            try:
                # Pedimos solo 5 días de datos (lo mínimo posible)
                df = yf.download(t, period="5d", progress=False)
                if not df.empty:
                    precio = float(df['Close'].iloc[-1])
                    st.success(f"✅ {t}: {precio:.2f}€ - ¡CONEXIÓN ÉXITOSA!")
            except Exception as e:
                st.error(f"❌ {t} sigue bloqueado.")

st.divider()
st.info("💡 Si sale el error rosa, espera unos minutos. Yahoo Finance a veces bloquea las IPs de servidores gratuitos como Streamlit por exceso de tráfico.")
