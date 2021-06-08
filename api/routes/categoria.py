from api import app, api
from ..resources.categoria import Categorias, Categoria, NovaCategoria
from ..models.categoria import CategoriaModel
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

@app.route('/categorias', methods=['GET'])
@jwt_required()
def get_categorias():
    return Categorias.get()


@app.route('/categorias/novo', methods=['POST'])
@jwt_required()
def post_categoria():
    return NovaCategoria.post()


@app.route('/categorias/<int:id>', methods=['GET'])
@jwt_required()
def get_categoriaby_id(id):
    return Categoria.get(id)


@app.route('/categorias/<int:id>', methods=['PUT'])
@jwt_required()
def put_categoria(id):
    return Categoria.put(id)

@app.route('/categorias/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_categorias(id):
    return Categoria.delete(id)

