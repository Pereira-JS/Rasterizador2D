class SistemaCoordenadas:

    def __init__(self, largura, altura, escala=2):
        self.largura = largura
        self.altura = altura
        self.escala = escala

    def para_tela(self, x, y):

        tela_x = int(x * self.escala)
        tela_y = int(y * self.escala)

        return tela_x, tela_y

    def para_cartesiana(self, x, y):

        x = x / self.escala
        y = y / self.escala

        return x, y