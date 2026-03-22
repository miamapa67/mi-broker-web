import streamlit as st

st.set_page_config(page_title="Miguel Terminal 35", layout="wide")

# Estilo Limpio
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal IBEX 35 - CONTROL TOTAL")
st.write("### 🚀 Panel de Acceso Directo y Análisis")

# --- LISTA OFICIAL 35 VALORES ---
ibex_35 = {
    "Acciona": "ANA:BME", "Acerinox": "ACX:BME", "ACS": "ACS:BME", "AENA": "AENA:BME", 
    "Amadeus": "AMS:BME", "ArcelorMittal": "MTS:BME", "Sabadell": "SAB:BME", "Santander": "SAN:BME", 
    "Bankinter": "BKT:BME", "BBVA": "BBVA:BME", "CaixaBank": "CABK:BME", "Cellnex": "CLNX:BME", 
    "Enagás": "ENG:BME", "Endesa": "ELE:BME", "Ferrovial": "FER:BME", "Fluidra": "FDR:BME", 
    "Grifols": "GRF:BME", "IAG": "IAG:BME", "Iberdrola": "IBE:BME", "Inditex": "ITX:BME", 
    "Indra": "IDR:BME", "Inm. Colonial": "COL:BME", "Logista": "LOG:BME", "Mapfre": "MAP:BME", 
    "Meliá Hotels": "MEL:BME", "Merlin Prop.": "MRL:BME", "Naturgy": "NTGY:BME", "Puig": "PUIG:BME", 
    "Redeia": "REE:BME", "Repsol": "REP:BME", "Rovi": "ROVI:BME", "Sacyr": "SCYR:BME", 
    "Solaria": "SLBA:BME", "Telefónica": "TEF:BME", "Unicaja": "UNI:BME"
}

# --- FILTROS RÁPIDOS ---
st.info("💡 Haz clic en cualquier valor para abrir su Gráfico Interactivo y Noticias en tiempo real (Sin bloqueos).")

columnas = st.columns(4) # 4 columnas para que quepan todos
for i, (nombre, ticker) in enumerate(ibex_35.items()):
    with columnas[i % 4]:
        url = f"https://www.google.com/finance/quote/{ticker}"
        st.link_button(f"📊 {nombre}", url, use_container_width=True)

st.divider()

# --- CALCULADORA DE BENEFICIOS (PLANIFICADOR) ---
st.subheader("💰 Calculadora de Operaciones")
c1, c2 = st.columns(2)

with c1:
    capital = st.number_input("Capital a invertir (€):", value=1000, step=100)
    precio_c = st.number_input("Precio de entrada (€):", value=10.0, step=0.1)
    
with c2:
    objetivo = st.slider("Objetivo de subida (%)", 1, 30, 10)
    ganancia = capital * (objetivo / 100)
    st.metric("Beneficio Estimado", f"+{ganancia:.2f}€", f"{objetivo}%")
    st.write(f"Si la acción llega a **{precio_c * (1 + objetivo/100):.2f}€**, habrás ganado la operación.")

st.divider()
st.write("⚠️ *Nota: El sistema de semáforos automáticos está temporalmente en pausa por el bloqueo de Yahoo Finance. Usa los botones de arriba para ver los datos oficiales.*")
