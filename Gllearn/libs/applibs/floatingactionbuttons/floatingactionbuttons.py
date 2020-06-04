import os

from kivy.animation import Animation
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.properties import StringProperty, DictProperty, ObjectProperty
from kivy.metrics import dp

from kivymd.uix.card import MDCard

kv_file = os.path.splitext(__file__)[0] + '.kv'
with open(kv_file, encoding='utf-8') as kv:
    Builder.load_string(kv.read())


class FloatingLabel(MDCard):
    text = StringProperty()


class FloatingActionButtons(FloatLayout):
    icon = StringProperty('checkbox-blank-circle')
    callback = ObjectProperty(lambda x: None)
    floating_data = DictProperty()
    show = False

    def __init__(self, **kwargs):
        super(FloatingActionButtons, self).__init__(**kwargs)

        self.lbl_list = [self.ids.f_lbl_1, self.ids.f_lbl_2, self.ids.f_lbl_3]
        self.btn_list = [self.ids.f_btn_1, self.ids.f_btn_2, self.ids.f_btn_3]

    def show_floating_buttons(self):
        step = dp(46)
        for btn in self.btn_list:
            step += dp(56)
            Animation(y=step, d=.5, t='out_elastic').start(btn)

        self.show = True if not self.show else False
        self.show_floating_labels() if self.show \
            else self.hide_floating_labels()

    def show_floating_labels(self):
        i = 0
        for lbl in self.lbl_list:
            i += .3
            pos_x = Window.width - (lbl.width + dp(46 + 21 * 1.5))
            Animation(x=pos_x, d=i, t='out_elastic').start(lbl)

    def hide_floating_buttons(self):
        for btn in self.btn_list:
            Animation(y=25, d=.5, t='in_elastic').start(btn)

    def hide_floating_labels(self):
        i = 1
        for lbl in self.lbl_list:
            i -= .3
            Animation(x=-lbl.width, d=i, t='out_elastic').start(lbl)
        self.hide_floating_buttons()
