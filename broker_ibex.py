import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="Miguel Terminal PRO", layout="wide")

# Estilo Profesional
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal IBEX 360 - MIGUEL")
st.write("Semáforos, Noticias y Gráficos Interactivos.")

# --- LISTA DE VALORES ---
ibex_35 = ["SAN.MC", "BBVA.MC", "TEF.MC", "REP.MC", "ITX.MC", "IAG.MC", "GRF.MC", "SAB.MC", "IBE.MC"]

# --- BOTÓN DE ESCÁNER ---
if st.button('🚀 ACTIVAR ESCÁNER Y SEMÁFOROS', use_container_width=True):
    lista_resultados = []
    
    with st.spinner('Buscando señales de compra...'):
        for t in ibex_35:
            try:
                # Intento de descarga protegida
                tk = yf.Ticker(t)
                df = tk.history(period="3mo")
                
                if not df.empty:
                    p_act = float(df['Close'].iloc[-1])
                    # Cálculo de Semáforo (RSI)
                    delta = df['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rsi = 100 - (100 / (1 + (gain.iloc[-1] / (loss.iloc[-1] + 0.001))))
                    
                    # Filtro de Semáforo
                    if rsi < 35: semaforo, estado = "🟢", "POTENCIAL"
                    elif rsi > 65: semaforo, estado = "🔴", "RIESGO"
                    else: semaforo, estado = "⚪", "NEUTRO"
                    
                    lista_resultados.append({
                        "ticker": t, "precio": p_act, "rsi": rsi, 
                        "semaforo": semaforo, "estado": estado, "df": df
                    })
            except:
                continue

    if lista_resultados:
        # --- RANKING DE FILTROS ---
        st.subheader("🏆 Filtro de Oportunidades")
        c1, c2 = st.columns(2)
        df_final = pd.DataFrame(lista_resultados)
        
        with c1:
            best = df_final.sort_values("rsi").iloc[0]
            st.success(f"💎 MEJOR COMPRA: {best['ticker']} (RSI: {best['rsi']:.1f})")
        with c2:
            worst = df_final.sort_values("rsi", ascending=False).iloc[0]
            st.error(f"⚠️ MÁS CARO: {worst['ticker']} (RSI: {worst['rsi']:.1f})")

        st.divider()

        # --- GRÁFICOS INTERACTIVOS Y NOTICIAS ---
        st.subheader("📊 Análisis Detallado")
        cols = st.columns(3)
        for i, item in enumerate(lista_resultados):
            with cols[i % 3]:
                with st.expander(f"{item['semaforo']} {item['ticker']}: {item['precio']:.2f}€"):
                    # Gráfico Interactivo de Velas
                    fig = go.Figure(data=[go.Candlestick(
                        x=item['df'].index[-20:],
                        open=item['df']['Open'][-20:],
                        high=item['df']['High'][-20:],
                        low=item['df']['Low'][-20:],
                        close=item['df']['Close'][-20:]
                    )])
                    fig.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Radar de Noticias
                    n_limpio = item['ticker'].split('.')[0]
                    st.markdown(f"**📰 Noticias:** [Ver últimas de {n_limpio}](https://www.google.com/search?q={n_limpio}+noticias+bolsa&tbm=nws)")
    else:
        st.error("⚠️ Yahoo sigue bloqueando el Semáforo. Inténtalo de nuevo en 5 minutos.")

st.divider()
# La calculadora se queda porque es lo único que no depende de Yahoo
st.subheader("💰 Calculadora Rápida")
inv = st.number_input("Inversión (€):", value=1000)
