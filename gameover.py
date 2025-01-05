import pygame
import sys

from menu import Menu
from highscore import Highscore


class GameOver:
    def __init__(self, screen, score, controlador):
        self.screen = screen
        self.score = score
        self.controlador = controlador
        self.highscore_manager = Highscore()
        self.font = pygame.font.Font(None, 55)
        self.gameover_text = pygame.image.load('assets/gameover2_text.png')
        self.botao_menu = pygame.image.load('assets/botao_menu.png')
        self.botao_sair = pygame.image.load('assets/botao_sair.png')
        self.highscore_asset = pygame.image.load('assets/highscore2.png')
        self.sua_score_texto = pygame.image.load('assets/sua_pontuacao_texto.png')
        self.highscore_manager.update_highscore(self.score)

    def draw_score(self):
        score_text = self.font.render(f'{self.highscore_manager.highscore}', True, (255, 255, 255))
        highscore_text = self.font.render(f'{self.score}', True, (255, 255, 255))
        self.screen.blit(self.highscore_asset, (400, 400))
        self.screen.blit(score_text, (700, 405))
        self.screen.blit(self.sua_score_texto, (400, 500))
        self.screen.blit(highscore_text, (700, 500))

    def run(self):
        pygame.mixer.music.load('assets/gameover.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if self.botao_menu.get_rect(topleft=(300, 270)).collidepoint(x, y):
                        pygame.mixer.music.load('assets/menu.mp3')
                        pygame.mixer.music.set_volume(0.2)
                        pygame.mixer.music.play(-1)
                        Menu(self.screen).main()
                        return True
                    elif self.botao_sair.get_rect(topleft=(710, 270)).collidepoint(x, y):
                        sys.exit()

            self.screen.fill((4, 3, 45))
            self.screen.blit(self.gameover_text, (300, 80))
            self.screen.blit(self.botao_menu, (300, 270))
            self.screen.blit(self.botao_sair, (710, 270))
            self.draw_score()
            pygame.display.flip()
