# Libraries
from layout import *
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty, ObjectProperty
import kivy.app
from kivy.clock import Clock
from kivy.lang import Builder
import glob
import os.path

# Application modules
import image
import light
import printer
from base import Direction


def load():
    screens = {}
    for fn in glob.glob(os.path.join(os.path.dirname(__file__), "res", "screens", "*.kv")):
        root = Builder.load_file(fn)
        screens[os.path.splitext(os.path.split(fn)[1])[0]] = root
    return screens


class CountdownScreen(KBScreen):
    def on_pre_enter(self, *args):
        self.ids.counter_widget.text = "10"
    def on_enter(self, *args):
        self.counter = Clock.schedule_interval(self.count, 1)
        light.set_brightness(0.5)
    def count(self, dt):
        count = int(self.ids.counter_widget.text) - 1
        self.ids.counter_widget.text = str(count)
        if count <= 1:
            light.set_brightness(1)
        if count == 0:
            self.counter.cancel()
            Clock.schedule_once(self.capture)
    def capture(self, dt):
        app.last_photo = app.camera.capture()
        light.set_brightness(0)
        app.go_to_screen("review", Direction.REPLACE)
    def on_pre_leave(self, *args):
        self.counter.cancel()
        light.set_brightness(0)

class ReviewScreen(KBScreen):
    def on_pre_enter(self, *args):
        # We need to create a thumbnail because the original image is too big
        # for Kivy to handle it
        self.thumbnail = image.Thumbnail(app.last_photo.path)
        self.ids.photo.source = self.thumbnail.path
        self.ids.photo.reload()
        app.store_job = app.last_photo.start_store()
    def on_pre_leave(self, *args):
        pass
        #app.last_photo.do_store = self.ids.store_allowed.active

class RefillScreen(KBScreen):
    def on_enter(self, *args):
        self.updater = Clock.schedule_interval(self.update, 0.5)
        self.runtime = 0
    def update(self, dt):
        status, _ = app.print_job.status()
        if status != printer.JobStatus.NEED_MAINTENANCE:
            app.go_to_screen("printing", Direction.REPLACE)
    def on_pre_leave(self, *args):
        self.updater.cancel()

class PrintingScreen(KBScreen):
    def on_enter(self, *args):
        self.updater = Clock.schedule_interval(self.update, 0.5)
        self.runtime = 0
    def on_pre_leave(self, *args):
        self.updater.cancel()
        #for job in self.jobs:
        #    job.cancel()
    def update(self, dt):
        self.runtime += dt
        job = app.print_job
        status, progress = job.status()
        if status == printer.JobStatus.NEED_MAINTENANCE:
            app.go_to_screen("refill")
        elif status in [printer.JobStatus.DONE, printer.JobStatus.FAILED, printer.JobStatus.CANCELED]:
            self.leave()
        self.ids.progress_bar.value = progress
    def cancel(self):
        self.leave()
    def leave(self):
        self.updater.cancel()
        Clock.schedule_once(lambda dt: app.go_to_screen("idle", Direction.REPLACE), 3)
        
class LoginScreen(KBScreen):
    def on_enter(self, *args):
        self.ids.password.focus = True

class AdminScreen(KBScreen):
    def on_pre_enter(self, *args):
        config = {"foo": True, "bar": False}
        for key, value in enumerate(config):
            self.ids.config.add_widget(ConfigBool())
