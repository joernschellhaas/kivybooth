'''
kivybooth
=========

A photobooth application, intended to consist of a touch screen, a libgphoto2
compatible camera, and a printer connected via USB.

See README.md for details.

'''

# Libraries
from time import time
from kivy.app import App
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
import kivysome
from kivy.config import Config
import os.path

# Modules
import camera


class KivyBoothApp(App):

    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(0)
    show_sourcecode = BooleanProperty(False)
    sourcecode = StringProperty()
    screen_names = ListProperty([])
    hierarchy = ListProperty([])
    last_photo = "res/background.png"

    def build(self):
        # Late loading of application modules - otherwise, they would not find the app instance
        import screens
        import layout
        self.title = 'KivyBooth'
        self.screens = screens.load()
        self.camera = camera.Camera()
        self.root = layout.root
        self.go_to_screen("idle")
        Clock.schedule_interval(self._update_clock, 1 / 60.)

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def go_to_screen(self, name, direction='left'):
        sm = self.root.ids.sm
        sm.switch_to(self.screens[name], direction=direction)
        self.current_title = self.screens[name].name

    def go_hierarchy_previous(self):
        ahr = self.hierarchy
        if len(ahr) == 1:
            return
        if ahr:
            ahr.pop()
        if ahr:
            idx = ahr.pop()
            self.go_screen(idx)

    def _update_clock(self, dt):
        self.time = time()


if __name__ == '__main__':
    kivysome.enable("https://kit.fontawesome.com/58bcf53674.js",
    font_folder=os.path.join(os.path.dirname(__file__), "venv", "lib", "fonts"),
    cached=True,
    group=kivysome.FontGroup.SOLID)
    KivyBoothApp().run()
