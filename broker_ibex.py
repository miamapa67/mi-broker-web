import streamlit as st
import yfinance as yf
import pandas as pd
from PIL import Image
import os

st.set_page_config(page_title="Miguel Terminal Ranking", layout="wide")

# Estilo Blanco Nítido
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

# --- 1. CABECERA ---
if os.path.exists("logo_miguel.png"):
    img = Image.open("logo_miguel.png")
    st.image(img, use_column_width=True)

st.title("🏹 Terminal Inteligente - MIGUEL")
st.write("Ranking de Oportunidades y Riesgos en el IBEX 35.")

# --- 2. LISTA COMPLETA IBEX 35 ---
ibex_35 = [
    "ANA.MC", "ACX.MC", "ACS.MC", "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "SAN.MC", "BKT.MC", "BBVA.MC",
    "CABK.MC", "CLNX.MC", "ENG.MC", "ELE.MC", "FER.MC", "FDR.MC", "GRF.MC", "IAG.MC", "IBE.MC", "ITX.MC",
    "IDR.MC", "COL.MC", "LOG.MC", "MAP.MC", "MEL.MC", "MRL.MC", "NTGY.MC", "PUIG.MC", "REE.MC", "REP.MC",
    "ROVI.MC", "SCYR.MC", "SLBA.MC", "TEF.MC", "UNI.MC"
]

if st.button('🚀 GENERAR RANKING Y ANALIZAR IBEX', use_container_width=True):
    lista_analisis = []
    
    with st.spinner('Escaneando el mercado...'):
        for t in ibex_35:
            try:
                tk = yf.Ticker(t)
                hist = tk.history(period="3mo")
                if hist.empty: continue
                
                precio_actual = float(hist['Close'].iloc[-1])
                
                # CÁLCULO RSI
                delta = hist['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi_val = 100 - (100 / (1 + rs.iloc[-1]))
                
                # DIVIDENDOS
                div_yield = tk.info.get('dividendYield', 0)
                if not div_yield:
                    divs = tk.dividends
                    if not divs.empty: div_yield = (divs.iloc[-1] * 2) / precio_actual
                
                lista_analisis.append({
                    "ticker": t,
                    "precio": precio_actual,
                    "rsi": rsi_val,
                    "div": div_yield * 100 if div_yield else 0
                })
            except: 
                continue # Si una acción falla, pasamos a la siguiente

    if lista_analisis:
        df_ranking = pd.DataFrame(lista_analisis)
        top_compras = df_ranking.sort_values(by="rsi").head(3)
        top_ventas = df_ranking.sort_values(by="rsi", ascending=False).head(3)

        col_rank1, col_rank2 = st.columns(2)
        with col_rank1:
            st.markdown("### 💎 TOP 3: COMPRA")
            for _, row in top_compras.iterrows():
                st.success(f"**{row['ticker']}** | RSI: {row['rsi']:.1f} | {row['precio']:.2f}€")
        with col_rank2:
            st.markdown("### ⚠️ TOP 3: RIESGO")
            for _, row in top_ventas.iterrows():
                st.error(f"**{row['ticker']}** | RSI: {row['rsi']:.1f} | {row['precio']:.2f}€")
        
        st.divider()

        # --- DETALLE DE LOS 35 (LÍNEA 99 CORREGIDA) ---
        st.subheader("📊 Detalle de los 35 Valores")
        cols = st.columns(3)
        for i, item in enumerate(lista_analisis):
            with cols[i % 3]:
                emoji = "🟢" if item['rsi'] < 30 else "🔴" if item['rsi'] > 70 else "⚪"
                with st.expander(f"{emoji} {item['ticker']}: {item['precio']:.2f}€"):
                    st.write(f"**Fuerza (RSI):** {item['rsi']:.1f}")
                    if item['div'] > 0: st.write(f"💰 **Div:** {item['div']:.2f}%")
                    
                    nombre_n = item['ticker'].split('.')[0]
                    # Aquí estaba el error (corregido):
                    url_news = f"https://www.google.com/search?q={nombre_n}+noticias+bolsa&tbm=nws"
                    st.markdown(f"[📰 Noticias]({url_news})")
                    st.markdown(f"[📊 Gráfico](https://www.google.com/finance/quote/{item['ticker'].replace('.MC', ':BME')})")

st.divider()

# --- CALCULADORA ---
st.subheader("💰 Simulador de Inversión")
c1, c2 = st.columns(2)
with c1:
    inver = st.number_input("Capital (€):", value=1000)
    acc_elegida = st.selectbox("Valor:", ibex_35)
    sub_obj = st.slider("Subida (%)", 1, 30, 5)
with c2:
    try:
        p_v = float(yf.Ticker(acc_elegida).history(period="1d")['Close'].iloc[-1])
        n_acc = int(inver / p_v)
        st.success(f"**Ganancia: +{(p_v * (sub_obj/100)) * n_acc:.2f}€**")
    except: st.write("Calculando...")
