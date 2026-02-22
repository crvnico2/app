import requests
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="ProBet AI", layout="wide")

st.title("⚽ ProBet AI - Partidos Reales Automáticos")

# Leer API KEY desde Secrets
API_KEY = st.secrets["API_KEY"]

# Fecha de hoy automática
hoy = datetime.now().strftime("%Y-%m-%d")

# 🔥 ENDPOINT PARA FREE API LIVE FOOTBALL DATA
url = "https://free-api-live-football-data.p.rapidapi.com/football-current-matches"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

st.write("Status Code:", response.status_code)

if response.status_code != 200:
    st.error("Error en la API")
    st.write(response.text)
    st.stop()

data = response.json()

if "data" not in data or len(data["data"]) == 0:
    st.warning("No hay partidos disponibles ahora mismo.")
    st.stop()

st.subheader("📅 Partidos Actuales")

for match in data["data"]:
    home = match.get("home_name", "Equipo Local")
    away = match.get("away_name", "Equipo Visitante")
    league = match.get("league_name", "Liga")
    st.write(f"🏟 {home} vs {away}  |  🏆 {league}")

