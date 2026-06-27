from cerebro import analisar_mensagem, escolher_proxima_acao, montar_contexto_alex
from observador import observar_aluno
from memoria import resumo_memoria
from perfil import resumo_perfil
from personalidade import personalidade_por_nivel
from evolucao import resumo_evolucao
from aprendizado import atualizar_aprendizado, resumo_aprendizado


def preparar_resposta_alex(mensagem, nivel, modo, perfil=None, memoria=None):
    analise = analisar_mensagem(mensagem)

    observacoes = observar_aluno(mensagem, analise)

    memoria = atualizar_aprendizado(memoria, observacoes)

    aprendizado = resumo_aprendizado(memoria)

    acao = escolher_proxima_acao(analise)

    contexto = montar_contexto_alex(
        perfil_resumo=resumo_perfil(perfil),
        memoria_resumo=resumo_memoria(memoria),
        acao=acao
    )

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
         "aprendizado": aprendizado
    }
