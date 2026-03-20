import streamlit as st
import yfinance as yf
import pandas as pd

# Configuración de página
st.set_page_config(page_title="IBEX 35 - Señales de Inversión", layout="wide")

# --- DISEÑO MODO CLARO TOTAL ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    h1, h2, h3 { color: #1e293b !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* Tarjetas de Oportunidad */
    .card-compra { 
        background-color: #f0fdf4; 
        color: #166534; 
        padding: 25px; 
        border-radius: 15px; 
        border: 2px solid #bbf7d0; 
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .card-venta { 
        background-color: #fef2f2; 
        color: #991b1b; 
        padding: 25px; 
        border-radius: 15px; 
        border: 2px solid #fecaca; 
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Estilo del botón */
    .stButton>button {
        background-color: #2563eb;
        color: white;
        border-radius: 10px;
        padding: 10px 25px;
        font-weight: bold;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 Escáner de Oportunidades IBEX 35")
st.write("Análisis basado en la tendencia de los últimos **20 días**.")

# Lista de valores
ibex_tickers = [
    "SAN.MC", "BBVA.MC", "TEF.MC", "IBE.MC", "ITX.MC", 
    "REP.MC", "CABK.MC", "SAB.MC", "AMS.MC", "ELE.MC",
    "ENG.MC", "NTGY.MC", "FER.MC", "GRF.MC", "ACS.MC"
]

@st.cache_data(ttl=600)
def escanear_mercado(tickers):
    compras, ventas = [], []
    for t in tickers:
        try:
            df = yf.download(t, period="2mo", progress=False)
            if not df.empty:
                # Limpieza de datos
                cierre = df['Close'].iloc[:, 0] if isinstance(df['Close'], pd.DataFrame) else df['Close']
                actual = float(cierre.iloc[-1])
                media_20 = float(cierre.tail(20).mean())
                variacion = ((actual / media_20) - 1) * 100
                
                info = {"ticker": t, "precio": actual, "dif": variacion}
                if actual > media_20:
                    compras.append(info)
                else:
                    ventas.append(info)
        except: continue
    return sorted(compras, key=lambda x: x['dif'], reverse=True), sorted(ventas, key=lambda x: x['dif'])

# Botón centralizado
if st.button('🚀 ACTUALIZAR SEÑALES AHORA'):
    listado_compra, listado_venta = escanear_mercado(ibex_tickers)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 PARA COMPRAR (Tendencia Alcista)")
        for item in listado_compra[:6]: # Mostramos los 6 mejores
            st.markdown(f"""
                <div class='card-compra'>
                    <h3 style='margin:0;'>{item['ticker']}</h3>
                    <span style='font-size:24px; font-weight:bold;'>{item['precio']:.2f}€</span><br>
                    <strong>+{item['dif']:.2f}%</strong> por encima de su media
                </div>
                """, unsafe_allow_html=True)
                
    with col2:
        st.subheader("🚨 PARA VENDER (Tendencia Bajista)")
        for item in listado_venta[:6]: # Mostramos los 6 peores
            st.markdown(f"""
                <div class='card-venta'>
                    <h3 style='margin:0;'>{item['ticker']}</h3>
                    <span style='font-size:24px; font-weight:bold;'>{item['precio']:.2f}€</span><br>
                    <strong>{item['dif']:.2f}%</strong> por debajo de su media
                </div>
                """, unsafe_allow_html=True)
else:
    st.info("Haz clic en el botón superior para analizar el mercado en tiempo real.")
