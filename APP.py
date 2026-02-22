import requests
import streamlit as st

# ==============================
# CONFIG
# ==============================

st.set_page_config(page_title="ProBet AI", layout="wide")
st.title("🔥 ProBet AI - Livescores iSports")

API_KEY = st.secrets["API_KEY"]

# ==============================
# OBTENER PARTIDOS
# ==============================

def obtener_livescores():
    url = f"http://api.isportsapi.com/sport/football/livescores?api_key={API_KEY}"

    try:
        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            st.error("❌ Error conexión API")
            st.write(r.text)
            return []

        data = r.json()

        partidos = data.get("data") or data.get("result") or []

        return partidos

    except Exception as e:
        st.error("❌ Error de conexión")
        st.write(e)
        return []


# ==============================
# CARGAR DATOS
# ==============================

partidos = obtener_livescores()

if not partidos:
    st.warning("⚠️ No hay partidos activos.")
    st.stop()

# ==============================
# CREAR LISTA USANDO ID (NO TEXTO)
# ==============================

opciones = {}

for p in partidos:

    partido_id = p.get("matchId") or p.get("id")

    home = p.get("homeTeam") or p.get("home_team") or "Local"
    away = p.get("awayTeam") or p.get("away_team") or "Visitante"

    label = f"{home} vs {away}"

    if partido_id:
        opciones[label] = partido_id

# Si no hay partidos válidos
if not opciones:
    st.error("❌ No se pudieron leer partidos correctamente.")
    st.stop()

# ==============================
# SELECTBOX
# ==============================

seleccion_label = st.selectbox("Selecciona Partido", list(opciones.keys()))
seleccion_id = opciones[seleccion_label]

# ==============================
# BUSCAR PARTIDO POR ID
# ==============================

seleccion = None

for p in partidos:
    pid = p.get("matchId") or p.get("id")
    if pid == seleccion_id:
        seleccion = p
        break

if not seleccion:
    st.error("❌ Error cargando partido.")
    st.stop()

# ==============================
# MOSTRAR INFO
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
