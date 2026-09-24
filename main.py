import pygame

from modelos.ponto import Ponto
from modelos.quadrilatero import Quadrilatero
from modelos.sistema_coordenadas import SistemaCoordenadas

from algoritmos.rasterizador import Rasterizador

from modelos.validacao import quadrilatero_valido

from transformacoes.transformacoes import Transformacoes


pygame.init()


# ============================================================
# CONFIGURAÇÕES DA TELA
# ============================================================

LARGURA = 1000
ALTURA = 600

LARGURA_MENU = 280

ESCALA = 2

tela = pygame.display.set_mode(
    (LARGURA, ALTURA)
)

pygame.display.set_caption(
    "Rasterizador 2D"
)


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


# ============================================================
# FONTES
# ============================================================

fonte_titulo = pygame.font.Font(
    None,
    30
)

fonte = pygame.font.Font(
    None,
    24
)

fonte_pequena = pygame.font.Font(
    None,
    20
)


# ============================================================
# SISTEMA
# ============================================================

sistema = SistemaCoordenadas(
    LARGURA,
    ALTURA,
    ESCALA
)

rasterizador = Rasterizador(
    sistema
)


# ============================================================
# ESTADO DO PROGRAMA
# ============================================================

pontos_selecionados = []

# Quadrilátero original
quadrilatero_original = None

# Quadrilátero atualmente exibido
quadrilatero = None


# ============================================================
# CAMPOS DE TEXTO
# ============================================================

campo_x = ""
campo_y = ""

campo_sx = "1"
campo_sy = "1"

campo_ativo = None


# ============================================================
# ÁREAS DOS COMPONENTES
# ============================================================

# Reset

botao_resetar = pygame.Rect(
    20,
    60,
    240,
    40
)


# Inserção de pontos

campo_x_rect = pygame.Rect(
    20,
    150,
    105,
    35
)

campo_y_rect = pygame.Rect(
    140,
    150,
    120,
    35
)

botao_adicionar = pygame.Rect(
    20,
    200,
    240,
    40
)


# Escala

campo_sx_rect = pygame.Rect(
    20,
    525,
    105,
    35
)

campo_sy_rect = pygame.Rect(
    140,
    525,
    120,
    35
)

botao_escala = pygame.Rect(
    20,
    570,
    240,
    40
)


# ============================================================
# FUNÇÕES
# ============================================================

def resetar():
    """
    Limpa os pontos e os quadriláteros.
    """

    global quadrilatero_original
    global quadrilatero

    global campo_x
    global campo_y

    pontos_selecionados.clear()

    quadrilatero_original = None
    quadrilatero = None

    campo_x = ""
    campo_y = ""


def adicionar_ponto(x, y):
    """
    Adiciona um ponto.

    Ao chegar em quatro pontos,
    cria o quadrilátero caso seja válido.
    """

    global quadrilatero_original
    global quadrilatero

    if len(pontos_selecionados) >= 4:
        return

    ponto = Ponto(
        x,
        y
    )

    pontos_selecionados.append(
        ponto
    )

    print(
        f"P{len(pontos_selecionados)}: "
        f"({x}, {y})"
    )

    if len(pontos_selecionados) == 4:

        if quadrilatero_valido(
            pontos_selecionados
        ):

            quadrilatero_original = Quadrilatero(
                pontos_selecionados.copy()
            )

            quadrilatero = Quadrilatero(
                pontos_selecionados.copy()
            )

            print(
                "Quadrilátero válido criado!"
            )

        else:

            print(
                "Quadrilátero inválido!"
            )

            pontos_selecionados.clear()


def aplicar_escala():
    """
    Aplica a escala usando os fatores SX e SY.

    A transformação sempre utiliza
    o quadrilátero original.
    """

    global quadrilatero

    if quadrilatero_original is None:

        print(
            "Nenhum quadrilátero criado."
        )

        return

    try:

        sx = float(campo_sx)
        sy = float(campo_sy)

        quadrilatero = Transformacoes.escalar(
            quadrilatero_original,
            sx,
            sy
        )

        print(
            f"Escala aplicada: "
            f"sx={sx}, sy={sy}"
        )

    except ValueError:

        print(
            "Digite valores numéricos "
            "para SX e SY."
        )


def desenhar_texto(
    texto,
    x,
    y,
    fonte_usada,
    cor=PRETO
):
    """
    Desenha um texto na tela.
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


def desenhar_botao(
    rect,
    texto,
    cor
):
    """
    Desenha um botão.
    """

    pygame.draw.rect(
        tela,
        cor,
        rect,
        border_radius=6
    )

    superficie = fonte.render(
        texto,
        True,
        BRANCO
    )

    texto_rect = superficie.get_rect(
        center=rect.center
    )

    tela.blit(
        superficie,
        texto_rect
    )


def desenhar_campo(
    rect,
    texto,
    ativo=False
):
    """
    Desenha um campo de entrada.
    """

    cor_borda = (
        AZUL
        if ativo
        else CINZA_ESCURO
    )

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

    # ========================================================
    # FUNDO
    # ========================================================

    pygame.draw.rect(
        tela,
        CINZA,
        (
            0,
            0,
            LARGURA_MENU,
            ALTURA
        )
    )

    # Separador do menu
    pygame.draw.line(
        tela,
        CINZA_ESCURO,
        (LARGURA_MENU, 0),
        (LARGURA_MENU, ALTURA),
        2
    )


    # ========================================================
    # TÍTULO
    # ========================================================

    desenhar_texto(
        "MENU DE AÇÕES",
        20,
        20,
        fonte_titulo
    )


    # ========================================================
    # RESET
    # ========================================================

    desenhar_botao(
        botao_resetar,
        "RESETAR",
        VERMELHO
    )


    # ========================================================
    # INSERÇÃO DE PONTOS
    # ========================================================

    desenhar_texto(
        "INSERIR PONTO",
        20,
        115,
        fonte_titulo
    )

    desenhar_texto(
        "X",
        20,
        130,
        fonte_pequena
    )

    desenhar_texto(
        "Y",
        140,
        130,
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


    # ========================================================
    # PONTOS
    # ========================================================

    desenhar_texto(
        "PONTOS:",
        20,
        270,
        fonte_titulo
    )

    y_texto = 305

    for i, ponto in enumerate(
        pontos_selecionados
    ):

        desenhar_texto(
            f"P{i + 1}: "
            f"({ponto.x:.0f}, {ponto.y:.0f})",
            20,
            y_texto,
            fonte_pequena
        )

        y_texto += 25


    # ========================================================
    # ESCALA
    # ========================================================

    desenhar_texto(
        "ESCALA",
        20,
        425,
        fonte_titulo
    )

    desenhar_texto(
        "SX",
        20,
        465,
        fonte_pequena
    )

    desenhar_texto(
        "SY",
        140,
        465,
        fonte_pequena
    )

    desenhar_campo(
        campo_sx_rect,
        campo_sx,
        campo_ativo == "sx"
    )

    desenhar_campo(
        campo_sy_rect,
        campo_sy,
        campo_ativo == "sy"
    )

    desenhar_botao(
        botao_escala,
        "APLICAR ESCALA",
        AZUL_ESCURO
    )


def desenhar_pontos_selecionados():
    """
    Desenha os pontos inseridos pelo usuário.
    """

    for i, ponto in enumerate(
        pontos_selecionados
    ):

        x, y = sistema.para_tela(
            ponto.x,
            ponto.y
        )

        # Não desenhar dentro do menu
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

        # ====================================================
        # FECHAR
        # ====================================================

        if evento.type == pygame.QUIT:

            rodando = False


        # ====================================================
        # CLIQUE DO MOUSE
        # ====================================================

        if evento.type == pygame.MOUSEBUTTONDOWN:

            x_mouse, y_mouse = evento.pos


            # =================================================
            # MENU
            # =================================================

            if x_mouse < LARGURA_MENU:


                # ---------------------------------------------
                # RESET
                # ---------------------------------------------

                if botao_resetar.collidepoint(
                    x_mouse,
                    y_mouse
                ):

                    resetar()


                # ---------------------------------------------
                # CAMPO X
                # ---------------------------------------------

                elif campo_x_rect.collidepoint(
                    x_mouse,
                    y_mouse
                ):

                    campo_ativo = "x"


                # ---------------------------------------------
                # CAMPO Y
                # ---------------------------------------------

                elif campo_y_rect.collidepoint(
                    x_mouse,
                    y_mouse
                ):

                    campo_ativo = "y"


                # ---------------------------------------------
                # ADICIONAR PONTO
                # ---------------------------------------------

                elif botao_adicionar.collidepoint(
                    x_mouse,
                    y_mouse
                ):

                    try:

                        x = float(
                            campo_x
                        )

                        y = float(
                            campo_y
                        )

                        adicionar_ponto(
                            x,
                            y
                        )

                        campo_x = ""
                        campo_y = ""

                        campo_ativo = None

                    except ValueError:

                        print(
                            "Digite valores "
                            "numéricos."
                        )


                # ---------------------------------------------
                # CAMPO SX
                # ---------------------------------------------

                elif campo_sx_rect.collidepoint(
                    x_mouse,
                    y_mouse
                ):

                    campo_ativo = "sx"


                # ---------------------------------------------
                # CAMPO SY
                # ---------------------------------------------

                elif campo_sy_rect.collidepoint(
                    x_mouse,
                    y_mouse
                ):

                    campo_ativo = "sy"


                # ---------------------------------------------
                # APLICAR ESCALA
                # ---------------------------------------------

                elif botao_escala.collidepoint(
                    x_mouse,
                    y_mouse
                ):

                    aplicar_escala()


            # =================================================
            # ÁREA DE RASTERIZAÇÃO
            # =================================================

            else:

                if len(pontos_selecionados) < 4:

                    x, y = sistema.para_cartesiana(
                        x_mouse,
                        y_mouse
                    )

                    adicionar_ponto(
                        x,
                        y
                    )


        # ====================================================
        # TECLADO
        # ====================================================

        if evento.type == pygame.KEYDOWN:


            # =================================================
            # CAMPO X
            # =================================================

            if campo_ativo == "x":

                if evento.key == pygame.K_BACKSPACE:

                    campo_x = campo_x[:-1]

                elif evento.key == pygame.K_RETURN:

                    campo_ativo = "y"

                elif (
                    evento.unicode.isdigit()
                    or evento.unicode in ".-"
                ):

                    campo_x += evento.unicode


            # =================================================
            # CAMPO Y
            # =================================================

            elif campo_ativo == "y":

                if evento.key == pygame.K_BACKSPACE:

                    campo_y = campo_y[:-1]

                elif evento.key == pygame.K_RETURN:

                    campo_ativo = None

                elif (
                    evento.unicode.isdigit()
                    or evento.unicode in ".-"
                ):

                    campo_y += evento.unicode


            # =================================================
            # CAMPO SX
            # =================================================

            elif campo_ativo == "sx":

                if evento.key == pygame.K_BACKSPACE:

                    campo_sx = campo_sx[:-1]

                elif evento.key == pygame.K_RETURN:

                    campo_ativo = None

                elif (
                    evento.unicode.isdigit()
                    or evento.unicode == "."
                ):

                    campo_sx += evento.unicode


            # =================================================
            # CAMPO SY
            # =================================================

            elif campo_ativo == "sy":

                if evento.key == pygame.K_BACKSPACE:

                    campo_sy = campo_sy[:-1]

                elif evento.key == pygame.K_RETURN:

                    campo_ativo = None

                elif (
                    evento.unicode.isdigit()
                    or evento.unicode == "."
                ):

                    campo_sy += evento.unicode


    # ========================================================
    # DESENHO
    # ========================================================

    tela.fill(BRANCO)

    desenhar_menu()

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


    # ========================================================
    # ATUALIZA A TELA
    # ========================================================

    pygame.display.flip()


pygame.quit()