from kivy.uix.screenmanager import Screen
import cv2
import os
import requests 
import json
import base64

class LoginScreen( Screen ):

    def __init__( self, **kwargs ):
        super( LoginScreen, self ).__init__( **kwargs )
        
    def mainFace(self):
        current_dir = os.getcwd()
        vc = cv2.VideoCapture(0)
        while vc.isOpened():
            _, frame = vc.read()
            if not _:
                print("failed to grab frame")
                break
            else:
                self.autoCropImage(frame, vc)
                self.sendImageToApi()
                break
            
    def sendImageToApi(self):
        api_url = 'http://127.0.0.1:5000/face'
        current_dir = os.getcwd()
        imgPath = os.path.join(current_dir,'UI','app','face','saved_img.jpg')
        with open(imgPath, 'rb') as image_file:
            response = requests.request( 'POST', api_url, files = { "img" : image_file } ).json()
            if response['id']:
                self.manager.user_id = response['id']
                self.manager.current = 'main_screen'
                self.manager.transition.direction = 'down'
        

    def autoCropImage( self, image, vc ):
        print("ENTERING IN IF IMAGE IS NOT NONE")
        if image is not None:
            im = image.copy()
            # Load HaarCascade from the file with OpenCV
            faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')
            # Read the image
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Detect faces in the image
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            faces = faceCascade.detectMultiScale(gray, 1.2, 5)
            print(faces)
            if len(faces) > 0:
                print("IN LEN FACE > 0")
                # # Aller dans le bon directory
                current_dir = os.getcwd()
                path  = os.path.join(current_dir,'UI','app','face','')
                cv2.imwrite(os.path.join(path, 'saved_img.jpg'), img=im)
        

    def redirectWithoutLogin( self ):
        #Redirection
        self.manager.current = 'main_screen'
        self.manager.transition.direction = 'down'