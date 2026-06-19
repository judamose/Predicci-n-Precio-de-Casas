import streamlit as st
import pandas as pd
import requests
import json

# =====================================
# CONFIGURACIÓN DATAROBOT
# =====================================

API_URL = "PEGA_AQUI_TU_PREDICTION_URL"

API_TOKEN = st.secrets["DATAROBOT_API_TOKEN"]

# =====================================
# INTERFAZ
# =====================================

st.title("🏠 Predicción de Precio de Viviendas")

col1, col2 = st.columns(2)

with col1:
    longitud = st.number_input("Longitud", value=-122.23)
    latitud = st.number_input("Latitud", value=37.88)
    edad_mediana = st.number_input("Edad Mediana Vivienda", value=20)

    total_habitaciones = st.number_input(
        "Total Habitaciones",
        value=1000
    )

with col2:
    total_bedrooms = st.number_input(
        "Total Dormitorios",
        value=200
    )

    poblacion = st.number_input(
        "Población",
        value=800
    )

    hogares = st.number_input(
        "Hogares",
        value=300
    )

    ingreso_mediano = st.number_input(
        "Ingreso Mediano",
        value=4.5
    )

proximidad_oceano = st.selectbox(
    "Proximidad al Océano",
    [
        "<1H OCEAN",
        "INLAND",
        "ISLAND",
        "NEAR BAY",
        "NEAR OCEAN"
    ]
)

# =====================================
# PREDICCIÓN
# =====================================

if st.button("Predecir"):

    datos = [{
        "Longitud": longitud,
        "Latitud": latitud,
        "Edad_mediana_vivienda": edad_mediana,
        "Total_Habitaciones": total_habitaciones,
        "total_bedrooms": total_bedrooms,
        "Poblacion": poblacion,
        "Hogares": hogares,
        "Ingreso_Mediano": ingreso_mediano,
        "Proximidad_Oceano": proximidad_oceano
    }]

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        API_URL,
        headers=headers,
        data=json.dumps(datos)
    )

    if response.status_code == 200:

        resultado = response.json()

        st.success("Predicción realizada")

        st.json(resultado)

    else:

        st.error(
            f"Error {response.status_code}"
        )

        st.write(response.text)