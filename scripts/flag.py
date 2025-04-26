import pygame
from quadtree import QuadTree
class Flag:
    def __init__(self, game, entity_type, pos, size):
        self.game = game
        self.e_type = entity_type
        self.pos = list(pos)
        self.size = size

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self):
        player_bounding_box = self.game.player.rect()
        quad_tree = QuadTree(player_bounding_box)
        flag_rect = self.rect()

        quad_tree.insert(flag_rect)
        colliding_flag = quad_tree.collision_detection(player_bounding_box)
        if colliding_flag:
            return True

    def render(self, surf, img, offset=(0, 0)):
        surf.blit(img,
                  (self.pos[0] - offset[0] - img.get_width() // 2, self.pos[1] - offset[1] - img.get_height() // 2))
