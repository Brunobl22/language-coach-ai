import streamlit as st
from openai import OpenAI
import json
import os

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ARQUIVO = "progresso.json"
ARQUIVO_USUARIOS = "usuarios.json"

if os.path.exists(ARQUIVO):
    with open(ARQUIVO, "r") as f:
        dados = json.load(f)
else:
    dados = {}
def salvar_progresso():
    dados = {
        "xp": st.session_state.xp,
        "moedas": st.session_state.moedas,
        "vidas": st.session_state.vidas,
        "missoes": st.session_state.missoes,
        "streak": st.session_state.streak
    }

    with open(ARQUIVO, "w") as f:
        json.dump(dados, f)
if os.path.exists(ARQUIVO_USUARIOS):
    with open(ARQUIVO_USUARIOS, "r") as f:
        usuarios = json.load(f)
else:
    usuarios = {}

st.sidebar.markdown("---")
st.sidebar.subheader("🔐 Login")

usuario = st.sidebar.text_input("Usuário")
senha = st.sidebar.text_input("Senha", type="password")

if st.sidebar.button("Entrar / Cadastrar"):
    if usuario not in usuarios:
        usuarios[usuario] = {"senha": senha}

        with open(ARQUIVO_USUARIOS, "w") as f:
            json.dump(usuarios, f)

        st.sidebar.success("Usuário criado!")

    elif usuarios[usuario]["senha"] == senha:
        st.sidebar.success("Login realizado!")

    else:
        st.sidebar.error("Senha incorreta")

st.set_page_config(page_title="AI Language Coach", layout="centered")

st.title("🌍 AI Language Coach")
st.write("Converse com um professor de inglês do dia a dia com IA.")

if "xp" not in st.session_state:
    st.session_state.xp = dados.get("xp", 0)

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

st.sidebar.header("Seu progresso")
if "streak" not in st.session_state:
    st.session_state.streak = dados.get("streak", 1)

st.sidebar.write(f"🔥 Sequência: {st.session_state.streak} dias")
if "vidas" not in st.session_state:
    st.session_state.vidas = dados.get("vidas", 5)

st.sidebar.write(f"❤️ Vidas: {st.session_state.vidas}/5")
if "moedas" not in st.session_state:
    st.session_state.moedas = dados.get("moedas", 0)

st.sidebar.write(f"🪙 Moedas: {st.session_state.moedas}")
if "missoes" not in st.session_state:
    st.session_state.missoes = dados.get("missoes", 0)

st.sidebar.write(f"🎯 Missões feitas: {st.session_state.missoes}/5")

if st.session_state.missoes >= 5:
    st.sidebar.success("🎁 Missão diária completa!")

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
    st.sidebar.markdown("---")
st.sidebar.subheader("🛒 Loja")

if st.sidebar.button("Comprar vida extra - 3 moedas"):
    if st.session_state.moedas >= 3:
        st.session_state.moedas -= 3
        st.session_state.vidas += 1
        salvar_progresso()
        st.sidebar.success("❤️ Vida extra comprada!")
    else:
        st.sidebar.error("Moedas insuficientes")

if st.sidebar.button("Comprar dica - 2 moedas"):
    if st.session_state.moedas >= 2:
        st.session_state.moedas -= 2
        salvar_progresso()
        st.sidebar.success("💡 Dica desbloqueada!")
    else:
        st.sidebar.error("Moedas insuficientes")
        st.sidebar.markdown("---")

if st.sidebar.button("📊 Meu Perfil"):
    st.sidebar.info(f"""
👤 Nome: Bruno

⭐ XP Total: {st.session_state.xp}

🏆 Nível: {nivel_usuario}

🪙 Moedas: {st.session_state.moedas}

🎯 Missões Concluídas: {st.session_state.missoes}

❤️ Vidas: {st.session_state.vidas}

🔥 Sequência: {st.session_state.streak} dias
""")
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
        st.session_state.missoes += 1
        salvar_progresso()
    
    elif "+5 XP" in resposta_texto:
        st.session_state.xp += 5
        st.session_state.moedas += 1
        st.session_state.missoes += 1
        salvar_progresso()
    
    st.session_state.mensagens.append(
    {"role": "assistant", "content": resposta_texto}
    )
    
    st.rerun()
