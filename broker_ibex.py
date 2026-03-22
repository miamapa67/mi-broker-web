import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import os

st.set_page_config(page_title="Miguel Terminal 360 Pro", layout="wide")

# Estilo Blanco Nítido Profesional
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

# --- 1. CABECERA ---
if os.path.exists("logo_miguel.png"):
    img = Image.open("logo_miguel.png")
    st.image(img, use_column_width=True)

st.title("🏹 Terminal Inteligente IBEX 35 - MIGUEL")
st.write("Análisis de Oportunidades, Semáforos, Gráficos de Velas y Noticias en Tiempo Real.")

# --- 2. LISTA OFICIAL DE LOS 35 DEL IBEX ---
ibex_35 = [
    "ANA.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", "BKT.MC", "BBVA.MC",
    "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC",
    "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC",
    "ROVI.MC", "SCYR.MC", "SLBA.MC", "TEF.MC", "UNI.MC"
]

# --- 3. BOTÓN DE ESCÁNER TOTAL ---
if st.button('🚀 EJECUTAR ANÁLISIS 360 (LOS 35 VALORES)', use_container_width=True):
    lista_analisis = []
    progreso = st.progress(0)
    status = st.empty()
    
    with st.spinner('Escaneando el mercado español...'):
        for i, t in enumerate(ibex_35):
            try:
                status.text(f"Analizando {t} ({i+1}/35)...")
                # Descarga de datos (6 meses para las velas y el RSI)
                df = yf.download(t, period="6mo", interval="1d", progress=False)
                
                if not df.empty and len(df) > 14:
                    precio_act = float(df['Close'].values[-1])
                    
                    # --- CÁLCULO RSI (SEMÁFORO) ---
                    delta = df['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain.values[-1] / (loss.values[-1] + 0.00001)
                    rsi_val = 100 - (100 / (1 + rs))
                    
                    # Clasificación para Filtros
                    if rsi_val < 35: sem, est, col = "🟢", "COMPRA", "green"
                    elif rsi_val > 65: sem, est, col = "🔴", "RIESGO", "red"
                    else: sem, est, col = "⚪", "NEUTRO", "gray"
                    
                    lista_analisis.append({
                        "ticker": t, "precio": precio_act, "rsi": float(rsi_val),
                        "estado": est, "emoji": sem, "df": df
                    })
                progreso.progress((i + 1) / len(ibex_35))
            except: continue

    status.empty()

    if lista_analisis:
        df_rank = pd.DataFrame(lista_analisis)
        
        # --- 4. RANKING TOP 3 Y FILTROS ---
        st.subheader("🏆 Filtro de Oportunidades y Riesgos")
        f1, f2, f3 = st.columns(3)
        
        with f1:
            mejores = df_rank.sort_values(by="rsi").head(3)
            st.success("💎 TOP 3: MEJOR COMPRA")
            for _, r in mejores.iterrows():
                st.write(f"**{r['ticker']}** (RSI: {r['rsi']:.1f})")
        
        with f2:
            neutros = df_rank[df_rank['estado'] == 'NEUTRO']
            st.info(f"⚪ VALORES EN CALMA: {len(neutros)}")
            st.write("Mercado estable para estos valores.")

        with f3:
            peores = df_rank.sort_values(by="rsi", ascending=False).head(3)
            st.error("⚠️ TOP 3: MÁS RIESGO")
            for _, r in peores.iterrows():
                st.write(f"**{r['ticker']}** (RSI: {r['rsi']:.1f})")

        st.divider()

        # --- 5. DETALLE DE LOS 35 (VELAS, SEMÁFORO Y NOTICIAS) ---
        st.subheader("📊 Radiografía Detallada de los 35")
        columnas = st.columns(3)
        
        for idx, item in enumerate(lista_analisis):
            with columnas[idx % 3]:
                with st.expander(f"{item['emoji']} {item['ticker']}: {item['precio']:.2f}€"):
                    st.write(f"**Fuerza RSI:** {item['rsi']:.1f} | **Estado:** {item['estado']}")
                    
                    # Gráfico Interactivo de Velas Japonesas
                    fig = go.Figure(data=[go.Candlestick(
                        x=item['df'].index[-30:],
                        open=item['df']['Open'][-30:],
                        high=item['df']['High'][-30:],
                        low=item['df']['Low'][-30:],
                        close=item['df']['Close'][-30:]
                    )])
                    fig.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Radar de Noticias e Info
                    n_limpio = item['ticker'].split('.')[0]
                    st.markdown(f"[📰 Noticias de {n_limpio}](https://www.google.com/search?q={n_limpio}+noticias+bolsa&tbm=nws)")
                    st.markdown(f"[📊 Google Finance](https://www.google.com/finance/quote/{item['ticker'].replace('.MC', ':BME')})")

st.divider()

# --- 6. CALCULADORA DE INVERSIÓN ---
st.subheader("💰 Simulador de Inversión Miguel")
c_sim1, c_sim2 = st.columns(2)
with c_sim1:
    inv = st.number_input("Dinero a invertir (€):", value=1000, step=500)
    acc = st.selectbox("Elegir Acción:", ibex_35)
with c_sim2:
    subida = st.slider("Subida esperada (%)", 1, 30, 10)
    ganancia = inv * (subida/100)
    st.metric("Beneficio Estimado", f"+{ganancia:.2f}€", f"{subida}%")
