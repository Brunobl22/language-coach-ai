 import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Language Coach")

st.title("🌍 AI Language Coach")
st.write("Professor de inglês do dia a dia com IA, desafios e XP.")

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

st.sidebar.header("Seu progresso")
st.sidebar.write(f"⭐ XP: {st.session_state.xp}")

nivel = st.selectbox("Seu nível:", ["Iniciante", "Intermediário", "Avançado"])
modo = st.selectbox("Modo:", ["Aula do dia", "Conversação", "Desafio rápido", "Correção de frase"])

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

texto = st.chat_input("Digite sua resposta ou mensagem...")

if texto:
    st.session_state.mensagens.append({"role": "user", "content": texto})

    prompt = f"""
Você é um professor de inglês do dia a dia.
Nível do aluno: {nivel}
Modo escolhido: {modo}

Regras:
- Fale em português simples.
- Ensine inglês útil para situações reais.
- Corrija erros do aluno com gentileza.
- Dê uma nota de 0 a 10 quando o aluno tentar responder em inglês.
- Se a resposta estiver boa, diga: +10 XP.
- Se tiver erro, diga: +5 XP por tentativa.
- No final, faça uma nova pergunta ou desafio curto.
"""

    resposta = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {"role": "system", "content": prompt},
            *st.session_state.mensagens
        ]
    )

    resposta_texto = resposta.output_text

    if "+10 XP" in resposta_texto:
        st.session_state.xp += 10
    elif "+5 XP" in resposta_texto:
        st.session_state.xp += 5

    st.session_state.mensagens.append(
        {"role": "assistant", "content": resposta_texto}
    )

    st.rerun()
