from .sql_alchemy import banco

class CategoriaModel(banco.Model):
    __tablename__ = 'CATEGORIA'

    idcategoria = banco.Column(banco.Integer, primary_key=True)
    nome_categoria = banco.Column(banco.String(20))

    def __init__(self, idcategoria, nome_categoria):
        self.idcategoria = idcategoria
        self.nome_categoria = nome_categoria

    def json(self):
        return {
            'idcategoria': self.idcategoria,
            'nome_categoria': self.nome_categoria
        }

    @classmethod
    def find_categoria(cls, idcategoria):
        categoria = cls.query.filter_by(idcategoria=idcategoria).first()
        if categoria:
            return categoria
        return None
        
    @classmethod
    def find_nome_categoria(cls, nome_categoria):        
        categoria = cls.query.filter_by(nome_categoria=nome_categoria).first()
        if categoria:
            return categoria
        return None

    def save_categoria(self):
        banco.session.add(self)
        banco.session.commit()

    def update_categoria(self, nome_categoria):
        self.nome_categoria = nome_categoria


    def delete_categoria(self):
        banco.session.delete(self)
        banco.session.commit()
