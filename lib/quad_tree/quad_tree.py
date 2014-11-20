from lib.ecs.component.shape import RectShapeComponent
from lib.geometry.rect import Rect

class QuadTreeNode(object):
    def __init__(self, x, y, width, height, max_count=4):
        self.rect = Rect(x, y, width, height)
        self.entities = []
        self.children =[]
        self.max_count = max_count

        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def intersects(self, entity):
        return self.rect.intersects(entity[RectShapeComponent])

    def add_entity(self, entity):
        if self.intersects(entity):
            self.entities.append(entity)
            if len(self.entities) > self.max_count:
                self.split()

    def remove_entity(self, entity):
        if len(self.children) > 0:
            for child in self.children:
                child.remove_entity(entity)
        else:
            if entity in self.entities:
                self.entities.remove(entity)

    def split(self):
        child_width = int(self.width / 2.0)
        child_height = int(self.height / 2.0)

        top_left_child = QuadTreeNode(self.x, self.y, child_width, child_height, self.max_count)
        top_right_child = QuadTreeNode(self.x + child_width, self.y, self.width - child_width, child_height, self.max_count)
        bottom_left_child = QuadTreeNode(self.x, self.y + child_height, child_width, self.height - child_height, self.max_count)
        bottom_right_child = QuadTreeNode(self.x + child_width, self.y + child_height, self.width - child_width, self.height - child_height, self.max_count)

        self.children.extend([top_left_child, top_right_child, bottom_left_child, bottom_right_child])

        for child in self.children:
            for entity in self.entities:
                child.add_entity(entity)

        self.entities = []

    def print_node(self, indentation_level=0):
        if indentation_level == 0:
            print

        quadrants = ['top left', 'top right', 'bottom left', 'bottom right']
        indentation = '    ' * indentation_level

        for entity in self.entities:
            x, y, width, height = entity.position.x, entity.position.y, entity[RectShapeComponent].width, entity[RectShapeComponent].height
            print '{}{}'.format(indentation, (x, y, width, height))

        for i, child in enumerate(self.children):
            new_indentation_level = indentation_level + 1
            print '{}[{} - ({}, {}) - {}x{}]'.format(
                '    ' * new_indentation_level,
                quadrants[i],
                child.rect.x,
                child.rect.y,
                child.rect.width,
                child.rect.height
            )
            child.print_node(new_indentation_level)
