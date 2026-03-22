import streamlit as st
import pandas as pd

st.set_page_config(page_title="Miguel Terminal", layout="wide")
st.title("🏹 Terminal IBEX - MIGUEL")

# Lista de acciones con sus códigos para Google Finance
acciones = {
    "Santander": "BME:SAN",
    "BBVA": "BME:BBVA",
    "Telefónica": "BME:TEF",
    "Inditex": "BME:ITX",
    "IAG": "BME:IAG"
}

st.subheader("📊 Acceso Directo al Mercado")
st.write("Debido a los bloqueos de Yahoo, he creado este panel de acceso rápido:")

cols = st.columns(len(acciones))

for i, (nombre, ticker) in enumerate(acciones.items()):
    with cols[i]:
        # Creamos un botón que te lleva directo al gráfico real
        url = f"https://www.google.com/finance/quote/{ticker}"
        st.markdown(f"### {nombre}")
        st.link_button(f"👁️ Ver {nombre}", url, use_container_width=True)

st.divider()

# --- CALCULADORA QUE SIEMPRE FUNCIONA ---
st.subheader("💰 Calculadora de Ganancias Automática")
col1, col2 = st.columns(2)

with col1:
    inversion = st.number_input("¿Cuánto dinero vas a meter? (€)", value=1000, step=100)
    precio_compra = st.number_input("Precio actual de la acción (€)", value=10.0, step=0.1)
    
with col2:
    objetivo = st.slider("Subida esperada (%)", 1, 50, 10)
    ganancia = inversion * (objetivo / 100)
    total = inversion + ganancia
    
    st.metric("Beneficio Estimado", f"+{ganancia:.2f}€", delta=f"{objetivo}%")
    st.info(f"Si sube un {objetivo}%, retirarías un total de **{total:.2f}€**")

st.divider()
st.info("💡 Miguel, cuando Yahoo desbloquee la IP de Streamlit (suele tardar unas horas), podremos volver a ver los gráficos automáticos. Mientras tanto, usa esta terminal para calcular tus beneficios.")
