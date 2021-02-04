from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
import time

class LoginScreen( Screen ):

    def __init__( self, **kwargs ):
        super( LoginScreen, self ).__init__( **kwargs )
        Clock.schedule_once( self.build )

    def build( self, *args ):  #Parameters: self and another one wich should be the instance calling this method
        self.camera = self.ids[ "camera" ]
        self.redirectWithoutLogin()

    def capture(self):
        timestr = time.strftime( "%Y%m%d_%H%M%S" )
        self.camera.export_to_png( "IMG_{}.png".format( timestr ) )
        print( "Captured" )

    def redirectWithoutLogin( self ):
        #Redirection
        self.manager.current = 'notes'
        self.manager.transition.direction = 'down'