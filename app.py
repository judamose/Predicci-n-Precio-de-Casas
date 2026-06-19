import streamlit as st
import pandas as pd
import joblib

# ==========================
# Cargar modelo entrenado
# ==========================
modelo = joblib.load("modelo.pkl")

# ==========================
# Configuración de la página
# ==========================
st.set_page_config(
    page_title="Predicción Precio de Viviendas",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Predicción de Precio Medio de Viviendas")
st.markdown(
    "Ingrese las características de la vivienda y presione **Predecir**."
)

# ==========================
# Entradas del usuario
# ==========================

col1, col2 = st.columns(2)

with col1:

    longitud = st.slider(
        "Longitud",
        min_value=-125.0,
        max_value=-114.0,
        value=-119.0,
        step=0.01
    )

    latitud = st.slider(
        "Latitud",
        min_value=32.0,
        max_value=42.0,
        value=36.0,
        step=0.01
    )

    edad_mediana = st.number_input(
        "Edad Mediana Vivienda",
        min_value=1,
        max_value=60,
        value=25
    )

    total_habitaciones = st.number_input(
        "Total Habitaciones",
        min_value=1,
        value=2500
    )

with col2:

    total_bedrooms = st.number_input(
        "Total Dormitorios",
        min_value=1,
        value=500
    )

    poblacion = st.number_input(
        "Población",
        min_value=1,
        value=1500
    )

    hogares = st.number_input(
        "Hogares",
        min_value=1,
        value=450
    )

    ingreso_mediano = st.number_input(
        "Ingreso Mediano",
        min_value=0.0,
        value=4.5,
        step=0.1
    )

# Variable categórica
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

# ==========================
# Botón de predicción
# ==========================

if st.button("🔍 Predecir"):

    datos = pd.DataFrame({
        "Longitud": [longitud],
        "Latitud": [latitud],
        "Edad_mediana_vivienda": [edad_mediana],
        "Total_Habitaciones": [total_habitaciones],
        "total_bedrooms": [total_bedrooms],
        "Poblacion": [poblacion],
        "Hogares": [hogares],
        "Ingreso_Mediano": [ingreso_mediano],
        "Proximidad_Oceano": [proximidad_oceano]
    })

    # Predicción
    prediccion = modelo.predict(datos)[0]

    st.success(
        f"Precio medio estimado: ${prediccion:,.2f}"
    )

    st.subheader("Datos utilizados")
    st.dataframe(datos)
