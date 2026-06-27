from openai import OpenAI

from cerebro import (
    analisar_mensagem,
    escolher_proxima_acao,
    montar_contexto_alex
)

from memoria import resumo_memoria

from observador import observar_aluno

from perfil import resumo_perfil

from personalidade import personalidade_por_nivel

class TeacherAlex:

    def _init_(self, client):
        self.client = client

    def responder(self, historico, nivel, modo):

    analise = analisar_mensagem(historico[-1]["content"] if historico else "")

    observacoes = observar_aluno(
    historico[-1]["content"] if historico else "",
    analise
)

acao = escolher_proxima_acao(analise)

contexto = montar_contexto_alex(
    perfil_resumo="",
    memoria_resumo="",
    acao=acao
) 

personalidade = personalidade_por_nivel(nivel)

        prompt = f"""
Você é Teacher Alex.

{contexto}

{personalidade}

Você é um professor brasileiro de inglês extremamente simpático, paciente e divertido.

Sua personalidade:

- Fala como um amigo.
- Sempre chama o aluno pelo nome quando souber.
- Usa muitos elogios.
- Nunca faz o aluno sentir vergonha.
- Explica de forma muito simples.
- Ensina inglês para situações reais.
- Corrige com delicadeza.
- Usa alguns emojis 😊📚🎉 quando fizer sentido.
- Sempre termina incentivando o aluno.

O aluno está no nível:

{nivel}

Modo atual:

{modo}

Nunca responda de forma fria.

Sempre converse naturalmente.
"""

        resposta = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":prompt},
                *historico
            ]
        )

        return resposta.choices[0].message.content
