import json
import os
import subprocess
import firebase_admin
from firebase_admin import credentials, auth
from flask import Flask, request
from functools import wraps
from shutil import make_archive
from zipfile import ZipFile

# App config
app = Flask(__name__)
firebase = firebase_admin.initialize_app()
users = [{'uid': 1, 'name': 'Noah Schairer'}]

def check_token(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not request.headers.get('authorization'):
            return {'message': 'No token provided'}, 400
        try:
            id_token = request.headers['authorization'].replace("Bearer", "", 1).strip()
            user = auth.verify_id_token(id_token)
            request.user = user
        except:
            return {'message': 'Invalid token provided.'}, 400
        return f()
    check_token.__doc__ = """This function is checks the firebase users auth token"""
    return wrap

@app.route('/download/zip', methods=['GET', 'POST', 'OPTIONS'])
@check_token
def download():
    folder_name = request.form.get('folderPath')
    print(check_token.__name__)
    print(check_token.__doc__)
    print(os.getenv('STORAGE_BUCKET'))
    subprocess.run(["script.sh", folder_name, os.path.expanduser('~')], shell=True)

    root_dir = os.path.expanduser('~') + "/" + folder_name
    make_archive(folder_name, "zip", root_dir)

    with ZipFile(folder_name + ".zip", 'r') as zip:
        for info in zip.infolist():
            print(info.filename)
    return "Done!"

@app.route('/welcome')
def welcome():
    return "Welcome"
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8082)))