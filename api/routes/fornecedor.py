from api import app, api
from ..resources.fornecedor import Fornecedores, Fornecedor, NovoFornecedor
from ..models.fornecedor import FornecedorModel
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

@app.route('/fornecedores', methods=['GET'])
@jwt_required()
def get_fornecedores():
    return Fornecedores.get()


@app.route('/fornecedores/novo', methods=['POST'])
@jwt_required()
def post_fornecedor():
    return NovoFornecedor.post()


@app.route('/fornecedores/<int:id>', methods=['GET'])
@jwt_required()
def get_fornecedorby_id(id):
    return Fornecedor.get(id)


@app.route('/fornecedores/<int:id>', methods=['PUT'])
@jwt_required()
def put_fornecedor(id):
    return Fornecedor.put(id)

@app.route('/fornecedores/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_fornecedor(id):
    return Fornecedor.delete(id)

