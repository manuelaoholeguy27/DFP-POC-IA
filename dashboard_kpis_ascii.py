# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Comparativo de KPIs", layout="wide")

st.title("Dashboard Comparativo de KPIs por Circuito")
st.write("Visualizacion automatica de KPIs enriquecidos y top 10 circuitos con mayor ahorro extra.")

uploaded_file = st.file_uploader("Subi la planilla enriquecida final", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Convertir columnas numericas con comas a float
    cols_to_clean = ["NEW_CUMULATED_SAVING", "CUMULATED_DISTANCE", "LDT", "OCIOSIDADE", "EXTRA_SAVING"]
    for col in cols_to_clean:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(",", ".").astype(float)

    st.subheader("Resumen de KPIs (deltas totales)")
    col1, col2, col3 = st.columns(3)
    col1.metric("Extra Saving Total", f"${df['EXTRA_SAVING'].sum():,.0f}")
    col2.metric("Extra Drivers", int(df['EXTRA_NUMBER_OF_DRIVERS'].sum()))
    col3.metric("Extra Vehicles", int(df['EXTRA_NUMBER_OF_VEHICLES'].sum()))

    st.markdown("---")

    st.subheader("Top 10 circuitos con mayor Extra Saving")
    top10 = df.sort_values(by="EXTRA_SAVING", ascending=False).head(10)

    st.dataframe(top10[[
        "ASSOCIATED_CURRENT_CIRCUIT", "MLP", "EXTRA_SAVING", "LDT", "OCIOSIDADE",
        "EXTRA_NUMBER_OF_DRIVERS", "EXTRA_NUMBER_OF_VEHICLES"
    ]].rename(columns={
        "ASSOCIATED_CURRENT_CIRCUIT": "Circuito",
        "MLP": "Transportadora",
        "EXTRA_SAVING": "Ahorro Extra",
        "LDT": "LDT (%)",
        "OCIOSIDADE": "Ociosidad (%)",
        "EXTRA_NUMBER_OF_DRIVERS": "Extra Choferes",
        "EXTRA_NUMBER_OF_VEHICLES": "Extra Vehiculos"
    }), use_container_width=True)

else:
    st.info("Subi una planilla Excel para comenzar.")
