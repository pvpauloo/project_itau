from flask_restful import Resource, reqparse
from ..models.fornecedor import FornecedorModel
from ..models.produto import ProdutoModel
from flask import jsonify


class Fornecedores():
    def get():
        return jsonify([fornecedor.json() for fornecedor in FornecedorModel.query.all()])

class NovoFornecedor():
    def post():
        dados = Fornecedor.atributos.parse_args()
        if FornecedorModel.find_fornecedorCNPJ(dados.cnpj):
            return {"message": "Fornecedor com CNPJ: '{}' já cadastrado.".format(dados.cnpj)},400

        fornecedor = FornecedorModel(None, **dados)

        try:
            fornecedor.save_fornecedor()
        except:
            return {"message": "Ocorreu um erro ao tentar salvar fornecedor."}, 500
        return fornecedor.json()

class Fornecedor():
    atributos = reqparse.RequestParser()
    atributos.add_argument('razao_social')
    atributos.add_argument('cnpj')

    def get(id):
        fornecedor = FornecedorModel.find_fornecedor(id)
        if fornecedor:
            return fornecedor.json()
        return {'message': 'Fornecedor não encontrado'}, 404

    def put(id):
        dados = Fornecedor.atributos.parse_args()

        fornecedorEncontrado = FornecedorModel.find_fornecedor(id)
        if fornecedorEncontrado:
            print('Fornecedor encontrado')
            fornecedorEncontrado.update_fornecedor(**dados)
            fornecedorEncontrado.save_fornecedor()
            return fornecedorEncontrado.json(), 200
        fornecedor = FornecedorModel(id, **dados)
        try:
            fornecedor.save_fornecedor()
        except:
            return {"message": "Ocorreu um erro ao tentar salvar fornecedor."}, 500
        return fornecedor.json(), 201

    def delete(id):
        fornecedor = FornecedorModel.find_fornecedor(id)
        if fornecedor:
            produto = ProdutoModel.find_fornecedor_produto(fornecedor.idfornecedor)
            if produto:
                return {"message": "Não é possível excluir um fornecedor com produto já cadastrado!"}, 400

            try:
                fornecedor.delete_fornecedor()
            except:
                return {"message": "Ocorreu um erro ao tentar excluir fornecedor."}, 500
            return {"message": "Fornecedor removido"}
        return {"message": "Fornecedor não encontrado"},404
