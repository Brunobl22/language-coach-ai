import streamlit as st
from openai import OpenAI
import json
import os
from datetime import date

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ARQUIVO = "progresso.json"
ARQUIVO_USUARIOS = "usuarios.json"

if os.path.exists(ARQUIVO):
    with open(ARQUIVO, "r") as f:
        dados = json.load(f)
else:
    dados = {}
def progresso_padrao():
    return {
        "xp": 0,
        "moedas": 0,
        "vidas": 5,
        "missoes": 0,
        "streak": 1,
        "ultimo_dia": "",
        "ultima_aula": "",
        "perfil": {
        "nome": "",
         "cidade": "",
          "objetivo": "",
          "erros_comuns": []
 }
  }
def salvar_usuarios():
    with open(ARQUIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f)

def salvar_progresso():
    if "usuario" not in st.session_state:
        return
    usuario_atual = st.session_state.usuario
    usuarios[usuario_atual]["progresso"] = {
        "xp": st.session_state.xp,
        "moedas": st.session_state.moedas,
        "vidas": st.session_state.vidas,
        "missoes": st.session_state.missoes,
        "streak": st.session_state.streak,
        "ultima_aula": st.session_state.get("ultima_aula", ""),
        "ultimo_dia": st.session_state.get("ultimo_dia", ""),
        "mensagens": st.session_state.mensagens,
        "perfil": st.session_state.get("perfil", {
        "nome": "",
        "cidade": "",
        "objetivo": "",
        "erros_comuns": []
})
 }
    salvar_usuarios()

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
        usuarios[usuario] = {
            "senha": senha,
            "progresso": progresso_padrao()
        }
        salvar_usuarios()
        st.sidebar.success("Usuário criado!")
        st.session_state.logado = True
        st.session_state.usuario = usuario
        st.rerun()

    elif usuarios[usuario]["senha"] == senha:
        progresso = usuarios[usuario].get("progresso", progresso_padrao())
        st.session_state.xp = progresso["xp"]
        st.session_state.moedas = progresso["moedas"]
        st.session_state.vidas = progresso["vidas"]
        st.session_state.missoes = progresso["missoes"]
        st.session_state.streak = progresso["streak"]
        st.session_state.ultimo_dia = progresso.get("ultimo_dia", "")
        st.session_state.ultima_aula = progresso.get("ultima_aula", "")
        st.session_state.mensagens = progresso.get("mensagens", [])
        perfil_salvo = progresso.get("perfil", {})
        st.session_state.perfil = {
            "nome": perfil_salvo.get("nome", ""),
            "cidade": perfil_salvo.get("cidade", ""),
            "objetivo": perfil_salvo.get("objetivo", ""),
            "erros_comuns": perfil_salvo.get("erros_comuns", [])
}
        st.write("OBJETIVO CARREGADO:", perfil_salvo.get("objetivo", "VAZIO"))
        st.sidebar.success("Login realizado!")
        st.session_state.logado = True
        st.session_state.usuario = usuario
        st.rerun()

    else:
        st.sidebar.error("Senha incorreta")

st.set_page_config(page_title="AI Language Coach", layout="centered")

st.title("🌍 AI Language Coach")
col1, col2 = st.columns([1, 4])

with col1:
    st.image(
        "https://api.dicebear.com/7.x/bottts/png?seed=TeacherAlex",
        width=120
    )

with col2:
    st.markdown("### 👨‍🏫 Teacher Alex")
    st.write("Seu professor virtual de inglês do dia a dia.")
st.write("Converse com um professor de inglês do dia a dia com IA.")

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

if "streak" not in st.session_state:
    st.session_state.streak = 1

if "ultimo_dia" not in st.session_state:
    st.session_state.ultimo_dia = ""

if "vidas" not in st.session_state:
    st.session_state.vidas = 5

if "moedas" not in st.session_state:
    st.session_state.moedas = 0

if "missoes" not in st.session_state:
    st.session_state.missoes = 0

st.sidebar.write(f"🎯 Missões feitas: {st.session_state.missoes}/5")

if st.session_state.missoes >= 5:
    st.sidebar.success("🎁 Missão diária completa!")

hoje = str(date.today())

if st.session_state.ultimo_dia != hoje:
    st.session_state.streak += 1
    st.session_state.ultimo_dia = hoje
    salvar_progresso()

st.sidebar.write(f"🔥 Streak diária: {st.session_state.streak} dias")

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

with st.sidebar.expander("📄 Meu Perfil", expanded=False):

    if "perfil" not in st.session_state:
        st.session_state.perfil = {
            "nome": "",
            "cidade": "",
            "objetivo": ""
        }

    nome_aluno = st.text_input(
        "Nome",
        value=st.session_state.perfil["nome"]
    )

    cidade_aluno = st.text_input(
        "Cidade",
        value=st.session_state.perfil["cidade"]
    )

    objetivo_aluno = st.text_input(
    "Objetivo",
    value=st.session_state.perfil.get("objetivo", ""),
    key="objetivo_perfil_input"
)

    if st.button("💾 Salvar Perfil"):
        st.session_state.perfil["nome"] = nome_aluno
        st.session_state.perfil["cidade"] = cidade_aluno
        st.session_state.perfil["objetivo"] = st.session_state.objetivo_perfil_input
        st.write(st.session_state.perfil)
        salvar_progresso()
        st.success("Perfil salvo!")
    
nivel = st.selectbox("Seu nível:", ["Iniciante", "Intermediário", "Avançado"])
modo = st.selectbox("Modo:", ["Conversação", "Aula do dia", "Desafio rápido", "Correção de frase"])
if modo == "Aula do dia":
    st.session_state.ultima_aula = "Greetings and Introductions"
    salvar_progresso()

st.markdown("### 👨‍🏫 Teacher Alex")
st.info("Olá! Eu sou seu professor de inglês. Vamos praticar conversa real.")

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

    if msg["role"] == "assistant":
        try:
            tts = gTTS(text=msg["content"], lang="en")
            tts.save("alex.mp3")
            with open("alex.mp3", "rb") as audio_file:
                st.audio(audio_file.read(), format="audio/mp3")
        except:
            pass
texto = st.chat_input("Digite sua resposta ou mensagem...")  

if texto:
    st.session_state.mensagens.append({"role": "user", "content": texto})

    prompt = f"""
Você é Teacher Alex, professor de inglês para brasileiros.

Nome do aluno: {st.session_state.perfil["nome"]}
Cidade: {st.session_state.perfil["cidade"]}
Objetivo: {st.session_state.perfil["objetivo"]}

Use essas informações para personalizar as aulas e exemplos.

Explique SEMPRE em português simples.
Use inglês apenas nos exemplos, frases e perguntas.
Sempre traduza o inglês para português.
Seja paciente, natural e motivador.

Formato:
Correção:
Tradução:
Explicação:
Novo exemplo:
Pergunta:
"""

    resposta = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {"role": "system", "content": prompt},
            *st.session_state.mensagens
        ]
    )

    resposta_texto = resposta.output_text

    st.session_state.xp += 10
    st.session_state.moedas += 1
    st.session_state.missoes = min(st.session_state.missoes + 1, 5)
    salvar_progresso()

    st.session_state.mensagens.append(
        {"role": "assistant", "content": resposta_texto}
    )

    st.rerun()
