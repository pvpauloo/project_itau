from flask_restful import Resource, reqparse
from ..models.usuario import UsuarioModel
from flask_jwt_extended import create_access_token, get_jwt
from werkzeug.security import safe_str_cmp
from ..blacklist import BLACKLIST
import bcrypt

atributos = reqparse.RequestParser()
atributos.add_argument('login')
atributos.add_argument('senha')

class Login():
    def post():
        dados = atributos.parse_args()

        usuario = UsuarioModel.find_loginUsuario(dados.login)

        if usuario and  bcrypt.checkpw(dados.senha.encode('utf8'), usuario.senha.encode('utf8')):
            token_acesso = create_access_token(identity=usuario.idusuario)
            return {"token": token_acesso, "idUsuario": usuario.idusuario}, 200
        return {"message": "Usuário ou senha incorretos."}, 401

class Logout():
    def post():
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {"message": "Deslogado!"}, 200
