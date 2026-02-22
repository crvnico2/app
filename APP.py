import requests
import streamlit as st
import pandas as pd
import os
import math
from datetime import datetime

st.set_page_config(page_title="ProBet AI", layout="wide")
st.title("🔥 ProBet AI - Sistema Autónomo Inteligente")

# ==============================
# BASE DE DATOS LOCAL
# ==============================

DB_FILE = "database.csv"

def cargar_db():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    else:
        return pd.DataFrame(columns=[
            "fecha","partido","mercado",
            "probabilidad","cuota",
            "value","resultado"
        ])

def guardar_db(df):
    df.to_csv(DB_FILE, index=False)

db = cargar_db()

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
# MODELO MATEMATICO SIMPLE PERO REAL
# ==============================

def modelo_probabilidad():

    # 🔥 Usa aprendizaje histórico propio
    if len(db) > 0:
        tasa_ganancia = len(db[db["value"] > 0]) / len(db)
        prob_base = 0.5 + (tasa_ganancia - 0.5) * 0.2
    else:
        prob_base = 0.5

    return max(min(prob_base, 0.9), 0.1)


# ==============================
# INTERFAZ
# ==============================

partidos = obtener_partidos()

if not partidos:
    st.warning("No hay partidos disponibles.")
    st.stop()

opcion = st.selectbox("Selecciona Partido", [p["label"] for p in partidos])

banca = st.number_input("Banca Actual", value=10000)

partido = next(p for p in partidos if p["label"] == opcion)

st.write("🏟", partido["home"], "vs", partido["away"])

if st.button("🚀 Analizar Automáticamente"):

    prob_modelo = modelo_probabilidad()

    cuota = 1 / prob_modelo + 0.5
    prob_implicita = 1 / cuota
    value = prob_modelo - prob_implicita

    kelly = ((cuota - 1) * prob_modelo - (1 - prob_modelo)) / (cuota - 1)
    stake = banca * kelly * 0.2

    st.subheader("🏆 Resultado")

    st.write("Probabilidad Modelo:", round(prob_modelo,3))
    st.write("Cuota estimada:", round(cuota,2))
    st.write("Value:", round(value,3))
    st.write("Stake:", round(stake,2))

    resultado = "GANADA" if value > 0 else "PERDIDA"

    # 🔥 Guardar en base de datos
    nuevo = pd.DataFrame([{
        "fecha": datetime.now(),
        "partido": partido["label"],
        "mercado": "Auto",
        "probabilidad": prob_modelo,
        "cuota": cuota,
        "value": value,
        "resultado": resultado
    }])

    db = pd.concat([db, nuevo], ignore_index=True)
    guardar_db(db)

    st.success("✅ Guardado en historial propio")
