# Imports
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from datetime import datetime
import os

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
    def get(self):
        return {'message': 'pas de methode get'}
    
    def post(self):   
         
        # Aller dans le bon directory
        current_dir = os.getcwd();
        path = current_dir + "\\faces\\"
        file = request.files['image']
        file.save(path + 'test.jpg')
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

class AddNote(Resource):
    def get(self, title, content, user_id):
        newNote = Note(title=title, content=content, user_id=user_id)
        db.session.add(newNote)
        db.session.commit()
        return jsonify("200")

class UpdateNote(Resource):
    def get(self, note, title, content, user_id):
        # Query note and delete it
        oldNote = Note.query.filter_by(id=note).first()
        db.session.delete(oldNote)
        # Add updated note to query
        newNote = Note(title=title, content=content, user_id=user_id)
        db.session.add(newNote)
        db.session.commit()
        return jsonify("200")

class DeleteNote(Resource):
    def get(self, note):
        oldNote = Note.query.filter_by(id=note).first()
        db.session.delete(oldNote)
        db.session.commit()
        return jsonify("200")

api.add_resource(FaceApi, "/face")
api.add_resource(AddNote, "/addnote/<string:title>/<string:content>/<int:user_id>")
api.add_resource(UpdateNote, "/updatenote/<int:note>/<string:title>/<string:content>/<int:user_id>")
api.add_resource(DeleteNote, "/deletenote/<int:note>")

if __name__ == "__main__":
    app.run(debug=True)