import requests
import streamlit as st

st.set_page_config(page_title="ProBet AI", layout="wide")
st.title("⚽ ProBet AI - Datos Públicos")

# Fuente pública más estable
url = "https://site.api.espn.com/apis/site/v2/sports/soccer/mex.1/scoreboard"

response = requests.get(url)

if response.status_code != 200:
    st.error("Error conectando a la fuente")
    st.write(response.text)
    st.stop()

data = response.json()

events = data.get("events", [])

if not events:
    st.warning("No hay partidos disponibles.")
    st.stop()

st.subheader("📅 Liga MX Partidos")

for event in events:
    competitions = event.get("competitions", [])
    if not competitions:
        continue

    comp = competitions[0]
    competitors = comp.get("competitors", [])

    if len(competitors) == 2:
        home = competitors[0]["team"]["displayName"]
        away = competitors[1]["team"]["displayName"]

        score_home = competitors[0].get("score", "0")
        score_away = competitors[1].get("score", "0")

        st.write(f"🏟 {home} {score_home} - {score_away} {away}")


