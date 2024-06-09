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
obstacles = []
clicked = False

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
            Sprite((tile[0], tile[1]), tile[2]).draw()

        return self.obstacles

class Snake():
    def __init__(self, x, y, lenght_required, special_food, direction):
        self.reset(x, y, lenght_required, special_food, direction)

    def update(self, direction, game_over, obstacles):

        # x and y update
        if direction == 2: self.pos[1] -= 50
        if direction == 0: self.pos[1] += 50
        if direction == -1: self.pos[0] -= 50
        if direction == 1: self.pos[0] += 50

        # make endless world
        if self.pos[0] == -50: self.pos[0] = 1250
        if self.pos[0] == 1300: self.pos[0] = 0
        if self.pos[1] == -50: self.pos[1] = 850
        if self.pos[1] == 900: self.pos[1] = 0

        game_over = self.check_game_over(game_over, direction)

        if game_over == 0:

            if self.pos == self.food or self.food == [None, None]:
                self.food = self.new_food(obstacles)
                Sprite(self.food, apple_img).draw()

            if self.spf[0][0] != None and self.spf[1][0] != None:
                self.new_special_food(obstacles)

        # overwrite old score
        for a in range(0, 800, 50):
            img = grass_img
            if (a, 850) in obstacles:
                img = wall_img
            Sprite((a, 850), img).draw()

        if game_over == 0:
            self.snake_animation()

        self.score()

        return game_over, self.snake_lenght, direction

    def check_game_over(self, game_over, direction):
        # check for collision with walls
        for obstacle in obstacles:
            if list(obstacle) == self.pos:
                main_music_fx.stop(), game_over_fx.play()
                game_over = -1
                break

        # check for collision with food
        if self.pos == self.food:
            self.lenght_add_counter += 1
            collect_fx.play()
        elif self.pos == self.spf_pos:
            self.lenght_add_counter += self.spf[self.spf_type][2]
            if self.spf_type == 0 and self.snake_lenght != self.lenght_required - 1:
                bonus_fx.play()
            elif self.spf_type == 1:
                penalty_fx.play()

        # gradually changes length
        if self.lenght_add_counter > 0:
            self.snake_lenght += 1
            self.path.append(list(self.pos))
            self.moves.append(direction)
            self.lenght_add_counter -= 1
        elif self.lenght_add_counter < 0:
            if self.snake_lenght != 2:
                self.snake_lenght -= 1
                self.path.remove(self.path[2])
                self.moves.remove(self.moves[2])
            self.lenght_add_counter += 1
        else:
            for a in range(1, self.snake_lenght):
                self.path[a - 1] = self.path[a]
                self.moves[a - 1] = self.moves[a]
            self.path[-1] = list(self.pos)
            self.moves[-1] = direction

        # check for collision with own body
        for a in range(0, self.snake_lenght-4):
            if self.pos == self.path[a]:
                main_music_fx.stop(), game_over_fx.play()
                game_over = -1
                break

        # check if snake reached the required length
        if self.snake_lenght == self.lenght_required:
            main_music_fx.stop(), congratulations_fx.play()
            game_over = 1

        return game_over

    def new_food(self, obstacles):
        loop = True
        while loop:
            a = random.randrange(0, 1250, 50)
            b = random.randrange(0, 850, 50)
            loop = False
            len = self.snake_lenght
            while len > 0:
                if self.path[-len] == (a, b):
                    loop = True
                    break
                len -= 1
            for obstacle in obstacles:
                if obstacle == (a, b):
                    loop = True
                    break
            if self.spf_pos == (a, b):
                loop = True

        return [a, b]

    def new_special_food(self, obstacles):
        if self.pos == self.spf_pos or self.spf_pos == [None, None] or self.wait_counter != 0:
            if self.interval_counter == self.spf[self.spf_type][0]:
                if self.wait_counter == self.spf[self.spf_type][1] or self.pos == self.spf_pos:
                    Sprite(self.spf_pos, grass_img).draw()
                    # reset special food variables
                    self.spf_pos = [None, None]
                    self.spf_type = random.randint(0, 1)
                    self.interval_counter = 0
                    self.wait_counter = 0
                else:
                    if self.spf_pos == [None, None]:
                        self.spf_pos = self.new_food(obstacles)

                    # draw special food onto screen
                    img = golden_apple_img
                    if self.spf_type == 1:
                        img = rotten_apple_img
                    Sprite(self.spf_pos, img).draw()

                    self.wait_counter += 1
            else:
                self.interval_counter += 1

    def snake_animation(self):

        """ snake's head """

        # draw grass onto screen, before head is drawn
        Sprite(self.path[-1], grass_img).draw()

        # head image
        self.image = self.snake_images[0][self.moves[-1]]

        # draw head
        Sprite(self.path[-1], self.image).draw()

        """ snake's tail """

        # draw grass onto screen, before tail is drawn
        Sprite(self.path[0], grass_img).draw()

        # tail image
        a = self.moves[-self.snake_lenght]
        b = self.moves[-self.snake_lenght + 1]
        variations = [(2, 1), (1, 2), (1, 0), (0, 1), (0, -1), (-1, 0), (-1, 2), (2, -1)]
        if (a, b) in variations:
            d = 5
            c = variations.index((a, b))
            if c == 0 or c == 2 or c == 4 or c == 6:
                d = 6
            self.image = self.snake_images[d][self.moves[-self.snake_lenght]]
        else:
            variations = [(2, 0), (0, 2), (-1, 1), (1, -1)]
            if (a, b) in variations:
                self.image = self.snake_images[4][b]
            else:
                self.image = self.snake_images[4][self.moves[-self.snake_lenght]]

        # draw tail
        Sprite(self.path[0], self.image).draw()

        """ snake's body """

        # draw grass onto screen, before body is drawn
        Sprite(self.path[-2], grass_img).draw()

        # body image
        a = self.moves[-2]
        b = self.moves[-2 + 1]
        d = 1
        variations = [(2, 1), (1, 2), (1, 0), (0, 1), (0, -1), (-1, 0), (-1, 2), (2, -1)]
        if (a, b) in variations:
            d = 2
            c = variations.index((a, b))
            if c == 0 or c == 2 or c == 4 or c == 6:
                d = 3
        self.image = self.snake_images[d][self.moves[-2]]

        # draw body
        Sprite(self.path[-2], self.image).draw()

    def score(self):
        if self.spf[0][0] != None and self.spf[1][0] != None:
            Text("score: " + str(self.snake_lenght) + "  score needed: " + str(self.lenght_required)
                 + "  bonus: +" + str(self.spf[0][2]) + "  penalty: " + str(self.spf[1][2]), font_ari_na40, black_col,
                 15, 860, 0, False).draw()
        else:
            Text("score: " + str(self.snake_lenght) + "  score needed: " + str(self.lenght_required), font_ari_na40,
                 black_col, 15, 860, 0, False).draw()

    def reset(self, x, y, lenght_required, special_food, direction):

        # basic game variables
        self.pos = [x, y]
        self.food = [None, None]
        self.lenght_add_counter = 0
        self.path = [list(self.pos)]
        if direction == 2:
            self.pos[1] += 50
        elif direction == 0:
            self.pos[1] -= 50
        elif direction == -1:
            self.pos[0] += 50
        elif direction == 1:
            self.pos[0] -= 50
        self.path.append(list(self.pos))
        self.moves = [direction, direction]
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
        self.spf = special_food
        self.spf_pos = [None, None]
        self.spf_type = random.randint(0, 1)
        self.interval_counter = 0
        self.wait_counter = 0

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

def btn_vars(btn, world, speed, level, snake, direction, obstacles, game_over, main_menu, delete_progress, music, sounds, run):
    if btn == 0:
        volume(1)
        music = True
    elif btn == 1:
        volume(2)
        sounds = True
    elif btn == 2:
        volume(-1)
        music = False
    elif btn == 3:
        volume(-2)
        sounds = False
    elif btn == 4:
        main_music_fx.play(-1, 0, 2000)
        world, speed, level, snake, direction = reset_level(level)
        Text("Level " + str(level), font_ari_na200, aqua_col, screen_width // 2 - 250,
             screen_height // 2 - 50, 1500, True).draw()
        obstacles = world.draw()
        game_over = 0
    elif btn == 5:
        main_music_fx.play(-1, 0, 2000)
        Text("Level " + str(level), font_ari_na200, aqua_col, screen_width // 2 - 250, screen_height // 2 - 50,
             1500, True).draw()
        obstacles = world.draw()
        main_menu = False
        game_over = 0
    elif btn == 6:
        delete_progress = True
        main_menu = False
    elif btn == 7:
        run = False
    elif btn == 8:
        main_music_fx.play(-1, 0, 2000)
        world, speed, level, snake, direction = record_level(level)
        Text("Level " + str(level), font_ari_na200, aqua_col, screen_width // 2 - 250,
             screen_height // 2 - 50, 1500, True).draw()
        obstacles = world.draw()
        game_over = 0
    elif btn == 9:
        world, speed, level, snake, direction = record_level(level)
        main_menu = True
    elif btn == 10:
        world, speed, level, snake, direction = record_level(0)
        screen.fill(black_col)
        Sprite((150, 400), progress_deleted_img).draw()
        pygame.display.update()
        pygame.time.wait(1500)
        delete_progress = False
        main_menu, music, sounds = True, True, True
    elif btn == 11:
        delete_progress = False
        main_menu = True

    pygame.time.wait(100)

    return world, speed, level, snake, direction, obstacles, game_over, main_menu, delete_progress, music, sounds, run

class Sprite:
    def __init__(self, pos, image, center=False):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        if center == True:
            self.rect.center = (pos[0], pos[1])

    def draw(self):
        screen.blit(self.image, self.rect)

class Button(Sprite):
    def __init__(self, x, y, image):
        super().__init__((x, y), image, True)
        self.x = x
        self.y = y

    def draw(self):
        super().draw()

    def click(self, pos):
        if self.rect.collidepoint(pos):
            return True
        else:
            return False

class Text(Sprite):
    def __init__(self, text, font, text_col, x, y, delay, fill_black):
        img = font.render(text, True, text_col)
        super().__init__((x, y), img)
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

# create buttons
all_btns = [Button(1180, 840, music_off_img), Button(1240, 840, sound_off_img), Button(1180, 840, music_on_img),
        Button(1240, 840, sound_on_img), Button(650, 450, replay_img), Button(650, 320, start_img),
        Button(650, 580, reset_img), Button(650, 450, exit_img), Button(650, 320, next_img),
        Button(650, 580, menu_img), Button(650, 450, yes_img), Button(650, 580, no_img)]

mus_off_btn = all_btns[0]
sou_off_btn = all_btns[1]
mus_on_btn = all_btns[2]
sou_on_btn = all_btns[3]
replay_btn = all_btns[4]
start_btn = all_btns[5]
reset_btn = all_btns[6]
exit_btn = all_btns[7]
next_btn = all_btns[8]
menu_btn = all_btns[9]
yes_btn = all_btns[10]
no_btn = all_btns[11]

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
        if pygame.mouse.get_pressed()[0] == 1 and clicked == False:
            clicked = True
            pos = pygame.mouse.get_pos()
            for btn in btns:
                if btn.click(pos):
                    ind = all_btns.index(btn)
                    world, speed, level, snake, direction, obstacles, game_over, main_menu, delete_progress, music, \
                    sounds, run = btn_vars(ind, world, speed, level, snake, direction, obstacles, game_over,
                                           main_menu, delete_progress, music, sounds, run)
        else:
            clicked = False

    if main_menu == True:
        btns = [all_btns[5], all_btns[6], all_btns[7]]
        fps = 60
        Sprite((0, 0), background_img).draw()
        start_btn.draw()
        exit_btn.draw()
        reset_btn.draw()
        if music == True:
            btns.append(all_btns[2])
            volume(1)
            mus_on_btn.draw()
        else:
            btns.append(all_btns[0])
            volume(-1)
            mus_off_btn.draw()
        if sounds == True:
            btns.append(all_btns[3])
            volume(2)
            sou_on_btn.draw()
        else:
            btns.append(all_btns[1])
            volume(-2)
            sou_off_btn.draw()

    # if reset button pressed
    elif delete_progress == True:
        btns = [all_btns[10], all_btns[11]]
        screen.fill(black_col)
        Sprite((650, 200), reset_game_data_img, True).draw()
        yes_btn.draw()
        no_btn.draw()

    else:

        # if player live
        if game_over == 0:
            fps = speed
            game_over, snake_lenght, direction = snake.update(direction, game_over, obstacles)

        # if player has died
        if game_over == -1:
            btns = [all_btns[4], all_btns[9]]
            fps = 60
            Sprite((650, 200), game_over_img, True).draw()
            menu_btn.draw()
            replay_btn.draw()

        # if player has completed the level
        if game_over == 1:
            fps = 60

            if level < max_level:
                btns = [all_btns[8], all_btns[9], all_btns[4]]
                Sprite((650, 200), level_completed_img, True).draw()
                next_btn.draw()
                menu_btn.draw()
                replay_btn.draw()

            else:
                btns = [all_btns[9], all_btns[4]]
                Sprite((650, 200), all_levels_completed_img, True).draw()
                menu_btn.draw()
                replay_btn.draw()

    pygame.display.update()

# overwrite music and sounds data
pickle_in = open(f'SP-materials/levels_data', 'rb')
levels = pickle.load(pickle_in)
levels[0][2], levels[0][3] = music, sounds

pickle_out = open(f'SP-materials/levels_data', 'wb')
pickle.dump(levels, pickle_out)
pickle_out.close()

