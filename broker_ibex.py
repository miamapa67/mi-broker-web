import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Miguel Terminal PRO", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal Inteligente IBEX 35 - MIGUEL")

# --- 1. CALCULADORA (FUNCIONANDO) ---
with st.expander("💰 CALCULADORA DE OPERACIÓN RÁPIDA", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1: inv = st.number_input("Inversión (€):", value=1000, step=100)
    with c2: pre = st.number_input("Precio Acción (€):", value=10.0, step=0.1)
    with c3:
        obj = st.slider("Objetivo (%)", 1, 30, 10)
        st.metric("Beneficio Estimado", f"+{inv * (obj/100):.2f}€", f"{obj}%")

st.divider()

# --- 2. FILTROS POR SECTOR ---
sectores = {
    "🏦 BANCA": ["SAN.MC", "BBVA.MC", "CABK.MC", "SAB.MC", "BKT.MC", "UNI.MC"],
    "⚡ ENERGÍA": ["IBE.MC", "REP.MC", "NTGY.MC", "ELE.MC", "ENG.MC", "REE.MC", "SLBA.MC"],
    "🏗️ IND/CONS": ["ITX.MC", "ANA.MC", "ACS.MC", "FER.MC", "ACX.MC", "MTS.MC", "IAG.MC", "PUIG.MC"],
    "📡 TECNO": ["TEF.MC", "CLNX.MC", "IDR.MC", "AMS.MC"],
    "🧬 OTROS": ["GRF.MC", "ROVI.MC", "COL.MC", "MRL.MC", "LOG.MC", "AENA.MC", "SCYR.MC", "FDR.MC", "MEL.MC"]
}

st.sidebar.header("🎯 FILTROS DE MERCADO")
sector_sel = st.sidebar.multiselect("Elegir Sectores:", list(sectores.keys()), default=list(sectores.keys()))

tickers_finales = []
for s in sector_sel:
    tickers_finales.extend(sectores[s])

# --- 3. MOTOR DE ANÁLISIS ---
if st.button(f'🚀 ANALIZAR {len(tickers_finales)} VALORES SELECCIONADOS', use_container_width=True):
    lista_analisis = []
    progreso = st.progress(0)
    status_msg = st.empty()
    
    with st.spinner('Analizando datos y noticias...'):
        for i, t in enumerate(tickers_finales):
            try:
                status_msg.text(f"Analizando {t}... ({i+1}/{len(tickers_finales)})")
                # Descarga protegida
                df = yf.download(t, period="1mo", interval="1d", progress=False, timeout=5)
                
                if not df.empty:
                    p_act = float(df['Close'].iloc[-1])
                    # RSI para el Semáforo
                    delta = df['Close'].diff()
                    up = delta.clip(lower=0).rolling(window=14).mean()
                    down = -1 * delta.clip(upper=0).rolling(window=14).mean()
                    rs = up.iloc[-1] / (down.iloc[-1] + 0.00001)
                    rsi = 100 - (100 / (1 + rs))
                    
                    sem = "🟢" if rsi < 40 else "🔴" if rsi > 65 else "⚪"
                    est = "COMPRA" if rsi < 40 else "RIESGO" if rsi > 65 else "NEUTRO"
                    
                    lista_analisis.append({
                        "ticker": t, "precio": p_act, "rsi": rsi, "emoji": sem, "estado": est, "df": df
                    })
                time.sleep(0.1) # Pausa anti-bloqueo
                progreso.progress((i + 1) / len(tickers_finales))
            except: continue

    status_msg.empty()

    if lista_analisis:
        df_rank = pd.DataFrame(lista_analisis)
        
        # --- TOP 3 DE MIGUEL ---
        st.subheader("🏆 Selección Inteligente")
        col1, col2 = st.columns(2)
        with col1:
            mejores = df_rank.sort_values("rsi").head(3)
            st.success("💎 TOP 3 COMPRA (RSI Bajo)")
            for _, r in mejores.iterrows():
                st.write(f"{r['emoji']} **{r['ticker']}**: {r['precio']:.2f}€ (RSI: {r['rsi']:.1f})")
        with col2:
            peores = df_rank.sort_values("rsi", ascending=False).head(3)
            st.error("⚠️ TOP 3 RIESGO (RSI Alto)")
            for _, r in peores.iterrows():
                st.write(f"{r['emoji']} **{r['ticker']}**: {r['precio']:.2f}€ (RSI: {r['rsi']:.1f})")

        st.divider()

        # --- DETALLE INDIVIDUAL ---
        cols = st.columns(3)
        for idx, item in enumerate(lista_analisis):
            with cols[idx % 3]:
                with st.expander(f"{item['emoji']} {item['ticker']} - {item['precio']:.2f}€"):
                    st.write(f"RSI: {item['rsi']:.1f} | **{item['estado']}**")
                    fig = go.Figure(data=[go.Scatter(x=item['df'].index[-15:], y=item['df']['Close'][-15:], mode='lines+markers')])
                    fig.update_layout(height=150, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
                    # NOTICIAS
                    n = item['ticker'].split('.')[0]
                    st.link_button(f"📰 Noticias {n}", f"https://www.google.com/search?q={n}+noticias+bolsa&tbm=nws", use_container_width=True)
    else:
        st.error("Yahoo sigue bloqueando la IP. Intenta analizar solo UN SECTOR desde la izquierda.")
