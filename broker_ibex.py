import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import time
import random

# Configuración de página ancha y profesional
st.set_page_config(page_title="Miguel Terminal 360 Pro", layout="wide")

# Estilo Blanco Nítido
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

# --- 1. CABECERA ---
st.title("🏹 Terminal Inteligente IBEX 35 - MIGUEL")
st.write("Análisis de Oportunidades, Semáforos RSI, Gráficos Interactivos de Línea y Noticias.")

# --- 2. DICCIONARIO OFICIAL POR SECTORES ---
sectores = {
    "Banca": ["SAN.MC", "BBVA.MC", "CABK.MC", "SAB.MC", "BKT.MC", "UNI.MC"],
    "Energía": ["IBE.MC", "REP.MC", "NTGY.MC", "ELE.MC", "ENG.MC", "REE.MC", "SLBA.MC"],
    "Ind. y Consumo": ["ITX.MC", "ANA.MC", "ACS.MC", "FER.MC", "ACX.MC", "MTS.MC", "IAG.MC", "PUIG.MC"],
    "Tecno y Telco": ["TEF.MC", "CLNX.MC", "IDR.MC", "AMS.MC"],
    "Otros": ["GRF.MC", "ROVI.MC", "COL.MC", "MRL.MC", "LOG.MC", "AENA.MC", "SCYR.MC", "FDR.MC", "MEL.MC"]
}

# --- 3. FILTROS LATERALES (SIDEBAR) ---
st.sidebar.header("🎯 Filtros de Mercado")
sector_sel = st.sidebar.multiselect("Seleccionar Sectores:", list(sectores.keys()), default=list(sectores.keys()))

# Crear lista plana de tickers seleccionados basándonos en los sectores
tickers_finales = []
for s in sector_sel:
    tickers_finales.extend(sectores[s])

# --- 4. BOTÓN DE ESCÁNER TOTAL ---
if st.button('🚀 EJECUTAR ANÁLISIS 360 (SEMÁFOROS Y RANKING)', use_container_width=True):
    lista_analisis = []
    progreso = st.progress(0)
    status_text = st.empty()
    
    with st.spinner('Analizando el IBEX 35 con gráficos interactivos...'):
        # TRUCO DE CAMUFLAJE: Pequeñas pausas para evitar bloqueos de Yahoo
        for i, t in enumerate(tickers_finales):
            try:
                status_text.text(f"Analizando {t}... ({i+1}/{len(tickers_finales)})")
                # Descarga protegida: solo 1 mes para que sea ultra-rápido
                df = yf.download(t, period="1mo", interval="1d", progress=False, timeout=8)
                
                if not df.empty and len(df) > 10:
                    p_act = float(df['Close'].iloc[-1])
                    
                    # --- CÁLCULO RSI (EL MOTOR DEL SEMÁFORO) ---
                    delta = df['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rsi = 100 - (100 / (1 + (gain.iloc[-1] / (loss.iloc[-1] + 0.001))))
                    
                    # Clasificación para Filtros
                    if rsi < 35: sem, est = "🟢", "COMPRA"
                    elif rsi > 65: sem, est = "🔴", "RIESGO"
                    else: sem, est = "⚪", "NEUTRO"
                    
                    lista_analisis.append({
                        "ticker": t, "precio": p_act, "rsi": rsi, 
                        "emoji": sem, "estado": est, "df": df
                    })
                
                # Pausa técnica aleatoria para no parecer un robot pesado
                time.sleep(random.uniform(0.1, 0.2))
                progreso.progress((i + 1) / len(tickers_finales))
            except:
                continue

    status_text.empty()

    if lista_analisis:
        df_rank = pd.DataFrame(lista_analisis)
        
        # --- 5. FILTROS Y RANKINGS (TOP 3) ---
        st.subheader("🏆 Filtro de Oportunidades y Riesgos")
        c_top1, c_top2 = st.columns(2)
        
        with c_top1:
            mejores = df_rank.sort_values("rsi").head(3)
            st.success("💎 TOP 3 COMPRA (RSI Bajo)")
            for _, r in mejores.iterrows():
                st.write(f"{r['emoji']} **{r['ticker']}** - Precio: {r['precio']:.2f}€ (RSI: {r['rsi']:.1f})")
        
        with c_top2:
            peores = df_rank.sort_values("rsi", ascending=False).head(3)
            st.error("⚠️ TOP 3 RIESGO (RSI Alto)")
            for _, r in peores.iterrows():
                st.write(f"{r['emoji']} **{r['ticker']}** - Precio: {r['precio']:.2f}€ (RSI: {r['rsi']:.1f})")

        st.divider()

        # --- 6. CUADRÍCULA DE VALORES CON GRÁFICOS INTERACTIVOS ---
        st.subheader("📊 Análisis Individual y Noticias")
        cols = st.columns(3)
        for idx, item in enumerate(lista_analisis):
            with cols[idx % 3]:
                with st.expander(f"{item['emoji']} {item['ticker']}: {item['precio']:.2f}€"):
                    st.write(f"**RSI:** {item['rsi']:.1f} | **Estado:** {item['estado']}")
                    
                    # --- GRÁFICO INTERACTIVO DE LÍNEA Ultraligero ---
                    # Mostramos los últimos 30 días
                    fig = go.Figure(data=[go.Scatter(
                        x=item['df'].index, 
                        y=item['df']['Close'], 
                        mode='lines', # Solo línea para velocidad
                        line=dict(color='#1f77b4', width=2),
                        name='Precio'
                    )])
                    
                    # Diseño limpio para que quepa bien en las tarjetas
                    fig.update_layout(
                        height=150, 
                        margin=dict(l=0, r=0, t=0, b=0), 
                        xaxis_visible=False, # Ocultamos fechas para limpiar
                        yaxis=dict(title="€", side="right"),
                        hovermode="x unified" # Muestra precio al pasar ratón
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Radar de Noticias e Info
                    n_limpio = item['ticker'].split('.')[0]
                    col_info1, col_info2 = st.columns(2)
                    with col_info1:
                        st.markdown(f"[📰 Noticias {n_limpio}](https://www.google.com/search?q={n_limpio}+noticias+bolsa&tbm=nws)")
                    with col_info2:
                        st.markdown(f"[📊 Google Finance](https://www.google.com/finance/quote/{item['ticker'].replace('.MC', ':BME')})")

    else:
        st.error("⚠️ Yahoo sigue bloqueando la IP de Streamlit Cloud por hoy.")
        st.info("💡 Miguel: Intenta abrir la app desde tu MÓVIL (con datos 4G/5G, desconectando el WiFi de casa). Si desde el móvil funciona, el problema es el WiFi de tu casa que Yahoo ha bloqueado temporalmente.")

st.divider()
# --- 7. CALCULADORA DE OPERACIÓN ---
st.subheader("💰 Calculadora de Operación Rápida")
inv = st.number_input("Inversión (€):", value=1000, step=500)
