import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Monitor IBEX 35", layout="wide")

st.title("🇪🇸 Semáforo IBEX 35: Señales de Compra/Venta")
st.write("Análisis visual de tendencia: Verde = Fuerte (Compra) | Rojo = Débil (Venta)")

# Lista oficial de los 35
ibex_35 = [
    "ANA.MC", "ACS.MC", "ACG.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", 
    "BKT.MC", "BBVA.MC", "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", 
    "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC", "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", 
    "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC", "ROVI.MC", "SCYR.MC", 
    "SLR.MC", "TEF.MC", "UNI.MC"
]

try:
    with st.spinner('Actualizando precios de Madrid...'):
        # Descargamos 40 días para asegurar que la media de 20 sea sólida
        data = yf.download(ibex_35, period="40d")['Close']
    
    if not data.empty:
        # Layout en columnas (5 por fila en PC, adaptado en móvil)
        cols = st.columns(5)
        
        for i, ticker in enumerate(ibex_35):
            with cols[i % 5]:
                serie = data[ticker].dropna()
                if not serie.empty:
                    actual = serie.iloc[-1]
                    media = serie.tail(20).mean()
                    
                    # CÁLCULO DE TENDENCIA (Lógica de Estrategia)
                    es_alcista = actual > media
                    status = "COMPRA" if es_alcista else "VENTA"
                    color_status = "green" if es_alcista else "red"
                    # 'normal' pone el delta en verde, 'inverse' en rojo
                    color_flecha = "normal" if es_alcista else "inverse"
                    
                    # Calculamos el porcentaje de desviación sobre la media
                    dif_pct = ((actual / media) - 1) * 100
                    
                    # Mostramos el Ticker en GRANDE y el STATUS en color
                    st.markdown(f"### {ticker.replace('.MC', '')}")
                    # Usamos Markdown para colorear la palabra
                    st.markdown(f"Status: **<span style='color:{color_status}'>{status}</span>**", unsafe_allow_html=True)
                    
                    # Mostramos el precio con su métrica de tendencia
                    st.metric(
                        label=f"Precio Actual",
                        value=f"{actual:.3f} €",
                        delta=f"{dif_pct:.2f}% vs media",
                        delta_color=color_flecha
                    )
                else:
                    st.caption(f"{ticker}: Sin datos")
        
        #st.divider() # Borrado para evitar el error 'divider'
        st.write("---")
        st.info("💡 Consejo: Las acciones en verde están 'fuertes' técnicamente.")
    else:
        st.error("No se han podido cargar los datos de Yahoo Finance.")

except Exception as e:
    st.error(f"Error técnico en el robot: {e}")

st.caption("Filtro: Precio actual comparado con Media Móvil Simple de 20 sesiones.")
                     
               

