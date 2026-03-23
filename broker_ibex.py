import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Miguel Terminal Interactiva", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal Inteligente IBEX 35: Análisis 360°")

# --- 1. LISTA OFICIAL 35 ---
ibex_35 = [
    "ANA.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", "BKT.MC", "BBVA.MC",
    "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC",
    "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC",
    "ROVI.MC", "SCYR.MC", "SLBA.MC", "TEF.MC", "UNI.MC"
]

# --- 2. MOTOR DE ANÁLISIS ---
if st.button('🚀 EJECUTAR ESCÁNER INTERACTIVO 35 VALORES', use_container_width=True):
    resultados = []
    progreso = st.progress(0)
    status = st.empty()
    
    with st.spinner('Procesando gráficos y datos técnicos...'):
        for i, t in enumerate(ibex_35):
            try:
                status.text(f"Analizando {t}...")
                tk = yf.Ticker(t)
                df = tk.history(period="3mo", interval="1d") 
                
                if not df.empty and len(df) >= 20:
                    p_act = df['Close'].iloc[-1]
                    p_ini_20 = df['Close'].iloc[-20]
                    var_20d = ((p_act - p_ini_20) / p_ini_20) * 100
                    
                    # Cálculo RSI 14
                    delta = df['Close'].diff()
                    gain = delta.where(delta > 0, 0).rolling(window=14).mean().iloc[-1]
                    loss = -delta.where(delta < 0, 0).rolling(window=14).mean().iloc[-1]
                    rsi = 100 - (100 / (1 + (gain / (loss + 0.0001))))
                    
                    # Semáforo
                    if rsi < 35: sem, col = "🟢 COMPRA", "green"
                    elif rsi > 65: sem, col = "🔴 RIESGO", "red"
                    else: sem, col = "⚪ NEUTRO", "gray"
                    
                    resultados.append({
                        "Ticker": t, "Precio": round(p_act, 2), "RSI": round(rsi, 1),
                        "Var20": round(var_20d, 2), "Sem": sem, "Col": col, "df": df
                    })
                
                time.sleep(0.05)
                progreso.progress((i + 1) / len(ibex_35))
            except: continue

    status.empty()

    if resultados:
        df_res = pd.DataFrame(resultados)
        
        # --- 3. TOP 3: SEMÁFORO DE COMPRA ---
        st.subheader("🚥 TOP 3: SEÑALES DE COMPRA DEL DÍA")
        top_compra = df_res.sort_values("RSI").head(3)
        c_top = st.columns(3)
        for idx, (_, r) in enumerate(top_compra.iterrows()):
            with c_top[idx]:
                st.success(f"💎 {r['Ticker']} - {r['Precio']}€")
                st.write(f"RSI: {r['RSI']} | Var 20d: {r['Var20']}%")

        st.divider()

        # --- 4. DESGLOSE INTERACTIVO DE LOS 35 ---
        st.subheader("📊 Radiografía Completa de los 35 Valores")
        
        # Creamos columnas para que no sea una lista infinita
        cols = st.columns(3)
        
        for idx, item in enumerate(resultados):
            with cols[idx % 3]:
                # Cada valor es un Expander (Acordeón) que puedes pinchar
                with st.expander(f"{item['Sem']} | {item['Ticker']} - {item['Precio']}€"):
                    # Datos Clave
                    c1, c2 = st.columns(2)
                    with c1:
                        st.metric("Precio Actual", f"{item['Precio']}€")
                        st.write(f"**Fuerza RSI:** {item['RSI']}")
                    with c2:
                        st.metric("Tendencia 20d", f"{item['Var20']}%")
                        name_link = item['Ticker'].split('.')[0]
                        st.link_button("📰 Ver Noticias", f"https://www.google.com/search?q={name_link}+noticias+bolsa&tbm=nws")
                    
                    # Gráfico Interactivo de Velas (Últimos 20 días)
                    df_plot = item['df'].tail(20)
                    fig = go.Figure(data=[go.Candlestick(
                        x=df_plot.index,
                        open=df_plot['Open'],
                        high=df_plot['High'],
                        low=df_plot['Low'],
                        close=df_plot['Close'],
                        name="Velas"
                    )])
                    fig.update_layout(
                        height=250, 
                        margin=dict(l=0, r=0, t=0, b=0),
                        xaxis_rangeslider_visible=False,
                        template="plotly_white"
                    )
                    st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("Error al obtener datos. Reintenta en unos segundos.")

# Calculadora lateral
st.sidebar.subheader("💰 Calculadora")
inv = st.sidebar.number_input("Inversión (€):", value=1000)
