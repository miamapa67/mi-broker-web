import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go # Librería para gráficos interactivos
from PIL import Image
import os

st.set_page_config(page_title="Miguel Terminal Visual", layout="wide")

# Estilo Blanco Nítido
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

# --- 1. CABECERA ---
if os.path.exists("logo_miguel.png"):
    img = Image.open("logo_miguel.png")
    st.image(img, use_column_width=True)

st.title("🏹 Terminal Visual Interactiva - MIGUEL")

# --- 2. DICCIONARIO DE SECTORES ---
sectores = {
    "Todos los Sectores": ["ANA.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", "BKT.MC", "BBVA.MC", "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC", "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC", "ROVI.MC", "SCYR.MC", "SLBA.MC", "TEF.MC", "UNI.MC"],
    "Banca y Seguros": ["SAN.MC", "BBVA.MC", "CABK.MC", "SAB.MC", "BKT.MC", "UNI.MC", "MAP.MC"],
    "Energía y Petróleo": ["IBE.MC", "REP.MC", "NTGY.MC", "ELE.MC", "ENG.MC", "REE.MC", "SLBA.MC"],
    "Tecnología y Telco": ["TEF.MC", "CLNX.MC", "IDR.MC"]
}

sector_elegido = st.selectbox("Selecciona sector:", list(sectores.keys()))
lista_tickers = sectores[sector_elegido]

if st.button(f'🚀 ANALIZAR Y GENERAR GRÁFICOS: {sector_elegido.upper()}', use_container_width=True):
    
    with st.spinner('Construyendo gráficos de velas...'):
        for t in lista_tickers:
            try:
                tk = yf.Ticker(t)
                # Bajamos 6 meses para que el gráfico tenga perspectiva
                df = tk.history(period="6mo")
                if df.empty: continue
                
                precio_act = float(df['Close'].iloc[-1])
                
                # --- CÁLCULO RSI ---
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi_val = 100 - (100 / (1 + rs.iloc[-1]))
                
                emo = "🟢" if rsi_val < 30 else "🔴" if rsi_val > 70 else "⚪"
                
                with st.expander(f"{emo} {t}: {precio_act:.2f}€ | Ver Análisis y Gráfico"):
                    
                    # --- GRÁFICO DE VELAS ---
                    fig = go.Figure(data=[go.Candlestick(
                        x=df.index,
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'],
                        name="Precio"
                    )])
                    
                    fig.update_layout(
                        title=f"Evolución 6 meses - {t}",
                        yaxis_title="Precio (€)",
                        xaxis_rangeslider_visible=False, # Quitamos la barra de abajo para que sea más limpio
                        height=400,
                        margin=dict(l=0, r=0, t=30, b=0)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # --- DATOS EXTRA ---
                    c1, c2, c3 = st.columns(3)
                    c1.metric("RSI (Fuerza)", f"{rsi_val:.1f}")
                    
                    p_obj = tk.info.get('targetMeanPrice')
                    if p_obj:
                        pot = ((p_obj - precio_act) / precio_act) * 100
                        c2.metric("Potencial", f"+{pot:.1f}%", delta_color="normal")
                    
                    n_n = t.split('.')[0]
                    c3.markdown(f"**Noticias:** [👉 Google News]({https://www.google.com/search?q={n_n}+noticias+bolsa&tbm=nws})")

            except: continue

st.divider()

# --- 3. CALCULADORA ---
st.subheader("💰 Simulador de Inversión")
c_sim1, c_sim2 = st.columns(2)
with c_sim1:
    inver = st.number_input("Capital (€):", value=1000)
    acc = st.selectbox("Valor:", lista_tickers)
    sub = st.slider("Subida (%)", 1, 30, 10)
with c_sim2:
    try:
        p_v = float(yf.Ticker(acc).history(period="1d")['Close'].iloc[-1])
        st.success(f"**Beneficio: +{(p_v * (sub/100)) * (int(inver/p_v)):.2f}€**")
    except: st.write("Calculando...")
