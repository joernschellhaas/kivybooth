'''
kivybooth
=========

A photobooth application, intended to consist of a touch screen, a libgphoto2
compatible camera, and a printer connected via USB.

See README.md for details.

'''


import log, logging

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
from res.fontawesome import *
from base import *


logger = logging.getLogger("kb.main")


class KivyBoothApp(App):

    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(0)
    show_sourcecode = BooleanProperty(False)
    sourcecode = StringProperty()
    logged_in = False
    screen_names = []
    hierarchy = []
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
        logger.info("Application started")

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def go_to_screen(self, name: str, direction = Direction.FORWARD):
        logger.info("Going to screen '%s' in %s (%s)", name, direction, direction.to_graphical())
        print(type(direction), type(Direction.FORWARD))
        if direction is Direction.FORWARD:
            self.hierarchy.append(name)
        elif direction == Direction.REPLACE:
            self.hierarchy[-1] = name
        elif direction is Direction.BACK:
            if len(self.hierarchy) > 1:
                self.hierarchy.pop()
            while self.hierarchy[-1] != name and len(self.hierarchy) > 1:
                self.hierarchy.pop()
            name = self.hierarchy[-1]
        print("Hierarchy", self.hierarchy)
        sm = self.root.ids.sm
        sm.switch_to(self.screens[name], direction=direction.to_graphical())
        self.current_title = self.screens[name].name

    def go_hierarchy_previous(self):
        if len(self.hierarchy) > 1:
            self.go_to_screen(self.hierarchy[-2], Direction.BACK)

    def _update_clock(self, dt):
        self.time = time()


if __name__ == '__main__':
    KivyBoothApp().run()
