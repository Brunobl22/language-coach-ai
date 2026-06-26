import streamlit as st
from openai import OpenAI
from supabase import create_client
from datetime import date

st.set_page_config(page_title="AI Language Coach", layout="centered")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

TABELA = "usuarios"


def progresso_padrao():
    return {
        "xp": 0,
        "moedas": 0,
        "vidas": 5,
        "missoes": 0,
        "streak": 1,
        "ultimo_dia": "",
        "ultima_aula": "",
        "mensagens": [],
        "perfil": {
            "nome": "",
            "cidade": "",
            "objetivo": "",
            "erros_comuns": []
        }
    }


def carregar_usuarios():
    usuarios = {}
    try:
        resposta = supabase.table(TABELA).select("*").execute()
        for item in resposta.data:
            usuarios[item["usuario"]] = {
                "senha": item["senha"],
                "progresso": item.get("progresso") or progresso_padrao()
            }
    except Exception:
        st.sidebar.error("Erro ao carregar usuários do banco")
    return usuarios


def salvar_usuario(usuario, senha, progresso):
    supabase.table(TABELA).upsert({
        "usuario": usuario,
        "senha": senha,
        "progresso": progresso
    }).execute()


def carregar_progresso(progresso):
    st.session_state.xp = progresso.get("xp", 0)
    st.session_state.moedas = progresso.get("moedas", 0)
    st.session_state.vidas = progresso.get("vidas", 5)
    st.session_state.missoes = progresso.get("missoes", 0)
    st.session_state.streak = progresso.get("streak", 1)
    st.session_state.ultimo_dia = progresso.get("ultimo_dia", "")
    st.session_state.ultima_aula = progresso.get("ultima_aula", "")
    st.session_state.mensagens = progresso.get("mensagens", [])
    st.session_state.perfil = progresso.get("perfil", progresso_padrao()["perfil"])


def salvar_progresso():
    if not st.session_state.get("logado"):
        return

    progresso = {
        "xp": st.session_state.get("xp", 0),
        "moedas": st.session_state.get("moedas", 0),
        "vidas": st.session_state.get("vidas", 5),
        "missoes": st.session_state.get("missoes", 0),
        "streak": st.session_state.get("streak", 1),
        "ultimo_dia": st.session_state.get("ultimo_dia", ""),
        "ultima_aula": st.session_state.get("ultima_aula", ""),
        "mensagens": st.session_state.get("mensagens", []),
        "perfil": st.session_state.get("perfil", progresso_padrao()["perfil"])
    }

    senha = st.session_state.get("senha", "")
    usuario = st.session_state.get("usuario", "")

    if usuario:
        salvar_usuario(usuario, senha, progresso)


def fazer_logout():
    for chave in list(st.session_state.keys()):
        del st.session_state[chave]
    st.rerun()


usuarios = carregar_usuarios()

if "logado" not in st.session_state:
    st.session_state.logado = False

if st.session_state.logado:
    st.sidebar.success(f"Logado como: {st.session_state.usuario}")

    if st.sidebar.button("Sair"):
        fazer_logout()

if not st.session_state.logado:
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔐 Login")

    usuario = st.sidebar.text_input("Usuário")
    senha = st.sidebar.text_input("Senha", type="password")

    if st.sidebar.button("Entrar / Cadastrar"):
        if not usuario or not senha:
            st.sidebar.error("Digite usuário e senha")

        elif usuario in usuarios:
            if usuarios[usuario]["senha"] == senha:
                st.session_state.logado = True
                st.session_state.usuario = usuario
                st.session_state.senha = senha
                carregar_progresso(usuarios[usuario]["progresso"])
                st.sidebar.success("Login realizado!")
                st.rerun()
            else:
                st.sidebar.error("Senha incorreta")

        else:
            progresso = progresso_padrao()
            salvar_usuario(usuario, senha, progresso)

            st.session_state.logado = True
            st.session_state.usuario = usuario
            st.session_state.senha = senha
            carregar_progresso(progresso)

            st.sidebar.success("Usuário criado!")
            st.rerun()


if "xp" not in st.session_state:
    carregar_progresso(progresso_padrao())


st.sidebar.markdown("---")
st.sidebar.write(f"🎯 Missões feitas: {st.session_state.missoes}/5")
st.sidebar.write(f"🔥 Streak diária: {st.session_state.streak} dias")
st.sidebar.write(f"⭐ XP: {st.session_state.xp}")
st.sidebar.write(f"🪙 Moedas: {st.session_state.moedas}")

nivel = max(1, st.session_state.xp // 100 + 1)
xp_restante = 100 - (st.session_state.xp % 100)

st.sidebar.write(f"🏆 Nível: {nivel}")
st.sidebar.progress((st.session_state.xp % 100) / 100)
st.sidebar.write(f"Faltam {xp_restante} XP para o próximo nível")

st.sidebar.markdown("### 🛒 Loja")

if st.sidebar.button("Comprar vida extra - 3 moedas"):
    if st.session_state.moedas >= 3:
        st.session_state.moedas -= 3
        st.session_state.vidas += 1
        salvar_progresso()
        st.sidebar.success("Vida extra comprada!")
        st.rerun()
    else:
        st.sidebar.error("Moedas insuficientes")

if st.sidebar.button("Comprar dica - 2 moedas"):
    if st.session_state.moedas >= 2:
        st.session_state.moedas -= 2
        salvar_progresso()
        st.sidebar.info("Dica: tente responder com frases curtas em inglês.")
        st.rerun()
    else:
        st.sidebar.error("Moedas insuficientes")

with st.sidebar.expander("📄 Meu Perfil"):
    nome = st.text_input("Nome", value=st.session_state.perfil.get("nome", ""))
    cidade = st.text_input("Cidade", value=st.session_state.perfil.get("cidade", ""))
    objetivo = st.text_area("Objetivo", value=st.session_state.perfil.get("objetivo", ""))

    if st.button("Salvar perfil"):
        st.session_state.perfil["nome"] = nome
        st.session_state.perfil["cidade"] = cidade
        st.session_state.perfil["objetivo"] = objetivo
        salvar_progresso()
        st.success("Perfil salvo!")


st.title("🌍 AI Language Coach")

col1, col2 = st.columns([1, 4])

with col1:
    st.image(
        "https://api.dicebear.com/7.x/bottts/png?seed=TeacherAlex",
        width=120
    )

with col2:
    st.markdown("## 👨‍🏫 Teacher Alex")
    st.write("Seu professor virtual de inglês do dia a dia.")

st.write("Converse com um professor de inglês do dia a dia com IA.")

nivel_escolhido = st.selectbox("Seu nível:", ["Iniciante", "Intermediário", "Avançado"])
modo = st.selectbox("Modo:", ["Conversação", "Correção", "Vocabulário", "Treino rápido"])

st.markdown("## 👨‍🏫 Teacher Alex")

if not st.session_state.mensagens:
    st.session_state.mensagens.append({
        "role": "assistant",
        "content": "Olá! Eu sou seu professor de inglês. Vamos praticar conversa real."
    })

for msg in st.session_state.mensagens:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])


mensagem = st.chat_input("Digite sua resposta ou mensagem...")

if mensagem:
    st.session_state.mensagens.append({"role": "user", "content": mensagem})

    prompt_sistema = f"""
Você é Teacher Alex, um professor de inglês amigável para brasileiros.
O aluno está no nível {nivel_escolhido}.
Modo atual: {modo}.

Responda em português simples, mas ensine inglês.
Corrija erros com calma.
Dê exemplos curtos.
Incentive o aluno.
Nunca seja rude.
"""

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt_sistema},
            *st.session_state.mensagens[-10:]
        ]
    )

    texto = resposta.choices[0].message.content

    st.session_state.mensagens.append({
        "role": "assistant",
        "content": texto
    })

    hoje = str(date.today())

    if st.session_state.ultimo_dia != hoje:
        st.session_state.streak += 1
        st.session_state.ultimo_dia = hoje

    st.session_state.xp += 10
    st.session_state.moedas += 1
    st.session_state.missoes += 1

    if st.session_state.missoes >= 5:
        st.session_state.missoes = 0
        st.session_state.moedas += 5

    salvar_progresso()
    st.rerun()
