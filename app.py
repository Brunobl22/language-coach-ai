import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Language Coach")

st.title("🌍 AI Language Coach")
st.write("Aprenda inglês e espanhol com IA.")

idioma = st.selectbox(
    "Idioma:",
    ["Inglês", "Espanhol"]
)

frase = st.text_input("Digite uma frase:")

if st.button("Traduzir"):

    prompt = f"""
    Traduza a frase abaixo para {idioma}:

    {frase}
    """

    resposta = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt
    )

    st.success(resposta.output_text)
