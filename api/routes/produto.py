from api import app, api
from ..resources.produto import Produtos, Produto, NovoProduto
from flask_jwt_extended import jwt_required

@app.route('/produtos', methods=['GET'])
@jwt_required()
def get_produtos():
    return Produtos.get()


@app.route('/produtos/novo', methods=['POST'])
@jwt_required()
def post_produto():
    return NovoProduto.post()


@app.route('/produtos/<int:id>', methods=['GET'])
@jwt_required()
def get_produtoby_id(id):
    return Produto.get(id)


@app.route('/produtos/<int:id>', methods=['PUT'])
@jwt_required()
def put_produto(id):
    return Produto.put(id)

@app.route('/produtos/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_produtos(id):
    return Produto.delete(id)

