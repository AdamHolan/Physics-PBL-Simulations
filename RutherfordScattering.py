import pygame
import math as m
pygame.init()

width, height = 800, 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Important variables
Z = 79
N = 118
A = Z + N
radius = 1
EK = 5

# Other things
show = True
i, j = 0, 2
frame = 0
elements = ["Hydrogen", "Helium", "Lithium", "Beryllium", "Boron", "Carbon", "Nitrogen", "Oxygen", "Fluorine", "Neon", "Sodium", "Magnesium", "Aluminium", "Silicon", "Phosphorus", "Sulfur", "Chlorine", "Argon", "Potassium", "Calcium", "Scandium", "Titanium", "Vanadium", "Chromium", "Manganese", "Iron", "Cobalt", "Nickel", "Copper", "Zinc", "Gallium", "Germanium", "Arsenic", "Selenium", "Bromine", "Krypton", "Rubidium", "Strontium", "Yttrium", "Zirconium", "Niobium", "Molybdenum", "Technetium", "Ruthenium", "Rhodium", "Palladium", "Silver", "Cadmium", "Indium", "Tin", "Antimony", "Tellurium", "Iodine", "Xenon", "Caesium", "Barium", "Lanthanum", "Cerium", "Praseodymium", "Neodymium", "Promethium", "Samarium", "Europium", "Gadolinium", "Terbium", "Dysprosium", "Holmium", "Erbium", "Thulium", "Ytterbium", "Lutetium", "Hafnium", "Tantalum", "Tungsten", "Rhenium", "Osmium", "Iridium", "Platinum", "Gold", "Mercury", "Thallium", "Lead", "Bismuth", "Polonium", "Astatine", "Radon", "Francium", "Radium", "Actinium", "Thorium", "Protactinium", "Uranium", "Neptunium", "Plutonium", "Americium", "Curium", "Berkelium", "Californium", "Einsteinium", "Fermium", "Mendelevium", "Nobelium", "Lawrencium", "Rutherfordium", "Dubnium", "Seaborgium", "Bohrium", "Hassium", "Meitnerium", "Darmstadtium", "Roentgenium", "Copernicium", "Nihonium", "Flerovium", "Moscovium", "Livermorium", "Tennessine", "Oganesson", "None"]
myfont = pygame.font.SysFont('Lucida Console', 20)
showKE = True
fontL = pygame.font.SysFont('Lucida Console', 20)
fontS = pygame.font.SysFont('Lucida Console', 12)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Rutherford Scattering')
done = False
clock = pygame.time.Clock()


#SCALING                                        # 1 pixel = 1e-15 metres
                                                # 1 frame = 1e-21 seconds
#def px(value):                  
#    return value*(10**15)                       # 1 m = 1e15 px
#def pxVel(value):                               
#    return value/(10**7)                        # 1 m/s = 1e-7 px/frame
#def pxAcc(value):
#    return value/(10**27)                       # 1 m/s2 = 1e-28 px/frame2
def joules(value):
    return value*(1.60218/10**13)

pxPerM = 10**15
fPerS = 10**21.3

def px(value):
    return(value*(pxPerM))
def pxVel(value):
    return(value*(pxPerM/fPerS))
def pxAcc(value):
    return(value*(pxPerM/fPerS/fPerS))
def sfRound(value):
    return'%s' % float('%0.3g' % value)


# Buttons
arrows = []

variables = {
    "Protons" : Z, 
    "Neutrons" : N,
    "Particle KE" : EK, 
}

def drawTriangle(x, y, dir, colour):
    pygame.draw.polygon(screen, colour, [(x, y), (x + 18, y), (x + 9, y + dir * 15)])


def drawTriangles(x):
    num = len(variables)
    global arrows
    arrows=[]
    if particle.particles==0:
        for i in range(num):
            drawTriangle(x, (i + 1) * (height - 100) / (num + 1) + 100, -1, green)        
            drawTriangle(x, (i + 1) * (height - 100) / (num + 1) + 120, 1, red)
            arrows.append((i + 1) * (height - 100) / (num + 1) + 110)
            textsurface = fontL.render(str(list(variables.keys())[i]), False, (white))
            screen.blit(textsurface, (x + 33, (i + 1) * (height - 100) / (num + 1) + 103))
    else:
        for i in range(num):
            drawTriangle(x, (i + 1) * (height - 100) / (num + 1) + 100, -1, (0,100,0))        
            drawTriangle(x, (i + 1) * (height - 100) / (num + 1) + 120, 1, (100,0,0))
            arrows.append((i + 1) * (height - 100) / (num + 1) + 110)
            textsurface = fontL.render(str(list(variables.keys())[i]), False, (white))
            screen.blit(textsurface, (x + 33, (i + 1) * (height - 100) / (num + 1) + 103))



def displayData(data):
    global text
    textsurface = fontL.render(data, False, (white))
    screen.blit(textsurface, (text))    
    text = (text[0], text[1]+20)


def displayInstructions(instructions):
    global text
    x = text[0]
    text = (text[0]-len(instructions)*12, text[1])
    textsurface = fontL.render(instructions, False, (white))
    screen.blit(textsurface, (text))
    text = (x, text[1] - 30)

# Alpha particles
speed = 1

class particle:
    def __init__(self):
        self.particles = 0
        self.deleteParticles = False
        self.velocity = m.sqrt(2*joules(EK)/(6.64216/10**27)) #m/s

        
    def shoot(self):
        if self.particles != 0:
            self.deleteParticles = True
        self.particles += 1
        self.particleY = height
        self.velocity = pxVel(m.sqrt(2*joules(EK)/(6.64216/10**27))) #m/s
        self.acceleration = pxAcc(-(self.velocity/pxVel(1)) ** 2 / (2 * ((height/px(1)) / 2 - d)))
    
    def calcForce(self):
        #for i, a in enumerate (self.x):
            #x, y = width / 2, height / 2 - self.particleY    # px
            #h = m.hypot(x,y) / px(1)  # m # converted from px
            f = height / 2 - self.particleY

            self.force = 4.6141551/10**28 * Z / (f ** 2)  # kg-m/s2 # 8.9875517923 * 10**9 * 2 * (1.602176634/10**19)**2 * Z / (h ** 2) # k 2e Ze / r^2 # uwu should be double?
            
    def drawForce(self):
        #for i, a in enumerate(self.x):
            end = (width/2,self.particleY+pxAcc(self.force)*10**58.9)
            pygame.draw.line(screen,red,(width/2,self.particleY),end)
            pygame.draw.circle(screen,red,end,1)


    def display(self):
        if self.deleteParticles:
            self.particles = 0
            self.velocity = pxVel(m.sqrt(2*joules(EK)/(6.64216/10**27)))
            self.deleteParticles = False
        elif 0 < self.particleY < 605:
            for i in range(speed):
                if Z != 0: self.velocity += self.acceleration
                self.particleY -= self.velocity
            pygame.draw.circle(screen, red, (width / 2, self.particleY), 5)
            #if showKE:
            #    textsurface = fontS.render(str(sfRound((6.64216/10**27)*(self.velocity/pxVel(1))**2/2/joules(1))) + " m/s", False, (white))  #(str(abs(round(m.hypot(self.vX[i],self.vY[i]),2))) + " m/s", False, (white))
            #    screen.blit(textsurface, (width/2-25, self.particleY-20))
        else:
            self.deleteParticles = True
            
    def check(self):
        if self.particles != 0: return True
        else: 
            self.velocity = pxVel(m.sqrt(2*joules(EK)/(6.64216/10**27)))
            return False

particle = particle()




while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if particle.particles==0:
                pos = pygame.mouse.get_pos()
                a = list(variables.keys())
                for i, x in enumerate(arrows):
                    if (x-25) < pos[1] < x:
                        variables[a[i]] += 1
                    if x < pos[1] < (x + 25):
                        variables[a[i]] -= 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                particle.shoot()
            if event.key == pygame.K_z:
                show = not show
            if event.key == pygame.K_BACKSPACE:
                print(radius, (height / 2 - radius))

    # Variable fixing
    if variables.get("Protons") > 118: variables["Protons"] = 118
    if variables.get("Protons") <= 0: variables["Protons"] = 0
    if variables.get("Neutrons") > variables.get("Protons") * 1.5: variables["Neutrons"] -= 1   # uwu something more accurate?
    if variables.get("Neutrons") < variables.get("Protons"): variables["Neutrons"] += 1
    if variables.get("Particle KE") <= 0: variables["Particle KE"] = 1

    Z = variables.get("Protons")
    N = variables.get ("Neutrons")
    A = Z + N
    EK = variables.get("Particle KE")

    radius =  1.2 / 10**15 * (A ** (1/3))   # m # R0 * A^1/3
    d = 4.6141551 / 10**28 * Z / joules(EK) # m # = k 2e Ze / (EK in joules)

    screen.fill(black)

    # Nucleus and alpha particles
    pygame.draw.circle(screen, white, (width / 2, height / 2), px(radius))
    if show:    
        pygame.draw.circle(screen, (175 + i, 175 + i, 175 + i), (width / 2, height / 2), px(d), width = 1)
        if abs(i) > 75:
            j = -j
        i += j

    if particle.check():
        particle.calcForce()
        particle.drawForce()
        particle.display()

    # UI
    drawTriangles(20)
    
    # Display text
    if frame%5 == 0 or round(particle.velocity,2) == 0:
        currentKE = sfRound(round((6.64216/10**27)*(particle.velocity/pxVel(1))**2/2/joules(1),2)) + " MeV"
        frame = 1
    
    text = (20, 20)
    displayData('Protons: ' + str(Z) + '')
    displayData('Neutrons: ' + str(N) + '')
    displayData('Atom: ' + elements[Z-1] + "-" + str(A))
    displayData('Nuclear Radius: ' + str(sfRound(radius)) + ' m')
    displayData('Closest Approach: ' + str(sfRound(d)) + ' m')
    #displayData('Initial KE: ' + str(EK) + '.0 MeV')
    displayData('Particle KE: ' +str(currentKE))
    

    text = (770, 550)
    displayInstructions('Spacebar: Alpha particle')
    displayInstructions('Z: Toggle boundary')

    frame+=1

    pygame.display.update()
    clock.tick(60)
