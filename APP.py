import requests
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="ProBet AI", layout="wide")
st.title("⚽ Selección de Liga y Partidos")

API_KEY = st.secrets["API_KEY"]

# ==============================
# OBTENER LIGAS
# ==============================

url_ligas = f"http://api2.isportsapi.com/sport/football/league/basic?api_key={API_KEY}"
response = requests.get(url_ligas, timeout=10)

if response.status_code != 200:
    st.error("❌ Error obteniendo ligas")
    st.stop()

ligas = response.json().get("data", [])

# 🔥 Prioridad personalizada
prioridad = [
    "Premier League",
    "La Liga",
    "Bundesliga",
    "Serie A",
    "Ligue 1",
    "Liga MX",
    "UEFA Champions League"
]

ordenadas = []

for liga in ligas:
    if liga.get("name") in prioridad:
        ordenadas.append(liga)

for liga in ligas:
    if liga.get("name") not in prioridad:
        ordenadas.append(liga)

# Crear selectbox
dict_ligas = {
    f"{l['name']} ({l.get('shortName')})": l["leagueId"]
    for l in ordenadas if l.get("leagueId")
}

liga_seleccionada = st.selectbox("Selecciona Liga", list(dict_ligas.keys()))
league_id = dict_ligas[liga_seleccionada]

st.success(f"✅ Liga: {liga_seleccionada}")

# ==============================
# OBTENER PARTIDOS (USAMOS FIXTURES)
# ==============================

url_partidos = f"http://api2.isportsapi.com/sport/football/fixtures?api_key={API_KEY}&leagueId={league_id}"

resp_partidos = requests.get(url_partidos, timeout=10)

if resp_partidos.status_code != 200:
    st.error("❌ Error obteniendo partidos")
    st.stop()

partidos_data = resp_partidos.json().get("data", [])

partidos = []

for p in partidos_data:

    home = p.get("homeTeam")
    away = p.get("awayTeam")
    fecha = p.get("matchTime") or p.get("date")

    if home and away:
        partidos.append(f"{home} vs {away} | 🗓 {fecha}")

# ==============================
# MOSTRAR PARTIDOS
# ==============================

if partidos:
    partido = st.selectbox("Selecciona Partido", partidos)
    st.info(f"🎯 Partido seleccionado: {partido}")
else:
    st.warning("⚠️ No hay partidos para esta liga.")
