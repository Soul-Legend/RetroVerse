import pygame

from highscore import Highscore
from gifanimation import Gif
from tutorial import Tutorial


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load('assets/assets_menu/tela_de_fundo_menu.png').convert()
        self.highscore_icon = pygame.image.load('assets/assets_menu/highscore.png')
        self.start_button = pygame.image.load('assets/assets_menu/botao_jogar.png')
        self.quit_button = pygame.image.load('assets/assets_menu/botao_tutorial.png')

        selection_icon1_frames = [pygame.image.load(f'assets/assets_menu/selecionador_frame{i}.png') for i in range(2)]
        selection_icon2_frames = [pygame.image.load(f'assets/assets_menu/selecionador2_frame{i}.png') for i in range(2)]
        press_space_frames = [pygame.image.load(f'assets/assets_menu/pressionar_espaco_frame{i}.png') for i in range(13)]

        selection_icon1_durations = [500] * 2
        selection_icon2_durations = [500] * 2
        press_space_durations = [150 if i in [0, 7] else 70 for i in range(13)]
        self.selection_icon1 = Gif(selection_icon1_frames, selection_icon1_durations)
        self.selection_icon2 = Gif(selection_icon2_frames, selection_icon2_durations)
        self.press_space = Gif(press_space_frames, press_space_durations)

        self.buttons = [self.start_button, self.quit_button]
        self.current_selection = 0
        self.button_positions = [(510, 225), (595, 418)]
        self.selection_positions = [(507, 240), (582, 422)]
        self.highscore = Highscore()
        self.font = pygame.font.SysFont('bahnschrift', 26)
        self.press_space_center_position = (600, 600)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.highscore_icon, (205, 375))
        highscore_text = self.font.render(str(self.highscore.highscore), True, (255, 215, 0))
        self.screen.blit(highscore_text, (245, 410))
        for i, button in enumerate(self.buttons):
            self.screen.blit(button, self.button_positions[i])
            if i == self.current_selection:
                if self.current_selection == 0:
                    self.screen.blit(self.selection_icon1.get_current_frame(), self.selection_positions[i])
                elif self.current_selection == 1:
                    self.screen.blit(self.selection_icon2.get_current_frame(), self.selection_positions[i])
        press_space_image = self.press_space.get_current_frame()
        press_space_position = (self.press_space_center_position[0] - press_space_image.get_width() / 2,
                                self.press_space_center_position[1] - press_space_image.get_height() / 2)
        self.screen.blit(press_space_image, press_space_position)
        pygame.display.flip()

    def main(self):
        running = True
        tutorial_screen = Tutorial(self.screen, self.press_space)
        while running:
            dt = self.clock.tick()  # retorna o tempo desde o ultimo tick

            self.selection_icon1.update(dt)
            self.selection_icon2.update(dt)
            self.press_space.update(dt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.current_selection = (self.current_selection - 1) % len(self.buttons)
                    elif event.key == pygame.K_s:
                        self.current_selection = (self.current_selection + 1) % len(self.buttons)
                    elif event.key == pygame.K_SPACE:
                        if self.current_selection == 0:
                            return 'start'
                        elif self.current_selection == 1:
                            tutorial_screen.main()
                            return

            self.draw()
