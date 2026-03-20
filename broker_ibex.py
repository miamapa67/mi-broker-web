import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Estratega Robot", layout="wide")

st.title("🤖 Mi Analista Estratega - IBEX & Wall Street")
st.write("Analizando tendencias con Medias Móviles (20 días)...")

tickers = ["SAN.MC", "TEF.MC", "ITX.MC", "BBVA.MC", "AAPL", "MSFT", "TSLA", "NVDA"]

try:
    # Descargamos datos de los últimos 40 días para calcular la media
    data = yf.download(tickers, period="40d")['Close']
    
    if not data.empty:
        st.subheader("📈 Análisis de Tendencias y Recomendación")
        
        # Creamos columnas para que se vea profesional (de 4 en 4)
        cols = st.columns(4)
        
        for i, ticker in enumerate(tickers):
            with cols[i % 4]:
                # Sacamos el precio actual y la media de los últimos 20 días
                precio_actual = data[ticker].iloc[-1]
                media_20 = data[ticker].tail(20).mean()
                
                # Lógica de tendencia
                if precio_actual > media_20:
                    recomendacion = "COMPRAR ✅"
                    color = "normal" # Verde en Streamlit
                    delta = f"Encima de media (+{((precio_actual/media_20)-1)*100:.2f}%)"
                else:
                    recomendacion = "VENDER ❌"
                    color = "inverse" # Rojo en Streamlit
                    delta = f"Debajo de media ({((precio_actual/media_20)-1)*100:.2f}%)"
                
                # Si es "nan" (mercado cerrado), avisamos
                if pd.isna(precio_actual):
                    st.metric(label=ticker, value="Cerrado")
                else:
                    st.metric(
                        label=f"{ticker} - {recomendacion}", 
                        value=f"{precio_actual:.2f}", 
                        delta=delta,
                        delta_color=color
                    )
        
        st.success("Análisis completado. Recuerda: esto es una ayuda técnica, no un consejo financiero legal.")
    else:
        st.error("No hay datos disponibles ahora mismo.")

except Exception as e:
    st.error(f"Error en el análisis: {e}")

st.write("---")
st.caption("Estrategia basada en Cruce de Media Móvil Simple (SMA20)")
