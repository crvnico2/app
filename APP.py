import requests
import streamlit as st
from datetime import datetime

# ==============================
# CONFIGURACIÓN
# ==============================

st.set_page_config(page_title="ProBet AI", layout="wide")
st.title("⚽ ProBet AI - Ligas y Partidos")

API_KEY = st.secrets["API_KEY"]

# ==============================
# OBTENER LIGAS
# ==============================

url_ligas = f"http://api2.isportsapi.com/sport/football/league/basic?api_key={API_KEY}"

response_ligas = requests.get(url_ligas, timeout=10)

if response_ligas.status_code != 200:
    st.error("❌ Error obteniendo ligas")
    st.stop()

ligas = response_ligas.json().get("data", [])

# ==============================
# PRIORIDAD INTELIGENTE
# ==============================

prioridad = [
    "Premier",
    "La Liga",
    "Bundesliga",
    "Serie A",
    "Ligue 1",
    "Liga MX",
    "Champions"
]

ordenadas = []

# Primero ligas que coincidan con prioridad
for palabra in prioridad:
    for liga in ligas:
        nombre = liga.get("name", "")
        if palabra.lower() in nombre.lower():
            if liga not in ordenadas:
                ordenadas.append(liga)

# Luego agregar las demás
for liga in ligas:
    if liga not in ordenadas:
        ordenadas.append(liga)

# ==============================
# SELECTBOX LIGAS
# ==============================

dict_ligas = {
    f"{l['name']} ({l.get('shortName')})": l["leagueId"]
    for l in ordenadas if l.get("leagueId")
}

liga_seleccionada = st.selectbox("Selecciona Liga", list(dict_ligas.keys()))
league_id = dict_ligas[liga_seleccionada]

st.success(f"✅ Liga seleccionada: {liga_seleccionada}")

# ==============================
# OBTENER PARTIDOS (FIXTURES + FECHA)
# ==============================

today = datetime.now().strftime("%Y-%m-%d")

url_partidos = (
    f"http://api2.isportsapi.com/sport/football/fixtures"
    f"?api_key={API_KEY}"
    f"&leagueId={league_id}"
    f"&date={today}"
)

response_partidos = requests.get(url_partidos, timeout=10)

if response_partidos.status_code != 200:
    st.error("❌ Error obteniendo partidos")
    st.write(response_partidos.text)
    st.stop()

partidos_data = response_partidos.json().get("data", [])

partidos = []

for p in partidos_data:
    home = p.get("homeTeam")
    away = p.get("awayTeam")
    time = p.get("matchTime")

    if home and away:
        partidos.append({
            "label": f"{home} vs {away} 🕒 {time}",
            "raw": p
        })

# ==============================
# MOSTRAR PARTIDOS
# ==============================

if partidos:

    seleccion = st.selectbox(
        "Selecciona Partido",
        [p["label"] for p in partidos]
    )

    partido_data = next(p for p in partidos if p["label"] == seleccion)["raw"]

    st.subheader("🏟 Información Partido")

    st.write("🔵 Local:", partido_data.get("homeTeam"))
    st.write("🔴 Visitante:", partido_data.get("awayTeam"))
    st.write("⚽ Marcador:",
             partido_data.get("homeScore"),
             "-",
             partido_data.get("awayScore"))
    st.write("⏱ Estado:", partido_data.get("status"))
    st.write("🕒 Hora:", partido_data.get("matchTime"))

else:
    st.warning("⚠️ No hay partidos disponibles para esta liga y fecha.")
