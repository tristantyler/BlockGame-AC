import random
import time

import HouseObject
from Settings import *

vec = pygame.math.Vector2


class Block(object):
    __slots__ = ('x', 'y', 'size', 'blockType')

    def __init__(self, x=0, y=0, blockType="empty"):
        self.x = x
        self.y = y
        self.blockType = blockType


class BlockSet(Block):

    # noinspection PyArgumentList
    def __init__(self, x=0, y=0, blockType="empty"):
        Block.__init__(self, x, y, blockType)

        self.pos = vec(int(x / mapDict["GRID_SIZE"]), int(y / mapDict["GRID_SIZE"]))

        self.imageIndex = 0
        self.timer = time.time()

        self.done = False

        self.rect = pygame.rect.Rect(self.x, self.y, mapDict["GRID_SIZE"],
                                     mapDict["GRID_SIZE"])

        if self.blockType == "empty":
            self.image = pygame.Surface((mapDict["GRID_SIZE"], mapDict["GRID_SIZE"])).convert()
        elif self.blockType == "temp":
            self.image = pygame.Surface((0, 0)).convert()
            self.origin = None
        elif self.blockType == "animation":
            self.images = None
            self.image = None
            self.indexMax = None
        elif self.blockType == "block":
            self.image = random.choice(blockimages)
        elif self.blockType == "chest":
            self.image = chestImages[globDict["selectind"]]
        elif self.blockType == "flower":
            self.indexMax = len(flowerImages) - 1
            self.image = random.choice(flowerImages)
        elif self.blockType == "house":
            self.indexMax = len(houseImages) - 1
            self.image = random.choice(houseImages)
            self.rect = pygame.rect.Rect(self.x, self.y, mapDict["GRID_SIZE"] * 2, mapDict["GRID_SIZE"] * 2)
            self.temps = []
            self.message = random.choice(messages).split()
            self.origin = (int(self.pos.x), int(self.pos.y))
            self.houseobj = HouseObject.HouseObject(10, 10)

    def update(self):
        if self.blockType == "point":
            self.animate(0.3)
        elif self.blockType == "animation":
            if not self.done:
                self.animate2(0.1)

    def animate2(self, freqency=0.5):
        if (time.time() - self.timer) > freqency and not self.imageIndex > self.indexMax:
            self.image = self.images[self.imageIndex]
            self.imageIndex += 1
            self.timer = time.time()
        if self.imageIndex > self.indexMax:
            self.done = True

    def animate(self, freqency=0.5):
        if (time.time() - self.timer) > freqency and not self.imageIndex > self.indexMax:
            self.image = self.images[self.imageIndex]
            self.imageIndex += 1
            if self.imageIndex > self.indexMax:
                self.imageIndex = 0
                pass
            self.timer = time.time()

    def __str__(self):
        return self.blockType
