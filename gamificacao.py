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
        },
        "conquistas": []
    }


def calcular_nivel(xp):
    return max(1, xp // 100 + 1)


def xp_restante(xp):
    return 100 - (xp % 100)


def progresso_nivel(xp):
    return (xp % 100) / 100


def dar_recompensa(st):
    st.session_state.xp += 10
    st.session_state.moedas += 1
    st.session_state.missoes += 1

    if st.session_state.missoes >= 5:
        st.session_state.missoes = 0
        st.session_state.moedas += 5

    return "🎉 Você ganhou 10 XP e 1 moeda!"
