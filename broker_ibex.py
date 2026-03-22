import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="Miguel Terminal 35", layout="wide")

# Estilo Profesional
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal IBEX 35 Completa - MIGUEL")
st.write("Análisis en tiempo real de los 35 valores del mercado español.")

# --- 1. LISTA COMPLETA DE LOS 35 VALORES ---
ibex_35 = [
    "ANA.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", "BKT.MC", "BBVA.MC",
    "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC",
    "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC",
    "ROVI.MC", "SCYR.MC", "SLBA.MC", "TEF.MC", "UNI.MC"
]

# --- 2. BOTÓN DE ESCÁNER TOTAL ---
if st.button('🚀 ESCANEAR LOS 35 VALORES DEL IBEX', use_container_width=True):
    lista_resultados = []
    progreso = st.progress(0)
    status_text = st.empty()
    
    for i, t in enumerate(ibex_35):
        try:
            status_text.text(f"Analizando {t} ({i+1}/35)...")
            tk = yf.Ticker(t)
            df = tk.history(period="6mo")
            
            if not df.empty:
                p_act = float(df['Close'].iloc[-1])
                # Cálculo de RSI para el semáforo
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain.iloc[-1] / (loss.iloc[-1] + 0.00001)
                rsi = 100 - (100 / (1 + rs))
                
                # Definir filtros/colores
                if rsi < 35: sem, est, col = "🟢", "COMPRA", "green"
                elif rsi > 65: sem, est, col = "🔴", "RIESGO", "red"
                else: sem, est, col = "⚪", "NEUTRO", "gray"
                
                lista_resultados.append({
                    "ticker": t, "precio": p_act, "rsi": rsi, 
                    "semaforo": sem, "estado": est, "df": df
                })
            progreso.progress((i + 1) / len(ibex_35))
        except:
            continue
    
    status_text.empty()

    if lista_resultados:
        df_final = pd.DataFrame(lista_resultados)
        
        # --- 3. FILTROS / RANKINGS ---
        st.subheader("🏆 Filtro de Oportunidades")
        col_f1, col_f2, col_f3 = st.columns(3)
        
        with col_f1:
            mejores = df_final[df_final['estado'] == 'COMPRA']
            st.success(f"💎 Oportunidades de Compra: {len(mejores)}")
            for ticker in mejores['ticker'].head(3): st.write(f"· {ticker}")
            
        with col_f2:
            neutros = df_final[df_final['estado'] == 'NEUTRO']
            st.info(f"⚪ Valores en Calma: {len(neutros)}")
            
        with col_f3:
            riesgos = df_final[df_final['estado'] == 'RIESGO']
            st.error(f"⚠️ Alertas de Riesgo: {len(riesgos)}")
            for ticker in riesgos['ticker'].head(3): st.write(f"· {ticker}")

        st.divider()

        # --- 4. CUADRÍCULA DE LOS 35 VALORES ---
        st.subheader("📊 Los 35 del IBEX")
        columnas_valores = st.columns(3)
        for idx, item in enumerate(lista_resultados):
            with columnas_valores[idx % 3]:
                with st.expander(f"{item['semaforo']} {item['ticker']}: {item['precio']:.2f}€"):
                    st.write(f"**Estado:** {item['estado']} (RSI: {item['rsi']:.1f})")
                    # Gráfico de Velas
                    fig = go.Figure(data=[go.Candlestick(
                        x=item['df'].index[-30:],
                        open=item['df']['Open'][-30:],
                        high=item['df']['High'][-30:],
                        low=item['df']['Low'][-30:],
                        close=item['df']['Close'][-30:]
                    )])
                    fig.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Noticias
                    nombre = item['ticker'].split('.')[0]
                    st.markdown(f"[📰 Ver Noticias de {nombre}](https://www.google.com/search?q={nombre}+noticias+bolsa&tbm=nws)")
    else:
        st.error("No se han podido cargar los datos. Por favor, reintenta en unos minutos.")

st.divider()
st.subheader("💰 Simulador de Inversión")
inv = st.number_input("Capital a invertir (€):", value=1000)
