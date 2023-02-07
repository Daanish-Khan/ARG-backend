from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
import firebase_admin
from firebase_admin import firestore, credentials
import os
from random import randrange

# Init flask
app = Flask(__name__)
api = Api(app)
CORS(app, allow_headers=["Access-Control-Allow-Credentials"])

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

        # Get requested key from database
        key_ref = db.collection('keys').document(args['k'])
        key = key_ref.get()

        # Get active event
        event_ref = db.collection('events').document('CURRENTEVENT')
        event = event_ref.get()

        # Check if key to event matches active event
        if event.to_dict()['event'] != key.to_dict()['event']:
            return {'key': args['k'], 'valid': False}, 200

        # Returns key, validity, and what event the key triggers (if valid key)
        if key.exists:

            # Update current event
            event_ref.update({u'event': event.to_dict()['event'] + 1})

            return {'key': args['k'], 'valid': True, 'trigger': key.to_dict()['event']}, 200
        else:
             return {'key': args['k'], 'valid': False}, 200
        
    pass

# Event getter
class Event(Resource):

    def get(self):
        
        # Get event
        event_ref = db.collection('events').document('CURRENTEVENT')
        event = event_ref.get()

        return {'event': event.to_dict()['event']}, 200
    pass

# File getter
class File(Resource):

    def get(self):
        
        filePick = randrange(1, 8)
        imgStr = ""

        if filePick == 1:
            imgStr = "broken"
        elif filePick == 2:
            imgStr = "deity"
        elif filePick == 3:
            imgStr = "desolation"
        elif filePick == 4:
            imgStr = "despair"
        elif filePick == 5:
            imgStr = "destruction"
        elif filePick == 6:
            imgStr = "emergence"
        elif filePick == 7:
            imgStr = "fear"

        try:
            return send_file("/img/" + imgStr + ".mc", download_name=imgStr + ".mc")
        except Exception as e:
            return str(e)
    pass

# Add endpoints to api
api.add_resource(Key, '/key')
api.add_resource(Event, '/event')
api.add_resource(File, '/file')