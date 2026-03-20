import streamlit as st
import yfinance as yf
import pandas as pd

# Configuración para móvil y PC
st.set_page_config(page_title="Analista Robot Pro", layout="wide")

st.title("🤖 Analista Robot Pro")

# Buscador de acciones
ticker = st.text_input("Introduce Ticker (ej: SAN.MC, BBVA.MC, NVDA):", value="SAN.MC").upper().strip()

if ticker:
    try:
        # Pedimos datos de los últimos 6 meses
        t = yf.Ticker(ticker)
        data = t.history(period="6mo")
        
        if not data.empty:
            # Cálculos del Semáforo
            precio_actual = float(data['Close'].iloc[-1])
            media_20 = float(data['Close'].tail(20).mean()) # Media de los últimos 20 días
            
            # Columnas para el diseño
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.metric(label="Precio Actual", value=f"{precio_actual:.2f}€")
                
                # Lógica del Semáforo
                if precio_actual > media_20:
                    st.success("🟢 SEÑAL: COMPRA")
                    st.write("El precio está en racha alcista.")
                else:
                    st.error("🔴 SEÑAL: VENTA")
                    st.write("El precio está en racha bajista.")
                
                distancia = ((precio_actual / media_20) - 1) * 100
                st.info(f"Distancia a la media: {distancia:.2f}%")
            
            with col2:
                # Gráfica interactiva
                st.area_chart(data['Close'])
                st.caption("Evolución de los últimos 6 meses")
                
        else:
            st.warning("No hay datos. Asegúrate de poner el punto en las españolas (ej: TEF.MC)")
            
    except Exception as e:
        st.error("Yahoo está saturado. Espera 10 segundos y pulsa Intro.")
