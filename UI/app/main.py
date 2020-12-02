from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window

from kivymd.app import MDApp

class SM(ScreenManager):
    pass


class MainScreen(Screen):

    def build(self):
        self.window_sizes = Window.size
        return

# sm = ScreenManager()
# sm.add_widget(MainScreen(name='main'))
# sm.add_widget(LoginScreen(name='login'))

class MainApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"  # "Light"
        self.theme_cls.primary_palette = "Green"  # "Purple", "Red"

        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")
        return


if __name__ == "__main__":
    MainApp().run()