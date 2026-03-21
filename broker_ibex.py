import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import os

st.set_page_config(page_title="Miguel Terminal 360", layout="wide")

# Estilo Blanco Nítido
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

# --- 1. CABECERA ---
if os.path.exists("logo_miguel.png"):
    img = Image.open("logo_miguel.png")
    st.image(img, use_column_width=True)

st.title("🏹 Terminal IBEX 360 - MIGUEL")
st.write("Ranking de Oportunidades + Semáforo RSI + Velas Japonesas + Noticias.")

# --- 2. LISTA OFICIAL IBEX 35 ---
ibex_35 = [
    "ANA.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", "BKT.MC", "BBVA.MC",
    "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC",
    "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC",
    "ROVI.MC", "SCYR.MC", "SLBA.MC", "TEF.MC", "UNI.MC"
]

if st.button('🚀 EJECUTAR ANÁLISIS TOTAL DEL MERCADO', use_container_width=True):
    lista_analisis = []
    
    with st.spinner('Procesando el IBEX 35...'):
        for t in ibex_35:
            try:
                tk = yf.Ticker(t)
                hist = tk.history(period="6mo")
                if hist.empty: continue
                
                precio_act = float(hist['Close'].iloc[-1])
                
                # --- SEMÁFORO (CÁLCULO RSI) ---
                delta = hist['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi_val = 100 - (100 / (1 + rs.iloc[-1]))
                
                if rsi_val > 70: est, color_c = "🔴 RIESGO (VENTA)", "#fef2f2"
                elif rsi_val < 30: est, color_c = "🟢 COMPRA (POTENCIAL)", "#f0fdf4"
                else: est, color_c = "⚪ NEUTRO", "#f8fafc"
                
                lista_analisis.append({
                    "ticker": t,
                    "precio": precio_act,
                    "rsi": rsi_val,
                    "estado": est,
                    "color": color_c,
                    "df": hist
                })
            except: continue

    # --- 3. MOSTRAR RANKINGS ---
    if lista_analisis:
        df_ranking = pd.DataFrame(lista_analisis)
        top_compras = df_ranking.sort_values(by="rsi").head(3)
        top_ventas = df_ranking.sort_values(by="rsi", ascending=False).head(3)

        c_r1, c_r2 = st.columns(2)
        
        with c_r1:
            st.markdown("### 💎 TOP 3: MÁS POTENCIAL (COMPRA)")
            for _, row in top_compras.iterrows():
                st.success(f"**{row['ticker']}** | RSI: {row['rsi']:.1f} | {row['precio']:.2f}€")
        
        with c_r2:
            st.markdown("### ⚠️ TOP 3: MÁS RIESGO (VENTA)")
            for _, row in top_ventas.iterrows():
                st.error(f"**{row['ticker']}** | RSI: {row['rsi']:.1f} | {row['precio']:.2f}€")
        
        st.divider()

        # --- 4. DETALLE DE LOS 35 CON VELAS Y NOTICIAS ---
        st.subheader("📊 Radiografía de los 35 Valores")
        cols = st.columns(3) # Dividimos en 3 columnas
        
        for i, item in enumerate(lista_analisis):
            with cols[i % 3]:
                # Tarjeta con el semáforo y precio visible
                with st.expander(f"{item['estado'].split(' ')[0]} {item['ticker']}: {item['precio']:.2f}€", expanded=True):
                    # GRÁFICO DE VELAS JAPONESAS (CORREGIDO)
                    fig = go.Figure(data=[go.Candlestick(
                        x=item['df'].index,
                        open=item['df']['Open'],
                        high=item['df']['High'],
                        low=item['df']['Low'],
                        close=item['df']['Close'],
                        name="Velas"
                    )])
                    # Ajuste visual del gráfico
                    fig.update_layout(
                        height=180, 
                        margin=dict(l=0,r=0,t=0,b=0), 
                        xaxis_rangeslider_visible=False,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Radar de Información
                    c_n1, c_n2 = st.columns(2)
                    with c_n1:
                        st.write(f"**RSI:** {item['rsi']:.1f}")
                        nombre_n = item['ticker'].split('.')[0]
                    with c_n2:
                        st.markdown(f"**📰 Información:**")
                        st.markdown(f"[📰 Noticias]({https://www.google.com/search?q={nombre_n}+noticias+bolsa&tbm=nws})")
                        st.markdown(f"[📊 Google Finance](https://www.google.com/finance/quote/{item['ticker'].replace('.MC', ':BME')})")

st.divider()

# --- 5. CALCULADORA (FUNCIONANDO) ---
st.subheader("💰 Simulador de Inversión")
c1, c2 = st.columns(2)
with c1:
    inver = st.number_input("Dinero (€):", value=1000, step=500)
    acc_elegida = st.selectbox("Acción:", ibex_35)
    sub_obj = st.slider("Subida (%)", 1, 30, 5)

with c2:
    try:
        data_s = yf.download(acc_elegida, period="1d", progress=False)
        p_v = float(data_s['Close'].iloc[-1])
        n_acc = int(inver / p_v)
        st.success(f"**Resultado para {acc_elegida}:**")
        st.write(f"Comprarías **{n_acc}** acciones a {p_v:.2f}€")
        st.write(f"Ganancia estimada: **+{(p_v * (sub_obj/100)) * n_acc:.2f}€**")
    except: st.write("Calculando...")
