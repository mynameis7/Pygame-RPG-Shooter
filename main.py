__author__ = 'Andrew'

import pygame
from pygame.locals import *
import sys
import sprites
import player
import weapon
import constants as C


def terminate():
    pygame.quit()
    sys.exit()


def test(playr=None):
    DISPLAYSURF = C.DISPLAYSURF

    player1 = player.Player()
    playerSP = sprites.PlayerSpr(player1)
    if playr:
        playerSP = sprites.PlayerSpr(playr)
    player1.equipped = weapon.generate_weapon("Machine Gun")

    clock = pygame.time.Clock()

    while True:
        DISPLAYSURF.fill(C.COLOR.BLACK)

        td = clock.tick(C.FPS)
        playerSP.update(td)
        playerSP.bullets.draw(DISPLAYSURF)
        DISPLAYSURF.blit(playerSP.image, playerSP.rect)
        C.EFFECTS.update(td)
        C.EFFECTS.draw(C.GAME_SURF)
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
        pygame.display.update()


def init():
    FLAGS = DOUBLEBUF #| FULLSCREEN
    pygame.init()
    C.DISPLAYSURF = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT), FLAGS)
    C.DISPLAY_RECT = C.DISPLAYSURF.get_rect()

    C.GAME_RECT = pygame.Rect(0, 0, C.GAME_WIDTH, C.GAME_HEIGHT)
    C.GAME_SURF = C.DISPLAYSURF.subsurface(C.GAME_RECT)

    C.UI_RECT = pygame.Rect(C.GAME_WIDTH, 0, C.UI_WIDTH, C.UI_HEIGHT)
    C.UI_SURF = C.DISPLAYSURF.subsurface(C.UI_RECT)

    C.KILL_RECT = C.GAME_RECT.inflate(0, 256)
    C.KILL_RECT.center = C.GAME_RECT.center

    C.ENEMIES = pygame.sprite.Group()
    C.EFFECTS = pygame.sprite.Group()

def main(testing=False):
    init()
    player1 = player.Player()
    print C.GAME_RECT.center
    x, y = C.GAME_RECT.center
    player1.x, player1.y = x, -y
    player1SP = sprites.PlayerSpr(player1)
    clock = pygame.time.Clock()
    while True:
        C.GAME_SURF.fill(C.COLOR.BLACK)
        C.UI_SURF.fill(C.COLOR.WHITE)
        td = clock.tick(C.FPS)
        player1SP.update(td)
        player1SP.bullets.draw(C.GAME_SURF)
        C.GAME_SURF.blit(player1SP.image, player1SP.rect)
        C.EFFECTS.update(td)
        C.EFFECTS.draw(C.GAME_SURF)
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
        pygame.display.update()


if __name__ == "__main__":
    main()
