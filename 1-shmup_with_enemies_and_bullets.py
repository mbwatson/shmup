# Pygame template - skeleton for a new pygame project
import pygame
import random

WIDTH = 480
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((50,10))
		self.image.fill(GREEN)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 10
		self.dx = 0

	def update(self):
		self.dx = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT] and self.rect.left > 0:
			self.dx = -5
		if keystate[pygame.K_RIGHT] and self.rect.right < WIDTH:
			self.dx = 5
		self.rect.x += self.dx

	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((5,5))
		self.image.fill(YELLOW)
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.bottom = y
		self.dy = -10

	def update(self):
		self.rect.y += self.dy
		# kill if leaves top of screen
		if self.rect.bottom < 0:
			self.kill()

class Mob(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((20,20))
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-100,-40)
		self.dx = random.randrange(-5,5)
		self.dy = random.randrange(1,8)

	def update(self):
		self.rect.x += self.dx
		self.rect.y += self.dy
		if self.rect.top > HEIGHT + 10 or self.rect.right < 0 or self.rect.left > WIDTH:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100,-40)
			self.dx = random.randrange(-5,5)
			self.dy = random.randrange(1,8)

# All Characters
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Spawn mobs
for i in range(10):
	m = Mob()
	all_sprites.add(m)
	mobs.add(m)

# Game loop
running = True

while running:
	# keep loop running at the right speed
	clock.tick(FPS)
	# Process input (events)
	for event in pygame.event.get():
		# check for closing window
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.shoot()

	# Update
	all_sprites.update()

	# check for collisions of bullets and mobs
	hits = pygame.sprite.groupcollide(bullets, mobs, True, True)
	for hit in hits:
		newmob = Mob()
		all_sprites.add(newmob)
		mobs.add(newmob)

	# check for collisions of player and all mobs
	hits = pygame.sprite.spritecollide(player, mobs, False)
	if hits:
		running = False

	# Draw / render
	screen.fill(BLACK)
	all_sprites.draw(screen)
	# *after* drawing everything, flip the display
	pygame.display.flip()

pygame.quit()
