import streamlit as st
import yfinance as yf
import pandas as pd
from PIL import Image
import os

st.set_page_config(page_title="Miguel Terminal Pro", layout="wide")

# Estilo Blanco Nítido
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

# --- 1. CABECERA CON TU LOGO ---
if os.path.exists("logo_miguel.png"):
    img = Image.open("logo_miguel.png")
    st.image(img, use_column_width=True)

st.title("🏹 Terminal Financiera - MIGUEL")
st.write("Precio en tiempo real + RSI + Noticias de última hora.")

# --- 2. MOTOR DE ANÁLISIS ---
tickers = ["SAN.MC", "BBVA.MC", "TEF.MC", "IBE.MC", "ITX.MC", "REP.MC", "CABK.MC", "SAB.MC", "GRF.MC"]

if st.button('🚀 EJECUTAR ANÁLISIS COMPLETO', use_container_width=True):
    st.subheader("📊 Cotizaciones y Noticias")
    
    with st.spinner('Actualizando precios de Madrid...'):
        for t in tickers:
            try:
                tk = yf.Ticker(t)
                hist = tk.history(period="3mo")
                if hist.empty: continue
                
                # PRECIO ACTUAL (Lo hacemos bien visible)
                precio_actual = float(hist['Close'].iloc[-1])
                
                # Cálculo de RSI
                delta = hist['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi_val = 100 - (100 / (1 + rs.iloc[-1]))
                
                # Color y Estado
                if rsi_val > 70: estado = "🔴 SOBRECOMPRA"
                elif rsi_val < 30: estado = "🟢 OPORTUNIDAD"
                else: estado = "⚪ NEUTRO"
                
                # LA TARJETA CON EL PRECIO BIEN GRANDE EN EL TÍTULO
                with st.expander(f"📈 {t}: {precio_actual:.2f}€ | {estado}", expanded=True):
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.metric(label="Precio Actual", value=f"{precio_actual:.2f}€")
                        st.write(f"**RSI:** {rsi_val:.1f}")
                        div = tk.info.get('dividendYield', 0)
                        if div: st.write(f"💰 **Div:** {div*100:.2f}%")
                    
                    with col2:
                        st.write("**📰 Noticias recientes:**")
                        news = tk.news[:2]
                        if news:
                            for n in news:
                                st.markdown(f"• [{n['title']}]({n['link']})")
                        else:
                            st.write("No hay noticias hoy.")
                            
            except: continue

st.divider()

# --- 3. CALCULADORA (SE MANTIENE) ---
st.subheader("💰 Simulador de Beneficios")
c1, c2 = st.columns(2)
with c1:
    inver = st.number_input("Dinero (€):", value=1000)
    acc = st.selectbox("Acción:", tickers)
    sub = st.slider("Subida (%)", 1, 25, 5)
with c2:
    try:
        p_v = float(yf.Ticker(acc).history(period="1d")['Close'].iloc[-1])
        n = int(inver / p_v)
        st.success(f"**Beneficio esperado: +{(p_v * (sub/100)) * n:.2f}€**")
    except: st.info("Cargando...")
