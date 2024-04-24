import pygame
import math
import random

# Screen setup
RATIO = 60
WIDTH, HEIGHT = 16 * RATIO, 9 * RATIO
FPS = 60

# COLORS
SAGE   = (181, 193, 142)
BEIGE  = (247, 220, 185)
BROWN  = (222, 172, 128)
RED = (255, 0, 0)

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TURRET")
clock  = pygame.time.Clock()
running = True

# Turret setup
cannonAngle = 90
cannonWidth = int(RATIO / 3)
cannonLength = int(RATIO * 2)
cannonX, cannonY = int(WIDTH / 2), int(HEIGHT * .9) - 1

# Game parameters
LoadTime = 1 # second
gravity = RATIO / 10
bulletSpeed = RATIO / 10
COOLDOWN = 60
bulletCounter = 0

# State variables
isPressed = False
coolDown = 0
hitTarget = 0

# Power setup
power = 0
power_max = RATIO / 6
fullPower = power_max / (LoadTime * FPS) 

bullets, targets = [], []

class Target:
	def __init__(self, pos):
		self.x = pos[0]
		self.y = pos[1]
		self.size = cannonWidth

		targets.append(self)

class Bullet:
	def __init__(self, pos, angle, power):
		self.power = power
		self.angle = angle
		self.speed = bulletSpeed
		self.size = cannonWidth
		self.x = pos[0]
		self.y = pos[1]
		self.speed_x = math.cos(math.radians(self.angle)) * self.power
		self.speed_y = math.sin(math.radians(self.angle)) * self.power
		# self.vel_x =
		self.vel_y = -gravity / FPS # pixel / s²
		bullets.append(self)

	def update(self):
		self.speed_y += self.vel_y

		self.x -= self.speed_x
		self.y -= self.speed_y

		# Detect Collusion
		leftTop     = [self.x, self.y]
		rightTop    = [self.x + self.size, self.y]
		leftBottom  = [self.x, self.y + self.size]
		rightBottom = [self.x + self.size, self.y + self.size]

		for target in targets:
			tLeftTop     = [target.x, target.y]
			tRightBottom = [target.x + target.size, target.y + target.size]

			if ((leftTop[0] < tRightBottom[0] and leftTop[1] < tRightBottom[1]) and (leftTop[0] > tLeftTop[0] and leftTop[1] > tLeftTop[1])) or ((rightTop[0] < tRightBottom[0] and rightTop[1] < tRightBottom[1]) and (rightTop[0] > tLeftTop[0] and rightTop[1] > tLeftTop[1])) or ((leftBottom[0] < tRightBottom[0] and leftBottom[1] < tRightBottom[1]) and (leftBottom[0] > tLeftTop[0] and leftBottom[1] > tLeftTop[1])) or ((rightBottom[0] < tRightBottom[0] and rightBottom[1] < tRightBottom[1]) and (rightBottom[0] > tLeftTop[0] and rightBottom[1] > tLeftTop[1])):
				global hitTarget

				targets.remove(target)
				bullets.remove(self)

				hitTarget += 1

		# Remove Bullet
		if self.x < 0 or self.x > WIDTH or self.y > HEIGHT * .9:
			bullets.remove(self)

def cannonPos(angle):
	x = int(math.cos(math.radians(angle)) * cannonLength)
	y = int(math.sin(math.radians(angle)) * cannonLength)

	return [cannonX - x, cannonY - y]


Mouse_x, Mouse_y = pygame.mouse.get_pos()

while running:
	screen.fill(BEIGE)

	# Target
	if len(targets) == 0:
		Target([random.randint(0, WIDTH), random.randint(0, HEIGHT * .7)])

	for target in targets:
		pygame.draw.rect(screen, RED, pygame.Rect(target.x, target.y, target.size, target.size))
	
	# Bullets
	if coolDown > 0:
		coolDown -= 1

	if isPressed == True and pygame.mouse.get_pressed()[0] == False and power > power_max * .1:
		if coolDown == 0:	
			isPressed = False
			Bullet(cannonPos(cannonAngle), cannonAngle, power)
			coolDown = COOLDOWN
			bulletCounter += 1
		power = 0

	for bullet in bullets:
		bullet.update()
		pygame.draw.rect(screen, SAGE, pygame.Rect(bullet.x, bullet.y, bullet.size, bullet.size))
	

	# TURRET
	pygame.draw.circle(screen, BROWN, [cannonX, cannonY + 1], 50)	
	pygame.draw.line(screen, BROWN, [cannonX, cannonY], cannonPos(cannonAngle), width=cannonWidth)

	# MENU
	pygame.draw.rect(screen, BROWN, pygame.Rect(0, int(HEIGHT * .9), WIDTH, int(HEIGHT * .1)))
	
	# CoolDown
	pygame.draw.rect(screen, BEIGE, pygame.Rect(int(WIDTH * .1), int(HEIGHT * .92), int(WIDTH * .1), int(HEIGHT * .06)))
	pygame.draw.rect(screen, SAGE, pygame.Rect(int(WIDTH * .1), int(HEIGHT * .92), int(coolDown * WIDTH * .1 / COOLDOWN), int(HEIGHT * .06)))

	# Angle
	font = pygame.font.Font('PixelifySans-VariableFont_wght.ttf', 24)
	text = font.render('Cannon Angle: ' + str(round(cannonAngle, 2)), True, BEIGE)
	screen.blit(text, [WIDTH * .22, HEIGHT * .92])

	# Power
	pygame.draw.rect(screen, BEIGE, pygame.Rect(int(WIDTH - WIDTH * .4), int(HEIGHT * .92), int(WIDTH * .1), int(HEIGHT * .06)))
	pygame.draw.rect(screen, SAGE, pygame.Rect(int(WIDTH - WIDTH * .4), int(HEIGHT * .92), int(WIDTH * .1 * power / power_max), int(HEIGHT * .06)))

	# Bullet Counter
	text = font.render('Bullets: ' + str(hitTarget) + "/" + str(bulletCounter), True, BEIGE)
	screen.blit(text, [WIDTH - WIDTH * .28, HEIGHT * .92])

	pygame.display.flip()

	clock.tick(FPS)

	# INPUT HANDLING
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT or event.key == pygame.K_a:
				cannonAngle -= 1
			if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				cannonAngle += 1

	if pygame.mouse.get_pressed()[0]:
		isPressed = True
		if power < power_max:
			power += fullPower

	if pygame.mouse.get_pressed()[2]:
		isPressed = False
		power = 0
		
	if (Mouse_x, Mouse_y) != pygame.mouse.get_pos():
		Mouse_x, Mouse_y = pygame.mouse.get_pos()

		# IF on the menu
		if Mouse_y < cannonY:
			x, y = Mouse_x - cannonX, Mouse_y - cannonY

			if x < 0:
				cannonAngle = math.degrees(math.atan(y / x))
			elif x > 0:
				cannonAngle = math.degrees(math.atan(y / x)) + 180

pygame.quit()