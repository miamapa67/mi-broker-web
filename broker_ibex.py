import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Miguel IBEX 35 Analizador", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Estrategia IBEX 35: RSI + Tendencia 20 Días")
st.write("Análisis técnico de alta precisión para Miguel")

# --- 1. LISTA COMPLETA 35 VALORES ---
ibex_35 = [
    "ANA.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", "BKT.MC", "BBVA.MC",
    "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC",
    "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC",
    "ROVI.MC", "SCYR.MC", "SLBA.MC", "TEF.MC", "UNI.MC"
]

# --- 2. MOTOR DE CÁLCULO ---
if st.button('🚀 LANZAR ESCÁNER DE MERCADO', use_container_width=True):
    resultados = []
    progreso = st.progress(0)
    
    with st.spinner('Analizando los 35 valores...'):
        for i, t in enumerate(ibex_35):
            try:
                # Descargamos datos de los últimos 2 meses para tener margen
                df = yf.download(t, period="2mo", interval="1d", progress=False)
                
                if not df.empty and len(df) >= 20:
                    # A. PRECIO ACTUAL Y VARIACIÓN 20 DÍAS
                    p_actual = float(df['Close'].iloc[-1])
                    p_hace_20 = float(df['Close'].iloc[-20])
                    var_20d = ((p_actual - p_hace_20) / p_hace_20) * 100
                    
                    # B. CÁLCULO RSI (14 periodos estándar)
                    delta = df['Close'].diff()
                    up = delta.clip(lower=0).rolling(window=14).mean()
                    down = -1 * delta.clip(upper=0).rolling(window=14).mean()
                    rs = up / (down + 0.00001)
                    rsi = 100 - (100 / (1 + rs.iloc[-1]))
                    
                    # C. LÓGICA SEMÁFORO
                    # Verde: RSI bajo (sobreventa) + Caída en 20 días (oportunidad de rebote)
                    if rsi < 40: sem, col = "🟢 COMPRA", "green"
                    elif rsi > 60: sem, col = "🔴 RIESGO", "red"
                    else: sem, col = "⚪ NEUTRO", "gray"
                    
                    resultados.append({
                        "Ticker": t, "Precio": p_actual, "Var 20d (%)": var_20d,
                        "RSI": rsi, "Semáforo": sem, "Color": col, "df": df
                    })
                
                time.sleep(0.1)
                progreso.progress((i + 1) / len(ibex_35))
            except: continue

    if resultados:
        df_res = pd.DataFrame(resultados)
        
        # --- 3. SEMÁFORO TOP 3: OPCIONES DE COMPRA ---
        st.subheader("🚥 SEMÁFORO: TOP 3 OPCIONES DE COMPRA (Basado en RSI)")
        # Filtramos los que tienen el RSI más bajo (potencial de subida)
        top_compra = df_res.sort_values("RSI").head(3)
        
        c_top = st.columns(3)
        for idx, (_, r) in enumerate(top_compra.iterrows()):
            with c_top[idx]:
                st.success(f"🥇 OPCIÓN {idx+1}: {r['Ticker']}")
                st.metric("RSI Actual", f"{r['RSI']:.1f}", delta="- Sobreventa" if r['RSI'] < 30 else None)
                st.write(f"**Variación 20 días:** {r['Var 20d (%)']:.2f}%")
                st.write(f"**Precio:** {r['Precio']:.2f}€")
                n_limpio = r['Ticker'].split('.')[0]
                st.markdown(f"[📰 Ver Noticias {n_limpio}](https://www.google.com/search?q={n_limpio}+noticias+bolsa&tbm=nws)")

        st.divider()

        # --- 4. TABLA COMPLETA DE LOS 35 ---
        st.subheader("📊 Análisis Detallado de los 35")
        
        # Formatear tabla para que se vea bonita
        df_tabla = df_res[["Ticker", "Semáforo", "Precio", "RSI", "Var 20d (%)"]]
        st.dataframe(df_tabla.sort_values("RSI"), use_container_width=True, hide_index=True)

        # Gráficos expansibles
        for item in resultados:
            with st.expander(f"{item['Semáforo']} | {item['Ticker']} - RSI: {item['RSI']:.1f}"):
                fig = go.Figure(data=[go.Scatter(x=item['df'].index[-20:], y=item['df']['Close'][-20:], mode='lines+markers', line=dict(color=item['Color']))])
                fig.update_layout(height=150, title="Evolución Últimos 20 Días", margin=dict(l=0,r=0,t=20,b=0))
                st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("No se han podido obtener datos. Inténtalo de nuevo en unos segundos.")

# --- CALCULADORA SIEMPRE AL FINAL ---
st.sidebar.divider()
st.sidebar.subheader("💰 Calculadora Miguel")
capital = st.sidebar.number_input("Inversión (€):", value=1000)
