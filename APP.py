import requests
import streamlit as st

st.set_page_config(page_title="ProBet AI", layout="wide")
st.title("🔥 ProBet AI - Selección Real de Partidos")

API_KEY = st.secrets["API_KEY"]

# ==============================
# OBTENER PARTIDOS DESDE BLOQUES
# ==============================

def obtener_partidos():

    url = f"http://api.isportsapi.com/sport/football/livescores?api_key={API_KEY}"

    r = requests.get(url, timeout=10)

    if r.status_code != 200:
        st.error("Error conectando API")
        return []

    data = r.json()

    bloques = data.get("data", [])

    partidos = []

    # 🔥 Recorrer cada bloque
    for bloque in bloques:

        # Cada bloque puede contener partidos
        for partido in bloque.get("list", []):

            home = partido.get("homeTeam") or partido.get("home_team")
            away = partido.get("awayTeam") or partido.get("away_team")

            partido_id = partido.get("matchId") or partido.get("id")

            if home and away and partido_id:

                partidos.append({
                    "id": partido_id,
                    "label": f"{home} vs {away}",
                    "data": partido
                })

    return partidos


# ==============================
# CARGAR PARTIDOS
# ==============================

partidos = obtener_partidos()

if not partidos:
    st.warning("No se encontraron partidos.")
    st.stop()

opcion = st.selectbox(
    "Selecciona Partido",
    [p["label"] for p in partidos]
)

seleccion = next(p for p in partidos if p["label"] == opcion)

st.subheader("🏟 Partido Seleccionado")

info = seleccion["data"]

st.write("Local:", info.get("homeTeam"))
st.write("Visitante:", info.get("awayTeam"))
st.write("Marcador:", info.get("homeScore"), "-", info.get("awayScore"))
st.write("Minuto:", info.get("matchTime"))

st.success("✅ Partido cargado correctamente")

