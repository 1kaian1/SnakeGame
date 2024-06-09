import pygame
import random
import pickle
from pygame import mixer

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

# define screen parameters
screen_width = 1300
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake by BrinyFlyer28795')
pygame.display.set_icon(pygame.image.load("SP-materials/snake0.png"))

# define fonts
font_ari_na200 = pygame.font.SysFont("arial narrow", 200)
font_ari_na40 = pygame.font.SysFont("arial narrow", 40)

# define game variables
delete_progress = False
main_menu = True
tile_size = 50
game_over = 0

# define colours
white_col = (255, 255, 255)
aqua_col = (0, 255, 255)
black_col = (0, 0, 0)

# load images
all_levels_completed_img = pygame.image.load("SP-materials/all-levels-completed.png")
progress_deleted_img = pygame.image.load("SP-materials/progress-deleted.png")
level_completed_img = pygame.image.load("SP-materials/level-completed.png")
reset_game_data_img = pygame.image.load("SP-materials/reset-game-data.png")
golden_apple_img = pygame.image.load("SP-materials/golden-apple.png")
rotten_apple_img = pygame.image.load("SP-materials/rotten-apple.png")
background_img = pygame.image.load("SP-materials/background.png")
game_over_img = pygame.image.load("SP-materials/game-over.png")
music_off_img = pygame.image.load("SP-materials/music-off.png")
sound_off_img = pygame.image.load("SP-materials/sound-off.png")
music_on_img = pygame.image.load("SP-materials/music-on.png")
sound_on_img = pygame.image.load("SP-materials/sound-on.png")
replay_img = pygame.image.load("SP-materials/replay.png")
start_img = pygame.image.load("SP-materials/start.png")
reset_img = pygame.image.load("SP-materials/reset.png")
grass_img = pygame.image.load("SP-materials/grass.png")
apple_img = pygame.image.load("SP-materials/apple.png")
exit_img = pygame.image.load("SP-materials/exit.png")
menu_img = pygame.image.load("SP-materials/menu.png")
next_img = pygame.image.load("SP-materials/next.png")
wall_img = pygame.image.load("SP-materials/wall.png")
yes_img = pygame.image.load("SP-materials/yes.png")
no_img = pygame.image.load("SP-materials/no.png")

# transform images
golden_apple_img = pygame.transform.scale(golden_apple_img, (tile_size, tile_size))
rotten_apple_img = pygame.transform.scale(rotten_apple_img, (tile_size, tile_size))
music_off_img = pygame.transform.scale(music_off_img, (tile_size, tile_size))
sound_off_img = pygame.transform.scale(sound_off_img, (tile_size, tile_size))
music_on_img = pygame.transform.scale(music_on_img, (tile_size, tile_size))
sound_on_img = pygame.transform.scale(sound_on_img, (tile_size, tile_size))
grass_img = pygame.transform.scale(grass_img, (tile_size, tile_size))
apple_img = pygame.transform.scale(apple_img, (tile_size, tile_size))
wall_img = pygame.transform.scale(wall_img, (tile_size, tile_size))

# load sounds
congratulations_fx = pygame.mixer.Sound("SP-materials/congratulations.wav")
main_music_fx = pygame.mixer.Sound("SP-materials/main_music.wav")
game_over_fx = pygame.mixer.Sound("SP-materials/game_over.wav")
penalty_fx = pygame.mixer.Sound("SP-materials/penalty.wav")
collect_fx = pygame.mixer.Sound("SP-materials/collect.wav")
bonus_fx = pygame.mixer.Sound("SP-materials/bonus.wav")

def volume(a):
	if a == 1:
		main_music_fx.set_volume(0.2)
	elif a == -1:
		main_music_fx.set_volume(0)
	elif a == 2:
		congratulations_fx.set_volume(0.2)
		game_over_fx.set_volume(0.5)
		penalty_fx.set_volume(0.2)
		collect_fx.set_volume(0.5)
		bonus_fx.set_volume(1)
	elif a == -2:
		congratulations_fx.set_volume(0)
		game_over_fx.set_volume(0)
		penalty_fx.set_volume(0)
		collect_fx.set_volume(0)
		bonus_fx.set_volume(0)

def record_level(level):
	level += 1

	pickle_in = open(f'SP-materials/levels_data', 'rb')
	levels = pickle.load(pickle_in)
	levels[0][0] = level

	pickle_out = open(f'SP-materials/levels_data', 'wb')
	pickle.dump(levels, pickle_out)
	pickle_out.close()

	return reset_level(level)

def reset_level(level):
	pickle_in = open(f"SP-materials/levels_data", "rb")
	levels = pickle.load(pickle_in)
	world_data, lenght_required, speed, start_pos_x, start_pos_y, direction, special_food = levels[level]
	world = World(world_data)

	snake = Snake(start_pos_x, start_pos_y, lenght_required, special_food, direction)
	snake.reset(start_pos_x, start_pos_y, lenght_required, special_food, direction)

	return world, speed, level, snake, direction

class Sprite:
	print("sprite")
	def __init__(self, x, y, image, center=False):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		if center == True:
			self.rect.center = (x, y)

	def draw(self):
		screen.blit(self.image, self.rect)

class Button(Sprite):
	def __init__(self, x, y, image):
		super().__init__(x, y, image, True)

	def draw(self):
		action = False
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				action = True

		super().draw()

		return action

class Text(Sprite):
	def __init__(self, text, font, text_col, x, y, delay, fill_black):
		img = font.render(text, True, text_col)
		super().__init__(x, y, img)
		self.fill_black = fill_black
		self.text_col = text_col
		self.delay = delay
		self.text = text
		self.font = font
		self.x = x
		self.y = y

	def draw(self):
		if self.fill_black == True:
			screen.fill(black_col)

		super().draw()

		pygame.display.update()
		pygame.time.wait(self.delay)

class World():
	def __init__(self, data):
		self.tile_list = []
		self.obstacles = []
		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				x = col_count * tile_size
				y = row_count * tile_size
				if tile == 1:
					tile = (x, y, grass_img)
				if tile == 2:
					tile = (x, y, wall_img)
					self.obstacles.append((x, y))
				self.tile_list.append(tile)
				col_count += 1
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			Sprite(tile[0], tile[1], tile[2]).draw()

		return self.obstacles

class Snake():
	def __init__(self, x, y, lenght_required, special_food, direction):
		self.reset(x, y, lenght_required, special_food, direction)

	def update(self, direction, game_over, obstacles):

		# x and y update
		if direction == 2: self.y -= 50
		if direction == 0: self.y += 50
		if direction == -1: self.x -= 50
		if direction == 1: self.x += 50

		# make endless world
		if self.x == -50: self.x = 1250
		if self.x == 1300: self.x = 0
		if self.y == -50: self.y = 850
		if self.y == 900: self.y = 0

		# paths update
		self.path_x.append(self.x)
		self.path_y.append(self.y)
		self.direction_path.append(direction)

		game_over = self.check_collision(game_over)

		if game_over == 0:

			if (self.x == self.food_x and self.y == self.food_y) or (self.food_x is None and self.food_y is None):
				self.food_x, self.food_y = self.new_food(obstacles)
				Sprite(self.food_x, self.food_y, apple_img).draw()

			if self.sp_f[0][0] != None and self.sp_f[1][0] != None:
				self.new_special_food(obstacles)

		# overwrite old score
		for a in range(0, 800, 50):
			img = grass_img
			if (a, 850) in obstacles:
				img = wall_img
			Sprite(a, 850, img).draw()

		if game_over == 0:
			self.snake_animation()

		self.score()

		return game_over, self.snake_lenght, direction

	def check_collision(self, game_over):

		# check for collision with walls
		for obstacle in obstacles:
			if obstacle == (self.x, self.y):
				main_music_fx.stop(), game_over_fx.play()
				game_over = -1
				break

		# check for collision with own body
		for e in range(2, self.snake_lenght+1):
			if self.path_x[-e] == self.x and self.path_y[-e] == self.y:
				main_music_fx.stop(), game_over_fx.play()
				game_over = -1
				break

		# check for collision with food
		if self.x == self.food_x and self.y == self.food_y:
			self.lenght_add_counter += 1
			collect_fx.play()
		elif self.x == self.sp_f_x and self.y == self.sp_f_y:
			self.lenght_add_counter += self.sp_f[self.sp_f_type][2]
			if self.sp_f_type == 0 and self.snake_lenght != self.lenght_required-1:
				bonus_fx.play()
			elif self.sp_f_type == 1:
				penalty_fx.play()

		# gradually changes length
		if self.lenght_add_counter > 0:
			self.snake_lenght += 1
			self.lenght_add_counter -= 1
		elif self.lenght_add_counter < 0:
			if self.snake_lenght != 2:
				self.snake_lenght -= 1
			self.lenght_add_counter += 1

			# draw grass on the extra tail
			Sprite(self.path_x[-self.snake_lenght - 2], self.path_y[-self.snake_lenght - 2], grass_img).draw()

		# check if snake reached the required length
		if self.snake_lenght == self.lenght_required:
			main_music_fx.stop(), congratulations_fx.play()
			game_over = 1

		return game_over

	def new_food(self, obstacles):
		loop = True
		while loop:
			x = random.randrange(0, 1250, 50)
			y = random.randrange(0, 850, 50)
			loop = False
			len = self.snake_lenght
			while len > 0:
				if self.path_x[-len] == x and self.path_y[-len] == y:
					loop = True
					break
				len -= 1
			for obstacle in obstacles:
				if obstacle == (x, y):
					loop = True
					break
			if self.sp_f_x == x and self.sp_f_y == y:
				loop = True

		return x, y

	def new_special_food(self, obstacles):
		if (self.x == self.sp_f_x and self.y == self.sp_f_y) or (self.sp_f_x is None and self.sp_f_y is None) or self.sp_f_wait_counter != 0:
			if self.sp_f_interval_counter == self.sp_f[self.sp_f_type][0]:
				if self.sp_f_wait_counter == self.sp_f[self.sp_f_type][1] or (self.x == self.sp_f_x and self.y == self.sp_f_y):
					Sprite(self.sp_f_x, self.sp_f_y, grass_img).draw()
					# reset special food variables
					self.sp_f_x = None
					self.sp_f_y = None
					self.sp_f_type = random.randint(0, 1)
					self.sp_f_interval_counter = 0
					self.sp_f_wait_counter = 0
				else:
					if self.sp_f_x == None and self.sp_f_y == None:
						self.sp_f_x, self.sp_f_y = self.new_food(obstacles)

					# draw special food onto screen
					img = golden_apple_img
					if self.sp_f_type == 1:
						img = rotten_apple_img
					Sprite(self.sp_f_x, self.sp_f_y, img).draw()

					self.sp_f_wait_counter += 1
			else:
				self.sp_f_interval_counter += 1

	def snake_animation(self):

		# draw grass on the end of snake
		Sprite(self.path_x[-self.snake_lenght - 1], self.path_y[-self.snake_lenght - 1], grass_img).draw()

		# snake animation
		for num in range(1, self.snake_lenght+1):

			# snake's head
			if num == 1:

				# draw grass onto screen, before head is drawn
				Sprite(self.path_x[-1], self.path_y[-1], grass_img).draw()

				self.image = self.snake_images[0][self.direction_path[-1]]

			# snake's tail
			elif num == self.snake_lenght:

				# draw grass onto screen, before tail is drawn
				Sprite(self.path_x[-self.snake_lenght], self.path_y[-self.snake_lenght], grass_img).draw()

				a = self.direction_path[-self.snake_lenght]
				b = self.direction_path[-self.snake_lenght + 1]
				variations = [(2, 1), (1, 2), (1, 0), (0, 1), (0, -1), (-1, 0), (-1, 2), (2, -1)]
				if (a, b) in variations:
					d = 5
					c = variations.index((a, b))
					if c == 0 or c == 2 or c == 4 or c == 6:
						d = 6
					self.image = self.snake_images[d][self.direction_path[-self.snake_lenght]]
				else:
					variations = [(2, 0), (0, 2), (-1, 1), (1, -1)]
					if (a, b) in variations:
						self.image = self.snake_images[4][b]
					else:
						self.image = self.snake_images[4][self.direction_path[-self.snake_lenght]]

			# snake's body
			else:

				# draw grass onto screen, before body is drawn
				Sprite(self.path_x[-num], self.path_y[-num], grass_img).draw()

				a = self.direction_path[-num]
				b = self.direction_path[-num + 1]
				d = 1
				variations = [(2, 1), (1, 2), (1, 0), (0, 1), (0, -1), (-1, 0), (-1, 2), (2, -1)]
				if (a, b) in variations:
					d = 2
					c = variations.index((a, b))
					if c == 0 or c == 2 or c == 4 or c == 6:
						d = 3
				self.image = self.snake_images[d][self.direction_path[-num]]

			# draw snake onto screen
			x = self.path_x[-num]
			y = self.path_y[-num]
			Sprite(x, y, self.image).draw()

	def score(self):
		if self.sp_f[0][0] != None and self.sp_f[1][0] != None:
			Text("score: " + str(self.snake_lenght) + "  score needed: " + str(self.lenght_required)
				+ "  bonus: +" + str(self.sp_f[0][2]) + "  penalty: " + str(self.sp_f[1][2]), font_ari_na40, black_col, 15, 860, 0, False).draw()
		else:
			Text("score: " + str(self.snake_lenght) + "  score needed: " + str(self.lenght_required), font_ari_na40, black_col, 15, 860, 0, False).draw()

	def reset(self, x, y, lenght_required, special_food, direction):

		# basic game variables
		self.x = x
		self.y = y
		self.food_x = None
		self.food_y = None
		self.lenght_add_counter = 0
		self.path_x = [self.x]
		self.path_y = [self.y]
		if direction == 2: self.y += 50
		elif direction == 0: self.y -= 50
		elif direction == -1: self.x += 50
		elif direction == 1: self.x -= 50
		self.path_x.append(self.x)
		self.path_y.append(self.y)
		self.direction_path = [direction, direction]
		self.snake_lenght = 2
		self.lenght_required = lenght_required

		# animations variables
		self.snake_images = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
		for num in range(0, 7):
			img_up = pygame.image.load(f"SP-materials/snake{num}.png")
			img_up = pygame.transform.scale(img_up, (tile_size, tile_size))
			img_left = pygame.transform.rotate(img_up, 90)
			img_right = pygame.transform.rotate(img_up, -90)
			img_down = pygame.transform.rotate(img_up, 180)
			self.snake_images[num][2] = img_up
			self.snake_images[num][0] = img_down
			self.snake_images[num][-1] = img_left
			self.snake_images[num][1] = img_right

		# special food variables
		self.sp_f = special_food
		self.sp_f_x = None
		self.sp_f_y = None
		self.sp_f_type = random.randint(0, 1)
		self.sp_f_interval_counter = 0
		self.sp_f_wait_counter = 0

# create buttons
replay_button = Button(screen_width // 2 - 225, screen_height // 2 - 50, replay_img)
reset_button = Button(screen_width // 2 - 225, screen_height // 2 + 50, reset_img)
start_button = Button(screen_width // 2 - 225, screen_height // 2 - 250, start_img)
next_button = Button(screen_width // 2 - 225, screen_height // 2 - 200, next_img)
exit_button = Button(screen_width // 2 - 225, screen_height // 2 - 100, exit_img)
menu_button = Button(screen_width // 2 - 225, screen_height // 2 + 100, menu_img)
yes_button = Button(screen_width // 2 - 225, screen_height // 2 - 50, yes_img)
no_button = Button(screen_width // 2 - 225, screen_height // 2 + 100, no_img)
music_off_button = Button(1180, 840, music_off_img)
music_on_button = Button(1180, 840, music_on_img)
sound_off_button = Button(1240, 840, sound_off_img)
sound_on_button = Button(1240, 840, sound_on_img)

# get actual level and number of levels
pickle_in = open(f'SP-materials/levels_data', 'rb')
levels = pickle.load(pickle_in)
level, max_level = levels[0][0], levels[0][1]

# set actual level
world, speed, level, snake, direction = reset_level(level)

# set music and sounds data
pickle_in = open(f'SP-materials/levels_data', 'rb')
levels = pickle.load(pickle_in)
music, sounds = levels[0][2], levels[0][3]

run = True
while run:

	clock.tick(fps)

	# event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			if (event.key == pygame.K_w or event.key == pygame.K_UP) and (snake_lenght == 2 or direction != 0):
				direction = 2
			elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and (snake_lenght == 2 or direction != 2):
				direction = 0
			elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and (snake_lenght == 2 or direction != 1):
				direction = -1
			elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and (snake_lenght == 2 or direction != -1):
				direction = 1

	if main_menu == True:

		fps = 60
		Sprite(0, 0, background_img).draw()

		if exit_button.draw():
			run = False
		elif reset_button.draw():
			pygame.time.wait(100)
			delete_progress = True
			main_menu = False
		if music == True:
			volume(1)
			if music_on_button.draw():
				pygame.time.wait(100)
				volume(-1)
				music = False
		else:
			volume(-1)
			if music_off_button.draw():
				pygame.time.wait(100)
				volume(1)
				music = True
		if sounds == True:
			volume(2)
			if sound_on_button.draw():
				pygame.time.wait(100)
				volume(-2)
				sounds = False
		else:
			volume(-2)
			if sound_off_button.draw():
				pygame.time.wait(100)
				volume(2)
				sounds = True
		if start_button.draw():
			main_music_fx.play(-1, 0, 2000)
			Text("Level " + str(level), font_ari_na200, aqua_col, screen_width // 2 - 250, screen_height // 2 - 50, 1500, True).draw()
			obstacles = world.draw()
			main_menu = False
			game_over = 0

	# if reset button pressed
	elif delete_progress == True:

		screen.fill(black_col)
		Sprite(150, 200, reset_game_data_img).draw()

		if yes_button.draw():
			pygame.time.wait(100)
			world, speed, level, snake, direction = record_level(0)
			screen.fill(black_col)
			Sprite(150, 400, progress_deleted_img).draw()
			pygame.display.update()
			pygame.time.wait(1500)
			delete_progress = False
			main_menu, music, sounds = True, True, True
		elif no_button.draw():
			delete_progress = False
			main_menu = True

	else:

		# if player live
		if game_over == 0:
			fps = speed
			game_over, snake_lenght, direction = snake.update(direction, game_over, obstacles)

		# if player has died
		if game_over == -1:
			fps = 60
			screen.blit(game_over_img, (350, 200))

			if menu_button.draw():
				pygame.time.wait(100)
				world, speed, level, snake, direction = reset_level(level)
				main_menu = True
			elif replay_button.draw():
				main_music_fx.play(-1, 0, 2000)
				Text("Level " + str(level), font_ari_na200, aqua_col, screen_width // 2 - 250, screen_height // 2 - 50,1500, True).draw()
				world, speed, level, snake, direction = reset_level(level)
				obstacles = world.draw()
				game_over = 0

		# if player has completed the level
		if game_over == 1:
			fps = 60

			if level < max_level:
				screen.blit(level_completed_img, (150, 100))

				if menu_button.draw():
					pygame.time.wait(100)
					world, speed, level, snake, direction = record_level(level)
					main_menu = True
				elif replay_button.draw():
					main_music_fx.play(-1, 0, 2000)
					world, speed, level, snake, direction = reset_level(level)
					Text("Level " + str(level), font_ari_na200, aqua_col, screen_width // 2 - 250, screen_height // 2 - 50, 1500, True).draw()
					obstacles = world.draw()
					game_over = 0
				elif next_button.draw():
					main_music_fx.play(-1, 0, 2000)
					world, speed, level, snake, direction = record_level(level)
					Text("Level " + str(level), font_ari_na200, aqua_col, screen_width // 2 - 250, screen_height // 2 - 50, 1500, True).draw()
					obstacles = world.draw()
					game_over = 0

			else:
				screen.blit(all_levels_completed_img, (305, 100))

				if menu_button.draw():
					pygame.time.wait(100)
					world, speed, level, snake, direction = reset_level(level)
					main_menu = True
				elif replay_button.draw():
					main_music_fx.play(-1, 0, 2000)
					world, speed, level, snake, direction = reset_level(level)
					Text("Level " + str(level), font_ari_na200, aqua_col, screen_width // 2 - 250, screen_height // 2 - 50, 1500, True).draw()
					obstacles = world.draw()
					game_over = 0

	pygame.display.update()

# overwrite music and sounds data
pickle_in = open(f'SP-materials/levels_data', 'rb')
levels = pickle.load(pickle_in)
levels[0][2], levels[0][3] = music, sounds

pickle_out = open(f'SP-materials/levels_data', 'wb')
pickle.dump(levels, pickle_out)
pickle_out.close()

pygame.quit()