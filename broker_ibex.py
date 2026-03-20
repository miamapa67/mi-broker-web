import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analista Robot Pro", layout="wide")

st.title("🤖 Analista Robot Pro")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Configuración")
    modo = st.radio("Selecciona modo:", ["Monitor General", "Buscador Individual", "Duelo de Acciones"])

# --- MODO 2: BUSCADOR INDIVIDUAL ---
if modo == "Buscador Individual":
    st.subheader("🔎 Análisis Detallado")
    t = st.text_input("Ticker (ej: BBVA.MC, TSLA):", value="SAN.MC").upper().strip()
    
    if t:
        try:
            ticker_obj = yf.Ticker(t)
            hist = ticker_obj.history(period="6mo")
            
            if not hist.empty:
                actual = float(hist['Close'].iloc[-1])
                media_20 = float(hist['Close'].tail(20).mean())
                
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.metric("Precio Actual", f"{actual:.2f}")
                    diff = ((actual/media_20)-1)*100
                    st.write(f"Vs Media 20d: {diff:.2f}%")
                    status = "COMPRA ✅" if actual > media_20 else "VENTA ❌"
                    color = "green" if actual > media_20 else "red"
                    st.markdown(f"### <span style='color:{color}'>{status}</span>", unsafe_allow_html=True)
                
                with c2:
                    # Creamos una gráfica "clásica" que no da errores de frontend
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.plot(hist.index, hist['Close'], color='#1f77b4')
                    ax.set_title(f"Evolución 6 meses: {t}")
                    plt.xticks(rotation=45)
                    st.pyplot(fig) # Esto envía una IMAGEN, evitando el error LargeUtf8
            else:
                st.warning("No hay datos.")
        except:
            st.error("Error al conectar con los datos.")

# --- MODO 1: MONITOR GENERAL ---
elif modo == "Monitor General":
    st.subheader("🇪🇸 Resumen IBEX 35")
    # Versión simplificada para evitar errores
    ibex_35 = ["SAN.MC", "BBVA.MC", "TEF.MC", "ITX.MC", "REP.MC", "IBE.MC", "IAG.MC"]
    data = yf.download(ibex_35, period="1mo")['Close']
    cols = st.columns(len(ibex_35))
    for i, ticker in enumerate(ibex_35):
        with cols[i]:
            val = data[ticker].iloc[-1]
            st.metric(ticker.replace(".MC",""), f"{val:.2f}€")

# --- MODO 3: DUELO ---
elif modo == "Duelo de Acciones":
    st.subheader("⚔️ Duelo")
    t1 = st.text_input("Acción 1:", "SAN.MC").upper()
    t2 = st.text_input("Acción 2:", "BBVA.MC").upper()
    if t1 and t2:
        df = yf.download([t1, t2], period="6mo")['Close']
        fig, ax = plt.subplots()
        ax.plot((df / df.iloc[0]) * 100)
        st.pyplot(fig)
   
   
