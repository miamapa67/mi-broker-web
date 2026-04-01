try:
    df_precios = cargar_datos()
    
    # CALCULAMOS EL RSI PARA CADA ACCIÓN
    resumen = []
    
    for ticker in ibex_35:
        if ticker in df_precios.columns:
            precios = df_precios[ticker].dropna()
            if len(precios) > 14:
                # Lógica simplificada de RSI
                delta = precios.diff()
                ganancia = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                perdida = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = ganancia / perdida
                rsi = 100 - (100 / (1 + rs))
                
                ultimo_precio = precios.iloc[-1]
                ultimo_rsi = rsi.iloc[-1]
                
                # Decidir estado
                estado = "⚪ NEUTRO"
                if ultimo_rsi < 35: estado = "🟢 COMPRA"
                elif ultimo_rsi > 65: estado = "🔴 RIESGO"
                
                resumen.append({
                    "Ticker": ticker,
                    "Precio": f"{ultimo_precio:.2f}€",
                    "RSI": round(ultimo_rsi, 2),
                    "Estado": estado
                })

    # Mostrar como una tabla bonita
    df_final = pd.DataFrame(resumen)
    st.subheader("💡 Análisis de Oportunidades")
    st.table(df_final) # st.table se ve más limpio para señales

except Exception as e:
    st.error(f"Error en el análisis: {e}")
