from cerebro import analisar_mensagem, escolher_proxima_acao, montar_contexto_alex
from observador import observar_aluno
from memoria import resumo_memoria
from perfil import resumo_perfil
from personalidade import personalidade_por_nivel
from evolucao import resumo_evolucao
from aprendizado import atualizar_aprendizado, resumo_aprendizado
from plano_aula import escolher_plano, resumo_plano
from mentor import orientar_professor, resumo_mentor
from missao import definir_missao, resumo_missao
from diretor_pedagogico import decidir_estrategia, resumo_estrategia


def preparar_resposta_alex(mensagem, nivel, modo, perfil=None, memoria=None):
    analise = analisar_mensagem(mensagem)

    observacoes = observar_aluno(mensagem, analise)

    memoria = atualizar_aprendizado(memoria, observacoes)

    acao = escolher_proxima_acao(analise)

    mentor = orientar_professor(
    analise,
    memoria,
    perfil
)

    mentor_resumo = resumo_mentor(mentor)

    missao = definir_missao(
    analise,
    memoria,
    perfil
)

   missao_resumo = resumo_missao(missao)

    plano = escolher_plano(acao, memoria, perfil)
    plano_resumo = resumo_plano(plano)

    contexto = montar_contexto_alex(
        perfil_resumo=resumo_perfil(perfil),
        memoria_resumo=resumo_memoria(memoria),
        acao=acao
    )

   contexto = contexto + f"""

    Orientações do Mentor:
    
    {mentor_resumo}
    
    Missão do Alex nesta resposta:
    
    {missao_resumo}
    
    Sempre siga essas orientações antes de responder ao aluno.
    """
    personalidade = personalidade_por_nivel(nivel)

    evolucao = resumo_evolucao(memoria)

    aprendizado = resumo_aprendizado(memoria)

    return {
        "analise": analise,
        "observacoes": observacoes,
        "acao": acao,
        "contexto": contexto,
        "personalidade": personalidade,
        "evolucao": evolucao,
        "aprendizado": aprendizado,
        "plano": plano_resumo
    }
