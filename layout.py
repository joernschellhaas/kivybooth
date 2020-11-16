from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.lang import Builder
import kivy.app


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


root = Builder.load_file('layout.kv')
app = kivy.app.App.get_running_app()
