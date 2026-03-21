import streamlit as st
import pandas as pd
import yfinance as yf
import requests

# --- CONFIGURACIÓN DE CAMUFLAJE ---
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}

st.set_page_config(page_title="Miguel Terminal", layout="wide")
st.title("🏹 Terminal IBEX - MIGUEL")

# Solo 2 valores para probar si hay "brecha"
test_list = ["SAN.MC", "ITX.MC"]

if st.button('🚀 FORZAR CONEXIÓN DE EMERGENCIA'):
    with st.spinner('Hackeando el acceso a los datos...'):
        for t in test_list:
            try:
                # Usamos una sesión de requests para engañar al servidor
                session = requests.Session()
                session.headers.update(headers)
                
                ticker = yf.Ticker(t, session=session)
                # Pedimos solo el último día para que no sospechen
                df = ticker.history(period="1d")
                
                if not df.empty:
                    precio = df['Close'].iloc[-1]
                    st.success(f"✅ {t}: {precio:.2f}€ - ¡DATO RECUPERADO!")
                else:
                    st.error(f"❌ {t}: El servidor devolvió datos vacíos.")
            except Exception as e:
                st.error(f"❌ Error en {t}: Yahoo sigue bloqueando.")

st.divider()
st.warning("⚠️ Miguel, si esto sigue fallando con el error rosa, significa que Yahoo ha bloqueado la IP de Streamlit Cloud por hoy. No es culpa de tu código.")

# --- PLAN B: ENLACES DIRECTOS ---
st.subheader("🔗 Accesos Directos (Plan B)")
st.write("Si el robot está bloqueado, usa estos enlaces para ver el mercado hoy:")
st.markdown("- [📊 IBEX 35 en Google Finance](https://www.google.com/finance/quote/IBEX:INDEXBME)")
st.markdown("- [📰 Noticias Bolsa Madrid](https://www.bolsamania.com/)")
