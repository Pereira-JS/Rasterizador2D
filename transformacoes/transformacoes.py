from modelos.ponto import Ponto
from modelos.quadrilatero import Quadrilatero


class Transformacoes:

    @staticmethod
    def escalar(quadrilatero, sx, sy):
        """
        Aplica escala aos vértices do quadrilátero.

        x' = x * sx
        y' = y * sy

        Retorna um novo quadrilátero,
        preservando o original.
        """

        novos_pontos = []

        for ponto in quadrilatero.pontos:

            novo_x = ponto.x * sx
            novo_y = ponto.y * sy

            novos_pontos.append(
                Ponto(novo_x, novo_y)
            )

        return Quadrilatero(novos_pontos)