from Blocks import *
from Chunk import findChunk
from Settings import mapDict


def removeBlock(gameobj, x, y):
    try:
        ind = gameobj.poslist[y][x]  # Index in main blocksetlist
        chunk = findChunk(gameobj, x, y)
        i = gameobj.chunklist[chunk].pl.index(ind)  # Chunk Index
    except:
        return

    if gameobj.blocksetlist[ind].blockType != "empty":
        gameobj.blocksetlist[ind] = BlockSet(x * mapDict["GRID_SIZE"], y * mapDict["GRID_SIZE"], "empty")
        gameobj.chunklist[chunk].bl.pop(i)
        gameobj.chunklist[chunk].pl.pop(i)
        gameobj.chunklist[chunk].rl.pop(i)


def removeBlockHouse(houseobj, x, y):
    try:
        ind = houseobj.poslist[y][x]
        i = houseobj.pl.index(ind)
    except:
        return

    if houseobj.blocksetlist[ind].blockType != "empty":
        houseobj.blocksetlist[ind] = BlockSet(x * mapDict["GRID_SIZE"], y * mapDict["GRID_SIZE"], "empty")
        houseobj.drawlist.pop(i)
        houseobj.pl.pop(i)


def wrapText(message, font, xstart, ystart, wrapnum=3, color=(84, 45, 3), linespacing=25):
    lines = int((len(message) / wrapnum)) + 1

    for line in range(lines):
        mes = message[line * wrapnum:line * wrapnum + wrapnum]
        mes = ' '.join(word for word in mes)
        background.blit(font.render(mes, 1, color), (xstart, line * linespacing + ystart))


def createImageTemps(gameobj, xsize, ysize, ind, mousex, mousey):
    for x in range(0, xsize):
        for y in range(ysize):
            if y == 0 and x == 0:
                continue
            try:
                temp = gameobj.poslist[mousey + y][mousex + x]
            except:
                continue

            chunkTemp = findChunk(gameobj, mousex + x, mousey + y)

            gameobj.blocksetlist[temp] = BlockSet((mousex + x) * mapDict["GRID_SIZE"],
                                                  (mousey + y) * mapDict["GRID_SIZE"], "temp")

            gameobj.blocksetlist[temp].origin = [mousex, mousey]
            gameobj.blocksetlist[ind].temps.append([mousex + x, mousey + y])

            gameobj.chunklist[chunkTemp].bl.append(gameobj.blocksetlist[temp])
            gameobj.chunklist[chunkTemp].pl.append(temp)
            gameobj.chunklist[chunkTemp].rl.append(gameobj.blocksetlist[temp].rect)


def createImageTemps2(gameobj, xsize, ysize, ind, mousex, mousey):
    for x in range(0, xsize):
        for y in range(ysize):
            if y == 0 and x == 0:
                continue
            try:
                temp = gameobj.poslist[mousey + y][mousex + x]
            except:
                continue

            gameobj.blocksetlist[temp] = BlockSet((mousex + x) * mapDict["GRID_SIZE"],
                                                  (mousey + y) * mapDict["GRID_SIZE"], "temp")

            gameobj.blocksetlist[temp].origin = [mousex, mousey]
            gameobj.blocksetlist[ind].temps.append([mousex + x, mousey + y])


def Animation(gameobj, x, y, images):
    try:
        ind = gameobj.poslist[y][x]
    except:
        return

    chunk = findChunk(gameobj, x, y)

    if gameobj.blocksetlist[ind].blockType == "empty":
        gameobj.blocksetlist[ind] = BlockSet(x * mapDict["GRID_SIZE"], y * mapDict["GRID_SIZE"], "animation")
        gameobj.blocksetlist[ind].images = images
        gameobj.blocksetlist[ind].image = gameobj.blocksetlist[ind].images[0]
        gameobj.blocksetlist[ind].indexMax = len(images) - 1
        gameobj.chunklist[chunk].bl.append(gameobj.blocksetlist[ind])
        gameobj.chunklist[chunk].pl.append(ind)
        gameobj.chunklist[chunk].rl.append(gameobj.blocksetlist[ind].rect)

        gameobj.fxlist.append([x, y])


def checkAnimation(gameobj, x, y):
    try:
        ind = gameobj.poslist[y][x]
    except:
        return False

    if gameobj.blocksetlist[ind].done:
        removeBlock(gameobj, x, y)
        return True
    else:
        return False


def getMousePos(gameobj):
    tempx, tempy = pygame.mouse.get_pos()
    tempx = int(
        ((tempx + gameobj.player.pos.x) - mapDict["HALF_WIDTH"]) / mapDict["GRID_SIZE"])
    tempy = int(
        ((tempy + gameobj.player.pos.y) - mapDict["HALF_HEIGHT"]) / mapDict["GRID_SIZE"])

    return tempx, tempy


def getMousePosHouse():
    tempx, tempy = pygame.mouse.get_pos()
    tempx = int(tempx / mapDict["GRID_SIZE"])
    tempy = int(tempy / mapDict["GRID_SIZE"])

    return tempx, tempy


def selectInventory():
    mousex, mousey = pygame.mouse.get_pos()
    mousex = int(mousex /mapDict["GRID_SIZE"])
    mousey = int(mousey / mapDict["GRID_SIZE"])

    ind = mousex + mousey*int(mapDict["SCREEN_WIDTH"]/mapDict["GRID_SIZE"])
    if ind > globDict["selectmax"]:
        globDict["selectind"] = globDict["selectmax"]
        globDict["blockimage"] = chestImages[globDict["selectind"]]
    else:
        globDict["selectind"] = ind
        globDict["blockimage"] = chestImages[globDict["selectind"]]


def random_block_color():
    r = random.randint(0, 100)
    g = random.randint(0, 100)
    b = random.randint(200, 255)
    rgbl = [r, g, b]
    return tuple(rgbl)
