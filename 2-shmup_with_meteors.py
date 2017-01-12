# Pygame template - skeleton for a new pygame project
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), "img")

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
		self.image = pygame.transform.scale(player_img, (50, 38))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.radius = 20
		pygame.draw.circle(self.image, BLUE, self.rect.center, self.radius)
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
		self.image = pygame.transform.scale(bullet_img, (6, 27))
		self.image.set_colorkey(BLACK)
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
		self.image_original = random.choice(meteor_images)
		self.image_original.set_colorkey(BLACK)
		self.image = self.image_original.copy()
		self.rect = self.image.get_rect()
		self.radius = int(self.rect.width * 0.85 / 2)
		pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-150,-100)
		self.dx = random.randrange(-4,4)
		self.dy = random.randrange(1,5)
		self.rot = 0
		self.drot = random.randrange(-5,5)
		self.last_update = pygame.time.get_ticks()

	def update(self):
		# self.rotate()
		self.rect.x += self.dx
		self.rect.y += self.dy
		if self.rect.top > HEIGHT + 10 or self.rect.right < 0 or self.rect.left > WIDTH:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100,-40)
			self.dx = random.randrange(-4,4)
			self.dy = random.randrange(1,5)

	def rotate(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > 50:
			self.last_update = now
			self.rot = (self.rot + self.drot) % 360
			new_image = pygame.transform.rotate(self.image_original, self.rot)
			old_center = self.rect.center
			self.image = new_image
			self.rect = self.image.get_rect()
			self.rect.center = old_center

# Load all game graphics
background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
meteor_images = []
meteor_list = [ "meteorBrown_big1.png", "meteorBrown_big2.png", "meteorBrown_big3.png", "meteorBrown_big4.png", 
				"meteorBrown_med1.png", "meteorBrown_med2.png", "meteorBrown_small1.png",
				"meteorBrown_small2.png", "meteorBrown_tiny1.png", "meteorBrown_tiny2.png"]
for img in meteor_list:
	meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())				

# All Characters
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Spawn mobs
for i in range(10):
	mob = Mob()
	all_sprites.add(mob)
	mobs.add(mob)

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
	hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
	if hits:
		running = False

	# Draw / render
	screen.fill(BLACK)
	screen.blit(background, background_rect)
	all_sprites.draw(screen)
	# *after* drawing everything, flip the display
	pygame.display.flip()

pygame.quit()
