from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
import firebase_admin
from firebase_admin import firestore, credentials
import os

# Init flask
app = Flask(__name__)
api = Api(app)
CORS(app)

# Firestore auth ---- CREDS INCLUDED IN GITIGNORE ---- DO NOT UPLOAD TO BRANCH 
cred_path = os.getcwd() + '/creds.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path
cred = credentials.Certificate(cred_path)

fb = firebase_admin.initialize_app()
db = firestore.client()

# Key validation
class Key(Resource):
    @cross_origin
    def get(self):
        args = request.args

        # Check if key exists
        doc_ref = db.collection('keys').document(args['k'])
        doc = doc_ref.get()

        # Returns key, validity, and what event the key triggers (if valid key)
        if doc.exists:
            resp = Flask.jsonify({'key': args['k'], 'valid': True, 'trigger': doc.to_dict()['return']})
            resp.headers.add('Access-Control-Allow-Origin', '*')
            return resp
        else:
            resp = Flask.jsonify({'key': args['k'], 'valid': False})
            resp.headers.add('Access-Control-Allow-Origin', '*')
            return resp
        
    pass

# Add endpoints to api
api.add_resource(Key, '/key')