import os

import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
XMAX_GRID = 100
YMAX_GRID = 100
GRID_SIZE = 48

# Dictionary with any relevant map-related objects
mapDict = {"SCREEN_WIDTH": SCREEN_WIDTH,
           "SCREEN_HEIGHT": SCREEN_HEIGHT,
           "HALF_WIDTH": SCREEN_WIDTH / 2,
           "HALF_HEIGHT": SCREEN_HEIGHT / 2,
           "XMAX_GRID": XMAX_GRID,
           "YMAX_GRID": YMAX_GRID,
           "GRID_SIZE": GRID_SIZE,
           "MAP_WIDTH": GRID_SIZE * XMAX_GRID,
           "MAP_HEIGHT": GRID_SIZE * YMAX_GRID,
           }

# Dictionary of misc variables that need to be accessed by various things
globDict = {"collisionON": False,
            "blockbuild": "Block",
            "blockimage": None,
            "selectind": 0,
            "selectmax": None,
            "inventory": False
            }


class Background:
    """ Creates the background image displayed under everything,
        Splices together the images based on size of the map."""
    image = None

    def __init__(self, filename='resources/grass.png', width=mapDict["XMAX_GRID"], height=mapDict["YMAX_GRID"]):
        img = pygame.image.load(filename).convert_alpha()
        ih = img.get_height()
        iw = img.get_width()
        w = int(width * mapDict["GRID_SIZE"])
        h = int(height * mapDict["GRID_SIZE"])
        bw = int((w / iw) + 0.9)
        bh = int((h / ih) + 0.9)
        self.image = pygame.Surface((w, h))

        count = 0
        for i in range(bh):
            for j in range(bw):
                count += 1
                self.image.blit(img, (j * iw, i * ih))
        print("Prepared Background Image:", count, "images")
        self.rect = self.image.get_rect(topleft=(0, 0))


class Cursor:
    def __init__(self):
        self.rect = cursorImage.get_rect()


class Spritesheet(object):

    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except:
            print('Unable to load spritesheet image:', filename)

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey=None):
        """Loads image from x,y,x+offset,y+offset"""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image


messages = [
    "The Neighbours Have Better Stuff",
    "Now Entering Drama Free Zone",
    "Shut The Front Door!",
    "Come Back When You Have Tacos And Booze",
    "Just So You Know Everyday Is Hump Day For Our Dog",
    "Beware Of Wife Kids Are Also Shady Husband Is Cool",
    "Drop It Like It's Hot",
    "It's Always Happy Hour Here",
    "She Doesn't Even Go Here",
    "Oh NO! Not You Again!"
]

FONT = pygame.font.Font('resources/KaushanScript-Regular.otf', 17)  # Font used when drawing text
housefont = pygame.font.Font('resources/KaushanScript-Regular.otf', 25)

# Screen and Background init
flags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
pygame.display.set_caption("AC")  # Set Title of Window

screen = pygame.display.set_mode((mapDict["SCREEN_WIDTH"], mapDict["SCREEN_HEIGHT"]))  # The overall screen
screenRect = pygame.rect.Rect(0, 0, mapDict["SCREEN_WIDTH"], mapDict["SCREEN_HEIGHT"])
screen.set_alpha(None)  # Set a specific color to be the transparent key
background = pygame.Surface(screen.get_size())  # Surface that everything is drawn on
bg = Background()  # Sets up a Background object to display background image that is layered
bgh = Background('resources/floor.png', 10, 10)  # House Background tile

pygame.mouse.set_visible(False)  # Makes mouse invisible, uses custom cursor
cursorImage = pygame.image.load('resources/cursor.png').convert_alpha()
cursor = Cursor()

""" Images """
sc = Spritesheet('resources/chests/chests.png')  # Image sheet for chests
sp = Spritesheet('resources/dog.png')  # Image sheet for player
ss = Spritesheet('resources/flowers.png')  # Image sheet for flowers
sss = Spritesheet("resources/stuff.png")

signImage = pygame.image.load('resources/sign.png').convert_alpha()
signrect = signImage.get_rect()

houseImages = []
for lvl in os.listdir("resources/houses/"):
    s = 'resources/houses/' + lvl
    img = pygame.image.load(s).convert_alpha()
    img = pygame.transform.scale(img, (mapDict["GRID_SIZE"] * 2, mapDict["GRID_SIZE"] * 2))
    houseImages.append(img)

blockimages = []  # Creates a list of images in the specified folder; can be used for animation
for lvl in os.listdir("resources/tree/"):
    s = 'resources/tree/' + lvl
    img = pygame.image.load(s).convert_alpha()
    img = pygame.transform.scale(img, (mapDict["GRID_SIZE"], mapDict["GRID_SIZE"]))  # Scales image to fit dimensions
    blockimages.append(img)

chestImages = []
for x in range(10):
    image = sc.image_at((x * 32, 0, 32, 32), -1)
    image = pygame.transform.scale(image, (int(mapDict["GRID_SIZE"]), int(mapDict["GRID_SIZE"])))
    chestImages.append(image)

for x in range(8):
    for y in range(16):
        image = sss.image_at((x * 32, y * 32 + 0, 32, 32), -1)
        image = pygame.transform.scale(image, (int(mapDict["GRID_SIZE"]), int(mapDict["GRID_SIZE"])))
        chestImages.append(image)

playerDImages = []
for x in range(3):
    image = sp.image_at((x * 48, 0, 48, 48), -1)
    image = pygame.transform.scale(image, (int(mapDict["GRID_SIZE"] * .9), int(mapDict["GRID_SIZE"] * .9)))
    playerDImages.append(image)

playerLImages = []
for x in range(3):
    image = sp.image_at((x * 48, 48, 48, 48), -1)
    image = pygame.transform.scale(image, (int(mapDict["GRID_SIZE"] * .9), int(mapDict["GRID_SIZE"] * .9)))
    playerLImages.append(image)

playerRImages = []
for x in range(3):
    image = sp.image_at((x * 48, 96, 48, 48), -1)
    image = pygame.transform.scale(image, (int(mapDict["GRID_SIZE"] * .9), int(mapDict["GRID_SIZE"] * .9)))
    playerRImages.append(image)

playerUImages = []
for x in range(3):
    image = sp.image_at((x * 48, 144, 48, 48), -1)
    image = pygame.transform.scale(image, (int(mapDict["GRID_SIZE"] * .9), int(mapDict["GRID_SIZE"] * .9)))
    playerUImages.append(image)

playerImage = playerDImages[0]

flowerImages = []
for x in range(3):
    for y in range(3):
        image = ss.image_at((x * 32, y * 32, 32, 32), -1)
        image = pygame.transform.scale(image, (int(mapDict["GRID_SIZE"] * .75), int(mapDict["GRID_SIZE"] * .75)))
        flowerImages.append(image)

globDict["blockimage"] = blockimages[0]
globDict["selectmax"] = len(chestImages) - 1

# Create Inventory image
box = pygame.Surface((mapDict["GRID_SIZE"], mapDict["GRID_SIZE"]))
box.fill((255, 245, 229))
pygame.draw.rect(box, (72, 188, 167), (0, 0, mapDict["GRID_SIZE"], mapDict["GRID_SIZE"]), 3)

oval = pygame.Surface((mapDict["SCREEN_WIDTH"], mapDict["SCREEN_HEIGHT"]))
oval.blit(bg.image, (0, 0))

count = 0
for i in range(int(mapDict["SCREEN_HEIGHT"]/mapDict["GRID_SIZE"])):
    for j in range(int(mapDict["SCREEN_WIDTH"]/mapDict["GRID_SIZE"])):
        oval.blit(box, (j * mapDict["GRID_SIZE"], i * mapDict["GRID_SIZE"]))
        if count <= globDict["selectmax"]:
            cimg = pygame.transform.scale(chestImages[count], (int(mapDict["GRID_SIZE"] * .75), int(mapDict["GRID_SIZE"] * .75)))
            oval.blit(cimg, (j * mapDict["GRID_SIZE"], i * mapDict["GRID_SIZE"]))
        count += 1


clock = pygame.time.Clock()

