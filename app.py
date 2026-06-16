import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Language Coach", layout="centered")

st.title("🌍 AI Language Coach")
st.write("Converse com um professor de inglês do dia a dia com IA.")

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

st.sidebar.header("Seu progresso")
if "streak" not in st.session_state:
    st.session_state.streak = 1

st.sidebar.write(f"🔥 Sequência: {st.session_state.streak} dias")
if "vidas" not in st.session_state:
    st.session_state.vidas = 5

st.sidebar.write(f"❤️ Vidas: {st.session_state.vidas}/5")
if "moedas" not in st.session_state:
    st.session_state.moedas = 0

st.sidebar.write(f"🪙 Moedas: {st.session_state.moedas}")
xp = st.session_state.xp
nivel_usuario = xp // 100 + 1
progresso = (xp % 100) / 100

st.sidebar.write(f"⭐ XP: {xp}")
st.sidebar.write(f"🏆 Nível: {nivel_usuario}")
st.sidebar.progress(progresso)
faltam = 100 - (xp % 100)

st.sidebar.write(f"Faltam {faltam} XP para o próximo nível")
if xp >= 50:
     st.sidebar.success("🥉 Primeiras 50 XP")
if xp >= 100:
    st.sidebar.success("🥉 Medalha Bronze")

if xp >= 500:
    st.sidebar.success("🥈 Medalha Prata")

if xp >= 1000:
    st.sidebar.success("🥇 Medalha Ouro")
    st.sidebar.success("🎓 Certificado desbloqueado!")
    
if xp >= 250:
    st.sidebar.success("🔥 Estudante Dedicado")

if xp >= 500:
    st.sidebar.success("🚀 Mestre da Conversação")

if xp >= 1000:
    st.sidebar.success("👑 Lenda do Inglês")
nivel = st.selectbox("Seu nível:", ["Iniciante", "Intermediário", "Avançado"])
modo = st.selectbox("Modo:", ["Conversação", "Aula do dia", "Desafio rápido", "Correção de frase"])

st.markdown("### 👨‍🏫 Teacher Alex")
st.info("Olá! Eu sou seu professor de inglês. Vamos praticar conversa real.")

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

texto = st.chat_input("Digite sua resposta ou mensagem...")

if texto:
    st.session_state.mensagens.append({"role": "user", "content": texto})

    prompt = f"""
Você é Teacher Alex, um professor de inglês para brasileiros.

Nível do aluno: {nivel}
Modo: {modo}

Regras:
- Responda em português simples.
- Use inglês do dia a dia.
- Corrija erros do aluno.
- Dê nota de 0 a 10.
- Se estiver bom, escreva exatamente: +10 XP
- Se tiver erro mas tentou, escreva exatamente: +5 XP
- Sempre termine com uma pergunta curta em inglês.
- Seja amigável e pareça um professor humano.
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
            st.session_state.moedas += 1
    
        elif "+5 XP" in resposta_texto:
            st.session_state.xp += 5
            st.session_state.moedas += 1
    
        st.session_state.mensagens.append(
            {"role": "assistant", "content": resposta_texto}
        )
    
        st.rerun()
            st.rerun()
