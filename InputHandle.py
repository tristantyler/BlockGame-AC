from Graphics import *
from Misc import selectInventory
from Settings import globDict, playerDImages, playerLImages, playerRImages, playerUImages

vec = pygame.math.Vector2


def initInputVars():
    keystate = {
        "right": False,
        "left": False,
        "down": False,
        "up": False,
        "buildMap": False,
        "clearMap": False,
        "info": False,
        "enter": False
    }

    mousestate = {
        "mouseKill": False,
        "mouseBuild": False
    }

    return keystate, mousestate


def inputChecker(gameobj):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameobj.close = True
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:  # Moves Right
                if not gameobj.keystate["right"]:
                    gameobj.player.images = playerRImages
                    gameobj.player.imageIndex = 0
                gameobj.keystate["right"] = True
            elif event.key == pygame.K_LEFT:  # Moves Left
                if not gameobj.keystate["left"]:
                    gameobj.player.images = playerLImages
                    gameobj.player.imageIndex = 0
                gameobj.keystate["left"] = True
            elif event.key == pygame.K_DOWN:  # Moves Down
                if not gameobj.keystate["down"]:
                    gameobj.player.images = playerDImages
                    gameobj.player.imageIndex = 0
                gameobj.keystate["down"] = True
            elif event.key == pygame.K_UP:  # Moves Up
                if not gameobj.keystate["up"]:
                    gameobj.player.images = playerUImages
                    gameobj.player.imageIndex = 0
                gameobj.keystate["up"] = True
            elif event.key == pygame.K_o:  # Toggles collision
                if globDict["collisionON"]:
                    print("Collision Turned OFF")
                    gameobj.player.hitright = False
                    gameobj.player.hitleft = False
                    gameobj.player.hitup = False
                    gameobj.player.hitdown = False
                    globDict["collisionON"] = False
                else:
                    print("Collision Turned ON")
                    globDict["collisionON"] = True
            elif event.key == pygame.K_u and not gameobj.houseState:  # Clears out the map
                gameobj.loading = True
                gameobj.draw("Clearing...")
                gameobj.keystate["clearMap"] = True
            elif event.key == pygame.K_b and not gameobj.houseState:  # Builds a new map
                gameobj.loading = True
                gameobj.draw("Building...")
                gameobj.keystate["buildMap"] = True
            elif event.key == pygame.K_p:  # Displays Info
                if gameobj.keystate["info"]:
                    print("Info Turned OFF")
                    gameobj.keystate["info"] = False
                else:
                    print("Info Turned ON")
                    gameobj.keystate["info"] = True
            elif event.key == pygame.K_LEFTBRACKET:  # Slow Down
                gameobj.player.PLAYER_ACC -= 10
                if gameobj.player.PLAYER_ACC < 0:
                    gameobj.player.PLAYER_ACC = 0
            elif event.key == pygame.K_RIGHTBRACKET:  # Speed up
                gameobj.player.PLAYER_ACC += 10
            elif event.key == pygame.K_w and globDict["blockbuild"] == "Chest":
                globDict["selectind"] += 1
                if globDict["selectind"] > globDict["selectmax"]:
                    globDict["selectind"] = 0
                globDict["blockimage"] = chestImages[globDict["selectind"]]
            elif event.key == pygame.K_s and globDict["blockbuild"] == "Chest":
                globDict["selectind"] -= 1
                if globDict["selectind"] < 0:
                    globDict["selectind"] = globDict["selectmax"]
                globDict["blockimage"] = chestImages[globDict["selectind"]]
            elif event.key == pygame.K_i:
                if globDict["inventory"]:
                    globDict["inventory"] = False
                else:
                    globDict["inventory"] = True
            elif event.key == pygame.K_1:  # Select building 'Block'
                if gameobj.houseState:
                    globDict["blockbuild"] = "Chest"
                    globDict["blockimage"] = chestImages[globDict["selectind"]]
                else:
                    globDict["blockbuild"] = "Block"
                    globDict["blockimage"] = blockimages[0]
            elif event.key == pygame.K_2:  # Select building 'Flower'
                globDict["blockbuild"] = "Flower"
                globDict["blockimage"] = pygame.transform.scale(flowerImages[0], (
                    int(mapDict["GRID_SIZE"]), int(mapDict["GRID_SIZE"])))
            elif event.key == pygame.K_3:  # Select building 'House'
                globDict["blockbuild"] = "House"
                globDict["blockimage"] = pygame.transform.scale(houseImages[0], (
                    int(mapDict["GRID_SIZE"]), int(mapDict["GRID_SIZE"])))
            elif event.key == pygame.K_BACKSPACE:  # Close Game
                if gameobj.houseState:
                    globDict["blockbuild"] = "Block"
                    globDict["blockimage"] = blockimages[0]
                gameobj.houseState = False
            elif event.key == pygame.K_RETURN:  # Enter
                gameobj.keystate["enter"] = True
            elif event.key == pygame.K_ESCAPE:  # Close Game
                gameobj.close = True
                break
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                gameobj.keystate["right"] = False
                gameobj.player.image = playerRImages[0]
            elif event.key == pygame.K_LEFT:
                gameobj.keystate["left"] = False
                gameobj.player.image = playerLImages[0]
            elif event.key == pygame.K_DOWN:
                gameobj.keystate["down"] = False
                gameobj.player.image = playerDImages[0]
            elif event.key == pygame.K_UP:
                gameobj.player.image = playerUImages[0]
                gameobj.keystate["up"] = False
            elif event.key == pygame.K_RETURN:  # Enter
                gameobj.keystate["enter"] = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            but1, but2, but3 = pygame.mouse.get_pressed()
            if but3:
                gameobj.mousestate["mouseBuild"] = True
            if but1:
                if globDict["inventory"]:
                    if gameobj.houseState:
                        selectInventory()
                    globDict["inventory"] = False
                else:
                    gameobj.mousestate["mouseKill"] = True
        if event.type == pygame.MOUSEBUTTONUP:
            gameobj.mousestate["mouseKill"] = False
            gameobj.mousestate["mouseBuild"] = False


def mouseHandler(gameobj):
    if gameobj.mousestate["mouseKill"]:  # Turns Blocks into emptyBlocks
        mouseChunkKill(gameobj)
    if gameobj.mousestate["mouseBuild"]:  # Turns emptyBlocks into blocks
        mouseChunkBuild(gameobj)


def keystateHandler(gameobj):
    mouseHandler(gameobj)

    if gameobj.keystate["buildMap"]:  # fills every possible spot with a block
        buildMap(gameobj)
        gameobj.keystate["buildMap"] = False
    elif gameobj.keystate["clearMap"]:  # fills every possible spot with an empty block
        eraseMap(gameobj)
        gameobj.keystate["clearMap"] = False
