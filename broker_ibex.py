import streamlit as st
import yfinance as yf
import pandas as pd

# Configuración de página con tema oscuro por defecto
st.set_page_config(page_title="Analista Robot Pro", layout="wide")

# Estilo CSS de super lujo (con textos claros y fondo oscuro)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 15px; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-size: 36px; font-weight: 700; }
    [data-testid="stMetricLabel"] { color: #8b949e !important; font-size: 16px; }
    [data-testid="stMetricDelta"] { font-size: 18px; }
    .stTextInput>div>div>input { background-color: #161b22; color: white; border: 1px solid #30363d; }
    h1 { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Analista Robot Pro")

# Buscador con estilo oscuro
ticker = st.text_input("Introduce un Ticker (ej: NVDA, SAN.MC, TSLA):", value="SAN.MC").upper().strip()

if ticker:
    try:
        t = yf.Ticker(ticker)
        # Traemos datos de 1 año para una gráfica bonita
        data = t.history(period="1y")
        
        if not data.empty:
            precios = data['Close']
            actual = float(precios.iloc[-1])
            media_20 = float(precios.tail(20).mean())
            
            # Cálculo de señales
            distancia = ((actual/media_20)-1)*100
            es_alcista = actual > media_20
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                # Métrica con delta y textos claros
                st.metric(label=f"Precio Actual {ticker}", value=f"{actual:.2f}€", delta=f"{distancia:.2f}%")
                
                if es_alcista:
                    st.success("🎯 SEÑAL: COMPRA")
                else:
                    st.error("🚨 SEÑAL: VENTA")
                
                # Métrica secundaria más pequeña
                st.metric(label="Media 20 días", value=f"{media_20:.2f}€")

            with col2:
                # --- LA CLAVE ---
                # Usamos st.line_chart y especificamos color='red'
                st.line_chart(precios, color="#FF4B4B", use_container_width=True)
                st.caption(f"Evolución de {ticker} - Último año")
                
        else:
            st.warning("Buscando datos...")
    except Exception as e:
        # Mostramos el error real si Yahoo falla
        st.error(f"Error de conexión: {e}")
        
