import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Analista Robot Pro", layout="wide")

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Analista Robot Pro - Inteligencia de Mercado")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Configuración")
    modo = st.radio("Selecciona modo:", ["Monitor General", "Buscador Individual", "Duelo de Acciones"])
    st.write("---")
    st.caption("Datos reales de Yahoo Finance")

# --- MODO 1: MONITOR GENERAL ---
if modo == "Monitor General":
    st.subheader("🇪🇸 Semáforo del IBEX 35")
    ibex_35 = ["ANA.MC", "ACS.MC", "ACG.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", "BKT.MC", "BBVA.MC", "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC", "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC", "ROVI.MC", "SCYR.MC", "SLR.MC", "TEF.MC", "UNI.MC"]
    
    try:
        data_ibex = yf.download(ibex_35, period="40d")['Close']
        cols = st.columns(5)
        for i, ticker in enumerate(ibex_35):
            with cols[i % 5]:
                serie = data_ibex[ticker].dropna()
                if not serie.empty:
                    act = serie.iloc[-1]
                    med = serie.tail(20).mean()
                    alc = act > med
                    status = "COMPRA" if alc else "VENTA"
                    color = "green" if alc else "red"
                    st.markdown(f"**{ticker.replace('.MC','')}**")
                    st.markdown(f"<span style='color:{color}; font-weight:bold;'>{status}</span>", unsafe_allow_html=True)
                    st.metric(label="Precio", value=f"{act:.2f}€", delta=f"{((act/med)-1)*100:.1f}%")
    except: st.error("Error cargando el monitor.")

# --- MODO 2: BUSCADOR INDIVIDUAL ---
elif modo == "Buscador Individual":
    st.subheader("🔎 Análisis Detallado de Activo")
    t = st.text_input("Introduce Ticker (ej: NVDA, TSLA, SAN.MC):", value="SAN.MC").upper()
    if t:
        d = yf.download(t, period="1y")['Close']
        if not d.empty:
            c1, c2 = st.columns([1, 3])
            with c1:
                actual = d.iloc[-1]
                st.metric("Precio Actual", f"{actual:.2f}")
                st.write(f"Variación anual: {((actual/d.iloc[0])-1)*100:.2f}%")
            with c2:
                st.line_chart(d)

# --- MODO 3: DUELO DE ACCIONES ---
elif modo == "Duelo de Acciones":
    st.subheader("⚔️ Duelo de Rentabilidad")
    col_a, col_b = st.columns(2)
    with col_a: t1 = st.text_input("Acción 1:", value="SAN.MC").upper()
    with col_b: t2 = st.text_input("Acción 2:", value="BBVA.MC").upper()
    
    if t1 and t2:
        df = yf.download([t1, t2], period="6mo")['Close']
        # Normalizamos a 100 para comparar rentabilidad real
        df_norm = (df / df.iloc[0]) * 100
        st.line_chart(df_norm)
        st.info("Gráfica normalizada: Ambas empiezan en 100 para ver cuál crece más porcentualmente.")
