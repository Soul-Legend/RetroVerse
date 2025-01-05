import pygame
import random


#---------------------------------------------------INICIALIZAÇÃO---------------------------------------------------#


class Entity:
    def __init__(self, width, height, x, y, color):
        self.color = color
        self.width = width
        self.height = height
        self.sprites = []
        self.load_animation()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0

    def load_animation(self):
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

    def update(self):
        pass

    def get_coords(self):
        return (self.rect.x, self.rect.y)


class Player(Entity, pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, color):
        self.acceleration = 1
        self.multiplier = 1.5
        self.tiros_prontos = 0
        self.velocity = 0
        self.lives = 3

        self.ultimo_tiro = 0
        self.tiro_recarga = 150
        self.tiro_pronto = True

        self.damage_ticks = 0
        self.damage_duration = 400
        self.tomando_dano = False

        self.invincible_ticks = pygame.time.get_ticks()
        self.invincible_duration = 1000
        self.is_invincible = True

        self.morte_ticks = 0
        self.morte_duration = 2000
        self.morrendo = False

        self.is_running = False
        self.is_jumping = False
        self.virado_esquerda = False

        self.blank = pygame.transform.scale(pygame.image.load('./assets/player/blank.png'), (60, 60))
        self.sprite_dano = pygame.transform.scale(pygame.image.load('./assets/player/mario_dano.png'), (60, 60))
        self.sprite_morte = pygame.transform.scale(pygame.image.load('./assets/player/mario_morte.png'), (60, 60))
        self.sprite_dano_invert = pygame.transform.scale(pygame.image.load('./assets/player/mario_bola_1.png'), (60, 60))

        super().__init__(width, height, x, y, (255, 255, 255))

    def animate_run(self):
        self.is_running = True
        if self.vel_x < 0:
            self.virado_esquerda = True
        else:
            self.virado_esquerda = False

    def tomar_dano(self):
        self.lives -= 1
        self.tomando_dano = True
        self.damage_ticks = pygame.time.get_ticks()
        self.is_invincible = True
        self.invincible_ticks = pygame.time.get_ticks()

    def get_vidas(self):
        return self.lives

    def jump_mario(self):
        self.velocity = -18
        self.is_jumping = True
    
    def jump_dino(self):
        self.velocity = -15
        self.is_jumping = True

    def jump_flappy(self):
        self.velocity = -4
        self.is_jumping = True

    def update(self):
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]

        if self.is_invincible and self.current_sprite % 1 >= 0.5:
            self.image = self.blank

        if self.tomando_dano:
            self.image = self.sprite_dano


class Enemy(Entity):
    def __init__(self, x, y, color, multiplier, x_sprite, y_sprite):
        self.multiplier = multiplier
        self.x_sprite = x_sprite
        self.y_sprite = y_sprite
        self.scale = (self.x_sprite * self.multiplier, self.y_sprite * self.multiplier)
        self.acceleration = 1
        self.velocity = 0
        self.is_running = True
        self.direction = [random.choice([-2, 2]), random.choice([-3, -2, -1, 1, 2, 3])]
        super().__init__(self.scale[0], self.scale[1], x, y, color)

    def update(self):
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]


#---------------------------------------------------ASTEROID---------------------------------------------------#


class PlayerAsteroid(Player):
    def load_animation(self):
        self.multiplier = 1.5
        scale = (28 * self.multiplier, 30 * self.multiplier)
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/player/mario_bola_1.png'), scale))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/player/mario_bola_2.png'), scale))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/player/mario_bola_3.png'), scale))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/player/mario_bola_4.png'), scale))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.rect.x, self.rect.y]


class InimigoAsteroid(Enemy):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, 2, 25, 21)

    def load_animation(self):
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/gumbas/gumba_laranja_voando_1.png'), self.scale))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/gumbas/gumba_laranja_voando_2.png'), self.scale))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.rect.x, self.rect.y]


#---------------------------------------------------DINO---------------------------------------------------#


class PlayerDino(Player):
    def load_animation(self):
        scale = (32 * self.multiplier, 40 * self.multiplier)
        self.sprite_pulando = pygame.transform.scale(pygame.image.load('./assets/player/dino_pulando.png'), scale)
        #self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/player/dino_sprite1.png'), scale))
        #self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/player/dino_sprite2.png'), scale))
        self.sprite_dano = pygame.transform.scale(pygame.image.load('./assets/player/mario_dano.png'), (60, 60))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/player/dino_andando_1.png'), scale))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/player/dino_andando_2.png'), scale))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.rect.x, self.rect.y]

    def update(self):
        self.current_sprite += 0.04
        if self.is_jumping:
            self.image = self.sprite_pulando
        else:
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)]
        if self.is_invincible and self.current_sprite % 1 >= 0.5:
            self.image = self.blank
        if self.tomando_dano:
            self.image = self.sprite_dano


class DinoEnemy(Enemy):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, 2.5, 17, 21)

    def load_animation(self):
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/gumbas/gumba_azul_andando_1.png'), self.scale))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/gumbas/gumba_azul_andando_2.png'), self.scale))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.rect.x, self.rect.y]


#---------------------------------------------------FLAPPY---------------------------------------------------#


class PlayerFlappy(Player):
    def load_animation(self):
        scale = (40 * self.multiplier, 29 * self.multiplier)
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/player/mario_flappy.png'), scale))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.rect.x, self.rect.y]


class InimigoFlappy(Enemy):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, 2, 25, 21)

    def load_animation(self):
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/gumbas/gumba_verde_voando_1.png'), self.scale))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/gumbas/gumba_verde_voando_2.png'), self.scale))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.rect.x, self.rect.y]


#---------------------------------------------------MARIO---------------------------------------------------#


class PlayerMario(Player):
    def load_animation(self):
        scale = (26 * self.multiplier, 40 * self.multiplier)
        self.sprite_parado = pygame.transform.scale(pygame.image.load('./assets/player/mario_parado.png'), scale)
        self.sprite_pulando = pygame.transform.scale(pygame.image.load('./assets/player/mario_pulando.png'), scale)
        self.sprite_parado_invert = pygame.transform.scale(pygame.image.load('./assets/player/mario_parado_invert.png'), scale)
        self.sprite_pulando_invert = pygame.transform.scale(pygame.image.load('./assets/player/mario_pulando_invert.png'), scale)
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/player/mario_andando_1.png'), scale))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/player/mario_andando_2.png'), scale))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/player/mario_andando_3.png'), scale))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/player/mario_andando_4.png'), scale))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/player/mario_andando_5.png'), scale))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/player/mario_andando_6.png'), scale))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/player/mario_andando_1_invert.png'), scale))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/player/mario_andando_2_invert.png'), scale))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/player/mario_andando_3_invert.png'), scale))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/player/mario_andando_4_invert.png'), scale))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/player/mario_andando_5_invert.png'), scale))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/player/mario_andando_6_invert.png'), scale))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.rect.x, self.rect.y]

    def update(self):
        self.current_sprite += 0.1
        if self.is_jumping:
            if self.virado_esquerda:
                self.image = self.sprite_pulando_invert
            else:
                self.image = self.sprite_pulando
        elif self.is_running:
            if self.virado_esquerda:
                if self.current_sprite < 6 or self.current_sprite >= len(self.sprites):
                    self.current_sprite = 6
                self.image = self.sprites[int(self.current_sprite)]
            else:
                if self.current_sprite >= 6:
                    self.current_sprite = 0
                self.image = self.sprites[int(self.current_sprite)]

        else:
            if self.virado_esquerda:
                self.image = self.sprite_parado_invert
            else:
                self.image = self.sprite_parado
        if self.is_invincible and self.current_sprite % 1 >= 0.5:
            self.image = self.blank
        if self.tomando_dano:
            self.image = self.sprite_dano


class InimigoMario(Enemy):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, 2.5, 17, 21)

    def load_animation(self):
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/gumbas/gumba_azul_andando_1.png'), self.scale))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/gumbas/gumba_azul_andando_2.png'), self.scale))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.rect.x, self.rect.y]


#---------------------------------------------------SHOOTER---------------------------------------------------#


class PlayerShooter(Player):
    def load_animation(self):
        scale = (40 * self.multiplier, 40 * self.multiplier)
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/player/mario_mira_1.png'), scale))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/player/mario_mira_2.png'), scale))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.rect.x, self.rect.y]

    def update(self):
        self.current_sprite += 0.07
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        if self.is_invincible and self.current_sprite % 1 >= 0.5:
            self.image = self.blank
        if self.tomando_dano:
            self.image = self.sprite_dano


class InimigoShooter(Enemy):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, 2, 25, 21)

    def load_animation(self):
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/gumbas/gumba_verde_voando_1.png'), self.scale))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/gumbas/gumba_verde_voando_2.png'), self.scale))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.rect.x, self.rect.y]


#---------------------------------------------------SPACE---------------------------------------------------#


class PlayerSpace(Player):
    def load_animation(self):
        scale = (44 * self.multiplier, 40 * self.multiplier)
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/player/mario_space.png'), scale))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.rect.x, self.rect.y]


class InimigoSpace(Enemy):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, 2, 25, 21)

    def load_animation(self):
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/gumbas/gumba_invader_sprite1.png'), self.scale))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/gumbas/gumba_invader_sprite2.png'), self.scale))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.rect.x, self.rect.y]


#---------------------------------------------------OUTROS---------------------------------------------------#


class Bullet(Entity):
    def __init__(self, x, y, vel_x, vel_y):
        self.scale = (20, 20)
        super().__init__(20, 20, x, y, (255, 255, 0))
        speed = 10
        self.pos = (x, y)

        if vel_x > 0:
            self.vel_x = speed
        elif vel_x < 0:
            self.vel_x = -speed
        else:
            self.vel_x = 0

        if vel_y > 0:
            self.vel_y = speed
        elif vel_y < 0:
            self.vel_y = -speed
        else:
            self.vel_y = 0

        if self.vel_x == 0 and self.vel_y == 0:
            self.vel_x = 0
            self.vel_y = -speed
        
    def load_animation(self):
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/fireball_gif-0.png'), self.scale))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/fireball_gif-1.png'), self.scale))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/fireball_gif-2.png'), self.scale))
        self.sprites.append(pygame.transform.scale(pygame.image.load('./assets/fireball_gif-3.png'), self.scale))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.rect.x, self.rect.y]

    def update(self):
        self.current_sprite += 0.2
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]


class Platform(Entity, pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__(width, height, x, y, (0, 255, 0))
