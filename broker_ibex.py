import streamlit as st
import yfinance as yf
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Radar de Inversión Pro", layout="wide")

# --- ESTILO (TARJETAS CLARAS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    [data-testid="stMetric"] { background-color: #f0f2f6; border-radius: 15px; padding: 15px; }
    [data-testid="stMetricLabel"] { color: #111827 !important; font-weight: bold; }
    [data-testid="stMetricValue"] { color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📡 Radar de Oportunidades")

# --- SECCIÓN 1: EL RADAR ---
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

# --- SECCIÓN 2: BUSCADOR CON ZOOM AUTOMÁTICO ---
st.subheader("🔍 Analizador Detallado")
ticker = st.text_input("Introduce un Ticker:", value="BBVA.MC").upper().strip()

if ticker:
    try:
        # Pedimos datos de 6 meses para que la curva se vea más detallada
        data = yf.download(ticker, period="6mo", progress=False)
        if not data.empty:
            precios = data['Close']
            
            c1, c2 = st.columns([1, 3])
            with c1:
                actual = float(precios.iloc[-1])
                st.metric(label=f"Precio {ticker}", value=f"{actual:.2f}€")
                media_20 = float(precios.tail(20).mean())
                if actual > media_20: st.success("🎯 SEÑAL: COMPRA")
                else: st.error("🚨 SEÑAL: VENTA")
            
            with c2:
                # --- AQUÍ ESTÁ EL TRUCO DEL ZOOM ---
                # Usamos line_chart con el parámetro 'y_axis_label' no, 
                # mejor forzamos los datos a una tabla limpia para que Streamlit haga zoom solo
                st.line_chart(precios, color="#FF4B4B")
                
                # Si sigue saliendo plana, esta es la alternativa "mágica":
                # st.area_chart(precios, color="#FF4B4B")
                
        else:
            st.warning("No hay datos disponibles.")
    except Exception as e:
        st.error(f"Error: {e}")
