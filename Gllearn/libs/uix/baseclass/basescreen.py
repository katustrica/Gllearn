from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.utils import get_hex_from_color

from libs.applibs.floatingactionbuttons import FloatingActionButtons


class BaseScreen(Screen):
    app = App.get_running_app()

    def on_enter(self):
        self.add_widget(FloatingActionButtons(
            icon='lead-pencil',
            floating_data={
                'Python': 'language-python',
                'Php': 'language-php',
                'C++': 'language-cpp'},
            callback=self.set_my_language))

    def set_my_language(self, instance_button=None):
        if instance_button:
            text = instance_button.icon.split('-')[1]
        else:
            text = 'Python'
        text = self.app.translation._(
            'Я программирую на [color=%s]%s[/color]') % (
                get_hex_from_color(self.app.theme_cls.primary_color),
                text.capitalize())
        self.ids.label_screen.text = text
        # self.app.back_screen(27)
        return text