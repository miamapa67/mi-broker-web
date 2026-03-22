import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Miguel Terminal 360 Pro", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

# --- 1. CABECERA ---
st.title("🏹 Terminal Inteligente IBEX 35 - MIGUEL")
st.write("Análisis de Oportunidades, Semáforos y Gráficos en Tiempo Real.")

# --- 2. LISTA OFICIAL (CON EL ORDEN CORREGIDO) ---
ibex_35 = [
    "ANA.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", "BKT.MC", "BBVA.MC",
    "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC",
    "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC",
    "ROVI.MC", "SCYR.MC", "SLBA.MC", "TEF.MC", "UNI.MC"
]

# --- 3. BOTÓN DE ESCÁNER CON SALTO DE ERRORES ---
if st.button('🚀 EJECUTAR ANÁLISIS TOTAL', use_container_width=True):
    lista_analisis = []
    progreso = st.progress(0)
    status_msj = st.empty()
    
    for i, t in enumerate(ibex_35):
        try:
            status_msj.text(f"Analizando {t} ({i+1}/35)...")
            # Descarga rápida con tiempo de espera (timeout) para que no se quede colgado
            df = yf.download(t, period="3mo", interval="1d", progress=False, timeout=5)
            
            if not df.empty and len(df) > 10:
                # Usamos .values[-1] para evitar errores de formato
                precio_act = float(df['Close'].values[-1])
                
                # CÁLCULO RSI
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rsi_val = 100 - (100 / (1 + (gain.values[-1] / (loss.values[-1] + 0.0001))))
                
                # Semáforo
                if rsi_val < 35: sem, est = "🟢", "COMPRA"
                elif rsi_val > 65: sem, est = "🔴", "RIESGO"
                else: sem, est = "⚪", "NEUTRO"
                
                lista_analisis.append({
                    "ticker": t, "precio": precio_act, "rsi": float(rsi_val),
                    "estado": est, "emoji": sem, "df": df
                })
            progreso.progress((i + 1) / len(ibex_35))
        except:
            # SI FALLA UN VALOR (COMO REE), EL ROBOT SIMPLEMENTE PASA AL SIGUIENTE
            continue

    status_msj.empty()

    if lista_analisis:
        # --- 4. FILTROS Y RANKINGS ---
        df_rank = pd.DataFrame(lista_analisis)
        st.subheader("🏆 Filtro de Oportunidades")
        f1, f2, f3 = st.columns(3)
        
        with f1:
            mejores = df_rank.sort_values(by="rsi").head(3)
            st.success("💎 TOP 3: MEJOR COMPRA")
            for _, r in mejores.iterrows():
                st.write(f"· **{r['ticker']}** (RSI: {r['rsi']:.1f})")
        
        with f2:
            st.info(f"⚪ VALORES ANALIZADOS: {len(lista_analisis)}")
            st.write("Datos procesados correctamente.")

        with f3:
            peores = df_rank.sort_values(by="rsi", ascending=False).head(3)
            st.error("⚠️ TOP 3: MÁS RIESGO")
            for _, r in peores.iterrows():
                st.write(f"· **{r['ticker']}** (RSI: {r['rsi']:.1f})")

        st.divider()

        # --- 5. CUADRÍCULA DE LOS 35 ---
        st.subheader("📊 Análisis Detallado")
        cols = st.columns(3)
        for idx, item in enumerate(lista_analisis):
            with cols[idx % 3]:
                with st.expander(f"{item['emoji']} {item['ticker']}: {item['precio']:.2f}€"):
                    st.write(f"RSI: {item['rsi']:.1f} | {item['estado']}")
                    # Gráfico de Velas Japonesas
                    fig = go.Figure(data=[go.Candlestick(
                        x=item['df'].index[-20:],
                        open=item['df']['Open'][-20:],
                        high=item['df']['High'][-20:],
                        low=item['df']['Low'][-20:],
                        close=item['df']['Close'][-20:]
                    )])
                    fig.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
                    # Enlace noticias
                    n_limpio = item['ticker'].split('.')[0]
                    st.markdown(f"[📰 Ver Noticias de {n_limpio}](https://www.google.com/search?q={n_limpio}+noticias+bolsa&tbm=nws)")
    else:
        st.error("⚠️ Error de conexión con Yahoo. Espera 10 segundos y vuelve a pulsar el botón.")

st.divider()
# --- CALCULADORA ---
st.subheader("💰 Simulador de Inversión")
inv = st.number_input("Dinero (€):", value=1000)
