import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="Miguel Terminal 360", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal IBEX 360 - MIGUEL")

# --- LISTA COMPLETA ---
ibex_35 = [
    "SAN.MC", "BBVA.MC", "TEF.MC", "REP.MC", "ITX.MC", "GRF.MC", "SAB.MC", "IBE.MC", "CABK.MC"
]

# BOTÓN DE ACCIÓN
if st.button('🚀 ESCANEAR VALORES AHORA', use_container_width=True):
    lista_analisis = []
    
    with st.spinner('Pidiendo permiso a la Bolsa de Madrid...'):
        for t in ibex_35:
            try:
                # TRUCO: Usamos 'period' de 1 año para que no nos bloqueen por pedir poco
                tk = yf.Ticker(t)
                df = tk.history(period="1y")
                
                if not df.empty:
                    # Cogemos el último precio plano
                    precio_act = float(df['Close'].iloc[-1])
                    
                    # Cálculo RSI (Semáforo)
                    delta = df['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rsi_val = 100 - (100 / (1 + (gain.iloc[-1] / loss.iloc[-1])))
                    
                    color = "🟢" if rsi_val < 35 else "🔴" if rsi_val > 65 else "⚪"
                    
                    lista_analisis.append({
                        "ticker": t, "precio": precio_act, "rsi": rsi_val, "emoji": color, "df": df
                    })
            except:
                continue

    if lista_analisis:
        # Mostramos los resultados en tarjetas limpias
        cols = st.columns(3)
        for i, item in enumerate(lista_analisis):
            with cols[i % 3]:
                with st.expander(f"{item['emoji']} {item['ticker']}: {item['precio']:.2f}€", expanded=True):
                    st.write(f"**RSI:** {item['rsi']:.1f}")
                    # Gráfico de línea rápido
                    fig = go.Figure(data=[go.Scatter(x=item['df'].index[-30:], y=item['df']['Close'][-30:], mode='lines', line=dict(color='#1f77b4'))])
                    fig.update_layout(height=120, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown(f"[📰 Noticias](https://www.google.com/search?q={item['ticker'].split('.')[0]}+noticias+bolsa&tbm=nws)")
    else:
        st.warning("⚠️ El mercado está saturado. Por favor, espera 10 segundos y pulsa el botón otra vez.")

st.divider()
st.subheader("💰 Simulador")
inv = st.number_input("Dinero (€):", value=1000)
st.write(f"Listo para simular con {inv}€")
