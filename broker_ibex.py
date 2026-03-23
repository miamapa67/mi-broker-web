import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import time

# Configuración de página
st.set_page_config(page_title="Miguel Terminal V3", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal Inteligente IBEX 35 - MIGUEL")
st.write("---")

# 1. DEFINICIÓN DE SECTORES (LOS 35 VALORES)
sectores = {
    "🏦 BANCA": ["SAN.MC", "BBVA.MC", "CABK.MC", "SAB.MC", "BKT.MC", "UNI.MC"],
    "⚡ ENERGÍA": ["IBE.MC", "REP.MC", "NTGY.MC", "ELE.MC", "ENG.MC", "REE.MC", "SLBA.MC"],
    "🏗️ IND. Y CONSUMO": ["ITX.MC", "ANA.MC", "ACS.MC", "FER.MC", "ACX.MC", "MTS.MC", "IAG.MC", "PUIG.MC"],
    "📡 TECNO Y TELCO": ["TEF.MC", "CLNX.MC", "IDR.MC", "AMS.MC"],
    "💊 OTROS (Farma/Inmo)": ["GRF.MC", "ROVI.MC", "COL.MC", "MRL.MC", "LOG.MC", "AENA.MC", "SCYR.MC", "FDR.MC", "MEL.MC"]
}

# 2. FILTROS LATERALES
st.sidebar.header("🎯 PANEL DE CONTROL")
sector_seleccionado = st.sidebar.selectbox("Elegir Sector para Analizar:", ["Todos"] + list(sectores.keys()))

# Preparar lista de tickers
if sector_seleccionado == "Todos":
    lista_tickers = [ticker for sublista in sectores.values() for ticker in sublista]
else:
    lista_tickers = sectores[sector_seleccionado]

# 3. BOTÓN DE ACCIÓN
if st.button(f'🚀 ESCANEAR {sector_seleccionado.upper()}', use_container_width=True):
    resultados = []
    barra = st.progress(0)
    status = st.empty()
    
    for i, t in enumerate(lista_tickers):
        try:
            status.text(f"Leyendo {t}...")
            # Descarga ultra-rápida (1 mes)
            data = yf.download(t, period="1mo", interval="1d", progress=False, timeout=5)
            
            if not data.empty and len(data) > 10:
                precio = float(data['Close'].iloc[-1])
                # Cálculo de RSI para el Semáforo
                delta = data['Close'].diff()
                subida = delta.clip(lower=0).rolling(window=14).mean()
                bajada = (-delta.clip(upper=0)).rolling(window=14).mean()
                rsi = 100 - (100 / (1 + (subida.iloc[-1] / (bajada.iloc[-1] + 0.0001))))
                
                # Clasificación
                color = "🟢" if rsi < 40 else "🔴" if rsi > 65 else "⚪"
                estado = "COMPRA" if rsi < 40 else "RIESGO" if rsi > 65 else "NEUTRO"
                
                resultados.append({"Ticker": t, "Precio": precio, "RSI": rsi, "Semaforo": color, "Estado": estado, "Data": data})
            
            time.sleep(0.1) # Respiro para el servidor
            barra.progress((i + 1) / len(lista_tickers))
        except:
            continue
            
    status.empty()

    if resultados:
        df_res = pd.DataFrame(resultados)
        
        # --- RANKING TOP 3 ---
        st.subheader("🏆 Selección Inteligente")
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("💎 TOP COMPRA (RSI Bajo)")
            for _, r in df_res.sort_values("RSI").head(3).iterrows():
                st.write(f"{r['Semaforo']} **{r['Ticker']}**: {r['Precio']:.2f}€")
                
        with col2:
            st.error("⚠️ TOP RIESGO (RSI Alto)")
            for _, r in df_res.sort_values("RSI", ascending=False).head(3).iterrows():
                st.write(f"{r['Semaforo']} **{r['Ticker']}**: {r['Precio']:.2f}€")

        st.divider()

        # --- CUADRÍCULA DE VALORES ---
        st.subheader("📊 Radiografía Detallada")
        columnas = st.columns(3)
        for idx, r in enumerate(resultados):
            with columnas[idx % 3]:
                with st.expander(f"{r['Semaforo']} {r['Ticker']} - {r['Precio']:.2f}€"):
                    st.write(f"RSI: {r['RSI']:.1f} | **{r['Estado']}**")
                    # Gráfico mini
                    fig = go.Figure(data=[go.Scatter(x=r['Data'].index[-15:], y=r['Data']['Close'][-15:], mode='lines+markers')])
                    fig.update_layout(height=150, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
                    # Noticias
                    st.markdown(f"[📰 Ver Noticias](https://www.google.com/search?q={r['Ticker'].split('.')[0]}+noticias+bolsa&tbm=nws)")
    else:
        st.error("❌ El servidor de bolsa está saturado. Intenta analizar un sector específico en lugar de 'Todos'.")

st.sidebar.divider()
# CALCULADORA
st.sidebar.subheader("💰 CALCULADORA")
capital = st.sidebar.number_input("Inversión (€):", value=1000)
