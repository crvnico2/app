import requests
import streamlit as st

st.set_page_config(page_title="League Test", layout="wide")
st.title("⚽ Test con Liga Fijada")

API_KEY = st.secrets["API_KEY"]

# 🔥 Cambia esto si necesitas otro ID de liga
LEAGUE_NAME = "Premier League"

url = f"http://api2.isportsapi.com/sport/football/livescores?api_key={API_KEY}&leagueName={LEAGUE_NAME}"

st.write("🔗 URL usada:")
st.code(url)

response = requests.get(url, timeout=10)

if response.status_code != 200:
    st.error("❌ Error API")
    st.write(response.text)
    st.stop()

data = response.json()

st.subheader("📦 JSON Devuelto")
st.json(data)

partidos = []

if "data" in data:
    for item in data["data"]:

        home = item.get("homeTeam") or item.get("home_team")
        away = item.get("awayTeam") or item.get("away_team")

        if home and away:
            partidos.append(f"{home} vs {away}")

st.subheader("⚽ Partidos Encontrados")

if partidos:
    for p in partidos:
        st.write("✅", p)
else:
    st.warning("⚠️ No se encontraron partidos para esa liga.")

