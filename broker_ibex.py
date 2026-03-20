import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Monitor Financiero", layout="wide")

# --- BARRA LATERAL (Buscador) ---
with st.sidebar:
    st.header("🔎 Buscador de Acciones")
    st.write("Introduce el símbolo (Ticker) de Yahoo Finance.")
    st.write("Ejemplos: `AAPL` (Apple), `TSLA` (Tesla), `REP.MC` (Repsol), `EURUSD=X` (Euro/Dólar)")
    
    # Campo de texto para buscar
    ticker_buscado = st.text_input("Símbolo a analizar:", value="AAPL").upper().strip()
    
    btn_buscar = st.button("Analizar Acción")

st.title("🤖 Tu Analista Robot Inteligente")
st.write("Analizando tendencias con Media Móvil de 20 sesiones (SMA20).")

# --- LÓGICA DEL BUSCADOR ---
if btn_buscar and ticker_buscado:
    st.divider()
    st.subheader(f"📊 Análisis Detallado: {ticker_buscado}")
    
    try:
        with st.spinner(f'Consultando datos de {ticker_buscado}...'):
            # Descargamos 60 días para el buscador para tener más contexto
            data_buscada = yf.download(ticker_buscado, period="60d")['Close']
        
        if not data_buscada.empty:
            # Quitamos los NaN
            data_buscada = data_buscada.dropna()
            
            # Cálculos
            precio_actual = data_buscada.iloc[-1]
            media_20 = data_buscada.tail(20).mean()
            
            # Decidimos la moneda (MC = Madrid = €, resto = $)
            moneda = "€" if ".MC" in ticker_buscado else "$"
            
            # Lógica de tendencia
            es_alcista = precio_actual > media_20
            status = "COMPRA ✅" if es_alcista else "VENTA ❌"
            color_status = "green" if es_alcista else "red"
            
            # Diseño visual del resultado
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.metric(
                    label=f"Precio Actual ({moneda})",
                    value=f"{precio_actual:.2f} {moneda}",
                    delta=f"{((precio_actual/media_20)-1)*100:.2f}% vs media",
                    delta_color="normal" if es_alcista else "inverse"
                )
                
                st.markdown(f"### Recomendación técnica:")
                st.markdown(f"### **<span style='color:{color_status}'>{status}</span>**", unsafe_allow_html=True)

            with col2:
                # Añadimos una gráfica sencilla de los últimos 60 días
                st.line_chart(data_buscada)
                st.caption("Evolución del precio (últimos 60 días)")
            
            st.success(f"Análisis de {ticker_buscado} completado.")
        else:
            st.error(f"No se han encontrado datos para el símbolo '{ticker_buscado}'. Revisa que el Ticker sea correcto en Yahoo Finance.")
            
    except Exception as e:
        st.error(f"Error al analizar {ticker_buscado}: {e}")

st.write("---")

# --- MONITOR GENERAL (Los 35 del IBEX) ---
st.subheader("🇪🇸 Resumen Semáforo: Los 35 del IBEX")

ibex_35 = [
    "ANA.MC", "ACS.MC", "ACG.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", 
    "BKT.MC", "BBVA.MC", "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", 
    "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC", "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", 
    "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC", "ROVI.MC", "SCYR.MC", 
    "SLR.MC", "TEF.MC", "UNI.MC"
]

try:
    with st.spinner('Actualizando precios de Madrid...'):
        data_ibex = yf.download(ibex_35, period="40d")['Close']
    
    if not data_ibex.empty:
        cols = st.columns(5)
        for i, ticker in enumerate(ibex_35):
            with cols[i % 5]:
                serie = data_ibex[ticker].dropna()
                if not serie.empty:
                    actual = serie.iloc[-1]
                    media = serie.tail(20).mean()
                    es_alcista = actual > media
                    status = "COMPRA" if es_alcista else "VENTA"
                    color_status = "green" if es_alcista else "red"
                    dif_pct = ((actual / media) - 1) * 100
                    
                    st.markdown(f"#### {ticker.replace('.MC', '')}")
                    st.markdown(f"Status: **<span style='color:{color_status}'>{status}</span>**", unsafe_allow_html=True)
                    st.metric(
                        label=f"Precio (€)",
                        value=f"{actual:.2f} €",
                        delta=f"{dif_pct:.2f}%",
                        delta_color="normal" if es_alcista else "inverse"
                    )
                else:
                    st.caption(f"{ticker}: Sin datos")
except Exception as e:
    st.error(f"Error en el monitor general: {e}")

st.caption("Filtro: Precio actual vs Media Móvil Simple de 20 sesiones.")
               

