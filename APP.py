import requests
import streamlit as st

st.set_page_config(page_title="League Basic", layout="wide")
st.title("⚽ Obtener Ligas - Endpoint Basic")

API_KEY = st.secrets["API_KEY"]

# Endpoint correcto según documentación
url = f"http://api.isportsapi.com/sport/football/league/basic?api_key={API_KEY}"

st.write("🔗 URL usada:")
st.code(url)

if st.button("Obtener Ligas"):

    try:
        response = requests.get(url, timeout=10)

        st.write("Status Code:")
        st.write(response.status_code)

        data = response.json()

        st.subheader("📦 JSON Devuelto")
        st.json(data)

        # Intentamos extraer ligas
        leagues = data.get("data", [])

        st.subheader("⚽ Ligas Encontradas")

        for league in leagues:
            name = league.get("name")
            league_id = league.get("leagueId")
            short = league.get("shortName")

            st.write(f"✅ {name} | ID: {league_id} | Short: {short}")

    except Exception as e:
        st.error("❌ Error llamando la API")
        st.write(str(e))
