"""
Origin Game Engine Library.
This file contains all game objects classes .
"""

import random
import pygame.draw
from functions import *


def rotate(image, pos, origin_pos, angle):
    """ Rotate pygame surface to given angle with stable origin position """

    # calculate the axis aligned bounding box of the rotated image
    w, h = image.get_size()
    box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot
    pivot = pygame.math.Vector2(origin_pos[0], -origin_pos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - origin_pos[0] + min_box[0] - pivot_move[0], pos[1] - origin_pos[1] - max_box[1] + pivot_move[1])

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    return rotated_image, [origin[0] + 25, origin[1] + 25]





class Surface(Pos):
    """ Surface class that allows you to set alpha value, colorkey and other cool things to show on pygame window"""

    def __init__(self, game, pos=None, size=None, alpha=255, colorkey=None):
        self.game = game

        super().__init__(pos)
        if size is None:
            self.size = [200, 100]
        else:
            self.size = size
        self.alpha = alpha
        self.colorkey = colorkey

        self.create_surface()

    def create_surface(self):
        """ Creates pygame surface """

        self.surface = pygame.Surface(self.size)
        self.surface.set_alpha(self.alpha)
        self.surface.set_colorkey(self.colorkey)

    def update(self):
        """ Shows the surface on a game app display """

        self.game.app.DISPLAY.blit(self.surface, self.pos)


class Label(Pos):
    """ Label UI object for pygame games. """

    def __init__(self, game, text="", pos=None, font_name="Segoe UI", font_size=100, bold=False, italic=False,
                 smooth=True, foreground=(200, 200, 200), background=None):
        self.game = game

        super().__init__(pos)
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.bold = bold
        self.italic = italic
        self.smooth = smooth
        self.foreground = foreground
        self.background = background

        self.font = pygame.font.SysFont(font_name, font_size, bold, italic)
        self.update_text(self.text, self.smooth, self.foreground, self.background)

    def update(self):
        """ Shows the surface of label on a game app display """

        self.game.app.DISPLAY.blit(self.surface, self.pos)

    def update_text(self, text, smooth=None, foreground=None, background=None):
        """ Updates text, smooth, foreground and background values of label and recreates surface of label """

        self.text = str(text)
        if smooth:
            self.smooth = smooth
        if foreground:
            self.foreground = foreground
        if background:
            self.background = background
        self.surface = self.font.render(self.text, self.smooth, self.foreground, self.background)
        self.size = self.surface.get_size()

    def center_x(self, y=0):
        """ Places label at the center of game app screen width """

        self.pos = [(self.game.app.WIDTH - self.size[0]) / 2, y]
        return self

    def center_y(self, x=0):
        """ Places label at the center of game app screen height """

        self.pos = [x, (self.game.app.HEIGHT - self.size[1]) / 2]
        return self

    def center(self):
        """ Places label at the center of game app screen width and height """

        self.pos = [(self.game.app.WIDTH - self.size[0]) / 2,
                    (self.game.app.HEIGHT - self.size[1]) / 2]
        return self

    def percent_x(self, percent=0, y=None):
        """ Places label at given percent on the game app screen width """

        one_percent = self.game.app.WIDTH / 100
        if y is None:
            self.pos = [percent * one_percent, (self.game.app.HEIGHT - self.size[1]) / 2]
        else:
            self.pos = [percent * one_percent, y]
        return self

    def percent_y(self, percent=0, x=None):
        """ Places label at given percent on the game app screen height """

        one_percent = self.game.app.HEIGHT / 100
        if x is None:
            self.pos = [(self.game.app.WIDTH - self.size[0]) / 2, percent * one_percent]
        else:
            self.pos = [x, percent * one_percent]
        return self

    def percent(self, percent_x=0, percent_y=0):
        """ Places label at given percent on the game app screen width and height """

        one_percent_x = self.game.app.WIDTH / 100
        one_percent_y = self.game.app.HEIGHT / 100
        self.pos = [percent_x * one_percent_x, percent_y * one_percent_y]
        return self


class Button(Label):
    """ Button UI object for pygame games. """

    def __init__(self, game, text="", pos=None, font_name="Segoe UI", font_size=60, bold=False, italic=False,
                 smooth=True, foreground=(200, 200, 200), background=None):
        super().__init__(game, text, pos, font_name, font_size, bold, italic, smooth, foreground, background)

        self.counter = 0
        self.counter_max = 50

    def clicked(self, mouse_buttons, mouse_position):
        """ Checks if button is clicked or not """

        x1 = mouse_position[0]
        x2 = self.pos[0]
        w2 = self.size[0]
        y1 = mouse_position[1]
        y2 = self.pos[1]
        h2 = self.size[1]
        if self.counter > 0:
            self.counter -= 1
        if mouse_buttons[0] and touched(x1, 1, x2, w2, y1, 1, y2, h2) and self.counter <= 0:
            self.counter = self.counter_max
            return True
        else:
            return False


class OptionButton(Button):
    """
    OptionButton UI object for pygame games.
    When clicked, switches current option to next option.
    """

    def __init__(self, game, text="", options=None, pos=None, font_name="Segoe UI", font_size=60, bold=False,
                 italic=False, smooth=True, foreground=(200, 200, 200), background=None,
                 current_option=0):
        if options is None:
            self.options = ["Option 1", "Option 2", "Option 3"]
        else:
            self.options = options
        self.current_option = current_option
        self.static_text = text
        self.text = self.static_text + str(self.options[self.current_option])
        super().__init__(game, self.text, pos, font_name, font_size, bold, italic, smooth, foreground, background)
        self.counter_max = 20

    def clicked(self, mouse_buttons, mouse_position):
        """ Checks if option button is clicked or not """

        x1 = mouse_position[0]
        x2 = self.pos[0]
        w2 = self.size[0]
        y1 = mouse_position[1]
        y2 = self.pos[1]
        h2 = self.size[1]
        if self.counter > 0:
            self.counter -= 1
        if mouse_buttons[0] and touched(x1, 1, x2, w2, y1, 1, y2, h2) and self.counter <= 0:
            self.counter = self.counter_max
            self.next_option()

    def next_option(self):
        """ Selects next option to display on option button """

        self.current_option += 1
        if self.current_option > len(self.options) - 1:
            self.current_option = 0
        self.text = self.static_text + str(self.options[self.current_option])
        self.update_text(self.text, self.smooth, self.foreground, self.background)

    def get_current_option(self):
        """ Returns current option value """

        return self.options[self.current_option]


class ColorOptionButton(OptionButton):
    """
    ColorOptionButton UI object for pygame games.
    When clicked, switches current option to next option.
    Option represents RGB color. Option example: (255, 0, 0).
    """

    def __init__(self, game, text="", color_rect_size=None, options=None, pos=None, font_name="Segoe UI", font_size=60,
                 bold=False, italic=False, smooth=True,
                 foreground=(200, 200, 200), background=None, current_option=0, outline=1):
        super().__init__(game, text, options, pos, font_name, font_size, bold, italic, smooth, foreground, background,
                         current_option)
        self.text = self.static_text
        self.outline = outline
        self.update_text(self.text, self.smooth, self.foreground, self.background)
        if options is None:
            self.options = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        else:
            self.options = options
        if color_rect_size is None:
            self.color_rect_size = [self.font_size * 2, self.font_size + 10]
        else:
            self.color_rect_size = color_rect_size

    def update(self):
        """ Shows the surface of label on a game app display and the rectangle with picked color option """

        pygame.draw.rect(self.game.app.DISPLAY, self.options[self.current_option],
                         pygame.Rect([self.pos[0] + self.size[0], self.pos[1]], self.color_rect_size))
        pygame.draw.rect(self.game.app.DISPLAY, self.foreground,
                         pygame.Rect([self.pos[0] + self.size[0], self.pos[1]], self.color_rect_size), self.outline)
        self.game.app.DISPLAY.blit(self.surface, self.pos)

    def next_option(self):
        """ Selects next option to display on color option button """

        self.current_option += 1
        if self.current_option > len(self.options) - 1:
            self.current_option = 0
        self.text = self.static_text
        self.update_text(self.text, self.smooth, self.foreground, self.background)


class Text(Label):
    """
    Text UI object for pygame games.
    This widget allows you to create multiple lines text.
    """

    def __init__(self, game, text="", pos=None, font_name="Segoe UI", font_size=60, bold=False, italic=False,
                 smooth=True, foreground=(200, 200, 200), background=None, line_height=None):
        super().__init__(game, text, pos, font_name, font_size, bold, italic, smooth, foreground, background)

        if line_height is None:
            self.line_height = font_size
        else:
            self.line_height = line_height

        self.text_list = self.text.split("\n")
        self.lines = len(self.text_list)
        self.surface_list = [self.font.render(i, self.smooth, self.foreground, self.background) for i in self.text_list]
        self.pos_list = [[self.pos[0], self.pos[1] + i * self.line_height] for i in range(len(self.text_list))]
        self.size_list = [self.surface_list[i].get_size() for i in range(self.lines)]

        self.size = [max([self.surface_list[i].get_size()[0] for i in range(self.lines)]),
                     self.lines * self.line_height]

    def percent_y(self, percent=0, x=None):
        """ Places Text at given percent on the game app screen height """

        one_percent = self.game.app.HEIGHT / 100
        if x is None:
            self.pos_list = [
                [(self.game.app.WIDTH - self.size_list[i][0]) / 2, percent * one_percent + i * self.line_height] for i
                in range(self.lines)]
        else:
            self.pos_list = [[x, percent * one_percent + i * self.line_height] for i in range(self.lines)]
        return self

    def update_y(self, y, x=None):
        """ Updates Text position at given percent on the game app screen height """

        self.pos[1] = y
        if x is None:
            self.pos_list = [[(self.game.app.WIDTH - self.size_list[i][0]) / 2, y + i * self.line_height] for i in
                             range(self.lines)]
        else:
            self.pos_list = [[x, y + i * self.line_height] for i in range(self.lines)]

    def update(self):
        """ Shows the surface of Text on a game app display """

        [self.game.app.DISPLAY.blit(self.surface_list[i], self.pos_list[i]) for i in range(self.lines)]


class Hexagon(Label):
    """
    Hexagon game object.
    Main game object for the Root Wars.
    """

    surface_size = [300, 300]
    height_scale = 3

    def __init__(self, game, pos=None, color=(255, 255, 255), outline_color=(10, 10, 10), width=5, hexagon_size=None,
                 hex_pos=None, energy=0,
                 text="", font_name="Segoe UI", font_size=60, bold=False, italic=False, smooth=True,
                 foreground=(40, 40, 40), background=None):
        super().__init__(game, text, pos, font_name, font_size, bold, italic, smooth, foreground, background)

        if hex_pos is None:
            self.hex_pos = []
        else:
            self.hex_pos = hex_pos
        self.color = color
        self.outline_color = outline_color
        self.width = width
        if hexagon_size is None:
            self.hexagon_size = [100, 100]
        else:
            self.hexagon_size = [hexagon_size[0] // 2, hexagon_size[1] // 2]
        self.text_surface = self.font.render(self.text, self.smooth, self.foreground, self.background)

        # game variables
        self.energy = energy

        self.draw_hexagon()

    def draw_hexagon(self):
        """ Draw hexagon on its surface """

        self.text_surface = self.font.render(str(int(self.energy)), self.smooth, self.foreground, self.background)
        self.surface = pygame.Surface(self.surface_size)
        self.surface.set_colorkey((0, 0, 0))

        self.pos_list = [[0, math.cos(deg_to_rad(60)) * self.hexagon_size[1] * 2.9 + self.width]]
        for i in range(1, 6):
            p = [
                self.pos_list[i - 1][0] + round(math.sin(deg_to_rad(i * 60)) * self.hexagon_size[0]),
                self.pos_list[i - 1][1] + round(math.cos(deg_to_rad(i * 60)) * self.hexagon_size[1])
            ]
            self.pos_list.append(p)
        for i in self.pos_list:
            i[0] = self.surface_size[0] - i[0] - self.width
            i[1] = self.surface_size[1] - i[1]
        if self.energy > 0:
            pygame.draw.lines(self.surface, self.outline_color, True, self.pos_list, self.width)
            for i in range(int(self.energy)):
                energy_pos_list = []
                for j in self.pos_list:
                    pos = [j[0] - i * self.height_scale, j[1] - i * self.height_scale]
                    energy_pos_list.append(pos)
                color = [self.color[0] - i * self.height_scale * 2 if self.color[0] != 0 else self.color[0],
                         self.color[1] - i * self.height_scale * 2 if self.color[1] != 0 else self.color[1],
                         self.color[2] - i * self.height_scale * 2 if self.color[2] != 0 else self.color[2]]
                color[0] = 0 if color[0] < 0 else color[0]
                color[1] = 0 if color[1] < 0 else color[1]
                color[2] = 0 if color[2] < 0 else color[2]
                color[0] = 255 if color[0] > 255 else color[0]
                color[1] = 255 if color[1] > 255 else color[1]
                color[2] = 255 if color[2] > 255 else color[2]

                pygame.draw.polygon(self.surface, color, energy_pos_list)
                if i % 5 == 0:
                    pygame.draw.lines(self.surface, self.color, True, energy_pos_list, self.width)
        else:
            pygame.draw.polygon(self.surface, self.color, self.pos_list)
            pygame.draw.lines(self.surface, self.outline_color, True, self.pos_list, self.width)

        self.text_surface = self.font.render(str(self.energy), self.smooth, self.foreground, self.background)

    def update(self):
        """ Shows the surface of Hexagon on a game app display """

        self.game.app.DISPLAY.blit(self.surface, [self.pos[0] + self.game.cords[0], self.pos[1] + self.game.cords[1]])
        if self.energy > 0:
            self.game.app.DISPLAY.blit(self.text_surface, [
                self.pos[0] + self.game.cords[0] + self.surface_size[0] - 50 - self.energy * self.height_scale -
                self.text_surface.get_size()[0] / 2,
                self.pos[1] + self.game.cords[1] + self.surface_size[0] - 90 - self.energy * self.height_scale])

    def zoom(self, size, pos):
        """ Zooms Hexagon size and position """

        self.pos = pos
        self.hexagon_size = [size[0] // 2, size[1] // 2]
        self.draw_hexagon()

    def set_color(self, color):
        """ Sets Hexagon color """

        self.color = color
        self.draw_hexagon()

    def set_outline_color(self, color):
        """ Sets Hexagon outline color """

        self.outline_color = color
        self.draw_hexagon()

    def set_energy(self, energy):
        """ Sets Hexagon energy """

        self.energy = energy
        self.draw_hexagon()


class Line(Vector):
    """ Line class for the Root Wars grid map. """

    def __init__(self, game, pos1=None, pos2=None, color=(255, 255, 255), width=5):
        self.game = game

        super().__init__(pos1, pos2)
        self.color = color
        self.width = width

    def update(self):
        """ Draws the Line on game app display """

        pygame.draw.line(self.game.app.DISPLAY, self.color,
                         [self.pos1[0] + self.game.cords[0], self.pos1[1] + self.game.cords[1]],
                         [self.pos2[0] + self.game.cords[0], self.pos2[1] + self.game.cords[1]],
                         self.width)


class Abstract3dLine:
    """ Line for 3d ray cast rendering """

    def __init__(self, game, pos1=None, pos2=None, color=(255, 255, 255), width=5):
        self.game = game

        if pos1 is None:
            self.pos1 = [0, 0, 0]
        else:
            self.pos1 = pos1
        if pos2 is None:
            self.pos2 = [0, 0, 0]
        else:
            self.pos2 = pos2
        self.color = color
        self.width = width

    def update(self):
        """ Draws the Line on game app display """

        pygame.draw.line(self.game.app.DISPLAY, self.color,
                         [self.pos1[0] + self.game.cords[0], self.pos1[1] + self.game.cords[1]],
                         [self.pos2[0] + self.game.cords[0], self.pos2[1] + self.game.cords[1]],
                         self.width)

class Circle:
    def __init__(self, game, center: list, radius: int, color=(255, 255, 255), width=5):
        self.game = game
        self.center = center
        self.radius = radius
        self.color = color
        self.width = width

    def update(self):
        """ Draw circle """

        pygame.draw.circle(self.game.app.DISPLAY, self.color, Pos.add_pos(self.center, self.game.cords), self.radius, self.width)


class Bullet:
    """ Bullet class """

    def __init__(self, game, pos, end_pos, color=(255, 255, 255), angle=None, speed=20, lifetime=60, size=1):
        self.game = game
        self.pos = list(pos)
        self.end_pos = end_pos
        self.color = color
        if angle is None:
            self.angle = -rotate_to_cord(self.pos, self.end_pos) + 90
        else:
            self.angle = angle
        self.speed = speed
        self.counter = 0
        self.lifetime = lifetime
        self.size = size

    def update(self):
        """ Update method """

        pygame.draw.line(self.game.app.DISPLAY, self.color, self.pos, self.end_pos, width=self.size)

        self.pos[0] += math.cos(deg_to_rad(self.angle)) * self.speed
        self.pos[1] += math.sin(deg_to_rad(self.angle)) * self.speed

        # pygame.draw.circle(self.game.app.DISPLAY, (255, 0, 0), self.end_pos, 10)

        if distance(self.pos, self.end_pos) < 10 or self.counter > self.lifetime:
            self.game.bullets.remove(self)

        self.counter += 1


class Enemy:
    """ Interesting enemy class """

    def __init__(self, game, pos=None, size=None, color=(255, 0, 0), angle=0, speed=5, health=1, anchor_point=None, debug=True,
                 vision_angle=180, detect_range=300, stop_range=100, damaged=False):
        self.game = game
        if pos is None:
            self.pos = [0, 0]
        else:
            self.pos = pos
        if size is None:
            self.size = 20
        else:
            self.size = size
        self.color = color
        self.angle = angle
        self.new_angle = int(angle)
        self.new_pos = list(self.pos)

        self.debug = debug
        self.detect_range = detect_range
        self.vision_angle = vision_angle
        self.stop_range = stop_range
        self.walk_range = 100
        if anchor_point is None:
            self.anchor_point = list(self.pos)
        else:
            self.anchor_point = anchor_point
        self.walk_point = None
        self.damaged = damaged
        self.speed = speed
        self.health = health

    def new_walk_point(self, min_distance=70):
        """ Generates realistic positions for random walks """

        pos = [round(self.pos[0]), round(self.pos[1])]
        while True:
            t = [self.anchor_point[0] + random.randint(-self.walk_range // 2, self.walk_range // 2),
                 self.anchor_point[1] + random.randint(-self.walk_range // 2, self.walk_range // 2)]
            if distance(pos, t) > min_distance:
                return t

    def update(self):
        """ Update method """

        # pygame.draw.line(self.game.app.DISPLAY, (255, 255, 255), self.pos,
        #                  [self.pos[0] + math.cos(deg_to_rad(self.angle)) * self.detect_range,
        #                   self.pos[1] + math.sin(deg_to_rad(self.angle)) * self.detect_range], 2)
        pygame.draw.circle(self.game.app.DISPLAY, self.color, self.pos, self.size)
        if self.debug:
            pygame.draw.polygon(self.game.app.DISPLAY, self.color,
                                [self.pos,
                                 [self.pos[0] + math.cos(deg_to_rad(self.angle - self.vision_angle // 2)) * self.detect_range,
                                  self.pos[1] + math.sin(deg_to_rad(self.angle - self.vision_angle // 2)) * self.detect_range],
                                 [self.pos[0] + math.cos(deg_to_rad(self.angle)) * self.detect_range,
                                  self.pos[1] + math.sin(deg_to_rad(self.angle)) * self.detect_range],
                                 [self.pos[0] + math.cos(deg_to_rad(self.angle + self.vision_angle // 2)) * self.detect_range,
                                  self.pos[1] + math.sin(deg_to_rad(self.angle + self.vision_angle // 2)) * self.detect_range]
                                 ], 2)
            pygame.draw.circle(self.game.app.DISPLAY, self.color, self.anchor_point, self.walk_range, 2)
            pygame.draw.circle(self.game.app.DISPLAY, self.color, self.anchor_point, 10, 2)

        if self.is_player_in_vision() or self.damaged:
            self.new_angle = -rotate_to_cord(self.pos, self.game.player.pos) + 90
            if distance(self.game.player.pos, self.pos) > self.stop_range:
                self.new_pos[0] += math.cos(deg_to_rad(self.new_angle)) * self.speed
                self.new_pos[1] += math.sin(deg_to_rad(self.new_angle)) * self.speed
            else:
                self.damaged = False
        elif self.walk_point:
            self.new_angle = -rotate_to_cord(self.pos, self.walk_point) + 90
            if abs(self.new_angle - self.angle) < 2:
                self.new_pos[0] += math.cos(deg_to_rad(self.new_angle)) * self.speed // 2
                self.new_pos[1] += math.sin(deg_to_rad(self.new_angle)) * self.speed // 2
                if distance(self.pos, self.walk_point) < 2:
                    self.walk_point = None
        elif distance(self.pos, self.anchor_point) > self.walk_range:
            self.new_angle = -rotate_to_cord(self.pos, self.walk_point) + 90
            self.walk_point = list(self.anchor_point)
        elif self.game.counter % 600 == 0:  # change every second
            if random.randint(0, 1) == 1:
                self.walk_point = self.new_walk_point()
            else:
                self.new_angle = round(self.angle) + random.randint(-90, 90)

        self.angle = lerp(self.angle, self.new_angle, 0.05)
        if self.angle > 359:
            self.angle = self.angle % 360

        self.pos[0] = lerp(self.pos[0], self.new_pos[0], 0.2)
        self.pos[1] = lerp(self.pos[1], self.new_pos[1], 0.2)

    def is_player_in_vision(self):
        """
        Check if the player is within the enemy's vision area.

        Returns:
            bool: True if the player is in vision, False otherwise.
        """

        # Calculate the vector from enemy to player
        direction_to_player = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])

        # Normalize the direction vector
        distance_to_player = math.sqrt(direction_to_player[0] ** 2 + direction_to_player[1] ** 2)
        if distance_to_player == 0 or distance_to_player > self.detect_range:
            return False  # Player and enemy are in the same position

        normalized_dir_to_player = (direction_to_player[0] / distance_to_player,
                                    direction_to_player[1] / distance_to_player)

        # Calculate the forward direction vector of the enemy
        enemy_forward = (math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle)))

        # Compute the dot product between the forward direction and the direction to the player
        dot_product = (enemy_forward[0] * normalized_dir_to_player[0] +
                       enemy_forward[1] * normalized_dir_to_player[1])

        # Calculate the angle between the vectors (in degrees)
        try:
            angle_to_player = math.degrees(math.acos(dot_product))
        except ValueError:
            return 0

        # Check if the player is within the vision cone
        return angle_to_player <= self.vision_angle / 2

    def damage(self, damage: int):
        """ Damage self """

        self.damaged = True
        self.health -= damage
        if self.health < 1:
            self.game.enemies_count -= 1
            self.game.objects.remove(self)


class Camera:
    """ Camera class to handle world movement """

    def __init__(self, game, width, height):
        self.game = game
        self.width = width
        self.height = height
        self.offset = [0, 0]  # World offset (x, y)

    def apply(self, pos):
        """ Apply camera offset to an object's position """
        return [pos[0] + self.offset[0], pos[1] + self.offset[1]]

    def update(self, player):
        """ Update the camera offset based on the player's position """
        screen_center = [self.width // 2, self.height // 2]
        self.offset[0] = screen_center[0] - player.pos[0]
        self.offset[1] = screen_center[1] - player.pos[1]


class Player:
    """ Player class """

    def __init__(self, game, pos=None, size=None, color=(255, 0, 0), angle=0, speed=5):
        self.game = game
        if pos is None:
            self.pos = [0, 0]
        else:
            self.pos = pos
        if size is None:
            self.size = 20
        else:
            self.size = size
        self.color = color
        self.angle = angle
        self.new_angle = int(angle)
        self.new_pos = list(self.pos)

        self.detect_range = 300
        self.vision_angle = 180
        self.recharge_counter = 0
        self.speed = speed

    def update(self, keys=None, mouse_position=None, mouse_buttons=None):
        if keys is None:
            return
        if mouse_buttons[0] and self.recharge_counter == 0:
            for i in range(10):
                self.recharge_counter = 0
                temp = int(self.angle)
                self.angle += random.randint(-180, 180)
                shoot(self)
                self.angle = int(temp)
        if mouse_buttons[2]:
            for obj in self.game.objects:
                if obj == self:
                    continue
                if not isinstance(obj, Explosive):
                    continue
                angle = -rotate_to_cord(obj.pos, self.pos) + 90
                obj.new_pos[0] += math.cos(deg_to_rad(angle)) * 10
                obj.new_pos[1] += math.sin(deg_to_rad(angle)) * 10
                break

        dx = dy = 0
        if keys[pygame.K_w]:
            dx += math.cos(deg_to_rad(self.angle)) * self.speed
            dy += math.sin(deg_to_rad(self.angle)) * self.speed
        if keys[pygame.K_s]:
            dx -= math.cos(deg_to_rad(self.angle)) * self.speed
            dy -= math.sin(deg_to_rad(self.angle)) * self.speed
        if keys[pygame.K_d]:
            dx += math.cos(deg_to_rad(self.angle + 90)) * self.speed
            dy += math.sin(deg_to_rad(self.angle + 90)) * self.speed
        if keys[pygame.K_a]:
            dx += math.cos(deg_to_rad(self.angle - 90)) * self.speed
            dy += math.sin(deg_to_rad(self.angle - 90)) * self.speed

        for obj in self.game.objects:
            if obj == self:
                continue
            obj.new_pos[0] -= dx
            obj.new_pos[1] -= dy

        def smooth():
            self.pos[0] = lerp(self.pos[0], self.new_pos[0], 0.2)
            self.pos[1] = lerp(self.pos[1], self.new_pos[1], 0.2)

        self.angle = -rotate_to_cord(self.pos, mouse_position) + 90
        pygame.draw.circle(self.game.app.DISPLAY, self.color, self.pos, self.size)
        pygame.draw.polygon(self.game.app.DISPLAY, self.color,
                            [self.pos,
                             [self.pos[0] + math.cos(deg_to_rad(self.angle - self.vision_angle // 2)) * self.detect_range,
                              self.pos[1] + math.sin(deg_to_rad(self.angle - self.vision_angle // 2)) * self.detect_range],
                             [self.pos[0] + math.cos(deg_to_rad(self.angle)) * self.detect_range,
                              self.pos[1] + math.sin(deg_to_rad(self.angle)) * self.detect_range],
                             [self.pos[0] + math.cos(deg_to_rad(self.angle + self.vision_angle // 2)) * self.detect_range,
                              self.pos[1] + math.sin(deg_to_rad(self.angle + self.vision_angle // 2)) * self.detect_range]
                             ], 2)

        smooth()
        if self.recharge_counter > 0:
            self.recharge_counter -= 1

    def damage(self, damage: int):
        """ Damage self """

        pass


class Rock:
    """ Rock class to make game levels more interesting """

    def __init__(self, game, pos=None, size=None, color=(50, 50, 50), angle=0):
        self.game = game
        if pos is None:
            self.pos = [0, 0]
        else:
            self.pos = pos
        if size is None:
            self.size = 20
        else:
            self.size = size
        self.color = color
        self.angle = angle
        self.new_angle = int(angle)
        self.new_pos = list(self.pos)

    def update(self):
        """ Update method """

        # camera_pos = self.game.camera.apply(self.pos)

        pygame.draw.circle(self.game.app.DISPLAY, self.color, self.pos, self.size)

        self.pos[0] = lerp(self.pos[0], self.new_pos[0], 0.02)
        self.pos[1] = lerp(self.pos[1], self.new_pos[1], 0.02)

    def damage(self, damage: int):
        """ Damage self """

        pass


class Explosive:
    """ Explosive class to make game levels more interesting """

    def __init__(self, game, pos=None, size=None, color=(255, 0, 0), angle=0, health=10, explosion_power=100):
        self.game = game
        if pos is None:
            self.pos = [0, 0]
        else:
            self.pos = pos
        if size is None:
            self.size = 20
        else:
            self.size = size
        self.color = color
        self.angle = angle
        self.new_angle = int(angle)
        self.new_pos = list(self.pos)
        self.health = health
        self.explosion_power = explosion_power
        self.explosion_time = 30  # in frames

        self.is_exploding = False
        self.counter = 0

    def update(self):
        """ Update method """

        self.pos[0] = lerp(self.pos[0], self.new_pos[0], 0.02)
        self.pos[1] = lerp(self.pos[1], self.new_pos[1], 0.02)

        if self.is_exploding:
            self.counter += 1
            progress = self.counter / self.explosion_time
            current_size = int(lerp(self.size, self.explosion_power, progress))
            fade_color = (
                int(self.color[0] * (1 - progress)),
                int(self.color[1] * (1 - progress)),
                int(self.color[2] * (1 - progress)),
            )
            pygame.draw.circle(self.game.app.DISPLAY, fade_color, self.pos, current_size, 2)

            if self.counter >= self.explosion_time:
                self.is_exploding = False  # End the explosion animation
                self.game.objects.remove(self)
            return

        pygame.draw.circle(self.game.app.DISPLAY, self.color, self.pos, self.size)

    def damage(self, damage: int):
        """ Damage self """

        self.health -= damage
        if self.health < 1:
            self.explode()

    def explode(self):
        """ Explosion method """

        self.is_exploding = True
        for obj in self.game.objects:
            if obj == self:
                return
            d = distance(self.pos, obj.pos)
            angle = -rotate_to_cord(self.pos, obj.pos) + 90
            if d < 200:
                obj.new_pos[0] += math.cos(deg_to_rad(angle)) * self.explosion_power
                obj.new_pos[1] += math.sin(deg_to_rad(angle)) * self.explosion_power
                if isinstance(obj, Explosive):
                    obj.is_exploding = True
                else:
                    obj.damage(self.explosion_power // 10)


def shoot(self):
    """ Shoot method """

    max_distance = 1000  # Maximum bullet range
    bullet_direction = [math.cos(deg_to_rad(self.angle)), math.sin(deg_to_rad(self.angle))]
    bullet_end = [self.pos[0] + bullet_direction[0] * max_distance,
                  self.pos[1] + bullet_direction[1] * max_distance]

    closest_hit = None
    closest_distance = float('inf')

    # Check for collisions
    for obj in self.game.objects:
        if obj == self:
            continue

        hit_point = line_circle_intersection(self.pos, bullet_end, obj.pos, obj.size)

        if hit_point:
            distance = math.sqrt((hit_point[0] - self.pos[0]) ** 2 + (hit_point[1] - self.pos[1]) ** 2)
            if distance < closest_distance:
                closest_distance = distance
                closest_hit = (hit_point, obj)

    if closest_hit:
        hit_point, hit_object = closest_hit
        bullet_end = hit_point

        hit_object.new_pos[0] += math.cos(deg_to_rad(self.angle)) * 1
        hit_object.new_pos[1] += math.sin(deg_to_rad(self.angle)) * 1

        hit_object.damage(5)

    bullet = Bullet(self.game, self.pos, bullet_end, angle=self.angle)
    self.game.bullets.append(bullet)
