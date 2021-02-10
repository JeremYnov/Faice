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

class SM( ScreenManager ):
    user_id = 1    #To do -> rendre dynamique
    selected_note = {}  #Can be accessed from all screens

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

if __name__ == "__main__":
    MainApp().run()