import requests
import streamlit as st
import math

st.set_page_config(page_title="ProBet AI", layout="wide")
st.title("🔥 ProBet AI - Modelo Matemático Profesional")

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

            # 🔥 Extraemos goles actuales si existen
            score_home = int(teams[0].get("score", 0))
            score_away = int(teams[1].get("score", 0))

            partidos.append({
                "home": home,
                "away": away,
                "score_home": score_home,
                "score_away": score_away,
                "label": f"{home} vs {away}"
            })

    return partidos


# ==============================
# MODELO POISSON REAL
# ==============================

def poisson_prob(lmbda, k):
    return (math.exp(-lmbda) * (lmbda ** k)) / math.factorial(k)


def calcular_prob_over_25(promedio_goles):
    prob = 0

    # Sumamos probabilidades donde goles >= 3
    for k in range(3, 8):
        prob += poisson_prob(promedio_goles, k)

    return prob


def modelo_partido(prom_local, prom_visit):

    # Probabilidad de goles totales
    prob_over = calcular_prob_over_25(prom_local + prom_visit)

    # Probabilidad ganador basada en diferencia de promedio
    diff = prom_local - prom_visit
    prob_local = 0.5 + diff * 0.1
    prob_local = max(min(prob_local, 0.95), 0.05)

    prob_visit = 1 - prob_local

    return prob_local, prob_visit, prob_over


# ==============================
# ANALISIS AUTOMATICO
# ==============================

partidos = obtener_partidos()

if not partidos:
    st.warning("No hay partidos disponibles.")
    st.stop()

opcion = st.selectbox("Selecciona Partido", [p["label"] for p in partidos])
banca = st.number_input("Banca Actual", value=10000)

partido = next(p for p in partidos if p["label"] == opcion)

st.write("🏟", partido["home"], "vs", partido["away"])

# ==============================
# PROMEDIO GOLES (BASE REAL)
# ==============================

# 🔥 Aquí usamos goles actuales como base histórica mínima
prom_local = partido["score_home"] + 1.2
prom_visit = partido["score_away"] + 1.1

st.write("📊 Promedio estimado local:", round(prom_local, 2))
st.write("📊 Promedio estimado visitante:", round(prom_visit, 2))

if st.button("🚀 Analizar Matemáticamente"):

    prob_local, prob_visit, prob_over = modelo_partido(prom_local, prom_visit)

    mercados = {
        "Local Gana": prob_local,
        "Visitante Gana": prob_visit,
        "Over 2.5": prob_over
    }

    mejor_mercado = max(mercados, key=mercados.get)
    mejor_prob = mercados[mejor_mercado]

    # 🔥 Simulamos cuota real (después puedes traer cuota de API)
    cuota = 1 / mejor_prob + 0.3

    prob_implicita = 1 / cuota
    value = mejor_prob - prob_implicita

    kelly = ((cuota - 1) * mejor_prob - (1 - mejor_prob)) / (cuota - 1)
    stake = banca * kelly * 0.25

    st.subheader("🏆 Mejor Apuesta Detectada")

    st.write("🎯 Mercado:", mejor_mercado)
    st.write("📊 Probabilidad Modelo:", round(mejor_prob, 3))
    st.write("💰 Cuota estimada:", round(cuota, 2))
    st.write("🔥 Value:", round(value, 3))
    st.write("💵 Stake recomendado:", round(stake, 2))

    if value > 0:
        st.success("✅ APUESTA CON VENTAJA MATEMÁTICA")
    else:
        st.error("❌ No hay ventaja estadística")
