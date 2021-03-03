from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
import cv2
import os
import requests 
import json
import base64

class LoginScreen( Screen ):

    def __init__( self, **kwargs ):
        super( LoginScreen, self ).__init__( **kwargs )
        self.cropped = False
        current_dir = os.getcwd()
        self.path = current_dir + '/face/'
        self.camera = self.ids[ 'camera' ]
        #Clock.schedule_interval(self.mainFace, 1)
        
    def mainFace(self):
        while self.cropped == False :
            self.camera.export_to_png('face_img.png')
            img = cv2.imread('face_img.png')
            self.autoCropImage( img )
            os.remove(os.path.join(os.getcwd(), 'face_img.png'))
        self.sendImageToApi()
        # os.remove(os.path.join(self.path,'saved_img-final.jpg'))
        # os.remove(os.path.join(self.path,'saved_img.jpg'))
            
    def sendImageToApi(self):
        api_url = 'http://127.0.0.1:5000/face'
        imgPath = self.path + 'saved_img-final.jpg'
        with open(imgPath, 'rb') as image_file:
            response = requests.request( 'POST', api_url, files = { "img" : image_file } )
        return print(response.text)  

    def autoCropImage( self, image ):
        if image is not None:
            print(type(image))
            im = image.copy()
            print(im.shape)
            # Load HaarCascade from the file with OpenCV
            faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
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
            if len(faces) > 0:
                # Draw a rectangle around the faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)        
                (x, y, w, h) = faces[0]
                center_x = x+w/2
                center_y = y+h/2
                height, width = im.shape[0], im.shape[1]
                b_dim = min(max(w,h)*1.2,width, height)
                box = [center_x-b_dim/2, center_y-b_dim/2, center_x+b_dim/2, center_y+b_dim/2]
                box = [int(x) for x in box]
                # Crop Image
                if box[0] >= 0 and box[1] >= 0 and box[2] <= width and box[3] <= height:
                    # cv2.imwrite(filename='saved_img.jpg', img=frame)
                    crpim = im[box[1]:box[3],box[0]:box[2]]
                    crpim = cv2.resize(crpim, (224,224), interpolation = cv2.INTER_AREA)
                    cv2.waitKey(1650)
                    cv2.destroyAllWindows()
                    gray = cv2.cvtColor(crpim, cv2.COLOR_BGR2GRAY)
                    # # Aller dans le bon directory
                    cv2.imwrite(os.path.join(self.path,'saved_img.jpg'), img=crpim)
                    cv2.imwrite(os.path.join(self.path,'saved_img-final.jpg'), img=gray)
                    self.cropped = True

    def redirectWithoutLogin( self ):
        #Redirection
        self.manager.current = 'main_screen'
        self.manager.transition.direction = 'down'