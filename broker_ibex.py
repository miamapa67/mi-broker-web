import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import time
import requests

st.set_page_config(page_title="Miguel Terminal PRO", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal Inteligente IBEX 35 - MIGUEL")

# --- 1. CALCULADORA (ACTIVA SIEMPRE) ---
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
sector_sel = st.sidebar.selectbox("Elegir Sector para Analizar:", ["SELECCIONAR..."] + list(sectores.keys()))

# --- 3. MOTOR DE ANÁLISIS CAMUFLADO ---
if sector_sel != "SELECCIONAR..." and st.button(f'🚀 ANALIZAR SECTOR {sector_sel}', use_container_width=True):
    lista_analisis = []
    progreso = st.progress(0)
    status_msg = st.empty()
    
    # DISFRAZ DE NAVEGADOR PROFESIONAL
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    sesion = requests.Session()
    sesion.headers.update(headers)

    with st.spinner(f'Analizando {sector_sel}...'):
        for i, t in enumerate(sectores[sector_sel]):
            try:
                status_msg.text(f"Pidiendo datos de {t}...")
                # Descarga individual con camuflaje
                ticker_obj = yf.Ticker(t, session=sesion)
                df = ticker_obj.history(period="1mo", interval="1d", timeout=10)
                
                if not df.empty:
                    p_act = float(df['Close'].iloc[-1])
                    # Cálculo RSI (Semáforo)
                    delta = df['Close'].diff()
                    up = delta.clip(lower=0).rolling(window=14).mean()
                    down = -1 * delta.clip(upper=0).rolling(window=14).mean()
                    rsi = 100 - (100 / (1 + (up.iloc[-1] / (down.iloc[-1] + 0.0001))))
                    
                    sem = "🟢" if rsi < 40 else "🔴" if rsi > 60 else "⚪"
                    
                    lista_analisis.append({
                        "ticker": t, "precio": p_act, "rsi": rsi, "emoji": sem, "df": df
                    })
                
                time.sleep(1.5) # Pausa humana para no ser bloqueados
                progreso.progress((i + 1) / len(sectores[sector_sel]))
            except: continue

    status_msg.empty()

    if lista_analisis:
        df_rank = pd.DataFrame(lista_analisis)
        
        # --- 4. TOP 3 DEL SECTOR ---
        st.subheader(f"🏆 Oportunidades en {sector_sel}")
        c1, c2 = st.columns(2)
        with c1:
            mejores = df_rank.sort_values("rsi").head(3)
            st.success("💎 MEJOR COMPRA (RSI Bajo)")
            for _, r in mejores.iterrows():
                st.write(f"{r['emoji']} **{r['ticker']}**: {r['precio']:.2f}€")
        with c2:
            peores = df_rank.sort_values("rsi", ascending=False).head(3)
            st.error("⚠️ RIESGO ALTO (RSI Alto)")
            for _, r in peores.iterrows():
                st.write(f"{r['emoji']} **{r['ticker']}**: {r['precio']:.2f}€")

        st.divider()

        # --- 5. CUADRÍCULA DETALLADA ---
        cols = st.columns(3)
        for idx, item in enumerate(lista_analisis):
            with cols[idx % 3]:
                with st.expander(f"{item['emoji']} {item['ticker']} - {item['precio']:.2f}€"):
                    st.write(f"Fuerza RSI: {item['rsi']:.1f}")
                    fig = go.Figure(data=[go.Scatter(x=item['df'].index[-15:], y=item['df']['Close'][-15:], mode='lines+markers')])
                    fig.update_layout(height=140, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
                    # NOTICIAS
                    n = item['ticker'].split('.')[0]
                    st.link_button(f"📰 Noticias {n}", f"https://www.google.com/search?q={n}+noticias+bolsa&tbm=nws", use_container_width=True)
    else:
        st.error("❌ El servidor sigue bloqueado. Prueba a analizar BANCA, que tiene menos valores.")
              
