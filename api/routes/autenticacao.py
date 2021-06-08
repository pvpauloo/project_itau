from api import app, api
from ..resources.autenticacao import Login, Logout
from flask_jwt_extended import jwt_required

@app.route('/login', methods=['POST'])
def login():
    return Login.post()

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return Logout.post()
