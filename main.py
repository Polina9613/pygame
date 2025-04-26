import pygame
import sys
from scripts.button import Button
from game import Game
from scripts.tilemap import Tilemap
from scripts.utils import load_images


WIDTH, HEIGHT = 1000, 562
background = pygame.image.load('images/background/colour.png')


class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.display = pygame.Surface((WIDTH // 2, HEIGHT // 2))
        self.assets = {
            'levels': load_images('menu/Levels')
        }
        self.tilemap = Tilemap(self, tile_size=45)
        try:
            self.tilemap.load('map_menu.json')
        except FileNotFoundError:
            pass

    def main_menu(self):
        self.menu_button = Button((WIDTH // 2 - 196//2) // 2, 200 // 2, 196//2, 84//2, '', 'images/menu/button/default.png',
                                   'images/menu/button/hover.png')
        self.exit_button = Button((WIDTH // 2 - 28) // 2, 400 // 2, 28, 28, '',
                                       'images/menu/exit.png', '')
        running = True
        while running:
            self.display.blit(background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.USEREVENT and event.button == self.menu_button:
                    Menu().menu()
                if event.type == pygame.USEREVENT and event.button == self.exit_button:
                    running = False

                for btn in [self.menu_button, self.exit_button]:
                    btn.handle_event(event)

            for btn in [self.menu_button, self.exit_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(self.display)
            font = pygame.font.Font(None, 36)
            text_menu = font.render('MENU', True, (255, 255, 255))
            text_rect = text_menu.get_rect(center=(WIDTH // 4, 100+20))
            self.display.blit(text_menu, text_rect)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            pygame.display.update()

    def menu(self):
        self.levels_button = Button((WIDTH // 2 - 42) // 2, 100 // 2 + 60, 42, 42, '', 'images/menu/Levels/default.png',
                                   'images/menu/Levels/hover.png')
        self.back_button = Button(15, 15, 42, 42, '', 'images/menu/back/default.png',
                                   'images/menu/back/hover.png')
        running = True
        while running:
            self.display.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.USEREVENT and event.button == self.levels_button:
                    Menu().levels_menu()
                if event.type == pygame.USEREVENT and event.button == self.back_button:
                    running = False
                for btn in [self.levels_button, self.back_button]:
                    btn.handle_event(event)

            for btn in [self.levels_button, self.back_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(self.display)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            pygame.display.update()
    def levels_menu(self):

        self.tilemap.load('maps/map_menu.json')
        self.back_button = Button(15, 15, 42, 42, '', 'images/menu/back/default.png',
                                       'images/menu/back/hover.png')
        running = True
        while running:
            self.display.blit(background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    tile_loc = str(int(pos[0] // 90)) + ';' + str(int(pos[1] // 90))
                    if tile_loc in self.tilemap.tilemap:
                        current_level = (self.tilemap.tilemap[tile_loc]['pos'][0])//2

                        cheese, die = Game(level=current_level).run()

                        Menu().next_or_repeat_level(current_level, cheese, die)

                if event.type == pygame.USEREVENT and event.button == self.back_button:
                    running = False
                for btn in [self.back_button]:
                    btn.handle_event(event)

            for btn in [self.back_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(self.display)
            self.tilemap.render(self.display, (0, 0))
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()

    def next_or_repeat_level(self, current_level, cheese, die):
        self.home_button = Button((WIDTH // 2 - 42) // 2, 400 // 2, 42, 42, '', 'images/menu/Home/default.png',
                                   'images/menu/Home/hover.png')
        self.repeat_button = Button((WIDTH // 2 - 42) // 2, 300 // 2, 42, 42, '', 'images/menu/Repeat/default.png',
                                       'images/menu/Repeat/hover.png')
        self.next_button = Button((WIDTH // 2 - 42) // 2, 200 // 2, 42, 42, '',
                                       'images/menu/next_level/default.png',
                                       'images/menu/next_level/hover.png')
        self.star_active = pygame.image.load('images/menu/Star/active.png')
        self.star_unactive = pygame.image.load('images/menu/Star/unactive.png')


        running = True
        while running:
            self.display.blit(background, (0, 0))
            if len(cheese) == 0 and not die:
                for i in range(4, 7):
                    self.display.blit(self.star_active, (i * 50 - 23, 25))
            elif 1 <= len(cheese) <= 2 and not die:
                for i in range(4, 6):
                    self.display.blit(self.star_active, (i * 50 - 23, 25))
                self.display.blit(self.star_unactive, (6 * 50 - 23, 25))
            else:
                for i in range(4, 7):
                    self.display.blit(self.star_unactive, (i * 50 - 23, 25))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.USEREVENT and event.button == self.home_button:
                    running = False
                if event.type == pygame.USEREVENT and event.button == self.repeat_button:
                    cheese, die = Game(level=current_level).run()



                if event.type == pygame.USEREVENT and event.button == self.next_button:
                    current_level += 1
                    cheese, die = Game(level=current_level).run()

                for btn in [self.home_button, self.repeat_button, self.next_button]:
                    btn.handle_event(event)

            for btn in [self.home_button, self.repeat_button, self.next_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(self.display)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            pygame.display.update()



if __name__ == '__main__':
    Menu().main_menu()
