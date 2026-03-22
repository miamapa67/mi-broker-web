import streamlit as st
import yfinance as yf
import pandas as pd
from PIL import Image
import os

st.set_page_config(page_title="Miguel Terminal 360", layout="wide")

# Estilo Blanco Nítido
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

# --- 1. CABECERA ---
if os.path.exists("logo_miguel.png"):
    img = Image.open("logo_miguel.png")
    st.image(img, use_column_width=True)

st.title("🏹 Terminal 360 - MIGUEL")
st.write("Semáforo de Inversión + Dividendos + Radar de Noticias.")

# --- 2. MOTOR DE ANÁLISIS TOTAL ---
tickers = ["SAN.MC", "BBVA.MC", "TEF.MC", "IBE.MC", "ITX.MC", "REP.MC", "CABK.MC", "SAB.MC", "GRF.MC"]

if st.button('🚀 EJECUTAR ANÁLISIS COMPLETO', use_container_width=True):
    st.subheader("📊 Panel de Oportunidades")
    
    with st.spinner('Calculando señales y dividendos...'):
        for t in tickers:
            try:
                tk = yf.Ticker(t)
                # Necesitamos 3 meses para el RSI
                hist = tk.history(period="3mo")
                if hist.empty: continue
                
                precio_actual = float(hist['Close'].iloc[-1])
                
                # --- CÁLCULO DEL SEMÁFORO (RSI) ---
                delta = hist['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi_val = 100 - (100 / (1 + rs.iloc[-1]))
                
                if rsi_val > 70: color, est = "#fef2f2", "🔴 PELIGRO (CARO)"
                elif rsi_val < 30: color, est = "#f0fdf4", "🟢 OPORTUNIDAD (COMPRA)"
                else: color, est = "#f8fafc", "⚪ NEUTRO"

                # --- BUSCAR DIVIDENDO ---
                div_yield = tk.info.get('dividendYield', 0)
                if not div_yield:
                    divs = tk.dividends
                    if not divs.empty: div_yield = (divs.iloc[-1] * 2) / precio_actual 
                div_final = (div_yield * 100) if div_yield else 0

                # --- NOTICIAS ---
                nombre_corto = t.split('.')[0]
                link_noticias = f"https://www.google.com/search?q={nombre_corto}+noticias+bolsa&tbm=nws"

                # MOSTRAR TARJETA
                with st.expander(f"📉 {t}: {precio_actual:.2f}€ | {est}", expanded=True):
                    c1, c2 = st.columns([1, 1.5])
                    with c1:
                        st.metric("Precio", f"{precio_actual:.2f}€")
                        st.write(f"**RSI (Riesgo):** {rsi_val:.1f}")
                        if div_final > 0:
                            st.markdown(f"<span style='color:green;'><b>💰 Dividendo: {div_final:.2f}%</b></span>", unsafe_allow_html=True)
                    
                    with c2:
                        st.write("**📰 Información y Noticias:**")
                        st.markdown(f"• [👉 Ver Noticias de {nombre_corto}]({link_noticias})")
                        st.markdown(f"• [📊 Gráfico Real en Google Finance](https://www.google.com/finance/quote/{t.replace('.MC', ':BME')})")

            except: continue

st.divider()

# --- 3. CALCULADORA ---
st.subheader("💰 Simulador de Ganancia Neta")
c1, c2 = st.columns(2)
with c1:
    inver = st.number_input("Dinero a invertir (€):", value=1000, step=500)
    acc_elegida = st.selectbox("Acción:", tickers)
    sub_obj = st.slider("Subida esperada (%)", 1, 30, 5)

with c2:
    try:
        p_v = float(yf.Ticker(acc_elegida).history(period="1d")['Close'].iloc[-1])
        n_acc = int(inver / p_v)
        gan_estimada = (p_v * (sub_obj/100)) * n_acc
        st.success(f"**Resultado: Ganarías +{gan_estimada:.2f}€**")
    except: st.write("Calculando...")
