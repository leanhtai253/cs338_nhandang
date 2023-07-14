from flask import Flask
from flask_restful import Resource, Api
from api.signIn import SignIn
from api.signUp import SignUp
from api.hello import Hello
app = Flask(__name__)
api = Api(app)

api.add_resource(Hello, "/hello")
api.add_resource(SignIn, "/sign-in")
api.add_resource(SignUp, "/sign-up")
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

