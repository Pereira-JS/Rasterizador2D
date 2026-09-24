import pygame

from modelos.ponto import Ponto
from modelos.quadrilatero import Quadrilatero
from modelos.sistema_coordenadas import SistemaCoordenadas

from algoritmos.rasterizador import Rasterizador

from modelos.validacao import quadrilatero_degenerado

from transformacoes.transformacoes import Transformacoes


pygame.init()


# ============================================================
# CONFIGURAÇÕES DA TELA
# ============================================================

LARGURA = 1000
ALTURA = 860

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

LARANJA = (240, 140, 30)
VERDE_ESCURO = (40, 130, 90)

# Opacidade do segundo polígono (transformado): 75%
OPACIDADE_TRANSFORMADO = round(0.75 * 255)

CINZA_GRADE = (225, 225, 225)
CINZA_EIXO = (140, 140, 140)


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
    ESCALA,
    offset_x=LARGURA_MENU
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

campo_angulo = "0"

campo_ativo = None

# Pivô usado tanto pela escala quanto pela rotação
pivot_selecionado = "origem"

# Mensagem de erro/validação exibida no menu (ex.: quadrilátero
# inválido ao inserir o 4º ponto, ou valores numéricos inválidos)
mensagem_erro = ""

# Indica se alguma transformação (escala ou rotação) já foi
# aplicada sobre o quadrilátero original - usado para saber se
# o polígono transformado deve ser desenhado junto do original
houve_transformacao = False


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


# Pivô da transformação (origem ou centroide)

botao_pivot_origem = pygame.Rect(
    20,
    465,
    115,
    35
)

botao_pivot_centroide = pygame.Rect(
    145,
    465,
    115,
    35
)


# Escala

campo_sx_rect = pygame.Rect(
    20,
    580,
    105,
    35
)

campo_sy_rect = pygame.Rect(
    140,
    580,
    120,
    35
)


# Rotação

campo_angulo_rect = pygame.Rect(
    20,
    700,
    240,
    35
)

botao_transformar = pygame.Rect(
    20,
    745,
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

    global mensagem_erro
    global houve_transformacao

    pontos_selecionados.clear()

    quadrilatero_original = None
    quadrilatero = None

    campo_x = ""
    campo_y = ""

    mensagem_erro = ""
    houve_transformacao = False


def adicionar_ponto(x, y):
    """
    Adiciona um ponto.

    Ao chegar em quatro pontos,
    cria o quadrilátero caso seja válido.
    """

    global quadrilatero_original
    global quadrilatero
    global mensagem_erro
    global houve_transformacao

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

        # Um quadrilátero inválido (pontos coincidentes, três
        # vértices consecutivos alinhados, ou arestas opostas que
        # se cruzam) NÃO pode ser criado. Rejeita apenas o último
        # ponto informado, para que o usuário tente novamente sem
        # perder P1, P2 e P3.

        if quadrilatero_degenerado(pontos_selecionados):

            pontos_selecionados.pop()

            mensagem_erro = (
                "Ponto inválido (pontos coincidentes, "
                "alinhados ou arestas cruzadas). "
                "Informe o 4º ponto novamente."
            )

            print(
                "Quadrilátero inválido - ponto rejeitado."
            )

            return

        mensagem_erro = ""
        houve_transformacao = False

        quadrilatero_original = Quadrilatero(
            pontos_selecionados.copy()
        )

        quadrilatero = Quadrilatero(
            pontos_selecionados.copy()
        )

        print(
            "Quadrilátero válido criado!"
        )


def selecionar_pivot(pivot):
    """
    Define o pivô (origem ou centroide) usado tanto pela
    escala quanto pela rotação.
    """

    global pivot_selecionado

    pivot_selecionado = pivot

    print(
        f"Pivô selecionado: {pivot}"
    )


def aplicar_transformacao():
    """
    Aplica escala E rotação ao mesmo tempo, num único passo,
    sempre a partir do quadrilátero ORIGINAL: primeiro escala
    (SX, SY) e depois rotaciona o resultado (ÂNGULO), usando o
    pivô selecionado.
    """

    global quadrilatero
    global houve_transformacao

    if quadrilatero_original is None:

        print(
            "Nenhum quadrilátero criado."
        )

        return

    try:

        sx = float(campo_sx)
        sy = float(campo_sy)
        angulo = float(campo_angulo)

    except ValueError:

        print(
            "Digite valores numéricos "
            "para SX, SY e ângulo."
        )

        return

    escalado = Transformacoes.escalar(
        quadrilatero_original,
        sx,
        sy,
        pivot=pivot_selecionado
    )

    quadrilatero = Transformacoes.rotacionar(
        escalado,
        angulo,
        pivot=pivot_selecionado
    )

    houve_transformacao = True

    print(
        f"Transformação aplicada: "
        f"sx={sx}, sy={sy}, "
        f"ângulo={angulo}°, "
        f"pivô={pivot_selecionado}"
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

    if mensagem_erro:

        desenhar_texto(
            "Ponto inválido, tente de novo",
            20,
            405,
            fonte_pequena,
            VERMELHO
        )

    # ========================================================
    # PIVÔ DA TRANSFORMAÇÃO
    # ========================================================

    desenhar_texto(
        "PIVÔ (ESCALA E ROTAÇÃO)",
        20,
        425,
        fonte_titulo
    )

    desenhar_botao(
        botao_pivot_origem,
        "ORIGEM",
        AZUL_ESCURO if pivot_selecionado == "origem" else CINZA_ESCURO
    )

    desenhar_botao(
        botao_pivot_centroide,
        "CENTROIDE",
        AZUL_ESCURO if pivot_selecionado == "centroide" else CINZA_ESCURO
    )


    # ========================================================
    # ESCALA
    # ========================================================

    desenhar_texto(
        "ESCALA",
        20,
        520,
        fonte_titulo
    )

    desenhar_texto(
        "SX",
        20,
        560,
        fonte_pequena
    )

    desenhar_texto(
        "SY",
        140,
        560,
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


    # ========================================================
    # ROTAÇÃO
    # ========================================================

    desenhar_texto(
        "ROTAÇÃO",
        20,
        640,
        fonte_titulo
    )

    desenhar_texto(
        "ÂNGULO (GRAUS)",
        20,
        680,
        fonte_pequena
    )

    desenhar_campo(
        campo_angulo_rect,
        campo_angulo,
        campo_ativo == "angulo"
    )

    desenhar_botao(
        botao_transformar,
        "TRANSFORMAR",
        AZUL_ESCURO
    )


def desenhar_plano_cartesiano():
    """
    Desenha um plano cartesiano (grade + eixos + coordenadas)
    como fundo da área de desenho, sem invadir o menu lateral.
    """

    espacamento = 50  # distância em pixels de tela entre linhas

    # ---- Linhas verticais (valores de X) ----
    x = LARGURA_MENU

    while x <= LARGURA:

        no_eixo = (x == LARGURA_MENU)

        pygame.draw.line(
            tela,
            CINZA_EIXO if no_eixo else CINZA_GRADE,
            (x, 0),
            (x, ALTURA),
            2 if no_eixo else 1
        )

        if not no_eixo and (x - LARGURA_MENU) % 100 == 0:

            valor_x, _ = sistema.para_cartesiana(x, 0)

            desenhar_texto(
                f"{valor_x:.0f}",
                x + 2,
                2,
                fonte_pequena,
                CINZA_EIXO
            )

        x += espacamento

    # ---- Linhas horizontais (valores de Y) ----
    y = 0

    while y <= ALTURA:

        no_eixo = (y == 0)

        pygame.draw.line(
            tela,
            CINZA_EIXO if no_eixo else CINZA_GRADE,
            (LARGURA_MENU, y),
            (LARGURA, y),
            2 if no_eixo else 1
        )

        if not no_eixo and y % 100 == 0:

            _, valor_y = sistema.para_cartesiana(LARGURA_MENU, y)

            desenhar_texto(
                f"{valor_y:.0f}",
                LARGURA_MENU + 4,
                y + 2,
                fonte_pequena,
                CINZA_EIXO
            )

        y += espacamento

    # ---- Origem ----
    desenhar_texto(
        "0",
        LARGURA_MENU + 4,
        4,
        fonte_pequena,
        CINZA_EIXO
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


def desenhar_vertices_quadrilatero(quad, cor, com_apostrofo=False):
    """
    Desenha um pequeno marcador e o rótulo (Pn ou Pn') em cada
    vértice do quadrilátero informado, sem invadir o menu lateral.
    """

    for i, ponto in enumerate(quad.pontos):

        x, y = sistema.para_tela(
            ponto.x,
            ponto.y
        )

        if x >= LARGURA_MENU:

            pygame.draw.circle(
                tela,
                cor,
                (x, y),
                4
            )

            rotulo = f"P{i + 1}'" if com_apostrofo else f"P{i + 1}"

            desenhar_texto(
                rotulo,
                x + 8,
                y - 10,
                fonte_pequena,
                cor
            )


def desenhar_legenda_poligonos():
    """
    Desenha, no canto superior direito da área de desenho, a
    legenda de cores explicando o quadrilátero original e o
    quadrilátero transformado.
    """

    x_legenda = LARGURA - 210
    y_legenda = 10

    pygame.draw.rect(
        tela,
        AZUL,
        (x_legenda, y_legenda, 14, 14)
    )

    desenhar_texto(
        "Original",
        x_legenda + 20,
        y_legenda - 2,
        fonte_pequena,
        PRETO
    )

    pygame.draw.rect(
        tela,
        LARANJA,
        (x_legenda, y_legenda + 22, 14, 14)
    )

    desenhar_texto(
        "Transformado (P')",
        x_legenda + 20,
        y_legenda + 20,
        fonte_pequena,
        PRETO
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
                # PIVÔ: ORIGEM
                # ---------------------------------------------

                elif botao_pivot_origem.collidepoint(
                    x_mouse,
                    y_mouse
                ):

                    selecionar_pivot("origem")


                # ---------------------------------------------
                # PIVÔ: CENTROIDE
                # ---------------------------------------------

                elif botao_pivot_centroide.collidepoint(
                    x_mouse,
                    y_mouse
                ):

                    selecionar_pivot("centroide")


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
                # CAMPO ÂNGULO
                # ---------------------------------------------

                elif campo_angulo_rect.collidepoint(
                    x_mouse,
                    y_mouse
                ):

                    campo_ativo = "angulo"


                # ---------------------------------------------
                # APLICAR TRANSFORMAÇÃO (ESCALA + ROTAÇÃO)
                # ---------------------------------------------

                elif botao_transformar.collidepoint(
                    x_mouse,
                    y_mouse
                ):

                    aplicar_transformacao()


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


            # =================================================
            # CAMPO ÂNGULO
            # =================================================

            elif campo_ativo == "angulo":

                if evento.key == pygame.K_BACKSPACE:

                    campo_angulo = campo_angulo[:-1]

                elif evento.key == pygame.K_RETURN:

                    campo_ativo = None

                elif (
                    evento.unicode.isdigit()
                    or evento.unicode in ".-"
                ):

                    campo_angulo += evento.unicode


    # ========================================================
    # DESENHO
    # ========================================================

    tela.fill(BRANCO)

    desenhar_plano_cartesiano()

    desenhar_menu()

    desenhar_pontos_selecionados()


    # ========================================================
    # QUADRILÁTERO(S)
    # ========================================================
    #
    # O quadrilátero original (criado a partir dos 4 pontos
    # informados) permanece sempre visível. Se alguma
    # transformação (escala/rotação) já foi aplicada, o
    # quadrilátero transformado também é desenhado, com cor e
    # rótulos de vértice (P1', P2', P3', P4') diferentes, para
    # que os dois fiquem visíveis ao mesmo tempo.

    if quadrilatero_original is not None:

        rasterizador.preencher_quadrilatero(
            tela,
            quadrilatero_original,
            AZUL
        )

        rasterizador.desenhar_quadrilatero(
            tela,
            quadrilatero_original,
            PRETO
        )

    if quadrilatero is not None and houve_transformacao:

        rasterizador.preencher_quadrilatero(
            tela,
            quadrilatero,
            LARANJA,
            alpha=OPACIDADE_TRANSFORMADO
        )

        rasterizador.desenhar_quadrilatero(
            tela,
            quadrilatero,
            VERDE_ESCURO,
            alpha=OPACIDADE_TRANSFORMADO
        )

        desenhar_vertices_quadrilatero(
            quadrilatero,
            VERDE_ESCURO,
            com_apostrofo=True
        )

        desenhar_legenda_poligonos()


    # ========================================================
    # ATUALIZA A TELA
    # ========================================================

    pygame.display.flip()


pygame.quit()