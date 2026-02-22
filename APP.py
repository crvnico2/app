import requests
import streamlit as st

st.set_page_config(page_title="ProBet AI", layout="wide")
st.title("🔥 ProBet AI - Partidos Futuros Automáticos")

API_KEY = st.secrets["API_KEY"]

# ==============================
# OBTENER TODAS LAS LIGAS
# ==============================

url_ligas = f"http://api2.isportsapi.com/sport/football/league/basic?api_key={API_KEY}"

resp_ligas = requests.get(url_ligas, timeout=10)

if resp_ligas.status_code != 200:
    st.error("❌ Error obteniendo ligas")
    st.stop()

ligas = resp_ligas.json().get("data", [])

if not ligas:
    st.warning("⚠️ No se encontraron ligas")
    st.stop()

# ==============================
# BUSCAR PARTIDOS EN CADA LIGA
# ==============================

all_matches = []

for liga in ligas:

    league_id = liga.get("leagueId")
    league_name = liga.get("name")

    if not league_id:
        continue

    url_partidos = (
        f"http://api2.isportsapi.com/sport/football/fixtures"
        f"?api_key={API_KEY}"
        f"&leagueId={league_id}"
        f"&status=NS"
    )

    try:
        r = requests.get(url_partidos, timeout=5)
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
    st.warning("⚠️ No se encontraron partidos futuros.")
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
