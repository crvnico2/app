import requests
import streamlit as st

st.set_page_config(page_title="ProBet AI - Elite Matches", layout="wide")
st.title("🔥 ProBet AI - Partidos Futuros Elite")

API_KEY = st.secrets["API_KEY"]

# ==============================
# OBTENER TODOS LOS PARTIDOS FUTUROS
# ==============================

st.write("🔎 Buscando partidos futuros...")

url = (
    f"http://api2.isportsapi.com/sport/football/fixtures"
    f"?api_key={API_KEY}"
    f"&status=NS"
)

response = requests.get(url, timeout=15)

if response.status_code != 200:
    st.error("❌ Error obteniendo partidos")
    st.write(response.text)
    st.stop()

partidos = response.json().get("data", [])

if not partidos:
    st.warning("⚠️ No hay partidos futuros disponibles.")
    st.stop()

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

partidos_filtrados = []

for p in partidos:

    liga = p.get("leagueName", "")

    for palabra in liga_keywords:
        if palabra.lower() in liga.lower():
            partidos_filtrados.append(p)
            break

if not partidos_filtrados:
    st.warning("⚠️ No hay partidos en ligas importantes.")
    st.stop()

st.success(f"✅ Se encontraron {len(partidos_filtrados)} partidos")

# ==============================
# MOSTRAR PARTIDOS
# ==============================

for p in partidos_filtrados:

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
