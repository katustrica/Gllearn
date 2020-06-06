import random
from collections import OrderedDict

from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivy.app import App


def shuffle_dict(d):
    keys = list(d.keys())
    random.shuffle(keys)
    return {k: d[k] for k in keys}

class Words(Screen):
    app = App.get_running_app()
    def on_enter(self):
        for word, color in shuffle_dict(self.app.words_with_color).items():
            self.ids.box_words.add_widget(
                MDLabel(
                    text=word,
                    halign="center",
                    theme_text_color='Custom',
                    text_color= color
                )
            )