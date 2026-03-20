import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Scanner IBEX 35 - Light Mode", layout="wide")

# --- DISEÑO MODO CLARO (Limpio y profesional) ---
st.markdown("""
    <style>
    /* Fondo principal blanco */
    .stApp { background-color: #ffffff; }
    
    /* Títulos en azul oscuro/negro para que resalten */
    h1, h2, h3 { color: #1e293b !important; font-weight: 800; }
    
    /* Tarjetas del escáner con bordes suaves */
    .card-compra { 
        background-color: #f0fdf4; 
        color: #166534; 
        padding: 20px; 
        border-radius: 12px; 
        border: 1px solid #bbf7d0; 
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .card-venta { 
        background-color: #fef2f2; 
        color: #991b1b; 
        padding: 20px; 
        border-radius: 12px; 
        border: 1px solid #fecaca; 
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Ajuste de las métricas individuales */
    [data-testid="stMetric"] {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 15px;
    }
    [data-testid="stMetricLabel"] { color: #475569 !important; }
    [data-testid="stMetricValue"] { color: #0f172a !important; }

    /* Divisores */
    hr { border-top: 1px solid #e2e8f0; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 Escáner de Oportunidades IBEX 35")

ibex_tickers = ["SAN.MC", "BBVA.MC", "TEF.MC", "IBE.MC", "ITX.MC", "REP.MC", "CABK.MC", "SAB.MC", "AMS.MC", "ELE.MC"]

@st.cache_data(ttl=3600)
def escanear_mercado(tickers):
    compras, ventas = [], []
    for t in tickers:
        try:
            df = yf.download(t, period="2mo", progress=False)
            if not df.empty:
                cierre = df['Close'].iloc[:, 0] if isinstance(df['Close'], pd.DataFrame) else df['Close']
                actual, media_20 = cierre.iloc[-1], cierre.tail(20).mean()
                variacion = ((actual / media_20) - 1) * 100
                info = {"ticker": t, "precio": actual, "dif": variacion}
                if actual > media_20: compras.append(info)
                else: ventas.append(info)
        except: continue
    return sorted(compras, key=lambda x: x['dif'], reverse=True), sorted(ventas, key=lambda x: x['dif'])

if st.button('🚀 ESCANEAR MERCADO AHORA'):
    listado_compra, listado_venta = escanear_mercado(ibex_tickers)
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🎯 OPORTUNIDADES (Alza)")
        for item in listado_compra[:4]:
            st.markdown(f"<div class='card-compra'><strong>{item['ticker']}</strong>: {item['precio']:.2f}€<br>Tendencia: +{item['dif']:.2f}%</div>", unsafe_allow_html=True)
    with c2:
        st.subheader("🚨 RIESGOS (Caída)")
        for item in listado_venta[:4]:
            st.markdown(f"<div class='card-venta'><strong>{item['ticker']}</strong>: {item['precio']:.2f}€<br>Tendencia: {item['dif']:.2f}%</div>", unsafe_allow_html=True)

st.divider()

# Gráfica detallada
st.subheader("🔍 Análisis de Gráfica")
ticker_ind = st.text_input("Ticker:", value="SAN.MC").upper()
if ticker_ind:
    data = yf.download(ticker_ind, period="6mo", progress=False)
    if not data.empty:
        cierre_ind = data['Close'].iloc[:, 0] if isinstance(data['Close'], pd.DataFrame) else data['Close']
        df_plot = pd.DataFrame({'Fecha': cierre_ind.index, 'Precio': cierre_ind.values})
        
        # Gráfica adaptada al modo claro
        fig = px.line(df_plot, x='Fecha', y='Precio', color_discrete_sequence=['#ef4444'])
        fig.update_layout(
            paper_bgcolor='white', 
            plot_bgcolor='#f8fafc', 
            font_color="#1e293b",
            margin=dict(l=0, r=0, t=10, b=0)
        )
        fig.update_xaxes(gridcolor='#e2e8f0')
        fig.update_yaxes(gridcolor='#e2e8f0')
        st.plotly_chart(fig, use_container_width=True)
