from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window

import time

from kivymd.uix.list import OneLineListItem
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivymd.app import MDApp


class SM(ScreenManager):
    note_id = StringProperty()  #Can be accessed from all screen

class MainScreen(Screen):
    pass


class LoginScreen(Screen):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.build)

    def build(self, *args):  #Parameters: self and another one wich should be the instance calling this method
        self.camera = self.ids["camera"]

    def capture(self):
        timestr = time.strftime("%Y%m%d_%H%M%S")
        self.camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")


class NotesListScreen(Screen):

    def __init__(self, **kwargs):
        super(NotesListScreen, self).__init__(**kwargs)
        self.note_id = 0
        Clock.schedule_once(self.build)

    def build(self, *args):
        self.container = self.ids["notes_list"]

        for i in range(21):
            self.container.add_widget(
                OneLineListItem(id=str(i), text=f"Single-line item {i}", on_release=lambda x:self.redirect(note_id = str(i)) )
            )

    def redirect(self, *args, note_id):  #def redirect(self, OneLineIconListItem, id):
        self.manager.note_id = str(note_id)
        self.manager.current = 'note'


class NoteScreen(Screen):

    def __init__(self, **kwargs):
        super(NoteScreen, self).__init__(**kwargs)

    def build(self, *args):
        self.id = self.manager.note_id
        self.note_field = self.ids["noteField"]
        print(self.id)
        self.note_field.text = self.id

# class NotesListScreen(Screen):

#     def __init__(self, **kwargs):
#         super(NotesListScreen, self).__init__(**kwargs)
#         self.note_id = 0
#         Clock.schedule_once(self.build)

#     def build(self, *args):
#         self.container = self.ids["notes_list"]

#         for i in range(21):
#             self.container.add_widget(
#                 OneLineListItem(id=str(i), text=f"Single-line item {i}", on_press=lambda x:self.redirect(self) )
#             )

#     def redirect(self, instance):  #def redirect(self, OneLineIconListItem, id):
#         print(instance.id)
#         self.manager.note_id = 'heelo'
#         self.manager.current = 'note'


# class NoteScreen(Screen):

#     def __init__(self, **kwargs):
#         super(NoteScreen, self).__init__(**kwargs)

#     def build(self, *args):
#         self.id = self.manager.note_id
#         self.note_field = self.ids["noteField"]
#         print(self.id)
#         self.note_field.text = self.id
class MainApp(MDApp):

    def build(self):
        Window.size = (960, 540)

if __name__ == "__main__":
    MainApp().run()