import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Configuración de página
st.set_page_config(page_title="Radar de Inversión Pro", layout="wide")

# Estilo CSS de lujo (Tarjetas claras)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    [data-testid="stMetric"] { background-color: #f0f2f6; border-radius: 15px; padding: 15px; }
    [data-testid="stMetricLabel"] { color: #111827 !important; font-weight: bold; }
    [data-testid="stMetricValue"] { color: #000000 !important; }
    h1, h2, h3 { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📡 Radar de Oportunidades")

# --- SECCIÓN 1: EL RADAR (YA FUNCIONA) ---
favoritos = ["SAN.MC", "BBVA.MC", "TEF.MC", "IBE.MC", "TSLA"]
cols = st.columns(len(favoritos))

for i, f in enumerate(favoritos):
    try:
        d = yf.download(f, period="1mo", progress=False)
        if not d.empty:
            p_actual = float(d['Close'].iloc[-1])
            p_media = float(d['Close'].tail(20).mean())
            with cols[i]:
                st.metric(label=f, value=f"{p_actual:.2f}€")
                if p_actual > p_media: st.success("🟢 COMPRA")
                else: st.error("🔴 VENTA")
    except: continue

st.divider()

# --- SECCIÓN 2: BUSCADOR CON GRÁFICA CORREGIDA ---
st.subheader("🔍 Analizador Detallado")
ticker = st.text_input("Introduce un Ticker:", value="BBVA.MC").upper().strip()

if ticker:
    try:
        data = yf.download(ticker, period="1y", progress=False)
        if not data.empty:
            # --- ARREGLO MÁGICO PARA LA GRÁFICA ---
            df_plot = data.reset_index()
            # Buscamos cómo se llama la columna de la fecha (a veces es 'Date', otras 'index')
            columna_fecha = df_plot.columns[0] 
            
            c1, c2 = st.columns([1, 3])
            with c1:
                actual = float(data['Close'].iloc[-1])
                st.metric(label=f"Precio {ticker}", value=f"{actual:.2f}€")
                media_20 = float(data['Close'].tail(20).mean())
                if actual > media_20: st.success("🎯 SEÑAL: COMPRA")
                else: st.error("🚨 SEÑAL: VENTA")
            
            with c2:
                # Usamos la columna detectada automáticamente
                fig = px.line(df_plot, x=columna_fecha, y='Close', 
                             color_discrete_sequence=['#FF4B4B'])
                
                fig.update_yaxes(autorange=True, fixedrange=False)
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color="white",
                    margin=dict(l=0, r=0, t=30, b=0),
                    height=350
                )
                st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error("Cargando gráfica...")
