import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Monitor IBEX 35", layout="wide")

st.title("🇪🇸 Monitor en Tiempo Real: Los 35 del IBEX")
st.write("Analizando tendencia y recomendación para todo el selectivo español.")

# Lista oficial de los 35 tickers de Yahoo Finance para el IBEX
ibex_35 = [
    "ANA.MC", "ACS.MC", "ACG.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", 
    "BKT.MC", "BBVA.MC", "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", 
    "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC", "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", 
    "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC", "ROVI.MC", "SCYR.MC", 
    "SLR.MC", "TEF.MC", "UNI.MC"
]

try:
    # Descargamos datos de 40 días para la media móvil
    with st.spinner('Conectando con la Bolsa de Madrid...'):
        data = yf.download(ibex_35, period="40d")['Close']
    
    if not data.empty:
        # Layout en columnas (5 por fila en PC)
        cols = st.columns(5)
        
        # Diccionario para nombres más legibles (opcional, aquí usamos el Ticker)
        for i, ticker in enumerate(ibex_35):
            with cols[i % 5]:
                # Obtener último precio disponible (que no sea NaN)
                serie_precios = data[ticker].dropna()
                if not serie_precios.empty:
                    precio_actual = serie_precios.iloc[-1]
                    media_20 = serie_precios.tail(20).mean()
                    
                    # Lógica de inversión
                    subida = precio_actual > media_20
                    rec = "COMPRA" if subida else "VENTA"
                    color_flecha = "normal" if subida else "inverse"
                    pct = ((precio_actual/media_20)-1)*100
                    
                    st.metric(
                        label=f"{ticker.replace('.MC', '')} ({rec})",
                        value=f"{precio_actual:.3f}€",
                        delta=f"{pct:.2f}% vs media",
                        delta_color=color_flecha
                    )
                else:
                    st.caption(f"{ticker}: Sin datos")
        
        st.divider()
        st.success("✅ Todos los valores del IBEX 35 analizados correctamente.")
    else:
        st.error("No se pudo conectar con los datos del IBEX.")

except Exception as e:
    st.error(f"Error técnico: {e}")

st.caption("Estrategia: Tendencia alcista si Precio > Media Móvil 20 sesiones.")
        
