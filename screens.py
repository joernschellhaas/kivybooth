from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty, ObjectProperty
import kivy.app
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget


def app():
    return kivy.app.App.get_running_app()


class KBScreen(Screen):
    fullscreen = BooleanProperty(False)
    keyboard = BooleanProperty(False)
    def add_widget(self, *args):
        if 'content' in self.ids:
            print("Delegating addition of widget to screen")
            return self.ids.content.add_widget(*args)
        return super().add_widget(*args)
    def on_pre_enter(self, *args, **kwargs):
        super().on_pre_enter(*args, **kwargs)
        if self.keyboard:
            self.ids.kbd_placeholder.height = 300

class AdaptiveBoxLayout(BoxLayout):
    def add_widget(self, *args):
        print("Wrapping addition of widget to AdaptiveBoxLayout")
        wrapper = AnchorLayout()
        super().add_widget(wrapper)
        wrapper.add_widget(*args)


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
            app().go_to_screen("idle")
    def on_pre_leave(self, *args):
        self.counter.cancel()

class LoginScreen(KBScreen):
    def on_enter(self, *args):
        self.ids.password.focus = True
