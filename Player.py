import pygame as pg
import os, time, math
import Entity as en
from pygame.locals import *
from Configs import *
from load import loadImage

######################## Declarações ########################
#[rgbBackground, rgbProta, rgbProton, rgbNeutron, rgbPhoton, rgbBlackHole]
rgbColors = getColors()
Screen = getScreen()
baseSize = getBaseSize()
configFPS = getFps()

screenX = Screen[0]
screenY = Screen[1]



######################## Player Status ########################

playerSpd = 3.5
playerSize = 45
playerSizeOffset = 0
playerSizeGain = 2
playerX = screenX/2
playerY = screenY/2
rgbPlayer = rgbColors[1]
offset = 1

#UP, DOWN, LEFT DOWN
actualDir = [0, 0, 0, 0]

runningSpd = 6
walkingSpd = 3

dashTime = 0.1
dashSpd = 30
cooldownDashTime = 3
cooldownAttackTime = 0.5

fpsCooldownDash = 0
fpsCooldownAttack = 0
sizeStack = 0

canDash = True
canParticleDash = True
run = False
moved = False



######################## Imagens ########################

#playerSecondLevel = pg.image.load(os.path.join('Sprites', 'prota_2.png'))
#playerThirdLevel = pg.image.load(os.path.join('Sprites', 'prota_3.png'))
#playerFirstLevel = pg.image.load(os.path.join('Sprites', 'prota_1.png'))
playerFirstLevel = loadImage('Sprites', 'fase_01', 'pontinho_1_001.png')
playerFirstLevel = pg.transform.scale(playerFirstLevel, (playerSize, playerSize))

playerRect = pg.Rect(playerX, playerY, playerSize, playerSize)
playerBoxCollider = pg.Rect(playerX - playerRect.w*2, playerY - playerRect.h*2, playerSize*5, playerSize*5)
##playerRect.inflate_ip(screenX/6, screenY/6)


######################## Camera Status ########################

cameraLimit = 50
levelLimit = False
linesToCreate = []
linesToCreateBH = []
linesToCreateSA = []


######################## Controle de Tempo ########################
FPS = 0
fpsCounter = 0
actualFPS = 0
prevTime = time.time()
now = time.time()
dt = now - prevTime
prevTime = now
LowerCounter = False
dashCounter = False
cooldownDashCounter = False
cooldownAttackCounter = False
fpsCounterBlackHole = False
death = False

# cameraRect = pg.draw.circle(Canvas, corProta, (playerX, playerY), playerSize)
# cameraCoordX = screenX/2
# cameraCoordY = screenY/2

def playerGrow(size):
    global playerSizeOffset, playerFirstLevel, sizeStack, death
    if type(size) == int:
        if playerSizeOffset + playerSize + size <= 0:
            print(playerSizeOffset - playerSize)
            death = True
        else:
            playerRect.inflate_ip(size, size)
            playerBoxCollider.inflate_ip(size*2, size*2)
            playerSizeOffset += size       
            playerFirstLevel = loadImage('Sprites', 'fase_01', 'pontinho_1_001.png')
            playerFirstLevel = pg.transform.scale(playerFirstLevel, (playerSize + playerSizeOffset, playerSize + playerSizeOffset))   
    else:
        sizeStack += size
        if sizeStack <= -1:
            sizeStack += 1            
            playerGrow(-1)


def playerColliderGrow(obj1, objlist):
    global playerSize, playerRect
    indexlist = obj1.collidelistall(objlist)
    if not indexlist == []:        
        for index in indexlist:
            linesToCreate.append(objlist[index])
    indexList_2 = playerRect.collidelistall(objlist)
    try:
        if not indexList_2 == []:
            for index_2 in indexList_2:
                objlist.pop(index_2)
                playerGrow(playerSizeGain)
    except IndexError:
        pass  

def playerColliderSuddenAttack(playerMask, objlist):
    global playerSize, playerRect
    indexlist = playerMask.collidelistall(objlist)
    if not indexlist == []:        
        for index in indexlist:
            linesToCreateSA.append(objlist[index])
    indexList_2 = playerRect.collidelistall(objlist)
    try:
        if not indexList_2 == []:
            for index_2 in indexList_2:
                objlist.pop(index_2)
                playerGrow(-10)
    except IndexError:
        pass


def playerColliderBlackHole(playerMask, objlist, dt):
    global playerSize, playerRect
    global fpsCounterBlackHole
    indexlist = playerMask.collidelistall(objlist)
    if not indexlist == []:
        for index in indexlist:
            catop = ((objlist[index].x + objlist[index].w//2) - (playerRect.x + playerRect.w//2))**2
            catadj = ((objlist[index].y + objlist[index].h//2) - (playerRect.y + playerRect.h//2))**2
            hip = (catadj + catop)**0.5
            if hip < en.blackHoleCircleCollider:
                linesToCreateBH.append(objlist[index])
                aux = en.BlackHoleDmgPS / configFPS
                playerGrow(-aux*2)
    # indexList_2 = playerRect.collidelistall(objlist)
    # try:
    #     if not indexList_2 == []:
    #         if not fpsCounterBlackHole:
    #             for index_2 in indexList_2:
    #                 playerGrow(en.blackHoleGain)
    #         else:
    #             pass
    # except IndexError:
    #     pass

def moveCamera(dir):
    aux = []
    aux.extend(en.neutronList)
    aux.extend(en.photonList)
    aux.extend(en.particleDashList)
    aux.extend(en.blackHoleList)
    aux.extend(en.suddenAtkList)
    if dir == "UP":
        for obj in aux:
            obj.y += int(playerSpd)
    elif dir == "DOWN":
        for obj in aux:
            obj.y -= int(playerSpd)
    elif dir == "LEFT":
        for obj in aux:
            obj.x += int(playerSpd)
    elif dir == "RIGHT":
        for obj in aux:
            obj.x -= int(playerSpd)

def draw(gameState, canvas):
    global linesToCreate, linesToCreateBH
    if not linesToCreate == []:
        for obj in linesToCreate:
            pg.draw.line(canvas, (255, 255, 255), (playerRect.x + playerRect.w//2 , playerRect.y + playerRect.h//2), (obj.x + obj.w//2, obj.y + obj.h//2))
            linesToCreate.remove(obj)

    if not linesToCreateBH == []:
        for obj in linesToCreateBH:
            pg.draw.line(canvas, (255, 20, 20), (playerRect.x + playerRect.w//2 , playerRect.y + playerRect.h//2), (obj.x + obj.w//2, obj.y + obj.h//2))
            linesToCreateBH.remove(obj)

            
    if not linesToCreateSA == []:
        for obj in linesToCreateSA:
            pg.draw.line(canvas, (255, 20, 20), (playerRect.x + playerRect.w//2 , playerRect.y + playerRect.h//2), (obj.x + obj.w//2, obj.y + obj.h//2))
            linesToCreateSA.remove(obj)

    #desenha a caixa de colisão que cria as linhas
    #pg.draw.rect(canvas, rgbPlayer, playerBoxCollider)

    #desenha a colisão do jogador
    #pg.draw.rect(canvas, (0, 0, 0), playerRect)

    #desenha o sprite do jogador
    canvas.blit(playerFirstLevel, playerRect)    

def tick(gameState, dt): 
    if gameState == "Game_01":
        global moved # Coisas para a Movimentação        
        global playerSpd # Coisas para a Corrida
        global fpsCounterDash, dashCounter, fpsCooldownDash, canDash, canParticleDash # Coisas para o Dash
        global cooldownAttackCounter, fpsCooldownAttack # Controla o tempo entre cada ataque
        global cameraLimit #Controlar a camera ué

        if death:
            return "Death_Screen"

        buttons = pg.key.get_pressed()
        if buttons[K_UP] or buttons[K_w]:
            if playerRect.y - playerRect.h < screenY//2 - cameraLimit:
                moveCamera("UP")
            else:
                playerRect.y -= playerSpd
            moved = True
        if buttons[K_DOWN] or buttons[K_s]:
            if playerRect.y + playerRect.h > screenY//2 + cameraLimit:
                moveCamera("DOWN")
            else:
                playerRect.y += playerSpd
            moved = True
        if buttons[K_LEFT] or buttons[K_a]:
            if playerRect.x - playerRect.w < screenX//2 - cameraLimit:
                moveCamera("LEFT")
            else:
                playerRect.x -= playerSpd
            moved = True
        if buttons[K_RIGHT] or buttons[K_d]:
            if playerRect.x + playerRect.w > screenX//2 + cameraLimit:
                moveCamera("RIGHT")
            else:
                playerRect.x += playerSpd
            moved = True

        # if not cameraLimit == 0 and playerSize*2 >= cameraLimit:
        #     cameraLimit = 0
        #     print("Mudei!")

        ### Colisões (Apenas quando se move) ###
        if moved:
            playerColliderGrow(playerBoxCollider, en.neutronList)
            playerColliderGrow(playerBoxCollider, en.photonList)
            playerColliderBlackHole(playerBoxCollider, en.blackHoleList, dt)
            playerColliderSuddenAttack(playerBoxCollider, en.suddenAtkList)
            playerBoxCollider.x = playerRect.x - playerRect.w*2 + playerSizeOffset*1.5
            playerBoxCollider.y = playerRect.y - playerRect.h*2 + playerSizeOffset*1.5

        ### Controle de Velocidade (Corrida) ###
        if buttons[K_LSHIFT]:
            playerSpd = runningSpd
        else:
            playerSpd = walkingSpd

        ### Controle do Dash ###
        if buttons[K_SPACE] and canDash:
            dashCounter = True
            fpsCounterDash = 0

        if dashCounter:
            canDash = False
            fpsCounterDash += 1 * dt
            if canParticleDash:
                en.generateParticles("dash", playerRect.x, playerRect.y, playerSize + playerSizeOffset)
                playerGrow(-en.particlesInDash)
                canParticleDash = False
            if fpsCounterDash <= configFPS * dt * dashTime:
                playerSpd = dashSpd
            else:
                playerSpd = walkingSpd
                fpsCounterDash = 0
                dashCounter = False
                fpsCooldownDash = 0
                canParticleDash = True
                
        ### Cooldown do dash ###
        else:
            fpsCooldownDash += 1 * dt
            if fpsCooldownDash >= configFPS * dt * cooldownDashTime:
                canDash = True

        if pg.mouse.get_pressed() == (1, 0, 0) or cooldownAttackCounter:
            if not cooldownAttackCounter:
                mouse = pg.mouse.get_pos()
                en.newPhoton(mouse[0], mouse[1])
                fpsCooldownAttack = 0
                playerGrow(-2)
                cooldownAttackCounter = True
            else:
                fpsCooldownAttack += 1 * dt
                if fpsCooldownAttack >= configFPS * dt * cooldownAttackTime:
                    cooldownAttackCounter = False 

        return "Game_01"   

    
    #elif 
    
