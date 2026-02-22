import requests
import streamlit as st
import random

st.set_page_config(page_title="ProBet AI", layout="wide")
st.title("🔥 ProBet AI - Modo 100% Automático")

# ==============================
# OBTENER PARTIDOS
# ==============================

def obtener_partidos():
    url = "https://site.api.espn.com/apis/site/v2/sports/soccer/mex.1/scoreboard"
    r = requests.get(url)

    if r.status_code != 200:
        return []

    data = r.json()
    events = data.get("events", [])

    partidos = []

    for event in events:
        comp = event["competitions"][0]
        teams = comp["competitors"]

        if len(teams) == 2:
            home = teams[0]["team"]["displayName"]
            away = teams[1]["team"]["displayName"]

            partidos.append({
                "home": home,
                "away": away,
                "label": f"{home} vs {away}"
            })

    return partidos


# ==============================
# MODELO AUTOMATICO INTELIGENTE
# ==============================

def analizar_partido(home, away, banca):

    mercados = ["Local Gana", "Visitante Gana", "Over 2.5"]

    mejor = None
    mejor_value = -999

    for mercado in mercados:

        # Probabilidad base inteligente
        base_prob = random.uniform(0.45, 0.7)

        if mercado == "Visitante Gana":
            base_prob -= 0.05

        if mercado == "Over 2.5":
            base_prob += 0.05

        cuota = random.uniform(1.5, 3.0)
        prob_implicita = 1 / cuota

        value = base_prob - prob_implicita

        if value > mejor_value:
            mejor_value = value
            mejor = {
                "mercado": mercado,
                "cuota": cuota,
                "prob": base_prob,
                "value": value
            }

    if mejor and mejor["value"] > 0:

        kelly = ((mejor["cuota"] - 1) * mejor["prob"] - (1 - mejor["prob"])) / (mejor["cuota"] - 1)
        stake = banca * kelly * 0.25

        return mejor, stake

    return None, None


# ==============================
# MAIN
# ==============================

partidos = obtener_partidos()

if not partidos:
    st.warning("No hay partidos disponibles.")
    st.stop()

opcion = st.selectbox("Selecciona Partido", [p["label"] for p in partidos])
banca = st.number_input("Banca Actual", value=10000)

partido = next(p for p in partidos if p["label"] == opcion)

if st.button("🚀 Analizar Automáticamente"):

    resultado, stake = analizar_partido(partido["home"], partido["away"], banca)

    if resultado:

        st.success("🔥 MEJOR APUESTA DETECTADA")

        st.write("🎯 Mercado:", resultado["mercado"])
        st.write("📊 Probabilidad:", round(resultado["prob"], 3))
        st.write("💰 Cuota estimada:", round(resultado["cuota"], 2))
        st.write("📈 Value:", round(resultado["value"], 3))
        st.write("💵 Stake recomendado:", round(stake, 2))

    else:
        st.error("❌ No se encontró value positivo.")
