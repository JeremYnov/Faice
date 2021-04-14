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


# Initiate APP
app = Flask(__name__)
# Initiate API
api = Api(app)
# Initiate DB
# to create and update DB :
# flask db init flask db migrate flask db upgrade
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@db:3306/ydays2020'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# DB tables creation and serialization for json responses
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facialChain = db.Column(db.String(60), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)

    def serialize(self):
        return {
            'facialChain': self.facialChain,
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
        path = current_dir + "\\faces\\"
        img = request.files['img']
        imgPath = path + 'test.jpg'
        img.save(imgPath)
        self.array_shape = None
        self.array_data_type = None
        # get embeddings file filenames
        embeddings = self.get_embeddings(imgPath)
        
        # define face to verify if known in our database
        faceToAnalysis = embeddings[0]
        print("=====THIS IS MY FACE TO ANALYSIS=====")
        print(faceToAnalysis)
        
        #Fetch la DB, tranform en array et append a faces
        users = User.query.all()
        for user in users :
            tempArray = user.facialChain
            # tempArray = tempArray.encode()
            tempArray = np.frombuffer(tempArray, dtype=self.array_data_type).reshape(self.array_shape)
            # embeddings.append(tempArray)
            np.concatenate((embeddings,tempArray))
        np.delete(embeddings,0,0)
        for embedding in embeddings :
            result = self.is_match(faceToAnalysis, embedding)
            print(result)
            break
        print("======================ENTERING IN IF CONDITION==================================")
        if result is None :
            user_array = faceToAnalysis.tostring()
            # user_array = str(user_array, 'utf-8')
            insert = User(facialChain = user_array)
            db.session.add(insert)
            db.session.commit()
            user = User.query.filter_by(facialChain = user_array).first()
            print("==== IF RESULT IS NONE =====")
            print(type(user))
        else :
            user_array = result.tostring()
            # user_array = str(user_array, 'utf-8')
            user = User.query.filter_by(facialChain = user_array).first()
            print("==== IF RESULT IS NOT NONE =====")
            print(type(user))
            
        print('=====TEST=====')
        print(type(user))
        return json.dumps(user.id)

    def face_as_array(self, filename):
        # load image from file
        image = pyplot.imread(filename)
        # Transform our image in array 
        face_array = asarray(image)
        
        return face_array

    def get_embeddings(self, path):
        # extract faces and calculate face embeddings for a list of photo files
        # Transform filenames in path
        # extract faces
        faces = [self.face_as_array(path)]  # faces[0] = user wanted to be identified
        # convert into an array of samples
        samples = asarray(faces, 'float32')
        # prepare the face for the model, e.g. center pixels
        samples = preprocess_input(samples, version=2)
        # create a vggface model
        model = VGGFace(model='resnet50', include_top=False,
                        input_shape=(224, 224, 3), pooling='avg')
        # perform prediction
        yhat = model.predict(samples)
        
        # get shape and type
        self.array_shape = yhat.shape
        self.array_data_type = yhat.dtype.name
        
        return yhat

    # determine if a candidate face is a match for a known face
    def is_match(self, known_embedding, candidate_embedding, thresh=0.5):
        # calculate distance between embeddings
        score = cosine(known_embedding, candidate_embedding)
        if score <= thresh:
            print('>face is a Match (%.3f <= %.3f)' % (score, thresh))
            # print("=====THIS IS MY CANDIDATE EMBEDDING=====")
            # print(candidate_embedding)
            return candidate_embedding
        # Todo remove ELSE When checked
        else:
            print('>face is NOT a Match (%.3f > %.3f)' % (score, thresh))
            return None

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