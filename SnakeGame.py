import pygame
import sys
import time
import random
import numpy as np
from math import inf


class SnakeGame:
    def __init__(self):
        # Difficulty settings
        # Easy      ->  10
        # Medium    ->  25
        # Hard      ->  40
        # Harder    ->  60
        # Impossible->  120
        self.difficulty = 25
        self.frame_size_x = 720
        self.frame_size_y = 480
        self.games = 0
        self.bestScore = 0
        check_errors = pygame.init()
        if check_errors[1] > 0:
            print(
                f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
            sys.exit(-1)
        else:
            print('[+] Game successfully initialised')
        pygame.display.set_caption('SnAIke')
        self.game_window = pygame.display.set_mode(
            (self.frame_size_x, self.frame_size_y))

        # Colors (R, G, B)
        self.black = pygame.Color(43, 54, 193)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(94, 0, 9)
        self.blue = pygame.Color(0, 0, 255)

        # FPS (frames per second) controller
        self.fps_controller = pygame.time.Clock()

        # Game variables
        self.snake_pos = [360, 240]
        self.snake_body = [[360, 240], [360-10, 240], [360-(2*10), 240]]

        self.food_pos = [random.randrange(1, (self.frame_size_x//10))
                         * 10, random.randrange(1, (self.frame_size_y//10)) * 10]
        self.food_spawn = True

        self.direction = 'RIGHT'
        self.change_to = self.direction

        self.score = 0
        self.reset_next = False

        self.dist = inf

        self.steps = 0
        self.maxsteps = 200
        self.bonus_steps = 100
        self.timed_out = False


    def reset(self):
        self.games += 1
        if(self.score > self.bestScore):
            self.bestScore = self.score
        self.difficulty = 25
        self.frame_size_x = 720
        self.frame_size_y = 480

        # Colors (R, G, B)
        self.black = pygame.Color(43, 54, 193)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(94, 0, 9)
        self.blue = pygame.Color(0, 0, 255)

        # Game variables
        self.snake_pos = [360, 240]
        self.snake_body = [[360, 240], [360-10, 240], [360-(2*10), 240]]

        self.food_pos = [random.randrange(1, (self.frame_size_x//10))
                         * 10, random.randrange(1, (self.frame_size_y//10)) * 10]

        self.food_spawn = True

        self.direction = 'RIGHT'
        self.change_to = self.direction

        self.score = 0
        self.reset_next = False

        self.dist = inf

        self.steps = 0
        self.timed_out = False

    def getScore(self):
        return self.score
    # Score

    def show_score(self, choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render(
            'Score: ' + str(self.score) + ' game ' + str(self.games) + ' best ' + str(self.bestScore), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (self.frame_size_x/10, 15)
        else:
            score_rect.midtop = (self.frame_size_x/2, self.frame_size_y/1.25)
        self.game_window.blit(score_surface, score_rect)

    def show(self):
        # GFX
        self.game_window.fill(self.black)
        for pos in self.snake_body:
            # Snake body
            # .draw.rect(play_surface, color, xy-coordinate)
            # xy-coordinate -> .Rect(x, y, size_x, size_y)
            pygame.draw.rect(self.game_window, self.green,
                             pygame.Rect(pos[0], pos[1], 10, 10))

        # Snake food
        pygame.draw.rect(self.game_window, self.white, pygame.Rect(
            self.food_pos[0], self.food_pos[1], 10, 10))

        self.show_score(1, self.white, 'consolas', 20)
        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        self.fps_controller.tick(self.difficulty)

    def takeAction(self, direction):
        self.change_to = direction
        return direction

    def update(self):
        # if(self.reset_next):
        #     self.reset()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Whenever a key is pressed down
            elif event.type == pygame.KEYDOWN:
                # W -> Up; S -> Down; A -> Left; D -> Right
                if event.key == pygame.K_UP or event.key == ord('w'):
                    self.change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.change_to = 'RIGHT'
                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Making sure the snake cannot move in the opposite self.direction instantaneously
        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

        # Moving the snake
        if self.direction == 'UP':
            self.snake_pos[1] -= 10
        if self.direction == 'DOWN':
            self.snake_pos[1] += 10
        if self.direction == 'LEFT':
            self.snake_pos[0] -= 10
        if self.direction == 'RIGHT':
            self.snake_pos[0] += 10

        # Snake body growing mechanism
        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
            self.score += 500
            self.food_spawn = False
            self.steps -= self.bonus_steps
        else:
            self.snake_body.pop()
            # self.score -= 1

        # Game Over conditions
        # Getting out of bounds
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.frame_size_x-10:
            self.reset_next = True
            
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.frame_size_y-10:
            self.reset_next = True

        # Touching the snake body
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                self.reset_next = True

        #ran out of time
        if self.steps >= self.maxsteps:
            self.reset_next = True
            self.timed_out = True
        self.steps += 1

        # Spawning food on the screen
        if not self.food_spawn:
            self.food_pos = [random.randrange(1, (self.frame_size_x//10))
                             * 10, random.randrange(1, (self.frame_size_y//10)) * 10]

        self.food_spawn = True

    def getStates(self):
        feature_arr = np.zeros(11)
        feature_arr[0] = 1 if self.snake_pos[0] >= self.food_pos[0] else 0
        feature_arr[1] = 1 if self.snake_pos[1] >= self.food_pos[1] else 0
        # Check if obstacle directly above
        if self.snake_pos[1] - 10 < 0:
            feature_arr[2] = 1
        else:
            for i in range(len(self.snake_body)):
                if(self.snake_body[i][0] == self.snake_pos[0] and self.snake_body[i][1] == self.snake_pos[1] - 10):
                    feature_arr[2] = 1
        # Check if obstacle directly below
        if self.snake_pos[1] + 10 > self.frame_size_y:
            feature_arr[3] = 1
        else:
            for i in range(len(self.snake_body)):
                if(self.snake_body[i][0] == self.snake_pos[0] and self.snake_body[i][1] == self.snake_pos[1] + 10):
                    feature_arr[3] = 1
        # Check if obstacle directly to the left
        if self.snake_pos[0] - 10 < 0:
            feature_arr[4] = 1
        else:
            for i in range(len(self.snake_body)):
                if(self.snake_body[i][1] == self.snake_pos[1] and self.snake_body[i][0] == self.snake_pos[0] - 10):
                    feature_arr[4] = 1
        # Check if obstacle directly to the right
        if self.snake_pos[0] + 10 > self.frame_size_x:
            feature_arr[5] = 1
        else:
            for i in range(len(self.snake_body)):
                if(self.snake_body[i][1] == self.snake_pos[1] and self.snake_body[i][0] == self.snake_pos[0] + 10):
                    feature_arr[5] = 1

        feature_arr[6] = 1 if self.direction == "UP" else 0
        feature_arr[7] = 1 if self.direction == "RIGHT" else 0
        feature_arr[8] = 1 if self.direction == "DOWN" else 0
        feature_arr[9] = 1 if self.direction == "LEFT" else 0

        feature_arr[10] = abs(self.food_pos[0]//10-self.snake_pos[0]//10) + \
            abs(self.food_pos[1]//10-self.snake_pos[1]//10)

        return feature_arr


if __name__ == '__main__':
    game = SnakeGame()
    while True:
        game.update()
        game.show()
