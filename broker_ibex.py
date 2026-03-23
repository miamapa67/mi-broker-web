import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import time
import requests

st.set_page_config(page_title="Miguel IBEX 35 Analizador", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Estrategia IBEX 35: RSI + Tendencia 20 Días")

# --- 1. LISTA OFICIAL IBEX 35 ---
ibex_35 = [
    "ANA.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", "BKT.MC", "BBVA.MC",
    "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC",
    "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC",
    "ROVI.MC", "SCYR.MC", "SLBA.MC", "TEF.MC", "UNI.MC"
]

# --- 2. MOTOR DE ANÁLISIS CON DISFRAZ ---
if st.button('🚀 LANZAR ESCÁNER DE MERCADO', use_container_width=True):
    resultados = []
    progreso = st.progress(0)
    status_msg = st.empty()
    
    # Truco: Sesión con "User-Agent" para evitar el bloqueo de Yahoo
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    sesion = requests.Session()
    sesion.headers.update(headers)

    with st.spinner('Analizando el mercado...'):
        for i, t in enumerate(ibex_35):
            try:
                status_msg.text(f"Analizando {t}...")
                # Descarga rápida individual con disfraz
                tk = yf.Ticker(t, session=sesion)
                df = tk.history(period="3mo")
                
                if not df.empty and len(df) >= 20:
                    p_actual = float(df['Close'].iloc[-1])
                    p_hace_20 = float(df['Close'].iloc[-20])
                    var_20d = ((p_actual - p_hace_20) / p_hace_20) * 100
                    
                    # Cálculo RSI 14
                    delta = df['Close'].diff()
                    up = delta.clip(lower=0).rolling(window=14).mean()
                    down = -1 * delta.clip(upper=0).rolling(window=14).mean()
                    rs = up / (down + 0.00001)
                    rsi = 100 - (100 / (1 + rs.iloc[-1]))
                    
                    if rsi < 40: sem, col = "🟢 COMPRA", "green"
                    elif rsi > 60: sem, col = "🔴 RIESGO", "red"
                    else: sem, col = "⚪ NEUTRO", "gray"
                    
                    resultados.append({
                        "Ticker": t, "Precio": p_actual, "Var 20d (%)": var_20d,
                        "RSI": rsi, "Semáforo": sem, "Color": col, "df": df
                    })
                
                time.sleep(0.15) # Pausa humana para no ser baneados
                progreso.progress((i + 1) / len(ibex_35))
            except: continue

    status_msg.empty()

    if resultados:
        df_res = pd.DataFrame(resultados)
        
        # --- 3. TOP 3: OPCIONES DE COMPRA ---
        st.subheader("🚥 SEMÁFORO: TOP 3 OPCIONES DE COMPRA")
        top_compra = df_res.sort_values("RSI").head(3)
        
        c_top = st.columns(3)
        for idx, (_, r) in enumerate(top_compra.iterrows()):
            with c_top[idx]:
                st.success(f"🥇 OPCIÓN {idx+1}: {r['Ticker']}")
                st.metric("RSI (Fuerza)", f"{r['RSI']:.1f}", delta="Oportunidad" if r['RSI'] < 30 else None)
                st.write(f"**Variación 20 días:** {r['Var 20d (%)']:.2f}%")
                st.write(f"**Precio Actual:** {r['Precio']:.2f}€")
                n_limpio = r['Ticker'].split('.')[0]
                st.markdown(f"[📰 Noticias {n_limpio}](https://www.google.com/search?q={n_limpio}+noticias+bolsa&tbm=nws)")

        st.divider()

        # --- 4. LISTADO DE LOS 35 ---
        st.subheader("📊 Análisis de Fuerza (RSI)")
        st.dataframe(df_res[["Ticker", "Semáforo", "Precio", "RSI", "Var 20d (%)"]].sort_values("RSI"), use_container_width=True, hide_index=True)
    else:
        st.error("❌ Yahoo sigue bloqueando la IP. Prueba a abrir la app desde tu móvil con el WiFi quitado.")

# CALCULADORA
st.sidebar.subheader("💰 Calculadora")
inv = st.sidebar.number_input("Inversión (€):", value=1000)
