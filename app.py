import streamlit as st
import pandas as pd
import requests

# =====================================================
# CONFIGURACIÓN DE LA PÁGINA
# =====================================================

st.set_page_config(
    page_title="Predicción Precio de Viviendas",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Predicción de Precio de Viviendas")

# =====================================================
# VERIFICAR TOKEN
# =====================================================

try:
    API_TOKEN = st.secrets["DATAROBOT_API_KEY"]
    st.success("Conexión con secretos OK")
except Exception as e:
    st.error("No se encontró DATAROBOT_API_TOKEN en Secrets")
    st.stop()

# =====================================================
# URL DEL DEPLOYMENT
# =====================================================

API_TOKEN = st.secrets["DATAROBOT_API_KEY"]
DEPLOYMENT_ID = st.secrets["DATAROBOT_DEPLOYMENT_ID"]
HOST = st.secrets["DATAROBOT_HOST"]

API_URL = (
    f"{HOST}/predApi/v1.0/deployments/"
    f"{DEPLOYMENT_ID}/predictions"
)

st.write("URL utilizada:")
st.code(API_URL)

# =====================================================
# FORMULARIO
# =====================================================

col1, col2 = st.columns(2)

with col1:

    longitud = st.number_input(
        "Longitud",
        value=-122.23,
        format="%.4f"
    )

    latitud = st.number_input(
        "Latitud",
        value=37.88,
        format="%.4f"
    )

    edad_mediana = st.number_input(
        "Edad Mediana Vivienda",
        min_value=1,
        value=20
    )

    total_habitaciones = st.number_input(
        "Total Habitaciones",
        min_value=1,
        value=1500
    )

with col2:

    total_bedrooms = st.number_input(
        "Total Dormitorios",
        min_value=1,
        value=300
    )

    poblacion = st.number_input(
        "Población",
        min_value=1,
        value=1000
    )

    hogares = st.number_input(
        "Hogares",
        min_value=1,
        value=350
    )

    ingreso_mediano = st.number_input(
        "Ingreso Mediano",
        min_value=0.0,
        value=5.0
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

# =====================================================
# BOTÓN
# =====================================================

if st.button("🔍 Predecir"):

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

    st.write("Datos enviados:")
    st.json(datos)

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    try:

        with st.spinner("Consultando DataRobot..."):

            response = requests.post(
                API_URL,
                headers=headers,
                json=datos,
                timeout=30
            )

        st.write("Código HTTP:", response.status_code)

        if response.status_code == 200:

            resultado = response.json()

            st.success("Predicción obtenida")

            st.subheader("Resultado")

            st.json(resultado)

        else:

            st.error(
                f"Error HTTP {response.status_code}"
            )

            st.code(response.text)

    except requests.exceptions.Timeout:

        st.error(
            "Tiempo de espera agotado. "
            "Verifica la URL del Deployment."
        )

    except Exception as e:

        st.error("Error inesperado")

        st.exception(e)