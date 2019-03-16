import random

from pygame.locals import *
import pygame


class cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dir_x=1, dir_y=0, color=(255, 0, 0)):
        self.pos = start
        self.dir_x = 1
        self.dir_y = 0
        self.color = color

    def move(self, dir_x, dir_y):
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.pos = (self.pos[0] + self.dir_x, self.pos[1] + self.dir_y)

    def draw(self, surface, eyes=False):
        distance = self.w // self.rows
        cube_row = self.pos[0]
        cube_column = self.pos[1]

        pygame.draw.rect(surface, self.color, (cube_row*distance+1, cube_column*distance+1, distance-2, distance-2))


class snake(object):
    body = []
    turns = {}

    i = 0

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dir_x = 0
        self.dir_y = 1

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT] and (self.dir_y != 0 and self.dir_x != 1):
                    self.dir_x = -1
                    self.dir_y = 0
                elif keys[pygame.K_RIGHT] and (self.dir_y != 0 and self.dir_x != -1):
                    self.dir_x = 1
                    self.dir_y = 0
                elif keys[pygame.K_UP] and (self.dir_y != 1 and self.dir_x != 0):
                    self.dir_x = 0
                    self.dir_y = -1
                elif keys[pygame.K_DOWN] and (self.dir_y != -1 and self.dir_x != 0):
                    self.dir_x = 0
                    self.dir_y = 1
                self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
        self.move()

    def move(self):
        self.i += 1

        if(self.i >= 60):
            self.i = 0

        speed = len(self.body)
        if(speed <= 2):
            speed = 2

        if(self.i % speed == 0): ## Modulus operator
            return

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(
                        self.body) - 1:  ## If we are on the last cube/turn, it needs to stop that cube from turning too, so we remove from list
                    self.turns.pop(p)

            else:  ## Checks if we are on the edge of the screen
                ## Runs through scenarios where if we hit an edge of the screen, it will place the snake accordingly on the other edge. If non of that is true we simply move
                if c.dir_x == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dir_x == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dir_y == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dir_y == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dir_x, c.dir_y)


    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dir_x = 0
        self.dir_y = 1

    def add_cube(self):
        tail = self.body[-1]
        dir_x, dir_y = tail.dir_x, tail.dir_y

        if dir_x == 1 and dir_y == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dir_x == -1 and dir_y == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dir_x == 0 and dir_y == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dir_x == 0 and dir_y == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dir_x = dir_x
        self.body[-1].dir_y = dir_y

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0: ## Checks if its the first snake "Cube", if so. it should have eyes, so we can see where the head is.
                c.draw(surface, True)
            else:
                c.draw(surface)

class game():
    def __init__(self):
        self.width = 500
        self.height = 500
        self.rows = 20
        self.player = snake((255, 0, 0), (10, 10))
        self.snack = cube(self.random_snack(self.rows, self.player), color=(0, 255, 0))

    def redraw_window(self,window):
        window.fill((0, 0, 0))
        self.player.draw(window)
        self.snack.draw(window)
        pygame.display.update()

    def random_snack(self,rows, player):
        positions = player.body

        while True:
            x = random.randrange(rows)
            y = random.randrange(rows)
            if len(list(filter(lambda it: it.pos == (x, y), positions))) > 0:
                continue
            else:
                break

        return x, y


    def start(self):
        window = pygame.display.set_mode((self.width, self.height))
        game = True

        clock = pygame.time.Clock()  ## Does so the game does not run more than 10 frames per sec
        while game:
            pygame.time.delay(50)  ## Delays the game with a few milisec so it doesnt run too fast
            clock.tick(60)
            self.player.event_handler()
            if self.player.body[0].pos == self.snack.pos:
                self.player.add_cube()
                self.snack = cube(self.random_snack(self.rows, self.player), color=(0, 255, 0))

            for x in range(len(self.player.body)):
                if self.player.body[x].pos in list(map(lambda it: it.pos, self.player.body[x + 1:])):
                    print("Score: ", len(self.player.body))
                    self.player.reset((10, 10))
                    break

            self.redraw_window(window)

        pass
game = game()
game.start();

