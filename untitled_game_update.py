"""
This file contains main game logic in a Game class
This class is invoked in main.py file
Update method of this class is called every 0.02 seconds (60 FPS (Depends on what the value of self.MAX_FPS is))
"""

import pygame
from objects import *


class Game:
    """
    Root Wars game class
    """

    def __init__(self, app):
        """ Game initialisation """

        # app variables
        self.app = app
        self.mode = "game"
        self.version = "1.0"

        self.objects = []
        self.bullets = []

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
            self.bullets.clear()

        if mode == "game":
            self.mode = mode
            clear()
            self.create_game_objects()

    def spawn_enemy(self):
        """ Spawns enemy """

        self.enemies_count += 1
        pos = [random.randint(0, self.app.WIDTH), random.randint(0, self.app.HEIGHT)]
        self.objects.append(Enemy(self, pos=pos, size=20, anchor_point=pos, debug=False, vision_angle=360, detect_range=1200,
                                  color=(0, 255, 0), stop_range=50, damaged=True))

    def create_game_objects(self):
        """ Creates game objects """

        self.camera = Camera(self, self.app.WIDTH, self.app.HEIGHT)
        self.enemies_count = 0
        for i in range(4):
            self.spawn_enemy()
        self.player = Player(self, pos=[self.app.WIDTH // 2, self.app.HEIGHT // 2], size=20, color=(0, 0, 255))
        self.objects.append(self.player)
        [self.objects.append(Rock(self, [random.randint(0, self.app.WIDTH),
                                         random.randint(0, self.app.HEIGHT)])) for _ in range(5)]
        [self.objects.append(Explosive(self, [random.randint(0, self.app.WIDTH),
                                         random.randint(0, self.app.HEIGHT)])) for _ in range(20)]
        # self.objects.append(Bullet(self, pos=[500, 500], end_pos=[1000, 600]))

    def update(self, mouse_buttons, mouse_position, events, keys):
        """ Main game logic """

        if self.mode == "game":
            self.app.DISPLAY.fill((0, 0, 0))

            self.mouse_position = mouse_position
            self.mouse_buttons = mouse_buttons

            if self.enemies_count < 4:
                self.spawn_enemy()

            for obj in self.objects:
                # obj.pos = self.camera.apply(obj.pos)
                obj.update()
                # obj.pos = mouse_position
            for bullet in self.bullets:
                bullet.update()

            self.player.update(keys, mouse_position, mouse_buttons)

            self.counter += 1
            if self.counter > 1000:
                self.counter = 0
