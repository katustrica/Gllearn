import webbrowser

from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image


class About(Screen):
    def open_url(self, instance, url):
        webbrowser.open(url)
