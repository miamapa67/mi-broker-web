import streamlit as st
import yfinance as yf
import pandas as pd

# Configuración de página
st.set_page_config(page_title="IBEX 35 - Scanner de Volumen", layout="wide")

# --- DISEÑO MODO CLARO PRO ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    h1, h2, h3 { color: #1e293b !important; }
    
    /* Tarjetas con indicador de volumen */
    .card-compra { 
        background-color: #f0fdf4; color: #166534; padding: 20px; 
        border-radius: 12px; border-left: 8px solid #22c55e; margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .card-venta { 
        background-color: #fef2f2; color: #991b1b; padding: 20px; 
        border-radius: 12px; border-left: 8px solid #ef4444; margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .vol-badge {
        background-color: #1e293b; color: white; padding: 4px 8px;
        border-radius: 6px; font-size: 12px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 Scanner de Volumen e Inversión IBEX 35")
st.write("Detectando dónde están entrando los 'peces gordos' hoy.")

# Lista ampliada del IBEX
ibex_tickers = [
    "SAN.MC", "BBVA.MC", "TEF.MC", "IBE.MC", "ITX.MC", "REP.MC", 
    "CABK.MC", "SAB.MC", "AMS.MC", "ELE.MC", "FER.MC", "ACS.MC", "GRF.MC"
]

@st.cache_data(ttl=600)
def escanear_volumen(tickers):
    compras, ventas = [], []
    for t in tickers:
        try:
            df = yf.download(t, period="2mo", progress=False)
            if not df.empty:
                # Datos de precio
                cierre = df['Close'].iloc[:, 0] if isinstance(df['Close'], pd.DataFrame) else df['Close']
                actual = float(cierre.iloc[-1])
                media_20 = float(cierre.tail(20).mean())
                dif_precio = ((actual / media_20) - 1) * 100
                
                # Datos de volumen
                vol_hoy = float(df['Volume'].iloc[-1])
                vol_medio = float(df['Volume'].tail(20).mean())
                fuerza_vol = (vol_hoy / vol_medio) * 100
                
                info = {"ticker": t, "precio": actual, "dif": dif_precio, "vol": fuerza_vol}
                if actual > media_20: compras.append(info)
                else: ventas.append(info)
        except: continue
    return sorted(compras, key=lambda x: x['vol'], reverse=True), sorted(ventas, key=lambda x: x['vol'], reverse=True)

if st.button('🔍 ANALIZAR FUERZA DEL MERCADO'):
    l_compra, l_venta = escanear_volumen(ibex_tickers)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 COMPRA CON FUERZA")
        for item in l_compra[:6]:
            st.markdown(f"""
                <div class='card-compra'>
                    <span class='vol-badge'>Volumen: {item['vol']:.0f}%</span>
                    <h3 style='margin:10px 0 5px 0;'>{item['ticker']} - {item['precio']:.2f}€</h3>
                    <strong> Tendencia: +{item['dif']:.2f}%</strong> (Alcista)
                </div>
                """, unsafe_allow_html=True)
                
    with col2:
        st.subheader("🚨 VENTA / DEBILIDAD")
        for item in l_venta[:6]:
            st.markdown(f"""
                <div class='card-venta'>
                    <span class='vol-badge'>Volumen: {item['vol']:.0f}%</span>
                    <h3 style='margin:10px 0 5px 0;'>{item['ticker']} - {item['precio']:.2f}€</h3>
                    <strong> Tendencia: {item['dif']:.2f}%</strong> (Bajista)
                </div>
                """, unsafe_allow_html=True)
   
