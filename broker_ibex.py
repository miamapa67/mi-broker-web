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

# --- MODO 2: BUSCADOR INDIVIDUAL (Corregido y reforzado) ---
if modo == "Buscador Individual":
    st.subheader("🔎 Análisis Detallado")
    t = st.text_input("Ticker (ej: NVDA, TSLA, SAN.MC):", value="SAN.MC").upper().strip()
    
    if t:
        try:
            # Usamos un método de descarga más estable
            ticker_obj = yf.Ticker(t)
            hist = ticker_obj.history(period="1y")
            
            if not hist.empty:
                d = hist['Close']
                c1, c2 = st.columns([1, 3])
                with c1:
                    actual = float(d.iloc[-1])
                    # Media de los últimos 20 días de cierre
                    media_val = float(d.tail(20).mean())
                    st.metric("Precio Actual", f"{actual:.2f}")
                    
                    diff = ((actual/media_val)-1)*100
                    st.write(f"Vs Media 20d: {diff:.2f}%")
                    
                    status = "COMPRA ✅" if actual > media_val else "VENTA ❌"
                    color = "green" if actual > media_val else "red"
                    st.markdown(f"### **<span style='color:{color}'>{status}</span>**", unsafe_allow_html=True)
                with c2:
                    st.line_chart(d)
            else:
                st.warning(f"No hay datos para {t}. ¿Has puesto bien el punto? Ej: SAN.MC")
        except Exception as e:
            st.error(f"Error de conexión: Yahoo está saturado. Reintenta en 10 segundos.")

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
                    st.markdown(f"**{ticker.replace('.MC','')}** : <span style='color:{color}'>{'OK' if act > med else 'BAJA'}</span>", unsafe_allow_html=True)
                    st.metric(label="Precio", value=f"{act:.2f}€", delta=f"{((act/med)-1)*100:.1f}%")
    except: st.write("Refrescando monitor...")

# --- MODO 3: DUELO ---
elif modo == "Duelo de Acciones":
    st.subheader("⚔️ Duelo")
    t1 = st.text_input("Acción 1:", value="SAN.MC").upper().strip()
    t2 = st.text_input("Acción 2:", value="BBVA.MC").upper().strip()
    if t1 and t2:
        df = yf.download([t1, t2], period="6mo")['Close']
        if not df.empty:
            st.line_chart((df / df.iloc[0]) * 100)
           
   
   
