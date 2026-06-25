import streamlit as st
from openai import OpenAI
from supabase import create_client
import json
import os
from datetime import date

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)
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
    if "usuario" not in st.session_state:
        return

    usuario_atual = st.session_state.usuario
    dados_usuario = usuarios[usuario_atual]

    supabase.table("usuarios").update({
        "senha": dados_usuario["senha"],
        "progresso": dados_usuario["progresso"]
    }).eq("usuario", usuario_atual).execute()

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

usuarios = {}

try:
    resposta = supabase.table("usuarios").select("*").execute()

    for item in resposta.data:
        usuarios[item["usuario"]] = {
            "senha": item["senha"],
            "progresso": item["progresso"]
        }

except Exception as e:
    st.sidebar.error("Erro ao carregar usuários do banco")
    
if not st.session_state.get("logado", False):
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔐 Login")

    usuario = st.sidebar.text_input("Usuário")
    senha = st.sidebar.text_input("Senha", type="password")

if st.sidebar.button("Entrar / Cadastrar"):
    if not usuario or not senha:
        st.sidebar.error("Digite usuário e senha")

    elif usuario in usuarios:
        if usuarios[usuario]["senha"] == senha:
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

            st.sidebar.success("Login realizado!")
            st.session_state.logado = True
            st.session_state.usuario = usuario
            st.rerun()
        else:
            st.sidebar.error("Senha incorreta")

    else:
        usuarios[usuario] = {
            "senha": senha,
            "progresso": progresso_padrao()
        }

        st.session_state.usuario = usuario
        salvar_usuarios()

        st.sidebar.success("Usuário criado!")
        st.session_state.logado = True
        st.session_state.usuario = usuario
        st.rerun()

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
st.sidebar.write(f"🪙 Moedas: {st.session_state.moedas}")
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
    st.session_state.perfil["objetivo"]
)

    if st.button("💾 Salvar Perfil"):
        st.session_state.perfil["nome"] = nome_aluno
        st.session_state.perfil["cidade"] = cidade_aluno
        st.session_state.perfil["objetivo"] = objetivo_aluno
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
Você é o Teacher Alex, um professor de inglês humano, amigável, paciente e motivador.

Nome do aluno: {st.session_state.perfil["nome"]}
Cidade: {st.session_state.perfil["cidade"]}
Objetivo: {st.session_state.perfil["objetivo"]}

Você conversa como um professor particular real.

REGRAS:

- Nunca responda como uma IA.
- Nunca responda como uma barra de pesquisa.
- Converse naturalmente.
- Demonstre interesse genuíno pelo aluno.
- Seja gentil, paciente e encorajador.
- Use o nome do aluno ocasionalmente.
- Faça a aula parecer uma conversa real.
- Sempre termine incentivando o aluno a continuar.

ENSINO:

- Explique em português simples.
- Use inglês apenas nos exemplos e exercícios.
- Sempre traduza exemplos importantes.
- Ensine uma coisa de cada vez.
- Evite respostas muito longas.
- Prefira conversas naturais em vez de listas.

CORREÇÃO INTELIGENTE:

- Se o aluno errar, não diga apenas que está errado.
- Mostre primeiro o que ele acertou.
- Explique de forma amigável.
- Mostre a forma correta.
- Explique o motivo do erro de forma simples.
- Dê um exemplo parecido.
- Peça para ele tentar novamente.
- Se ele estiver muito próximo da resposta correta, diga que ele quase acertou.
- Se ele acertar, elogie e ensine uma forma mais natural usada por nativos.

COMPORTAMENTO:

- Fale como um professor humano conversando.
- Evite usar sempre os mesmos títulos.
- Não use obrigatoriamente "Correção", "Tradução" ou "Explicação".
- Varie a forma de responder.
- Misture conversa, ensino e motivação.
- Faça o aluno se sentir confortável mesmo errando.

OBJETIVO PRINCIPAL:

Fazer o aluno aprender inglês através de uma conversa natural, leve e divertida, como se estivesse conversando com um professor particular de verdade.
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
