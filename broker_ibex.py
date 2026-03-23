import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import time
import requests

st.set_page_config(page_title="Miguel Terminal PRO", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal Inteligente IBEX 35 - MIGUEL")

# --- 1. ESTRUCTURA DE SECTORES ---
sectores = {
    "Banca": ["SAN.MC", "BBVA.MC", "CABK.MC", "SAB.MC", "BKT.MC", "UNI.MC"],
    "Energía": ["IBE.MC", "REP.MC", "NTGY.MC", "ELE.MC", "ENG.MC", "REE.MC", "SLBA.MC"],
    "Ind. y Consumo": ["ITX.MC", "ANA.MC", "ACS.MC", "FER.MC", "ACX.MC", "MTS.MC", "IAG.MC", "PUIG.MC"],
    "Tecno y Telco": ["TEF.MC", "CLNX.MC", "IDR.MC", "AMS.MC"],
    "Otros": ["GRF.MC", "ROVI.MC", "COL.MC", "MRL.MC", "LOG.MC", "AENA.MC", "SCYR.MC", "FDR.MC", "MEL.MC"]
}

st.sidebar.header("🎯 Filtros de Selección")
sector_sel = st.sidebar.multiselect("Filtrar Sectores:", list(sectores.keys()), default=list(sectores.keys()))

tickers_finales = []
for s in sector_sel:
    tickers_finales.extend(sectores[s])

# --- 2. MOTOR DE ANÁLISIS ---
if st.button('🚀 LANZAR ESCÁNER 360 (RANKING Y SEMÁFOROS)', use_container_width=True):
    lista_analisis = []
    progreso = st.progress(0)
    
    # DISFRAZ PARA EL SERVIDOR
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    sesion = requests.Session()
    sesion.headers.update(headers)

    with st.spinner('Pidiendo permiso al mercado...'):
        for i, t in enumerate(tickers_finales):
            try:
                # Descarga protegida sin Warnings
                tk = yf.Ticker(t, session=sesion)
                df = tk.history(period="1mo")
                
                if not df.empty:
                    # Arreglo de la línea 41 (evitamos el Warning)
                    p_act = float(df['Close'].iloc[-1])
                    
                    # CÁLCULO RSI
                    delta = df['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rsi = 100 - (100 / (1 + (gain.iloc[-1] / (loss.iloc[-1] + 0.001))))
                    
                    sem = "🟢" if rsi < 40 else "🔴" if rsi > 60 else "⚪"
                    
                    lista_analisis.append({
                        "ticker": t, "precio": p_act, "rsi": rsi, "emoji": sem, "df": df
                    })
                time.sleep(0.1)
                progreso.progress((i + 1) / len(tickers_finales))
            except:
                continue

    if lista_analisis:
        df_rank = pd.DataFrame(lista_analisis)
        
        # --- 3. EL RANKING TOP 3 ---
        st.subheader("🏆 Oportunidades de Compra y Riesgo")
        c1, c2 = st.columns(2)
        with c1:
            mejores = df_rank.sort_values("rsi").head(3)
            st.success("💎 TOP 3 COMPRA (RSI Bajo)")
            for _, r in mejores.iterrows():
                st.write(f"{r['emoji']} **{r['ticker']}**: {r['precio']:.2f}€")
        with c2:
            peores = df_rank.sort_values("rsi", ascending=False).head(3)
            st.error("⚠️ TOP 3 RIESGO (RSI Alto)")
            for _, r in peores.iterrows():
                st.write(f"{r['emoji']} **{r['ticker']}**: {r['precio']:.2f}€")

        st.divider()

        # --- 4. CUADRÍCULA DETALLADA ---
        cols = st.columns(3)
        for idx, item in enumerate(lista_analisis):
            with cols[idx % 3]:
                with st.expander(f"{item['emoji']} {item['ticker']} - {item['precio']:.2f}€"):
                    st.write(f"RSI: {item['rsi']:.1f}")
                    fig = go.Figure(data=[go.Scatter(x=item['df'].index[-15:], y=item['df']['Close'][-15:], mode='lines+markers')])
                    fig.update_layout(height=140, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown(f"[📰 Noticias](https://www.google.com/search?q={item['ticker'].split('.')[0]}+noticias+bolsa&tbm=nws)")
    else:
        st.error("⚠️ Yahoo sigue bloqueando la IP. Prueba en 5 minutos o desde el móvil con datos.")

st.divider()
st.subheader("💰 Calculadora Operativa")
inv = st.number_input("Inversión (€):", value=1000)
