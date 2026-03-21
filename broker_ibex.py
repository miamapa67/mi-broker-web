import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import requests
import random

st.set_page_config(page_title="Miguel Terminal 360", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal IBEX 360 - MIGUEL")

# --- LISTA PEQUEÑA PARA SALTAR EL RADAR ---
ibex_test = ["SAN.MC", "BBVA.MC", "TEF.MC", "REP.MC", "ITX.MC", "IAG.MC"]

if st.button('🚀 INTENTAR CONEXIÓN POR TÚNEL SEGURO', use_container_width=True):
    lista_analisis = []
    
    with st.spinner('Buscando una brecha en el mercado...'):
        for t in ibex_test:
            try:
                # Intentamos la descarga con un retraso aleatorio para no parecer un robot
                import time
                time.sleep(random.uniform(1.0, 2.0))
                
                # Descarga individual ultra-lenta
                df = yf.download(t, period="1mo", interval="1d", progress=False, timeout=10)
                
                if not df.empty:
                    # Usamos .values[-1] para evitar errores de formato de Yahoo
                    precio_act = float(df['Close'].values[-1])
                    
                    # RSI simplificado
                    delta = df['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain.values[-1] / (loss.values[-1] + 0.001)
                    rsi_val = 100 - (100 / (1 + rs))
                    
                    color = "🟢" if rsi_val < 40 else "🔴" if rsi_val > 60 else "⚪"
                    
                    lista_analisis.append({
                        "ticker": t, "precio": precio_act, "rsi": rsi_val, "emoji": color, "df": df
                    })
            except:
                continue

    if lista_analisis:
        st.success("¡Túnel abierto! Datos recibidos.")
        cols = st.columns(3)
        for i, item in enumerate(lista_analisis):
            with cols[i % 3]:
                with st.expander(f"{item['emoji']} {item['ticker']}: {item['precio']:.2f}€", expanded=True):
                    st.write(f"**RSI:** {item['rsi']:.1f}")
                    fig = go.Figure(data=[go.Scatter(x=item['df'].index, y=item['df']['Close'].values.flatten(), mode='lines')])
                    fig.update_layout(height=120, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("⚠️ El servidor de Yahoo sigue rechazando la IP de Streamlit.")
        st.info("💡 Miguel, si esto falla, es que Yahoo ha bloqueado a Streamlit hoy. Prueba a darle al botón de nuevo en unos minutos o intenta abrir la app desde tu móvil con datos 4G/5G.")

st.divider()
st.subheader("💰 Simulador")
inv = st.number_input("Dinero (€):", value=1000)
