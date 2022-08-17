import pygame as pg
import Entity as en
import os
from random import randint
from Configs import getScreen

Screen = getScreen()
screenX = Screen[0]
screenY = Screen[1]

def loadImage(folder, level, img):
	image = pg.image.load(os.path.join(folder, level, img))

	return image

def loadLevelOne(levelY, levelX):

	en.blackHoleList = []
	en.photonList = []
	en.neutronList = []
	for x in range(en.photonQtde):
		
		posX = randint(-levelX, levelX + screenX)
		posY = randint(-levelY, levelY + screenY)
		en.newPhoton(posX, posY)

	for x in range(en.neutronQtde):
	   	posX = randint(-levelX, levelX + screenX)
	   	posY = randint(-levelY, levelY + screenY)
	   	en.newNeutron(posX, posY)

	for x in range(en.blackHoleQtde):		
		posX = randint(-levelX, levelX + screenX)
		posY = randint(-levelY, levelY + screenY)
		en.newBlackHole(posX, posY)

def tick(gameState):
	if gameState == "Load_01":
		levelY = screenX 
		levelX = screenX 
		loadLevelOne(levelY, levelX)
		return "Game_01"
	else:
		return gameState