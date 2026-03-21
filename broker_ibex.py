import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import os
import warnings

# Bloqueamos los avisos pesados de Yahoo para que no saturen la app
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Miguel Terminal 360", layout="wide")

# Estilo Blanco Nítido
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

# --- 1. CABECERA ---
if os.path.exists("logo_miguel.png"):
    img = Image.open("logo_miguel.png")
    st.image(img, use_column_width=True)

st.title("🏹 Terminal IBEX 360 - MIGUEL")

# --- 2. LISTA OFICIAL IBEX 35 ---
ibex_35 = [
    "ANA.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", "BKT.MC", "BBVA.MC",
    "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC",
    "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC",
    "ROVI.MC", "SCYR.MC", "SLBA.MC", "TEF.MC", "UNI.MC"
]

# --- 3. MOTOR DE ANÁLISIS ---
if st.button('🚀 EJECUTAR ANÁLISIS TOTAL DEL MERCADO', use_container_width=True):
    lista_analisis = []
    progreso = st.progress(0)
    contenedor_status = st.empty()
    
    for i, t in enumerate(ibex_35):
        try:
            contenedor_status.text(f"Analizando {t} ({i+1}/35)...")
            
            # Descarga forzada con 'yf.download' simplificado
            data = yf.download(t, period="6mo", interval="1d", progress=False, group_by='ticker')
            
            if data.empty or len(data) < 20:
                continue
            
            # Limpiamos los datos para evitar el error 'Deprecation'
            cierre = data['Close'].values.flatten()
            precio_act = float(cierre[-1])
            
            # --- SEMÁFORO (CÁLCULO RSI LIMPIO) ---
            delta = pd.Series(cierre).diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi_val = 100 - (100 / (1 + rs.iloc[-1]))
            
            if rsi_val > 70: est, emoji = "🔴 RIESGO", "🔴"
            elif rsi_val < 30: est, emoji = "🟢 COMPRA", "🟢"
            else: est, emoji = "⚪ NEUTRO", "⚪"
            
            lista_analisis.append({
                "ticker": t, "precio": precio_act, "rsi": float(rsi_val),
                "estado": est, "emoji": emoji, "df": data
            })
            progreso.progress((i + 1) / len(ibex_35))
        except:
            continue

    contenedor_status.empty()

    if lista_analisis:
        # --- RANKING ---
        df_rank = pd.DataFrame(lista_analisis)
        t_compras = df_rank.sort_values(by="rsi").head(3)
        t_ventas = df_rank.sort_values(by="rsi", ascending=False).head(3)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 💎 TOP 3: POTENCIAL")
            for _, r in t_compras.iterrows():
                st.success(f"**{r['ticker']}** | RSI: {r['rsi']:.1f} | {r['precio']:.2f}€")
        with c2:
            st.markdown("### ⚠️ TOP 3: RIESGO")
            for _, r in t_ventas.iterrows():
                st.error(f"**{r['ticker']}** | RSI: {r['rsi']:.1f} | {r['precio']:.2f}€")
        
        st.divider()

        # --- RADIOGRAFÍA ---
        st.subheader("📊 Radiografía de los 35 Valores")
        columnas = st.columns(3)
        for i, item in enumerate(lista_analisis):
            with columnas[i % 3]:
                with st.expander(f"{item['emoji']} {item['ticker']}: {item['precio']:.2f}€"):
                    # VELAS JAPONESAS
                    fig = go.Figure(data=[go.Candlestick(
                        x=item['df'].index,
                        open=item['df']['Open'].values.flatten(),
                        high=item['df']['High'].values.flatten(),
                        low=item['df']['Low'].values.flatten(),
                        close=item['df']['Close'].values.flatten()
                    )])
                    fig.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    n_limpio = item['ticker'].split('.')[0]
                    st.markdown(f"[📰 Noticias](https://www.google.com/search?q={n_limpio}+noticias+bolsa&tbm=nws)")

st.divider()
# --- SIMULADOR ---
st.subheader("💰 Simulador")
inv = st.number_input("Dinero (€):", value=1000)
acc = st.selectbox("Acción:", ibex_35)
try:
    p_sim = float(yf.download(acc, period="1d", progress=False)['Close'].values[-1])
    st.info(f"Comprarías {int(inv/p_sim)} acciones de {acc}")
except: pass
