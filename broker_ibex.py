import streamlit as st
import yfinance as yf
import pandas as pd
from PIL import Image
import os

st.set_page_config(page_title="Miguel Financial Terminal", layout="wide")

# Estilo Blanco Nítido
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

# --- 1. CABECERA CON TU LOGO ---
if os.path.exists("logo_miguel.png"):
    img = Image.open("logo_miguel.png")
    st.image(img, use_column_width=True)

st.title("🏹 Terminal Financiera - MIGUEL")
st.write("Escáner de Oportunidades + Radar de Noticias en Tiempo Real.")

# --- 2. MOTOR DE ANÁLISIS Y NOTICIAS ---
tickers = ["SAN.MC", "BBVA.MC", "TEF.MC", "IBE.MC", "ITX.MC", "REP.MC", "CABK.MC", "SAB.MC", "GRF.MC"]

if st.button('🚀 EJECUTAR ESCÁNER DE MERCADO Y NOTICIAS', use_container_width=True):
    st.subheader("📊 Análisis de Activos")
    
    with st.spinner('Rastreando prensa financiera y cotizaciones...'):
        for t in tickers:
            try:
                tk = yf.Ticker(t)
                # Datos de precio (últimos 3 meses para RSI)
                hist = tk.history(period="3mo")
                if hist.empty: continue
                
                actual = float(hist['Close'].iloc[-1])
                
                # Cálculo de RSI
                delta = hist['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi_val = 100 - (100 / (1 + rs.iloc[-1]))
                
                # Noticias (sacamos las 2 más recientes)
                news = tk.news[:2]
                
                # Color según RSI
                if rsi_val > 70: col_bg, estado = "#fef2f2", "⚠️ SOBRECOMPRA"
                elif rsi_val < 30: col_bg, estado = "#f0fdf4", "✅ OPORTUNIDAD"
                else: col_bg, estado = "#f8fafc", "⚖️ NEUTRO"
                
                # Tarjeta de la Empresa
                with st.expander(f"PROYECCIÓN: {t} - {actual:.2f}€ ({estado})", expanded=True):
                    c1, c2 = st.columns([1, 2])
                    with c1:
                        st.write(f"**RSI:** {rsi_val:.1f}")
                        div = tk.info.get('dividendYield', 0)
                        if div: st.write(f"💰 **Div:** {div*100:.2f}%")
                    
                    with c2:
                        st.write("**📰 Última hora:**")
                        if news:
                            for n in news:
                                st.markdown(f"• [{n['title']}]({n['link']})")
                        else:
                            st.write("Sin noticias recientes destacadas.")
                            
            except Exception as e:
                continue

st.divider()

# --- 3. CALCULADORA DE BENEFICIOS (OPTIMIZADA) ---
st.subheader("💰 Simulador de Ganancia Neta")
col_sim1, col_sim2 = st.columns(2)

with col_sim1:
    inver = st.number_input("Capital a invertir (€):", value=1000, step=500)
    acc_sim = st.selectbox("Valor para simular:", tickers)
    objetivo = st.slider("Subida esperada (%)", 1, 25, 5)

with col_sim2:
    try:
        t_sim = yf.Ticker(acc_sim)
        p_act = float(t_sim.history(period="1d")['Close'].iloc[-1])
        n_acc = int(inver / p_act)
        beneficio = (p_act * (objetivo/100)) * n_acc
        
        st.success(f"**Resultado para {acc_sim}:**")
        st.write(f"Comprarías **{n_acc}** acciones.")
        st.write(f"Beneficio estimado: **+{beneficio:.2f}€**")
    except:
        st.info("Esperando selección...")
