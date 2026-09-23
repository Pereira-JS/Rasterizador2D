import pygame



# classes do projeto
from modelos.ponto import Ponto
from modelos.quadrilatero import Quadrilatero
from algoritmos.bresenham import bresenham

pygame.init()

tela = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Rasterizador 2D")


p1 = Ponto(100, 100)
p2 = Ponto(500, 400)

pontos = bresenham(p1, p2)

for x, y in pontos:
    tela.set_at((x, y), (255, 255, 255))

rodando = True
while rodando:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        # eventos de mouse
        # eventos de teclado
        # etc.

    # atualizar objetos
    # rasterizar
    # desenhar na tela

    pygame.display.flip()

pygame.quit()