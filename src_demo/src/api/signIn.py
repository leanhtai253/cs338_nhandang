from flask_restful import Resource
from flask import request, make_response
from service.accountService import AccountService
from model.modelService import ModelService
from firebase.firebaseApp import FirebaseApp

class SignIn(Resource):
    fb = FirebaseApp()
    def post(self):
        email = request.form['email']
        password = request.form['password']
        audio = request.files['audio']
        # self.fb.download_blob(email, 10)
        # self.fb.upload_blob_signin(username=email, file=audio)
        # self.fb.download_blob_signin(username=email)
        score = ""
        code, msg = AccountService.authenticateUser(email, password, audio)
        if code == 200:
            score = ModelService.check(email)[0][0]
            if score > 0.5:
                resp = make_response(dict(predictedScore=str(score), status='successful'), 200)
            else:
                resp = make_response(dict(predictedScore=str(score), status='failed'), 401)
        else:
            resp = make_response(msg, code)
        resp.headers['Access-Control-Allow-Origin'] = "*"
        return resp