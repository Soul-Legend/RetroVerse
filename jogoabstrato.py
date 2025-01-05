import pygame
import random
import sys
from sistemas import SistemaDesenho, SistemaMovimento, SistemaPlataformas


class JogoAbstrato:
    def __init__(self, screen, entidades, player, inimigos=[], plataformas=[]):
        self.trocar_player(player)
        self.clock = pygame.time.Clock()
        self.start_ticks = pygame.time.get_ticks()
        self.screen = screen
        self.entidades = []
        self.sistemas = []
        self.score = 0

        self.entidades = entidades
        self.inimigos = inimigos
        self.plataformas = plataformas
        for _ in range(5):
            self.inicializar_entidades()
        self.inicializar_sistemas()

    def rodar_sistemas(self):
        for sistema in self.sistemas:
            sistema.tick()
        list_removed = self.inimigos_sys.check_removed()
        for removed in list_removed:
            self.score += 100
            self.inimigos_sys.clear_removed()
            self.inicializar_entidades()

    def gen_inimigo_coords(self):
        for _ in range(1000):
            x_novo = random.randint(0, 1150)
            y_novo = random.randint(65, 500)
            if not any(abs(x_novo - inimigo.rect.x) < 55 and abs(y_novo - inimigo.rect.y) < 55 for inimigo in self.inimigos)\
                and not abs(x_novo - self.player.rect.x) < 150 and not abs(y_novo - self.player.rect.y) < 150:
                break
        return (x_novo, y_novo)

    def inicializar_entidades(self):

        for inimigo in self.inimigos:
            x, y = inimigo.get_coords()
            conversao = self.inimigo(x, y)
            self.inimigos.remove(inimigo)
            self.inimigos.append(conversao)

        for _ in range(5 - len(self.inimigos)):
            x, y = self.gen_inimigo_coords()
            self.inimigos.append(self.inimigo(x, y))

        self.entidades.append(self.player)

        for inimigo in self.inimigos:
            self.entidades.append(inimigo)
        for plataforma in self.plataformas:
            self.entidades.append(plataforma)

    def inicializar_sistemas(self, sistemas_desenho=False):
        plataformas = SistemaPlataformas(self.plataformas)
        self.sistemas.append(plataformas)

        if (sistemas_desenho):
            desenho = SistemaDesenho([self.inimigos_sys, *sistemas_desenho], self.player, self.screen)
        else:
            desenho = SistemaDesenho([self.inimigos_sys], self.player, self.screen)
        self.sistemas.append(desenho)

        movimento = SistemaMovimento([self.inimigos_sys], self.player, plataformas)
        self.sistemas.append(movimento)

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.rodar_sistemas()

        self.clock.tick(90)

    def set_lives(self, lives):
        self.player.lives = lives

    def get_lives(self):
        return self.player.lives

    def get_player(self):
        return self.player

    def get_inimigos(self):
        return self.inimigos

    def get_plataformas(self):
        return self.plataformas

    def get_score(self):
        return self.score

    def inimigo(self):
        pass
