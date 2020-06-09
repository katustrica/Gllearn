import logging
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.uix.screenmanager import Screen
from kivy.vector import Vector
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from random import randint
from collections import deque


def update_window_size():
    global WINDOW_HEIGHT, WINDOW_WIDTH
    WINDOW_WIDTH, WINDOW_HEIGHT = Window.size
    WINDOW_HEIGHT -= 60

PLAYER_SIZE = 40
GAME_SPEED = .15


class Fruit(Widget):
    def __init__(self, color, word, **kwargs):
        super(Fruit, self).__init__(**kwargs)

        pos = [PLAYER_SIZE * randint(0, int(WINDOW_WIDTH / PLAYER_SIZE) - 2),
               PLAYER_SIZE * randint(0, int(WINDOW_HEIGHT / PLAYER_SIZE) - 2)]
        size = (PLAYER_SIZE, PLAYER_SIZE)
        self.label = Label(text=word,
                           font_size='10sp',
                           color=(1, 1, 1, 1),
                           pos=[pos[0]-30, pos[1]-30],
                           halign='center',
                           valign='center',
                           text_size=[size[0], size[1]])
        with self.label.canvas.before:
            Color(*color)
            self.label.rect = Ellipse(pos=pos, size=size)
        self.add_widget(self.label)

class SnakeTail(Widget):

    def move(self, new_pos):
        self.pos = new_pos


class SnakeHead(Widget):

    orientation = (PLAYER_SIZE, 0)

    def reset_pos(self):
        update_window_size()
        # positions the player roughly in the middle of the gameboard
        self.pos = \
            [int(WINDOW_WIDTH / 2 - (WINDOW_WIDTH / 2 % PLAYER_SIZE)),
             int(WINDOW_HEIGHT / 2 - (WINDOW_HEIGHT / 2 % PLAYER_SIZE))]
        self.orientation = (PLAYER_SIZE, 0)

    def move(self):
        self.pos = Vector(*self.orientation) + self.pos


class smartGrid:

    def __init__(self):
        """2D grid of zeros used to track if snake collides with its tail

        Usage: self.occupied[coords] = True
               if self.occupied[coords] is True
        """
        update_window_size()
        self.grid = [[False for i in range(WINDOW_HEIGHT)]
                     for j in range(WINDOW_WIDTH)]

    def __getitem__(self, coords):
        return self.grid[coords[0]][coords[1]]

    def __setitem__(self, coords, value):
        self.grid[coords[0]][coords[1]] = value


class SnakeGame(Widget):
    app = App.get_running_app()
    head = ObjectProperty(None)
    fruits_pos = deque()
    fruits = deque()
    score = StringProperty("")
    player_size = NumericProperty(PLAYER_SIZE)
    game_over = StringProperty("")

    def __init__(self, **kwargs):
        super(SnakeGame, self).__init__(**kwargs)
        update_window_size()
        Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        Window.bind(on_key_down=self.key_action)

        if PLAYER_SIZE < 3:
            raise ValueError("Player size should be at least 3 px")

        if WINDOW_HEIGHT < 3 * PLAYER_SIZE or WINDOW_WIDTH < 3 * PLAYER_SIZE:
            raise ValueError(
                "Window size must be at least 3 times larger than player size")
        self.tail = []
        self.timer = None

    def restart_game(self):
        """Resets the game to its initial state
        """
        update_window_size()
        self.occupied = smartGrid()
        logging.info('Restarted game.')
        # resets the timer
        if self.timer:
            self.timer.cancel()
        self.timer = Clock.schedule_interval(self.refresh, GAME_SPEED)
        self.head.reset_pos()
        self.score = ''

        for block in self.tail:
            self.remove_widget(block)

        # the tail is indexed in a way that the last block is idx 0
        self.tail = []

        # first two blocks added to the tail
        self.tail.append(
            SnakeTail(
                pos=(self.head.pos[0] - PLAYER_SIZE, self.head.pos[1]),
                size=(self.head.size)
            )
        )
        # self.tail[0].canvas.children[0].rgb = [1, 1, 1]
        self.add_widget(self.tail[-1])
        self.occupied[self.tail[-1].pos] = True

        self.tail.append(
            SnakeTail(
                pos=(self.head.pos[0] - 2 * PLAYER_SIZE, self.head.pos[1]),
                size=(self.head.size)
            )
        )
        self.add_widget(self.tail[-1])
        self.occupied[self.tail[1].pos] = True

        self.spawn_fruit()

    def refresh(self, dt):
        """This block of code is executed every GAME_SPEED seconds

        'dt' must be used to allow kivy.Clock objects to use this function
        """
        update_window_size()
        # outside the boundaries of the game
        if not (0 <= self.head.pos[0] < WINDOW_WIDTH) or \
           not (0 <= self.head.pos[1] < WINDOW_HEIGHT):
            self.restart_game()
            return

        # collides with its tail
        if self.occupied[self.head.pos] is True:
            self.restart_game()
            return

        # move the tail
        self.occupied[self.tail[-1].pos] = False
        self.tail[-1].move(self.tail[-2].pos)

        for i in range(2, len(self.tail)):
            self.tail[-i].move(new_pos=(self.tail[-(i + 1)].pos))

        self.tail[0].move(new_pos=self.head.pos)
        self.occupied[self.tail[0].pos] = True

        self.head.move()
        if not self.fruits_pos:
            self.end_round()
            return
        if (self.head.pos[0] == int(self.fruits_pos[0][0])) and (self.head.pos[1] == int(self.fruits_pos[0][1])):
            self.fruits_pos.popleft()
            fruit = self.fruits.popleft()
            self.score += str(fruit.label.text) + ' '
            self.remove_widget(fruit)
            self.tail.append(
                SnakeTail(
                    pos=self.head.pos,
                    size=self.head.size))
            self.add_widget(self.tail[-1])

    def spawn_fruit(self):
        for fruit in self.fruits:
            self.remove_widget(fruit)
        words_with_color = self.app.snake_words_with_color[self.app.current_round_snake]
        self.fruits = deque([Fruit(color, word) for word, color in words_with_color.items()])
        self.fruits_pos = deque([fruit.label.rect.pos for fruit in self.fruits])

        for fruit in self.fruits:
            self.add_widget(fruit)

    def key_action(self, *args):
        """This handles user input
        """

        command = list(args)[3]

        if command == 'w' or command == 'up':
            self.head.orientation = (0, PLAYER_SIZE)
        elif command == 's' or command == 'down':
            self.head.orientation = (0, -PLAYER_SIZE)
        elif command == 'a' or command == 'left':
            self.head.orientation = (-PLAYER_SIZE, 0)
        elif command == 'd' or command == 'right':
            self.head.orientation = (PLAYER_SIZE, 0)
        elif command == 'r':
            self.restart_game()

    def on_touch_up(self, touch):
        dx = touch.x - touch.opos[0]
        dy = touch.y - touch.opos[1]
        if abs(dx) > abs(dy):
            if dx > 0:
                self.head.orientation = (PLAYER_SIZE, 0)
            else:
                self.head.orientation = (-PLAYER_SIZE, 0)
        else:
            if dy > 0:
                self.head.orientation = (0, PLAYER_SIZE)
            else:
                self.head.orientation = (0, -PLAYER_SIZE)

    def end_round(self):
        if self.timer:
            self.timer.cancel()
        self.clear_widgets()
        self.app.current_round_snake += 1
        self.app.next_snake_words()


class Snake(Screen):
    game = SnakeGame()

    def on_enter(self):
        update_window_size()
        self.game.restart_game()
        self.add_widget(self.game)

    def on_leave(self):
        if self.game.timer:
            self.game.timer.cancel()
        self.clear_widgets()
