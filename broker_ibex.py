import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from PIL import Image # Añadimos esta herramienta para abrir imágenes
import os

st.set_page_config(page_title="Scanner Miguel Pro", layout="wide")

# Estilo
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

# --- CABECERA CON LOGO (FORZADO) ---
if os.path.exists("logo_miguel.png"):
    img = Image.open("logo_miguel.png")
    st.image(img, use_container_width=True) # Esto ajusta el logo al ancho de la pantalla
else:
    st.warning("Buscando logo...") # Si sale esto, es que GitHub aún no ha enviado el archivo al servidor
