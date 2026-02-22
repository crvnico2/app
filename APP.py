import requests
import streamlit as st

st.set_page_config(page_title="API Test", layout="wide")
st.title("🔎 Prueba Conexión iSports")

API_KEY = st.secrets["API_KEY"]

url = f"http://api.isportsapi.com/sport/football/competitions?api_key={API_KEY}"

st.write("🔗 URL usada:")
st.code(url)

try:
    response = requests.get(url, timeout=5)

    st.write("Status Code:")
    st.write(response.status_code)

    st.write("Respuesta:")
    st.code(response.text)

except Exception as e:
    st.error("Error conectando:")
    st.write(str(e))
