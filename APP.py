import requests
import streamlit as st

st.set_page_config(page_title="Liga Test", layout="wide")
st.title("⚽ Test Endpoint - Liga Básico")

API_KEY = st.secrets["API_KEY"]

league_id = st.text_input("Escribe el League ID", value="")

if st.button("Consultar Liga"):

    if not league_id:
        st.warning("Escribe un League ID")
        st.stop()

    url = f"http://api2.isportsapi.com/deporte/fútbol/liga/básico?api_key={API_KEY}&leagueId={league_id}"

    st.write("🔗 URL Usada:")
    st.code(url)

    response = requests.get(url, timeout=10)

    st.write("Status Code:")
    st.write(response.status_code)

    st.write("Respuesta:")
    st.json(response.json())
