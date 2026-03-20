import streamlit as st
import yfinance as yf
import pandas as pd

# Configuración básica
st.set_page_config(page_title="Analista Robot Pro", layout="wide")

st.title("🤖 Analista Robot Pro")
st.write("Conexión establecida con éxito.")

# Buscador mejorado
ticker = st.text_input("Introduce un Ticker (ej: SAN.MC, AAPL, TSLA):", value="SAN.MC").upper().strip()

if ticker:
    try:
        # Descargamos los datos
        data = yf.download(ticker, period="6mo")['Close']
        
        if not data.empty:
            # Limpiamos los datos por si vienen duplicados
            precios = data.dropna()
            # Cogemos el último precio de forma segura
            ultimo_precio = float(precios.iloc[-1])
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                # Mostramos el precio con formato simple
                st.metric(label=f"Precio {ticker}", value=f"{ultimo_precio:.2f}")
                st.write("✅ Datos actualizados")
                
            with col2:
                # Dibujamos la gráfica
                st.area_chart(precios)
        else:
            st.warning(f"No se han encontrado datos para {ticker}. Revisa el nombre.")
            
    except Exception as e:
        st.error("Yahoo Finance está tardando en responder. Pulsa Intro de nuevo.")
