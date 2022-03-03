import firebase_admin
from firebase_admin import credentials, auth
from flask import Flask
from flask.wrappers import Request

# Only showing how to set this middleware up as a class and use class methods
class AuthMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        if not request.headers.get('authorization'):
            return {'message': 'No token provided'}, 400
        try:
            id_token = request.headers['authorization'].replace("Bearer", "", 1).strip()
            decoded_token = auth.verify_id_token(id_token)
            print(decoded_token['uid'])
        except:
            return {'message': 'Invalid token provided.'}, 400
        return self.app(environ, start_response)

    def get_user(user):
        return "{}".format(user)