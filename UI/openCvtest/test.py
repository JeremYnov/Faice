import cv2
import os
import requests
import json
import base64


def auto_crop_image(image, vc):
    print("==================ENTER IN AUTOCROPIMAGE=======================")
    print(image)
    if image is not None:
        im = image.copy()
        # Load HaarCascade from the file with OpenCV
        faceCascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

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
            # # Aller dans le bon directory
            current_dir = os.getcwd()
            path  = os.path.join(current_dir,'UI','openCVtest','face','')
            # path = current_dir + "\\UI\\openCVtest\\face\\"
            cv2.imwrite(os.path.join(path, 'saved_img.jpg'), img=im)
    print("==================RETURN IN AUTOCROPIMAGE=======================")
    return


def send_image_to_api():
    api_url = "http://127.0.0.1:5000/face"
    current_dir = os.getcwd()
    path  = os.path.join(current_dir,'UI','openCVtest','face','')
    # path = current_dir + "\\UI\\openCVtest\\face\\"
    imgPath = path + "saved_img.jpg"

    with open(imgPath, "rb") as image_file:
        print("==== REQUEST TO API =====")
        response = requests.request('POST', api_url, files={"img": image_file})
        print(response.text)




def webcam_face_recognizer():
    vc = cv2.VideoCapture(0)

    while vc.isOpened():
        _, frame = vc.read()
        if not _:
            print("failed to grab frame")
            break
        else:
            auto_crop_image(frame, vc)
            send_image_to_api()
            current_dir = os.getcwd()
            print(current_dir)
            # path = current_dir + "\\UI\\openCVtest\\face\\"
            path  = os.path.join(current_dir,'UI','openCVtest','face','')
            break


webcam_face_recognizer()
