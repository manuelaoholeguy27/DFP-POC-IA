# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard de Enrichment", layout="wide")

st.title("📊 Dashboard de Enrichment sobre Circuitos")
st.write("Análisis de KPIs generados al comparar un escenario baseline con uno enriquecido.")

uploaded_file = st.file_uploader("📁 Subí la planilla enriquecida", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Limpieza de columnas numéricas
    cols_to_clean = [
        "EXTRA_SAVING", "EXTRA_NUMBER_OF_VEHICLES", "EXTRA_NUMBER_OF_DRIVERS",
        "EXTRA_DISTANCE", "OCIOSIDADE", "LDT"
    ]
    for col in cols_to_clean:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(",", ".").astype(float)

    # Filtros por circuito y OBS
    st.sidebar.header("🎛️ Filtros")
    circuit_filter = st.sidebar.multiselect(
        "Filtrar por Circuito:", options=df["ASSOCIATED_CURRENT_CIRCUIT"].unique()
    )
    obs_filter = st.sidebar.multiselect(
        "Filtrar por OBS:", options=df["OBS"].dropna().unique()
    )

    df_filtered = df.copy()
    if circuit_filter:
        df_filtered = df_filtered[df_filtered["ASSOCIATED_CURRENT_CIRCUIT"].isin(circuit_filter)]
    if obs_filter:
        df_filtered = df_filtered[df_filtered["OBS"].isin(obs_filter)]

    # Sesión 1: Big Numbers
    st.subheader("📌 KPIs Agregados")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Extra Saving Total", f"${df_filtered['EXTRA_SAVING'].sum():,.0f}")
    col2.metric("Extra Cant. de Viajes", int(df_filtered['OVERALL_TRAVELS_NUMBER'].sum()))
    col3.metric("Extra Vehículos", int(df_filtered['EXTRA_NUMBER_OF_VEHICLES'].sum()))
    col4.metric("Extra Drivers", int(df_filtered['EXTRA_NUMBER_OF_DRIVERS'].sum()))

    # Sesión 2: Cluster OBS
    st.markdown("---")
    st.subheader("🔍 Cantidad de circuitos por tipo de OBS")
    obs_counts = df_filtered["OBS"].fillna("Sin OBS").value_counts()
    st.bar_chart(obs_counts)

    # Sesión 3: Top 10 por Extra Saving
    st.markdown("---")
    st.subheader("🏁 Top 10 Circuitos con mayor Extra Saving")
    top10 = df_filtered.sort_values(by="EXTRA_SAVING", ascending=False).head(10)
    st.bar_chart(top10.set_index("ASSOCIATED_CURRENT_CIRCUIT")["EXTRA_SAVING"])

    # Sesión 4: Tabla detallada
    st.markdown("---")
    st.subheader("📋 Detalle por Circuito (KPIs seleccionados)")
    cols_to_show = [
        "OBS", "MLP", "BASELINE_CUMULATED_SAVING", "NEW_CUMULATED_SAVING", "EXTRA_SAVING",
        "EXTRA_NUMBER_OF_VEHICLES", "EXTRA_DISTANCE", "LDT", "OCIOSIDADE",
        "BASELINE_NUMBER_OF_DRIVERS", "NEW_NUMBER_OF_DRIVERS", "EXTRA_NUMBER_OF_DRIVERS",
        "BASELINE_NUMBER_OF_FACILITIES", "NUMBER_OF_FACILITIES", "EXTRA_NUMBER_OF_FACILITIES",
        "BASELINE_NUMBER_OF_STATES", "NUMBER_OF_STATES", "EXTRA_NUMBER_OF_STATES"
    ]

    table = df_filtered.sort_values(by="EXTRA_SAVING", ascending=False)
    st.dataframe(table[cols_to_show], use_container_width=True)

else:
    st.info("Subí una planilla Excel para comenzar.")
