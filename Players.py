import time

import pygame

from Settings import mapDict, globDict
from Settings import playerImage, playerDImages

vec = pygame.math.Vector2


# noinspection PyArgumentList,PyArgumentList,PyArgumentList,PyArgumentList,PyArgumentList,PyArgumentList,PyArgumentList,PyArgumentList
class Player:
    def __init__(self):
        self.image = playerImage
        self.images = None

        self.rect = self.image.get_rect(topleft=(0, 0))
        self.rect.height -= 2
        self.rect.width -= 2

        self.rectLeft = pygame.rect.Rect(self.rect.x - 3, self.rect.y + 1, 3, self.rect.height * 0.8)
        self.rectRight = pygame.rect.Rect(self.rect.x + self.rect.width, self.rect.y + 1, 3, self.rect.height * 0.8)
        self.rectUp = pygame.rect.Rect(self.rect.x + 1, self.rect.y - 3, self.rect.width * 0.8, 3)
        self.rectDown = pygame.rect.Rect(self.rect.x + 1, self.rect.y + self.rect.height, self.rect.width * 0.8, 3)

        self.rectOuter = pygame.rect.Rect(self.rect.x - 6, self.rect.y - 6, self.rect.width + 14, self.rect.height + 14)

        self.blockType = "player"
        self.startPos = vec(0, 0)
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.timer = time.time()
        self.done = False
        self.imageIndex = 0
        self.indexMax = len(playerDImages) - 1

        self.PLAYER_FRICTIONX = -0.15
        self.PLAYER_FRICTIONY = -0.15
        self.PLAYER_ACC = mapDict["GRID_SIZE"] * .9

        self.hitright = False
        self.hitleft = False
        self.hitup = False
        self.hitdown = False

        self.resetting = False

        self.resources = {
            "wood": 9999
        }

    def reset(self):
        self.pos = vec(self.startPos.x, self.startPos.y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.resetting = False

    def animate(self, freqency=0.5):
        if (time.time() - self.timer) > freqency and not self.imageIndex > self.indexMax:
            self.image = self.images[self.imageIndex]
            self.imageIndex += 1
            if self.imageIndex > self.indexMax:
                self.imageIndex = 0
            self.timer = time.time()

    def update(self, gameobj, seconds):

        if not self.resetting and not gameobj.houseState:
            self.acc = vec(0, 0)
            if gameobj.keystate["right"] and not self.hitright:
                self.acc.x = self.PLAYER_ACC * seconds
                self.animate(0.1)
            if gameobj.keystate["left"] and not self.hitleft:
                self.acc.x = -self.PLAYER_ACC * seconds
                self.animate(0.1)
            if gameobj.keystate["down"] and not self.hitdown:
                self.acc.y = self.PLAYER_ACC * seconds
                self.animate(0.1)
            if gameobj.keystate["up"] and not self.hitup:
                self.acc.y = -self.PLAYER_ACC * seconds
                self.animate(0.1)

            self.acc.x += self.vel.x * self.PLAYER_FRICTIONX
            self.acc.y += self.vel.y * self.PLAYER_FRICTIONY
            self.acc.y = self.acc.y

            self.vel += self.acc

            gameobj.player.pos += self.vel + mapDict["GRID_SIZE"] * seconds * self.acc

            self.rect.topleft = self.pos
            self.rectLeft.topleft = (self.rect.x - 3, self.rect.y + 3)
            self.rectRight.topleft = (self.rect.x + self.rect.width, self.rect.y + 3)
            self.rectUp.topleft = (self.rect.x + 3, self.rect.y - 3)
            self.rectDown.topleft = (self.rect.x + 3, self.rect.y + self.rect.height)

            self.rectOuter.topleft = (self.rect.x - 6, self.rect.y - 6)

        if globDict["collisionON"]:

            if self.rectLeft.collidelistall(gameobj.drawrect) or gameobj.player.pos.x < 0:
                self.hitleft = True
                self.vel.x = 0
                self.acc.x = 0
                # print("Left side hit")
            else:
                self.hitleft = False
            if self.rectRight.collidelistall(gameobj.drawrect) or gameobj.player.pos.x > mapDict["MAP_WIDTH"] - 48:
                self.hitright = True
                self.vel.x = 0
                self.acc.x = 0
                # print("Right side hit")
            else:
                self.hitright = False

            if self.rectUp.collidelistall(gameobj.drawrect) or gameobj.player.pos.y < 0:
                self.hitup = True
                self.vel.y = 0
                self.acc.y = 0
                # print("Top side hit")
            else:
                self.hitup = False
            if self.rectDown.collidelistall(gameobj.drawrect) or gameobj.player.pos.y > mapDict["MAP_HEIGHT"] - 48:
                self.hitdown = True
                self.vel.y = 0
                self.acc.y = 0
                # print("Bot side hit")
            else:
                self.hitdown = False
