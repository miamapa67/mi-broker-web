import streamlit as st
import yfinance as yf
import pandas as pd
from PIL import Image
import os

st.set_page_config(page_title="Miguel Terminal Pro", layout="wide")

# Estilo Blanco Nítido
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

# --- 1. CABECERA ---
if os.path.exists("logo_miguel.png"):
    img = Image.open("logo_miguel.png")
    st.image(img, use_column_width=True)

st.title("🏹 Terminal Financiera - MIGUEL")

# --- 2. MOTOR DE ANÁLISIS MEJORADO ---
tickers = ["SAN.MC", "BBVA.MC", "TEF.MC", "IBE.MC", "ITX.MC", "REP.MC", "CABK.MC", "SAB.MC", "GRF.MC"]

if st.button('🚀 EJECUTAR ANÁLISIS Y BUSCAR NOTICIAS', use_container_width=True):
    st.subheader("📊 Panel de Control en Tiempo Real")
    
    with st.spinner('Escaneando prensa y cotizaciones...'):
        for t in tickers:
            try:
                tk = yf.Ticker(t)
                hist = tk.history(period="3mo")
                if hist.empty: continue
                
                precio_actual = float(hist['Close'].iloc[-1])
                
                # RSI para el semáforo
                delta = hist['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi_val = 100 - (100 / (1 + rs.iloc[-1]))
                
                # Estado visual
                if rsi_val > 70: est = "🔴 SOBRECOMPRA"
                elif rsi_val < 30: est = "🟢 OPORTUNIDAD"
                else: est = "⚪ NEUTRO"
                
                # MOSTRAR TARJETA
                with st.expander(f"📈 {t}: {precio_actual:.2f}€ | {est}", expanded=True):
                    c1, c2 = st.columns([1, 2])
                    with c1:
                        st.metric("Precio", f"{precio_actual:.2f}€")
                        st.caption(f"RSI: {rsi_val:.1f}")
                    
                    with c2:
                        st.write("**📰 Radar de Noticias:**")
                        news = tk.news
                        if news and len(news) > 0:
                            for n in news[:2]: # Mostramos las 2 primeras si existen
                                st.markdown(f"• [{n['title']}]({n['link']})")
                        else:
                            # PLAN B: Enlace directo a Google News si Yahoo falla
                            nombre_limpio = t.split('.')[0]
                            st.info(f"🔍 Yahoo no responde. Pulsa aquí:")
                            st.markdown(f"[👉 Ver últimas noticias de {nombre_limpio} en Google News](https://www.google.com/search?q={nombre_limpio}+noticias+bolsa&tbm=nws)")

            except Exception as e:
                continue

st.divider()

# --- 3. CALCULADORA ---
st.subheader("💰 Simulador de Beneficios")
c1, c2 = st.columns(2)
with c1:
    inver = st.number_input("Dinero a invertir (€):", value=1000, step=100)
    acc = st.selectbox("Valor elegido:", tickers)
    sub = st.slider("Subida objetivo (%)", 1, 25, 5)
with c2:
    try:
        p_v = float(yf.Ticker(acc).history(period="1d")['Close'].iloc[-1])
        n = int(inver / p_v)
        gan = (p_v * (sub/100)) * n
        st.success(f"**Ganancia estimada: +{gan:.2f}€**")
    except: st.write("Cargando...")
