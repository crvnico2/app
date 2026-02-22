response = requests.get(url)

st.subheader("Status Code")
st.write(response.status_code)

st.subheader("Respuesta Cruda")
st.write(response.text)

if response.status_code == 200:
    st.subheader("JSON Parseado")
    st.write(response.json())
