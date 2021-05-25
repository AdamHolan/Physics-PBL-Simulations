#Matthew Oliveira
#May. 23, 2021
#Physics Smimulation Demonstrating the Photoelectric Effect

import pygame
import pygame.gfxdraw
import random as r
import math as m

#Defining some RGB Colours
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
INDIGO = (100, 70, 255)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

### Initializing Pygame ###

pygame.init()
pygame.font.init()
width = 1000
height = 700
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Photoelectric Effect")
exitCondition = False
exitCondition2 = False
clock = pygame.time.Clock()

myfont = pygame.font.SysFont("Ariel Black", 20)
biggerfont = pygame.font.SysFont("Ariel Black", 35)
bigfont = pygame.font.SysFont("Ariel Black", 50)
mehfont = pygame.font.SysFont("Ariel Black", 29)

### Defining Global Variables ###

h = 6.63 * 10 ** -34 #Planck's Constant
eV = 1.60 * 10 ** -19 #Electrovolts to joules
WF = 2 # Work Function for Aluminum
eM = 9.11 * 10 ** -31

#We will need to keep track of the following varibles, and will need two dictionaries

v = 5
f = 100

w = 3
f2 = 3

#Will keep track of the frequency in relation to the voltage
clickTrackerVF = {
    "Voltage" : v,
    "Frequency" : f,
}

#Will keep track of the frequency in relation to the wavelength
clickTrackerWF = {
    "Wavelength" : w,
    "Frequency" : f2,
}

#Draws an arrow in the direction given
def drawArrow(x, y, direction, colour):
    pygame.draw.polygon(screen, colour, [(x, y), (x, y + 24), (x + direction * 12, y + 12)])

#Drawing multiple arrows in pairs
def drawArrowsVF(x):
    for i in range(2):
        drawArrow(x + 3, (i+1) * 20, 1, GREEN)
        drawArrow(x - 3, (i+1) * 20, -1, RED)
        textsurface = myfont.render(str(list(clickTrackerVF.keys())[i]), False, (WHITE))
        screen.blit(textsurface, (x + 24, (i+1) * 20))

def drawArrowsWF(x):
    for i in range(2):
        drawArrow(x + 3, (i+1) * 20, 1, GREEN)
        drawArrow(x - 3, (i+1) * 20, -1, RED)
        textsurface = myfont.render(str(list(clickTrackerWF.keys())[i]), False, (WHITE))
        screen.blit(textsurface, (x + 24, (i+1) * 20))

#Setting up the page for scenario 1
def pageSetupVF(f):

    colour = BLACK

    if 0 <= f <= 30:
        colour = RED
    elif 31 <= f <= 60:
        colour = ORANGE
    elif 61 <= f <= 90:
        colour = YELLOW
    elif 91 <= f <= 120:
        colour = GREEN
    elif 121 <= f <= 150:
        colour = INDIGO
    else:
        colour = PURPLE


    if f > 0:
        try:
            pygame.gfxdraw.hline(screen, 200, 300, 600, WHITE)
            pygame.gfxdraw.hline(screen, 400, 600, 600, WHITE)
            pygame.gfxdraw.vline(screen, 200, 600, 200, WHITE)
            pygame.gfxdraw.vline(screen, 600, 600, 200, WHITE)
            pygame.gfxdraw.hline(screen, 200, 300, 200, WHITE)
            pygame.gfxdraw.hline(screen, 500, 600, 200, WHITE)

            pygame.gfxdraw.box(screen, [300, 150, 10, 100], WHITE)
            pygame.gfxdraw.box(screen, [490, 150, 10, 100], WHITE)

            pygame.gfxdraw.box(screen, [300, 580, 100, 40], WHITE)

            pygame.gfxdraw.filled_circle(screen, 600, 400, 50, WHITE)

            text = biggerfont.render("+  V  -", False, BLACK)
            screen.blit(text, (320, 590))
            text = myfont.render("Current: ", False, BLACK)
            screen.blit(text, (585, 370))

            pygame.gfxdraw.filled_polygon(screen, [(600, 0), (310, 165), (310, 235)], colour)

            pygame.gfxdraw.vline(screen, 700, 700, 0, WHITE)
        except OverflowError:
            pass

    if f <= 0:
        try:
            pygame.gfxdraw.hline(screen, 200, 300, 600, WHITE)
            pygame.gfxdraw.hline(screen, 400, 600, 600, WHITE)
            pygame.gfxdraw.vline(screen, 200, 600, 200, WHITE)
            pygame.gfxdraw.vline(screen, 600, 600, 200, WHITE)
            pygame.gfxdraw.hline(screen, 200, 300, 200, WHITE)
            pygame.gfxdraw.hline(screen, 500, 600, 200, WHITE)

            pygame.gfxdraw.box(screen, [300, 150, 10, 100], WHITE)
            pygame.gfxdraw.box(screen, [490, 150, 10, 100], WHITE)

            pygame.gfxdraw.box(screen, [300, 580, 100, 40], WHITE)

            pygame.gfxdraw.filled_circle(screen, 600, 400, 50, WHITE)

            text = biggerfont.render("+  V  -", False, BLACK)
            screen.blit(text, (320, 590))
            text = myfont.render("Current: ", False, BLACK)
            screen.blit(text, (585, 370))

            pygame.gfxdraw.filled_polygon(screen, [(600, 0), (310, 165), (310, 235)], BLACK)

            pygame.gfxdraw.vline(screen, 700, 700, 0, WHITE)
        except OverflowError:
            pass

#Setting up the page for scenario 2
def pageSetupWF(w, f):

    colour = BLACK

    if w <= 1:
        colour = PURPLE
    elif w == 2:
        colour = INDIGO
    elif w == 3:
        colour = GREEN
    elif w == 4:
        colour = YELLOW
    elif w == 5:
        colour = ORANGE
    elif w == 0 or f == 0:
        colour = BLACK
    else:
        colour = RED


    if w > 0 and f > 0:
        try:
            pygame.gfxdraw.box(screen, [200, 600, 200, 100], (195, 202, 206))
            pygame.gfxdraw.filled_polygon(screen, [(0, 0), (250, 700), (350, 700)], colour)
            pygame.gfxdraw.vline(screen, 700, 1000, 0, WHITE)
        except OverflowError:
            pass

    if w <= 0 or f <= 0:
        try:
            pygame.gfxdraw.box(screen, [200, 600, 200, 100], (195, 202, 206))
            pygame.gfxdraw.filled_polygon(screen, [(0, 0), (250, 700), (350, 700)], BLACK)
            pygame.gfxdraw.vline(screen, 700, 1000, 0, WHITE)
            pygame.gfxdraw.box(screen, [200, 600, 200, 100], (195, 202, 206))
        except OverflowError:
            pass

#Class for electrons in scenario 1
class ElectronVF():
    def __init__(self, freqClicks = 1, Voltage = 1):
        self.x = 310
        self.y = r.uniform(150, 250)
        self.speed = int(r.uniform(0, freqClicks))
        self.sV = Voltage
        self.angle = r.uniform(m.pi, m.pi / 2)

    #Will display electrons in scenario 1
    def display(self):
        if self.x < 490:
            try:
                pygame.gfxdraw.filled_circle(screen, int(self.x.real), int(self.y.real), 6, BLUE)
            except OverflowError:
                pass

    def move(self):
        self.speed = self.speed - self.sV
        if self.speed < 0:
            self.x = self.x + self.speed
            self.y = self.y + m.sin(self.angle) * self.speed
        else:
            self.x = self.x + self.speed

    def currentCheck(self):
        if self.x >= 488:
            return True
        elif self.x < 488:
            return False


#This class will be responsible for generating and moving electrons in the scenario 2
class ElectronWF():
    def __init__(self, pX, pY, freqClicks = 1):
        self.x = pX
        self.y = pY
        self.speed = freqClicks
        self.angle = r.uniform(m.pi / 2, m.pi)

    #This function will draw the electrons
    def display(self):
        try:
            pygame.gfxdraw.filled_circle(screen, int(self.x.real), int(self.y.real), 6, BLUE)
        except OverflowError:
            pass

    #Moves the electron
    def move(self):
        self.x = self.x + m.sin(self.angle) * self.speed
        self.y = self.y + m.cos(self.angle) * self.speed


### Animation ###
# A second while loop for the animation loop that allows me to restart the animation of the electrons over and over
while not exitCondition2:

    sprites = []
    for i in range(5):
        p = ElectronVF(f, v)
        sprites.append(p)

    moresprites = []
    for i in range(5):
        p = ElectronWF(r.randint(200, 400), r.randint(600, 700), f2)
        moresprites.append(p)


    #Variable to decide what type of unit to show calculations if:
    current = 0

    if not exitCondition2:
        exitCondition = False

    #Animation Loop
    while not exitCondition:

        for i in range(int(f/20)):
            g = ElectronVF(f, v)
            sprites.append(g)

        screen.fill(BLACK)

        #Checks for mouse clicks and changes frequency and wavelength depending on
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitCondition = True
                exitCondition2 = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                p = pygame.mouse.get_pos()
                a = list(clickTrackerVF.keys())
                for i in range(2):
                    if ((i+1) * 20 - 1) < p[1] < ((i+1) * 20 + 25) and 752 < p[0] < 778:
                        clickTrackerVF[a[i]] += 1
                    if ((i+1) * 20 - 1) < p[1] < ((i+1) * 20 + 25) and 722 < p[0] < 748:
                        clickTrackerVF[a[i]] += -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    exitCondition = True


        #Keeping the frequency from becoming negative because electrons don't like that
        if clickTrackerVF.get("Frequency") <= 0:
            clickTrackerVF["Frequency"] = 0

        if clickTrackerVF.get("Voltage") <= 0:
            clickTrackerVF["Voltage"] = 0

        #Retrieving values from the dictionary
        v = clickTrackerVF.get("Voltage")

        f = clickTrackerVF.get("Frequency")

        #Needed to make 0 condition work with the electrons
        currentVoltage = v

        stoppingVoltage = f ** 2 /(2 * 178)


        if v == 0:
            f = 0
            clickTrackerVF["Frequency"] = 0

        #Creating the UI
        pageSetupVF(f)
        drawArrowsVF(750)

        #Displaying text

        text = biggerfont.render("Stopping Voltage:", False, WHITE)
        screen.blit(text, (720, 200))
        text = biggerfont.render(str(stoppingVoltage) + ' V', False, WHITE)
        screen.blit(text, (720, 230))
        text = biggerfont.render("Current Voltage: ", False, WHITE)
        screen.blit(text, (720, 400))
        text = biggerfont.render(str(currentVoltage) + ' V', False, WHITE)
        screen.blit(text, (720, 430))
        text = biggerfont.render("Frequency: ", False, WHITE)
        screen.blit(text, (720, 600))

        trueFrequency = f / h / (10 ** 21)
        text = mehfont.render(str(trueFrequency) + " Hz", False, WHITE)
        screen.blit(text, (720, 630))
        text = biggerfont.render("Press Space to Toggle to Einstein Model", False, WHITE)
        screen.blit(text, (100, 650))
        text = biggerfont.render(str(current) + " eV/s", False, BLACK)
        screen.blit(text, (555, 390))

        current = 0

        for i, sprite in enumerate(sprites):
            sprite.display()
            sprite.move()
            if sprite.currentCheck():
                current = current + 1

        pygame.display.flip()
        clock.tick(30)

    #Animation Loop
    if not exitCondition2:
        exitCondition = False


    while not exitCondition:

        for i in range(f2):
            g = ElectronWF(r.randint(200, 400), r.randint(600, 700), f2)
            moresprites.append(g)

        screen.fill(BLACK)

        #Checks for mouse clicks and changes frequency and wavelength depending on
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitCondition = True
                exitCondition2 = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                p = pygame.mouse.get_pos()
                a = list(clickTrackerWF.keys())
                for i in range(2):
                    if ((i+1) * 20 - 1) < p[1] < ((i+1) * 20 + 25) and 752 < p[0] < 778:
                        clickTrackerWF[a[i]] += 1
                        if i == 0:
                            clickTrackerWF[a[i + 1]] += -1
                        if i == 1:
                            clickTrackerWF[a[i - 1]] += -1
                    if ((i+1) * 20 - 1) < p[1] < ((i+1) * 20 + 25) and 722 < p[0] < 748:
                        clickTrackerWF[a[i]] += -1
                        if i == 0:
                            clickTrackerWF[a[i + 1]] += 1
                        if i == 1:
                            clickTrackerWF[a[i - 1]] += 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    exitCondition = True

        #Keeping the frequency from becoming negative because electrons don't like that
        if clickTrackerWF.get("Frequency") <= 0:
            clickTrackerWF["Frequency"] = 0
            clickTrackerWF["Wavelength"] = 6

        if clickTrackerWF.get("Wavelength") <= 0:
            clickTrackerWF["Frequency"] = 6
            clickTrackerWF["Wavelength"] = 0

        #Retrieving values from the dictionary
        w = clickTrackerWF.get("Wavelength")

        f2 = clickTrackerWF.get("Frequency")

        #Needed to make 0 condition work with the electrons
        if w == 0:
            f2 = 0

        #Creating the UI
        pageSetupWF(w, f2)
        drawArrowsWF(750)

        #Displaying text

        text = bigfont.render("Space to toggle Simulations", False, WHITE)
        screen.blit(text, (20, 200))
        text = biggerfont.render("Wavelength: ", False, WHITE)
        screen.blit(text, (720, 400))
        text = biggerfont.render(str(w * 10 ** 2) + " nm", False, WHITE)
        screen.blit(text, (720, 430))
        text = biggerfont.render("Frequency:" , False, WHITE)
        screen.blit(text, (720, 500))
        text = biggerfont.render(str(clickTrackerWF.get("Frequency") * 10 ** 2) + " THz", False, WHITE)
        screen.blit(text, (720, 530))


        for i, sprite in enumerate(moresprites):
            sprite.display()
            sprite.move()

        pygame.display.flip()
        clock.tick(30)
