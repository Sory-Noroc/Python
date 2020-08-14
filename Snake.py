# Snake game made by me
# Script designed on Windows. Cross-platform

import pygame
import sys
import tkinter
from time import sleep
from random import randrange
from os import environ


class StarterGui:
    def __init__(self):
        self.mw = tkinter.Tk()  # The main window
        self.mw.title('Snake')
        self.mw.configure(bg='yellow')  # Configuring the background
        self.x = self.mw.winfo_screenwidth() // 4
        self.y = self.mw.winfo_screenheight() // 4
        self.mw_width = self.mw.winfo_screenwidth() // 2
        self.mw_height = self.mw.winfo_screenheight() // 2
        self.mw.geometry(f'{self.mw_width}x{self.mw_height}+{self.x}+{self.y}')  # Main window positioning

    def lobby(self):
        for child in self.mw.winfo_children():  # The clearing mechanism before the lobby initialization
            child.destroy()  # Clears all the widgets
        title = tkinter.StringVar(self.mw)
        title.set('Snake')
        title_label = tkinter.Label(self.mw, justify='center', textvariable=title, fg='darkblue', bg='yellow',
                                    anchor='center', font='Arial 60', padx=0, pady=0)  # The name of the game
        settings_button = tkinter.Button(self.mw, activebackground='lightblue', bg='lightgray', fg='blue', width=30,
                                         text='Settings', command=self.settings)
        play_button = tkinter.Button(self.mw, activebackground='lightblue', bg='lightgray', fg='blue', text='Play',
                                     justify='center', width=30, command=game.game_loop)
        exit_button = tkinter.Button(self.mw, activebackground='lightblue', bg='lightgray', fg='blue', text='Exit',
                                     justify='center', width=30, command=sys.exit)

        title_label.place(x=220, y=50)  # Placing all the widgets
        play_button.place(x=220, y=160)
        exit_button.place(x=220, y=240)
        settings_button.place(x=220, y=200)
        self.mw.mainloop()  # GUI mainloop

    def settings(self):
        for child in self.mw.winfo_children():  # Clears the interface
            child.destroy()

        choose_diff_text = tkinter.StringVar(self.mw)
        choose_diff_text.set('Choose difficulty')
        difficulty_label = tkinter.Label(self.mw, justify='center', textvariable=choose_diff_text, fg='blue',
                                         bg='yellow', anchor='center', font='Arial 20', padx=0, pady=0)
        easy_button = tkinter.Button(self.mw, activebackground='lightblue', bg='lightgray', fg='blue', width=6,
                                     text='Easy', command=self.easy)
        medium_button = tkinter.Button(self.mw, activebackground='lightblue', bg='lightgray', fg='blue', width=6,
                                       text='Medium', command=self.medium)
        expert_button = tkinter.Button(self.mw, activebackground='lightblue', bg='lightgray', fg='blue', width=6,
                                       text='Expert', command=self.expert)
        return_button = tkinter.Button(self.mw, activebackground='lightblue', bg='lightgray', fg='blue', width=6,
                                       text='Return', command=self.lobby)
        exit_button = tkinter.Button(self.mw, activebackground='lightblue', bg='lightgray', fg='blue', width=6,
                                     text='Exit', command=sys.exit)

        difficulty_label.place(x=240, y=100)
        easy_button.place(x=180, y=140)
        medium_button.place(x=320, y=140)
        expert_button.place(x=460, y=140)
        return_button.place(x=280, y=300)
        exit_button.place(x=360, y=300)

    @staticmethod
    def easy():
        game.difficulty = 10

    @staticmethod
    def medium():
        game.difficulty = 25

    @staticmethod
    def expert():
        game.difficulty = 50


class Game:
    width = 720
    height = 420
    difficulty = 25

    def __init__(self, x, y):
        self.x, self.y = x, y
        pygame.init()
        self.fps_controller = pygame.time.Clock()
        self.score = 0
        self.game_window = None

    def show_score(self, choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (self.width / 10, 15)
        else:
            score_rect.midtop = (self.width / 2, self.height / 1.25)
        game.game_window.blit(score_surface, score_rect)

    def game_loop(self):  # The main game loop that runs continuously
        starter_gui.mw.destroy()  # Clears the screen
        game.__init__(starter_gui.x, starter_gui.y)
        pygame.display.set_caption('Snake')
        environ['SDL_VIDEO_WINDOW_POS'] = f"{self.x},{self.y}"
        self.game_window = pygame.display.set_mode((self.width, self.height))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Whenever a key is pressed down
                elif event.type == pygame.KEYDOWN:
                    # W -> Up; S -> Down; A -> Left; D -> Right
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        snake.change_to = 'UP'
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        snake.change_to = 'DOWN'
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        snake.change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        snake.change_to = 'RIGHT'
                    # Esc -> Create event to quit the game
                    if event.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT, {}))

            snake.move()
            snake.grow()  # Snake body growing mechanism
            food.spawn_food()
            snake.draw()
            food.draw()
            snake.check_pos()  # Getting out of bounds
            self.show_score(1, (255, 255, 255), 'consolas', 20)
            pygame.display.update()
            game.fps_controller.tick(game.difficulty)  # Refresh rate

    def over(self):  # Game Over
        my_font = pygame.font.SysFont('times new roman', 90)
        game_over_label = my_font.render('YOU DIED', True, (255, 0, 0))
        game_over_rect = game_over_label.get_rect()
        game_over_rect.midtop = (self.width / 2, self.height / 4)
        self.game_window.fill((0, 0, 0))
        self.game_window.blit(game_over_label, game_over_rect)
        self.show_score(0, (255, 0, 0), 'times', 20)
        small_font = pygame.font.SysFont('times new roman', 20)
        wait_label = small_font.render('Wait a second...', True, (255, 255, 255))
        wait_rect = wait_label.get_rect()
        wait_rect.midtop = (self.width / 2, self.height / 1.1)
        self.game_window.blit(wait_label, wait_rect)
        pygame.display.flip()
        sleep(1)
        pygame.quit()
        snake.__init__()  # For the next game
        food.__init__()
        starter_gui.__init__()
        starter_gui.lobby()


class Snake:
    def __init__(self):
        self.pos = [100, 50]
        self.body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
        self.direction = 'RIGHT'
        self.change_to = self.direction

    def draw(self):
        game.game_window.fill((0, 0, 0))
        for pos in self.body:
            pygame.draw.rect(game.game_window, (0, 255, 0), pygame.Rect(pos[0], pos[1], 10, 10))

    def grow(self):
        self.body.insert(0, list(self.pos))
        if self.pos[0] == food.pos[0] and self.pos[1] == food.pos[1]:
            game.score += 1
            food.spawn = False
        else:
            self.body.pop()

    def check_pos(self):
        if self.pos[0] < 0 or self.pos[0] > game.width - 10:
            game.over()
        if self.pos[1] < 0 or self.pos[1] > game.height - 10:
            game.over()
        for block in self.body[1:]:  # Touching the snake body
            if self.pos[0] == block[0] and self.pos[1] == block[1]:
                game.over()

    def move(self):
        # Making sure the snake cannot move in the opposite direction instantaneously
        if snake.change_to == 'UP' and snake.direction != 'DOWN':
            snake.direction = 'UP'
        if snake.change_to == 'DOWN' and snake.direction != 'UP':
            snake.direction = 'DOWN'
        if snake.change_to == 'LEFT' and snake.direction != 'RIGHT':
            snake.direction = 'LEFT'
        if snake.change_to == 'RIGHT' and snake.direction != 'LEFT':
            snake.direction = 'RIGHT'
        # Moving the snake
        if self.direction == 'UP':
            self.pos[1] -= 10
        if self.direction == 'DOWN':
            snake.pos[1] += 10
        if self.direction == 'LEFT':
            snake.pos[0] -= 10
        if self.direction == 'RIGHT':
            snake.pos[0] += 10


class Food:
    def __init__(self):
        self.pos = [randrange(1, (game.width // 10)) * 10, randrange(1, (game.height // 10))
                    * 10]
        self.spawn = True

    def draw(self):
        pygame.draw.rect(game.game_window, (255, 255, 255), pygame.Rect(self.pos[0], self.pos[1], 10, 10))

    def spawn_food(self):
        if not self.spawn:
            self.pos = [randrange(1, (game.width // 10)) * 10, randrange(1, (game.height // 10)) * 10]
        self.spawn = True


if __name__ == '__main__':
    starter_gui = StarterGui()
    game = Game(starter_gui.x, starter_gui.y)
    snake = Snake()
    food = Food()
    starter_gui.lobby()
