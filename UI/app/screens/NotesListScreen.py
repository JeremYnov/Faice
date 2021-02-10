from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from kivy.network.urlrequest import UrlRequest

from kivymd.uix.list import ThreeLineListItem

from conf.utils import *

class NotesListScreen( Screen ):

    def __init__( self, **kwargs ):
        super( NotesListScreen, self ).__init__( **kwargs )
        Clock.schedule_once( self.build )

    def build( self, *args ):
        #View components binding.
        self.notes_container = self.ids[ "notesContainer" ]
        self.spinner = self.ids[ "spinner" ]

    #API call
    def get_notes( self ):
        self.spinner.active = True
        self.notes_container.clear_widgets()
        self.request = UrlRequest( base_url + 'getnote/' + str(self.manager.user_id),
                                   on_success = self.display_notes,
                                   #on_error = self.manager.display_dialog('network_error')
                                 )

    def display_notes( self, *args ):
        self.spinner.active = False

        if self.request.result[ 'notes' ]:
            for note in self.request.result[ 'notes' ]:
                self.notes_container.add_widget(
                    ThreeLineListItem(
                        id = str( note[ 'id' ] ),
                        text = note[ 'title' ],
                        secondary_text = note[ 'content' ],
                        tertiary_text = note[ 'updated' ],
                        on_press=self.note_details
                    )
                )
        else:
            self.manager.display_dialog( 'empty_notes_list' )

    def note_details( self, instance ):
        self.manager.selected_note = {
            'id' : instance.id,
            'title' : instance.text,
            'content' : instance.secondary_text,
            'updated' : instance.tertiary_text,
            'user_id' : self.manager.user_id
        }
        #Redirection
        self.manager.current = 'note'
        self.manager.transition.direction = 'left'

    def create_note( self ):
        self.manager.selected_note = {
            'id' : None,
            'title' : '',
            'content' : '',
            'updated' : '',
            'user_id' : self.manager.user_id
        }
        #Redirection
        self.manager.current = 'note'
        self.manager.transition.direction = 'left'