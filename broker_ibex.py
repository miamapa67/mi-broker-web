import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import os

# Configuración básica
st.set_page_config(page_title="Miguel Terminal 360", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal IBEX 360 - MIGUEL")

# Lista reducida para probar que funciona (luego pondremos los 35)
ibex_test = ["SAN.MC", "BBVA.MC", "TEF.MC", "REP.MC", "ITX.MC", "GRF.MC"]

if st.button('🚀 PROBAR CONEXIÓN Y ANÁLISIS', use_container_width=True):
    lista_analisis = []
    
    with st.spinner('Conectando con Madrid...'):
        for t in ibex_test:
            try:
                # Descarga ultra-simple
                df = yf.download(t, period="3mo", interval="1d", progress=False)
                
                if not df.empty:
                    # Usamos .iloc[-1] con valores planos para evitar errores de formato
                    precio_act = float(df['Close'].values[-1])
                    
                    # Cálculo RSI básico
                    delta = df['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    rsi_val = 100 - (100 / (1 + rs.values[-1]))
                    
                    color = "🟢" if rsi_val < 35 else "🔴" if rsi_val > 65 else "⚪"
                    
                    lista_analisis.append({
                        "ticker": t, "precio": precio_act, "rsi": float(rsi_val), "emoji": color, "df": df
                    })
            except:
                continue

    if lista_analisis:
        cols = st.columns(3)
        for i, item in enumerate(lista_analisis):
            with cols[i % 3]:
                with st.expander(f"{item['emoji']} {item['ticker']}: {item['precio']:.2f}€"):
                    st.write(f"**RSI (Fuerza):** {item['rsi']:.1f}")
                    # Gráfico rápido
                    fig = go.Figure(data=[go.Scatter(x=item['df'].index, y=item['df']['Close'], mode='lines')])
                    fig.update_layout(height=150, margin=dict(l=0,r=0,t=0,b=0))
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown(f"[📰 Noticias](https://www.google.com/search?q={item['ticker'].split('.')[0]}+noticias+bolsa&tbm=nws)")
    else:
        st.error("No se han podido recibir datos. Reintentando conexión...")

st.divider()
st.subheader("💰 Simulador Rápido")
inv = st.number_input("Dinero (€):", value=1000)
st.write(f"Simulador listo para {inv}€")
