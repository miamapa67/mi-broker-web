import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Analista Robot Pro", layout="wide")

st.title("🤖 Analista Robot Pro")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Configuración")
    modo = st.radio("Selecciona modo:", ["Monitor General", "Buscador Individual", "Duelo de Acciones"])
    st.write("---")
    st.caption("Datos reales de Yahoo Finance")

# --- MODO 2: BUSCADOR INDIVIDUAL ---
if modo == "Buscador Individual":
    st.subheader("🔎 Análisis Detallado")
    t = st.text_input("Ticker (ej: BBVA.MC, TSLA):", value="SAN.MC").upper().strip()
    
    if t:
        try:
            ticker_obj = yf.Ticker(t)
            hist = ticker_obj.history(period="6mo")
            
            if not hist.empty:
                # Limpiamos los datos para que no den error visual
                df_plot = hist[['Close']].copy()
                actual = float(df_plot['Close'].iloc[-1])
                media_20 = float(df_plot['Close'].tail(20).mean())
                
                c1, c2 = st.columns([1, 3])
                with c1:
                    st.metric("Precio Actual", f"{actual:.2f}")
                    diff = ((actual/media_20)-1)*100
                    st.write(f"Vs Media 20d: {diff:.2f}%")
                    
                    status = "COMPRA ✅" if actual > media_20 else "VENTA ❌"
                    color = "green" if actual > media_20 else "red"
                    st.markdown(f"### **<span style='color:{color}'>{status}</span>**", unsafe_allow_html=True)
                
                with c2:
                    # Cambiamos st.line_chart por st.area_chart que suele ser más estable
                    st.area_chart(df_plot)
            else:
                st.warning("No hay datos para este símbolo.")
        except:
            st.error("Error de conexión con Yahoo Finance.")

# --- MODO 1: MONITOR GENERAL ---
elif modo == "Monitor General":
    st.subheader("🇪🇸 Semáforo del IBEX 35")
    ibex_35 = ["ANA.MC", "ACS.MC", "ACG.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", "BKT.MC", "BBVA.MC", "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC", "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC", "ROVI.MC", "SCYR.MC", "SLR.MC", "TEF.MC", "UNI.MC"]
    try:
        data_ibex = yf.download(ibex_35, period="1mo")['Close']
        cols = st.columns(5)
        for i, ticker in enumerate(ibex_35):
            with cols[i % 5]:
                serie = data_ibex[ticker].dropna()
                if not serie.empty:
                    act = float(serie.iloc[-1]); med = float(serie.tail(20).mean())
                    color = "green" if act > med else "red"
                    st.markdown(f"**{ticker.replace('.MC','')}**")
                    st.markdown(f"<span style='color:{color}; font-weight:bold;'>{'COMPRA' if act > med else 'VENTA'}</span>", unsafe_allow_html=True)
                    st.metric(label="Precio", value=f"{act:.2f}€", delta=f"{((act/med)-1)*100:.1f}%")
    except: st.write("Cargando...")

# --- MODO 3: DUELO ---
elif modo == "Duelo de Acciones":
    st.subheader("⚔️ Duelo de Rentabilidad")
    t1 = st.text_input("Acción 1:", "SAN.MC").upper()
    t2 = st.text_input("Acción 2:", "BBVA.MC").upper()
    if t1 and t2:
        df = yf.download([t1, t2], period="6mo")['Close']
        if not df.empty:
            st.area_chart((df / df.iloc[0]) * 100)
   
   
