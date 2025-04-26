import random
from quadtree import QuadTree
import pygame

class PhysicsEntity:
    def __init__(self, game, entity_type, pos, size):
        self.game = game
        self.type = entity_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.action = ''
        self.flip = False
        self.set_action('idle')
        self.last_movement = [0, 0]

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def update(self, tilemap, movement=(0, 0)):

        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]

        entity_rect = self.rect()
        entity_bounding_box = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        quad_tree = QuadTree(entity_bounding_box)

        for tile_rect in tilemap.physics_rects_around(self.pos):
            quad_tree.insert(tile_rect)
        colliding_tiles = quad_tree.collision_detection(entity_bounding_box)

        for tile_rect in colliding_tiles:
            print(1)
            if frame_movement[0] > 0:
                entity_rect.right = tile_rect.left
                self.collisions['right'] = True
            if frame_movement[0] < 0:
                entity_rect.left = tile_rect.right
                self.collisions['left'] = True
            self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]

        entity_rect = self.rect()
        player_bounding_box = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        quad_tree = QuadTree(player_bounding_box)

        for tile_rect in tilemap.physics_rects_around(self.pos):
            quad_tree.insert(tile_rect)
        colliding_tiles = quad_tree.collision_detection(player_bounding_box)

        for tile_rect in colliding_tiles:
            if frame_movement[1] > 0:
                entity_rect.bottom = tile_rect.top
                self.collisions['down'] = True
            if frame_movement[1] < 0:
                entity_rect.top = tile_rect.bottom
                self.collisions['up'] = True
            self.pos[1] = entity_rect.y

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True
        self.last_movement = movement
        self.velocity[1] = min(5, self.velocity[1] + 0.1)
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)
        self.animation.update()

    def render(self, surface, offset=(0, 0)):
        surface.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0], self.pos[1] - offset[1]))

class Enemy(PhysicsEntity):

    def __init__(self, game, pos, size):
        super().__init__(game, 'enemy', pos, size)

        self.walking = 0

    def update(self, tilemap, movement=(0, 0)):
        if self.walking:
            if tilemap.solid_check((self.rect().centerx + (-15 if self.flip else 15), self.pos[1] + 24)):
                if (self.collisions['right'] or self.collisions['left']):
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)
            if not self.walking:
                dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
                if (abs(dis[1]) < 16):
                    if (self.flip and dis[0] < 0):
                        self.game.projectiles.append([[self.rect().centerx - 7, self.rect().centery], -1.5, 0])
                    if (not self.flip and dis[0] > 0):
                        self.game.projectiles.append([[self.rect().centerx + 7, self.rect().centery], 1.5, 0])


        elif random.random() < 0.01:
            self.walking = random.randint(30, 120)

        super().update(tilemap, movement=movement)

        if movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.jumps = 2

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)
        self.air_time += 1

        if self.air_time > 200:
            if not self.game.dead:
                self.game.screenshake = max(16, self.game.screenshake)
            self.game.dead += 1

        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 2

        if (self.collisions['right'] or self.collisions['left']) and self.air_time > 5:
            if self.last_movement[0] < 0:
                self.velocity[0] = 2
                self.velocity[1] = 2
            if self.last_movement[0] > 0:
                self.velocity[0] = -2
                self.velocity[1] = 2

        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)

    def jump(self):
        if self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5
            return True