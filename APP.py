import requests
import streamlit as st
from datetime import datetime

st.title("ProBet AI - Partidos Reales")

API_KEY = st.secrets["API_KEY"]

# Fecha de hoy automática
hoy = datetime.now().strftime("%Y-%m-%d")

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
querystring = {
    "date": hoy,
    "league": "262",  # Liga MX
    "season": "2026"
}

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

# 👇 MOSTRAMOS EL STATUS PARA DEBUG
st.write("Status Code:", response.status_code)

if response.status_code != 200:
    st.error("Error en la API")
    st.stop()

data = response.json()

# 👇 MOSTRAMOS EL JSON COMPLETO PARA VER QUÉ ESTÁ LLEGANDO
st.write(data)

if "response" not in data:
    st.error("La API no devolvió 'response'")
    st.stop()

if len(data["response"]) == 0:
    st.warning("No hay partidos hoy en Liga MX")
    st.stop()

for match in data["response"]:
    home = match["teams"]["home"]["name"]
    away = match["teams"]["away"]["name"]
    st.write(f"{home} vs {away}")
