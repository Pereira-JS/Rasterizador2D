from modelos.ponto import Ponto
from modelos.quadrilatero import Quadrilatero

from algoritmos.bresenham import bresenham
from algoritmos.preenchimento import preencher_scanline


class Rasterizador:

    def __init__(self, sistema):
        self.sistema = sistema

    def _para_tela(self, ponto):
        x, y = self.sistema.para_tela(ponto.x,ponto.y)

        return Ponto(x, y)

    def _quadrilatero_para_tela(self, quadrilatero):

        pontos = [
            self._para_tela(ponto)
            for ponto in quadrilatero.pontos
        ]

        return Quadrilatero(pontos)

    def _dentro_da_area_desenhavel(self, x, y):
        """
        Impede que qualquer pixel seja pintado sobre o menu lateral
        (à esquerda de sistema.offset_x) ou fora dos limites da
        janela - evita tanto a sobreposição visual quanto erros de
        índice fora da superfície do pygame.
        """

        return (
            self.sistema.offset_x <= x < self.sistema.largura
            and 0 <= y < self.sistema.altura
        )

    def _misturar_com_fundo(self, tela, x, y, cor, alpha):
        """
        Mistura 'cor' com o pixel de fundo já presente na tela,
        de acordo com 'alpha' (0 a 255), simulando opacidade.
        alpha=255 é totalmente opaco (cor pura).
        """

        if alpha >= 255:
            return cor

        fundo = tela.get_at((x, y))

        a = alpha / 255

        r = int(cor[0] * a + fundo[0] * (1 - a))
        g = int(cor[1] * a + fundo[1] * (1 - a))
        b = int(cor[2] * a + fundo[2] * (1 - a))

        return (r, g, b)

    def desenhar_linha(self, tela, p1, p2, cor, alpha=255):

        p1_tela = self._para_tela(p1)
        p2_tela = self._para_tela(p2)

        pontos = bresenham(p1_tela,p2_tela)

        for x, y in pontos:
            if self._dentro_da_area_desenhavel(x, y):
                cor_final = self._misturar_com_fundo(tela, x, y, cor, alpha)
                tela.set_at((x, y), cor_final)

    def desenhar_quadrilatero(self, tela, quadrilatero, cor, alpha=255):

        pontos = quadrilatero.pontos

        self.desenhar_linha(tela,pontos[0],pontos[1],cor,alpha)

        self.desenhar_linha(tela,pontos[1],pontos[2],cor,alpha)

        self.desenhar_linha(tela,pontos[2],pontos[3],cor,alpha)

        self.desenhar_linha(tela,pontos[3],pontos[0],cor,alpha)

    def preencher_quadrilatero(self, tela, quadrilatero, cor, alpha=255):

        quadrilatero_tela = self._quadrilatero_para_tela(quadrilatero)

        preencher_scanline(
            tela,
            quadrilatero_tela,
            cor,
            limite_esquerdo=self.sistema.offset_x,
            limite_direito=self.sistema.largura,
            limite_superior=0,
            limite_inferior=self.sistema.altura,
            alpha=alpha,
        )