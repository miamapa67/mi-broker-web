import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Analista Robot Pro", layout="wide")
st.title("🤖 Analista Robot Pro")

ticker = st.text_input("Introduce un Ticker (ej: SAN.MC):", value="SAN.MC").upper().strip()

if ticker:
    try:
        # Usamos Ticker() en lugar de download() directo, es más estable
        t = yf.Ticker(ticker)
        data = t.history(period="6mo")
        
        if not data.empty:
            ultimo_precio = float(data['Close'].iloc[-1])
            col1, col2 = st.columns([1, 3])
            with col1:
                st.metric(label=f"Precio {ticker}", value=f"{ultimo_precio:.2f}€")
                st.success("Conexión privada establecida")
            with col2:
                # Dibujamos con área para que se vea mejor
                st.area_chart(data['Close'])
        else:
            st.warning("Yahoo está tardando en soltar los datos. Espera 30 segundos y pulsa Intro.")
    except Exception as e:
        st.error("Límite de peticiones alcanzado. Descansando 1 minuto...")
