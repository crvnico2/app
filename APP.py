import requests
import streamlit as st

st.set_page_config(page_title="ProBet AI - Ligas", layout="wide")
st.title("⚽ Selección Inteligente de Ligas")

API_KEY = st.secrets["API_KEY"]

# ==============================
# Obtener Ligas
# ==============================

url_ligas = f"http://api2.isportsapi.com/sport/football/league/basic?api_key={API_KEY}"
response = requests.get(url_ligas, timeout=10)

if response.status_code != 200:
    st.error("❌ Error obteniendo ligas")
    st.stop()

data = response.json()
ligas = data.get("data", [])

# ==============================
# 🔥 FILTRAR SOLO LAS QUE NOS INTERESAN
# ==============================

ligas_importantes = [
    "Liga MX",
    "La Liga",
    "Premier League",
    "Bundesliga",
    "Serie A",
    "Ligue 1",
    "UEFA Champions League"
]

# Crear lista priorizada
lista_priorizada = []

# Primero agregamos las importantes si existen
for liga in ligas:
    nombre = liga.get("name")
    if nombre in ligas_importantes:
        lista_priorizada.append(liga)

# Luego agregamos las demás ligas que NO están en la lista importante
for liga in ligas:
    nombre = liga.get("name")
    if nombre not in ligas_importantes:
        lista_priorizada.append(liga)

# ==============================
# Crear SelectBox
# ==============================

dict_ligas = {
    f"{liga.get('name')} ({liga.get('shortName')})": liga.get("leagueId")
    for liga in lista_priorizada
    if liga.get("leagueId")
}

liga_seleccionada = st.selectbox(
    "Selecciona Liga",
    list(dict_ligas.keys())
)

league_id = dict_ligas[liga_seleccionada]

st.success(f"✅ Liga seleccionada: {liga_seleccionada}")
st.write("League ID:", league_id)
