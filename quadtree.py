import pygame

class QuadTree:
    def __init__(self, bounding_box, depth=8, items=None):
        self.bounding_box = bounding_box
        self.depth = depth
        self.items = items if items is not None else []
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None

        if self.depth > 0 and len(self.items) > 0: # Если depth больше нуля и есть объекты для вставки (items)
            center_x = (self.bounding_box.left + self.bounding_box.right) // 2 # вычисляются центры фигуры
            center_y = (self.bounding_box.top + self.bounding_box.bottom) // 2

            nw_items = [item for item in self.items if item.colliderect(
                pygame.Rect(self.bounding_box.left, self.bounding_box.top, center_x, center_y))]
            ne_items = [item for item in self.items if item.colliderect(
                pygame.Rect(center_x, self.bounding_box.top, self.bounding_box.right, center_y))]
            sw_items = [item for item in self.items if item.colliderect(
                pygame.Rect(self.bounding_box.left, center_y, center_x, self.bounding_box.bottom))]
            se_items = [item for item in self.items if item.colliderect(
                pygame.Rect(center_x, center_y, self.bounding_box.right, self.bounding_box.bottom))]

            self.nw = QuadTree(pygame.Rect(self.bounding_box.left, self.bounding_box.top, center_x, center_y), depth - 1, nw_items)
            self.ne = QuadTree(pygame.Rect(center_x, self.bounding_box.top, self.bounding_box.right, center_y), depth - 1, ne_items)
            self.sw = QuadTree(pygame.Rect(self.bounding_box.left, center_y, center_x, self.bounding_box.bottom), depth - 1, sw_items)
            self.se = QuadTree(pygame.Rect(center_x, center_y, self.bounding_box.right, self.bounding_box.bottom), depth - 1, se_items)

            self.items = []

    def insert(self, rect):
        if self.depth == 0 or not rect.colliderect(self.bounding_box):
            return

        if len(self.items) < 4:
            self.items.append(rect)
            return

        center_x = (self.bounding_box.left + self.bounding_box.right) // 2
        center_y = (self.bounding_box.top + self.bounding_box.bottom) // 2

        top_left = pygame.Rect(self.bounding_box.left, self.bounding_box.top, center_x, center_y)
        top_right = pygame.Rect(center_x, self.bounding_box.top, self.bounding_box.right, center_y)
        bottom_left = pygame.Rect(self.bounding_box.left, center_y, center_x, self.bounding_box.bottom)
        bottom_right = pygame.Rect(center_x, center_y, self.bounding_box.right, self.bounding_box.bottom)

        if rect.bounding_box.intersects(top_left):
            self.nw.insert(rect)
        elif rect.bounding_box.intersects(top_right):
            self.ne.insert(rect)
        elif rect.bounding_box.intersects(bottom_left):
            self.sw.insert(rect)
        else:
            self.se.insert(rect)

    def collision_detection(self, rect):
        colliding_items = []

        if not rect.colliderect(self.bounding_box):
            return colliding_items

        for item in self.items:
            if rect.colliderect(item):
                colliding_items.append(item)

        if self.nw:
            colliding_items.extend(self.nw.collision_detection(rect))
        if self.ne:
            colliding_items.extend(self.ne.collision_detection(rect))
        if self.sw:
            colliding_items.extend(self.sw.collision_detection(rect))
        if self.se:
            colliding_items.extend(self.se.collision_detection(rect))


        return colliding_items

