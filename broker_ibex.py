import streamlit as st
import yfinance as yf
import pandas as pd
from PIL import Image
import os

st.set_page_config(page_title="Miguel Terminal Inversión", layout="wide")

# Estilo Blanco Nítido
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

# --- 1. CABECERA ---
if os.path.exists("logo_miguel.png"):
    img = Image.open("logo_miguel.png")
    st.image(img, use_column_width=True)

st.title("🏹 Terminal de Inversión - MIGUEL")
st.write("Análisis de Precios, Dividendos y Noticias en Directo.")

# --- 2. MOTOR DE ANÁLISIS ---
tickers = ["SAN.MC", "BBVA.MC", "TEF.MC", "IBE.MC", "ITX.MC", "REP.MC", "CABK.MC", "SAB.MC", "GRF.MC"]

if st.button('🚀 EJECUTAR ANÁLISIS COMPLETO', use_container_width=True):
    st.subheader("📊 Panel de Activos IBEX 35")
    
    with st.spinner('Extrayendo dividendos y noticias...'):
        for t in tickers:
            try:
                tk = yf.Ticker(t)
                # Forzamos la descarga de datos históricos y dividendos
                hist = tk.history(period="1mo")
                if hist.empty: continue
                
                precio_actual = float(hist['Close'].iloc[-1])
                
                # --- BUSCAR DIVIDENDO ---
                # Intentamos sacarlo de 'info' y si no del historial de dividendos
                div_yield = tk.info.get('dividendYield', 0)
                if not div_yield:
                    divs = tk.dividends
                    if not divs.empty:
                        # Estimación: Último dividendo * frecuencia (aprox) / precio
                        div_yield = (divs.iloc[-1] * 2) / precio_actual 
                
                div_final = (div_yield * 100) if div_yield else 0

                # --- RADAR DE NOTICIAS (LINK DIRECTO) ---
                nombre_corto = t.split('.')[0]
                link_noticias = f"https://www.google.com/search?q={nombre_corto}+noticias+bolsa&tbm=nws"
                link_finance = f"https://www.google.com/finance/quote/{t.replace('.MC', ':BME')}"

                # MOSTRAR TARJETA
                with st.expander(f"📈 {t}: {precio_actual:.2f}€", expanded=True):
                    c1, c2 = st.columns([1, 1.5])
                    with c1:
                        st.metric("Precio", f"{precio_actual:.2f}€")
                        if div_final > 0:
                            st.success(f"💰 Dividendo: {div_final:.2f}% anual")
                        else:
                            st.warning("💰 Dividendo: Consultar próximo pago")
                    
                    with c2:
                        st.write("**📰 Radar de Información:**")
                        st.markdown(f"• [🔍 Ver Últimas Noticias de {nombre_corto}]({link_noticias})")
                        st.markdown(f"• [📊 Ver Gráfico y Datos en Google Finance]({link_finance})")

            except Exception as e:
                continue

st.divider()

# --- 3. CALCULADORA ---
st.subheader("💰 Simulador de Ganancia Neta")
c1, c2 = st.columns(2)
with c1:
    inver = st.number_input("Capital a invertir (€):", value=1000, step=500)
    acc_elegida = st.selectbox("Acción:", tickers)
    sub_obj = st.slider("Subida esperada (%)", 1, 30, 5)

with c2:
    try:
        p_v = float(yf.Ticker(acc_elegida).history(period="1d")['Close'].iloc[-1])
        n_acc = int(inver / p_v)
        gan_estimada = (p_v * (sub_obj/100)) * n_acc
        st.success(f"**Resultado: Ganarías +{gan_estimada:.2f}€**")
        st.info(f"Comprarías {n_acc} acciones a {p_v:.2f}€")
    except: st.write("Calculando...")
