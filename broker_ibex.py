import yfinance as yf
import pandas as pd
import streamlit as st

# Configuramos la página web
st.set_page_config(page_title="Mi Broker Global", page_icon="🌍", layout="centered")

st.title("🌍 Mi Analista Robot - IBEX & Wall Street")
st.write("Analizando los mercados de España y Estados Unidos en tiempo real...")

# ¡AQUÍ ESTÁ LA MAGIA! Hemos ampliado tu cartera de activos
empresas_mercado = {
    # Gigantes del IBEX 35 (España)
    'Inditex': 'ITX.MC',
    'Banco Santander': 'SAN.MC',
    'Iberdrola': 'IBE.MC',
    'BBVA': 'BBVA.MC',
    'Telefónica': 'TEF.MC',
    'Repsol': 'REP.MC',
    'CaixaBank': 'CABK.MC',
    'Aena': 'AENA.MC',
    
    # Gigantes de Wall Street (EEUU)
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Nvidia': 'NVDA',
    'Tesla': 'TSLA',
    'Amazon': 'AMZN'
}

resultados = []
historicos = {} 

# Ponemos un "cargador" visual mientras descarga los datos
with st.spinner('Descargando datos globales (esto puede tardar unos segundos más)...'):
    for nombre, ticker in empresas_mercado.items():
        accion = yf.Ticker(ticker)
        historial = accion.history(period="6mo")
        
        if not historial.empty:
            historicos[nombre] = historial 
            
            precio_actual = historial['Close'].iloc[-1]
            sma_20 = historial['Close'].rolling(window=20).mean().iloc[-1]
            sma_50 = historial['Close'].rolling(window=50).mean().iloc[-1]
            
            if precio_actual > sma_20 and sma_20 > sma_50:
                tendencia = "🟢 Alcista Fuerte"
                recomendacion = "COMPRAR"
            elif precio_actual < sma_20 and sma_20 < sma_50:
                tendencia = "🔴 Bajista Fuerte"
                recomendacion = "VENDER"
            else:
                tendencia = "🟡 Lateral"
                recomendacion = "ESPERAR"
                
            resultados.append({
                'Empresa': nombre,
                'Precio ($/€)': round(precio_actual, 2),
                'SMA 20': round(sma_20, 2),
                'SMA 50': round(sma_50, 2),
                'Tendencia': tendencia,
                'Recomendación': recomendacion
            })

# Mostramos la tabla principal
if resultados:
    st.subheader("📊 Resumen de Mercados")
    tabla_resultados = pd.DataFrame(resultados)
    st.dataframe(tabla_resultados, use_container_width=True)
    
    # SECCIÓN DE GRÁFICOS
    st.divider() 
    st.subheader("📉 Gráfico de Cotización (Últimos 6 meses)")
    
    empresa_seleccionada = st.selectbox("Selecciona una empresa para analizar su gráfico:", list(empresas_mercado.keys()))
    
    datos_grafico = historicos[empresa_seleccionada][['Close']]
    st.line_chart(datos_grafico)