import pygame as pg
from pygame.locals import *

def initPygame():
    Screen = getScreen()
    pg.init()
    Canvas = pg.display.set_mode(Screen, 0, 32)
    pg.display.set_caption("Iniciando")
    return Canvas

######################## INPUT ########################

def getScreen():
    Configs = open("Configs.txt", "r")

    aux = Configs.readline().strip()
    listTemp = aux.split(';')
    screenX = int(listTemp[0])
    screenY = int(listTemp[1])

    Configs.close()

    return (screenX, screenY)

def getFps():    
    Configs = open("Configs.txt", "r")
    #pular primeira linha
    aux = Configs.readline().strip()
    
    aux = Configs.readline().strip()
    listTemp = aux.split(';')
    FPS = int(listTemp[0])

    Configs.close()

    return FPS

def getColors():
    Configs = open("Configs.txt", "r")
    #pular primeira e segunda linha
    aux = Configs.readline().strip()    
    aux = Configs.readline().strip()
    ##[rgbBackground, rgbProta, rgbProton, rgbNeutron, rgbPhoton, rgbBlackHole]

    RGB = []
    for color in range(7):
        aux = Configs.readline().strip()
        listTemp = aux.split(';')
        for x in range(3):
            listTemp[x] = int(listTemp[x])
        RGB.append(tuple(listTemp))

    Configs.close() 

    return RGB

def getProtaColor():
    colors = getColors()
    return colors[1]

def getBaseSize():
    baseSize = 10
    return baseSize    


######################## OUTPUT ########################

def saveScreen(x, y):
    Configs = open("Configs.txt", "r")
    listOfLines = Configs.readlines()
    print(listOfLines)
    listOfLines[0] = "{}; {};\n".format(x, y)
    Configs = open("Configs.txt", "w")    
    Configs.writelines(listOfLines)
    Configs.close()

def saveFps(FPS):
    Configs = open("Configs.txt", "r")
    listOfLines = Configs.readlines()
    print(listOfLines)
    listOfLines[1] = "{};\n".format(FPS)
    Configs = open("Configs.txt", "w")
    Configs.writelines(listOfLines)    

    Configs.close()

def saveRgbProta(r, g, b):
    Configs = open("Configs.txt", "r")
    listOfLines = Configs.readlines()
    print(listOfLines)
    listOfLines[3] = "{};{};{}\n".format(r, g, b)
    Configs = open("Configs.txt", "w")
    Configs.writelines(listOfLines)    

    Configs.close()

######################## Load ########################

##def load(FPS):
    
    
    

    
    
