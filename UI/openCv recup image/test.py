import numpy as np
import cv2
import os

def auto_crop_image(image, frame, vc):
    if image is not None:
        im = image.copy()
        # Load HaarCascade from the file with OpenCV
        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        
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
            height, width, channels = im.shape
            b_dim = min(max(w,h)*1.2,width, height)
            box = [center_x-b_dim/2, center_y-b_dim/2, center_x+b_dim/2, center_y+b_dim/2]
            box = [int(x) for x in box]
            # Crop Image
            if box[0] >= 0 and box[1] >= 0 and box[2] <= width and box[3] <= height:
                
                # cv2.imwrite(filename='saved_img.jpg', img=frame)
                vc.release()
                crpim = im[box[1]:box[3],box[0]:box[2]]
                crpim = cv2.resize(crpim, (224,224), interpolation = cv2.INTER_AREA)
                cv2.waitKey(1650)
                cv2.destroyAllWindows()
                print("Processing image...")
                gray = cv2.cvtColor(crpim, cv2.COLOR_BGR2GRAY)
                cv2.imwrite(filename='saved_img.jpg', img=crpim)
                img_resized = cv2.imwrite(filename='saved_img-final.jpg', img=gray)
                print("Image saved!")
                
                # crpim = im[box[1]:box[3],box[0]:box[2]]
                # crpim = cv2.resize(crpim, (224,224), interpolation = cv2.INTER_AREA)
                # print(crpim)
                # return crpim, image, (x, y, w, h)
    return None, image, (0,0,0,0)

def send_image_to_api():
    api_url = "http://127.0.0.1:5000/face"
    headers = {'content-type': 'image/jpeg'}

    img = cv2.imread('saved_img-final.jpg')
    response = requests.post(api_url, data=img.tostring(), headers=headers)

    print(json.loads(response.text))


def webcam_face_recognizer():
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)
    
    while vc.isOpened():
        _, frame = vc.read()
        img = frame
        # Image analysis (start here with img loaded with your image)
        # We do not want to detect a new identity while the program is in the process of identifying another person
        imgcrop,img, (x, y, w, h) = auto_crop_image(img, frame, vc)
        send_image_to_api()
 
        key = cv2.waitKey(1) & 0xff
        if key == 27: # exit on ESC
            break
    cv2.destroyWindow("preview")
    
webcam_face_recognizer()