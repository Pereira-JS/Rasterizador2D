def preencher_scanline(tela, quadrilatero, cor):
    pontos = quadrilatero.pontos

    # Encontra os limites verticais do quadrilátero
    y_min = min(p.y for p in pontos)
    y_max = max(p.y for p in pontos)

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

            for x in range(x_inicio, x_fim + 1):
                tela.set_at((x, y), cor)