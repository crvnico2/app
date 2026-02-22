import requests
import streamlit as st
from bs4 import BeautifulSoup

st.set_page_config(page_title="ProBet AI", layout="wide")
st.title("⚽ ProBet AI - Partidos Automáticos (Sin API Key)")

# 🔥 Fuente pública
url = "https://www.flashscore.com/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

if response.status_code != 200:
    st.error("No se pudo obtener información")
    st.stop()

soup = BeautifulSoup(response.text, "html.parser")

# Buscar elementos que contienen partidos
matches = soup.find_all("div")

st.subheader("📅 Datos obtenidos (Vista básica)")

count = 0

for match in matches:
    text = match.get_text(strip=True)
    if "vs" in text.lower():
        st.write(text)
        count += 1
    if count > 20:
        break

