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
from coordenador import avaliar_resposta, resumo_coordenador
from supervisor import revisar_resposta, resumo_supervisor


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

    estrategia = decidir_estrategia(
    analise,
    memoria,
    perfil,
    missao,
    plano
)

    estrategia_resumo = resumo_estrategia(estrategia)

    coordenador = avaliar_resposta(
    analise,
    memoria,
    perfil
    )

    coordenador_resumo = resumo_coordenador(coordenador)

    supervisor = revisar_resposta(
    analise,
    estrategia,
    coordenador
)

    supervisor_resumo = resumo_supervisor(supervisor)

    contexto = montar_contexto_alex(
        perfil_resumo=resumo_perfil(perfil),
        memoria_resumo=resumo_memoria(memoria),
        acao=acao
    )

    contexto = contexto + f"""

    Orientações do Mentor:
    
    {mentor_resumo}

    Estratégia pedagógica:

    {estrategia_resumo}

    Sempre siga essa estratégia durante esta resposta.

    Avaliação do Coordenador:

    {coordenador_resumo}
    
    Utilize essa avaliação para decidir se deve reforçar, explicar novamente ou avançar.

    Revisão do Supervisor:

    {supervisor_resumo}

    Siga também esta revisão antes de responder ao aluno.
      
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
