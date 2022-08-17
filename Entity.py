import pygame as pg
import Player as p
import os, math
from Configs import getColors, getScreen, getBaseSize, getFps
from load import loadImage
from random	import randint

######################## INIT ########################
#[rgbBackground, rgbProta, rgbProton, rgbNeutron, rgbPhoton, rgbBlackHole]
rgbColors = getColors()
Screen = getScreen()
baseSize = getBaseSize()
configFPS = getFps()
screenX = Screen[0]
screenY = Screen[1]
offset = 0



######################## Photons ########################
photonList, photonCoordList = [], []
photonSize = 5 
photonQtde = 50
photonGain = 4
rgbPhoton = rgbColors[4]
#photonSprite = pg.image.load(os.path.join('Sprites', 'photon.png'))
photonSprite = loadImage('Sprites', 'fase_01', 'ponto_comum_ver2_01.png')
photonSprite = pg.transform.scale(photonSprite, (photonSize, photonSize))

def newPhoton(posX, posY):
    new = pg.Rect(posX - photonSize, posY - photonSize, photonSize, photonSize)
    #new.center = new.w//2, new.h//2
    photonList.append(new)

def delPhoton(obj):
	photonList.remove(obj)

######################## Neutrons ########################
neutronList, neutronCoordList = [], []
neutronQtde = 50
neutronGain = -10
neutronSize = 14 
rgbNeutron = rgbColors[3]
#neutronSprite = pg.image.load(os.path.join('Sprites', 'neutron.png'))
neutronSprite = loadImage('Sprites', 'fase_01', 'ponto_comum_ver1_01.png')
neutronSprite = pg.transform.scale(neutronSprite, (neutronSize, neutronSize))

def newNeutron(posX, posY):
    new = pg.Rect(posX - neutronSize, posY - neutronSize, neutronSize, neutronSize)
    #new.center = new.w//2, new.h//2
    neutronList.append(new)

######################## Black Holes ########################
blackHoleList, blackHoleCoordList = [], []
blackHoleQtde = 20
blackHoleGain = -5
blackHoleSize = 48*2
blackHoleTimer = 0
BlackHoleHp = 3
blackHoleCircleCollider = 48 + 48
BlackHoleDmgPS = 1
rgbBlackHole = rgbColors[5]

fpsCounterRotateBH = 0
blackHoleRotateTimer = 0.1
blackHoleSpriteAngle = 0
rotateBlackHoles = True

#blackHoleSprite = pg.image.load(os.path.join('Sprites', 'blackHole.png'))
#blackHoleSprite = pg.transform.scale(blackHoleSprite, (blackHoleSize, blackHoleSize))
blackHoleSprite = loadImage('Sprites', 'fase_01', 'buraco_negro_1_001.png')
blackHoleSprite_rotated = loadImage('Sprites', 'fase_01', 'buraco_negro_1_001.png')
blackHoleSpriteBoxCollider_1 = loadImage('Sprites', 'fase_01', 'Circulo_de_Dano_Buraco_Negro_2.png')

blackHoleSprite = pg.transform.scale(blackHoleSprite, (blackHoleSize, blackHoleSize))
blackHoleSprite_rotated = pg.transform.scale(blackHoleSprite_rotated, (blackHoleSize, blackHoleSize))
blackHoleSpriteBoxCollider_1 = pg.transform.scale(blackHoleSpriteBoxCollider_1, (blackHoleCircleCollider*2, blackHoleCircleCollider*2))

def newBlackHole(posX, posY):
	new = pg.Rect(posX - blackHoleSize, posY - blackHoleSize, blackHoleSize, blackHoleSize)	
	blackHoleList.append(new)

######################## Sudden Attack ########################

fpsCounterSuddenAtk = 0
fpsCounterCooldownSuddenAtk = 0
cooldownSuddenAtk = 2
suddenAtkDelay = 0.5
suddenAtkQtde = 2
canSuddenAttack = True

suddenAtkSprite = loadImage('Sprites', 'fase_01', 'meteoro_1.png')

suddenAtkList = []
def newSuddenAtk(top, left, width, height):
	global suddenAtkSprite
	new = pg.Rect(top, left, width, height) #Rect(left, top, width, height)
	if randint(1, 2) == 2:
		suddenAtkSprite = loadImage('Sprites', 'fase_01', 'meteoro_1.png')
		suddenAtkSprite = pg.transform.scale(suddenAtkSprite, (width, height))
	else:
		suddenAtkSprite = loadImage('Sprites', 'fase_01', 'meteoro_2.png')
		suddenAtkSprite = pg.transform.scale(suddenAtkSprite, (width, height))
	#new = [startPos, endPos, width]
	suddenAtkList.append(new)

######################## Particulas ########################

particleSpd = 1
particleDecay = 3
angleX = 0.05
angleY = 0.05

######## Dash ########
particleDashDecayCounter = 0
particlesInDash = 5
particleDashList = []

######## Run ########
particleRunDecayCounter = 0

def generateParticles(style, posX, posY, size):
	if style == "dash":
		for x in range(particlesInDash):
			offset = 0
			newParticle = pg.Rect(randint(posX, posX + size - offset), randint(posY + offset, posY + size - offset), 5, 5)
			particleDashList.append(newParticle)
	elif style == "run":
		for x in range(particlesInRun):
			offset = 0
			newParticle = pg.Rect(randint(posX, posX + size - offset), randint(posY + offset, posY + size - offset), 5, 5)

######################## Rotação de imagem ########################

def imageRotate(canvas, source, pos, angle):
	source_rotated = pg.transform.rotate(source, blackHoleSpriteAngle)
	newRect = source_rotated.get_rect(center = source.get_rect(topleft = pos).center)

	canvas.blit(source_rotated, newRect.topleft)

######################## Plano de fundo ########################


######################## Atualizações ########################

def draw(gameState, canvas):
	# global blackHoleSprite_rotated
	if gameState == "Game_01" :

		for obj in suddenAtkList:
			if obj.x > 0 - obj.w and obj.y < screenX + obj.w and obj.y > 0 - obj.h and obj.y < screenY + obj.h:	
				#pg.draw.rect(canvas, (255, 255, 255), obj)
				canvas.blit(suddenAtkSprite, obj)
			#pg.draw.line(canvas, (255, 255, 255), obj[0], obj[1], obj[2])


		for obj in photonList:
			if obj.x > 0 - offset and obj.y < screenX + offset and obj.y > 0 - offset and obj.y < screenY + offset:	
				#Ver caixa de colisão:
				#pg.draw.rect(canvas, (255, 255, 255), obj)	

				#Desenhar Sprite:		
				canvas.blit(photonSprite, obj)

		for obj in neutronList:
			if obj.x > 0 and obj.y < screenX and obj.y > 0 and obj.y < screenY:
				#Ver caixa de colisão:
				#pg.draw.rect(canvas, (255, 255, 255), obj)

				#Desenhar Sprite:
				canvas.blit(neutronSprite, obj)

		for obj in particleDashList:
			if obj.x  > 0 and obj.y  < screenX and obj.y > 0 and obj.y < screenY:
				pg.draw.rect(canvas, (randint(0,255),randint(0,255),randint(0,255)), obj)

		for obj in blackHoleList:
			if obj.x + obj.w + 128 >= 0 and obj.y - obj.h - 128 <= screenX and obj.y + obj.h + 128 >= 0 and obj.y - obj.h - 128 <= screenY:
				#Ver caixa de colisão:
				#pg.draw.rect(canvas, (255, 255, 255), obj)				
				canvas.blit(blackHoleSpriteBoxCollider_1, (obj.x - obj.w//2, obj.y - obj.h//2))

				#Desenha o Sprite rodando
				imageRotate(canvas, blackHoleSprite, (obj.x, obj.y), blackHoleSpriteAngle)

		




def tick(gameState, dt):
	if gameState == "Game_01":
		global angleX
		global particleDashDecayCounter, particleDashList
		global photonList, blackHoleList
		global fpsCounterRotateBH, blackHoleSpriteAngle, blackHoleSprite, blackHoleSprite_rotated, rotateBlackHoles
		global fpsCounterSuddenAtk, canSuddenAttack, fpsCounterCooldownSuddenAtk
		if not particleDashList == []:					
			for obj in particleDashList:
				obj.x += int(math.cos(angleX)*5)
				angleX += randint(1, 5)/60		
			if particleDashDecayCounter >= particleDecay * dt * configFPS:
				del particleDashList[0:particlesInDash]
				particleDashDecayCounter = 0				
				angleX = randint(1, 10)/10
			else:
				particleDashDecayCounter += 1 * dt
		else:
			angleX = 0.05
			angleY = 0.05
		
		### Colisão do Buraco Negro ###
		for obj in blackHoleList:
			if obj.x + obj.w > 0 and obj.y + obj.h < screenX and obj.y > 0 and obj.y < screenY:
				indexList = obj.collidelistall(photonList)
				if len(indexList) >= BlackHoleHp:
					try:
						blackHoleList.remove(obj)
					except IndexError:
						pass

		fpsCounterRotateBH += 1 * dt
		if fpsCounterRotateBH >= blackHoleRotateTimer * configFPS * dt:
			#blackHoleSprite_rotated = pg.transform.rotate(blackHoleSprite, blackHoleSpriteAngle)
			rotateBlackHoles = True
			#blackHoleSprite = rot_center(blackHoleSprite, blackHoleSpriteAngle)
			blackHoleSpriteAngle += 5
			if blackHoleSpriteAngle >= 360:
				blackHoleSpriteAngle -= 360
			fpsCounterRotateBH = 0
		else:
			rotateBlackHoles = False


		fpsCounterSuddenAtk += 1 * dt
		if fpsCounterSuddenAtk >= configFPS * dt * suddenAtkDelay and canSuddenAttack:
			chance = randint(1, 10)
			if chance <= 7:

				posX = randint(0, screenX)
				posY = randint(0, screenY)
				w = h = randint(5, 30)
				newSuddenAtk(posX, posY, w, h) #Rect((left, top), width, height)
				canSuddenAttack = False
				fpsCounterSuddenAtk = 0
			else:
				canSuddenAttack = False

		if not canSuddenAttack:
			fpsCounterCooldownSuddenAtk += 1 * dt 
			if fpsCounterCooldownSuddenAtk >= configFPS * dt * cooldownSuddenAtk:
				canSuddenAttack = True
				fpsCounterSuddenAtk = 0
				fpsCounterCooldownSuddenAtk = 0
				if not suddenAtkList == []:
					suddenAtkList.pop(0)



		return "Game_01"

	if gameState == "Death_Screen":
		return "Death_Screen"








		