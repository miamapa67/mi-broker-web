import streamlit as st
import yfinance as yf
import pandas as pd

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Miguel Terminal PRO", layout="wide")

st.title("🚀 Terminal Inteligente IBEX 35 - MIGUEL")

# 2. LISTA ACTUALIZADA
ibex_35 = [
    "ANA.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", 
    "MRL.MC", "BBVA.MC", "BKT.MC", "CABK.MC", "ENG.MC", 
    "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", 
    "IBE.MC", "ITX.MC", "IDR.MC", "COL.MC", "LOG.MC", 
    "MAP.MC", "MEL.MC", "NTGY.MC", "PUIG.MC", "RED.MC", 
    "ROVI.MC", "SAB.MC", "SAN.MC", "SCYR.MC", "TEF.MC", 
    "UNI.MC"
]

# 3. SIDEBAR
with st.sidebar:
    st.header("💰 CALCULADORA")
    capital = st.number_input("Inversión (€):", value=1000)
    st.divider()
    st.success("🟢 COMPRA: RSI < 35")
    st.error("🔴 RIESGO: RSI > 65")

# 4. FUNCIÓN PARA CARGAR DATOS (Crucial que esté aquí arriba)
@st.cache_data(ttl=600)
def cargar_datos(tickers):
    df = yf.download(tickers, period="3mo")['Close']
    return df

# 5. MOTOR DE ANÁLISIS
try:
    df_precios = cargar_datos(ibex_35)
    
    resumen = []
    for ticker in ibex_35:
        if ticker in df_precios.columns:
            precios = df_precios[ticker].dropna()
            if len(precios) > 14:
                # Cálculo de RSI
                delta = precios.diff()
                ganancia = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                perdida = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = ganancia / perdida
                rsi = 100 - (100 / (1 + rs))
                
                ultimo_precio = precios.iloc[-1]
                ultimo_rsi = rsi.iloc[-1]
                
                # Clasificación
                estado = "⚪ NEUTRO"
                if ultimo_rsi < 35: estado = "🟢 COMPRA"
                elif ultimo_rsi > 65: estado = "🔴 RIESGO"
                
                resumen.append({
                    "Ticker": ticker,
                    "Precio": f"{ultimo_precio:.2f}€",
                    "RSI": round(ultimo_rsi, 2),
                    "Estado": estado
                })

    if resumen:
        df_final = pd.DataFrame(resumen)
        st.subheader("💡 Análisis de Oportunidades")
        st.dataframe(df_final, use_container_width=True)
    else:
        st.warning("No se pudieron calcular señales. Reintentando...")

except Exception as e:
    st.error(f"Error en el análisis: {e}")
