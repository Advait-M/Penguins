#Import modules
from tkinter import *
from time import *
from random import *
from math import *
import random
import math
import winsound

#Start tkinter
tk = Tk()
screen = Canvas(tk, width=1000,height=800, background="white")
screen.pack()

#Import sound and5 initialize snowfall variables
jingleBells = "Jingle Bells.wav"
numsnowflakes = 500
windSpeed = 5

snowflakes = []
xSnowSpeeds = []
ySnowSpeeds = []
snowxPos = []
snowxyPos = []
snowXStart = []
snowYStart = []
snowSizes = []
snowTime = []

#Fill snowfall arrays
for n in range(0,numsnowflakes):
    snowxPos.append(0)
    snowxyPos.append(0)
    xSnowSpeeds.append( windSpeed )
    ySnowSpeeds.append( randint(8,11))
    snowXStart.append( randint(-200*windSpeed,800))
    snowYStart.append( randint(-800,0))
    snowSizes.append( randint(2,4) )
    snowflakes.append(0)
    snowTime.append(0)




#ANIMATION PARAMETERS
numPenguins = 11

iceBergLength = 600         #THE LENGTH OF THE ICEBERG
iceBergThickness = 200      #THE THICKNESS OF THE ICEBERG
xMin = 200                   #THE X-VALUE OF THE LEFT END OF THE ICEBERG
xMax = xMin + iceBergLength #THE Y-VALUE OF THE LEFT END OF THE ICEBERG
yIceBerg = 250              #THE HEIGHT OF THE TOP OF THE ICEBERG

penguinWidth = 22     #THE WIDTH OF THE PENGUINS 
minSpeed = 7          #MINIMUM SPEED OF PENGUINS
maxSpeed = 10         #MAXIMUM SPEED OF PENGUINS
fallingSpeed = 0      #HOW FAST THE PENGUINS FALL
totalParticles = 100  #HOW MANY PARTICLES ARE IN EACH SPLASH
waterFrames = 30      #HOW LONG PARTICLES STAY ON THE SCREEN

gap = (iceBergLength - 25 - numPenguins*penguinWidth) / (numPenguins-1) #HOW MUCH SPACE IS BETWEEN EACH PENGUIN AT THE BEGINNING

#Initializing arrays
penguinGraphics = []
xPos = []
yPos = []
xSpeeds = []
ySpeeds = []
counters = []
counters2 = []
x1p = []
y1p = []
x2p = []
y2p = []
leftPenguin = PhotoImage(file = "penguinleft.png")
rightPenguin = PhotoImage(file = "penguinright.png")
falling = []
vix = []
viy = []
ft = []
finalX = []
m = []
t = []
initx = []
inity = []

anglec = []
b = []
xP = []
yP = []
particles = []
angles = []
xSizes = []
ySizes = []
r = []
rSpeeds = []
counterParticles = []
fCur = []
stayInWaterFrames = []

pengsr = []
pengsl = []

#Fills image arrays
for i in range(0, 91):
    pengsr.append(0)
    pengsl.append(0)
for i in range(0, 91):
    pengsr[i] = PhotoImage(file = "penguinRight " + str(i) + ".gif")
    pengsl[i] = PhotoImage(file = "penguinLeft copy " + str(i) + ".gif")

#Calculates angle between 2 lines (acute angle)
def angle(m1, m2):
    if isPerpendicular(m1, m2) == True:
        return 90
    elif m1 == "undefined" or m2 == "undefined":
        if m1 == "undefined" and m2 == "undefined":
            return 0
        elif m1 == "undefined":
            tanAngle = abs(m2)
            angleRadians = math.atan(tanAngle)
            angleDegrees = angleRadians * (180/pi)
            return angleDegrees
        else:
            tanAngle = abs(m1)
            angleRadians = math.atan(tanAngle)
            angleDegrees = angleRadians * (180/pi)
            return angleDegrees
    else:
        tanAngle = abs((m1 - m2) / (1 + m1 * m2))
        angleRadians = math.atan(tanAngle)
        angleDegrees = angleRadians * (180/pi)
        return angleDegrees

#Helper function that returns whether two lines are perpendicular or not (True or False)
def isPerpendicular(m1, m2):
    if m1 == "undefined" or m2 == "undefined":
        if m1 == 0 or m2 == 0:
            return True
        else:
            return False
    else:
        if m1 * m2 == -1:
            return True
        else:
            return False
        
#DRAWS THE ICEBERG
def drawIceBerg():
    xm = xMin
    xM = xMax
    y = yIceBerg
    screen.create_polygon(xm, y, xm+50, y+100, xm+25, y+150, xm+75, y+300, xm+100, 800, xM, 800, xM-60, y+250, xM-25, y+175, xM-80, y+100, xM, y, fill = "white")

#DRAWS THE BACKGROUND
def drawBackgroundScenery():
    screen.create_rectangle( 0,0,1000, 800, fill="sky blue")
         
#CALCULATES THE DISTANCE BETWEEN THE X-VALUES x1 AND x2.
#THIS IS USED TO HELP DETERMINE IF TWO PENGUINS HAVE JUST COLLIDED.
def distanceBetweenXvalues( x1, x2 ):
    distance = x2-x1
    return distance

#RETURNS TRUE IF PENGUINS i1 AND i2 HAVE JUST COLLIDED, AND FALSE OTHERWISE
def collision( i1, i2 ):
    if -penguinWidth/2 < distanceBetweenXvalues(i1, i2) <= penguinWidth/2:
        return True
    return False

#RETURNS TRUE IF PENGUIN i IS ABOUT TO FALL OFF THE ICE BERG, AND FALSE OTHERWISE
def readyToFallOff( i ):
    if x1p[i] > xMax or x1p[i] < xMin or x2p[i] > xMax or x2p[i] <xMin:
        return True
    return False

#Returns direction of penguin
def directionOfFall(i):
    if x1p[i] > xMax or x2p[i] > xMax:
        return "right"
    else:
        return "left"
    
#DRAWS PENGUIN i AT ITS CURRENT POSITION
def drawPenguin( i, anglec = 0):
    x1p[i] = xPos[i] - penguinWidth/2
    y1p[i] = yPos[i] - 25
    x2p[i] = xPos[i] + penguinWidth/2
    y2p[i] = yPos[i] + 25
    if xSpeeds[i] > 0:
        penguinGraphics[i] = screen.create_image(xPos[i], yPos[i], image = pengsr[round(anglec)])
    else:
        penguinGraphics[i] = screen.create_image(xPos[i], yPos[i], image = pengsl[round(anglec)])


#Fills arrays
def setStartingPositionsAndSpeeds():
    x = xMin + 20
    for i in range(0,numPenguins):
        
        penguinGraphics.append( 0 )
        speed = randint(-maxSpeed, maxSpeed)
        while -minSpeed < speed < minSpeed:
            speed = randint(-maxSpeed, maxSpeed)
        
        s = speed #At the start, each penguin is moving either to the left or to the right 
        xSpeeds.append( s )
        vix.append(0)
        viy.append(0)
        ft.append(0)
        ySpeeds.append( 0 ) #Penguins have no vertical motion at the start

        xPos.append( x )
        x = x + penguinWidth + gap #Ensures that the penguins aren't overlapping at the start
        yPos.append( yIceBerg - 50 )
        counters.append(False)
        counters2.append(False)
        x1p.append(0)
        y1p.append(0)
        x2p.append(0)
        y2p.append(0)
        finalX.append(0)
        m.append(1)
        falling.append(False)
        t.append(0)
        initx.append(0)
        inity.append(0)
        anglec.append(0)
        b.append(0)
        
        rTemp = []
        xSizesTemp = []
        ySizesTemp = []
        rSpeedsTemp = []
        particlesTemp = []
        anglesTemp = []
        xPTemp = []
        yPTemp = []
        counterParticles.append(True)
        fCur.append(0)
        stayInWaterFrames.append(waterFrames)
        
        for particleNum in range(0, totalParticles):
            particlesTemp.append(0)
            xPTemp.append(0)
            yPTemp.append(0)
            dAngle = random.randint(1, 360)
            rAngle = math.radians(dAngle)
            anglesTemp.append(rAngle)
            rTemp.append(random.randint(-15, 15))
            xSizesTemp.append(random.randint(3, 7))
            ySizesTemp.append(random.randint(3, 7))
            rSpeedsTemp.append(random.randint(-15, 15))
            while rSpeedsTemp[particleNum] == 0:
                rSpeedsTemp[particleNum] = random.randint(-15, 15)
                
        r.append(rTemp)
        xSizes.append(xSizesTemp)
        ySizes.append(ySizesTemp)
        rSpeeds.append(rSpeedsTemp)
        particles.append(particlesTemp)
        angles.append(anglesTemp)
        xP.append(xPTemp)
        yP.append(yPTemp)


#DRAWS CLOUD WITH GIVEN ARGUMENTS
def drawCloud(xCentre, yCentre, maxWidth, maxHeight, numOvals, col):
      
      for i in range(1, numOvals + 1):
            xUL = xCentre - random.randint(1, maxWidth)
            yUL = yCentre - random.randint(1, maxHeight)
            xLR = xCentre + random.randint(1, maxWidth)
            yLR = yCentre + random.randint(1, maxHeight)
            oval = screen.create_oval(xUL, yUL, xLR, yLR, fill=col, outline=col)
            
#DRAWS SNOW FALLING DOWN
def snow():
    for n in range(0, numsnowflakes):

            snowxPos[n] = xSnowSpeeds[n] * snowTime[n] + snowXStart[n]
            snowxyPos[n] = ySnowSpeeds[n] * snowTime[n] + snowYStart[n]

            snowflakes[n] = screen.create_oval(snowxPos[n],snowxyPos[n],snowxPos[n]+snowSizes[n],snowxyPos[n]+snowSizes[n], fill="white", outline="white")

            snowTime[n] = snowTime[n] + 1

            if snowxyPos[n] >= 600:
                snowTime[n] = 0
                snowYStart[n] = 0
                
#DRAWS ALL THE CLOUDS
def drawAllClouds():
    for cloudNum in range(1,30):
      
        xCentre = randint(0,1000)
        yCentre = randint(5,150)
        maxWidth = randint(40,80)
        maxHeight = randint(10,30)
      
        drawCloud( xCentre, yCentre, maxWidth, maxHeight, 30, "grey" + str(randint(50, 100)))
        
#CHECKS WHETHER PROGRAM IS OVER OR NOT (WHETHER THE LAST PENGUIN HAS SPLASHED INTO THE WATER)
#RETURNS TRUE IF THE PROGRAM IIS NOT OVER AND FALSE OTHERWISE
def running():
    for w in range(0, numPenguins):
            if counterParticles[w]:
                return True
    return False

#Draws elements of the background that need to be drawn after the penguins
def otherBackground():
    screen.create_rectangle(0, 600, 1000, 800, fill = "blue")
    screen.create_polygon(xMin+350, 650, xMin+400, 750, xMin+450, 725, xMin+425, 680, fill = "white", smooth = True)
    screen.create_polygon(xMin+400, 625, xMin+230, 625, xMin+150, 725, xMin+275, 700, fill = "white", smooth = True)
    #screen.create_polygon(725, 700, 825, 625, 850, 650, 800, 700, fill = "black", smooth = True)#800, 700, 850, 750, 875, 725, 750, 700, fill = "black") 
    #screen.create_polygon(800, 660, 820, 640, 810, 660, fill = "white", smooth = True)

#RUNS THE ANIMATION
def runAnimation():
    #Play sound and set up the background
    #Also set up the arrays
    winsound.PlaySound(jingleBells, winsound.SND_FILENAME| winsound.SND_ASYNC)
    
    setStartingPositionsAndSpeeds()   
    drawBackgroundScenery()
    drawIceBerg()
    #Initialize frame counter
    f = 0

    #Draw clouds
    drawAllClouds()
    
    #Runs while at least one penguin is on the screen
    while running():
        #f counts the frames
        f += 1
        #Draw the penguins
        for i in range(0, numPenguins):
            drawPenguin(i, anglec[i])
                
        #Reset collided array
        collided = []
        
        for i in range(0, numPenguins): #FOR EACH PENGUIN, DRAW IT IN ITS CURRENT POSITION, CHECK FOR COLLISIONS, AND UPDATE ITS POSITION
            if not readyToFallOff(i):
                
                #Checks for collisions and records them in collided array
                for p in range(0, numPenguins):
                    #Don't check for collisions against itself
                    if p == i:
                        pass
                    else:
                        xis = [x1p[i], x2p[i]]
                        xps = [x1p[p], x2p[p]]
                        if collision(x1p[i], x2p[p]) or collision(x2p[i], x1p[p]):
                            collided.append([i, p])
                            
                #Switches the speeds of penguins which have collided
                for e in range(0, len(collided)):
                    temp = xSpeeds[collided[e][0]]
                    xSpeeds[collided[e][0]] = xSpeeds[collided[e][1]]
                    xSpeeds[collided[e][1]] = temp
                    
                #Updates x and y positions
                xPos[i] = xPos[i] + xSpeeds[i]
                yPos[i] = yPos[i] + ySpeeds[i]

            else:
                #Checks if penguin is ready to make a splash
                if yPos[i] > 645 + penguinWidth/2:
                    #Only runs first time the penguin is in the splash
                    #fCur is frame at which penguin splashed
                    if counterParticles[i]:
                        fCur[i] = f
                        counterParticles[i] = False
                        
                    #Draws the particles
                    for q in range(0, totalParticles):
                        #Uses trigonometry to find the x and y positions of particles
                        xP[i][q] = xPos[i] + r[i][q] * math.cos(angles[i][q])
                        yP[i][q] = yPos[i] - r[i][q] * math.sin(angles[i][q])
                        r[i][q] = r[i][q] + rSpeeds[i][q]
                        
                        #Draws ovals/rectangles to represent droplets of water
                        if q % 2 == 0 and f - fCur[i] < stayInWaterFrames[i]:
                            particles[i][q] = screen.create_oval(xP[i][q], yP[i][q], xP[i][q] + xSizes[i][q], yP[i][q] + ySizes[i][q], fill = "blue")
                        elif f - fCur[i] < stayInWaterFrames[i]:
                            particles[i][q] = screen.create_rectangle(xP[i][q], yP[i][q], xP[i][q] + xSizes[i][q], yP[i][q] + ySizes[i][q], fill = "blue")
                else:
                    #Saves initial x and y coordinates when the penguin jumps
                    if not counters2[i]:
                        initx[i] = xPos[i]
                        inity[i] = yPos[i]
                        counters2[i] = True
                    #Calculates anglec 
                    if xPos[i] != initx[i]:
                        curM = (yPos[i] - inity[i])/(xPos[i] - initx[i])
                        b[i] += 1
                        if anglec[i] > 89:
                            pass
                        else:
                            anglec[i] = b[i] % 360
                    #Uses the velocity formulas to calculate the parabolic trajectory of the penguins
                    vix[i] = xSpeeds[i]
                    viy[i] = abs(vix[i] * 5)
                    ft[i] = -2 * viy[i] / -9.8
                    finalX[i] = vix[i] * ft[i]
                    m[i] += 1
                    t[i] = abs(ft[i]/finalX[i] * m[i])

                    #Makes penguins go in the right direction
                    if directionOfFall(i) == "left":
                        xPos[i] = vix[i] * t[i] + xMin 
                    else:
                        xPos[i] = vix[i] * t[i] + xMax
                    yPos[i] = -1*(viy[i] * t[i] + 0.5*-9.8*t[i]**2) + yIceBerg - 50
                    
        #Creating more elements of the background
        snow()
        otherBackground()
        screen.update()
        sleep(0.05)

        #Delete penguins and their particles (water droplets)
        for i in range(0, numPenguins):
            screen.delete( penguinGraphics[i] )
            for q in range(0, totalParticles):
                screen.delete(particles[i][q])
        #Delete snow flakes
        for n in range(0, numsnowflakes):
            screen.delete(snowflakes[n])

#CALLS THE PROCEDURE runAnimation()
runAnimation()



