from .sql_alchemy import banco

class UsuarioModel(banco.Model):
    __tablename__ = 'USUARIO'

    idusuario = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(50))
    login = banco.Column(banco.String(20))
    senha = banco.Column(banco.String(72))

    def __init__(self, idusuario, nome, login, senha):
        self.idusuario = idusuario
        self.nome = nome
        self.login = login
        self.senha = senha        

    def json(self):
        return {
            'idusuario': self.idusuario,
            'nome': self.nome,
            'login': self.login
        }

    @classmethod
    def find_usuario(cls, idusuario):
        usuario = cls.query.filter_by(idusuario=idusuario).first()
        if usuario:
            return usuario
        return None

    @classmethod
    def find_loginUsuario(cls, login):
        usuario = cls.query.filter_by(login=login).first()
        if usuario:
            return usuario
        return None

    def save_usuario(self):
        banco.session.add(self)
        banco.session.commit()

    def update_usuario(self, nome, login, senha):
        self.nome = nome
        self.login = login
        self.senha = senha

    def delete_usuario(self):
        banco.session.delete(self)
        banco.session.commit()
