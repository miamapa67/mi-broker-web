import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Miguel Terminal PRO", layout="wide")

# Estilo Limpio Profesional
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal Inteligente IBEX 35 - MIGUEL")

# --- 1. ESTRUCTURA DE SECTORES (FILTROS) ---
sectores = {
    "Banca": ["SAN.MC", "BBVA.MC", "CABK.MC", "SAB.MC", "BKT.MC", "UNI.MC"],
    "Energía": ["IBE.MC", "REP.MC", "NTGY.MC", "ELE.MC", "ENG.MC", "REE.MC", "SLBA.MC"],
    "Ind. y Consumo": ["ITX.MC", "ANA.MC", "ACS.MC", "FER.MC", "ACX.MC", "MTS.MC", "IAG.MC", "PUIG.MC"],
    "Tecno y Telco": ["TEF.MC", "CLNX.MC", "IDR.MC", "AMS.MC"],
    "Otros": ["GRF.MC", "ROVI.MC", "COL.MC", "MRL.MC", "LOG.MC", "AENA.MC", "SCYR.MC", "FDR.MC", "MEL.MC"]
}

# Filtro lateral interactivo
st.sidebar.header("🎯 Filtros de Selección")
sector_sel = st.sidebar.multiselect("Seleccionar Sectores:", list(sectores.keys()), default=list(sectores.keys()))

tickers_finales = []
for s in sector_sel:
    tickers_finales.extend(sectores[s])

# --- 2. MOTOR DE ANÁLISIS ---
if st.button('🚀 LANZAR ANÁLISIS 360 (RANKING Y SEMÁFOROS)', use_container_width=True):
    lista_analisis = []
    progreso = st.progress(0)
    status_text = st.empty()
    
    with st.spinner('Escaneando el IBEX...'):
        for i, t in enumerate(tickers_finales):
            try:
                status_text.text(f"Analizando {t}... ({i+1}/{len(tickers_finales)})")
                
                # Descarga rápida de 1 mes
                df = yf.download(t, period="1mo", interval="1d", progress=False)
                
                if not df.empty and len(df) > 10:
                    p_act = float(df['Close'].iloc[-1])
                    
                    # Cálculo RSI (Semáforo Automático)
                    delta = df['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rsi = 100 - (100 / (1 + (gain.iloc[-1] / (loss.iloc[-1] + 0.0001))))
                    
                    # Clasificación
                    sem = "🟢" if rsi < 40 else "🔴" if rsi > 60 else "⚪"
                    est = "COMPRA" if rsi < 40 else "RIESGO" if rsi > 60 else "NEUTRO"
                    
                    lista_analisis.append({
                        "ticker": t, "precio": p_act, "rsi": rsi, "emoji": sem, "estado": est, "df": df
                    })
                
                time.sleep(0.2) # Pausa estratégica anti-bloqueo
                progreso.progress((i + 1) / len(tickers_finales))
            except:
                continue

    status_text.empty()

    if lista_analisis:
        df_rank = pd.DataFrame(lista_analisis)
        
        # --- 3. RANKING TOP 3 (COMPRA Y RIESGO) ---
        st.subheader("🏆 Selección Inteligente de Hoy")
        c1, c2 = st.columns(2)
        with c1:
            mejores = df_rank.sort_values("rsi").head(3)
            st.success("💎 TOP 3: MEJOR OPORTUNIDAD (RSI Bajo)")
            for _, r in mejores.iterrows():
                st.write(f"{r['emoji']} **{r['ticker']}**: {r['precio']:.2f}€ (RSI: {r['rsi']:.1f})")
        with c2:
            peores = df_rank.sort_values("rsi", ascending=False).head(3)
            st.error("⚠️ TOP 3: MAYOR RIESGO (RSI Alto)")
            for _, r in peores.iterrows():
                st.write(f"{r['emoji']} **{r['ticker']}**: {r['precio']:.2f}€ (RSI: {r['rsi']:.1f})")

        st.divider()

        # --- 4. RADIOGRAFÍA INDIVIDUAL Y NOTICIAS ---
        st.subheader("📊 Análisis por Valor")
        cols = st.columns(3)
        for idx, item in enumerate(lista_analisis):
            with cols[idx % 3]:
                with st.expander(f"{item['emoji']} {item['ticker']} - {item['precio']:.2f}€"):
                    st.write(f"Estado: **{item['estado']}** | RSI: {item['rsi']:.1f}")
                    # Gráfico de Línea
                    fig = go.Figure(data=[go.Scatter(x=item['df'].index[-15:], y=item['df']['Close'][-15:], mode='lines+markers')])
                    fig.update_layout(height=140, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
                    # Noticias
                    nombre_corto = item['ticker'].split('.')[0]
                    st.markdown(f"[📰 Noticias {nombre_corto}](https://www.google.com/search?q={nombre_corto}+noticias+bolsa&tbm=nws)")
    else:
        st.error("❌ El servidor de bolsa sigue bloqueado. Intenta de nuevo en unos minutos.")

st.divider()
st.subheader("💰 Calculadora Rápida")
inv = st.number_input("Inversión (€):", value=1000)
