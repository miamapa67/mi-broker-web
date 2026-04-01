import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import time
import requests

st.set_page_config(page_title="Miguel Terminal PRO", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal Inteligente IBEX 35 - MIGUEL")

# --- 1. LISTA OFICIAL 35 VALORES ---
ibex_35 = [
    "ANA.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", "BKT.MC", "BBVA.MC",
    "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC",
    "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC",
    "ROVI.MC", "SCYR.MC", "SLBA.MC", "TEF.MC", "UNI.MC"
]

# --- 2. MOTOR DE ANÁLISIS CON "DISFRAZ" ---
if st.button('🚀 LANZAR ESCÁNER 360 (RANKING Y SEMÁFOROS)', use_container_width=True):
    lista_analisis = []
    progreso = st.progress(0)
    
    # Creamos una sesión con identidad de navegador real
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    session = requests.Session()
    session.headers.update(headers)

    with st.spinner('Analizando los 35 valores...'):
        for i, t in enumerate(ibex_35):
            try:
                # Descargamos con la sesión camuflada
                tk = yf.Ticker(t, session=session)
                df = tk.history(period="3mo", interval="1d")
                
                if not df.empty and len(df) >= 20:
                    p_act = float(df['Close'].iloc[-1])
                    p_ini_20 = float(df['Close'].iloc[-20])
                    var_20d = ((p_act - p_ini_20) / p_ini_20) * 100
                    
                    # Cálculo RSI 14
                    delta = df['Close'].diff()
                    up = delta.clip(lower=0).rolling(window=14).mean()
                    down = -1 * delta.clip(upper=0).rolling(window=14).mean()
                    rs = up.iloc[-1] / (down.iloc[-1] + 0.00001)
                    rsi = 100 - (100 / (1 + rs))
                    
                    if rsi < 40: sem, col = "🟢 COMPRA", "green"
                    elif rsi > 60: sem, col = "🔴 RIESGO", "red"
                    else: sem, col = "⚪ NEUTRO", "gray"
                    
                    lista_analisis.append({
                        "ticker": t, "precio": p_act, "rsi": rsi, "var20": var_20d, "sem": sem, "df": df
                    })
                
                # Pausa de seguridad para evitar baneos (0.2 segundos)
                time.sleep(0.2)
                progreso.progress((i + 1) / len(ibex_35))
            except: continue

    if lista_analisis:
        df_rank = pd.DataFrame(lista_analisis)
        
        # --- TOP 3 DE COMPRA ---
        st.subheader("🏆 TOP 3: MEJORES OPORTUNIDADES")
        top_3 = df_rank.sort_values("rsi").head(3)
        c_top = st.columns(3)
        for idx, (_, r) in enumerate(top_3.iterrows()):
            with c_top[idx]:
                with st.container(border=True):
                    st.success(f"🥇 OPCIÓN {idx+1}: {r['ticker']}")
                    st.metric("Precio", f"{r['precio']:.2f}€", f"{r['var20']:.2f}%")
                    st.write(f"RSI: {r['rsi']:.1f}")
                    name = r['ticker'].split('.')[0]
                    st.link_button("📰 Noticias", f"https://www.google.com/search?q={name}+noticias+bolsa&tbm=nws")

        st.divider()
        
        # --- DESGLOSE DE LOS 35 ---
        cols = st.columns(3)
        for idx, item in enumerate(lista_analisis):
            with cols[idx % 3]:
                with st.expander(f"{item['sem']} | {item['ticker']} - {item['precio']:.2f}€"):
                    st.write(f"RSI: {item['rsi']:.1f} | Var 20d: {item['var20']:.2f}%")
                    fig = go.Figure(data=[go.Candlestick(x=item['df'].index[-20:], open=item['df']['Open'][-20:], high=item['df']['High'][-20:], low=item['df']['Low'][-20:], close=item['df']['Close'][-20:])])
                    fig.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("❌ El servidor sigue bloqueado. Intenta cerrar la app y abrirla de nuevo en 5 minutos.")

# Calculadora lateral siempre activa
st.sidebar.subheader("💰 Calculadora Miguel")
inv = st.sidebar.number_input("Inversión (€):", value=1000)
