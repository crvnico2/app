headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

if response.status_code != 200:
    st.error("Error obteniendo datos")
    st.write(response.text)
    st.stop()

data = response.json()

events = data.get("events", [])

if not events:
    st.warning("No hay partidos en vivo actualmente.")
    st.stop()

st.subheader("📅 Partidos en Vivo")

for match in events:
    home = match["homeTeam"]["name"]
    away = match["awayTeam"]["name"]
    score_home = match.get("homeScore", {}).get("current", 0)
    score_away = match.get("awayScore", {}).get("current", 0)

    st.write(f"🏟 {home} {score_home} - {score_away} {away}")
