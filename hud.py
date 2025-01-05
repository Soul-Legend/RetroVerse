import pygame


class Hud:
    def __init__(self):
        self.font = pygame.font.SysFont('bahnschrift', 35)

        self.vida_icon = pygame.image.load('assets/vida.png')  # icone de vida
        self.vidas_text = pygame.image.load('assets/vidas_texto.png')  # texto "Vidas:"

        self.troca_mundo_texto = pygame.image.load('assets/troca_de_mundo_texto.png')  # texto "troca de mundo:"

        self.tempo_texto_icon = pygame.image.load('assets/tempo_texto.png')
        self.tempo_icon = pygame.image.load('assets/relogio1.5.png')

        self.score_texto = pygame.image.load('assets/score_texto.png')
        self.trofeu = pygame.image.load('assets/trofeu.png')

        self.barra_vertical_icon = pygame.image.load('assets/linha_vertical.png')
        self.barra_horizontal_icon = pygame.image.load('assets/linha_horizontal.png')

    def draw(self, screen, vidas, tempo_troca_de_fase, tempo_na_fase, tempo, score):
        screen.blit(self.barra_horizontal_icon, (0, 62))

        # Desenhar o número de vidas
        screen.blit(self.vidas_text, (10, 20))
        for i in range(vidas):
            screen.blit(self.vida_icon, (120 + i * (self.vida_icon.get_width() + 10), 15))
        screen.blit(self.barra_vertical_icon, (280, 0))

        # Desenhar o tempo restante para a troca de mundo
        screen.blit(self.tempo_icon, (300, 10))
        screen.blit(self.troca_mundo_texto, (350, 20))
        tempo_troca_mundo = round(tempo_troca_de_fase - tempo_na_fase) +1
        tempo_troca_text = self.font.render(str(tempo_troca_mundo), True, (0, 0, 0))
        screen.blit(tempo_troca_text, (610, 18))
        screen.blit(self.barra_vertical_icon, (660, 0))

        # Desenhar o tempo total decorrido
        screen.blit(self.tempo_texto_icon, (680, 20))
        tempo_total_text = self.font.render(str(round(tempo)), True, (0, 0, 0))
        screen.blit(tempo_total_text, (800, 18))
        screen.blit(self.barra_vertical_icon, (920, 0))

        # Desenhar a pontuação
        screen.blit(self.trofeu, (930, 10))
        screen.blit(self.score_texto, (980, 20))
        score_text = self.font.render(str(score), True, (0, 0, 0))
        screen.blit(score_text, (1090, 18))

        pygame.display.flip()

    def update(self):
        pass
