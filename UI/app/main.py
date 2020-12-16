from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window

import time

from kivymd.app import MDApp

class SM(ScreenManager):
    pass


class MainScreen(Screen):
    pass

class LoginScreen(Screen):

    def build(self):
        self.camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        self.camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")


class NotesScreen(Screen):
    pass

class MainApp(MDApp):

    def build(self):
        Window.size = (960, 540)


if __name__ == "__main__":
    MainApp().run()