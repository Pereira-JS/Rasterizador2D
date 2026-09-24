import pygame

from modelos.ponto import Ponto
from modelos.quadrilatero import Quadrilatero
from modelos.sistema_coordenadas import SistemaCoordenadas
from algoritmos.rasterizador import Rasterizador


pygame.init()

# ==========================
# CONFIGURAÇÕES
# ==========================

LARGURA = 900
ALTURA = 600
ESCALA = 2

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Rasterizador 2D")

sistema = SistemaCoordenadas(
    LARGURA,
    ALTURA,
    ESCALA
)

rasterizador = Rasterizador(sistema)


# ==========================
# VARIÁVEIS
# ==========================

pontos_selecionados = []
quadrilatero = None

rodando = True


# ==========================
# LOOP PRINCIPAL
# ==========================

while rodando:

    # --------------------------
    # EVENTOS
    # --------------------------

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        # Clique esquerdo
        if evento.type == pygame.MOUSEBUTTONDOWN:

            if evento.button == 1:

                # Só permite selecionar 4 pontos
                if len(pontos_selecionados) < 4:

                    x, y = evento.pos

                    # Converte pixel da tela
                    # para coordenada do sistema
                    x, y = sistema.para_cartesiana(
                        x,
                        y
                    )

                    ponto = Ponto(x, y)

                    pontos_selecionados.append(ponto)

                    print(
                        f"P{len(pontos_selecionados)}: "
                        f"({x}, {y})"
                    )

                    # Quando tiver 4 pontos,
                    # cria o quadrilátero
                    if len(pontos_selecionados) == 4:

                        quadrilatero = Quadrilatero(
                            pontos_selecionados
                        )

                        print("Quadrilátero criado!")


    # --------------------------
    # LIMPA A TELA
    # --------------------------

    tela.fill((255, 255, 255))


    # --------------------------
    # MOSTRA OS PONTOS CLICADOS
    # --------------------------

    for ponto in pontos_selecionados:

        x, y = sistema.para_tela(
            ponto.x,
            ponto.y
        )

        # Pequeno quadrado apenas para
        # visualizar o ponto selecionado
        for dx in range(-2, 3):
            for dy in range(-2, 3):

                px = x + dx
                py = y + dy

                if (
                    0 <= px < LARGURA
                    and 0 <= py < ALTURA
                ):
                    tela.set_at(
                        (px, py),
                        (255, 0, 0)
                    )


    # --------------------------
    # DESENHA QUADRILÁTERO
    # --------------------------

    if quadrilatero is not None:

        # Preenchimento
        rasterizador.preencher_quadrilatero(
            tela,
            quadrilatero,
            (50, 150, 255)
        )

        # Bordas
        rasterizador.desenhar_quadrilatero(
            tela,
            quadrilatero,
            (0, 0, 0)
        )


    # --------------------------
    # ATUALIZA A TELA
    # --------------------------

    pygame.display.flip()


pygame.quit()