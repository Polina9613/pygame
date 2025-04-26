import pygame
import random

from scripts.utils import load_image, load_images, Animation
from scripts.entities import Player, Enemy
from scripts.tilemap import Tilemap
from scripts.cheese import Cheese
from scripts.flag import Flag
from scripts.button import Button
from quadtree import QuadTree


class Game:
    def __init__(self, level=0):
        pygame.init()
        pygame.display.set_caption('MOUSE VS CAT')

        self.screen = pygame.display.set_mode((1000, 562))

        self.display = pygame.Surface((500, 281))
        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.assets = {
            'decor': load_images('decor'),
            'grass': load_images('grass'),
            'large_decor': load_images('large_decor'),
            'player': load_image('player/idle/00.png'),
            'colour': load_image('background/colour.png'),
            'enemy/idle': Animation(load_images('enemy/idle'), img_dur=4),
            'enemy/run': Animation(load_images('enemy/run'), img_dur=6),
            'player/idle': Animation(load_images('player/idle'), img_dur=5),
            'player/run': Animation(load_images('player/run'), img_dur=6),
            'player/jump': Animation(load_images('player/jump')),
            'player/wall_slide': Animation(load_images('player/wall_slide')),
            'projectile': load_image('projectile.png'),
            'cheese': Animation(load_images('cheese')),
            'flag': load_image('flag/flag.png')

        }

        self.player = Player(self, (50, 50), (32, 14))

        self.tilemap = Tilemap(self, tile_size=16)

        self.level = level
        self.load_level(self.level)

        self.screenshake = 0

    def load_level(self, map_id):
        self.tilemap.load('maps/' + str(map_id) + '.json')
        self.enemies = []
        self.cheese = []

        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']

            else:
                self.enemies.append(Enemy(self, spawner['pos'], (20, 19)))

        for eat in self.tilemap.extract([('cheese', 0), ('cheese', 1)]):
            self.cheese.append(Cheese(self, 'cheese', eat['pos'], (18, 18)))

        self.flag_pos = self.tilemap.extract([('flag', 0)])[0]['pos']
        self.flag = Flag(self, 'flag', self.flag_pos, (16, 25))


        self.projectiles = []

        self.scroll = [0, 0]

        self.dead = 0

        self.play_button = Button((self.display.get_width() - 98) // 2,
                                         self.display.get_height() // 2 - 42, 98, 42, '',
                                         'images/menu/play/default.png',
                                         'images/menu/play/hover.png')

    def run(self):
        self.dead = 0
        run = True
        paused = False

        while run:
            self.display.blit(self.assets['colour'], (0, 0))

            self.screenshake = max(0, self.screenshake - 1)

            if self.flag.update():
                run = False

            if self.dead:
                run = False

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0])
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1])

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)
            self.flag.render(self.display, self.assets['flag'], offset=render_scroll)

            for cheese in self.cheese.copy():
                kill = cheese.update()
                cheese.render(self.display, offset=render_scroll)
                if kill:
                    self.cheese.remove(cheese)

            for enemy in self.enemies.copy():
                enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)



            if not self.dead and not paused:
                self.player.render(self.display, offset=render_scroll)

                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))


            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1
                img = self.assets['projectile']
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))

                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)

                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)

                player_bounding_box = pygame.Rect(self.player.pos[0], self.player.pos[1], self.player.size[0], self.player.size[1])
                quad_tree = QuadTree(player_bounding_box)
                projectile_rect = pygame.Rect(projectile[0][0], projectile[0][1], 6, 4)

                quad_tree.insert(projectile_rect)
                colliding_projectiles = quad_tree.collision_detection(player_bounding_box)
                for proj_rect in colliding_projectiles:
                    self.projectiles.remove(projectile)
                    self.dead += 1
                    self.screenshake = max(16, self.screenshake)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.player.jump()

                if event.type == pygame.KEYUP:

                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_p:
                        paused = not paused
                if event.type == pygame.USEREVENT and event.button == self.play_button:
                    paused = not paused

            if paused:

                self.display.blit(self.assets['colour'], (0, 0))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                    elif event.type == pygame.USEREVENT and event.button == self.play_button:
                        if event.button == self.play_button:
                            paused = not paused
                        break

                self.play_button.handle_event(event)
                self.play_button.check_hover(pygame.mouse.get_pos())
                self.play_button.draw(self.display)

                self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), screenshake_offset)

            pygame.display.update()

            self.clock.tick(60)

        return self.cheese, self.dead

