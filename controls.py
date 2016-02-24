import pygame
from pygame.locals import *
import math


class MOUSE:
    LEFT_CLICK = 1
    RIGHT_CLICK = 3
    MIDDLE_CLICK = 2
    WHEEL_UP = 4
    WHEEL_DOWN = 5


class MAP:
    UP = math.atan2(1, 0)
    DOWN = math.atan2(-1, 0)
    LEFT = math.atan2(0, -1)
    RIGHT = math.atan2(0, 1)
    UP_LEFT = math.atan2(1, -1)
    UP_RIGHT = math.atan2(1, 1)
    DOWN_LEFT = math.atan2(-1, -1)
    DOWN_RIGHT = math.atan2(-1, 1)

    key1 = {(K_w,): UP,
            (K_s,): DOWN,
            (K_a,): LEFT,
            (K_d,): RIGHT,
            (K_w, K_a): UP_LEFT,
            (K_w, K_d): UP_RIGHT,
            (K_s, K_a): DOWN_LEFT,
            (K_s, K_d): DOWN_RIGHT
    }

    key2 = {(K_i,): UP,
            (K_k,): DOWN,
            (K_j,): LEFT,
            (K_l,): RIGHT,
            (K_i, K_j): UP_LEFT,
            (K_i, K_l): UP_RIGHT,
            (K_k, K_j): DOWN_LEFT,
            (K_k, K_l): DOWN_RIGHT
    }


class Controls(object):

    def __init__(self, src="MOUSE"):
        self.source = src
        self.joy = None
        self.direction = 0
        self.magnitude = 0
        self.shoot = 0
        self.switch = 0
        self.last_switch = 0
        self.time = 0
        self.mouse_pressed = [0, 0, 0, 0, 0, 0, 0]

    def update(self, td, player):
        #self.shoot = 0
        self.time += td
        if self.source == "KEY1":
            #-------------------------------
            #Movement
            #-------------------------------
            pressed = pygame.key.get_pressed()
            keys = []
            for i in K_w, K_s, K_a, K_d:
                if pressed[i]:
                    keys.append(i)
            keys = tuple(keys)
            if keys in MAP.key1:
                self.magnitude = 1
                self.direction = MAP.key1[keys]
            else:
                self.magnitude = 0

            #--------------------------------
            #Shooting
            #--------------------------------
            self.shoot = pressed[K_SPACE]

            #--------------------------------
            #Switch
            #--------------------------------
            if self.time - self.last_switch > 150 and pressed[K_LALT]:
                self.switch = 1
                self.last_switch = self.time
            else:
                self.switch = 0

        elif self.source == "KEY2":
            #-------------------------------
            #Movement
            #-------------------------------
            pressed = pygame.key.get_pressed()
            keys = []
            for i in K_i, K_k, K_j, K_l:
                if pressed[i]:
                    keys.append(i)
            keys = tuple(keys)
            if keys in MAP.key2:
                self.magnitude = 1
                self.direction = MAP.key2[keys]
            else:
                self.magnitude = 0

            #--------------------------------
            #Shooting
            #--------------------------------
            self.shoot = pressed[K_SPACE]
        elif self.source == "MOUSE":

            #--------------------------------
            #Movement
            #--------------------------------
            x, y = pygame.mouse.get_pos()
            dx = x - player.x
            dy = y - (-player.y)
            dist_sq = math.hypot(dx, dy)
            self.magnitude = (1-math.pow(math.e, -dist_sq/10))
            if self.magnitude < .01:
                self.magnitude = 0
            self.direction = math.atan2(-dy, dx)

            #set current button states
            for event in pygame.event.get(MOUSEBUTTONDOWN):
                self.mouse_pressed[event.button] = 1

            #-----------------------------------
            #Shooting
            #-----------------------------------
            self.shoot = pygame.mouse.get_pressed()[0]

            #-----------------------------------
            #Switching
            #-----------------------------------
            #print (self.mouse_pressed[MOUSE.WHEEL_DOWN] or self.mouse_pressed[MOUSE.WHEEL_UP])
            if self.time - self.last_switch > 150 and (self.mouse_pressed[MOUSE.WHEEL_DOWN] or self.mouse_pressed[MOUSE.WHEEL_UP]):
                if self.mouse_pressed[MOUSE.WHEEL_DOWN]:
                    self.switch = 1
                elif self.mouse_pressed[MOUSE.WHEEL_UP]:
                    self.switch = -1
                self.last_switch = self.time
            else:
                self.switch = 0

            #release the mouse button states
            for event in pygame.event.get(MOUSEBUTTONUP):
                self.mouse_pressed[event.button] = 0
        else:
            #source is a joystick
            direction = math.atan2(self.joy)
