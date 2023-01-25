from flask import Flask, request
from flask_restful import Resource, Api
import firebase_admin
from firebase_admin import firestore, credentials
import os

# Init flask
app = Flask(__name__)
api = Api(app)

# Firestore auth ---- CREDS INCLUDED IN GITIGNORE ---- DO NOT UPLOAD TO BRANCH 
cred_path = os.getcwd() + '/creds.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path
cred = credentials.Certificate(cred_path)

fb = firebase_admin.initialize_app()
db = firestore.client()

# Key validation
class Key(Resource):
    def get(self):
        args = request.args

        # Check if key exists
        doc_ref = db.collection('keys').document(args['k'])
        doc = doc_ref.get()

        if doc.exists:
            return {'key': args['k'], 'validity': True}, 200
        else:
             return {'key': args['k'], 'validity': False}, 200
        
    pass

# Add endpoints to api
api.add_resource(Key, '/key')

if __name__ == '__main__':
    app.run()