from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from kivymd.app import MDApp

from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog

from screens.FirstScreen import FirstScreen
from screens.LoginScreen import LoginScreen
from screens.NotesListScreen import NotesListScreen
from screens.NoteScreen import NoteScreen

from conf.utils import *

class MyScreenManager( ScreenManager ):
    user_id = 0    #To do -> rendre dynamique
    selected_note = {}  #Can be accessed from all screens

    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        self.add_widget(FirstScreen(name='first_screen'))
        self.add_widget(LoginScreen(name='login_screen'))
        self.add_widget(NotesListScreen(name='main_screen'))
        self.add_widget(NoteScreen(name='note_screen'))
    
    def build(self):
        self.add_widget(FirstScreen(name='first_screen'))

    def display_dialog( self, dialog_type ):

        if dialog_type in dialogs_dict.keys():
            self.dialog = MDDialog(
                title = 'Warning',
                text = dialogs_dict[ dialog_type ],
                buttons = [ MDRaisedButton(text="Ok") ]
            )
            self.dialog.open()


class MainApp( MDApp ):

    def build( self ):
        Window.size = window_size
        sm = MyScreenManager()
        return sm
        

if __name__ == "__main__":
    MainApp().run()