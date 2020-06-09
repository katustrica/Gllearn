from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.utils import get_hex_from_color

from kivymd.uix.button import MDFloatingActionButtonSpeedDial

class BaseScreen(Screen):
    app = App.get_running_app()
    data = {
        'language-python': 'Змейка полиглот',
        'translate': 'Переводы',
        'web': 'Язык игр',
    }

    def hello(self, instance_button=None):
        text = self.app.translation._('Привет! Во что будешь [color={}]играть[/color]? ').format(
            get_hex_from_color(self.app.theme_cls.primary_color)
        )
        self.ids.label_screen.text = text
        return text

    def select_game(self, instance):
        if instance.icon == 'language-python':
            self.app.show_words(self)
        elif instance.icon == 'translate':
            pass
        elif instance.icon == 'web':
            self.app.select_game_locale(self)