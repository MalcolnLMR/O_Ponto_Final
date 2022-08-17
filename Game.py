#  P Ponto Final 
# 
# 
# 
# 
#
######################## Bibliotecas do Python ########################
import math, time
import pygame as pg

######################## Outros Arquivos ########################

import Configs as config
import Menu as menu
import Player as player
import Entity as en
import load
from pygame.locals import *
##from Configs import *

gameloop = True
gameState = "Menu"

######################## Pygame ########################
Canvas = config.initPygame()


######################## Init FPS ########################
clock = pg.time.Clock()
FPS = 0
fpsCounter = 0
actualFPS = 0
configFPS = config.getFps()
prevTime = time.time()
clock.tick(FPS)
now = time.time()
dt = now - prevTime
prevTime = now

######################## Atualizações Globais ########################
def globalTick(displayFPS):
     title = "FPS: " + str(displayFPS)
     pg.display.set_caption(title)


######################## Game Loop ########################
while gameloop:
     Canvas.fill(en.rgbColors[0])

     clock.tick(configFPS)
     now = time.time()
     dt = now - prevTime
     prevTime = now

     FPS += 1
     fpsCounter += 1 * dt
     if fpsCounter >= configFPS * dt:
        actualFPS = FPS
        fpsCounter = 0
        FPS = 0

     if gameState == "Menu":
        pg.mixer.music.load("Sounds\industrial.mp3")
        pg.mixer.music.play(-1)
        menu.draw(gameState, Canvas)
        pg.display.update()
        gameState = menu.tick(gameState)

     elif gameState == "Load_01":
        pg.mixer.music.stop()
        pg.mixer.music.load("Sounds\white_noise_1.mp3")
        pg.mixer.music.play(-1)
        gameState = load.tick(gameState)

     elif gameState == "Game_01":             
        en.draw(gameState, Canvas)
        player.draw(gameState, Canvas)                
        pg.display.update()        
        gameState = player.tick(gameState, dt)
        gameState = en.tick(gameState, dt)

     elif gameState == "Death_Screen":
        pg.mixer.music.stop()
        pg.mixer.music.load("Sounds\industrial.mp3")
        pg.mixer.music.play(-1)
        menu.draw(gameState, Canvas)
        pg.display.update()
        gameState = menu.tick(gameState)

     elif gameState == "Quit":        
        gameloop = False

     globalTick(actualFPS)
     for event in pg.event.get():
        if event.type == QUIT:
            gameloop = False    

pg.display.quit()
print("Fim do Programa")
    


