import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Miguel Terminal 360", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal Inteligente IBEX 35 - MIGUEL")

# --- 1. LISTA COMPLETA 35 VALORES ---
ibex_35 = [
    "ANA.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", "BKT.MC", "BBVA.MC",
    "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC",
    "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC",
    "ROVI.MC", "SCYR.MC", "SLBA.MC", "TEF.MC", "UNI.MC"
]

# --- 2. BOTÓN DE ESCÁNER TOTAL ---
if st.button('🚀 EJECUTAR ANÁLISIS 360 (SEMÁFOROS Y FILTROS)', use_container_width=True):
    lista_analisis = []
    progreso = st.progress(0)
    status = st.empty()
    
    with st.spinner('Analizando los 35 valores...'):
        for i, t in enumerate(ibex_35):
            try:
                status.text(f"Procesando {t}... ({i+1}/35)")
                # Descarga protegida: solo 1 mes para evitar bloqueos
                df = yf.download(t, period="1mo", interval="1d", progress=False, timeout=5)
                
                if not df.empty and len(df) > 10:
                    precio_act = float(df['Close'].iloc[-1])
                    
                    # CÁLCULO RSI (EL MOTOR DEL SEMÁFORO)
                    delta = df['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rsi = 100 - (100 / (1 + (gain.iloc[-1] / (loss.iloc[-1] + 0.001))))
                    
                    # Clasificación para Filtros
                    if rsi < 35: sem, est = "🟢", "COMPRA"
                    elif rsi > 65: sem, est = "🔴", "RIESGO"
                    else: sem, est = "⚪", "NEUTRO"
                    
                    lista_analisis.append({
                        "ticker": t, "precio": precio_act, "rsi": rsi, 
                        "emoji": sem, "estado": est, "df": df
                    })
                
                # Pausa técnica para que Yahoo no nos bloquee
                time.sleep(0.2)
                progreso.progress((i + 1) / len(ibex_35))
            except:
                continue

    status.empty()

    if lista_analisis:
        df_rank = pd.DataFrame(lista_analisis)
        
        # --- 3. FILTROS Y RANKINGS ---
        st.subheader("🏆 Filtro de Oportunidades (Basado en RSI)")
        c1, c2, c3 = st.columns(3)
        
        with c1:
            mejores = df_rank.sort_values("rsi").head(3)
            st.success("💎 TOP 3 COMPRA")
            for _, r in mejores.iterrows():
                st.write(f"**{r['ticker']}** (RSI: {r['rsi']:.1f})")
        
        with c2:
            st.info(f"📊 Analizados: {len(lista_analisis)}/35")
            st.write("Estado general del mercado.")

        with c3:
            peores = df_rank.sort_values("rsi", ascending=False).head(3)
            st.error("⚠️ TOP 3 RIESGO")
            for _, r in peores.iterrows():
                st.write(f"**{r['ticker']}** (RSI: {r['rsi']:.1f})")

        st.divider()

        # --- 4. CUADRÍCULA DE LOS 35 (GRÁFICOS Y NOTICIAS) ---
        st.subheader("📊 Análisis Individual y Noticias")
        cols = st.columns(3)
        for idx, item in enumerate(lista_analisis):
            with cols[idx % 3]:
                with st.expander(f"{item['emoji']} {item['ticker']}: {item['precio']:.2f}€"):
                    st.write(f"**RSI:** {item['rsi']:.1f} | **Estado:** {item['estado']}")
                    
                    # Gráfico de Velas Interactivo
                    fig = go.Figure(data=[go.Candlestick(
                        x=item['df'].index,
                        open=item['df']['Open'],
                        high=item['df']['High'],
                        low=item['df']['Low'],
                        close=item['df']['Close']
                    )])
                    fig.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Enlace a Noticias
                    n_limpio = item['ticker'].split('.')[0]
                    st.markdown(f"[📰 Noticias de {n_limpio}](https://www.google.com/search?q={n_limpio}+noticias+bolsa&tbm=nws)")

st.divider()
# --- CALCULADORA ---
st.subheader("💰 Calculadora de Operación")
inv = st.number_input("Inversión (€):", value=1000)
