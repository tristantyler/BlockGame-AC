import random
from Settings import chestImages
import Blocks


class HouseObject(object):

    def __init__(self, width, height):
        self.blocksetlist = [Blocks.BlockSet(x * Blocks.mapDict["GRID_SIZE"], y * Blocks.mapDict["GRID_SIZE"], "empty")
                             for y in range(height) for x in range(width)]

        self.poslist = []
        self.drawlist = []
        self.pl = []
        self.buildPositionList(width, height)
        self.randomplace()

        self.fxlist = []

    def randomplace(self):
        for i in range(10):
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            self.place(x, y)

    def place(self,x, y):
        ind = self.poslist[y][x]

        self.blocksetlist[ind] = Blocks.BlockSet(x * Blocks.mapDict["GRID_SIZE"], y * Blocks.mapDict["GRID_SIZE"], "chest")
        self.blocksetlist[ind].image = random.choice(chestImages)
        self.drawlist.append(self.blocksetlist[ind])
        self.pl.append(ind)

    def buildPositionList(self, width, height):
        self.poslist = [[] for _ in range(height)]
        coordx = 0
        coordy = 0

        for i in range(width * height):
            self.poslist[coordy].append(i)
            if coordx == width - 1:
                coordx = 0
                coordy += 1
            else:
                coordx += 1
