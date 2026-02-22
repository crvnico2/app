import requests
import streamlit as st

st.title("🔥 ProBet AI - Partidos Futbol API Pública")

# Endpoint público
url = "https://api.football-data.org/v4/matches"

response = requests.get(url)

st.write("Status:", response.status_code)

if response.status_code == 200:
    data = response.json()
    st.json(data)
else:
    st.error("Error al obtener datos de partidos")
    st.write(response.text)
