"""
This file contains the main game logic in a Game class
This class is invoked in main.py file
Update method of this class is called every 0.02 seconds (60 FPS (Depends on what the value of self.MAX_FPS is))
"""

import pygame
from objects import *


class Game:
    """
    Game class
    """

    def __init__(self, app):
        """ Game initialisation """

        # app variables
        self.app = app
        self.mode = "game"
        self.version = "1.0"

        self.objects = []
        self.cords = [self.app.WIDTH // 2, self.app.HEIGHT // 2]

        self.counter = 0

        self.create_game_objects()

    def change_mode(self, mode):
        """
        Changes mode to a new mode if it's matches one of the possible modes,
        clearing all variables of all modes except settings
        """

        def clear():
            """ Clears all variables of all modes except settings """

            self.objects.clear()

        if mode == "game":
            self.mode = mode
            clear()
            self.create_game_objects()

    def create_game_objects(self):
        """ Creates game objects """

        self.line = Line(self, [-200, 0], [200, 0])
        self.circle = Circle(self, [self.app.WIDTH // 2, self.app.HEIGHT // 2], 100)

        self.objects.append(self.line)
        self.objects.append(self.circle)

    def raycast_light(self, origin, circle_center, circle_radius, ray_count=360, max_length=500):
        for angle in range(0, ray_count):
            rad = math.radians(angle)
            x, y = origin
            for i in range(max_length):
                x += math.cos(rad)
                y += math.sin(rad)

                dx = x - circle_center[0]
                dy = y - circle_center[1]
                dist_to_circle = math.sqrt(dx * dx + dy * dy)

                # Проверяем, внутри ли окружности
                if dist_to_circle <= circle_radius:
                    # Затухание по расстоянию от мыши
                    dist_from_origin = math.sqrt((x - origin[0]) ** 2 + (y - origin[1]) ** 2)
                    intensity = max(0, 255 - int(dist_from_origin * 1.2))  # коэффициент 1.2 можно менять
                    color = (intensity, intensity, intensity)
                    self.app.DISPLAY.set_at((int(x), int(y)), color)
                else:
                    if i > circle_radius:
                        break

    def update(self, mouse_buttons, mouse_position, events, keys):
        """ Main game logic """

        if self.mode == "game":
            self.app.DISPLAY.fill((0, 0, 0))

            self.mouse_position = mouse_position
            self.mouse_buttons = mouse_buttons

            # for obj in self.objects:
            #     obj.update()

            pygame.draw.circle(self.app.DISPLAY, (255, 0, 0), self.circle.center, self.circle.radius, 2)

            # self.circle.center = Pos.sub_pos(mouse_position, self.cords)

            pygame.draw.circle(self.app.DISPLAY, (255, 0, 0), self.circle.center, self.circle.radius, 2)
            self.raycast_light(self.mouse_position, self.circle.center, self.circle.radius)

            self.counter += 1
            if self.counter > 1000:
                self.counter = 0
