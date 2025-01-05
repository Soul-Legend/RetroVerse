import pygame
from controlador import Controlador

pygame.init()
pygame.mixer.music.load('assets/menu.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
screen = pygame.display.set_mode((1200, 700))
controlador = Controlador(screen)
controlador.run()
