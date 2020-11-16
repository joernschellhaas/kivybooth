from layout import *
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty, ObjectProperty
import kivy.app
from kivy.clock import Clock
from kivy.lang import Builder
import glob
import os.path

import image
import light


def load():
    screens = {}
    for fn in glob.glob(os.path.join(os.path.dirname(__file__), "res", "screens", "*.kv")):
        root = Builder.load_file(fn)
        screens[os.path.splitext(os.path.split(fn)[1])[0]] = root
    return screens


class CountdownScreen(KBScreen):
    def on_pre_enter(self, *args):
        self.ids.counter_widget.text = "3"
    def on_enter(self, *args):
        self.counter = Clock.schedule_interval(self.count, 1)
        light.set_brightness(0.5)
    def count(self, dt):
        count = int(self.ids.counter_widget.text) - 1
        self.ids.counter_widget.text = str(count)
        if count == 1:
            light.set_brightness(1)
        if count == 0:
            self.counter.cancel()
            Clock.schedule_once(self.capture)
    def capture(self, dt):
        app.last_photo = app.camera.capture()
        app.go_to_screen("review")
    def on_pre_leave(self, *args):
        self.counter.cancel()
        light.set_brightness(0)

class ReviewScreen(KBScreen):
    def on_pre_enter(self, *args):
        # We need to create a thumbnail because the original image is too big
        # for Kivy to handle it
        self.ids.photo.source = image.thumbnail(app.last_photo)
        self.ids.photo.reload()

class LoginScreen(KBScreen):
    def on_enter(self, *args):
        self.ids.password.focus = True
