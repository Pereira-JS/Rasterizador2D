def preencher_scanline(
    tela,
    quadrilatero,
    cor,
    limite_esquerdo=None,
    limite_direito=None,
    limite_superior=None,
    limite_inferior=None,
    alpha=255,
):
    """
    limite_esquerdo/direito/superior/inferior (opcionais) restringem
    a área onde os pixels podem ser pintados - usados para impedir
    que o preenchimento invada o menu lateral ou saia da janela.

    alpha (0 a 255) controla a opacidade do preenchimento: 255 é
    totalmente opaco (cor pura); valores menores misturam a cor
    com o que já está desenhado na tela (opacidade/transparência).
    """

    pontos = quadrilatero.pontos

    # Encontra os limites verticais do quadrilátero
    y_min = min(p.y for p in pontos)
    y_max = max(p.y for p in pontos)

    if limite_superior is not None:
        y_min = max(y_min, limite_superior)

    if limite_inferior is not None:
        y_max = min(y_max, limite_inferior - 1)

    # Percorre cada linha horizontal
    for y in range(y_min, y_max + 1):

        intersecoes = []

        # Percorre as 4 arestas
        for i in range(4):
            p1 = pontos[i]
            p2 = pontos[(i + 1) % 4]

            # Ignora arestas horizontais
            if p1.y == p2.y:
                continue

            # Verifica se a linha Y cruza a aresta
            if min(p1.y, p2.y) <= y < max(p1.y, p2.y):

                # Calcula a posição X da interseção
                x = p1.x + (y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y)

                intersecoes.append(int(x))

        # Ordena as interseções
        intersecoes.sort()

        # Preenche entre os pares de interseções
        for i in range(0, len(intersecoes), 2):

            if i + 1 >= len(intersecoes):
                break

            x_inicio = intersecoes[i]
            x_fim = intersecoes[i + 1]

            if limite_esquerdo is not None:
                x_inicio = max(x_inicio, limite_esquerdo)

            if limite_direito is not None:
                x_fim = min(x_fim, limite_direito - 1)

            for x in range(x_inicio, x_fim + 1):

                if alpha >= 255:

                    tela.set_at((x, y), cor)

                else:

                    fundo = tela.get_at((x, y))

                    a = alpha / 255

                    cor_final = (
                        int(cor[0] * a + fundo[0] * (1 - a)),
                        int(cor[1] * a + fundo[1] * (1 - a)),
                        int(cor[2] * a + fundo[2] * (1 - a)),
                    )

                    tela.set_at((x, y), cor_final)