import pygame
import random as r
import math as m
from pygame import gfxdraw

# some colours
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

#                               PYGAME INITIAL CONDITIONS
#--------------------------------------------------------------------------------------#
pygame.init()

# screen dimensions
width = 1200
height = 900

# # Generate random colour. Looks pretty and saves time hardcoding stuff idk
# def randColour():
#     colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#     return colour

# set screen size & instantiate
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Particle Collisions')

# loop until close
done = False

# screen updates (for readability)
clock = pygame.time.Clock()

# Specific Globals
numParticles = 10
boltzmannConstant = 1.380649 * 10 ** -23
energyList = []

visualtext = []
font = pygame.font.Font('freesansbold.ttf', 24)
visualtext.append(font.render('Press to Disable Visuals', True, white, black))
visualtext.append(font.render('I -> Particles ', True,          white, black))
visualtext.append(font.render('P -> Photons ', True,            white, black))
visualtext.append(font.render( 'O -> Collision Points' , True,  white, black))

# in reverse order to work with positioning
physicstext = []
physicstext.append(font.render('                                     ', True,   white, black)) 
physicstext.append(font.render('Click to add a Particle Pair at any Location',               True,   white, black))
physicstext.append(font.render('                                     ', True,   white, black)) 
physicstext.append(font.render('Press Space to Add a Particle Pair Randomly',      True,   white, black)) 
       
       
                    
textRect = visualtext[0].get_rect()
textRect.height *= len(visualtext)
textRect.center = (width // 2, height // 2)

#--------------------------------------------------------------------------------------#
#                                   PYGAME OBJECTS
#--------------------------------------------------------------------------------------#
class Particle():
    def __init__(self, x, y, mass, size, charge, angle = 0):
        if angle == 0:
            angle = r.uniform(0, m.pi*2)
        self.x = x; self.y = y
        self.mass = mass
        self.size = size
        self.charge = charge
        self.angle = angle
        self.speed = r.randint(7, 10)
        self.energy = 0.5 * self.mass * (self.speed ** 2)

    def display(self):
        try:
            pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), self.size, (255 * (self.charge > 0), 0, 255 * (self.charge < 0)))
        except OverflowError:
            pass

    # Speed is a vector and thus can be represented by its direction, determined by it's angle, and its magnitude, which I call speed for simplicities sake:
    def move(self):
        self.x += m.sin(self.angle) * self.speed
        self.y -= m.cos(self.angle) * self.speed
        self.energy = 0.5 * self.mass * (self.speed ** 2)

    def bounce(self):
        # Clever implementation of collision with walls from: http://archive.petercollingridge.co.uk/book/export/html/6

        # Right boundary
        if self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.angle = - self.angle

        # Left boundary
        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle

        # Top boundary
        if self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.angle = m.pi - self.angle

        # Bottom boundary
        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = m.pi - self.angle


class Photon():
    def __init__(self, x, y):
        self.x, self.y = (x, y)
        self.bumps = [(x, y)] 
        self.speed = 70
        self.angle = r.uniform(0, m.pi)
        self.size = 0

    def display(self):
        currentPos = (self.x, self.y)
        self.bumps.append(currentPos)
        for i in range(len(self.bumps) - 1):
            pygame.draw.line(screen, yellow, self.bumps[i], self.bumps[i+1])
            pass # for debugging
        self.bumps.remove(currentPos)

    def move(self):
        self.x += m.sin(self.angle) * self.speed
        self.y -= m.cos(self.angle) * self.speed

    def bounce(self):
        # Clever implementation of collision with walls from: http://archive.petercollingridge.co.uk/book/export/html/6
        # Right boundary
        if self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.angle = - self.angle
            self.bumps.append((self.x, self.y))

        # Left boundary
        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle
            self.bumps.append((self.x, self.y))

        # Top boundary
        if self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.angle = m.pi - self.angle
            self.bumps.append((self.x, self.y))

        # Bottom boundary
        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = m.pi - self.angle
            self.bumps.append((self.x, self.y))


#--------------------------------------------------------------------------------------#
#                                DEFINING FUNCTIONS
#--------------------------------------------------------------------------------------#

# Adding angle and length components of vectors together
def addVectors(vector1, vector2):
    a1, l1 = vector1
    a2, l2 = vector2
    x = m.sin(a1) * l1 + m.sin(a2) * l2
    y = m.cos(a1) * l1 + m.cos(a2) * l2
    length = m.hypot(x, y)
    angle = 0.5 * m.pi - m.atan2(y, x)
    return angle, length

sprites = []
destroyed = []
photons = []
# Collision function
def collide(p1, p2):

    # Linear algebra
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    distance = m.hypot(dx, dy)
    
    if distance < p1.size + p2.size:
        if p1.charge == p2.charge * -1:
            # print(p1.charge, p2.charge)
            sprites.remove(p1)
            sprites.remove(p2)
            midPos = ((p1.x + p2.x)/2, (p1.y + p2.y)/2)
            photons.append(Photon(midPos[0] + 2, midPos[1] + 2))
            destroyed.append(midPos)
            # print(midPos)
        else:
            angle = m.atan2(dy, dx) + 0.5 * m.pi
            p1.angle, p1.speed = addVectors((p1.angle, 0), (angle, p1.speed))
            p2.angle, p2.speed = addVectors((p2.angle, 0), (angle + m.pi, p2.speed))

            # Swap speeds in one line by constructing a tuple
            p1.speed, p2.speed = (p2.speed, p1.speed)

def addRandomParticles():
    mass = 5
    # NOTE: Here radius = mass
    p = Particle(r.randint(0, width), r.randint(0, height), mass, mass, 1)
    p2 =  Particle(r.randint(0, width), r.randint(0, height), mass, mass, -1)
    sprites.append(p)
    sprites.append(p2)

def addPreciseParticles(coordinate):
    # init of variables for a generic particle
    mass = 5
    angle1 = r.uniform(0, m.pi)
    # i think this was for tangent math but i dont honestly know at this point
    angle2 = angle1 - m.pi
    # create particles
    p1 = Particle(coordinate[0] + 10, coordinate[1] + 10, mass, mass, 1, angle1)
    p2 = Particle(coordinate[0] - 10, coordinate[1] - 10, mass, mass, -1, angle2)

    # append particles to list
    sprites.append(p1)
    sprites.append(p2)

#--------------------------------------------------------------------------------------#
#                               OBJECT INSTANTIATION
#--------------------------------------------------------------------------------------#

for i in range(int(numParticles/2)):
    addRandomParticles()

#--------------------------------------------------------------------------------------#
#                                        MAIN
#--------------------------------------------------------------------------------------#

# variables for controlling display+
frame = 0
displayParticles = 1
displayPhotons = 1
displayInactive = 1

# Main loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:

            # Controlling visuals
            if event.key == pygame.K_i:
                displayParticles *= -1
            if event.key == pygame.K_p:
                displayPhotons *= -1
            if event.key == pygame.K_o:
                displayInactive *= -1

            # Controlling physics
            if event.key == pygame.K_SPACE:
                addRandomParticles()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            addPreciseParticles(pos)   

    # Wipes screen every time to avoid clipping and stuff
    screen.fill(black)

    # Control the behaviour of particles
    for i, sprite in enumerate(sprites):
        

        for particle in sprites[i+1:]:
            # if sprite.size > 0 and particle.size > 0: 
            collide(sprite, particle)

        sprite.bounce()
        sprite.move()

        # particle display control
        if displayParticles > 0:
            sprite.display()
    
    # Code for controlling the behaviour of photons
    for i, quanta in enumerate(photons):

        for point in destroyed:
            for particle in photons:
                # if a particle meets a point where it can become matter
                if particle.size == 0 and (int(particle.x), int(particle.y)) == (int(point[0]), int(point[1])):
                    # remove the point from the lists
                    destroyed.remove(point)
                    photons.remove(particle)

                    # debug
                    print(particle, end='')
                    print('at: ' + str((int(particle.x), int(particle.y))) + ' and the destroyed point it hit is: ' + str((int(point[0]), int(point[1]))))
        
                    addPreciseParticles(point)
            
            # control deadzone display
            if displayInactive > 0:
                gfxdraw.pixel(screen, int(point[0]), int(point[1]), white)
        
        # i made code that draws the trails but this snips it and you can change the inequality to make photons have tails
        if len(quanta.bumps) > 1:
            quanta.bumps.remove(quanta.bumps[0])

        quanta.bounce()
        quanta.move()

        # control photon display
        if displayPhotons > 0:
            quanta.display()

    for i in range(len(visualtext)):
        screen.blit(visualtext[i], (0, 24*i))

    for i in reversed(range(len(physicstext))):
        screen.blit(physicstext[i], (0, height - 24*(i + 1)))

    # Display graphics
    pygame.display.flip()
    clock.tick(60)
