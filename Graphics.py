from Blocks import *
from Chunk import *
from Misc import removeBlock, getMousePos, createImageTemps, Animation, getMousePosHouse, removeBlockHouse, wrapText


def draw(gameobj, loadText="Loading..."):
    if globDict["inventory"]:
        background.blit(oval, (0, 0))

        cursor.rect.center = pygame.mouse.get_pos()

        background.blit(cursorImage, cursor.rect)

        screen.blit(background, (0, 0))
    elif not gameobj.loading and not gameobj.houseState:
        chunkDraw(gameobj)
        uiList = updateUIText(gameobj)

        background.fill((66, 203, 245))
        background.blit(bg.image, gameobj.camera.apply(bg))

        # Draws every block in drawlist(i.e the viewsize area)
        [background.blit(gameobj.drawlist[i].image, gameobj.camera.apply(gameobj.drawlist[i])) and gameobj.drawlist[
            i].update() for i in range(len(gameobj.drawlist))]

        background.blit(gameobj.player.image, gameobj.camera.apply(gameobj.player))

        for elt in uiList:
            elt.draw(background)
        background.blit(globDict["blockimage"], (mapDict["HALF_WIDTH"] - mapDict["GRID_SIZE"], mapDict["SCREEN_HEIGHT"] - mapDict["GRID_SIZE"]))

        # Draws the cursor image and sets it at the current mouse pos
        cursor.rect.center = pygame.mouse.get_pos()

        background.blit(cursorImage, cursor.rect)

        # Blits the whole background as one image to the screen
        screen.blit(background, (0, 0))
    elif gameobj.loading:  # Draws the loading screen, with optional loadtext string rendered
        print(loadText)
        background.fill((66, 203, 245))
        background.blit(bg.image, (0, 0))

        background.blit(
            pygame.font.Font('resources/KaushanScript-Regular.otf', 72).render(loadText, 1, (255, 255, 255)),
            (mapDict["HALF_WIDTH"] - 100, mapDict["HALF_HEIGHT"] - 100))
        screen.blit(background, (0, 0))
        gameobj.loading = False
        pygame.display.update()

    elif gameobj.houseState:  # Draws the loading screen, with optional loadtext string rendered
        uiList = updateUIText(gameobj)

        origin = gameobj.house.origin
        tempind = gameobj.poslist[origin[1]][origin[0]]
        ho = gameobj.blocksetlist[tempind]

        background.blit(bg.image, (0, 0))
        background.blit(bgh.image, (0, 0))

        background.blit(signImage, ((mapDict["GRID_SIZE"] * 10.25), 100))

        wrapText(ho.message, housefont, mapDict["GRID_SIZE"] * 11, 160)

        [background.blit(ho.houseobj.drawlist[i].image, ho.houseobj.drawlist[i].rect) for i in
         range(len(ho.houseobj.drawlist))]

        for elt in uiList:
            elt.draw(background)

        background.blit(globDict["blockimage"], (mapDict["HALF_WIDTH"] - mapDict["GRID_SIZE"], mapDict["SCREEN_HEIGHT"] - mapDict["GRID_SIZE"]))

        cursor.rect.center = pygame.mouse.get_pos()

        background.blit(cursorImage, cursor.rect)

        screen.blit(background, (0, 0))


def chunkDraw(gameobj):
    if len(gameobj.chunklist) > 0:
        px = int(gameobj.player.pos.x / mapDict["GRID_SIZE"])
        py = int(gameobj.player.pos.y / mapDict["GRID_SIZE"])

        chunknum = findChunk(gameobj, px, py)

        gameobj.drawlist = []
        gameobj.drawrect = []

        gameobj.drawlist += gameobj.chunklist[chunknum].bl
        gameobj.drawrect += gameobj.chunklist[chunknum].rl

        for i in gameobj.chunklist[chunknum].neighbors:
            gameobj.drawlist += gameobj.chunklist[i].bl
            gameobj.drawrect += gameobj.chunklist[i].rl


def buildMap(gameobj):
    start_time = time.time()

    gameobj.buildPositionList()
    gameobj.buildBlockListMap()

    print("Took", time.time() - start_time, "secs to build")


def eraseMap(gameobj):
    start_time = time.time()

    gameobj.buildBlockListEmpty()

    print("Took", time.time() - start_time, "secs to erase")


def updateUIText(gameobj):
    """Returns a list of a ll the UI elements that should be rendered"""
    lst = []
    gameobj.fpsbox = TextBox(0, mapDict["SCREEN_HEIGHT"]-20, 100, 20, "FPS:" + str(int(clock.get_fps())))
    lst.append(gameobj.fpsbox)

    buildselected = TextBox(mapDict["HALF_WIDTH"], mapDict["SCREEN_HEIGHT"]-20, 100, 20, (globDict["blockbuild"]))
    buildimage = TextBox(mapDict["HALF_WIDTH"] - mapDict["GRID_SIZE"] - 3, mapDict["SCREEN_HEIGHT"]-mapDict["GRID_SIZE"], mapDict["GRID_SIZE"] + 3,
                         mapDict["GRID_SIZE"] + 3, " ")
    resources = TextBox(mapDict["HALF_WIDTH"] + 100, mapDict["SCREEN_HEIGHT"]-20, 100, 20, ("Wood: " + str(gameobj.player.resources["wood"])))

    lst.append(resources)
    lst.append(buildselected)
    lst.append(buildimage)

    if gameobj.player.rectUp.collidelistall(gameobj.drawrect):
        collidingobject = gameobj.drawlist[gameobj.player.rectUp.collidelistall(gameobj.drawrect)[0]]
        if collidingobject.blockType in ("temp", "house"):
            if not gameobj.houseState and gameobj.keystate["enter"]:
                gameobj.houseState = True
                globDict["blockbuild"] = "Chest"
                globDict["blockimage"] = chestImages[globDict["selectind"]]
                gameobj.house = collidingobject

    if gameobj.keystate["info"]:
        x = int(gameobj.player.pos.x / mapDict["GRID_SIZE"])
        px = TextBox(0, 20, 100, 20, "X:" + str(x))
        y = int(gameobj.player.pos.y / mapDict["GRID_SIZE"])
        py = TextBox(0, 40, 100, 20, "Y:" + str(y))

        tempx, tempy = getMousePos(gameobj)

        mx = TextBox(100, 20, 100, 20, "MX:" + str(int(tempx)))
        my = TextBox(100, 40, 100, 20, "MY:" + str(int(tempy)))
        try:
            ind = gameobj.poslist[tempy][tempx]
            mouseOverType = TextBox(100, 60, 100, 20, "MO:" + str(gameobj.blocksetlist[ind].blockType))
            mouseOverRect = TextBox(100, 80, 200, 20, str(gameobj.blocksetlist[ind].rect))
            mouseOverIndex = TextBox(100, 100, 100, 20, "ID:" + str(ind))
            lst.append(mouseOverRect)
            lst.append(mouseOverType)
            lst.append(mouseOverIndex)

            col = TextBox(0, 200, 150, 20, "Col UP: " + str(collidingobject.blockType))
            lst.append(col)
        except:
            pass

        pvel = TextBox(0, 60, 100, 20, "Vel:" + str(int(gameobj.player.vel.x)) + ", " + str(int(gameobj.player.vel.y)))

        chunkNum = TextBox(0, 80, 100, 20, "Chunk:" + str(findChunk(gameobj, x, y)))
        drawwlistLen = TextBox(0, 100, 100, 20, "Objects:" + str(len(gameobj.drawlist)))
        entlistLen = TextBox(0, 120, 100, 20, "Entities:" + str(len(gameobj.entlist)))
        colON = TextBox(0, 140, 100, 20, "Col:" + str(globDict["collisionON"]))
        curtime = TextBox(0, 160, 100, 20, "Time:" + str(int(time.time() - gameobj.startTime)))
        buildtypebox = TextBox(0, 180, 100, 20, (globDict["blockbuild"]))

        lst.append(buildtypebox)

        lst.append(pvel)
        lst.append(px)
        lst.append(my)
        lst.append(mx)
        lst.append(py)
        lst.append(chunkNum)
        lst.append(drawwlistLen)
        lst.append(entlistLen)
        lst.append(colON)
        lst.append(curtime)
    return lst


def mouseChunkBuild(gameobj):
    if not gameobj.houseState:
        mousex, mousey = getMousePos(gameobj)

        try:
            ind = gameobj.poslist[mousey][mousex]
            ind2 = gameobj.poslist[mousey + 1][mousex + 1]
            ind3 = gameobj.poslist[mousey][mousex + 1]
            ind4 = gameobj.poslist[mousey + 1][mousex]
        except:
            return

        empty = [gameobj.blocksetlist[ind].blockType, gameobj.blocksetlist[ind2].blockType,
                 gameobj.blocksetlist[ind3].blockType, gameobj.blocksetlist[ind4].blockType]
        empty = list(set(empty))

        chunk = findChunk(gameobj, mousex, mousey)

        if gameobj.blocksetlist[ind].blockType == "empty":
            if globDict["blockbuild"].lower() in ("block", "flower"):
                gameobj.blocksetlist[ind] = BlockSet(mousex * mapDict["GRID_SIZE"], mousey * mapDict["GRID_SIZE"],
                                                     globDict["blockbuild"].lower())
                gameobj.chunklist[chunk].bl.append(gameobj.blocksetlist[ind])
                gameobj.chunklist[chunk].pl.append(ind)
                if globDict["blockbuild"].lower() == "flower":
                    # Makes it so player won't collide with them
                    gameobj.chunklist[chunk].rl.append(pygame.rect.Rect(-10, -10, 0, 0))
                else:
                    gameobj.chunklist[chunk].rl.append(gameobj.blocksetlist[ind].rect)
            elif globDict["blockbuild"].lower() == "house" and len(empty) == 1 and empty[0] == "empty":
                gameobj.blocksetlist[ind] = BlockSet(mousex * mapDict["GRID_SIZE"], mousey * mapDict["GRID_SIZE"],
                                                     globDict["blockbuild"].lower())
                createImageTemps(gameobj, 2, 2, ind, mousex, mousey)
                gameobj.chunklist[chunk].bl.append(gameobj.blocksetlist[ind])
                gameobj.chunklist[chunk].pl.append(ind)
                gameobj.chunklist[chunk].rl.append(gameobj.blocksetlist[ind].rect)

    elif gameobj.player.resources["wood"] > 0:
        origin = gameobj.house.origin
        tempind = gameobj.poslist[origin[1]][origin[0]]
        ho = gameobj.blocksetlist[tempind]

        mousex, mousey = getMousePosHouse()

        try:
            ind = ho.houseobj.poslist[mousey][mousex]
        except:
            return

        if ho.houseobj.blocksetlist[ind].blockType == "empty":
            if globDict["blockbuild"].lower() in ("chest", "flower"):
                ho.houseobj.blocksetlist[ind] = BlockSet(mousex * mapDict["GRID_SIZE"], mousey * mapDict["GRID_SIZE"],
                                                         globDict["blockbuild"].lower())
                ho.houseobj.drawlist.append(ho.houseobj.blocksetlist[ind])
                ho.houseobj.pl.append(ind)
                gameobj.player.resources["wood"] -= 1


def mouseChunkKill(gameobj):
    if not gameobj.houseState:
        mousex, mousey = getMousePos(gameobj)

        try:
            ind = gameobj.poslist[mousey][mousex]
        except:
            return

        if gameobj.blocksetlist[ind].blockType != "empty":
            if gameobj.blocksetlist[ind].blockType == "temp":
                mousex, mousey = gameobj.blocksetlist[ind].origin[0], gameobj.blocksetlist[ind].origin[1]
                ind = gameobj.poslist[mousey][mousex]
            if gameobj.blocksetlist[ind].blockType not in "animation":
                if gameobj.blocksetlist[ind].blockType == "house":
                    for temp in gameobj.blocksetlist[ind].temps:
                        removeBlock(gameobj, temp[0], temp[1])
                removeBlock(gameobj, mousex, mousey)
                gameobj.player.resources["wood"] += 1

    else:
        origin = gameobj.house.origin
        tempind = gameobj.poslist[origin[1]][origin[0]]
        ho = gameobj.blocksetlist[tempind]

        mousex, mousey = getMousePosHouse()

        try:
            ind = ho.houseobj.poslist[mousey][mousex]
        except:
            return

        if ho.houseobj.blocksetlist[ind].blockType != "empty":
            if ho.houseobj.blocksetlist[ind].blockType not in ("animation", "house", "temp"):
                removeBlockHouse(ho.houseobj, mousex, mousey)
                gameobj.player.resources["wood"] += 1


class TextBox:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (30, 30, 30)
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.bkground = pygame.Surface((w, h))
        self.bkground.fill((255, 245, 229))

    def draw(self, screen):
        self.bkground.blit(self.txt_surface, (2, -3))
        screen.blit(self.bkground, (self.rect.x, self.rect.y))
        pygame.draw.rect(screen, (72, 188, 167), self.rect, 2)

    def __str__(self):
        return self.text
