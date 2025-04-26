import pygame
from quadtree import QuadTree

class Cheese:
    def __init__(self, game, entity_type, pos, size):
        self.game = game
        self.e_type = entity_type
        self.pos = list(pos)
        self.animation = self.game.assets[entity_type].copy()
        self.size = size

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self):
        player_bounding_box = self.game.player.rect()
        quad_tree = QuadTree(player_bounding_box)
        cheese_rect = self.rect()

        quad_tree.insert(cheese_rect)
        colliding_cheese = quad_tree.collision_detection(player_bounding_box)
        if colliding_cheese:
            return True
    def render(self, surf, offset=(0, 0)):
        img = self.animation.img()
        surf.blit(img, (self.pos[0] - offset[0] - img.get_width() // 2, self.pos[1] - offset[1] - img.get_height() // 2))
