import pygame, random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height + 40))
pygame.display.set_caption('Snake - advanced game')

#define game variables
main_menu = True


def calculate_new_food_position(path_x, path_y, lenght):
    again = True
    while again:
        print("Again")
        a = random.randrange(0, 1000, 50)
        b = random.randrange(0, 600, 50)
        again = False
        article = -lenght
        while article < 0:
            if path_x[article] == a and path_y[article] == b:
                again = True
                print("False a, b coordinates")
                break
            print("Re-check a, b coordinates")
            article += 1
    print("True a, b coordinates")
    return a, b


def hit_body_check(x, y, path_x, path_y, lenght):
    article = -lenght
    while article < -1:
        print("Snake article hit check")
        if (path_x[article] == x) and (path_y[article] == y):
            print("True hit")
            return True
        article += 1
    print("False hit")
    return False


def end_of_game(lenght, lenght_required, level):
    if lenght == lenght_required:
        t_level_completed = pygame.font.SysFont("arial narrow", 120).render("Level " + str(level) + " completed!", True, (0, 255, 0))
        screen.blit(t_level_completed, (500 - t_level_completed.get_width() // 2, 300 - t_level_completed.get_height() // 2))

        print("-----------------------------------------------------\nLevel", level, "completed\n-----------------------------------------------------")

        level += 1

        pygame.display.flip()
        pygame.time.wait(3000)

        screen.fill((0, 0, 0))
        pygame.display.flip()

        f = open("Snake-game-data.abc", "w")
        f.write(str(level))
        f.close()

        return levels(level)

    else:
        t_gameover = pygame.font.SysFont("arial narrow", 120).render("GAME OVER!", True, (200, 0, 0))
        screen.blit(t_gameover, (500 - t_gameover.get_width() // 2, 200 - t_gameover.get_height() // 2))

        pygame.draw.rect(screen, (255, 102, 0), pygame.Rect(200, 350, 200, 100))

        t_play_again = pygame.font.SysFont("arial narrow", 45).render("PLAY AGAIN", True, (0, 0, 0))
        screen.blit(t_play_again, (300 - t_play_again.get_width() // 2, 390 - t_play_again.get_height() // 2))

        t_press_up_or_w_2 = pygame.font.SysFont("arial narrow", 30).render("Press UP or \"W\"", True, (0, 0, 0))
        screen.blit(t_press_up_or_w_2, (300 - t_press_up_or_w_2.get_width() // 2, 420 - t_press_up_or_w_2.get_height() // 2))

        pygame.draw.rect(screen, (255, 102, 0), pygame.Rect(600, 350, 200, 100))

        t_return_to_menu = pygame.font.SysFont("arial narrow", 30).render("RETURN TO MENU", True, (0, 0, 0))
        screen.blit(t_return_to_menu, (700 - t_return_to_menu.get_width() // 2, 390 - t_return_to_menu.get_height() // 2))

        t_press_m = pygame.font.SysFont("arial narrow", 30).render("Press \"M\"", True, (0, 0, 0))
        screen.blit(t_press_m, (700 - t_press_m.get_width() // 2, 420 - t_press_m.get_height() // 2))

        print("-----------------------------------------------------\nLevel", level, "incompleted\n-----------------------------------------------------")

        pygame.display.flip()
        pygame.time.wait(1000)

        waiting_for_operation = True
        while waiting_for_operation:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting_for_operation = False
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == pygame.K_w):
                    print("Play again\n-----------------------------------------------------")
                    return levels(level)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    print("Returning to menu\n-----------------------------------------------------")
                    return menu()


def walk_through_wall(x, y):
    if x == -50:
        x = 950
    elif x == 1000:
        x = 0
    if y == -50:
        y = 550
    elif y == 600:
        y = 0
    return x, y


def walk_through_wall_random(x, y):
    if (y == -50) and (0 <= x <= 950):  # top side
        x, y = random.choice([(0, 50), (0, 100), (0, 150), (0, 200), (0, 250), (0, 300), (0, 350), (0, 400), (0, 450),
                              (0, 500), (0, 550), (950, 50), (950, 100), (950, 150), (950, 200), (950, 250), (950, 300),
                              (950, 350), (950, 400), (950, 450), (950, 500), (950, 550), (50, 550), (100, 550),
                              (150, 550), (200, 550), (250, 550), (300, 550), (350, 550), (400, 550), (450, 550),
                              (500, 550), (550, 550), (600, 550), (650, 550), (700, 550), (750, 550), (800, 550),
                              (850, 550), (900, 550)])
    elif (y == 600) and (0 <= x <= 950):  # down side
        x, y = random.choice([(0, 0), (0, 50), (0, 100), (0, 150), (0, 200), (0, 250), (0, 300), (0, 350), (0, 400),
                              (0, 450), (0, 500), (50, 0), (100, 0), (150, 0), (200, 0), (250, 0), (300, 0), (350, 0),
                              (400, 0), (450, 0), (500, 0), (550, 0), (600, 0), (650, 0), (700, 0), (750, 0), (800, 0),
                              (850, 0), (900, 0), (950, 0), (950, 50), (950, 100), (950, 150), (950, 200), (950, 250),
                              (950, 300), (950, 350), (950, 400), (950, 450), (950, 500)])
    elif (x == -50) and (0 <= y <= 550):  # left side
        x, y = random.choice([(50, 0), (100, 0), (150, 0), (200, 0), (250, 0), (300, 0), (350, 0), (400, 0), (450, 0),
                              (500, 0), (550, 0), (600, 0), (650, 0), (700, 0), (750, 0), (800, 0), (850, 0), (900, 0),
                              (950, 0), (950, 50), (950, 100), (950, 150), (950, 200), (950, 250), (950, 300),
                              (950, 350), (950, 400), (950, 450), (950, 500), (50, 550), (100, 550), (150, 550),
                              (200, 550), (250, 550), (300, 550), (350, 550), (400, 550), (450, 550), (500, 550),
                              (550, 550), (600, 550), (650, 550), (700, 550), (750, 550), (800, 550), (850, 550),
                              (900, 550), (950, 550)])
    elif (x == 1000) and (0 <= y <= 550):  # right side
        x, y = random.choice([(0, 550), (50, 550), (100, 550), (150, 550), (200, 550), (250, 550), (300, 550),
                              (350, 550), (400, 550), (450, 550), (500, 550), (550, 550), (600, 550), (650, 550),
                              (700, 550), (750, 550), (800, 550), (850, 550), (900, 550), (0, 0), (0, 50), (0, 100),
                              (0, 150), (0, 200), (0, 250), (0, 300), (0, 350), (0, 400), (0, 450), (0, 500), (50, 0),
                              (100, 0), (150, 0), (200, 0), (250, 0), (300, 0), (350, 0), (400, 0), (450, 0), (500, 0),
                              (550, 0), (600, 0), (650, 0), (700, 0), (750, 0), (800, 0), (850, 0), (900, 0)])
    return x, y


def flashing_snake(colors, actual_color, lenght, path_x, path_y):
    if (actual_color is None) or (actual_color == colors[1]):
        color = colors[0]
    elif actual_color == colors[0]:
        color = colors[1]
    article = -lenght
    while article < 0:
        print("Snake article color change")
        pygame.draw.rect(screen, color, pygame.Rect(path_x[article], path_y[article], 50, 50))
        article += 1
    return color


def levels(level):
    if level == 1:
        return the_game(a=random.randrange(0, 1000, 50), b=random.randrange(0, 600, 50), speed=3, lenght_required=20,
                        level_settings={"level": level, "walk-through-wall": True, "walk-through-wall-random": False,
                                        "flashing-snake": False, "snake-color": (255, 255, 255)})
    elif level == 2:
        return the_game(a=random.randrange(0, 1000, 50), b=random.randrange(0, 600, 50), speed=4, lenght_required=40,
                        level_settings={"level": level, "walk-through-wall": False, "walk-through-wall-random": False,
                                        "flashing-snake": False, "snake-color": (0, 204, 255)})
    elif level == 3:
        return the_game(a=random.randrange(0, 1000, 50), b=random.randrange(0, 600, 50), speed=4, lenght_required=50,
                        level_settings={"level": level, "walk-through-wall": False, "walk-through-wall-random": True,
                                        "flashing-snake": False, "snake-color": (255, 102, 0)})
    elif level == 4:
        return the_game(a=random.randrange(0, 1000, 50), b=random.randrange(0, 600, 50), speed=3, lenght_required=65,
                        level_settings={"level": level, "walk-through-wall": False, "walk-through-wall-random": True,
                                        "flashing-snake": True, "snake-colors": [(255, 255, 0), (0, 255, 0)]})
    elif level == 5:
        return the_game(a=random.randrange(0, 1000, 50), b=random.randrange(0, 600, 50), speed=5, lenght_required=10,
                        level_settings={"level": level, "walk-through-wall": False, "walk-through-wall-random": True,
                                        "flashing-snake": True, "snake-colors": [(255, 255, 255), (0, 0, 0)]})
    else:
        screen.fill((0, 0, 0))
        pygame.display.flip()

        t_game_finished = pygame.font.SysFont("arial narrow", 120).render("Game finished!", True, (153, 204, 0))
        screen.blit(t_game_finished, (500 - t_game_finished.get_width() // 2, 300 - t_game_finished.get_height() // 2))

        t_feedback = pygame.font.SysFont("arial narrow", 25).render("Please, give me some feedback to I can improve my skills in Pygame, thank you!", True, (153, 204, 0))
        screen.blit(t_feedback, (500 - t_feedback.get_width() // 2, 400 - t_feedback.get_height() // 2))

        print("Game finished\n-----------------------------------------------------")

        pygame.display.flip()
        pygame.time.wait(3000)

        menu()


def the_game(a, b, speed, lenght_required, level_settings):
    screen.fill((0, 0, 0))

    t_level = pygame.font.SysFont("arial narrow", 120).render("Level " + str(level_settings["level"]), True, (0, 255, 255))
    screen.blit(t_level, (500 - t_level.get_width() // 2, 300 - t_level.get_height() // 2))

    print("Level", str(level_settings["level"]), "\n-----------------------------------------------------")

    pygame.display.flip()
    pygame.time.wait(2000)

    screen.fill((0, 0, 0))
    pygame.display.flip()

    x, y = None, None
    path_x, path_y = [-50], [0]
    direction, lenght, actual_color = 3, 1, None

    playing = True
    while playing:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: playing = False
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != 1: direction = 0
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != 0: direction = 1
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != 3: direction = 2
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != 2: direction = 3

            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                print("Returning to menu\n-----------------------------------------------------")

                screen.fill((0, 0, 0))
                pygame.display.flip()

                return menu()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                t_paused = pygame.font.SysFont("arial narrow", 25).render("PAUSED", True, (0, 255, 0))
                screen.blit(t_paused, (950 - t_paused.get_width() // 2, 620 - t_paused.get_height() // 2))

                print("Game paused\n-----------------------------------------------------")

                pygame.display.flip()
                pygame.time.wait(500)

                wait = True
                while wait:
                    for event in pygame.event.get():
                        if (event.type == pygame.QUIT) or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: playing, wait = False, False

                        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                            print("Returning to menu\n-----------------------------------------------------")

                            screen.fill((0, 0, 0))
                            pygame.display.flip()

                            return menu()

                    if pygame.key.get_pressed()[pygame.K_p]:
                        print("Resuming game\n-----------------------------------------------------")
                        wait = False

        if (x and y) is None:
            x, y = 0, 0
        else:
            print("Direction:")
            if direction == 0:
                y -= 50
                print("UP")
            elif direction == 1:
                y += 50
                print("DOWN")
            elif direction == 2:
                x -= 50
                print("LEFT")
            elif direction == 3:
                x += 50
                print("RIGHT")

        if level_settings["walk-through-wall"] is True:
            x, y = walk_through_wall(x, y)

        elif level_settings["walk-through-wall-random"] is True:
            x, y = walk_through_wall_random(x, y)

        elif (level_settings["walk-through-wall"] and level_settings["walk-through-wall-random"]) is False:
            if (x < 0) or (x > 950) or (y < 0) or (y > 550):
                return end_of_game(lenght, lenght_required, level_settings["level"])

        path_x.append(x)
        path_y.append(y)

        if lenght == lenght_required or hit_body_check(x, y, path_x, path_y, lenght) is True:
            return end_of_game(lenght, lenght_required, level_settings["level"])

        else:
            if x == a and y == b:
                a, b = calculate_new_food_position(path_x, path_y, lenght)
                lenght += 1

            if level_settings["flashing-snake"] is True:
                actual_color = flashing_snake(level_settings["snake-colors"], actual_color, lenght, path_x, path_y)
            else:
                actual_color = level_settings["snake-color"]

            pygame.draw.rect(screen, actual_color, pygame.Rect(path_x[-2], path_y[-2], 50, 50))                   # snake's body
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(path_x[-lenght - 1], path_y[-lenght - 1], 50, 50))    # a square at the end of snake
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x, y, 50, 50))                                  # snake's head
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(a, b, 50, 50))                                      # food
            pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(0, 600, 1000, 50))                                 # bottom bar

            t_information = pygame.font.SysFont("arial narrow", 25).render("lenght required: " + str(lenght_required) +
                                                                           " | lenght: " + str(lenght) + " | speed: " + str(speed) +
                                                                           " | direction: WASD/arrows | pause: P | menu: M | close game: ESC", True, (255, 255, 0))
            screen.blit(t_information, (440 - t_information.get_width() // 2, 620 - t_information.get_height() // 2))

            print("x:", x, "y:", y, "a:", a, "b:", b, "lenght:", lenght, "speed:", speed, "fps\n-----------------------------------------------------")

            pygame.display.flip()

        pygame.time.Clock().tick_busy_loop(speed)


def menu():
    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (255, 102, 0), pygame.Rect(400, 150, 200, 100), 1)

    t_play = pygame.font.SysFont("arial narrow", 100).render("Play", True, (255, 204, 0))
    screen.blit(t_play, (500 - t_play.get_width() // 2, 190 - t_play.get_height() // 2))

    t_press_up_or_w = pygame.font.SysFont("arial narrow", 30).render("Press UP or \"W\"", True, (255, 204, 0))
    screen.blit(t_press_up_or_w, (500 - t_press_up_or_w.get_width() // 2, 235 - t_press_up_or_w.get_height() // 2))

    pygame.draw.rect(screen, (255, 102, 0), pygame.Rect(400, 300, 200, 100), 1)

    t_reset = pygame.font.SysFont("arial narrow", 50).render("Reset game", True, (255, 204, 0))
    screen.blit(t_reset, (500 - t_reset.get_width() // 2, 340 - t_reset.get_height() // 2))

    t_press_r = pygame.font.SysFont("arial narrow", 30).render("Press \"R\"", True, (255, 204, 0))
    screen.blit(t_press_r, (500 - t_press_r.get_width() // 2, 380 - t_press_r.get_height() // 2))

    print("Menu\n-----------------------------------------------------")

    pygame.display.flip()

    waiting_for_operation = True
    while waiting_for_operation:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_operation = False
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == pygame.K_w):
                try:
                    f = open("Snake-game-data.abc", "r")
                    content = int(f.read())
                    f.close()
                except (FileNotFoundError, ValueError):
                    f = open("Snake-game-data.abc", "w")
                    f.write("1")
                    f.close()
                    content = 1
                finally:
                    return levels(content)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                screen.fill((0, 0, 0))

                f = open("Snake-game-data.abc", "w")
                f.close()

                t_game_data_reset = pygame.font.SysFont("arial narrow", 120).render("Game data reset!", True, (153, 204, 0))
                screen.blit(t_game_data_reset, (500 - t_game_data_reset.get_width() // 2, 300 - t_game_data_reset.get_height() // 2))

                print("Game data reset\n-----------------------------------------------------")

                pygame.display.flip()
                pygame.time.wait(3000)

                menu()


menu()

screen.fill((0, 0, 0))

t_closing_game = pygame.font.SysFont("arial narrow", 120).render("Closing game!", True, (0, 255, 255))
screen.blit(t_closing_game, (500 - t_closing_game.get_width() // 2, 300 - t_closing_game.get_height() // 2))

print("Closing game\n-----------------------------------------------------")

pygame.display.flip()
pygame.time.wait(1000)



