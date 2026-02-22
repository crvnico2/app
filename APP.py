import requests
import streamlit as st
from datetime import datetime

# ==============================
# CONFIG
# ==============================

st.set_page_config(page_title="ProBet AI - Partidos Futuros", layout="wide")
st.title("🔥 ProBet AI - Partidos Futuros (Para Apuestas)")

API_KEY = st.secrets["API_KEY"]

# ==============================
# FECHA ACTUAL
# ==============================

today = datetime.now().strftime("%Y-%m-%d")

# ==============================
# OBTENER PARTIDOS FUTUROS
# ==============================

url = (
    f"http://api2.isportsapi.com/sport/football/fixtures"
    f"?api_key={API_KEY}"
    f"&date={today}"
)

st.write("🔗 Consultando partidos futuros...")

response = requests.get(url, timeout=15)

if response.status_code != 200:
    st.error("❌ Error obteniendo partidos")
    st.write(response.text)
    st.stop()

data = response.json()
partidos = data.get("data", [])

if not partidos:
    st.warning("⚠️ No hay partidos futuros disponibles.")
    st.stop()

# ==============================
# MOSTRAR PARTIDOS
# ==============================

st.subheader("⚽ Partidos Futuros Disponibles")

for p in partidos:

    home = p.get("homeTeam")
    away = p.get("awayTeam")
    liga = p.get("leagueName")
    fecha = p.get("matchTime")

    if home and away:

        with st.expander(f"{home} vs {away} 🕒 {fecha}"):

            st.write("🏆 Liga:", liga)
            st.write("📅 Fecha:", fecha)
            st.write("⚽ Local:", home)
            st.write("🔴 Visitante:", away)

            st.write("📊 Datos Crudos:")
            st.json(p)
