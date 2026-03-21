import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import os

st.set_page_config(page_title="Miguel Terminal Pro", layout="wide")

# Estilo Blanco Nítido
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

# --- 1. CABECERA ---
if os.path.exists("logo_miguel.png"):
    img = Image.open("logo_miguel.png")
    st.image(img, use_column_width=True)

st.title("🏹 Terminal IBEX 35 Profesional - MIGUEL")

# --- 2. LISTA OFICIAL ---
ibex_35 = [
    "ANA.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", "BKT.MC", "BBVA.MC",
    "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC",
    "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC",
    "ROVI.MC", "SCYR.MC", "SLBA.MC", "TEF.MC", "UNI.MC"
]

if st.button('🚀 ESCANEAR MERCADO, NOTICIAS Y GRÁFICOS', use_container_width=True):
    lista_analisis = []
    
    with st.spinner('Analizando los 35 valores...'):
        for t in ibex_35:
            try:
                tk = yf.Ticker(t)
                hist = tk.history(period="6mo")
                if hist.empty: continue
                
                precio_act = float(hist['Close'].iloc[-1])
                
                # CÁLCULO RSI
                delta = hist['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi_val = 100 - (100 / (1 + rs.iloc[-1]))
                
                lista_analisis.append({"ticker": t, "precio": precio_act, "rsi": rsi_val, "df": hist})
            except: continue

    if lista_analisis:
        # --- RANKING INICIAL ---
        df_ranking = pd.DataFrame(lista_analisis)
        t1, t2 = st.columns(2)
        with t1:
            st.success(f"💎 TOP COMPRA: {df_ranking.sort_values('rsi').iloc[0]['ticker']}")
        with t2:
            st.error(f"⚠️ TOP RIESGO: {df_ranking.sort_values('rsi', ascending=False).iloc[0]['ticker']}")

        st.divider()

        # --- DETALLE CON VELAS Y NOTICIAS ---
        for i, item in enumerate(lista_analisis):
            emoji = "🟢" if item['rsi'] < 30 else "🔴" if item['rsi'] > 70 else "⚪"
            with st.expander(f"{emoji} {item['ticker']} - {item['precio']:.2f}€"):
                c1, c2 = st.columns([2, 1])
                
                with c1:
                    # GRÁFICO DE VELAS JAPONESAS (FORZADO)
                    fig = go.Figure(data=[go.Candlestick(
                        x=item['df'].index,
                        open=item['df']['Open'],
                        high=item['df']['High'],
                        low=item['df']['Low'],
                        close=item['df']['Close'],
                        name="Velas"
                    )])
                    fig.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
                    st.plotly_chart(fig, use_container_width=True)

                with c2:
                    st.write(f"**Fuerza RSI:** {item['rsi']:.1f}")
                    nombre_n = item['ticker'].split('.')[0]
                    st.markdown(f"**📰 Radar de Noticias:**")
                    st.markdown(f"[👉 Leer noticias de {nombre_n}](https://www.google.com/search?q={nombre_n}+noticias+bolsa&tbm=nws)")
                    st.markdown(f"[📊 Google Finance](https://www.google.com/finance/quote/{item['ticker'].replace('.MC', ':BME')})")

st.divider()

# --- CALCULADORA ---
st.subheader("💰 Simulador")
inver = st.number_input("Dinero (€):", value=1000)
acc_e = st.selectbox("Acción:", ibex_35)
if st.write(f"Con {inver}€ podrías comprar unas acciones de {acc_e}."):
    pass
