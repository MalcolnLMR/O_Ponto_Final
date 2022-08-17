import pygame as pg
import os
from pygame.locals import *
from Configs import *

######################## Declarações ########################
Screen = getScreen()
#[rgbBackground, rgbProta, rgbProton, rgbNeutron, rgbPhoton, rgbBlackHole]
rgbColors = getColors()
buttonWidth = 100
buttonHeigth = 40
ScreenX = Screen[0] 
screenY = Screen[1]

buttonStart = pg.Rect(ScreenX/2 - buttonWidth/2 + 10, screenY/2 - buttonHeigth/2, buttonWidth, buttonHeigth)
buttonRestart = pg.Rect(ScreenX/2 - buttonWidth/2, screenY/2 - buttonHeigth/2, buttonWidth, buttonHeigth)
buttonExit = pg.Rect(ScreenX/2 - 30 , screenY/2 + buttonHeigth, buttonWidth, buttonHeigth)
loseText = pg.Rect(ScreenX/2 - 105, screenY/2 - 30, buttonWidth, buttonHeigth)

pg.font.init()
font = pg.font.Font('freesansbold.ttf', 18)

######################## Iniciando o menu ########################
def draw(gameState, canvas):
    if gameState == "Menu":
        logo = pg.image.load(os.path.join('Sprites', 'logo sem fundo.png'))
        logo = pg.transform.scale(logo, (450, 300))
        canvas.blit(logo, (130, 100))
        
        text_ini = font.render('INICIAR', True, (255, 164, 27))
        canvas.blit(text_ini, buttonStart)
        # pg.draw.rect(canvas, rgbColors[1], buttonStart)

        text_ini = font.render('SAIR', True, (250, 164, 27))
        canvas.blit(text_ini, buttonExit)

        text_cred = font.render('Músicas tiradas de https://www.zapsplat.com', True, (255, 164, 27))
        canvas.blit(text_cred, (175, 700))
    
    elif gameState == "Death_Screen":
        text_ini = font.render('SAIR', True, (255, 164, 27))
        canvas.blit(text_ini, buttonExit)

        text_ini = font.render('O fim de um recomeço.', True, (250, 164, 27))
        canvas.blit(text_ini, loseText)

    

def tick(gameState):
    if gameState == "Menu":
        mousePos = pg.mouse.get_pos()
        if pg.mouse.get_pressed() == (1, 0, 0) and buttonStart.collidepoint(mousePos):
            return "Load_01"
        elif pg.mouse.get_pressed() == (1, 0, 0) and buttonExit.collidepoint(mousePos):
            return "Quit"
        else:
            return "Menu"

    elif gameState == "Tutorial":
        return gameState
    
    elif gameState == "Death_Screen":
        mousePos = pg.mouse.get_pos()
        if pg.mouse.get_pressed() == (1, 0, 0) and buttonExit.collidepoint(mousePos):
            return "Quit"
        elif pg.mouse.get_pressed() == (1, 0, 0) and buttonRestart.collidepoint(mousePos):
            return "Load_01"
        else:
            return "Death_Screen"
        
        
        

