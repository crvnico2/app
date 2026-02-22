import requests
import streamlit as st

# ==============================
# CONFIGURACIÓN
# ==============================

st.set_page_config(page_title="ProBet AI", layout="wide")
st.title("🔥 ProBet AI - Livescores iSports")

# Tu API Key desde Secrets
API_KEY = st.secrets["API_KEY"]

# ==============================
# FUNCION PARA TRAER PARTIDOS
# ==============================

def obtener_livescores():
    url = f"http://api.isportsapi.com/sport/football/livescores?api_key={API_KEY}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            st.error("❌ Error conectando a la API")
            st.write(response.text)
            return []

        data = response.json()

        # Algunos planes devuelven "data", otros "result"
        partidos = data.get("data") or data.get("result") or []

        return partidos

    except Exception as e:
        st.error("❌ Error de conexión")
        st.write(e)
        return []


# ==============================
# OBTENER DATOS
# ==============================

partidos = obtener_livescores()

if not partidos:
    st.warning("⚠️ No hay partidos activos o la API no devolvió datos.")
    st.stop()

# ==============================
# FORMATEAR LISTA PARA SELECTBOX
# ==============================

lista_partidos = []

for p in partidos:
    home = p.get("homeTeam") or p.get("home_team") or "Local"
    away = p.get("awayTeam") or p.get("away_team") or "Visitante"

    etiqueta = f"{home} vs {away}"
    lista_partidos.append(etiqueta)

# ==============================
# SELECCIONAR PARTIDO
# ==============================

opcion = st.selectbox("Selecciona Partido", lista_partidos)

seleccion = None

for p in partidos:
    home = p.get("homeTeam") or p.get("home_team") or ""
    away = p.get("awayTeam") or p.get("away_team") or ""

    etiqueta = f"{home} vs {away}"

    if etiqueta == opcion:
        seleccion = p
        break

if not seleccion:
    st.error("❌ No se pudo cargar el partido seleccionado")
    st.stop()

# ==============================
# MOSTRAR INFORMACIÓN
# ==============================

st.subheader("🏟 Partido Seleccionado")

home = seleccion.get("homeTeam") or seleccion.get("home_team")
away = seleccion.get("awayTeam") or seleccion.get("away_team")

home_score = seleccion.get("homeScore") or seleccion.get("home_score") or 0
away_score = seleccion.get("awayScore") or seleccion.get("away_score") or 0

minute = seleccion.get("matchTime") or seleccion.get("minute") or "N/A"

st.write("🔵 Local:", home)
st.write("🔴 Visitante:", away)
st.write("⚽ Marcador:", home_score, "-", away_score)
st.write("⏱ Minuto:", minute)

st.success("✅ Datos cargados correctamente")
