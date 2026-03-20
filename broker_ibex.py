import streamlit as st
import yfinance as yf
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Analista Robot Pro", layout="wide")

# Estilo CSS de lujo (Copia y pega este bloque sobre el anterior)
st.markdown("""
    <style>
    .stMetric { background-color: #1e2229; border: 1px solid #3e4451; padding: 20px; border-radius: 15px; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-size: 32px; }
    [data-testid="stMetricLabel"] { color: #8b949e !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Analista Robot Pro")

# Buscador
ticker = st.text_input("Introduce un Ticker (ej: NVDA, SAN.MC, TSLA):", value="SAN.MC").upper().strip()

if ticker:
    try:
        t = yf.Ticker(ticker)
        data = t.history(period="1y")
        
        if not data.empty:
            precios = data['Close']
            actual = float(precios.iloc[-1])
            media_20 = float(precios.tail(20).mean())
            
            distancia = ((actual/media_20)-1)*100
            es_alcista = actual > media_20
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.metric(label=f"Precio Actual {ticker}", value=f"{actual:.2f}€", delta=f"{distancia:.2f}%")
                
                if es_alcista:
                    st.success("🎯 SEÑAL: COMPRA")
                else:
                    st.error("🚨 SEÑAL: VENTA")
                
                st.info(f"Media 20 días: {media_20:.2f}€")

            with col2:
                # Gráfica de área moderna
                st.area_chart(precios)
                
        else:
            st.warning("Buscando datos...")
    except:
        st.error("Yahoo está descansando. Espera 10 segundos.")
