import streamlit as st
import yfinance as yf
import pandas as pd

# Configuración de página con tema oscuro por defecto
st.set_page_config(page_title="Analista Robot Pro", layout="wide")

# Estilo CSS para que se vea de lujo
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_allow_html=True)

st.title("🤖 Analista Robot Pro")

# Buscador
ticker = st.text_input("Introduce un Ticker (ej: NVDA, SAN.MC, TSLA):", value="SAN.MC").upper().strip()

if ticker:
    try:
        t = yf.Ticker(ticker)
        # Traemos un poco más de historial para que la gráfica luzca
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
                st.metric(label=f"Precio Actual {ticker}", value=f"{actual:.2f}€", delta=f"{distancia:.2f}%")
                
                if es_alcista:
                    st.success("🎯 SEÑAL: COMPRA")
                    st.write("📈 El precio está en racha alcista.")
                else:
                    st.error("🚨 SEÑAL: VENTA")
                    st.write("📉 El precio está en racha bajista.")
                
                st.info(f"Media 20 días: {media_20:.2f}€")

            with col2:
                # Gráfica de área moderna (Streamlit la hace degradada automáticamente)
                st.area_chart(precios, use_container_width=True)
                st.caption(f"Evolución de {ticker} - Último año")
                
        else:
            st.warning("Buscando datos...")
    except:
        st.error("Yahoo está saturado. Espera 10 segundos.")
