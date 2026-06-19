import streamlit as st
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
# LEER SECRETOS
# =====================================================

try:
    API_TOKEN = st.secrets["DATAROBOT_API_KEY"]
    DEPLOYMENT_ID = st.secrets["DATAROBOT_DEPLOYMENT_ID"]
    HOST = st.secrets["DATAROBOT_HOST"]

    st.success("Conexión con Secrets OK")

except Exception as e:
    st.error(f"Error leyendo Secrets: {e}")
    st.stop()

# =====================================================
# URL DEL DEPLOYMENT
# =====================================================

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
# BOTÓN DE PREDICCIÓN
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

    st.subheader("Datos enviados")
    st.json(datos)

    headers = {
            "Authorization": f"Bearer {API_KEY}",
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

        st.subheader("Diagnóstico")

        st.write("Status Code:")
        st.write(response.status_code)

        st.write("Headers enviados:")
        st.json(headers)

        st.write("Respuesta completa:")
        st.text(response.text)

        if response.status_code == 200:

            resultado = response.json()

            st.success("Predicción obtenida correctamente")

            st.subheader("Resultado")

            st.json(resultado)

        else:

            st.error(
                f"DataRobot respondió con HTTP {response.status_code}"
            )

    except requests.exceptions.Timeout:

        st.error(
            "Timeout al conectar con DataRobot."
        )

    except Exception as e:

        st.error("Error inesperado")

        st.exception(e)