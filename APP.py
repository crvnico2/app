import requests
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="ProBet AI", layout="wide")
st.title("🔥 ProBet AI - Todos los Partidos Futuros")

API_KEY = st.secrets["API_KEY"]

# ==============================
# OBTENER TODOS LOS FIXTURES
# ==============================

url = (
    f"http://api2.isportsapi.com/sport/football/fixtures"
    f"?api_key={API_KEY}"
    f"&status=NS"
)

st.write("🔎 Consultando API...")

response = requests.get(url, timeout=15)

if response.status_code != 200:
    st.error("❌ Error en la API")
    st.write(response.text)
    st.stop()

data = response.json()
partidos = data.get("data", [])

if not partidos:
    st.warning("⚠️ No se encontraron partidos futuros.")
    st.stop()

st.success(f"✅ Se encontraron {len(partidos)} partidos")

# ==============================
# MOSTRAR PARTIDOS
# ==============================

for p in partidos:

    home = p.get("homeTeam")
    away = p.get("awayTeam")
    liga = p.get("leagueName")
    fecha = p.get("matchTime")

    if home and away:

        with st.expander(f"{home} vs {away} 🏆 {liga}"):

            st.write("📅 Fecha:", fecha)
            st.write("⚽ Local:", home)
            st.write("🔴 Visitante:", away)
            st.write("⏱ Estado:", p.get("status"))

            st.json(p)
