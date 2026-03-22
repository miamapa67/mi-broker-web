import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Miguel Terminal 360", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal IBEX 360 - MIGUEL")

# --- LISTA COMPLETA 35 VALORES ---
ibex_35 = [
    "ANA.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", "BKT.MC", "BBVA.MC",
    "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC",
    "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC",
    "ROVI.MC", "SCYR.MC", "SLBA.MC", "TEF.MC", "UNI.MC"
]

if st.button('🚀 ACTIVAR ANÁLISIS TOTAL (LOS 35 VALORES)', use_container_width=True):
    lista_analisis = []
    progreso = st.progress(0)
    status = st.empty()
    
    with st.spinner('Conectando con el parqué de Madrid...'):
        for i, t in enumerate(ibex_35):
            try:
                status.text(f"Analizando {t}... ({i+1}/35)")
                # Descargamos solo 1 mes para que sea ultra-rápido y no nos bloqueen
                df = yf.download(t, period="1mo", interval="1d", progress=False)
                
                if not df.empty:
                    p_act = float(df['Close'].iloc[-1])
                    
                    # Cálculo RSI (Semáforo)
                    delta = df['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rsi = 100 - (100 / (1 + (gain.iloc[-1] / (loss.iloc[-1] + 0.001))))
                    
                    color = "🟢" if rsi < 35 else "🔴" if rsi > 65 else "⚪"
                    
                    lista_analisis.append({
                        "ticker": t, "precio": p_act, "rsi": rsi, "emoji": color, "df": df
                    })
                # Pequeña pausa de seguridad para engañar al servidor
                time.sleep(0.1)
                progreso.progress((i + 1) / len(ibex_35))
            except:
                continue

    status.empty()

    if lista_analisis:
        # --- FILTROS DE OPORTUNIDAD ---
        st.subheader("🏆 Oportunidades del IBEX 35")
        df_rank = pd.DataFrame(lista_analisis)
        c1, c2 = st.columns(2)
        with c1:
            mejores = df_rank.sort_values("rsi").head(3)
            st.success(f"💎 POTENCIAL: {', '.join(mejores['ticker'].tolist())}")
        with c2:
            peores = df_rank.sort_values("rsi", ascending=False).head(3)
            st.error(f"⚠️ RIESGO: {', '.join(peores['ticker'].tolist())}")

        st.divider()

        # --- CUADRÍCULA DE LOS 35 ---
        st.subheader("📊 Radiografía Detallada")
        cols = st.columns(3)
        for idx, item in enumerate(lista_analisis):
            with cols[idx % 3]:
                with st.expander(f"{item['emoji']} {item['ticker']}: {item['precio']:.2f}€"):
                    st.write(f"RSI: {item['rsi']:.1f}")
                    # Gráfico rápido
                    fig = go.Figure(data=[go.Scatter(x=item['df'].index, y=item['df']['Close'], mode='lines')])
                    fig.update_layout(height=120, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown(f"[📰 Noticias](https://www.google.com/search?q={item['ticker'].split('.')[0]}+noticias+bolsa&tbm=nws)")
    else:
        st.error("❌ El bloqueo de Yahoo persiste. Inténtalo de nuevo en unos minutos.")

st.divider()
st.subheader("💰 Simulador Rápido")
inv = st.number_input("Capital (€):", value=1000)
