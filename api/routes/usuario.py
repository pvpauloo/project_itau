from api import app, api
from ..resources.usuario import Usuarios, Usuario, NovoUsuario
from flask_jwt_extended import jwt_required

@app.route('/usuarios', methods=['GET'])
@jwt_required()
def get_usuarios():
    return Usuarios.get()


@app.route('/usuarios/novo', methods=['POST'])
@jwt_required()
def post_usuarios():
    return NovoUsuario.post()


@app.route('/usuarios/<int:id>', methods=['GET'])
@jwt_required()
def get_usuariosby_id(id):
    return Usuario.get(id)


@app.route('/usuarios/<int:id>', methods=['PUT'])
@jwt_required()
def put_usuarios(id):
    return Usuario.put(id)

@app.route('/usuarios/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_usuarios(id):
    return Usuario.delete(id)
