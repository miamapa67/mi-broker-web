import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Configuración
st.set_page_config(page_title="Radar de Inversión Pro", layout="wide")

# Estilo
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

# --- RADAR ---
favoritos = ["SAN.MC", "BBVA.MC", "TEF.MC", "IBE.MC", "TSLA"]
cols = st.columns(len(favoritos))

for i, f in enumerate(favoritos):
    try:
        d = yf.download(f, period="1mo", progress=False)
        if not d.empty:
            # Limpieza segura del precio
            p_actual = float(d['Close'].iloc[-1])
            p_media = float(d['Close'].mean())
            with cols[i]:
                st.metric(label=f, value=f"{p_actual:.2f}€")
                if p_actual > p_media: st.success("🟢 COMPRA")
                else: st.error("🔴 VENTA")
    except: continue

st.divider()

# --- ANALIZADOR DETALLADO CORREGIDO ---
st.subheader("🔍 Analizador Detallado")
ticker = st.text_input("Introduce un Ticker:", value="BBVA.MC").upper().strip()

if ticker:
    try:
        # Descargamos datos de 6 meses para que la curva sea nítida
        df = yf.download(ticker, period="6mo", progress=False)
        
        if not df.empty:
            # TRUCO MAESTRO: Forzamos a que solo use la columna 'Close' sin duplicados
            precios_limpios = df['Close'].copy()
            if isinstance(precios_limpios, pd.DataFrame):
                precios_limpios = precios_limpios.iloc[:, 0]
            
            # Creamos la tabla final para la gráfica
            df_final = pd.DataFrame(precios_limpios).reset_index()
            df_final.columns = ['Fecha', 'Precio']
            
            c1, c2 = st.columns([1, 3])
            with c1:
                actual = float(df_final['Precio'].iloc[-1])
                st.metric(label=f"Precio {ticker}", value=f"{actual:.2f}€")
                media_20 = df_final['Precio'].tail(20).mean()
                if actual > media_20: st.success("🎯 SEÑAL: COMPRA")
                else: st.error("🚨 SEÑAL: VENTA")
            
            with c2:
                # GRÁFICA INTERACTIVA CON ZOOM REAL
                fig = px.line(df_final, x='Fecha', y='Precio', 
                             color_discrete_sequence=['#FF4B4B'],
                             title=f"Movimiento Real de {ticker}")
                
                # Forzamos el zoom al rango de precios (ej: de 15 a 20 euros)
                fig.update_yaxes(autorange=True, fixedrange=False)
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font_color="white", margin=dict(l=0, r=0, t=30, b=0), height=400
                )
                st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error("Esperando datos de Yahoo...")
