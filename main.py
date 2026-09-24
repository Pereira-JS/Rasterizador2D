import pygame

from modelos.ponto import Ponto
from modelos.quadrilatero import Quadrilatero
from modelos.sistema_coordenadas import SistemaCoordenadas
from algoritmos.rasterizador import Rasterizador


pygame.init()

LARGURA = 900
ALTURA = 900

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Rasterizador 2D")

sistema = SistemaCoordenadas(LARGURA, ALTURA, escala=1)
rasterizador = Rasterizador(sistema)


# Quadrilátero em coordenadas cartesianas
p1 = Ponto(20, 15)
p2 = Ponto(30, 15)
p3 = Ponto(35, 25)
p4 = Ponto(5, 25)

quadrilatero = Quadrilatero([
    p1,
    p2,
    p3,
    p4
])


rodando = True

while rodando:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

    # Limpa a tela
    tela.fill((255, 255, 255))

    # ==========================
    # PLANO CARTESIANO
    # ==========================

    # ==========================
    # QUADRILÁTERO
    # ==========================

    rasterizador.preencher_quadrilatero(
        tela,
        quadrilatero,
        (50, 150, 255)
    )

    rasterizador.desenhar_quadrilatero(
        tela,
        quadrilatero,
        (0, 0, 0)
    )

    pygame.display.flip()


pygame.quit()