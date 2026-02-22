import requests
import streamlit as st
import random

st.set_page_config(page_title="ProBet AI", layout="wide")
st.title("⚽ ProBet AI - Picks y Parlays")

# =======================
# OBTENER PARTIDOS
# =======================

url = "https://site.api.espn.com/apis/site/v2/sports/soccer/mex.1/scoreboard"

response = requests.get(url)

if response.status_code != 200:
    st.error("Error obteniendo partidos")
    st.stop()

data = response.json()
events = data.get("events", [])

if not events:
    st.warning("No hay partidos disponibles.")
    st.stop()

partidos = []

for event in events:
    comp = event["competitions"][0]
    teams = comp["competitors"]

    if len(teams) == 2:
        home = teams[0]["team"]["displayName"]
        away = teams[1]["team"]["displayName"]
        partidos.append(f"{home} vs {away}")

# =======================
# SELECCION PARTIDO
# =======================

partido_seleccionado = st.selectbox("Selecciona Partido", partidos)

mercado = st.selectbox("Selecciona Mercado", ["Local Gana", "Visitante Gana", "Over 2.5"])

cuota = st.number_input("Ingresa la cuota", value=2.0)

banca = st.number_input("Banca actual", value=10000)

# =======================
# GENERADOR DE PICK
# =======================

if st.button("🔥 Generar Pick Automático"):

    # 🔥 Probabilidad simulada inteligente
    prob_modelo = random.uniform(0.45, 0.75)

    prob_implicita = 1 / cuota
    value = prob_modelo - prob_implicita

    kelly = ((cuota - 1) * prob_modelo - (1 - prob_modelo)) / (cuota - 1)
    stake = banca * kelly * 0.25

    st.subheader("📊 Resultado")

    st.write("Probabilidad Modelo:", round(prob_modelo, 2))
    st.write("Probabilidad Implícita:", round(prob_implicita, 2))
    st.write("Value:", round(value, 2))

    if value > 0:
        st.success("✅ HAY VALUE — Recomendado")
    else:
        st.error("❌ NO HAY VALUE")

    st.write("💰 Stake recomendado:", round(stake, 2))
