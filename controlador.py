import pygame
import random
import time

from entidade import Player, Platform
from gameover import GameOver
from menu import Menu
from hud import Hud

from jogos.asteroid import Asteroid
from jogos.dino import Dino
from jogos.flappy import Flappy
from jogos.mario import Mario
from jogos.shooter import Shooter
from jogos.space import Space


class Controlador:
    def __init__(self, screen):
        self.novo_jogo = None
        pygame.display.set_caption("RetroVerse")
        self.jogos = {'Asteroid': Asteroid, 'Dino':Dino, 'Mario': Mario, 'Shooter': Shooter, 'Space': Space, 'Flappy': Flappy}
        self.jogo_atual = random.choice(list(self.jogos.values()))
        self.screen = screen
        self.hud = Hud()
        self.player = Player(37.5, 60, 500, 450, (255, 255, 255))
        self.plataforma = [Platform(1200, 40, 0, 660), Platform(250, 64, 690, 475), Platform(250, 64, 260, 325)]
        self.tempo_troca_de_fase = 8
        self.font = pygame.font.Font(None, 36)
        self.running = True
        self.jogos_disponiveis = list(self.jogos.values()).copy()
        self.inicio_jogo = time.time()
        pygame.mixer.init()
        self.lives = 3
        self.tempo_na_fase = 0
        self.score = 0
        self.temp_score = 0
        self.player.lives = 3
        self.num_fases = 0
        self.tempo_na_fase = 0
        self.tempo = 0
        self.background = pygame.image.load('assets/cachoeira.png').convert()

    def set_jogo(self, jogo_nome):
        self.jogo_atual = self.jogos[jogo_nome]

    def contar_tempo(self):
        self.tempo = time.time() - self.inicio_jogo
        self.tempo_na_fase = self.tempo - self.tempo_troca_de_fase * self.num_fases

    def contar_pontuacao(self):
        self.temp_score = self.novo_jogo.get_score()

    def mudar_jogo(self):
        if len(self.jogos_disponiveis) == 1:
            self.jogos_disponiveis = list(self.jogos.values()).copy()
        self.jogos_disponiveis.remove(self.jogo_atual)
        self.jogo_atual = random.choice(self.jogos_disponiveis)
        self.num_fases += 1

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        self.contar_tempo()
        self.contar_pontuacao()
        self.hud.update()

    def refazer_inimigos(self):
        inimigos = self.novo_jogo.get_inimigos()
        self.player = self.novo_jogo.get_player()
        self.plataforma = self.novo_jogo.get_plataformas()
        self.novo_jogo = self.jogo_atual(self.screen, [], self.player, inimigos, self.plataforma)
        self.novo_jogo.set_lives(self.lives)

    def game_over_reset(self):
        pygame.mixer_music.stop()
        self.jogos_disponiveis = list(self.jogos.values()).copy()
        gameover_screen = GameOver(self.screen, self.score + self.temp_score, self)
        self.running = False
        if gameover_screen.run():
            self.running = True

        self.jogo_atual = self.jogos[random.choice(list(self.jogos.keys()))]
        self.novo_jogo = self.jogo_atual(self.screen, [], self.player, [], self.plataforma)
        self.inicio_jogo = time.time()
        self.atualizar_entre_jogos()

        self.novo_jogo.set_lives(3)
        self.num_fases = 0
        self.score = 0
        self.temp_score = 0

    def atualizar_entre_jogos(self):
        self.jogo_atual = self.jogos[random.choice(list(self.jogos.keys()))]
        self.novo_jogo = self.jogo_atual(self.screen, [], self.player, [], self.plataforma)
        self.novo_jogo.set_lives(self.lives)
        self.inicio_jogo = time.time()
        pygame.mixer.music.load('assets/jogo.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def atualizar_contexto(self):
        self.score += self.temp_score
        self.score += 500
        self.mudar_jogo()
        self.refazer_inimigos()

    def run(self):
        menu = Menu(self.screen)
        while self.running:
            result = menu.main()
            if result == 'start':
                self.atualizar_entre_jogos()
                while self.running:
                    self.screen.blit(self.background, (0, 0))
                    #self.screen.fill((0, 0, 0))
                    self.novo_jogo.run()
                    self.lives = self.novo_jogo.get_lives()
                    self.hud.draw(self.screen, self.lives, self.tempo_troca_de_fase,
                                  self.tempo_na_fase, self.tempo,
                                  self.score + self.temp_score)
                    self.update()
                    pygame.display.flip()
                    if self.tempo_na_fase >= self.tempo_troca_de_fase:
                        self.atualizar_contexto()
                    if self.novo_jogo.get_lives() <= 0:
                        self.game_over_reset()
        pygame.quit()
