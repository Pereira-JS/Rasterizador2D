import pygame

from modelos.ponto import Ponto
from modelos.quadrilatero import Quadrilatero
from modelos.sistema_coordenadas import SistemaCoordenadas
from algoritmos.rasterizador import Rasterizador
from modelos.validacao import quadrilatero_valido


pygame.init()


# ============================================================
# CONFIGURAÇÕES DA TELA
# ============================================================

LARGURA = 1000
ALTURA = 600

LARGURA_MENU = 250

ESCALA = 2

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Rasterizador 2D")


# ============================================================
# CORES
# ============================================================

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (230, 230, 230)
CINZA_ESCURO = (80, 80, 80)
AZUL = (50, 150, 255)
AZUL_ESCURO = (30, 100, 180)
VERMELHO = (220, 50, 50)
VERDE = (50, 170, 80)


# ============================================================
# FONTES
# ============================================================

fonte_titulo = pygame.font.Font(None, 30)
fonte = pygame.font.Font(None, 24)
fonte_pequena = pygame.font.Font(None, 20)


# ============================================================
# SISTEMA
# ============================================================

sistema = SistemaCoordenadas(
    LARGURA,
    ALTURA,
    ESCALA
)

rasterizador = Rasterizador(sistema)


# ============================================================
# ESTADO DO PROGRAMA
# ============================================================

pontos_selecionados = []
quadrilatero = None


# Campos de texto
campo_x = ""
campo_y = ""

campo_ativo = None


# ============================================================
# ÁREAS DOS BOTÕES E CAMPOS
# ============================================================

botao_resetar = pygame.Rect(
    20, 60, 210, 40
)

campo_x_rect = pygame.Rect(
    20, 150, 90, 35
)

campo_y_rect = pygame.Rect(
    130, 150, 100, 35
)

botao_adicionar = pygame.Rect(
    20, 200, 210, 40
)


# ============================================================
# FUNÇÕES
# ============================================================

def resetar():
    """
    Limpa todos os pontos e o quadrilátero.
    """
    global pontos_selecionados
    global quadrilatero
    global campo_x
    global campo_y

    pontos_selecionados.clear()

    quadrilatero = None

    campo_x = ""
    campo_y = ""


def adicionar_ponto(x, y):
    """
    Adiciona um ponto à lista.

    Quando chegar a quatro pontos,
    tenta criar o quadrilátero.
    """

    global quadrilatero

    if len(pontos_selecionados) >= 4:
        return

    ponto = Ponto(x, y)

    pontos_selecionados.append(ponto)

    print(
        f"P{len(pontos_selecionados)}: "
        f"({x}, {y})"
    )

    # Quando tivermos 4 pontos
    if len(pontos_selecionados) == 4:

        if quadrilatero_valido(pontos_selecionados):

            quadrilatero = Quadrilatero(
                pontos_selecionados.copy()
            )

            print("Quadrilátero válido criado!")

        else:

            print("Quadrilátero inválido!")

            pontos_selecionados.clear()


def desenhar_texto(texto, x, y, fonte_usada, cor=PRETO):
    """
    Facilita o desenho de textos na tela.
    """

    superficie = fonte_usada.render(
        texto,
        True,
        cor
    )

    tela.blit(
        superficie,
        (x, y)
    )


def desenhar_botao(rect, texto, cor):
    """
    Desenha um botão simples.
    """

    pygame.draw.rect(
        tela,
        cor,
        rect,
        border_radius=6
    )

    texto_superficie = fonte.render(
        texto,
        True,
        BRANCO
    )

    texto_rect = texto_superficie.get_rect(
        center=rect.center
    )

    tela.blit(
        texto_superficie,
        texto_rect
    )


def desenhar_campo(rect, texto, ativo=False):
    """
    Desenha um campo de entrada de texto.
    """

    cor_borda = AZUL if ativo else CINZA_ESCURO

    pygame.draw.rect(
        tela,
        BRANCO,
        rect
    )

    pygame.draw.rect(
        tela,
        cor_borda,
        rect,
        2
    )

    desenhar_texto(
        texto,
        rect.x + 8,
        rect.y + 8,
        fonte
    )


def desenhar_menu():
    """
    Desenha o menu lateral.
    """

    # Fundo do menu
    pygame.draw.rect(
        tela,
        CINZA,
        (0, 0, LARGURA_MENU, ALTURA)
    )

    # Separação entre menu e área de desenho
    pygame.draw.line(
        tela,
        CINZA_ESCURO,
        (LARGURA_MENU, 0),
        (LARGURA_MENU, ALTURA),
        2
    )

    # Título
    desenhar_texto(
        "MENU DE AÇÕES",
        20,
        20,
        fonte_titulo
    )

    # Botão resetar
    desenhar_botao(
        botao_resetar,
        "RESETAR",
        VERMELHO
    )

    # -------------------------
    # Inserção de pontos
    # -------------------------

    desenhar_texto(
        "INSERIR PONTO",
        20,
        115,
        fonte_titulo
    )

    desenhar_texto(
        "X:",
        20,
        160,
        fonte_pequena
    )

    desenhar_texto(
        "Y:",
        130,
        160,
        fonte_pequena
    )

    desenhar_campo(
        campo_x_rect,
        campo_x,
        campo_ativo == "x"
    )

    desenhar_campo(
        campo_y_rect,
        campo_y,
        campo_ativo == "y"
    )

    desenhar_botao(
        botao_adicionar,
        "ADICIONAR PONTO",
        AZUL_ESCURO
    )

    # -------------------------
    # Informações dos pontos
    # -------------------------

    desenhar_texto(
        "PONTOS:",
        20,
        270,
        fonte_titulo
    )

    y_texto = 305

    for i, ponto in enumerate(pontos_selecionados):

        desenhar_texto(
            f"P{i + 1}: ({ponto.x:.0f}, {ponto.y:.0f})",
            20,
            y_texto,
            fonte_pequena
        )

        y_texto += 25

    # -------------------------
    # Transformações
    # -------------------------

    desenhar_texto(
        "TRANSFORMAÇÕES",
        20,
        425,
        fonte_titulo
    )

    desenhar_texto(
        "Escala: será adicionada",
        20,
        460,
        fonte_pequena,
        CINZA_ESCURO
    )

    desenhar_texto(
        "Rotação: será adicionada",
        20,
        485,
        fonte_pequena,
        CINZA_ESCURO
    )


def desenhar_pontos_selecionados():
    """
    Desenha os pontos que ainda estão sendo selecionados.
    """

    for i, ponto in enumerate(pontos_selecionados):

        x, y = sistema.para_tela(
            ponto.x,
            ponto.y
        )

        # Só desenha se estiver na área de rasterização
        if x >= LARGURA_MENU:

            pygame.draw.circle(
                tela,
                VERMELHO,
                (x, y),
                5
            )

            desenhar_texto(
                f"P{i + 1}",
                x + 8,
                y - 10,
                fonte_pequena,
                VERMELHO
            )


# ============================================================
# LOOP PRINCIPAL
# ============================================================

rodando = True

while rodando:

    for evento in pygame.event.get():

        # ----------------------------------------------------
        # FECHAR
        # ----------------------------------------------------

        if evento.type == pygame.QUIT:
            rodando = False


        # ----------------------------------------------------
        # CLIQUE DO MOUSE
        # ----------------------------------------------------

        if evento.type == pygame.MOUSEBUTTONDOWN:

            x_mouse, y_mouse = evento.pos


            # -----------------------------------------------
            # MENU
            # -----------------------------------------------

            if x_mouse < LARGURA_MENU:

                # Resetar
                if botao_resetar.collidepoint(
                    x_mouse,
                    y_mouse
                ):
                    resetar()


                # Campo X
                elif campo_x_rect.collidepoint(
                    x_mouse,
                    y_mouse
                ):
                    campo_ativo = "x"


                # Campo Y
                elif campo_y_rect.collidepoint(
                    x_mouse,
                    y_mouse
                ):
                    campo_ativo = "y"


                # Adicionar ponto
                elif botao_adicionar.collidepoint(
                    x_mouse,
                    y_mouse
                ):

                    try:

                        x = float(campo_x)
                        y = float(campo_y)

                        adicionar_ponto(x, y)

                        campo_x = ""
                        campo_y = ""
                        campo_ativo = None

                    except ValueError:

                        print(
                            "Digite valores numéricos."
                        )


            # -----------------------------------------------
            # ÁREA DE RASTERIZAÇÃO
            # -----------------------------------------------

            else:

                if len(pontos_selecionados) < 4:

                    x, y = sistema.para_cartesiana(
                        x_mouse,
                        y_mouse
                    )

                    adicionar_ponto(x, y)


        # ----------------------------------------------------
        # TECLADO
        # ----------------------------------------------------

        if evento.type == pygame.KEYDOWN:

            # Campo X
            if campo_ativo == "x":

                if evento.key == pygame.K_BACKSPACE:

                    campo_x = campo_x[:-1]

                elif evento.key == pygame.K_RETURN:

                    campo_ativo = "y"

                else:

                    if evento.unicode.isdigit() or evento.unicode in ".-":

                        campo_x += evento.unicode


            # Campo Y
            elif campo_ativo == "y":

                if evento.key == pygame.K_BACKSPACE:

                    campo_y = campo_y[:-1]

                elif evento.key == pygame.K_RETURN:

                    campo_ativo = None

                else:

                    if evento.unicode.isdigit() or evento.unicode in ".-":

                        campo_y += evento.unicode


    # ========================================================
    # DESENHO
    # ========================================================

    tela.fill(BRANCO)

    # Menu
    desenhar_menu()

    # Pontos selecionados
    desenhar_pontos_selecionados()


    # ========================================================
    # QUADRILÁTERO
    # ========================================================

    if quadrilatero is not None:

        # Preenchimento
        rasterizador.preencher_quadrilatero(
            tela,
            quadrilatero,
            AZUL
        )

        # Bordas
        rasterizador.desenhar_quadrilatero(
            tela,
            quadrilatero,
            PRETO
        )


    pygame.display.flip()


pygame.quit()