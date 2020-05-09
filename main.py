'''
Showcase of Kivy Features
=========================

This showcases many features of Kivy. You should see a
menu bar across the top with a demonstration area below. The
first demonstration is the accordion layout. You can see, but not
edit, the kv language code for any screen by pressing the bug or
'show source' icon. Scroll through the demonstrations using the
left and right icons in the top right or selecting from the menu
bar.

The file showcase.kv describes the main container, while each demonstration
pane is described in a separate .kv file in the data/screens directory.
The image data/background.png provides the gradient background while the
icons in data/icon directory are used in the control bar. The file
data/faust_github.jpg is used in the Scatter pane. The icons are
from `http://www.gentleface.com/free_icon_set.html` and licensed as
Creative Commons - Attribution and Non-commercial Use Only; they
sell a commercial license.

The file android.txt is used to package the application for use with the
Kivy Launcher Android application. For Android devices, you can
copy/paste this directory into /sdcard/kivy/showcase on your Android device.

'''

from time import time
from kivy.app import App
import os.path
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
import glob


class ShowcaseScreen(Screen):
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(ShowcaseScreen, self).add_widget(*args)


class ShowcaseApp(App):

    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(0)
    show_sourcecode = BooleanProperty(False)
    sourcecode = StringProperty()
    screen_names = ListProperty([])
    hierarchy = ListProperty([])

    def build(self):
        self.title = 'Kivybooth'
        self.load_screens()
        self.go_to_screen("idle")
        Clock.schedule_interval(self._update_clock, 1 / 60.)

    def load_screens(self):
        self.screens = {}
        for fn in glob.glob(os.path.join(os.path.dirname(__file__), "res", "screens", "*.kv")):
            self.screens[os.path.splitext(os.path.split(fn)[1])[0]] = Builder.load_file(fn)

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def go_to_screen(self, name):
        sm = self.root.ids.sm
        sm.switch_to(self.screens[name], direction='right')
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
    ShowcaseApp().run()
