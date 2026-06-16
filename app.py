import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Language Coach")

st.title("🌍 AI Language Coach")
st.write("Converse com um professor de inglês ou espanhol com IA.")

idioma = st.selectbox("Idioma:", ["Inglês", "Espanhol"])
nivel = st.selectbox("Seu nível:", ["Iniciante", "Intermediário", "Avançado"])
objetivo = st.selectbox("Objetivo:", ["Viagem", "Trabalho", "Conversação", "Entrevista"])

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

texto = st.chat_input("Digite sua mensagem...")

if texto:
    st.session_state.mensagens.append({"role": "user", "content": texto})

    prompt = f"""
Você é um professor de {idioma}.
O aluno é nível {nivel}.
Objetivo do aluno: {objetivo}.

Responda como um tutor de idiomas.
Se o aluno escrever em português, traduza e ensine.
Se ele tentar escrever em {idioma}, corrija os erros.
Use resposta curta, simples e didática.
"""

    resposta = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {"role": "system", "content": prompt},
            *st.session_state.mensagens
        ]
    )

    resposta_texto = resposta.output_text

    st.session_state.mensagens.append(
        {"role": "assistant", "content": resposta_texto}
    )

    st.rerun()
