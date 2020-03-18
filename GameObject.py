import MapGenerator
from Cameras import *
from InputHandle import *
from Misc import checkAnimation, createImageTemps2
from Players import *


class GameObject(object):

    def __init__(self):

        self.keystate, self.mousestate = initInputVars()  # Sets up Mouse/Key States

        self.blocksetlist = []  # Initializes the list for all the blocks, entities, levels
        self.chunklist = []  # Contains all the chunks that get generated once the map is built
        self.entlist = []  # Contains all the entities in the world

        self.player = Player()  # Setup a player

        self.poslist = []  # Position list used to quickly look up blocks
        self.buildPositionList()

        self.camera = Camera(simple_camera, mapDict["MAP_WIDTH"], mapDict["MAP_HEIGHT"])
        self.fpsbox = TextBox(0, 0, 80, 20, "")
        self.drawlist = []
        self.drawrect = []

        self.fxlist = []  # List of active animations

        self.end = 0
        self.start = time.time()
        self.startTime = time.time()  # the starting time for total time spent in app

        self.loading = True
        self.houseState = False  # Toggle whether inside house
        self.house = None  # Holds house object

        draw(self)
        buildMap(self)

        self.close = False

    def update(self):
        self.end = time.time()
        self.player.update(self, self.end - self.start)
        inputChecker(self)
        keystateHandler(self)
        for fx in self.fxlist:
            if checkAnimation(self, fx[0], fx[1]):
                self.fxlist.remove(fx)
        self.camera.update(self.player)
        self.start = time.time()

    def draw(self, loadtext="Loading..."):
        draw(self, loadtext)  # Graphics.draw

    def buildPositionList(self):
        self.poslist = [[] for _ in range(mapDict["YMAX_GRID"])]
        coordx = 0
        coordy = 0

        for i in range(mapDict["XMAX_GRID"] * mapDict["YMAX_GRID"]):
            self.poslist[coordy].append(i)
            if coordx == mapDict["XMAX_GRID"] - 1:
                coordx = 0
                coordy += 1
            else:
                coordx += 1

    def buildBlockListMap(self):
        self.blocksetlist = MapGenerator.getMap(mapDict["XMAX_GRID"], mapDict["YMAX_GRID"], random.random(), 32)
        count = 0
        temps = []
        h = 0
        for y in range(mapDict["YMAX_GRID"]):
            for x in range(mapDict["XMAX_GRID"]):
                if count not in temps:
                    if self.blocksetlist[count] == 1:
                        self.blocksetlist[count] = BlockSet(x * mapDict["GRID_SIZE"], y * mapDict["GRID_SIZE"], "block")
                    elif random.randint(0, 8) == 1:
                        self.blocksetlist[count] = BlockSet(x * mapDict["GRID_SIZE"], y * mapDict["GRID_SIZE"], "flower")
                    elif random.randint(0, 100) == 1:
                        try:
                            ind2 = self.poslist[y + 1][x]
                            ind3 = self.poslist[y][x + 1]
                            ind4 = self.poslist[y + 1][x + 1]
                        except:
                            self.blocksetlist[count] = BlockSet(x * mapDict["GRID_SIZE"], y * mapDict["GRID_SIZE"], "empty")
                            continue
                        temp = list({self.blocksetlist[ind2], self.blocksetlist[ind3], self.blocksetlist[ind4]})
                        if len(temp) == 1 and temp[0] == 0:
                            temps.append(ind2)
                            temps.append(ind3)
                            temps.append(ind4)
                            self.blocksetlist[count] = BlockSet(x * mapDict["GRID_SIZE"], y * mapDict["GRID_SIZE"], "house")
                            createImageTemps2(self, 2, 2, count, x, y)
                            h +=1
                        else:
                            self.blocksetlist[count] = BlockSet(x * mapDict["GRID_SIZE"], y * mapDict["GRID_SIZE"], "empty")
                    else:
                        self.blocksetlist[count] = BlockSet(x * mapDict["GRID_SIZE"], y * mapDict["GRID_SIZE"], "empty")
                count += 1
        print(h)
        getChunks(self)

    def buildBlockListEmpty(self):
        self.blocksetlist = [BlockSet(x * mapDict["GRID_SIZE"], y * mapDict["GRID_SIZE"], "empty") for y in
                             range(mapDict["YMAX_GRID"]) for x in range(mapDict["XMAX_GRID"])]
        getChunks(self)
