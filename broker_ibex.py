import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import requests

st.set_page_config(page_title="Miguel Terminal PRO", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal Profesional IBEX 35 - MIGUEL")

# --- LISTA REDUCIDA PARA EVITAR BLOQUEOS (Los más importantes) ---
ibex_35 = [
    "SAN.MC", "BBVA.MC", "TEF.MC", "ITX.MC", "REP.MC", "IAG.MC", 
    "GRF.MC", "SAB.MC", "IBE.MC", "CABK.MC", "CLNX.MC", "AMS.MC"
]

if st.button('🚀 ACTIVAR ESCÁNER DE MERCADO', use_container_width=True):
    lista_analisis = []
    progreso = st.progress(0)
    
    # TRUCO DE CAMUFLAJE: Engañamos al servidor
    sesion = requests.Session()
    sesion.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })

    with st.spinner('Entrando en la Bolsa de Madrid...'):
        for i, t in enumerate(ibex_35):
            try:
                # Pedimos los datos usando el disfraz (sesion)
                ticker = yf.Ticker(t, session=sesion)
                df = ticker.history(period="3mo")
                
                if not df.empty:
                    p_act = float(df['Close'].iloc[-1])
                    # Semáforo RSI
                    delta = df['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rsi = 100 - (100 / (1 + (gain.iloc[-1] / (loss.iloc[-1] + 0.001))))
                    
                    color = "🟢" if rsi < 35 else "🔴" if rsi > 65 else "⚪"
                    est = "COMPRA" if rsi < 35 else "RIESGO" if rsi > 65 else "NEUTRO"
                    
                    lista_analisis.append({
                        "ticker": t, "precio": p_act, "rsi": rsi, "emoji": color, "estado": est, "df": df
                    })
                progreso.progress((i + 1) / len(ibex_35))
            except:
                continue

    if lista_analisis:
        st.success("✅ ¡Conexión establecida con éxito!")
        # Rankings
        df_rank = pd.DataFrame(lista_analisis)
        c1, c2 = st.columns(2)
        with c1:
            mejores = df_rank.sort_values("rsi").head(2)
            st.info(f"💎 OPORTUNIDADES: {', '.join(mejores['ticker'].tolist())}")
        with c2:
            peores = df_rank.sort_values("rsi", ascending=False).head(2)
            st.warning(f"⚠️ RIESGOS: {', '.join(peores['ticker'].tolist())}")
        
        st.divider()
        
        # Cuadrícula
        cols = st.columns(3)
        for idx, item in enumerate(lista_analisis):
            with cols[idx % 3]:
                with st.expander(f"{item['emoji']} {item['ticker']}: {item['precio']:.2f}€", expanded=True):
                    st.write(f"RSI: {item['rsi']:.1f} | {item['estado']}")
                    fig = go.Figure(data=[go.Scatter(x=item['df'].index[-20:], y=item['df']['Close'][-20:], mode='lines+markers')])
                    fig.update_layout(height=140, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown(f"[📰 Noticias](https://www.google.com/search?q={item['ticker'].split('.')[0]}+noticias+bolsa&tbm=nws)")
    else:
        st.error("❌ El servidor de bolsa sigue cerrado para esta conexión.")
        st.info("💡 Miguel: Intenta abrir la app desde tu MÓVIL (con datos 4G/5G, no WiFi). Si desde el móvil funciona, el problema es el WiFi de tu casa/oficina que Yahoo ha bloqueado.")

st.divider()
st.subheader("💰 Simulador Rápido")
inv = st.number_input("Capital (€):", value=1000)
