import os
import sys
import traceback

from gllearn import Gllearn

import kivy
from kivymd.theming import ThemeManager


NICK_NAME_AND_NAME_REPOSITORY = 'https://github.com/katustrica/Gllearn'

directory = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.join(directory, 'libs/applibs'))

try:
    from kivy.config import Config
    Config.set('kivy', 'keyboard_mode', 'system')
    Config.set('kivy', 'log_enable', 0)
except Exception:
    traceback.print_exc(file=open(os.path.join(directory, 'error.log'), 'w'))
    print(traceback.print_exc())
    sys.exit(1)

def main():
    app = None

    try:
        app = Gllearn()
        app.run()
    except Exception:
        from kivy.app import App
        from kivy.uix.boxlayout import BoxLayout

        traceback.print_exc(file=open(os.path.join(directory, 'error.log'), 'w'))
        print(traceback.print_exc())

        if app:
            try:
                app.stop()
            except AttributeError:
                app = None
                traceback.print_exc(file=open(os.path.join(directory, 'error.log'), 'w'))
                print(traceback.print_exc())



if __name__ in ('__main__', '__android__'):
    main()
