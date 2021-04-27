# Imports API
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from datetime import datetime
import os
import json
# # Imports IA
from matplotlib import pyplot
from numpy import asarray
from scipy.spatial.distance import cosine
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input
import numpy as np
from PIL import Image
from mtcnn.mtcnn import MTCNN


# Initiate APP
app = Flask(__name__)
# Initiate API
api = Api(app)
# Initiate DB
# to create and update DB :
# flask db init flask db migrate flask db upgrade
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/ydays2020'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# DB tables creation and serialization for json responses
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(60), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)
    def serialize(self):
        return {
            'id':self.id,
            'image_url': self.image_url,
            'created': self.created
        }

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500))
    updated = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def serialize(self):
        return {
            'id' : self.id,
            'title': self.title,
            'content': self.content,
            'updated': self.updated,
            'user_id': self.user_id
        }

# API routes creation
class FaceApi(Resource):
    def post(self):
        # Aller dans le bon directory
        current_dir = os.getcwd()
        path = os.path.join(current_dir, 'API', 'faces','')
        # path = current_dir + "\\API\\faces\\"
        img = request.files['img']
        date = str(datetime.now()).replace(' ','').replace('-','').replace('.','').replace(':','')
        imgPath = path +date+'.jpg'
        # Save image in folder faces
        img.save(imgPath)
        
        #Fetch la DB, tranform en array et append a faces
        # filenames = ['/API'+user.image_url for user in User.query.all()]
        filenames = []
        for user in User.query.all():
            filenames.append(user.image_url)
            
        faceToAnalysis = date+'.jpg'
        
        filenames.insert(0,faceToAnalysis)
        
        embeddings = get_embeddings(filenames)
        user = None
        
        for i in range(len(embeddings)):
            if i != 0:
                matching = is_match(embeddings[0],embeddings[i])
                if matching:
                    print("=====FACE IS RECOGNIZE=====")
                    matchingUser = filenames[i]
                    os.remove(imgPath)
                    user = User.query.filter_by(image_url=matchingUser).first()
                    break                   
        if user == None:
            print('=====FACE IS NOT RECOGNIZE=====')
            datePath = date + ".jpg"
            print("=====CREATION OF NEW USER=====")
            newUser = User(image_url = datePath)
            db.session.add(newUser)
            db.session.commit()
            user = User.query.filter_by(image_url=datePath).first()
            
        return jsonify(user.serialize())


def extract_face(filename, required_size=(224, 224)):
    # load image from file
    pixels = pyplot.imread(os.path.join(os.getcwd(),'API','faces',filename))
    
    # create the detector, using default weights
    detector = MTCNN()
    
    # detect faces in the image
    results = detector.detect_faces(pixels)
    
    # extract the bounding box from the first face
    x1, y1, width, height = results[0]['box']
    x2, y2 = x1 + width, y1 + height
    
    # extract the face
    face = pixels[y1:y2, x1:x2]
    
    # resize pixels to the model size
    image = Image.fromarray(face)
    image = image.resize(required_size)
    
    # Transform our image in array 
    face_array = asarray(image)
    
    # get shape and type
    array_shape = face_array.shape
    array_data_type = face_array.dtype.name
    
    # converting to string
    face_array_str = face_array.tostring()
    # TODO => Push this str in database
    
    # converting back to numpy array
    # TODO => Converting back our str in array
    new_arr = np.frombuffer(face_array_str, dtype=array_data_type).reshape(array_shape)
    return face_array

# extract faces and calculate face embeddings for a list of photo files


def get_embeddings(filenames):
    # extract faces
    faces = [extract_face(f) for f in filenames]

    # convert into an array of samples
    samples = asarray(faces, 'float32')

    # prepare the face for the model, e.g. center pixels
    samples = preprocess_input(samples, version=2)

    # create a vggface model
    model = VGGFace(model='resnet50', include_top=False,
                    input_shape=(224, 224, 3), pooling='avg')

    # perform prediction
    yhat = model.predict(samples)

    return yhat



# determine if a candidate face is a match for a known face
def is_match(known_embedding, candidate_embedding, thresh=0.5):
    # calculate distance between embeddings
    score = cosine(known_embedding, candidate_embedding)
    if score <= thresh:
        print('>face is a Match (%.3f <= %.3f)' % (score, thresh))
        return True
    else:
        print('>face is NOT a Match (%.3f > %.3f)' % (score, thresh))
        return False
            

class GetNote(Resource):
    def get(self, user_id):
        userNotes = Note.query.filter_by(user_id=user_id).all()
        return jsonify(notes=[note.serialize() for note in userNotes])

class AddNote(Resource):
    def post(self):
        req = request.json
        newNote = Note(title=req['title'], content=req['content'], updated=req['updated'], user_id=req['user_id'])
        db.session.add(newNote)
        db.session.commit()
        return jsonify("200")

class UpdateNote(Resource):
    def post(self):
        req = request.json
        updatedNote = Note.query.filter_by(id=req['id']).first()
        updatedNote.title=req['title']
        updatedNote.content=req['content']
        updatedNote.updated=req['updated']
        db.session.commit()
        return jsonify("200")

class DeleteNote(Resource):
    def get(self, note):
        oldNote = Note.query.filter_by(id=note).first()
        db.session.delete(oldNote)
        db.session.commit()
        return jsonify("200")

api.add_resource(FaceApi, "/face")
api.add_resource(GetNote, "/getnote/<int:user_id>")
api.add_resource(AddNote, "/addnote")
api.add_resource(UpdateNote, "/updatenote")
api.add_resource(DeleteNote, "/deletenote/<int:note>")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')