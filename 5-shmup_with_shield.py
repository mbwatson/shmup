# Pygame template - skeleton for a new pygame project
# Music: "Ove Melaa - High Stakes,Low Chances" written and produced by Ove Melaa (Omsofware@hotmail.com) 
#   Or Additional samples by Ove Melaa (Omsofware@hotmail.com) -2013 Ove Melaa
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")

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

font_name = pygame.font.match_font('arial')
def draw_text(surface, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, WHITE) # T/F for anti-aliasing
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x,y)
	surface.blit(text_surface, text_rect)

def draw_shield_bar(surface, x, y, amt):
	if amt < 0:
		amt = 0
	BAR_LENGTH = 100
	BAR_HEIGHT = 20
	fill = (amt / 100.0) * BAR_LENGTH
	bar_outline = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
	bar_fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surface, GREEN, bar_fill)
	pygame.draw.rect(surface, WHITE, bar_outline, 2)
	# draw_text(surface, str(amt), 18, 10, 30)

def spawn_mob():
	mob = Mob()
	all_sprites.add(mob)
	mobs.add(mob)

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(player_img, (50, 38))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.radius = 20
		# pygame.draw.circle(self.image, BLUE, self.rect.center, self.radius)
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 10
		self.dx = 0
		self.shield = 100

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
		shoot_sound.play()

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
		# pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-150,-100)
		self.dx = random.randrange(-4,4)
		self.dy = random.randrange(1,5)
		self.rot = 0
		self.drot = random.randrange(-5,5)
		self.last_update = pygame.time.get_ticks()

	def update(self):
		self.rotate()
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
# Load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, "Laser_Shoot14.wav"))
shoot_sound.set_volume(0.25)
explosion_sounds = []
for filename in ["Explosion2.wav", "Explosion5.wav"]:
	explosion_sounds.append(pygame.mixer.Sound(path.join(snd_dir, filename)))
for snd in explosion_sounds:
	snd.set_volume(0.5)
pygame.mixer.music.load(path.join(snd_dir, "Ove Melaa - High Stakes,Low Chances.mp3"))
pygame.mixer.music.set_volume(0.75)

# All Characters
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Spawn mobs
for i in range(10):
	spawn_mob()
# Initialize score
score = 0

# Cue music!
pygame.mixer.music.play()

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
	hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
	for hit in hits:
		score += 50 - hit.radius
 		random.choice(explosion_sounds).play()
		spawn_mob()

	# check for collisions of player and all mobs
	hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
	for hit in hits:
		# spawn_mob()
		player.shield -= hit.radius
		if player.shield <= 0:
			running = False

	# Draw / render
	screen.fill(BLACK)
	screen.blit(background, background_rect)
	all_sprites.draw(screen)
	draw_text(screen, str(score), 18, WIDTH / 2, 10)
	draw_shield_bar(screen, 5, 5, player.shield)
	# *after* drawing everything, flip the display
	pygame.display.flip()

pygame.quit()
