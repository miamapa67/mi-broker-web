import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="Miguel Terminal PRO", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal Inteligente IBEX 35 - MIGUEL")

# --- 1. CALCULADORA LATERAL ---
with st.sidebar:
    st.header("💰 CALCULADORA")
    capital = st.number_input("Inversión (€):", value=1000, step=100)
    st.divider()
    st.info("🟢 COMPRA: RSI < 35\n🔴 RIESGO: RSI > 65")

# --- 2. LISTA POR SECTORES ---
sectores = {
    "🏦 BANCA": ["SAN.MC", "BBVA.MC", "CABK.MC", "SAB.MC", "BKT.MC", "UNI.MC"],
    "⚡ ENERGÍA": ["IBE.MC", "REP.MC", "NTGY.MC", "ELE.MC", "ENG.MC", "REE.MC", "SLBA.MC"],
    "🏗️ IND/CONS": ["ITX.MC", "ANA.MC", "ACS.MC", "FER.MC", "ACX.MC", "MTS.MC", "IAG.MC", "PUIG.MC"],
    "📡 TECNO": ["TEF.MC", "CLNX.MC", "IDR.MC", "AMS.MC"],
    "🧬 OTROS": ["GRF.MC", "ROVI.MC", "COL.MC", "MRL.MC", "LOG.MC", "AENA.MC", "SCYR.MC", "FDR.MC", "MEL.MC"]
}

# --- 3. MOTOR DE CÁLCULO ---
def analizar_valor(ticker):
    try:
        # Descarga rápida de 1 mes
        df = yf.download(ticker, period="1mo", interval="1d", progress=False)
        if not df.empty:
            precio = float(df['Close'].iloc[-1])
            # Cálculo RSI
            delta = df['Close'].diff()
            up = delta.clip(lower=0).rolling(window=14).mean()
            down = -1 * delta.clip(upper=0).rolling(window=14).mean()
            rs = up.iloc[-1] / (down.iloc[-1] + 0.00001)
            rsi = 100 - (100 / (1 + rs))
            return precio, rsi
    except:
        return None, None
    return None, None

# --- 4. PANEL DE CONTROL ---
tab_list = st.tabs(list(sectores.keys()))

for i, sector in enumerate(sectores.keys()):
    with tab_list[i]:
        # Botón para activar el análisis por sector
        if st.button(f"🔍 ESCANEAR PRECIOS Y RSI - {sector}", key=f"btn_{sector}"):
            cols = st.columns(3)
            for idx, t in enumerate(sectores[sector]):
                precio, rsi = analizar_valor(t)
                
                # Lógica de colores del Semáforo
                if rsi and rsi < 35: 
                    color, txt, emoji = "#d4edda", "COMPRA", "🟢"
                elif rsi and rsi > 65: 
                    color, txt, emoji = "#f8d7da", "RIESGO", "🔴"
                else: 
                    color, txt, emoji = "#f8f9fa", "NEUTRO", "⚪"
                
                with cols[idx % 3]:
                    st.markdown(f"""
                        <div style="background-color:{color}; padding:20px; border-radius:15px; border:2px solid #eee; text-align:center; margin-bottom:10px;">
                            <h2 style="margin:0; color:#333;">{t}</h2>
                            <h1 style="margin:10px 0; color:#000;">{f'{precio:.2f}€' if precio else '---'}</h1>
                            <p style="font-size:1.2em; margin:0;"><b>RSI:</b> {f'{rsi:.1f}' if rsi else '---'}</p>
                            <hr style="margin:10px 0; border:0; border-top:1px solid #ccc;">
                            <h3 style="margin:0;">{emoji} {txt}</h3>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Enlaces directos
                    c1, c2 = st.columns(2)
                    with c1:
                        st.link_button("📊 Gráfico", f"https://www.google.com/finance/quote/{t.replace('.MC','')}:BME", use_container_width=True)
                    with c2:
                        st.link_button("📰 Noticias", f"https://www.google.com/search?q={t}+noticias+bolsa&tbm=nws", use_container_width=True)
                time.sleep(0.1) # Evita baneo de Yahoo
        else:
            st.info(f"Haz clic en el botón de arriba para cargar los precios de {sector}")

st.divider()
st.caption("Miguel Terminal v4.0 - Inteligencia Técnica")
