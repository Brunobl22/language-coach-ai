import streamlit as st
from openai import OpenAI
from supabase import create_client
from datetime import date

from teacher_alex import TeacherAlex
from gamificacao import progresso_padrao, calcular_nivel
from supabase_db import (
    carregar_usuarios,
    salvar_usuario,
    usuario_existe,
    senha_correta
)

st.set_page_config(page_title="AI Language Coach", page_icon="🌍", layout="wide")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
alex = TeacherAlex(client)
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

TABELA = "usuarios"


st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #111827 50%, #1e1b4b 100%);
    color: white;
}

.main-card {
    background: rgba(255,255,255,0.08);
    padding: 30px;
    border-radius: 25px;
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
}

.teacher-card {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    padding: 25px;
    border-radius: 25px;
    color: white;
    margin-bottom: 20px;
}

.metric-card {
    background: rgba(255,255,255,0.10);
    padding: 15px;
    border-radius: 18px;
    margin-bottom: 10px;
    border: 1px solid rgba(255,255,255,0.12);
}

.chat-box {
    background: rgba(255,255,255,0.08);
    padding: 18px;
    border-radius: 18px;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)


def progresso_padrao():
    return {
        "xp": 0,
        "moedas": 0,
        "vidas": 5,
        "missoes": 0,
        "streak": 1,
        "ultimo_dia": "",
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
    except Exception as e:
        st.sidebar.error("Erro ao carregar usuários do Supabase")
    return usuarios


def salvar_usuario(usuario, senha, progresso):
    try:
        supabase.table(TABELA).upsert(
            {
                "usuario": usuario,
                "senha": senha,
                "progresso": progresso
            },
            on_conflict="usuario"
        ).execute()
    except Exception as e:
        st.error("Erro ao salvar no Supabase. Confira se a coluna usuario está com regra UNIQUE.")
        st.stop()


def carregar_progresso(progresso):
    padrao = progresso_padrao()

    st.session_state.xp = progresso.get("xp", padrao["xp"])
    st.session_state.moedas = progresso.get("moedas", padrao["moedas"])
    st.session_state.vidas = progresso.get("vidas", padrao["vidas"])
    st.session_state.missoes = progresso.get("missoes", padrao["missoes"])
    st.session_state.streak = progresso.get("streak", padrao["streak"])
    st.session_state.ultimo_dia = progresso.get("ultimo_dia", padrao["ultimo_dia"])
    st.session_state.mensagens = progresso.get("mensagens", padrao["mensagens"])
    st.session_state.perfil = progresso.get("perfil", padrao["perfil"])


def montar_progresso():
    return {
        "xp": st.session_state.get("xp", 0),
        "moedas": st.session_state.get("moedas", 0),
        "vidas": st.session_state.get("vidas", 5),
        "missoes": st.session_state.get("missoes", 0),
        "streak": st.session_state.get("streak", 1),
        "ultimo_dia": st.session_state.get("ultimo_dia", ""),
        "mensagens": st.session_state.get("mensagens", []),
        "perfil": st.session_state.get("perfil", progresso_padrao()["perfil"])
    }


def salvar_progresso():
    if st.session_state.get("logado") and st.session_state.get("usuario"):
        salvar_usuario(
            st.session_state.usuario,
            st.session_state.senha,
            montar_progresso()
        )


def logout():
    st.session_state.clear()
    st.rerun()


usuarios = carregar_usuarios()

if "logado" not in st.session_state:
    st.session_state.logado = False


with st.sidebar:
    st.markdown("## 🌍 AI Coach")

    if st.session_state.logado:
        st.success(f"Logado como: {st.session_state.usuario}")

        if st.button("Sair"):
            logout()

    else:
        st.markdown("### 🔐 Entrar ou cadastrar")
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar / Cadastrar"):
            if not usuario or not senha:
                st.error("Digite usuário e senha")

            elif usuario in usuarios:
                if usuarios[usuario]["senha"] == senha:
                    st.session_state.logado = True
                    st.session_state.usuario = usuario
                    st.session_state.senha = senha
                    carregar_progresso(usuarios[usuario]["progresso"])
                    st.rerun()
                else:
                    st.error("Senha incorreta")

            else:
                progresso = progresso_padrao()
                salvar_usuario(usuario, senha, progresso)

                st.session_state.logado = True
                st.session_state.usuario = usuario
                st.session_state.senha = senha
                carregar_progresso(progresso)
                st.rerun()

    if "xp" not in st.session_state:
        carregar_progresso(progresso_padrao())

    nivel_atual = max(1, st.session_state.xp // 100 + 1)
    progresso_nivel = (st.session_state.xp % 100) / 100
    xp_restante = 100 - (st.session_state.xp % 100)

    st.markdown("---")
    st.markdown("### 📊 Seu progresso")
    st.write(f"🎯 Missões feitas: *{st.session_state.missoes}/5*")
    st.write(f"🔥 Streak diária: *{st.session_state.streak} dias*")
    st.write(f"⭐ XP: *{st.session_state.xp}*")
    st.write(f"🪙 Moedas: *{st.session_state.moedas}*")
    st.write(f"🏆 Nível: *{nivel_atual}*")
    st.progress(progresso_nivel)
    st.caption(f"Faltam {xp_restante} XP para o próximo nível")

    st.markdown("---")
    st.markdown("### 🛒 Loja")

    if st.button("Comprar vida extra - 3 moedas"):
        if st.session_state.moedas >= 3:
            st.session_state.moedas -= 3
            st.session_state.vidas += 1
            salvar_progresso()
            st.success("Vida comprada!")
            st.rerun()
        else:
            st.error("Moedas insuficientes")

    if st.button("Comprar dica - 2 moedas"):
        if st.session_state.moedas >= 2:
            st.session_state.moedas -= 2
            salvar_progresso()
            st.info("Dica: responda com frases curtas em inglês.")
        else:
            st.error("Moedas insuficientes")

    with st.expander("📄 Meu Perfil"):
        nome = st.text_input("Nome", value=st.session_state.perfil.get("nome", ""))
        cidade = st.text_input("Cidade", value=st.session_state.perfil.get("cidade", ""))
        objetivo = st.text_area("Objetivo", value=st.session_state.perfil.get("objetivo", ""))

        if st.button("Salvar perfil"):
            st.session_state.perfil["nome"] = nome
            st.session_state.perfil["cidade"] = cidade
            st.session_state.perfil["objetivo"] = objetivo
            salvar_progresso()
            st.success("Perfil salvo!")


col_esq, col_dir = st.columns([1, 2])

with col_esq:
    st.markdown("""
    <div class="teacher-card">
        <h1>🤖 Teacher Alex</h1>
        <p>Seu professor virtual de inglês do dia a dia.</p>
        <p>Aprenda conversando, ganhe XP, moedas e evolua seu nível.</p>
    </div>
    """, unsafe_allow_html=True)

    st.image(
        "https://api.dicebear.com/7.x/bottts/png?seed=TeacherAlex",
        width=220
    )

    st.markdown(f"""
    <div class="metric-card">🏆 Nível atual: <b>{nivel_atual}</b></div>
    <div class="metric-card">⭐ XP: <b>{st.session_state.xp}</b></div>
    <div class="metric-card">🪙 Moedas: <b>{st.session_state.moedas}</b></div>
    <div class="metric-card">❤️ Vidas: <b>{st.session_state.vidas}</b></div>
    """, unsafe_allow_html=True)


with col_dir:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)

    st.title("🌍 AI Language Coach")
    st.subheader("Aprenda inglês conversando com IA")

    if not st.session_state.logado:
        st.warning("Faça login na barra lateral para salvar seu progresso.")

    nivel_escolhido = st.selectbox(
        "Seu nível:",
        ["Iniciante", "Intermediário", "Avançado"]
    )

    modo = st.selectbox(
        "Modo:",
        ["Conversação", "Correção", "Vocabulário", "Treino rápido"]
    )

    if not st.session_state.mensagens:
        st.session_state.mensagens.append({
            "role": "assistant",
            "content": "Olá! Eu sou o Teacher Alex. Vamos praticar inglês de um jeito simples e real."
        })

    for msg in st.session_state.mensagens:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    mensagem = st.chat_input("Digite sua resposta ou mensagem...")

    if mensagem:
        st.session_state.mensagens.append({
            "role": "user",
            "content": mensagem
        })

        prompt_sistema = f"""
Você é Teacher Alex, um professor de inglês amigável para brasileiros.

O aluno está no nível: {nivel_escolhido}.
Modo atual: {modo}.

Regras:
- Responda em português simples.
- Ensine inglês do dia a dia.
- Corrija o aluno com calma.
- Dê exemplos curtos.
- Incentive o aluno.
- Não seja rude.
- Se o aluno escrever algo em inglês errado, corrija e explique.
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

    st.markdown("</div>", unsafe_allow_html=True)
