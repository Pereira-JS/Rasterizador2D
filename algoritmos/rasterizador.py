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

    def desenhar_linha(self, tela, p1, p2, cor):

        p1_tela = self._para_tela(p1)
        p2_tela = self._para_tela(p2)

        pontos = bresenham(p1_tela,p2_tela)

        for x, y in pontos:
            tela.set_at((x, y), cor)

    def desenhar_quadrilatero(self, tela, quadrilatero, cor):

        pontos = quadrilatero.pontos

        self.desenhar_linha(tela,pontos[0],pontos[1],cor)

        self.desenhar_linha(tela,pontos[1],pontos[2],cor)

        self.desenhar_linha(tela,pontos[2],pontos[3],cor)

        self.desenhar_linha(tela,pontos[3],pontos[0],cor)

    def preencher_quadrilatero(self, tela, quadrilatero, cor):

        quadrilatero_tela = self._quadrilatero_para_tela(quadrilatero)

        preencher_scanline(tela,quadrilatero_tela,cor)