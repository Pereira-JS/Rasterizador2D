def pontos_coincidentes(p1, p2, p3, p4):
    pontos = [p1, p2, p3, p4]

    for i in range(4):
        for j in range(i + 1, 4):

            if (
                pontos[i].x == pontos[j].x
                and pontos[i].y == pontos[j].y
            ):
                return True

    return False


def pontos_colineares(p1, p2, p3):
    """
    Verifica se três pontos estão na mesma reta.
    """

    area = (
        p1.x * (p2.y - p3.y)
        + p2.x * (p3.y - p1.y)
        + p3.x * (p1.y - p2.y)
    )

    return area == 0


def quadrilatero_valido(pontos):

    if len(pontos) != 4:
        return False

    p1, p2, p3, p4 = pontos

    # Pontos repetidos
    if pontos_coincidentes(p1, p2, p3, p4):
        return False

    # Três pontos consecutivos colineares
    if pontos_colineares(p1, p2, p3):
        return False

    if pontos_colineares(p2, p3, p4):
        return False

    if pontos_colineares(p3, p4, p1):
        return False

    if pontos_colineares(p4, p1, p2):
        return False

    return True