import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Miguel Terminal PRO", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal Inteligente IBEX 35 - MIGUEL")

# --- DICCIONARIO POR SECTORES ---
sectores = {
    "Banca": ["SAN.MC", "BBVA.MC", "CABK.MC", "SAB.MC", "BKT.MC", "UNI.MC"],
    "Energía": ["IBE.MC", "REP.MC", "NTGY.MC", "ELE.MC", "ENG.MC", "REE.MC", "SLBA.MC"],
    "Ind. y Consumo": ["ITX.MC", "ANA.MC", "ACS.MC", "FER.MC", "ACX.MC", "MTS.MC", "IAG.MC", "PUIG.MC"],
    "Tecno y Telco": ["TEF.MC", "CLNX.MC", "IDR.MC", "AMS.MC"],
    "Otros (Farma/Inmo)": ["GRF.MC", "ROVI.MC", "COL.MC", "MRL.MC", "LOG.MC", "AENA.MC", "SCYR.MC", "FDR.MC", "MEL.MC"]
}

# Filtro en la barra lateral
st.sidebar.header("🎯 Filtros de Mercado")
sector_sel = st.sidebar.multiselect("Seleccionar Sectores:", list(sectores.keys()), default=list(sectores.keys()))

# Crear lista plana de tickers seleccionados
tickers_finales = []
for s in sector_sel:
    tickers_finales.extend(sectores[s])

if st.button('🚀 ACTIVAR ESCÁNER 360 (SEMÁFOROS Y RANKING)', use_container_width=True):
    lista_analisis = []
    progreso = st.progress(0)
    
    with st.spinner('Analizando el IBEX por sectores...'):
        for i, t in enumerate(tickers_finales):
            try:
                # TRUCO: Pedimos solo 1 mes para evitar que Yahoo nos detecte como bot pesado
                df = yf.download(t, period="1mo", interval="1d", progress=False, timeout=7)
                
                if not df.empty and len(df) > 10:
                    p_act = float(df['Close'].iloc[-1])
                    # Cálculo RSI (Semáforo)
                    delta = df['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rsi = 100 - (100 / (1 + (gain.iloc[-1] / (loss.iloc[-1] + 0.001))))
                    
                    sem = "🟢" if rsi < 35 else "🔴" if rsi > 65 else "⚪"
                    est = "OPORTUNIDAD" if rsi < 35 else "RIESGO" if rsi > 65 else "NEUTRO"
                    
                    lista_analisis.append({
                        "ticker": t, "precio": p_act, "rsi": rsi, "emoji": sem, "estado": est, "df": df
                    })
                time.sleep(0.1) # Pausa anti-bloqueo
                progreso.progress((i + 1) / len(tickers_finales))
            except:
                continue

    if lista_analisis:
        df_rank = pd.DataFrame(lista_analisis)
        
        # --- TOP 3 DE COMPRA Y RIESGO ---
        st.subheader("🏆 Ranking de Selección Inteligente")
        c1, c2 = st.columns(2)
        with c1:
            mejores = df_rank.sort_values("rsi").head(3)
            st.success("💎 TOP 3: MEJORES PARA COMPRAR (RSI BAJO)")
            for _, r in mejores.iterrows():
                st.write(f"{r['emoji']} **{r['ticker']}** - Precio: {r['precio']:.2f}€ (RSI: {r['rsi']:.1f})")
        with c2:
            peores = df_rank.sort_values("rsi", ascending=False).head(3)
            st.error("⚠️ TOP 3: VALORES EN RIESGO (RSI ALTO)")
            for _, r in peores.iterrows():
                st.write(f"{r['emoji']} **{r['ticker']}** - Precio: {r['precio']:.2f}€ (RSI: {r['rsi']:.1f})")

        st.divider()

        # --- CUADRÍCULA CON GRÁFICOS Y NOTICIAS ---
        st.subheader("📊 Análisis por Valor")
        cols = st.columns(3)
        for idx, item in enumerate(lista_analisis):
            with cols[idx % 3]:
                with st.expander(f"{item['emoji']} {item['ticker']} - {item['precio']:.2f}€", expanded=True):
                    st.write(f"Estado: **{item['estado']}** (RSI: {item['rsi']:.1f})")
                    # Gráfico mini de velas
                    fig = go.Figure(data=[go.Candlestick(x=item['df'].index[-15:], open=item['df']['Open'][-15:], high=item['df']['High'][-15:], low=item['df']['Low'][-15:], close=item['df']['Close'][-15:])])
                    fig.update_layout(height=150, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
                    # Noticias
                    t_clean = item['ticker'].split('.')[0]
                    st.markdown(f"[📰 Noticias {t_clean}](https://www.google.com/search?q={t_clean}+noticias+bolsa&tbm=nws)")
    else:
        st.error("⚠️ El servidor de datos sigue bloqueado. Espera 1 minuto y pulsa de nuevo.")

st.divider()
st.subheader("💰 Calculadora de Inversión")
inv = st.number_input("Capital (€):", value=1000)
