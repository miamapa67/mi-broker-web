import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Scanner IBEX 35 Pro", layout="wide")

# Estilo para que las señales de compra/venta se vean claras
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .card-compra { background-color: #064e3b; color: #ecfdf5; padding: 15px; border-radius: 10px; border: 1px solid #10b981; margin-bottom: 10px; }
    .card-venta { background-color: #450a0a; color: #fef2f2; padding: 15px; border-radius: 10px; border: 1px solid #ef4444; margin-bottom: 10px; }
    [data-testid="stMetric"] { background-color: #f0f2f6; border-radius: 15px; padding: 15px; }
    h1, h2, h3 { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 Escáner de Oportunidades IBEX 35")

# Lista de los principales valores del IBEX 35
ibex_tickers = [
    "SAN.MC", "BBVA.MC", "TEF.MC", "IBE.MC", "ITX.MC", "REP.MC", "CABK.MC", 
    "SAB.MC", "AMS.MC", "ELE.MC", "ENG.MC", "NTGY.MC", "FER.MC", "GRF.MC"
]

@st.cache_data(ttl=3600) # Para que no descargue todo cada vez que tocas un botón
def escanear_mercado(tickers):
    compras = []
    ventas = []
    for t in tickers:
        try:
            df = yf.download(t, period="2mo", progress=False)
            if not df.empty:
                # Calculamos media de 20 días
                cierre = df['Close'].iloc[:, 0] if isinstance(df['Close'], pd.DataFrame) else df['Close']
                actual = cierre.iloc[-1]
                media_20 = cierre.tail(20).mean()
                variacion = ((actual / media_20) - 1) * 100
                
                info = {"ticker": t, "precio": actual, "dif": variacion}
                if actual > media_20:
                    compras.append(info)
                else:
                    ventas.append(info)
        except: continue
    return sorted(compras, key=lambda x: x['dif'], reverse=True), sorted(ventas, key=lambda x: x['dif'])

if st.button('🚀 ESCANEAR IBEX 35 AHORA'):
    listado_compra, listado_venta = escanear_mercado(ibex_tickers)
    
    col_compra, col_venta = st.columns(2)
    
    with col_compra:
        st.header("🎯 TOP COMPRA (Al alza)")
        for item in listado_compra[:4]: # Los 4 mejores
            st.markdown(f"""<div class='card-compra'>
                <strong>{item['ticker']}</strong>: {item['precio']:.2f}€ <br>
                Tendencia: +{item['dif']:.2f}% sobre su media
                </div>""", unsafe_allow_html=True)
                
    with col_venta:
        st.header("🚨 TOP VENTA (En caída)")
        for item in listado_venta[:4]: # Los 4 que más caen
            st.markdown(f"""<div class='card-venta'>
                <strong>{item['ticker']}</strong>: {item['precio']:.2f}€ <br>
                Tendencia: {item['dif']:.2f}% bajo su media
                </div>""", unsafe_allow_html=True)

st.divider()

# Mantenemos tu buscador detallado abajo por si quieres ver la gráfica de uno concreto
st.subheader("🔍 Análisis Detallado con Gráfica")
ticker_individual = st.text_input("Introduce Ticker para ver gráfica:", value="SAN.MC").upper()
if ticker_individual:
    data = yf.download(ticker_individual, period="6mo", progress=False)
    if not data.empty:
        cierre_ind = data['Close'].iloc[:, 0] if isinstance(data['Close'], pd.DataFrame) else data['Close']
        df_plot = pd.DataFrame({'Fecha': cierre_ind.index, 'Precio': cierre_ind.values})
        fig = px.line(df_plot, x='Fecha', y='Precio', color_discrete_sequence=['#FF4B4B'])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig, use_container_width=True)
