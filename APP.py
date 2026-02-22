import requests
import streamlit as st

st.set_page_config(page_title="ProBet AI", layout="wide")
st.title("🔥 ProBet AI - iSports Livescores")

# ==============================
# API KEY
# ==============================

API_KEY = st.secrets["API_KEY"]

# ==============================
# Obtener partidos en vivo
# ==============================

def obtener_livescores():
    url = f"http://api.isportsapi.com/sport/football/livescores?api_key={API_KEY}"
    
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            st.error("Error conectando a la API")
            st.write(r.text)
            return []
        
        data = r.json()
        return data.get("data", [])

    except Exception as e:
        st.error("Error de conexión")
        st.write(e)
        return []

# ==============================
# UI
# ==============================

partidos = obtener_livescores()

if not partidos:
    st.warning("No hay partidos activos.")
    st.stop()

opcion = st.selectbox(
    "Selecciona Partido",
    [f"{p['homeTeam']} vs {p['awayTeam']}" for p in partidos]
)

seleccion = next(
    p for p in partidos
    if f"{p['homeTeam']} vs {p['awayTeam']}" == opcion
)

st.subheader("🏟 Partido Seleccionado")
st.write("Local:", seleccion["homeTeam"])
st.write("Visitante:", seleccion["awayTeam"])
st.write("Marcador:", seleccion["homeScore"], "-", seleccion["awayScore"])
st.write("Minuto:", seleccion.get("matchTime", "N/A"))
