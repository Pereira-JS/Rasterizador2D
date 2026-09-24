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


def quadrilatero_degenerado(pontos):
    """
    Indica se o quadrilátero é um caso degenerado: vértices
    coincidentes ou três vértices consecutivos alinhados.

    Importante: um quadrilátero degenerado ainda deve ser aceito
    e desenhado pelo sistema (a especificação exige isso). Esta
    função serve apenas para informar/avisar o usuário sobre o
    caso, nunca para bloquear a criação do quadrilátero.
    """

    if len(pontos) != 4:
        return True

    p1, p2, p3, p4 = pontos

    if pontos_coincidentes(p1, p2, p3, p4):
        return True

    if pontos_colineares(p1, p2, p3):
        return True

    if pontos_colineares(p2, p3, p4):
        return True

    if pontos_colineares(p3, p4, p1):
        return True

    if pontos_colineares(p4, p1, p2):
        return True

    return False


def quadrilatero_valido(pontos):
    """
    Mantido por compatibilidade: um quadrilátero é "válido" no
    sentido estrito (não degenerado) quando tem 4 pontos e nenhum
    caso de coincidência/alinhamento ocorre.

    Não use esta função para decidir se o quadrilátero deve ser
    criado/desenhado - todo quadrilátero de 4 pontos deve ser
    aceito. Use quadrilatero_degenerado() para saber se é preciso
    avisar o usuário sobre um caso degenerado.
    """

    if len(pontos) != 4:
        return False

    return not quadrilatero_degenerado(pontos)