import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="ProBet AI", layout="wide")

st.title("📊 ProBet AI - Partidos Reales Automáticos")

# --- CONFIG API ---
API_KEY = st.secrets["API_KEY"]  # La pondremos en Streamlit Cloud
headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

# --- BANCA ---
st.sidebar.header("💰 Gestión de Banca")
banca = st.sidebar.number_input("Banca actual", value=10000)
kelly_factor = st.sidebar.slider("Kelly conservador", 0.1, 1.0, 0.25)

# --- LIGAS IDs ---
ligas = {
    "Liga MX": 262,
    "Premier League": 39,
    "La Liga": 140,
    "Champions League": 2
}

liga_nombre = st.selectbox("Selecciona Liga", list(ligas.keys()))
liga_id = ligas[liga_nombre]

# --- TRAER PARTIDOS HOY ---
fecha_hoy = datetime.today().strftime('%Y-%m-%d')

url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?league={liga_id}&season=2024&date={fecha_hoy}"

response = requests.get(url, headers=headers)
data = response.json()

partidos = []

for match in data["response"]:
    local = match["teams"]["home"]["name"]
    visitante = match["teams"]["away"]["name"]
    partidos.append((local, visitante))

if len(partidos) == 0:
    st.warning("No hay partidos hoy en esta liga.")
else:
    partido_seleccionado = st.selectbox("Selecciona Partido", partidos)
    local, visitante = partido_seleccionado

    st.write(f"### {local} vs {visitante}")

    # Simulación promedio goles (luego podemos traer reales)
    prom_local = 1.5
    prom_visit = 1.2
    cuota = 2.0

    def prob_over25(l, v):
        prob = 0
        for i in range(6):
            for j in range(6):
                if i + j >= 3:
                    prob += (np.exp(-l) * l**i / np.math.factorial(i)) * \
                            (np.exp(-v) * v**j / np.math.factorial(j))
        return prob

    if st.button("🔥 Generar Pick"):
        prob_modelo = prob_over25(prom_local, prom_visit)
        prob_implicita = 1 / cuota
        value = prob_modelo - prob_implicita

        kelly = ((cuota - 1) * prob_modelo - (1 - prob_modelo)) / (cuota - 1)
        stake = banca * kelly * kelly_factor

        col1, col2, col3 = st.columns(3)
        col1.metric("Probabilidad Modelo", round(prob_modelo,2))
        col2.metric("Value", round(value,2))
        col3.metric("Stake Recomendado", round(stake,2))