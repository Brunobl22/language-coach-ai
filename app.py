import streamlit as st

st.set_page_config(page_title="AI Language Coach")

st.title("🌎 AI Language Coach")

idioma = st.selectbox(
    "Escolha o idioma:",
    ["Inglês", "Espanhol"]
)

mensagem = st.text_input("Digite uma frase:")

traducao_en = {
    "bom dia": "Good morning",
    "boa tarde": "Good afternoon",
    "boa noite": "Good night",
    "olá": "Hello",
    "tchau": "Goodbye"
}

traducao_es = {
    "bom dia": "Buenos días",
    "boa tarde": "Buenas tardes",
    "boa noite": "Buenas noches",
    "olá": "Hola",
    "tchau": "Adiós"
}

if st.button("Enviar"):
    texto = mensagem.lower()

    if idioma == "Inglês":
        resposta = traducao_en.get(
            texto,
            "Tradução não encontrada."
        )
    else:
        resposta = traducao_es.get(
            texto,
            "Tradução não encontrada."
        )

    st.success(resposta)
