import logging
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.vector import Vector
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from random import randint


def update_window_size():
    global WINDOW_HEIGHT, WINDOW_WIDTH
    WINDOW_WIDTH, WINDOW_HEIGHT = Window.size
    WINDOW_HEIGHT -= 60

PLAYER_SIZE = 40
GAME_SPEED = .15


class Words():
    def __init__(self, words):
        colors = [white, red, green, blue, yellow]
        random.shuffle(colors)
        colors = colors[:len(words)]
        words_combination = [[word, color] for word, color in zip(words, colors[:])]
        random.shuffle(words_combination)
        self.not_shuffled_words = words
        self.diction = [[word, color] for word, color in zip(words, colors)]
        self.words_combination = words_combination
        self.colors = colors


class Fruit(Widget):
    def move(self, new_pos):
        self.pos = new_pos


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

    head = ObjectProperty(None)
    fruit = ObjectProperty(None)
    score = NumericProperty(0)
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
        self.score = 0

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

        # move the head
        self.head.move()

        # check if we found the fruit, if so, add another tail
        if self.head.pos == self.fruit.pos:
            self.score += 1
            self.tail.append(
                SnakeTail(
                    pos=self.head.pos,
                    size=self.head.size))
            self.add_widget(self.tail[-1])
            self.spawn_fruit()

    def spawn_fruit(self):
        roll = self.fruit.pos
        found = False
        while not found:
            # roll new random positions until one is free
            roll = [PLAYER_SIZE *
                    randint(0, int(WINDOW_WIDTH / PLAYER_SIZE) - 1),
                    PLAYER_SIZE *
                    randint(0, int(WINDOW_HEIGHT / PLAYER_SIZE) - 1)]

            if self.occupied[roll] is True or \
                    roll == self.head.pos:
                continue

            found = True

        self.fruit.move(roll)

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
