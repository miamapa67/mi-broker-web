import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Miguel Terminal 360", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal Inteligente IBEX 35 - MIGUEL")

# --- 1. CALCULADORA RÁPIDA (SIEMPRE VISIBLE) ---
with st.expander("💰 CALCULADORA DE OPERACIÓN RÁPIDA", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        capital = st.number_input("Inversión (€):", value=1000, step=100)
    with c2:
        precio_entrada = st.number_input("Precio Acción (€):", value=10.0, step=0.1)
    with c3:
        objetivo = st.slider("Objetivo de subida (%)", 1, 30, 10)
        ganancia = capital * (objetivo / 100)
        st.metric("Beneficio Estimado", f"+{ganancia:.2f}€", f"{objetivo}%")

st.divider()

# --- 2. LISTA 35 VALORES ---
ibex_35 = [
    "ANA.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", "BKT.MC", "BBVA.MC",
    "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC",
    "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC",
    "ROVI.MC", "SCYR.MC", "SLBA.MC", "TEF.MC", "UNI.MC"
]

# --- 3. MOTOR DE ANÁLISIS ---
if st.button('🚀 EJECUTAR ANÁLISIS 360 (RANKING Y SEMÁFOROS)', use_container_width=True):
    lista_analisis = []
    progreso = st.progress(0)
    status_msg = st.empty()
    
    with st.spinner('Escaneando los 35 valores...'):
        for i, t in enumerate(ibex_35):
            try:
                status_msg.text(f"Analizando {t}... ({i+1}/35)")
                df = yf.download(t, period="1mo", interval="1d", progress=False, timeout=10)
                
                if not df.empty and len(df) > 10:
                    p_act = float(df['Close'].iloc[-1])
                    # RSI para el Semáforo
                    delta = df['Close'].diff()
                    up = delta.clip(lower=0).rolling(window=14).mean()
                    down = -1 * delta.clip(upper=0).rolling(window=14).mean()
                    rsi = 100 - (100 / (1 + (up.iloc[-1] / (down.iloc[-1] + 0.0001))))
                    
                    sem = "🟢" if rsi < 40 else "🔴" if rsi > 60 else "⚪"
                    
                    lista_analisis.append({
                        "ticker": t, "precio": p_act, "rsi": rsi, "emoji": sem, "df": df
                    })
                time.sleep(0.1)
                progreso.progress((i + 1) / len(ibex_35))
            except:
                continue
    status_msg.empty()

    if lista_analisis:
        df_rank = pd.DataFrame(lista_analisis)
        
        # --- TOP 3 DE MIGUEL ---
        st.subheader("🏆 Selección Inteligente de Hoy")
        col_m, col_p = st.columns(2)
        with col_m:
            mejores = df_rank.sort_values("rsi").head(3)
            st.success("💎 TOP 3 COMPRA (RSI Bajo)")
            for _, r in mejores.iterrows():
                st.write(f"{r['emoji']} **{r['ticker']}**: {r['precio']:.2f}€")
        with col_p:
            peores = df_rank.sort_values("rsi", ascending=False).head(3)
            st.error("⚠️ TOP 3 RIESGO (RSI Alto)")
            for _, r in peores.iterrows():
                st.write(f"{r['emoji']} **{r['ticker']}**: {r['precio']:.2f}€")

        st.divider()
        
        # --- DETALLE INDIVIDUAL ---
        st.subheader("📊 Radiografía de los 35")
        cols = st.columns(3)
        for idx, item in enumerate(lista_analisis):
            with cols[idx % 3]:
                with st.expander(f"{item['emoji']} {item['ticker']} - {item['precio']:.2f}€"):
                    st.write(f"RSI: {item['rsi']:.1f}")
                    fig = go.Figure(data=[go.Scatter(x=item['df'].index[-15:], y=item['df']['Close'][-15:], mode='lines')])
                    fig.update_layout(height=140, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
                    n_limpio = item['ticker'].split('.')[0]
                    st.markdown(f"[📰 Noticias {n_limpio}](https://www.google.com/search?q={n_limpio}+noticias+bolsa&tbm=nws)")
    else:
        st.error("⚠️ Error de conexión. Intenta de nuevo en unos segundos.")
