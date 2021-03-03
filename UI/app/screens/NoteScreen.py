from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from kivy.network.urlrequest import UrlRequest

from datetime import date
import json

from conf.utils import *

class NoteScreen( Screen ):

    def __init__( self, **kwargs ):
        super( NoteScreen, self ).__init__( **kwargs )
        #View components binding.
        self.note_title = self.ids[ 'noteTitle' ]
        self.note_content = self.ids[ 'noteContent' ]

    def build( self, *args ):
        #Fill fields with selected note values.
        self.note_title.text = self.manager.selected_note[ 'title' ]
        self.note_content.text = self.manager.selected_note[ 'content' ]

    #API call
    def save_note( self ):
        #Set selected note values to new values.
        self.manager.selected_note[ 'title' ] = self.note_title.text
        self.manager.selected_note[ 'content' ] = self.note_content.text
        self.manager.selected_note[ 'updated' ] = date.today().strftime( "%Y-%m-%d" )

        if self.manager.selected_note[ 'title' ] != '' and self.manager.selected_note[ 'content' ] != '':
            body = json.dumps( self.manager.selected_note )
            headers = { 'Content-type': 'application/json', 'Accept': 'text/plain' }  #To do accept...

            #Update
            if self.manager.selected_note['id']:
                req = UrlRequest( base_url + 'updatenote',
                                  on_success = self.manager.display_dialog( 'note_updated' ),
                                  req_body = body,
                                  req_headers = headers,
                                  #on_error = self.manager.display_dialog('network_error')
                                )
            #Create
            else :
                req = UrlRequest( base_url + 'addnote',
                                  on_success = self.manager.display_dialog( 'note_created' ),
                                  req_body = body,
                                  req_headers = headers,
                                  #on_error = self.manager.display_dialog('network_error')
                                )
            self.return_to_list()

        else:
            self.manager.display_dialog( 'note_field_missing' )

    #API call
    def delete_note( self ) :
        req = UrlRequest( base_url + 'deletenote/' + str( self.manager.selected_note[ 'id' ] ),
                                  on_success = self.manager.display_dialog( 'note_created' ),
                                  req_body = body,
                                  req_headers = headers,
                                  #on_error = self.manager.display_dialog('network_error')
                        )

    def return_to_list( self ):
        #Redirection
        self.manager.current = 'main_screen'
        self.manager.transition.direction = 'right'