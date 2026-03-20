import streamlit as st
import yfinance as yf
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Scanner IBEX - Dividendos Pro", layout="wide")

# --- DISEÑO MODO CLARO ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    h1, h2, h3 { color: #1e293b !important; }
    
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
    .badge {
        background-color: #1e293b; color: white; padding: 4px 10px;
        border-radius: 6px; font-size: 11px; font-weight: bold; margin-right: 5px;
    }
    .badge-div {
        background-color: #2563eb; color: white; padding: 4px 10px;
        border-radius: 6px; font-size: 11px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💰 Radar de Dividendos e Inversión")
st.write("Analizando tendencia, volumen y rentabilidad por dividendo del IBEX 35.")

# Lista de valores clave para dividendos
ibex_tickers = [
    "SAN.MC", "BBVA.MC", "TEF.MC", "IBE.MC", "ITX.MC", "REP.MC", 
    "ENG.MC", "ELE.MC", "NTGY.MC", "ACS.MC", "CABK.MC", "SAB.MC"
]

@st.cache_data(ttl=3600)
def escanear_completo(tickers):
    compras, ventas = [], []
    for t in tickers:
        try:
            stock = yf.Ticker(t)
            df = stock.history(period="2mo")
            info = stock.info
            
            if not df.empty:
                # Precio y Tendencia
                actual = float(df['Close'].iloc[-1])
                media_20 = float(df['Close'].tail(20).mean())
                dif_precio = ((actual / media_20) - 1) * 100
                
                # Volumen
                vol_hoy = float(df['Volume'].iloc[-1])
                vol_medio = float(df['Volume'].tail(20).mean())
                fuerza_vol = (vol_hoy / vol_medio) * 100
                
                # Dividendo (Convertimos a porcentaje, ej: 0.05 -> 5%)
                rent_div = info.get('dividendYield', 0)
                rent_div = (rent_div * 100) if rent_div else 0
                
                datos = {"ticker": t, "precio": actual, "dif": dif_precio, "vol": fuerza_vol, "div": rent_div}
                
                if actual > media_20: compras.append(datos)
                else: ventas.append(datos)
        except: continue
    return sorted(compras, key=lambda x: x['div'], reverse=True), sorted(ventas, key=lambda x: x['div'], reverse=True)

if st.button('🚀 ESCANEAR RENTABILIDAD AHORA'):
    l_compra, l_venta = escanear_completo(ibex_tickers)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 COMPRA (Alcistas + Dividendos)")
        for item in l_compra:
            st.markdown(f"""
                <div class='card-compra'>
                    <span class='badge'>Volumen: {item['vol']:.0f}%</span>
                    <span class='badge-div'>Dividendo: {item['div']:.2f}%</span>
                    <h3 style='margin:10px 0 5px 0;'>{item['ticker']} - {item['precio']:.2f}€</h3>
                    <strong>Tendencia: +{item['dif']:.2f}%</strong>
                </div>
                """, unsafe_allow_html=True)
                
    with col2:
        st.subheader("🚨 VENTA (Bajistas / Riesgo)")
        for item in l_venta:
            st.markdown(f"""
                <div class='card-venta'>
                    <span class='badge'>Volumen: {item['vol']:.0f}%</span>
                    <span class='badge-div'>Dividendo: {item['div']:.2f}%</span>
                    <h3 style='margin:10px 0 5px 0;'>{item['ticker']} - {item['precio']:.2f}€</h3>
                    <strong>Tendencia: {item['dif']:.2f}%</strong>
                </div>
                """, unsafe_allow_html=True)
