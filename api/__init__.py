from flask import Flask, jsonify
from flask_restful import Api
from .env import DATABASE_URI, JWT_KEY, ACCESS_EXPIRES
from flask_script import Manager
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .blacklist import BLACKLIST
import requests, json
import json_logging

def logsplunk(myjson):
        # ENDPOINT DA CHAMADA
        # url = 'http://localhost:8088/services/collector/event/1.0'
        url = 'http://spaceps.ddns.net:8222/services/collector/event/1.0'
        headers = {'Content-Type': 'application/json', 'Authorization': 'Splunk 6a83d080-f7f0-4a7e-bf44-4189fc34a9a4'}
        # BODY DO POSTMAN PASSADO PARA EFETUAR O METODO POST
        payload = [{"event": f"{json.dumps(myjson)}","sourcetype": "json_no_timestamp"}]
        r = requests.post(url, json=payload, headers=headers)
        print('Log Splunk: ', r.text)


app = Flask(__name__)

json_logging.ENABLE_JSON_LOGGING = 'True'
json_logging.init(framework_name='flask')
json_logging.init_request_instrument(app)

# init the logger as usual
# logger = logging.getLogger("test-logger")
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.FileHandler(filename='json.log'))

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = JWT_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXPIRES
app.config['JWT_BLACKLIST_ENABLED'] = True

cors = CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app)
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_invalidado(jwt_header, jwt_payload):
    return jsonify({"message": "Usuário deslogado!"}), 401

from .models.sql_alchemy import banco
banco.init_app(app)
# app.run(debug=True)

manager = Manager(app)
from .routes import fornecedor, usuario, produto, autenticacao, categoria, movimentacao
from .resources.fornecedor import Fornecedores, Fornecedor, NovoFornecedor
from .resources.usuario import Usuarios, Usuario, NovoUsuario
from .resources.produto import Produtos, Produto, NovoProduto
from .resources.autenticacao import Login, Logout
from .resources.categoria import Categorias, Categoria, NovaCategoria
from .resources.movimentacao import NovaMovimentacao, Movimentacoes, Movimentacao

