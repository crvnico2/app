import requests
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="ProBet AI - Smart Matches", layout="wide")
st.title("🔥 ProBet AI - Partidos Futuros Inteligentes")

API_KEY = st.secrets["API_KEY"]

st.write("🔎 Buscando partidos...")

# ==============================
# TRAER TODOS LOS FIXTURES
# ==============================

url = f"http://api2.isportsapi.com/sport/football/fixtures?api_key={API_KEY}"

response = requests.get(url, timeout=20)

if response.status_code != 200:
    st.error("❌ Error en la API")
    st.write(response.text)
    st.stop()

partidos = response.json().get("data", [])

if not partidos:
    st.warning("⚠️ No se encontraron partidos.")
    st.stop()

# ==============================
# FILTRAR SOLO PARTIDOS FUTUROS
# ==============================

hoy = datetime.now()

partidos_futuros = []

for p in partidos:

    fecha_str = p.get("matchTime")

    if not fecha_str:
        continue

    try:
        fecha_partido = datetime.strptime(fecha_str[:10], "%Y-%m-%d")

        if fecha_partido >= hoy:
            partidos_futuros.append(p)

    except:
        continue

# ==============================
# FILTRAR SOLO LIGAS IMPORTANTES
# ==============================

liga_keywords = [
    "Premier",
    "Bundesliga",
    "Serie A",
    "Ligue 1",
    "La Liga",
    "Liga MX",
    "Champions",
    "Europa"
]

partidos_final = []

for p in partidos_futuros:

    liga = p.get("leagueName", "")

    for palabra in liga_keywords:
        if palabra.lower() in liga.lower():
            partidos_final.append(p)
            break

if not partidos_final:
    st.warning("⚠️ No hay partidos futuros en ligas importantes.")
    st.stop()

st.success(f"✅ Se encontraron {len(partidos_final)} partidos")

# ==============================
# MOSTRAR PARTIDOS
# ==============================

for p in partidos_final:

    home = p.get("homeTeam")
    away = p.get("awayTeam")
    liga = p.get("leagueName")
    fecha = p.get("matchTime")

    with st.expander(f"{home} vs {away} | {liga}"):

        st.write("📅 Fecha:", fecha)
        st.write("⚽ Local:", home)
        st.write("🔴 Visitante:", away)
        st.write("🏆 Liga:", liga)

        st.json(p)
