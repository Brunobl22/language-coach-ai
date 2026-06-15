import streamlit as st

st.title("🌎 AI Language Coach")

st.write("Bem-vindo ao nosso MVP!")

idioma = st.selectbox(
    "Escolha o idioma:",
    ["Inglês", "Espanhol"]
)

mensagem = st.text_input(
    "Digite uma frase:"
)

if st.button("Enviar"):

    if idioma == "Inglês":
        resposta = f"Tradução para inglês: {mensagem}"

    else:
        resposta = f"Tradução para espanhol: {mensagem}"

    st.success(resposta)