import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import time
import datetime

st.set_page_config(page_title="Miguel Terminal ELITE", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal de Inteligencia IBEX 35: Señales de Élite")
st.write(f"Análisis técnico de alta precisión. Actualizado: {datetime.datetime.now().strftime('%H:%M:%S')}")

# --- 1. LISTA OFICIAL 35 VALORES ---
ibex_35 = [
    "ANA.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", "BKT.MC", "BBVA.MC",
    "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC",
    "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC",
    "ROVI.MC", "SCYR.MC", "SLBA.MC", "TEF.MC", "UNI.MC"
]

# --- 2. MOTOR DE ANÁLISIS ---
if st.button('🚀 EJECUTAR ESCÁNER DE ALTA PRECISIÓN 35', use_container_width=True):
    lista_analisis = []
    progreso = st.progress(0)
    status_msg = st.empty()
    
    with st.spinner('Procesando los 35 valores y generando gráficos interactivos...'):
        for i, t in enumerate(ibex_35):
            try:
                status_msg.text(f"Analizando {t}... ({i+1}/35)")
                tk = yf.Ticker(t)
                df = tk.history(period="3mo", interval="1d") 
                
                if not df.empty and len(df) >= 20:
                    # PRECIO Y VARIACIÓN 20D
                    p_act = df['Close'].iloc[-1]
                    p_ini_20 = df['Close'].iloc[-20]
                    var_20d = ((p_act - p_ini_20) / p_ini_20) * 100
                    
                    # CÁLCULO RSI (Semáforo)
                    delta = df['Close'].diff()
                    up = delta.clip(lower=0).rolling(window=14).mean()
                    down = -1 * delta.clip(upper=0).rolling(window=14).mean()
                    rs = up.iloc[-1] / (down.iloc[-1] + 0.00001)
                    rsi = 100 - (100 / (1 + rs))
                    
                    # Semáforo
                    if rsi < 38: sem, col = "🟢 COMPRA", "green"
                    elif rsi > 62: sem, col = "🔴 RIESGO", "red"
                    else: sem, col = "⚪ NEUTRO", "gray"
                    
                    lista_analisis.append({
                        "ticker": t, "precio": round(p_act, 2), "rsi": round(rsi, 1),
                        "var20": round(var_20d, 2), "emoji": sem, "df": df
                    })
                
                time.sleep(0.05)
                progreso.progress((i + 1) / len(ibex_35))
            except: continue

    status_msg.empty()

    if lista_analisis:
        df_rank = pd.DataFrame(lista_analisis)
        
        # --- 3. TOP 3: EL CENTRO DE MANDO (CON GRÁFICOS INTERACTIVOS) ---
        st.subheader("🚥 SEMÁFORO: TOP 3 MEJORES OPORTUNIDADES DE COMPRA")
        # El criterio es el RSI más bajo (más barato/sobrevendido)
        top_compra = df_rank.sort_values("rsi").head(3)
        c_top = st.columns(3)
        
        for idx, (index, r) in enumerate(top_compra.iterrows()):
            with c_top[idx]:
                # Tarjeta Profesional con Borde
                with st.container(border=True):
                    st.success(f"💎 OPCIÓN {idx+1}: {r['ticker']}")
                    
                    # Métricas destacadas
                    m1, m2 = st.columns(2)
                    with m1:
                        st.metric("Precio", f"{r['precio']}€", f"{r['var20']}% (1m)")
                    with m2:
                        st.write(f"**RSI (Fuerza):** {r['rsi']} (Sobreventa)")
                        name_link = r['ticker'].split('.')[0]
                        st.link_button("📰 Ver Noticias", f"https://www.google.com/search?q={name_link}+noticias+bolsa&tbm=nws", use_container_width=True)
                    
                    st.write("---")
                    
                    # --- GRÁFICO DE VELAS INTERACTIVO (PROFESIONAL) ---
                    df_plot = r['df'].tail(25) # Mostramos un poco más (25 días)
                    fig = go.Figure(data=[go.Candlestick(
                        x=df_plot.index, open=df_plot['Open'], high=df_plot['High'],
                        low=df_plot['Low'], close=df_plot['Close']
                    )])
                    fig.update_layout(
                        height=220, 
                        margin=dict(l=0,r=0,t=0,b=0), 
                        xaxis_rangeslider_visible=False,
                        xaxis_visible=False,
                        template="plotly_white"
                    )
                    st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # --- 4. RADIOGRAFÍA DETALLADA DE LOS 35 ---
        st.subheader("📊 Análisis Individual de los 35 Valores")
        cols = st.columns(3)
        for idx, item in enumerate(lista_analisis):
            with cols[idx % 3]:
                with st.expander(f"{item['emoji']} {item['ticker']} - {item['precio']}€"):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.write(f"**RSI:** {item['rsi']}")
                        st.write(f"**Var 20d:** {item['var20']}%")
                    with c2:
                        nombre_not = item['ticker'].split('.')[0]
                        st.link_button("📰 Noticias", f"https://www.google.com/search?q={nombre_not}+noticias+bolsa&tbm=nws")
                    
                    # Gráfico mini (más pequeño que en el Top 3)
                    df_plot_mini = item['df'].tail(15)
                    fig_mini = go.Figure(data=[go.Scatter(x=df_plot_mini.index, y=df_plot_mini['Close'], mode='lines', line=dict(color='blue'))])
                    fig_mini.update_layout(height=120, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False)
                    st.plotly_chart(fig_mini, use_container_width=True)
    else:
        st.error("Error de conexión. Intenta pulsar de nuevo.")

# Calculadora lateral
st.sidebar.subheader("💰 Calculadora Miguel")
inv = st.sidebar.number_input("Inversión (€):", value=1000)
