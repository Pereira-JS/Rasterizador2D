from algoritmos.bresenham import bresenham

class Rasterizador:
    def desenhar_linha(self, tela, p1, p2):   
        pontos = bresenham(p1, p2)
        
        for x, y in pontos:
            tela.set_at((x, y), (255, 0, 0))
    
    def desenhar_quadrilatero(self, tela, quadrilatero):
        
        pontos = quadrilatero.pontos
        self.desenhar_linha(tela, pontos[0], pontos[1])
        self.desenhar_linha(tela, pontos[1], pontos[2])
        self.desenhar_linha(tela, pontos[2], pontos[3])
        self.desenhar_linha(tela, pontos[3], pontos[0])
    