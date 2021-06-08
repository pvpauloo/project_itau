from flask_restful import Resource, reqparse
from ..models.produto import ProdutoModel
from ..models.categoria import CategoriaModel
from ..models.fornecedor import FornecedorModel
from ..models.movimentacao import MovimentacaoModel
from flask import jsonify

atributos = reqparse.RequestParser()
atributos.add_argument('nome_produto')
atributos.add_argument('status_produto')
atributos.add_argument('quantidade')
atributos.add_argument('id_fornecedor')
atributos.add_argument('id_categoria')

def validaQuantidade(quantidade):
    try:
        if int(quantidade) < 0:
            return "Quantidade inválida! Informe uma quantidade maior ou igual à zero."
    except:
        return "Quantidade inválida! Informe uma quantidade maior ou igual à zero."
    return ""

def validaCategoria(categoria):
    try:
        if int(categoria) <= 0:
            return "Categoria inválida! Informe uma categoria maior ou igual à zero."

        categoria = CategoriaModel.find_categoria(categoria)
        if not categoria:
            return "Categoria não encontrada"
    except:
        return "Categoria inválida!"
    return ""

def validaFornecedor(fornecedor):
    try:
        if int(fornecedor) <= 0:
            return "Fornecedor inválido! Informe um fornecedor maior ou igual à zero."

        fornecedor = FornecedorModel.find_fornecedor(fornecedor)
        if not fornecedor:
            return "Fornecedor não encontrado"
    except:
        return "Fornecedor inválido!"
    return ""

class Produtos():
    def get():
        return jsonify([produto.json() for produto in ProdutoModel.query.all()])

class NovoProduto():
    def post():
        dados = atributos.parse_args()

        errorMessage = validaQuantidade(dados.quantidade)
        if errorMessage != "":
            return {"message": errorMessage}, 400
        
        errorMessage = validaCategoria(dados.id_categoria)
        if errorMessage != "":
            return {"message": errorMessage}, 400

        errorMessage = validaFornecedor(dados.id_fornecedor)
        if errorMessage != "":
            return {"message": errorMessage}, 400

        if ProdutoModel.find_nome_produto(dados.nome_produto):
            return {"message": "Produto com nome: '{}' já cadastrado.".format(dados.nome_produto)},400

        produto = ProdutoModel(None, **dados)
        try:
            produto.save_produto()
        except:
            return {"message": "Ocorreu um erro ao tentar salvar produto."}, 500
        return produto.json()

class Produto():

    def get(id):
        produto = ProdutoModel.find_produto(id)
        if produto:
            return produto.json()
        return {"message": "Produto não encontrado."}, 404

    def put(id):
        dados = atributos.parse_args()

        errorMessage = validaQuantidade(dados.quantidade)
        if errorMessage != "":
            return {"message": errorMessage}, 400
        
        errorMessage = validaCategoria(dados.id_categoria)
        if errorMessage != "":
            return {"message": errorMessage}, 400

        errorMessage = validaFornecedor(dados.id_fornecedor)
        if errorMessage != "":
            return {"message": errorMessage}, 400

        if ProdutoModel.find_nome_produto(dados.nome_produto):
            produto = ProdutoModel.find_nome_produto(dados.nome_produto)
            print(produto.idproduto)
            if (produto.idproduto != id):
                return {"message": "Produto com nome: '{}' já cadastrado.".format(dados.nome_produto)},400

        produtoEncontrado = ProdutoModel.find_produto(id)
        if produtoEncontrado:
            produtoEncontrado.update_produto(dados.nome_produto, dados.status_produto, dados.quantidade)
            produtoEncontrado.save_produto()
            return produtoEncontrado.json(), 200
            
        produto = ProdutoModel(id, **dados)
        try:
            produto.save_produto()
        except:
            return {"message": "Ocorreu um erro ao tentar salvar produto."}, 500
        return produto.json(), 201


    def delete(id):
        produto = ProdutoModel.find_produto(id)
        if produto:
            movimentacao = MovimentacaoModel.find_movimentacaoProduto(produto.idproduto)
            if movimentacao:
                return {"message": "Não é possível excluir um produto com movimentação já cadastrada!"}, 400

            try:
                produto.delete_produto()
            except:
                return {"message": "Ocorreu um erro ao excluir o produto"}, 500
            return {"message": "Produto removido"}
        return {"message": "Produto não encontrado"}, 404
