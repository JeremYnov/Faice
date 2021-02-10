# Imports
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from datetime import datetime
import os
import base64

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
        current_dir = os.getcwd();
        path = current_dir + "\\faces\\"
        img = request.files['image']
        img.save(path + 'test.jpg')
        response = {'message':'image received'}
        return response

        # LA SUITE !!!!
        # # Query the User
        # user = User.query.filter_by(facialChain=facialChain).first()
        # # if user doesn't exist, create a new user
        # if user is None :
        #     newUser = User(facialChain=facialChain)
        #     db.session.add(newUser)
        #     db.session.commit()
        #     user = User.query.filter_by(facialChain=facialChain).first()
        # # Query the notes of the user
        # userNotes = Note.query.filter_by(user_id=user.id).all()
        # # If no notes, return a statement
        # if not userNotes :
        #     return jsonify('You don\'t have any notes for now... Start noting')
        # # Else return notes
        # return jsonify(notes=[note.serialize() for note in userNotes])

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

class B64(Resource):
    def post(self):
        # Aller dans le bon directory
        current_dir = os.getcwd();
        path = current_dir + "\\faces\\"
        file = request.body()
        file = base64.b64decode(file)
        file.save(path + 'test.jpg')
        response = {'message':'image received'}
        return response

api.add_resource(FaceApi, "/face")
api.add_resource(GetNote, "/getnote/<int:user_id>")
api.add_resource(AddNote, "/addnote")
api.add_resource(UpdateNote, "/updatenote")
api.add_resource(DeleteNote, "/deletenote/<int:note>")
api.add_resource(B64, "/face64")

if __name__ == "__main__":
    app.run(debug=True)