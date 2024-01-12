import pygame
import math
from scipy import spatial

class Board:
    def __init__(self, width, height):
        self.particles = []
        self.FPS = 60
        self.size = (width, height)
        self.gravity = 0
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        

        
    def mainloop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    particle = Particle(pygame.mouse.get_pos())
                    self.particles.append(particle)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.gravity += 1
                    if event.key == pygame.K_DOWN:
                        self.gravity -= 1
                    
            
            self.screen.fill("black")
            
            for particle in self.particles:
                pygame.draw.circle(self.screen, "white", (particle.x, particle.y), particle.radius)

            pygame.display.flip()
            
            self.update()
            self.clock.tick(self.FPS)
    
    def drawParticle(self):
        pass
    
    def update(self):
        for particle in self.particles:
            particle.calculateAcceleration(self.particles, self.size, self.gravity)
            particle.calculateVelocity(self.size)
            particle.calcutateCordinates()


class Particle:
    def __init__(self, cordinates):
        self.radius = 5
        self.smoothing = 10 # percentage 
        self.ACC_CONSTANT = 10**4
        self.x, self.y = cordinates
        self.accelerationX = 0
        self.accelerationY = 0
        self.velocityX = 0
        self.velocityY = 0
        
    def calculateVelocity(self, size):
        # will be run FPS times a second
        # v = u + at
        self.velocityX = self.velocityX + self.accelerationX
        self.velocityY = self.velocityY + self.accelerationY
        
        self.velocityX = self.velocityX * (100 - self.smoothing) / 100
        self.velocityY = self.velocityY * (100 - self.smoothing) / 100
        
        width, height = size
        
        if self.x <= 0:
            self.velocityX = 5
        if self.x >= width:
            self.velocityX = -5
        if self.y <= 0:
            self.velocityY = 5
        if self.y >= height:
            self.velocityY = -5
        
        
    def calcutateCordinates(self):
        self.x += self.velocityX
        self.y += self.velocityY
        

                
    def calculateAcceleration(self, particles, size, gravity):
        width, height = size
         
        if self.x <= 0:
            return
        if self.x >= width:
            return
        if self.y <= 0:
            return
        if self.y >= height:
            return
        
        particles2 = particles.copy()
        particles2.remove(self)
        nodes = [(particle.x, particle.y) for particle in particles2]
        
        nodes.append((0, self.y))
        nodes.append((self.x, 0))
        nodes.append((self.x, height))
        nodes.append((width, self.y))
        
        
        width, height = size
        
        accelerationX = 0
        accelerationY = -gravity / 100
        
        for node in nodes:
            nodeX, nodeY = node
            dist = math.dist((nodeX, nodeY), (self.x, self.y))
            theta = math.atan2((nodeY - self.y), (nodeX - self.x))
            accelerationX += self.ACC_CONSTANT / (dist ** 2) * math.cos(theta)
            accelerationY += self.ACC_CONSTANT / (dist ** 2) * math.sin(theta)

        
        self.accelerationX = -accelerationX
        self.accelerationY = -accelerationY
        
        
        
        
        