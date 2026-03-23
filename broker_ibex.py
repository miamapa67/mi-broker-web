import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Miguel Terminal PRO", layout="wide")

# Diseño profesional
st.markdown("<style>.stApp { background-color: #f8f9fa; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal Inteligente IBEX 35 - MIGUEL")

# --- 1. SECTORES CONFIGURADOS ---
sectores = {
    "🏦 BANCA": ["SAN.MC", "BBVA.MC", "CABK.MC", "SAB.MC", "BKT.MC", "UNI.MC"],
    "⚡ ENERGÍA": ["IBE.MC", "REP.MC", "NTGY.MC", "ELE.MC", "ENG.MC", "REE.MC", "SLBA.MC"],
    "🛍️ CONSUMO/IND": ["ITX.MC", "ANA.MC", "ACS.MC", "FER.MC", "ACX.MC", "MTS.MC", "IAG.MC"],
    "📡 TECNOLOGÍA": ["TEF.MC", "CLNX.MC", "IDR.MC", "AMS.MC"],
    "🧪 OTROS": ["GRF.MC", "ROVI.MC", "COL.MC", "MRL.MC", "AENA.MC"]
}

# Sidebar: Filtros y Calculadora
with st.sidebar:
    st.header("⚙️ PANEL DE CONTROL")
    sector_sel = st.selectbox("Elegir Sector para Analizar:", list(sectores.keys()))
    st.divider()
    st.header("💰 CALCULADORA")
    capital = st.number_input("Inversión (€):", value=1000)

# --- 2. EL MOTOR DE ANÁLISIS ---
if st.button(f"🚀 ANALIZAR SECTOR {sector_sel}", use_container_width=True):
    lista_analisis = []
    progreso = st.progress(0)
    
    with st.spinner(f'Analizando {sector_sel}...'):
        for i, t in enumerate(sectores[sector_sel]):
            try:
                # Descarga con "disfraz" y tiempo de espera
                ticker = yf.Ticker(t)
                df = ticker.history(period="1mo")
                
                if not df.empty:
                    # Precio y RSI
                    p_act = float(df['Close'].iloc[-1])
                    delta = df['Close'].diff()
                    up = delta.clip(lower=0).rolling(window=14).mean()
                    down = -1 * delta.clip(upper=0).rolling(window=14).mean()
                    rs = up / (down + 0.00001)
                    rsi = 100 - (100 / (1 + rs.iloc[-1]))
                    
                    # Semáforo
                    if rsi < 40: sem, est = "🟢", "COMPRA"
                    elif rsi > 60: sem, est = "🔴", "RIESGO"
                    else: sem, est = "⚪", "NEUTRO"
                    
                    lista_analisis.append({
                        "ticker": t, "precio": p_act, "rsi": rsi, 
                        "emoji": sem, "estado": est, "df": df
                    })
                
                time.sleep(0.5) # Pausa para que no nos bloqueen
                progreso.progress((i + 1) / len(sectores[sector_sel]))
            except:
                continue

    if lista_analisis:
        df_rank = pd.DataFrame(lista_analisis)
        
        # --- 3. TOP 3 Y FILTROS ---
        st.subheader(f"🏆 Ranking de Oportunidades: {sector_sel}")
        c1, c2 = st.columns(2)
        with c1:
            mejores = df_rank.sort_values("rsi").head(2)
            st.success("💎 MEJORES PARA COMPRAR")
            for _, r in mejores.iterrows():
                st.write(f"{r['emoji']} **{r['ticker']}** - {r['precio']:.2f}€")
        with c2:
            peores = df_rank.sort_values("rsi", ascending=False).head(2)
            st.error("⚠️ VALORES EN RIESGO")
            for _, r in peores.iterrows():
                st.write(f"{r['emoji']} **{r['ticker']}** - {r['precio']:.2f}€")

        st.divider()

        # --- 4. DETALLE INDIVIDUAL ---
        st.subheader("📊 Gráficos y Noticias")
        cols = st.columns(3)
        for idx, item in enumerate(lista_analisis):
            with cols[idx % 3]:
                with st.expander(f"{item['emoji']} {item['ticker']} - {item['precio']:.2f}€"):
                    st.write(f"RSI: {item['rsi']:.1f} ({item['estado']})")
                    # Gráfico mini
                    fig = go.Figure(data=[go.Scatter(x=item['df'].index[-15:], y=item['df']['Close'][-15:], mode='lines+markers')])
                    fig.update_layout(height=150, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
                    # Noticias
                    n = item['ticker'].split('.')[0]
                    st.markdown(f"[📰 Ver Noticias {n}](https://www.google.com/search?q={n}+noticias+bolsa&tbm=nws)")
    else:
        st.error("❌ El servidor de bolsa sigue bloqueado. Intenta de nuevo en unos minutos.")
