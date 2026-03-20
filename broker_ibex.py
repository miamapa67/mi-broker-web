import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Monitor IBEX 35", layout="wide")

st.title("🇪🇸 Semáforo IBEX 35: Estrategia de Medias")
st.write("Verde = Tendencia Alcista (Compra) | Rojo = Tendencia Bajista (Venta)")

# Lista oficial de los 35 componentes
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
        # Mostramos 5 columnas en PC, se adaptará a 1 o 2 en el móvil
        cols = st.columns(5)
        
        for i, ticker in enumerate(ibex_35):
            with cols[i % 5]:
                serie = data[ticker].dropna()
                if not serie.empty:
                    actual = serie.iloc[-1]
                    media = serie.tail(20).mean()
                    
                    # CÁLCULO DE TENDENCIA
                    es_alcista = actual > media
                    status = "COMPRA" if es_alcista else "VENTA"
                    # 'normal' pone el delta en verde, 'inverse' en rojo
                    color_semaforo = "normal" if es_alcista else "inverse"
                    
                    # Calculamos el porcentaje de desviación sobre la media
                    dif_pct = ((actual / media) - 1) * 100
                    
                    st.metric(
                        label=f"{ticker.replace('.MC', '')} [{status}]",
                        value=f"{actual:.3f} €",
                        delta=f"{dif_pct:.2f}% vs media",
                        delta_color=color_semaforo
                    )
                else:
                    st.caption(f"{ticker}: Sin datos")
        
        st.divider()
        st.info("💡 Consejo: Las acciones en verde están 'fuertes' técnicamente.")
    else:
        st.error("No se han podido cargar los datos de Yahoo Finance.")

except Exception as e:
    st.error(f"Error en el robot: {e}")

st.caption("Filtro: Precio actual comparado con Media Móvil Simple de 20 sesiones.")
