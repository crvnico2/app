import requests
import streamlit as st

st.set_page_config(page_title="ProBet AI", layout="wide")
st.title("🔥 ProBet AI - Partidos Futuros Estables")

API_KEY = st.secrets["API_KEY"]

# =====================================================
# OBTENER PARTIDOS DESDE FUENTE MÁS ESTABLE
# =====================================================

st.subheader("⚽ Cargando partidos futuros...")

# Endpoint público alternativo (sin token complicado)
url = "https://api-football-v1.p.rapidapi.com/v3/fixtures?next=50"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

try:
    response = requests.get(url, headers=headers, timeout=15)

    if response.status_code != 200:
        st.error("❌ Error obteniendo partidos")
        st.write(response.text)
        st.stop()

    data = response.json()
    partidos = data.get("response", [])

except Exception as e:
    st.error("❌ Error de conexión")
    st.write(str(e))
    st.stop()

if not partidos:
    st.warning("⚠️ No hay partidos futuros disponibles.")
    st.stop()

st.success(f"✅ Se encontraron {len(partidos)} partidos")

# =====================================================
# MOSTRAR PARTIDOS
# =====================================================

for p in partidos:

    fixture = p.get("fixture", {})
    teams = p.get("teams", {})
    league = p.get("league", {})

    home = teams.get("home", {}).get("name")
    away = teams.get("away", {}).get("name")
    liga = league.get("name")
    fecha = fixture.get("date")

    if home and away:

        with st.expander(f"{home} vs {away} | {liga}"):

            st.write("📅 Fecha:", fecha)
            st.write("🏆 Liga:", liga)
            st.write("⚽ Local:", home)
            st.write("🔴 Visitante:", away)

            st.json(p)
