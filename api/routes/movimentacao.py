from api import app, api
from ..resources.movimentacao import NovaMovimentacao, Movimentacoes, Movimentacao
from flask_jwt_extended import jwt_required


@app.route('/movimentacoes', methods=['GET'])
@jwt_required()
def get_movimentacoes():
  return Movimentacoes.get()

@app.route('/movimentacoes/<int:id>', methods=['GET'])
@jwt_required()
def get_movimentacao(id):
  return Movimentacao.get(id)

@app.route('/movimentacao/novo', methods=['POST'])
@jwt_required()
def post_movimentacao():
    return NovaMovimentacao.post()
