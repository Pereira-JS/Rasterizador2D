def bresenham(p1, p2):

    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y

    pontos = []

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    erro = dx - dy

    while True:

        pontos.append((x1, y1))

        if x1 == x2 and y1 == y2:
            break

        erro2 = 2 * erro

        if erro2 > -dy:
            erro -= dy
            x1 += sx

        if erro2 < dx:
            erro += dx
            y1 += sy

    return pontos