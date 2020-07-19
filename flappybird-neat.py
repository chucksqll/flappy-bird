import pygame
import random
import time
import os
import neat
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
		self.score=0

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
		self.vel += self.gravity
		self.rotate()	
		self.rect.top += self.vel

	def jump(self):
		if self.is_alive is True:
			self.vel = -2.5

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
		self.rect.left -= 2

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
		self.rect.left -= 2

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
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption('Flappy Bird Neat')
		self.nr_of_birds = 20
		self.birds = []
		self.nr_of_pipes = 3
		self.space_between_pipes = 130
		self.bot_pipes = [Pipe(width, height, True) for i in range(self.nr_of_pipes)]
		self.top_pipes = [Pipe(width, height, False) for i in range(self.nr_of_pipes)]
		self.base = Base()
		self.bg = Background()
		self.score_last =- 1
		self.score_value = 0
		self.text = Text(f'Score: {self.score_value}')

	def create_pipes(self):
		self.bot_pipes = [Pipe(self.width, self.height, True) for i in range(self.nr_of_pipes)]
		self.top_pipes = [Pipe(self.width, self.height, False) for i in range(self.nr_of_pipes)]
		for i in range(self.nr_of_pipes):
			y_random = random.randint(-400,-200)
			self.bot_pipes[i].rect.top = y_random+self.space_between_pipes + self.top_pipes[i].rect.height
			self.top_pipes[i].rect.top = y_random
			self.bot_pipes[i].rect.left = self.width + i*(self.width+self.bot_pipes[i].rect.width)/self.nr_of_pipes
			self.top_pipes[i].rect.left = self.width + i*(self.width+self.bot_pipes[i].rect.width)/self.nr_of_pipes

	def is_collison(self, bird):
		for i in range(self.nr_of_pipes):
			if  (
					bird.rect.colliderect(self.top_pipes[i].rect) or 
					bird.rect.colliderect(self.bot_pipes[i].rect) or 
					bird.rect.colliderect(self.base.rect)
				):
				bird.is_alive=False
				return True	

	def is_score(self, bird):
		for i in range(self.nr_of_pipes):
			if  (
					bird.rect.left > self.top_pipes[i].rect.left+self.top_pipes[i].rect.width and
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
				bird.score +=1
				return True

	def move(self):
		for bird in self.birds:
			bird.move()

		for i in range(self.nr_of_pipes):
			self.bot_pipes[i].move(self.bot_pipes[i].rect.top, self.bot_pipes[i].rect.left + i*self.width/self.nr_of_pipes)
			self.top_pipes[i].move(self.top_pipes[i].rect.top, self.top_pipes[i].rect.left + i*self.width/self.nr_of_pipes)
			if self.bot_pipes[i].rect.left + self.bot_pipes[i].rect.width < 0:
				self.bot_pipes[i].rect.left = self.width
				self.top_pipes[i].rect.left = self.width

				y_random = random.randint(-400, -200)
				self.bot_pipes[i].rect.top = y_random+self.space_between_pipes + self.top_pipes[i].rect.height
				self.top_pipes[i].rect.top = y_random

		self.base.move()
		self.text.update(f'Score: {self.score_value}')

	def draw(self):
		self.bg.draw(self.screen)
		for i in range((self.nr_of_pipes)):
			self.bot_pipes[i].draw(self.screen)
			self.top_pipes[i].draw(self.screen)
		self.base.draw(self.screen)
		for bird in self.birds:
			bird.draw(self.screen)
		self.text.draw(self.screen) 

		pygame.display.update()

	def restart(self):
		self.birds = [Bird(self.width/3,self.height/2) for i in range(self.nr_of_birds)]
		for i, bird in enumerate(self.birds):
			self.birds[i] = Bird(self.width/3,self.height/2)
		self.create_pipes()
		self.score_last =- 1
		self.score_value = 0

	def get_positions(self, bird):
		if self.score_last == 2:
			next_pipe_index = 0
		else:
			next_pipe_index = self.score_last + 1

		x_distance_to_pipe = self.bot_pipes[next_pipe_index].rect.left - bird.rect.left
		y_distance_to_bottom_pipe_top_corner = self.bot_pipes[next_pipe_index].rect.top - bird.rect.top
		y_distance_to_top_pipe_top_corner = self.top_pipes[next_pipe_index].rect.top + self.top_pipes[next_pipe_index].rect.height-bird.rect.top
		
		return(bird.vel, x_distance_to_pipe, y_distance_to_bottom_pipe_top_corner, y_distance_to_top_pipe_top_corner)

	def game_on(self, genomes, config):

		self.restart()

		nets = []
		ge = []
		for _, genome in genomes:
			net = neat.nn.FeedForwardNetwork.create(genome, config)
			nets.append(net)
			ge.append(genome)
			genome.fitness = 0

		clock = pygame.time.Clock()
		running=True
		while running and len(self.birds) > 0 :
			clock.tick(90)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
					pygame.quit()


			self.move()
			self.draw()

			for i, bird in enumerate(self.birds):
				ge[i].fitness += 0.1

				output = nets[i].activate(self.get_positions(bird))

				if output[0] > 0.5:
					bird.jump()

			add_score = False
			for i, bird in enumerate(self.birds):
				if self.is_collison(bird):	
					self.birds
					ge[i].fitness -=1
					self.birds.pop(i)
					nets.pop(i)
					ge.pop(i)

				if self.is_score(bird):
					add_score = True

			if add_score:
				self.score_value +=1
				for g in ge:
					g.fitness += 5



def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    game=Game()
    winner = p.run(game.game_on, 10)



if __name__ == '__main__':
	#runs only if you run it directly by typing python flappybird-neat.py
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-neat.txt')
    run(config_path)
