import math

from modelos.ponto import Ponto
from modelos.quadrilatero import Quadrilatero


class Transformacoes:

    # ============================================================
    # PIVÔ (ponto de referência da transformação)
    # ============================================================

    @staticmethod
    def centroide(quadrilatero):
        """
        Calcula o centroide (centro geométrico) do quadrilátero,
        como a média aritmética dos vértices.
        """

        pontos = quadrilatero.pontos
        n = len(pontos)

        soma_x = sum(p.x for p in pontos)
        soma_y = sum(p.y for p in pontos)

        return Ponto(soma_x / n, soma_y / n)

    @staticmethod
    def _resolver_pivot(quadrilatero, pivot):
        """
        Resolve o ponto de referência usado como pivô da transformação.

        pivot: "origem" -> (0, 0)
               "centroide" -> centro geométrico do próprio quadrilátero
        """

        if pivot == "centroide":
            return Transformacoes.centroide(quadrilatero)

        if pivot == "origem":
            return Ponto(0, 0)

        raise ValueError(
            f"Pivô inválido: '{pivot}'. Use 'origem' ou 'centroide'."
        )

    # ============================================================
    # ESCALA
    # ============================================================

    @staticmethod
    def escalar(quadrilatero, sx, sy, pivot="origem"):
        """
        Aplica escala aos vértices do quadrilátero.

        x' = x * sx
        y' = y * sy

        pivot: "origem" (0, 0) ou "centroide" do próprio quadrilátero.
        Estratégia: transladar o pivô para a origem, escalar,
        e transladar de volta.

        Retorna um novo quadrilátero, preservando o original.
        """

        referencia = Transformacoes._resolver_pivot(quadrilatero, pivot)

        novos_pontos = []

        for ponto in quadrilatero.pontos:

            # Translada o pivô para a origem
            x = ponto.x - referencia.x
            y = ponto.y - referencia.y

            # Escala
            x = x * sx
            y = y * sy

            # Translada de volta
            x = x + referencia.x
            y = y + referencia.y

            novos_pontos.append(
                Ponto(x, y)
            )

        return Quadrilatero(novos_pontos)

    # ============================================================
    # ROTAÇÃO
    # ============================================================

    @staticmethod
    def rotacionar(quadrilatero, angulo_graus, pivot="origem"):
        """
        Aplica rotação 2D aos vértices do quadrilátero.

        x' = x*cos(a) - y*sin(a)
        y' = x*sin(a) + y*cos(a)

        pivot: "origem" (0, 0) ou "centroide" do próprio quadrilátero.
        Estratégia: transladar o pivô para a origem, rotacionar,
        e transladar de volta.

        Retorna um novo quadrilátero, preservando o original.
        """

        referencia = Transformacoes._resolver_pivot(quadrilatero, pivot)

        angulo_rad = math.radians(angulo_graus)

        cos_a = math.cos(angulo_rad)
        sin_a = math.sin(angulo_rad)

        novos_pontos = []

        for ponto in quadrilatero.pontos:

            # Translada o pivô para a origem
            x = ponto.x - referencia.x
            y = ponto.y - referencia.y

            # Rotaciona
            novo_x = x * cos_a - y * sin_a
            novo_y = x * sin_a + y * cos_a

            # Translada de volta
            novo_x += referencia.x
            novo_y += referencia.y

            novos_pontos.append(
                Ponto(novo_x, novo_y)
            )

        return Quadrilatero(novos_pontos)