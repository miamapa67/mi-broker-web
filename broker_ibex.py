import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Miguel Terminal PRO", layout="wide")

# Estilo profesional
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

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
if st.button(f"🚀 LANZAR ESCÁNER: {sector_sel}", use_container_width=True):
    lista_analisis = []
    progreso = st.progress(0)
    status_msg = st.empty()
    
    with st.spinner(f'Analizando {sector_sel}...'):
        for i, t in enumerate(sectores[sector_sel]):
            try:
                status_msg.text(f"Analizando {t}...")
                tk = yf.Ticker(t)
                df = tk.history(period="1mo")
                
                if not df.empty:
                    p_act = float(df['Close'].iloc[-1])
                    # Cálculo RSI (Semáforo)
                    delta = df['Close'].diff()
                    up = delta.clip(lower=0).rolling(window=14).mean()
                    down = -1 * delta.clip(upper=0).rolling(window=14).mean()
                    rs = up / (down + 0.00001)
                    rsi = 100 - (100 / (1 + rs.iloc[-1]))
                    
                    # Semáforo de colores
                    if rsi < 40: sem, col, est = "🟢", "green", "COMPRA"
                    elif rsi > 60: sem, col, est = "🔴", "red", "RIESGO"
                    else: sem, col, est = "⚪", "gray", "NEUTRO"
                    
                    lista_analisis.append({
                        "ticker": t, "precio": p_act, "rsi": rsi, 
                        "emoji": sem, "color": col, "estado": est, "df": df
                    })
                
                time.sleep(0.2)
                progreso.progress((i + 1) / len(sectores[sector_sel]))
            except:
                continue
    
    status_msg.empty()

    if lista_analisis:
        df_rank = pd.DataFrame(lista_analisis)
        
        # --- 3. RANKING DE OPORTUNIDADES (TOP 3) ---
        st.subheader(f"🏆 Ranking de Selección: {sector_sel}")
        c1, c2 = st.columns(2)
        
        with c1:
            mejores = df_rank.sort_values("rsi").head(3)
            st.markdown("### 💎 TOP 3: MEJOR COMPRA")
            for _, r in mejores.iterrows():
                st.info(f"{r['emoji']} **{r['ticker']}** - {r['precio']:.2f}€ (RSI: {r['rsi']:.1f})")
        
        with c2:
            peores = df_rank.sort_values("rsi", ascending=False).head(3)
            st.markdown("### ⚠️ TOP 3: MAYOR RIESGO")
            for _, r in peores.iterrows():
                st.error(f"{r['emoji']} **{r['ticker']}** - {r['precio']:.2f}€ (RSI: {r['rsi']:.1f})")

        st.divider()

        # --- 4. DETALLE INDIVIDUAL CON GRÁFICOS Y NOTICIAS ---
        st.subheader("📊 Análisis Detallado y Noticias")
        cols = st.columns(3)
        for idx, item in enumerate(lista_analisis):
            with cols[idx % 3]:
                # Tarjeta visual
                with st.container(border=True):
                    st.markdown(f"#### {item['emoji']} {item['ticker']}")
                    st.write(f"**Precio:** {item['precio']:.2f}€")
                    st.write(f"**Estado:** {item['estado']} (RSI: {item['rsi']:.1f})")
                    
                    # Gráfico mini
                    fig = go.Figure(data=[go.Scatter(x=item['df'].index[-15:], y=item['df']['Close'][-15:], mode='lines+markers', line=dict(color=item['color']))])
                    fig.update_layout(height=140, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Botón de Noticias Individual
                    nombre_corto = item['ticker'].split('.')[0]
                    st.link_button(f"📰 Noticias de {nombre_corto}", f"https://www.google.com/search?q={nombre_corto}+noticias+bolsa&tbm=nws", use_container_width=True)
    else:
        st.error("Error al recuperar datos. Pulsa de nuevo.")

st.divider()
st.subheader("💰 Calculadora Rápida")
inv = st.number_input("Inversión (€):", value=1000)
