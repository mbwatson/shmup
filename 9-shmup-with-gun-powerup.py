# Pygame template - skeleton for a new pygame project
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>

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
LASERBLUE = (0, 189, 242)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('monospace')
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

def draw_ammo_bar(surface, x, y, amt):
	if amt < 0:
		amt = 0
	BAR_LENGTH = 100
	BAR_HEIGHT = 20
	fill = (amt / float(player.max_ammo)) * BAR_LENGTH
	bar_outline = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
	bar_fill = pygame.Rect(x, y, fill, BAR_HEIGHT)	
	pygame.draw.rect(surface, LASERBLUE, bar_fill)
	pygame.draw.rect(surface, WHITE, bar_outline, 2)

def draw_lives(surface, x, y, lives, img):
	for i in range(lives):
		img_rect = img.get_rect()
		img_rect.x = x - 30 * i
		img_rect.y = y
		surface.blit(img, img_rect)

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
		self.shoot_delay = 100
		self.last_shot = pygame.time.get_ticks()
		self.lives = 3
		self.hidden = False
		self.hide_timer = pygame.time.get_ticks()
		self.power = 1
		self.power_time = pygame.time.get_ticks()
		self.max_ammo = 50
		self.ammo = 50
		self.last_ammo_add = pygame.time.get_ticks()

	def update(self):
		# unhide if hidden
		if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
			self.hidden = False
			self.rect.centerx = WIDTH / 2
			self.rect.bottom = HEIGHT - 10
		self.dx = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT] and self.rect.left > 0:
			self.dx = -5
		if keystate[pygame.K_RIGHT] and self.rect.right < WIDTH:
			self.dx = 5
		if keystate[pygame.K_SPACE] and player.ammo > 0:
			self.shoot()
		self.rect.x += self.dx
		now = pygame.time.get_ticks()
		if now - self.last_shot >= 1000 and now - self.last_ammo_add >= 1000 and self.ammo < self.max_ammo:
			self.ammo += 1
			self.last_ammo_add = pygame.time.get_ticks()

	def powerup(self):
		self.power = min(self.power + 1, 3)
		self.power_time = pygame.time.get_ticks()

	def shoot(self):
		now = pygame.time.get_ticks()
		if now - self.last_shot >= self.shoot_delay:
			self.last_shot = now
			self.ammo -= 1
			if self.power == 1 or self.power == 3:
				bullet = Bullet(self.rect.centerx, self.rect.top)
				all_sprites.add(bullet)
				bullets.add(bullet)
			shoot_sound.play()
			if self.power == 2 or self.power == 3:
				left_bullet = Bullet(self.rect.left, self.rect.centery)
				right_bullet = Bullet(self.rect.right, self.rect.centery)
				all_sprites.add(left_bullet)
				all_sprites.add(right_bullet)
				bullets.add(left_bullet)
				bullets.add(right_bullet)

	def hide(self):
		# temporarily hide player
		self.hidden = True
		self.hide_timer = pygame.time.get_ticks()
		self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(bullet_img, (3, 27))
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

class Pow(pygame.sprite.Sprite):
	def __init__(self, center, dx, dy):
		pygame.sprite.Sprite.__init__(self)
		self.type = random.choice(['gun', 'shield'])
		self.image = powerup_images[self.type]
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.dx = dx
		self.dy = dy / 2 + 1

	def update(self):
		self.rect.x += self.dx
		self.rect.y += self.dy
		# kill if leaves bottom of screen
		if self.rect.top > HEIGHT:
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
		self.rect.x = random.randrange(WIDTH)
		self.rect.y = random.randrange(-150,-100)
		self.dx = random.randrange(-1,1)
		self.dy = random.randrange(1,3)
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

class Explosion(pygame.sprite.Sprite):
	def __init__(self, type, center, dx, dy):
		pygame.sprite.Sprite.__init__(self)
		self.type = type
		self.image = explosion_anim[self.type][0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.dx = dx
		self.dy = dy
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50

	def update(self):
		self.rect.centerx += self.dx
		self.rect.centery += self.dy
		now = pygame.time.get_ticks()
		if now - self.last_update >= self.frame_rate:
			self.frame += 1
			if self.frame == len(explosion_anim[self.type]):
				self.kill()
			else:
				self.image = explosion_anim[self.type][self.frame]
			self.last_update = now

##########################
# Load all game graphics #
##########################

background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_blue.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, "laserBlue01.png")).convert()
shield_powerup_img = pygame.image.load(path.join(img_dir, "shield_gold.png")).convert()
gun_powerup_img = pygame.image.load(path.join(img_dir, "star_gold.png")).convert()
meteor_images = []
meteor_list = [ "meteorGrey_big1.png", "meteorGrey_big2.png", "meteorGrey_big3.png", "meteorGrey_big4.png", 
				"meteorGrey_med1.png", "meteorGrey_med2.png", "meteorGrey_small1.png",
				"meteorGrey_small2.png", "meteorGrey_tiny1.png", "meteorGrey_tiny2.png"]
for filename in meteor_list:
	meteor_images.append(pygame.image.load(path.join(img_dir, filename)).convert())
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['death'] = []
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png'))
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'star_gold.png'))

for i in range(9):
	filename = 'regularExplosion0{}.png'.format(i)
	img = pygame.image.load(path.join(img_dir, filename)).convert()
	img.set_colorkey(BLACK)
	img_lg = pygame.transform.scale(img, (75, 75))
	explosion_anim['lg'].append(img_lg)
	img_sm = pygame.transform.scale(img, (32, 32))
	explosion_anim['sm'].append(img_sm)
	filename = "sonicExplosion0{}.png".format(i)
	img = pygame.image.load(path.join(img_dir, filename)).convert()
	img.set_colorkey(BLACK)
	explosion_anim['death'].append(img)

########################
# Load all game sounds #
########################

shoot_sound = pygame.mixer.Sound(path.join(snd_dir, "shoot.wav"))
shoot_sound.set_volume(1)
explosion_sounds = []
for filename in ["explosion.wav"]:
	explosion_sounds.append(pygame.mixer.Sound(path.join(snd_dir, filename)))
for snd in explosion_sounds:
	snd.set_volume(1)
hurt_sound = pygame.mixer.Sound(path.join(snd_dir, "hurt.wav"))
hurt_sound.set_volume(1)
powerup_sound = pygame.mixer.Sound(path.join(snd_dir, "powerup.wav"))
powerup_sound.set_volume(1)
death_sound = pygame.mixer.Sound(path.join(snd_dir, "rumble.ogg"))
death_sound.set_volume(1)
pygame.mixer.music.load(path.join(snd_dir, "tgfcoder-FrozenJam-SeamlessLoop.ogg"))
pygame.mixer.music.set_volume(0.50)

###########################
# Generate all characters #
###########################

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

bullets = pygame.sprite.Group()

powerups = pygame.sprite.Group()

# Spawn mobs
for i in range(10):
	spawn_mob()

# Initialize score
score = 0

# Cue music!
pygame.mixer.music.play(-1)

# # # # # # # # # # # # # # #
# # # # # # # # # # # # # # #
# # #     Game loop     # # #
# # # # # # # # # # # # # # #
# # # # # # # # # # # # # # #

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
			if event.key == pygame.K_ESCAPE:
				running = False

	# Update all Sprites
	all_sprites.update()

	# Bullets / Mobs Collision
	hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
	for hit in hits:
		score += ( 100 - hit.radius ) / 2 + 1
 		random.choice(explosion_sounds).play()
 		explosion = Explosion('lg', hit.rect.center, hit.dx, hit.dy)
 		all_sprites.add(explosion)
 		if random.random() > 0.95:        
 			pow = Pow(hit.rect.center, hit.dx, hit.dy)
 			all_sprites.add(pow)
 			powerups.add(pow)
		spawn_mob()

	# Player / Mobs Collision
	hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
	for hit in hits:
 		explosion = Explosion('sm', hit.rect.center, 0, 0)
 		all_sprites.add(explosion)
		hurt_sound.play()
 		player.shield -= hit.radius
		player.power = max(1, player.power - 1)
		spawn_mob()
		if player.shield <= 0:
			death_explosion = Explosion('death', player.rect.center, 0, 0)
			death_sound.play()
			all_sprites.add(death_explosion)
			player.hide()
			player.lives -= 1
			player.shield = 100
			player.ammo = player.max_ammo
			player.power = 1

	# Player / Powerups Collision
	hits = pygame.sprite.spritecollide(player, powerups, True)
	for hit in hits:
		score += 500
		powerup_sound.play()
		if hit.type == 'shield':
			player.shield = min(player.shield + 20, 100)
		if hit.type == 'gun':
			player.powerup()
	
	# Bullets / Powerups Collision
	hits = pygame.sprite.groupcollide(bullets, powerups, True, True)
	for hit in hits:
		hit.kill()
	
	# if player dies and explosion has finished
	if player.lives == 0 and not death_explosion.alive():
		running = False

	# Draw / render
	screen.fill(BLACK)
	screen.blit(background, background_rect)
	all_sprites.draw(screen)
	draw_text(screen, str(score), 18, WIDTH / 2, 10)
	draw_shield_bar(screen, 5, 5, player.shield)
	draw_ammo_bar(screen, 5, 30, player.ammo)
	# draw_text(screen, "Power: {}".format(str(player.power)), 12, 35, 30)
	draw_lives(screen, WIDTH - 30, 5, player.lives, player_mini_img )
	# *after* drawing everything, flip the display
	pygame.display.flip()

pygame.quit()