import requests
import streamlit as st

st.set_page_config(page_title="API Test", layout="wide")
st.title("🔎 Test Conexión iSports - API2")

API_KEY = st.secrets["API_KEY"]

# 🔥 USAMOS API2
url = f"http://api2.isportsapi.com/sport/football/livescores?api_key={API_KEY}"

st.write("🌍 URL usada:")
st.code(url)

try:
    response = requests.get(url, timeout=10)

    st.write("📊 Status Code:")
    st.write(response.status_code)

    st.write("📦 Respuesta Cruda:")
    st.code(response.text)

except Exception as e:
    st.error("❌ Error conectando")
    st.write(str(e))
