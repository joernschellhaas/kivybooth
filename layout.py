from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.lang import Builder
import kivy.app
from kivysome import icon


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
    def add_widget(self, widget, index=0, canvas=None):
        print("Wrapping addition of widget to AdaptiveBoxLayout")
        wrapper = AnchorLayout()
        super().add_widget(wrapper)
        wrapper.add_widget(widget, index, canvas)
        wrapper.size_hint = widget.size_hint

class KBButton(Button):
    pass

class KBIconButton(KBButton):
    icon = StringProperty("")
    text = StringProperty("")
    def on_kv_post(self, base_widget):
        self.text = "{} {}".format(icon(self.icon), self.text)
        super().on_kv_post(base_widget)


root = Builder.load_file('layout.kv')
app = kivy.app.App.get_running_app()
