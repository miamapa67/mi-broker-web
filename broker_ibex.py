import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Miguel Terminal 360", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal Inteligente IBEX 35 - MIGUEL")

# --- LISTA OFICIAL IBEX 35 ---
ibex_35 = [
    "ANA.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", "BKT.MC", "BBVA.MC",
    "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC",
    "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC",
    "ROVI.MC", "SCYR.MC", "SLBA.MC", "TEF.MC", "UNI.MC"
]

if st.button('🚀 ACTIVAR ANÁLISIS TOTAL 360', use_container_width=True):
    lista_analisis = []
    progreso = st.progress(0)
    
    with st.spinner('Analizando los 35 del IBEX...'):
        for i, t in enumerate(ibex_35):
            try:
                # Descarga mínima de 1 mes (para que no pese)
                df = yf.download(t, period="1mo", interval="1d", progress=False, timeout=10)
                
                if not df.empty and len(df) > 5:
                    p_act = float(df['Close'].iloc[-1])
                    
                    # Cálculo RSI (Motor del Semáforo)
                    delta = df['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rsi = 100 - (100 / (1 + (gain.iloc[-1] / (loss.iloc[-1] + 0.001))))
                    
                    sem = "🟢" if rsi < 40 else "🔴" if rsi > 60 else "⚪"
                    est = "POTENCIAL" if rsi < 40 else "RIESGO" if rsi > 60 else "NEUTRO"
                    
                    lista_analisis.append({
                        "ticker": t, "precio": p_act, "rsi": rsi, 
                        "emoji": sem, "estado": est, "df": df
                    })
                
                # Pausa de seguridad cada valor
                time.sleep(0.1)
                progreso.progress((i + 1) / len(ibex_35))
            except:
                continue

    if lista_analisis:
        # --- FILTROS Y RANKING ---
        df_rank = pd.DataFrame(lista_analisis)
        st.subheader("🏆 Filtro de Oportunidades")
        c1, c2 = st.columns(2)
        with c1:
            mejores = df_rank.sort_values("rsi").head(3)
            st.success(f"💎 TOP 3 COMPRA: {', '.join(mejores['ticker'].tolist())}")
        with c2:
            peores = df_rank.sort_values("rsi", ascending=False).head(3)
            st.error(f"⚠️ TOP 3 RIESGO: {', '.join(peores['ticker'].tolist())}")

        st.divider()

        # --- RADIOGRAFÍA DE LOS 35 ---
        st.subheader("📊 Gráficos y Noticias Individuales")
        cols = st.columns(3)
        for idx, item in enumerate(lista_analisis):
            with cols[idx % 3]:
                with st.expander(f"{item['emoji']} {item['ticker']}: {item['precio']:.2f}€"):
                    st.write(f"RSI: {item['rsi']:.1f} | {item['estado']}")
                    # Gráfico Interactivo de Velas (Últimos 15 días)
                    fig = go.Figure(data=[go.Candlestick(
                        x=item['df'].index[-15:],
                        open=item['df']['Open'][-15:],
                        high=item['df']['High'][-15:],
                        low=item['df']['Low'][-15:],
                        close=item['df']['Close'][-15:]
                    )])
                    fig.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Radar de Noticias
                    n_limpio = item['ticker'].split('.')[0]
                    st.markdown(f"[📰 Noticias de {n_limpio}](https://www.google.com/search?q={n_limpio}+noticias+bolsa&tbm=nws)")
    else:
        st.error("Error de conexión. Intenta pulsar el botón de nuevo.")

st.divider()
st.subheader("💰 Calculadora")
inv = st.number_input("Dinero (€):", value=1000)
