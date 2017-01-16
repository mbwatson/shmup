# Pygame template - skeleton for a new pygame project
# "Dark Ambience Loop by Iwan Gabovitch qubodup.net" or "Dark Ambience Loop by Iwan Gabovitch http://opengameart.org/users/qubodup"

import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")
font_dir = path.join(path.dirname(__file__), "fonts")

WIDTH = 480
HEIGHT = 600
FPS = 60

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LASER_BAR_COLOR = (0, 189, 242)
SHIELD_BAR_COLOR = (255, 199, 56)

# Define fonts
TITLE_FONT = "kenpixel_blocks.ttf"
TEXT_FONT = "kenvector_future_thin.ttf"

# initialize pygame and create window
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

# font_name = pygame.font.match_font('monospace')
def draw_text(surface, text, size, x, y, style = TEXT_FONT):
	# font = pygame.font.Font(font_name, size)
	font = pygame.font.Font(path.join(font_dir, style), size)
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
	pygame.draw.rect(surface, SHIELD_BAR_COLOR, bar_fill)
	pygame.draw.rect(surface, WHITE, bar_outline, 3)

def draw_ammo_bar(surface, x, y, amt):
	if amt < 0:
		amt = 0
	BAR_LENGTH = 100
	BAR_HEIGHT = 20
	fill = (amt / float(player.max_ammo)) * BAR_LENGTH
	bar_outline = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
	bar_fill = pygame.Rect(x, y, fill, BAR_HEIGHT)	
	pygame.draw.rect(surface, LASER_BAR_COLOR, bar_fill)
	pygame.draw.rect(surface, WHITE, bar_outline, 3)

def draw_lives(surface, x, y, lives, img):
	for i in range(lives):
		img_rect = img.get_rect()
		img_rect.x = x - 30 * i
		img_rect.y = y
		surface.blit(img, img_rect)

def spawn_meteor():
	meteor = Meteor()
	all_sprites.add(meteor)
	meteors.add(meteor)

def spawn_enemy():
	enemy_spawn_sound.play()
	enemy = Enemy()
	all_sprites.add(enemy)
	enemies.add(enemy)

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
		self.reload_time = 500

	def update(self):
		# unhide if hidden
		if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
			self.hidden = False
			self.rect.centerx = WIDTH / 2
			self.rect.bottom = HEIGHT - 10
		# OK
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
		if now - self.last_shot >= self.reload_time and now - self.last_ammo_add >= self.reload_time and self.ammo < self.max_ammo:
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

class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(random.choice(enemy_images), (50, 38))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.radius = 20
		self.rect.centerx = random.randrange(30, WIDTH - 30) 
		self.rect.top = 10
		self.dx = 1
		self.dy = 0
		self.last_shot = pygame.time.get_ticks()
		self.shoot_delay = 300
		self.distance_to_player = abs(player.rect.centerx - self.rect.centerx)

	def update(self):
		if self.rect.centerx > player.rect.centerx:
			self.dx = -1
		elif self.rect.centerx < player.rect.centerx:
			self.dx = 1
		else:
			self.dx = 0
		self.rect.x += self.dx
		self.rect.y += self.dy
		self.distance_to_player = abs(player.rect.centerx - self.rect.centerx)
		if self.distance_to_player < 50:
			self.shoot()

	def shoot(self):
		now = pygame.time.get_ticks()
		if now - self.last_shot >= self.shoot_delay:
			self.last_shot = now
			bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
			all_sprites.add(bullet)
			enemy_bullets.add(bullet)
			shoot_sound.play()

class EnemyBullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(enemy_bullet_img, (6, 27))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.bottom = y
		self.dy = 15

	def update(self):
		self.rect.y += self.dy
		# kill if leaves top of screen
		if self.rect.bottom < 0:
			self.kill()

class Meteor(pygame.sprite.Sprite):
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

def show_game_begin_screen():
	screen.blit(background, background_rect)
	draw_text(screen, "SPACE", 70, WIDTH / 2, HEIGHT * 3 / 32, TITLE_FONT)
	draw_text(screen, "BLASTER", 86, WIDTH / 2 + 10, HEIGHT * 6 / 32 - 1, TITLE_FONT)
	draw_text(screen, "C o n t r o l s :", 24, WIDTH / 2, HEIGHT * 7 / 16, TITLE_FONT)
	draw_text(screen, "Move: left & right arrows", 18, WIDTH / 2, HEIGHT * 16 / 32)
	draw_text(screen, "Shoot: spacebar", 18, WIDTH / 2, HEIGHT * 17 /32)
	draw_text(screen, "Press any key to begin", 24, WIDTH / 2, HEIGHT * 28 / 32, TITLE_FONT)
	draw_text(screen, "q to quit", 18, WIDTH / 2, HEIGHT * 30 / 32)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
					pygame.quit()
			if event.type == pygame.KEYUP:
				waiting = False

def show_pause_screen():
	screen.blit(background, background_rect)
	draw_text(screen, "PAUSED!", 64, WIDTH / 2, HEIGHT / 5, TITLE_FONT)
	draw_text(screen, "C o n t r o l s :", 24, WIDTH / 2, HEIGHT * 7 / 16, TITLE_FONT)
	draw_text(screen, "Move: left & right arrows", 18, WIDTH / 2, HEIGHT * 16 / 32)
	draw_text(screen, "Shoot: spacebar", 18, WIDTH / 2, HEIGHT * 17 /32)
	draw_text(screen, "Press any key to resume", 24, WIDTH / 2, HEIGHT * 28 / 32, TITLE_FONT)
	draw_text(screen, "q to quit", 18, WIDTH / 2, HEIGHT * 30 / 32)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
				pygame.quit()
			if event.type == pygame.KEYUP and not event.key == pygame.K_ESCAPE:
				waiting = False

def show_game_over_screen():
	screen.blit(background, background_rect)
	draw_text(screen, "GAME", 70, WIDTH / 2, HEIGHT * 3 / 32, TITLE_FONT)
	draw_text(screen, "OVER", 86, WIDTH / 2 + 10, HEIGHT * 6 / 32 - 1, TITLE_FONT)
	draw_text(screen, "Your score", 24, WIDTH / 2, HEIGHT * 7 / 16, TITLE_FONT)
	draw_text(screen, "Press any key to play again", 24, WIDTH / 2, HEIGHT * 28 / 32, TITLE_FONT)
	draw_text(screen, "q to quit", 18, WIDTH / 2, HEIGHT * 30 / 32)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
					pygame.quit()
			if event.type == pygame.KEYUP:
				waiting = False

##########################
# Load all game graphics #
##########################

background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_blue.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, "laserBlue01.png")).convert()
enemy_bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
shield_powerup_img = pygame.image.load(path.join(img_dir, "shield_gold.png")).convert()
gun_powerup_img = pygame.image.load(path.join(img_dir, "star_gold.png")).convert()
# Enemies
enemy_images = []
enemy_list = [ "enemyRed1.png", "enemyRed2.png", "enemyRed3.png", "enemyRed4.png", "enemyRed5.png"]
for filename in enemy_list:
	enemy_images.append(pygame.image.load(path.join(img_dir, filename)).convert())
# Meteors
meteor_images = []
meteor_list = [ "meteorGrey_big1.png", "meteorGrey_big2.png", "meteorGrey_big3.png", "meteorGrey_big4.png", 
				"meteorGrey_med1.png", "meteorGrey_med2.png", "meteorGrey_small1.png",
				"meteorGrey_small2.png", "meteorGrey_tiny1.png", "meteorGrey_tiny2.png"]
for filename in meteor_list:
	meteor_images.append(pygame.image.load(path.join(img_dir, filename)).convert())
# Explosions
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['death'] = []
# Powerups
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
shoot_sound.set_volume(0.5)
enemy_spawn_sound = pygame.mixer.Sound(path.join(snd_dir, "enemy_spawn.wav"))
enemy_spawn_sound.set_volume(2)
explosion_sounds = []
for filename in ["explosion.wav"]:
	explosion_sounds.append(pygame.mixer.Sound(path.join(snd_dir, filename)))
for snd in explosion_sounds:
	snd.set_volume(0.5)
hurt_sound = pygame.mixer.Sound(path.join(snd_dir, "hurt.wav"))
hurt_sound.set_volume(0.5)
powerup_sound = pygame.mixer.Sound(path.join(snd_dir, "powerup.wav"))
powerup_sound.set_volume(0.5)
death_sound = pygame.mixer.Sound(path.join(snd_dir, "rumble.ogg"))
death_sound.set_volume(0.5)
pygame.mixer.music.load(path.join(snd_dir, "Iwan Gabovitch - Dark Ambience Loop.mp3"))
pygame.mixer.music.set_volume(0.50)

# Cue music!
pygame.mixer.music.play(-1)

# # # # # # # # # # # # # # #
# # # # # # # # # # # # # # #
# # #     Game loop     # # #
# # # # # # # # # # # # # # #
# # # # # # # # # # # # # # #

running = True
game_over = False
paused = False

show_game_begin_screen()
# Generate all characters
all_sprites = pygame.sprite.Group()
meteors = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
# Spawn meteors
for i in range(10):
	spawn_meteor()
# Initialize score
score = 0

while running:
	if paused:
		show_pause_screen()
		paused = False
	if game_over:
		show_game_over_screen()
		game_over = False
		# Generate all characters
		all_sprites = pygame.sprite.Group()
		meteors = pygame.sprite.Group()
		enemies = pygame.sprite.Group()
		enemy_bullets = pygame.sprite.Group()
		player = Player()
		all_sprites.add(player)
		bullets = pygame.sprite.Group()
		powerups = pygame.sprite.Group()
		# Spawn meteors
		for i in range(10):
			spawn_meteor()
		# Initialize score
		score = 0

	# keep loop running at the right speed
	clock.tick(FPS)

	# Process input (events)
	for event in pygame.event.get():
		# check for closing window
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				paused = True

	# Update all Sprites
	all_sprites.update()

	# Possibly spawn enemy
	if random.random() < 0.005 and not enemies:
		spawn_enemy()

	# (All) Bullets / Meteors Collision
	hits = pygame.sprite.groupcollide(meteors, bullets, True, True)
	hits.update(pygame.sprite.groupcollide(meteors, enemy_bullets, True, True))
	for hit in hits:
		score += ( 100 - hit.radius ) / 2 + 1
 		random.choice(explosion_sounds).play()
 		explosion = Explosion('lg', hit.rect.center, hit.dx, hit.dy)
 		all_sprites.add(explosion)
 		if random.random() > 0.95:        
 			pow = Pow(hit.rect.center, hit.dx, hit.dy)
 			all_sprites.add(pow)
 			powerups.add(pow)
		spawn_meteor()

	# Bullets / Enemies Collision
	hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
	for hit in hits:
		score += 1000
 		random.choice(explosion_sounds).play()
 		explosion = Explosion('lg', hit.rect.center, hit.dx, hit.dy)
 		all_sprites.add(explosion)

	# Player / Meteors Collision
	hits = pygame.sprite.spritecollide(player, meteors, True, pygame.sprite.collide_circle)
	for hit in hits:
 		explosion = Explosion('sm', hit.rect.center, 0, 0)
 		all_sprites.add(explosion)
		hurt_sound.play()
 		player.shield -= hit.radius
		player.power = max(1, player.power - 1)
		spawn_meteor()
		if player.shield <= 0:
			death_explosion = Explosion('death', player.rect.center, 0, 0)
			death_sound.play()
			all_sprites.add(death_explosion)
			player.hide()
			player.lives -= 1
			player.shield = 100
			player.ammo = player.max_ammo
			player.power = 1

	# Player / EnemyBullets Collision
	hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
	for hit in hits:
 		explosion = Explosion('sm', hit.rect.center, 0, 0)
 		all_sprites.add(explosion)
		hurt_sound.play()
 		player.shield -= 20
		player.power = max(1, player.power - 1)
		if player.shield <= 0:
			death_explosion = Explosion('death', player.rect.center, 0, 0)
			death_sound.play()
			all_sprites.add(death_explosion)
			player.hide()
			player.lives -= 1
			player.shield = 100
			player.ammo = player.max_ammo
			player.power = 1

	# (All) Bullets / Powerups Collision
	hits = pygame.sprite.groupcollide(bullets, powerups, True, True)
	hits.update(pygame.sprite.groupcollide(enemy_bullets, powerups, True, True))
	for hit in hits:
		hit.kill()
	
	# Player / Powerups Collision
	hits = pygame.sprite.spritecollide(player, powerups, True)
	for hit in hits:
		score += 500
		powerup_sound.play()
		if hit.type == 'shield':
			player.shield = min(player.shield + 20, 100)
		if hit.type == 'gun':
			player.powerup()
	
	# if player dies and explosion has finished
	if player.lives == 0 and not death_explosion.alive():
		game_over = True

	# Draw / render
	screen.fill(BLACK)
	screen.blit(background, background_rect)
	all_sprites.draw(screen)
	draw_text(screen, str(score), 18, WIDTH / 2, 10)
	draw_shield_bar(screen, 5, 7, player.shield)
	draw_ammo_bar(screen, 5, 35, player.ammo)
	# draw_text(screen, "Power: {}".format(str(player.power)), 12, 35, 30)
	draw_lives(screen, WIDTH - 30, 5, player.lives, player_mini_img )
	# *after* drawing everything, flip the display
	pygame.display.flip()

pygame.quit()