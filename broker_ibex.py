import streamlit as st
import yfinance as yf
import pandas as pd
from PIL import Image
import os

st.set_page_config(page_title="Miguel Terminal 360", layout="wide")

# Estilo Blanco Nítido
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

# --- 1. CABECERA ---
if os.path.exists("logo_miguel.png"):
    img = Image.open("logo_miguel.png")
    st.image(img, use_column_width=True)

st.title("🏹 Terminal de Inversión 360 - MIGUEL")
st.write("Semáforo RSI + Potencial de Analistas + Dividendos + Noticias.")

# --- 2. LISTA COMPLETA IBEX 35 ---
ibex_35 = [
    "ANA.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", "BKT.MC", "BBVA.MC",
    "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC",
    "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC",
    "ROVI.MC", "SCYR.MC", "SLBA.MC", "TEF.MC", "UNI.MC"
]

if st.button('🚀 EJECUTAR ANÁLISIS TOTAL DEL IBEX', use_container_width=True):
    lista_analisis = []
    
    with st.spinner('Analizando los 35 valores paso a paso...'):
        for t in ibex_35:
            try:
                tk = yf.Ticker(t)
                hist = tk.history(period="3mo")
                if hist.empty: continue
                
                precio_actual = float(hist['Close'].iloc[-1])
                info = tk.info
                
                # --- RSI (Semáforo) ---
                delta = hist['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi_val = 100 - (100 / (1 + rs.iloc[-1]))
                
                # --- POTENCIAL (Analistas) ---
                p_obj = info.get('targetMeanPrice')
                potencial = ((p_obj - precio_actual) / precio_actual) * 100 if p_obj else 0
                
                # --- DIVIDENDOS ---
                div_yield = info.get('dividendYield', 0)
                if not div_yield:
                    divs = tk.dividends
                    if not divs.empty: div_yield = (divs.iloc[-1] * 2) / precio_actual
                
                lista_analisis.append({
                    "ticker": t, "precio": precio_actual, "rsi": rsi_val,
                    "potencial": potencial, "div": div_yield * 100 if div_yield else 0
                })
            except: continue

    if lista_analisis:
        df = pd.DataFrame(lista_analisis)
        
        # --- BLOQUE 1: EL SEMÁFORO (TOP 3 COMPRA / VENTA) ---
        st.markdown("## 🚦 Semáforo de Oportunidades (RSI)")
        c_rsi1, c_rsi2 = st.columns(2)
        with c_rsi1:
            st.success("💎 TOP 3: MEJORES COMPRAS (RSI bajo)")
            for _, row in df.sort_values(by="rsi").head(3).iterrows():
                st.write(f"**{row['ticker']}** | RSI: {row['rsi']:.1f} | {row['precio']:.2f}€")
        with c_rsi2:
            st.error("⚠️ TOP 3: MÁS CAROS (RSI alto)")
            for _, row in df.sort_values(by="rsi", ascending=False).head(3).iterrows():
                st.write(f"**{row['ticker']}** | RSI: {row['rsi']:.1f} | {row['precio']:.2f}€")

        st.divider()

        # --- BLOQUE 2: EL POTENCIAL (TOP 3 ANALISTAS) ---
        st.markdown("## 🎯 Ranking de Potencial (Precio Objetivo)")
        top_pot = df.sort_values(by="potencial", ascending=False).head(3)
        c_pot1, c_pot2, c_pot3 = st.columns(3)
        cols_pot = [c_pot1, c_pot2, c_pot3]
        for idx, (_, row) in enumerate(top_pot.iterrows()):
            cols_pot[idx].info(f"**{row['ticker']}**\n\nSubida: **+{row['potencial']:.1f}%**")

        st.divider()

        # --- DETALLE GENERAL ---
        st.subheader("📊 Detalle de los 35 Valores")
        cols = st.columns(3)
        for i, item in enumerate(lista_analisis):
            with cols[i % 3]:
                emo = "🟢" if item['rsi'] < 30 else "🔴" if item['rsi'] > 70 else "⚪"
                with st.expander(f"{emo} {item['ticker']}: {item['precio']:.2f}€"):
                    st.write(f"**RSI:** {item['rsi']:.1f} | **Potencial:** +{item['potencial']:.1f}%")
                    if item['div'] > 0: st.write(f"💰 **Div:** {item['div']:.2f}%")
                    n_n = item['ticker'].split('.')[0]
                    st.markdown(f"[📰 Noticias](https://www.google.com/search?q={n_n}+noticias+bolsa&tbm=nws) | [📊 Gráfico](https://www.google.com/finance/quote/{item['ticker'].replace('.MC', ':BME')})")

st.divider()

# --- CALCULADORA ---
st.subheader("💰 Simulador de Beneficios")
c_sim1, c_sim2 = st.columns(2)
with c_sim1:
    inver = st.number_input("Capital (€):", value=1000)
    acc = st.selectbox("Valor:", ibex_35)
    sub = st.slider("Subida (%)", 1, 30, 10)
with c_sim2:
    try:
        p_v = float(yf.Ticker(acc).history(period="1d")['Close'].iloc[-1])
        st.success(f"**Ganancia: +{(p_v * (sub/100)) * (int(inver/p_v)):.2f}€**")
    except: st.write("Calculando...")
