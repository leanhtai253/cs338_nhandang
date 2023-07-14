from flask_restful import Resource
from firebase.firebaseApp import FirebaseApp
class Hello(Resource):
    fb = FirebaseApp()
    def get(self):
        self.fb.get_blob('audio/liam.nguyen@vah.com.au/0377b300-00c8-4219-b035-cf90794341c9')
        return ""