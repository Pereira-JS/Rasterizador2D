class SistemaCoordenadas:

    def __init__(self, largura, altura, escala=2, offset_x=0, offset_y=0):
        self.largura = largura
        self.altura = altura
        self.escala = escala
        self.offset_x = offset_x
        self.offset_y = offset_y

    def para_tela(self, x, y):

        tela_x = int(x * self.escala) + self.offset_x
        tela_y = int(y * self.escala) + self.offset_y

        return tela_x, tela_y

    def para_cartesiana(self, x, y):

        x = (x - self.offset_x) / self.escala
        y = (y - self.offset_y) / self.escala

        return x, y