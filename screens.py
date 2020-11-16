from layout import *
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty, ObjectProperty
import kivy.app
from kivy.clock import Clock
from kivy.lang import Builder
import glob
import os.path


def load():
    screens = {}
    for fn in glob.glob(os.path.join(os.path.dirname(__file__), "res", "screens", "*.kv")):
        root = Builder.load_file(fn)
        screens[os.path.splitext(os.path.split(fn)[1])[0]] = root
    return screens


class CountdownScreen(KBScreen):
    counter_widget = ObjectProperty()
    def on_pre_enter(self, *args):
        self.ids.counter_widget.text = "3"
    def on_enter(self, *args):
        self.counter = Clock.schedule_interval(self.count, 1)
    def count(self, dt):
        count = int(self.ids.counter_widget.text) - 1
        self.ids.counter_widget.text = str(count)
        if count == 0:
            app.go_to_screen("idle")
    def on_pre_leave(self, *args):
        self.counter.cancel()

class LoginScreen(KBScreen):
    def on_enter(self, *args):
        self.ids.password.focus = True
