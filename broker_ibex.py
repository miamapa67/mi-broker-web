import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Miguel IBEX Analizador", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Estrategia IBEX 35: RSI + Tendencia 20 Días")

# --- 1. LISTA OFICIAL 35 ---
ibex_35 = [
    "ANA.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", "BKT.MC", "BBVA.MC",
    "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC",
    "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC",
    "ROVI.MC", "SCYR.MC", "SLBA.MC", "TEF.MC", "UNI.MC"
]

# --- 2. MOTOR DE ANÁLISIS ---
if st.button('🚀 LANZAR ESCÁNER DEFINITIVO', use_container_width=True):
    resultados = []
    progreso = st.progress(0)
    status = st.empty()
    
    with st.spinner('Analizando los 35 valores...'):
        for i, t in enumerate(ibex_35):
            try:
                status.text(f"Analizando {t}...")
                # Usamos un periodo corto para evitar bloqueos
                tk = yf.Ticker(t)
                df = tk.history(period="1mo") # 1 mes es suficiente para 20 días + RSI
                
                if not df.empty and len(df) >= 15:
                    p_act = df['Close'].iloc[-1]
                    p_ini = df['Close'].iloc[0]
                    var_20d = ((p_act - p_ini) / p_ini) * 100
                    
                    # RSI Simplificado (Fuerza Relativa)
                    delta = df['Close'].diff()
                    gain = delta.where(delta > 0, 0).rolling(window=14).mean().iloc[-1]
                    loss = -delta.where(delta < 0, 0).rolling(window=14).mean().iloc[-1]
                    rsi = 100 - (100 / (1 + (gain / (loss + 0.001))))
                    
                    # Semáforo de Compra
                    if rsi < 35: sem, col = "🟢 COMPRA", "green"
                    elif rsi > 65: sem, col = "🔴 RIESGO", "red"
                    else: sem, col = "⚪ ESPERAR", "gray"
                    
                    resultados.append({
                        "Ticker": t, "Precio": round(p_act, 2), "RSI": round(rsi, 1),
                        "Variación 20d": f"{var_20d:.2f}%", "Semáforo": sem, "df": df
                    })
                
                time.sleep(0.05)
                progreso.progress((i + 1) / len(ibex_35))
            except: continue

    status.empty()

    if resultados:
        df_res = pd.DataFrame(resultados)
        
        # --- 3. EL TOP 3 DE MIGUEL (OPCIONES DE COMPRA) ---
        st.subheader("🚥 SEMÁFORO: TOP 3 MEJORES OPCIONES DE COMPRA")
        # El criterio es RSI más bajo (valor más barato/sobrevendido)
        top_3 = df_res.sort_values("RSI").head(3)
        
        c1, c2, c3 = st.columns(3)
        for idx, (index, row) in enumerate(top_3.iterrows()):
            with [c1, c2, c3][idx]:
                st.success(f"🥇 OPCIÓN {idx+1}: {row['Ticker']}")
                st.metric("Precio Actual", f"{row['Precio']}€")
                st.write(f"**Fuerza RSI:** {row['RSI']} (Sobreventa)")
                st.write(f"**Tendencia 20 días:** {row['Variación 20d']}")
                name = row['Ticker'].split('.')[0]
                st.markdown(f"[📰 Ver Noticias {name}](https://www.google.com/search?q={name}+bolsa+noticias&tbm=nws)")

        st.divider()

        # --- 4. LISTADO GENERAL ---
        st.subheader("📊 Análisis de los 35 Valores")
        st.dataframe(df_res[["Ticker", "Semáforo", "Precio", "RSI", "Variación 20d"]].sort_values("RSI"), use_container_width=True, hide_index=True)
    else:
        st.error("⚠️ El servidor de datos está saturado. Intenta pulsar de nuevo en 30 segundos.")

st.sidebar.subheader("💰 Calculadora")
inv = st.sidebar.number_input("Inversión (€):", value=1000)
