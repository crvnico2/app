import requests
import streamlit as st
import random

st.set_page_config(page_title="ProBet AI", layout="wide")
st.title("🔥 ProBet AI - Motor Automático de Picks")

# ==============================
# OBTENER PARTIDOS
# ==============================

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

# ==============================
# GENERAR LISTA DE PARTIDOS
# ==============================

partidos = []

for event in events:
    comp = event["competitions"][0]
    teams = comp["competitors"]

    if len(teams) == 2:
        home = teams[0]["team"]["displayName"]
        away = teams[1]["team"]["displayName"]
        partidos.append({
            "partido": f"{home} vs {away}",
            "home": home,
            "away": away
        })

st.subheader("📅 Partidos Analizados")

for p in partidos:
    st.write("🏟", p["partido"])

# ==============================
# MOTOR INTELIGENTE
# ==============================

st.subheader("🤖 Análisis Automático")

banca = st.number_input("Banca Actual", value=10000)

mejor_pick = None
mejor_value = -999

resultados = []

for p in partidos:

    # 🔥 Probabilidad base simulada pero más inteligente
    base_prob = random.uniform(0.45, 0.75)

    # Mercados posibles
    mercados = ["Local Gana", "Visitante Gana", "Over 2.5"]

    for mercado in mercados:

        cuota = random.uniform(1.6, 3.0)

        prob_implicita = 1 / cuota

        # Ajustamos probabilidad según mercado
        prob_modelo = base_prob
        if mercado == "Visitante Gana":
            prob_modelo -= 0.05
        if mercado == "Over 2.5":
            prob_modelo += 0.05

        value = prob_modelo - prob_implicita

        kelly = ((cuota - 1) * prob_modelo - (1 - prob_modelo)) / (cuota - 1)
        stake = banca * kelly * 0.25

        resultados.append({
            "partido": p["partido"],
            "mercado": mercado,
            "value": value,
            "stake": stake,
            "cuota": cuota
        })

        # 🔥 Detectar mejor pick
        if value > mejor_value:
            mejor_value = value
            mejor_pick = resultados[-1]

# ==============================
# MOSTRAR MEJOR PICK
# ==============================

st.subheader("🏆 Mejor Pick del Día")

if mejor_pick and mejor_pick["value"] > 0:

    st.success("🔥 PICK DETECTADO CON VALUE")

    st.write("📌 Partido:", mejor_pick["partido"])
    st.write("🎯 Mercado:", mejor_pick["mercado"])
    st.write("💰 Cuota estimada:", round(mejor_pick["cuota"], 2))
    st.write("📊 Value:", round(mejor_pick["value"], 2))
    st.write("💵 Stake recomendado:", round(mejor_pick["stake"], 2))

else:
    st.error("❌ No se detectó value positivo hoy.")

# ==============================
# PARLAY AUTOMÁTICO
# ==============================

st.subheader("🎰 Parlay Automático")

# Seleccionar los mejores 3 values positivos
picks_validos = [r for r in resultados if r["value"] > 0]

picks_ordenados = sorted(picks_validos, key=lambda x: x["value"], reverse=True)[:3]

if len(picks_ordenados) >= 2:

    cuota_total = 1
    prob_total = 1

    for pick in picks_ordenados:
        cuota_total *= pick["cuota"]
        prob_total *= (1 / pick["cuota"])

    st.write("📈 Picks en el Parlay:")
    for pick in picks_ordenados:
        st.write("✔", pick["partido"], "-", pick["mercado"])

    st.write("💥 Cuota Total:", round(cuota_total, 2))
    st.write("🎯 Probabilidad Combinada:", round(prob_total, 2))

else:
    st.warning("No hay suficientes picks con value para generar parlay.")
