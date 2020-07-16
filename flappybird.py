import pygame
import random
import time

pygame.init()

bird_images=[
		pygame.transform.scale(pygame.image.load("images/bird1.png"),(40,40)),
		pygame.transform.scale(pygame.image.load("images/bird2.png"),(40,40)),
		pygame.transform.scale(pygame.image.load("images/bird3.png"),(40,40))
	]

background_image = pygame.image.load("images/background.png")
base_image = pygame.image.load("images/base.png")
pipe_image = pygame.image.load("images/pipe.png")

class Bird:
	def __init__(self,x,y):
		self.IMGS = bird_images
		self.image = self.IMGS[0]	
		self.image_count = 0
		self.dead = False
		self.rect =	self.image.get_rect()
		self.rect.left = x
		self.rect.top = y
		self.is_alive = True
		self.vel = 0
		self.time = time.perf_counter()
		self.gravity = 0.1
		self.angle = 0
		self.animation_time = 5
		self.max_rotation = 45
		self.rotated_bird = self.image

	def rotate(self):
		if self.vel <- 2:
			self.angle = self.max_rotation
		elif self.vel > 4:
			self.angle =- self.max_rotation*2
		else:
			self.angle =- self.vel*22.5

		self.rotated_bird = pygame.transform.rotozoom(self.image, self.angle, 1)

	def animate(self):
		if self.image_count <= self.animation_time:
			self.image = self.IMGS[0]
		elif self.image_count <= self.animation_time*2:
			self.image = self.IMGS[1]
		elif self.image_count <= self.animation_time*3:
			self.image = self.IMGS[2]
		elif self.image_count <= self.animation_time*4:
			self.image = self.IMGS[1]
		elif self.image_count == self.animation_time*4 + 1:
			self.image = self.IMGS[0]
			self.image_count = 0
		self.image_count += 1
		
	def move(self):
		# if self.dead is True:
		# 	pass
		if self.time < time.perf_counter() - 0.015:
			self.vel += self.gravity
			self.time = time.perf_counter()
		self.rotate()	

		self.rect.top += self.vel

	def jump(self):
		if self.is_alive is True:
			self.vel =- 2

	def draw(self, win):
		self.animate()
		win.blit(self.rotated_bird, self.rect)


class Pipe:
	def __init__(self,x,y, is_bottom_pipe):
		self.image = pipe_image
		self.image = pygame.transform.scale(self.image, (90, 450))
		self.rect =	self.image.get_rect()
		self.is_bottom_pipe = is_bottom_pipe
		self.rect.left = x
		self.rect.top = y
		if is_bottom_pipe is False:
			self.image = pygame.transform.rotate(self.image, 180)

	def move(self,top = None,left = None):
		self.rect.left -= 1

	def rotate_pipe(self):
		self.image = pygame.transform.rotate(self.image, 180)

	def draw(self, win):
		win.blit(self.image, self.rect)


class Base:
	def __init__(self):
		self.image = base_image
		self.image = pygame.transform.scale(self.image,(800,100))
		self.rect = self.image.get_rect()
		self.rect.top = 400
		self.rect.left = 0

	def move(self):
		if self.rect.left <- 100:
			self.rect.left = 0
		self.rect.left -= 1

	def draw(self, win):
		win.blit(self.image, self.rect)

class Background:
	def __init__(self):
		self.image = background_image

	def draw(self, win):
		win.blit(self.image, [0, 0])

class Text:
	def __init__(self, text):
		pygame.font.init()          
		self.myfont = pygame.font.SysFont('Comic Sans MS', 20)
		self.textsurface = self.myfont.render(text, False, (0, 0, 0))

	def update(self, text):
		self.textsurface = self.myfont.render(text, False, (0, 0, 0))

	def draw(self,win):
		win.blit(self.textsurface, (0, 0))


class Game:
	def __init__(self, width=640, height=480):
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((self.width, height))
		self.bird = Bird(width/3,height/2)
		self.nr_of_pipes = 3
		self.space_between_pipes = 130
		self.bot_pipe = [Pipe(width, height, True) for i in range(self.nr_of_pipes)]
		self.top_pipe = [Pipe(width, height, False) for i in range(self.nr_of_pipes)]
		self.base = Base()
		self.bg = Background()
		self.score_last =- 1
		self.score_value = 0
		self.text = Text(f'Score: {self.score_value}')

	def create_pipes(self):
		for i in range(self.nr_of_pipes):
			y_random = random.randint(-400,-200)
			self.bot_pipe[i].rect.top = y_random+self.space_between_pipes + self.top_pipe[i].rect.height
			self.top_pipe[i].rect.top = y_random
			self.bot_pipe[i].rect.left = self.width + i*(self.width+self.bot_pipe[i].rect.width)/self.nr_of_pipes
			self.top_pipe[i].rect.left = self.width + i*(self.width+self.bot_pipe[i].rect.width)/self.nr_of_pipes

	def is_collison(self):
		for i in range(self.nr_of_pipes):
			if  (
					self.bird.rect.colliderect(self.top_pipe[i].rect) or 
					self.bird.rect.colliderect(self.bot_pipe[i].rect) or 
					self.bird.rect.colliderect(self.base.rect)
				):
				self.bird.is_alive=False
				return True
			if  (
					self.bird.rect.left > self.top_pipe[i].rect.left and
					(
						(
							self.score_last == 2 and
							i == 0
						) or
						(
							self.score_last == i - 1
						)
					)
				):
				self.score_last = i
				self.score_value+=1

	def move(self):
		self.bird.move()
		for i in range(self.nr_of_pipes):
			self.bot_pipe[i].move(self.bot_pipe[i].rect.top, self.bot_pipe[i].rect.left + i*self.width/self.nr_of_pipes)
			self.top_pipe[i].move(self.top_pipe[i].rect.top, self.top_pipe[i].rect.left + i*self.width/self.nr_of_pipes)
			if self.bot_pipe[i].rect.left + self.bot_pipe[i].rect.width < 0:
				self.bot_pipe[i].rect.left = self.width
				self.top_pipe[i].rect.left = self.width

				y_random = random.randint(-400, -200)
				self.bot_pipe[i].rect.top = y_random+self.space_between_pipes + self.top_pipe[i].rect.height
				self.top_pipe[i].rect.top = y_random

		self.base.move()
		self.text.update(f'Score: {self.score_value}')

	def draw(self):
		self.bg.draw(self.screen)
		for i in range((self.nr_of_pipes)):
			self.bot_pipe[i].draw(self.screen)
			self.top_pipe[i].draw(self.screen)
		self.base.draw(self.screen)
		self.bird.draw(self.screen)
		self.text.draw(self.screen) 

	def restart(self):
		self.bird=Bird(self.width/3,self.height/2)
		self.create_pipes()
		self.score_last =- 1
		self.score_value = 0

	def game_on(self):
		self.restart()
		running=True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				if event.type == pygame.KEYDOWN:
					self.bird.jump() 
			self.move()
			self.draw()
			if self.is_collison():	
				time.sleep(1)
				self.restart()

			pygame.display.update()
			

game=Game()
game.game_on()

pygame.quit()
