import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import requests

st.set_page_config(page_title="Miguel Terminal 360", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal IBEX 360 - MIGUEL")

# --- LISTA DE PRUEBA (Si esta funciona, pondremos los 35) ---
ibex_test = ["SAN.MC", "BBVA.MC", "TEF.MC", "REP.MC", "ITX.MC", "IAG.MC"]

if st.button('🚀 ESCANEAR CON CAMUFLAJE', use_container_width=True):
    lista_analisis = []
    
    with st.spinner('Disfrazando la conexión para entrar en el mercado...'):
        # --- EL TRUCO DEL CAMUFLAJE ---
        # Esto hace que parezcamos un navegador real
        sesion = requests.Session()
        sesion.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        for t in ibex_test:
            try:
                # Descargamos los datos usando la sesión camuflada
                tk = yf.Ticker(t, session=sesion)
                df = tk.history(period="1mo")
                
                if not df.empty:
                    precio_act = float(df['Close'].iloc[-1])
                    
                    # Cálculo RSI rápido
                    delta = df['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rsi_val = 100 - (100 / (1 + (gain.iloc[-1] / (loss.iloc[-1] + 0.00001))))
                    
                    color = "🟢" if rsi_val < 35 else "🔴" if rsi_val > 65 else "⚪"
                    
                    lista_analisis.append({
                        "ticker": t, "precio": precio_act, "rsi": rsi_val, "emoji": color, "df": df
                    })
            except:
                continue

    if lista_analisis:
        st.success(f"¡Conexión establecida! Mostrando {len(lista_analisis)} valores.")
        cols = st.columns(3)
        for i, item in enumerate(lista_analisis):
            with cols[i % 3]:
                with st.expander(f"{item['emoji']} {item['ticker']}: {item['precio']:.2f}€", expanded=True):
                    st.write(f"**RSI (Fuerza):** {item['rsi']:.1f}")
                    # Gráfico mini
                    fig = go.Figure(data=[go.Scatter(x=item['df'].index, y=item['df']['Close'], mode='lines', line=dict(color='#1f77b4'))])
                    fig.update_layout(height=130, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("❌ Yahoo sigue bloqueando la entrada. Espera 30 segundos e inténtalo de nuevo.")

st.divider()
st.subheader("💰 Simulador")
inv = st.number_input("Dinero (€):", value=1000)
st.write(f"Sistema listo para {inv}€")
