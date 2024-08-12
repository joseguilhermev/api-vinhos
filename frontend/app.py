import streamlit as st
import requests

BASE_URL = "http://localhost:8000"


def fetch_data(endpoint):
    response = requests.get(f"{BASE_URL}{endpoint}")
    return response.json() if response.ok else []


def main():
    st.sidebar.title("Dados da Vitivinicultura")
    app_mode = st.sidebar.selectbox(
        "Escolha uma categoria",
        ["Producao", "Processamento", "Comercializacao", "Importacao", "Exportacao"],
    )

    year = st.sidebar.slider(
        "Selecione o ano", min_value=1970, max_value=2023, value=2023
    )

    if app_mode == "Producao":
        item = st.sidebar.text_input("Item")
        if st.button("Pegue os dados"):
            data = fetch_data(f"/producao/{year}/{item}")
            st.write(data)

    elif app_mode == "Processamento":
        category = st.sidebar.text_input("Categoria")
        item = st.sidebar.text_input("Item")
        if st.button("Pegue os dados"):
            data = fetch_data(f"/processamento/{year}/{category}/{item}")
            st.write(data)

    elif app_mode == "Comercializacao":
        item = st.sidebar.text_input("Item")
        if st.button("Pegue os dados"):
            data = fetch_data(f"/comercializacao/{year}/{item}")
            st.write(data)

    elif app_mode == "Importacao":
        category = st.sidebar.text_input("Categoria")
        if st.button("Pegue os dados"):
            data = fetch_data(f"/importacao/{year}/{category}")
            st.write(data)

    elif app_mode == "Exportacao":
        category = st.sidebar.text_input("Categoria")
        if st.button("Pegue os dados"):
            data = fetch_data(f"/exportacao/{year}/{category}")
            st.write(data)


if __name__ == "__main__":
    main()
