import streamlit as st

st.set_page_config(page_title="Miguel Terminal 360", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🏹 Terminal Profesional IBEX 35 - MIGUEL")
st.write("### 🚀 Panel de Control y Análisis Directo")

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

st.info("💡 Haz clic en los botones para abrir el análisis técnico, semáforos y noticias de Google Finance sin bloqueos.")

# --- CUADRÍCULA DE LOS 35 ---
cols = st.columns(4)
for i, (nombre, ticker) in enumerate(ibex_35.items()):
    with cols[i % 4]:
        url_g = f"https://www.google.com/finance/quote/{ticker}"
        st.link_button(f"📊 {nombre}", url_g, use_container_width=True)

st.divider()

# --- CALCULADORA DE POSICIONES ---
st.subheader("💰 Calculadora de Operación")
c1, c2 = st.columns(2)
with c1:
    cap = st.number_input("Capital (€):", value=1000)
    ent = st.number_input("Precio entrada (€):", value=10.0)
with c2:
    obj = st.slider("Objetivo (%)", 1, 30, 10)
    gan = cap * (obj / 100)
    st.metric("Beneficio", f"+{gan:.2f}€", f"{obj}%")

st.divider()
st.warning("⚠️ Nota: Los semáforos automáticos de Yahoo están bloqueados por el servidor. Usa los enlaces de arriba para ver el RSI y las Velas en tiempo real.")
