import pygame
import random

pygame.init()

scr_width, scr_height=640, 480
screen = pygame.display.set_mode((scr_width, scr_height))
class Bird:
	def __init__(self,x,y,velocity):
		self.image = pygame.image.load("images/bird.png")
		self.rect =	self.image.get_rect()
		self.rect.center=scr_width/3, scr_height/2 
		self.x=x
		self.y=y
		self.vel=velocity

	def move():
		pass

	def jump():
		pass

	def draw(self, win):
		screen.blit(self.image,self.rect)

class Pipe:
	SPACE = 50
	def __init__(self):
		self.x=x
		self.width=width

	def move():
		pass

	def draw():
		pass

bg_img = pygame.image.load("images/background.png")
ptak = Bird(100,100,10)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        screen.blit(bg_img, [0, 0])
        ptak.draw(screen)
        pygame.display.flip()


pygame.quit()

