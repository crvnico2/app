import requests
import streamlit as st

st.set_page_config(page_title="ProBet AI - Elite Leagues", layout="wide")
st.title("🔥 ProBet AI - Partidos Elite")

API_KEY = st.secrets["API_KEY"]

# ==============================
# LIGAS QUE NOS INTERESAN
# ==============================

league_keywords = [
    "Premier",
    "Bundesliga",
    "Serie A",
    "Ligue 1",
    "La Liga",
    "Liga MX",
    "Champions",
    "Europa"
]

st.write("🔎 Buscando ligas importantes...")

# ==============================
# OBTENER TODAS LAS LIGAS
# ==============================

url_ligas = f"http://api2.isportsapi.com/sport/football/league/basic?api_key={API_KEY}"
resp = requests.get(url_ligas, timeout=10)

if resp.status_code != 200:
    st.error("❌ Error obteniendo ligas")
    st.stop()

ligas = resp.json().get("data", [])

# Filtrar solo ligas importantes
ligas_filtradas = []

for liga in ligas:
    nombre = liga.get("name", "")

    for palabra in league_keywords:
        if palabra.lower() in nombre.lower():
            ligas_filtradas.append(liga)
            break

if not ligas_filtradas:
    st.warning("⚠️ No se encontraron ligas importantes.")
    st.stop()

# ==============================
# BUSCAR PARTIDOS SOLO EN ESAS LIGAS
# ==============================

all_matches = []

for liga in ligas_filtradas:

    league_id = liga.get("leagueId")
    league_name = liga.get("name")

    url_partidos = (
        f"http://api2.isportsapi.com/sport/football/fixtures"
        f"?api_key={API_KEY}"
        f"&leagueId={league_id}"
        f"&status=NS"
    )

    try:
        r = requests.get(url_partidos, timeout=8)
        data = r.json().get("data", [])

        for match in data:
            match["leagueName"] = league_name
            all_matches.append(match)

    except:
        continue

# ==============================
# MOSTRAR RESULTADOS
# ==============================

if not all_matches:
    st.warning("⚠️ No hay partidos futuros en las ligas seleccionadas.")
    st.stop()

st.success(f"✅ Se encontraron {len(all_matches)} partidos futuros")

for p in all_matches:

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
