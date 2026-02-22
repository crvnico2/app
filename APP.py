import requests
import streamlit as st

st.set_page_config(page_title="ProBet AI - Ligas y Partidos", layout="wide")
st.title("⚽ Selección de Liga y Partidos en Vivo")

API_KEY = st.secrets["API_KEY"]

# ==============================
# 1️⃣ Obtener todas las ligas
# ==============================
url_ligas = f"http://api2.isportsapi.com/sport/football/league/basic?api_key={API_KEY}"
response = requests.get(url_ligas, timeout=10)
data = response.json()
ligas = data.get("data", [])

# Crear diccionario: nombre -> leagueId
dict_ligas = {liga.get("name"): liga.get("leagueId") for liga in ligas if liga.get("leagueId")}

# Selectbox de ligas
liga_seleccionada = st.selectbox("Selecciona Liga", list(dict_ligas.keys()))
league_id = dict_ligas[liga_seleccionada]

# ==============================
# 2️⃣ Obtener partidos de la liga
# ==============================
url_partidos = f"http://api2.isportsapi.com/sport/football/livescores?api_key={API_KEY}&leagueId={league_id}"

response_partidos = requests.get(url_partidos, timeout=10)
data_partidos = response_partidos.json()
partidos_data = data_partidos.get("data", [])

# Extraer partidos para selectbox
partidos = []
for p in partidos_data:
    home = p.get("homeTeam") or p.get("home_team")
    away = p.get("awayTeam") or p.get("away_team")
    match_id = p.get("matchId") or p.get("id")
    if home and away and match_id:
        partidos.append({"id": match_id, "label": f"{home} vs {away}", "raw": p})

# Selectbox de partidos
if partidos:
    partido_seleccionado = st.selectbox("Selecciona Partido", [p["label"] for p in partidos])
    seleccion = next(p for p in partidos if p["label"] == partido_seleccionado)
    info = seleccion["raw"]

    st.subheader("🏟 Partido Seleccionado")
    st.write("🔵 Local:", info.get("homeTeam") or info.get("home_team"))
    st.write("🔴 Visitante:", info.get("awayTeam") or info.get("away_team"))
    st.write("⚽ Marcador:", info.get("homeScore") or info.get("home_score"), "-", info.get("awayScore") or info.get("away_score"))
    st.write("⏱ Minuto:", info.get("matchTime") or info.get("minute"))
else:
    st.warning("⚠️ No hay partidos en esta liga actualmente.")
