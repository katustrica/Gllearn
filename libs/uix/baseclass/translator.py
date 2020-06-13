from kivy.config import Config
Config.set('graphics','resizable',False)

from kivy.core.window import Window

from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from googletrans import Translator

from kivymd.theming import ThemeManager
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.button import MDRaisedButton

language_1 = ''
language_2 = ''

class P(FloatLayout):
    def En(self):
        global language_1
        language_1 = 'en'
        close_popup()

    def Ru(self):
        global language_1
        language_1 = 'ru'
        close_popup()

    def Fr(self):
        global language_1
        language_1 = 'fr'
        close_popup()

    def Tt(self):
        global language_1
        language_1 = 'tt'
        close_popup()


class P2(FloatLayout):
    def En2(self):
        global language_2
        language_2 = 'en'
        close_popup2()

    def Ru2(self):
        global language_2
        language_2 = 'ru'
        close_popup2()

    def Fr2(self):
        global language_2
        language_2 = 'fr'
        close_popup2()

    def Tt2(self):
        global language_2
        language_2 = 'tt'
        close_popup2()

translator = Translator()
class Enter(Widget):
    def translater(self):
        try:
            translated = translator.translate(self.lang_1.text,dest=language_2,src=language_1)
            self.lang_2.text = '{}'.format(translated.text)
        except TypeError:
            self.lang_2.text = 'You did not enter text'
    def btn(self):
        show_popup()
    def btn2(self):
        show_popup2()

def show_popup():
    show = P()
    global popup_window
    popup_window = Popup(title='Choose Language', content=show, size_hint=(None,None),size =(300,300))
    popup_window.open()

def show_popup2():
    show = P2()
    global popup_window2
    popup_window2 = Popup(title='Choose Language',content=show,size_hint=(None,None),size =(300,300))
    popup_window2.open()

def close_popup():
    popup_window.dismiss()
def close_popup2():
    popup_window2.dismiss()

class Translator(Screen):
    game = Enter()
    def on_enter(self):
        self.add_widget(self.game)

    def on_leave(self):
        self.clear_widgets()