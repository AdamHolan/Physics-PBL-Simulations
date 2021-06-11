# Anika Jade Tan
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
width = 800
height = 800

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
numParticles = 50
boltzmannConstant = 1.380649 * 10 ** -23
energyList = []

#--------------------------------------------------------------------------------------#
#                                   PYGAME OBJECTS
#--------------------------------------------------------------------------------------#
class Particle():
    def __init__(self, x, y, mass, size, charge, angle = r.uniform(0, m.pi*2)):
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
            sprites.append(Photon(midPos[0] + 2, midPos[1] + 2))
            destroyed.append(midPos)
            # print(midPos)
        else:
            angle = m.atan2(dy, dx) + 0.5 * m.pi
            p1.angle, p1.speed = addVectors((p1.angle, 0), (angle, p1.speed))
            p2.angle, p2.speed = addVectors((p2.angle, 0), (angle + m.pi, p2.speed))

            # Swap speeds in one line by constructing a tuple
            p1.speed, p2.speed = (p2.speed, p1.speed)

#--------------------------------------------------------------------------------------#
#                               OBJECT INSTANTIATION
#--------------------------------------------------------------------------------------#

for i in range(int(numParticles/2)):
    mass = 5
    # NOTE: Here radius = mass
    p = Particle(r.randint(0, width), r.randint(0, height), mass, mass, 1)
    p2 =  Particle(r.randint(0, width), r.randint(0, height), mass, mass, -1)
    sprites.append(p)
    sprites.append(p2)

#--------------------------------------------------------------------------------------#
#                                        MAIN
#--------------------------------------------------------------------------------------#

frame = 0
photons = 1
# Main loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                photons *= -1

    # Wipes screen every time to avoid clipping and stuff
    screen.fill(black)

    for i, sprite in enumerate(sprites):
        sprite.display()
        sprite.bounce()

        for particle in sprites[i+1:]:
            if sprite.size > 0 and particle.size > 0: 
                collide(sprite, particle)

        for point in destroyed:
            for particle in sprites:
                if particle.size == 0 and (int(particle.x), int(particle.y)) == (int(point[0]), int(point[1])):
                    destroyed.remove(point)
                    sprites.remove(particle)
                    print(particle, end='')
                    print('at: ' + str((int(particle.x), int(particle.y))) + ' and the destroyed point it hit is: ' + str((int(point[0]), int(point[1]))))
                    mass = 5
                    angle1 = r.uniform(0, m.pi)
                    angle2 = angle1 - m.pi
                    diff = point
                    p1 = Particle(point[0] + 10, point[1] + 10, mass, mass, 1, angle1)
                    p2 = Particle(point[0] - 10, point[1] - 10, mass, mass, -1, angle2)
                    sprites.append(p1)
                    sprites.append(p2)
                    

        if sprite.size == 0:
            if len(sprite.bumps) > 1:
                sprite.bumps.remove(sprite.bumps[0])

        sprite.move()
    
    # Display graphics
    pygame.display.flip()
    clock.tick(60)
