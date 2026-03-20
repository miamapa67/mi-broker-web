import streamlit as st
import yfinance as yf
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Scanner IBEX Pro", layout="wide")

# Diseño Modo Claro Profesional
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .card { padding: 20px; border-radius: 12px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 8px solid; }
    .compra { background-color: #f0fdf4; color: #166534; border-left-color: #22c55e; }
    .venta { background-color: #fef2f2; color: #991b1b; border-left-color: #ef4444; }
    .vol-badge { background-color: #1e293b; color: white; padding: 4px 8px; border-radius: 6px; font-size: 12px; }
    h1, h2, h3 { color: #1e293b !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 Scanner de Inversión Pro")
st.write("Analizando Tendencia y Volumen del IBEX 35")

# Lista optimizada
tickers = ["SAN.MC", "BBVA.MC", "TEF.MC", "IBE.MC", "ITX.MC", "REP.MC", "CABK.MC", "SAB.MC", "ACS.MC", "GRF.MC"]

if st.button('🔍 ESCANEAR MERCADO AHORA'):
    col1, col2 = st.columns(2)
    
    with st.spinner('Calculando fuerza de mercado...'):
        for t in tickers:
            try:
                # Descarga mínima para evitar bloqueos
                df = yf.download(t, period="2mo", progress=False)
                if not df.empty:
                    # Precio y Media
                    cierre = df['Close'].iloc[:, 0] if len(df['Close'].shape) > 1 else df['Close']
                    actual = float(cierre.iloc[-1])
                    media_20 = float(cierre.tail(20).mean())
                    dif = ((actual / media_20) - 1) * 100
                    
                    # Volumen
                    vol_hoy = float(df['Volume'].iloc[-1])
                    vol_med = float(df['Volume'].tail(20).mean())
                    fuerza_v = (vol_hoy / vol_med) * 100
                    
                    # Mostrar en la columna correspondiente
                    if actual > media_20:
                        with col1:
                            st.markdown(f"""<div class="card compra">
                                <span class="vol-badge">Volumen: {fuerza_v:.0f}%</span>
                                <h3>{t} - {actual:.2f}€</h3>
                                <strong>Tendencia: +{dif:.2f}% (Alcista)</strong>
                            </div>""", unsafe_allow_html=True)
                    else:
                        with col2:
                            st.markdown(f"""<div class="card venta">
                                <span class="vol-badge">Volumen: {fuerza_v:.0f}%</span>
                                <h3>{t} - {actual:.2f}€</h3>
                                <strong>Tendencia: {dif:.2f}% (Bajista)</strong>
                            </div>""", unsafe_allow_html=True)
            except:
                continue
    st.success("¡Análisis completado!")
