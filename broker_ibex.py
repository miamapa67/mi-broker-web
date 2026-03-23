import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Miguel Terminal PRO", layout="wide")
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
    
    with st.spinner('Analizando los 35 valores y noticias de última hora...'):
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
        
        # --- 3. TOP 3: SEÑALES DE COMPRA CON NOTICIAS ---
        st.subheader("🚥 TOP 3: MEJORES SEÑALES DE COMPRA DEL DÍA")
        # El criterio es el RSI más bajo (más sobrevendido)
        top_compra = df_res.sort_values("RSI").head(3)
        c_top = st.columns(3)
        
        for idx, (index, r) in enumerate(top_compra.iterrows()):
            with c_top[idx]:
                # Tarjeta de Éxito
                with st.container(border=True):
                    st.success(f"🥇 OPCIÓN {idx+1}: {r['Ticker']}")
                    st.metric("Precio Actual", f"{r['Precio']}€", f"{r['Var20']}% (20d)")
                    st.write(f"**Fuerza RSI:** {r['RSI']} (Oportunidad)")
                    
                    # Botón de Noticias específico para el Top 3
                    nombre_top = r['Ticker'].split('.')[0]
                    st.link_button(f"📰 Ver Noticias de {nombre_top}", 
                                   f"https://www.google.com/search?q={nombre_top}+noticias+bolsa&tbm=nws",
                                   use_container_width=True)

        st.divider()

        # --- 4. DESGLOSE INTERACTIVO DE LOS 35 ---
        st.subheader("📊 Radiografía Completa de los 35 Valores")
        cols = st.columns(3)
        
        for idx, item in enumerate(resultados):
            with cols[idx % 3]:
                with st.expander(f"{item['Sem']} | {item['Ticker']} - {item['Precio']}€"):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.write(f"**RSI:** {item['RSI']}")
                        st.write(f"**Var 20d:** {item['Var20']}%")
                    with c2:
                        name_link = item['Ticker'].split('.')[0]
                        st.link_button("📰 Noticias", f"https://www.google.com/search?q={name_link}+noticias+bolsa&tbm=nws")
                    
                    # Gráfico de Velas Interactivo
                    df_plot = item['df'].tail(20)
                    fig = go.Figure(data=[go.Candlestick(
                        x=df_plot.index, open=df_plot['Open'], high=df_plot['High'],
                        low=df_plot['Low'], close=df_plot['Close']
                    )])
                    fig.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
                    st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("Error al obtener datos. Reintenta en unos segundos.")

# Calculadora lateral
st.sidebar.subheader("💰 Calculadora")
inv = st.sidebar.number_input("Inversión (€):", value=1000)
