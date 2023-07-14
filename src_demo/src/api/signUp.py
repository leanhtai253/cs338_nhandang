from flask_restful import Resource
from flask import request
from flask import Response
from firebase.firebaseApp import FirebaseApp
from service.accountService import AccountService
from model.modelService import ModelService
MAX_TIMES_SIGN_UP = 10
class SignUp(Resource):
    fb = FirebaseApp()
    def post(self):
        email = request.form['email']
        password = request.form['password']
        fullName = request.form['fullName']
        audio = request.files['audio']
        if not AccountService.checkEmailExist(email):
            AccountService.insertUser(email, password, fullName)
        
        if AccountService.checkEmailExist(email):
            data = {
                'qualified': False
            }
            num = self.fb.get_latest_blobNum(username=email)
            if num == MAX_TIMES_SIGN_UP:
                data['qualified'] = True
                ModelService.train(username=email)
            elif num < MAX_TIMES_SIGN_UP:
                num += 1
                self.fb.upload_blob(username=email, file=audio, fileNum=num)
                if num == MAX_TIMES_SIGN_UP:
                    data['qualified'] = True
            return data
        