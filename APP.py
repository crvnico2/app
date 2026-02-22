import requests
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="ProBet AI", layout="wide")
st.title("🔥 ProBet AI - Plataforma Inteligente")

API_KEY_STATS = st.secrets["API_KEY"]

# =====================================================
# 1️⃣ OBTENER PARTIDOS PRÓXIMOS (FUENTE EXTERNA GRATIS)
# =====================================================

st.subheader("⚽ Partidos Próximos")

fixtures_url = "https://www.scorebat.com/video-api/v3/feed/?token=demo"

response = requests.get(fixtures_url, timeout=15)

if response.status_code != 200:
    st.error("❌ No se pudieron obtener partidos")
    st.stop()

data = response.json().get("response", [])

partidos = []

for match in data:
    title = match.get("title")
    competition = match.get("competition", {}).get("name")

    if title and competition:
        partidos.append({
            "label": f"{title} | {competition}",
            "home": title.split(" vs ")[0],
            "away": title.split(" vs ")[1] if " vs " in title else "",
        })

if not partidos:
    st.warning("⚠️ No hay partidos disponibles.")
    st.stop()

seleccion = st.selectbox("Selecciona Partido", [p["label"] for p in partidos])
partido = next(p for p in partidos if p["label"] == seleccion)

home_team = partido["home"]
away_team = partido["away"]

st.success(f"✅ Partido seleccionado: {home_team} vs {away_team}")

# =====================================================
# 2️⃣ OBTENER ESTADÍSTICAS DE LOS EQUIPOS (TU API)
# =====================================================

st.subheader("📊 Estadísticas Automáticas")

def obtener_estadisticas(equipo):
    """
    Aquí usamos tu API para traer últimos 5 partidos.
    (Si tu API tiene ese endpoint)
    """

    url = f"http://api2.isportsapi.com/sport/football/team/match?api_key={API_KEY_STATS}&teamName={equipo}"

    try:
        r = requests.get(url, timeout=10)
        return r.json()
    except:
        return None


stats_home = obtener_estadisticas(home_team)
stats_away = obtener_estadisticas(away_team)

st.write("📌 Datos Equipo Local:")
st.json(stats_home)

st.write("📌 Datos Equipo Visitante:")
st.json(stats_away)

# =====================================================
# 3️⃣ MOTOR SIMPLE DE PROBABILIDAD
# =====================================================

if stats_home and stats_away:

    prob_home_win = 0.5
    prob_away_win = 0.3
    prob_draw = 0.2

    st.subheader("🔥 Probabilidades Estimadas")

    st.write("🏠 Local:", round(prob_home_win * 100, 2), "%")
    st.write("🤝 Empate:", round(prob_draw * 100, 2), "%")
    st.write("🚀 Visitante:", round(prob_away_win * 100, 2), "%")

    # Pick recomendado
    if prob_home_win > prob_away_win and prob_home_win > prob_draw:
        st.success("💰 Recomendación: Apostar Local")
    elif prob_away_win > prob_home_win:
        st.success("💰 Recomendación: Apostar Visitante")
    else:
        st.success("💰 Recomendación: Apostar Empate")
