import requests
import streamlit as st

st.set_page_config(page_title="Debug API", layout="wide")
st.title("🔎 DEBUG iSports API")

API_KEY = st.secrets["API_KEY"]

url = f"http://api.isportsapi.com/sport/football/livescores?api_key={API_KEY}"

try:
    response = requests.get(url, timeout=10)

    st.subheader("Status Code")
    st.write(response.status_code)

    st.subheader("Respuesta Cruda")
    st.code(response.text)

    if response.status_code == 200:
        st.subheader("JSON Parseado")
        st.write(response.json())

except Exception as e:
    st.error("❌ Error conectando a la API")
    st.write(str(e))
