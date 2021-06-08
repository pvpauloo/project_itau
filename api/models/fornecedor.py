from .sql_alchemy import banco

class FornecedorModel(banco.Model):
    __tablename__ = 'FORNECEDOR'

    idfornecedor = banco.Column(banco.Integer, primary_key=True)
    razao_social = banco.Column(banco.String(50))
    cnpj = banco.Column(banco.String(14))

    def __init__(self, idfornecedor, razao_social, cnpj):
        self.idfornecedor = idfornecedor
        self.razao_social = razao_social
        self.cnpj = cnpj

    def json(self):
        return {
            'idfornecedor': self.idfornecedor,
            'razao_social': self.razao_social,
            'cnpj': self.cnpj
        }

    @classmethod
    def find_fornecedor(cls, idfornecedor):
        fornecedor = cls.query.filter_by(idfornecedor=idfornecedor).first()
        if fornecedor:
            return fornecedor
        return None

    @classmethod
    def find_fornecedorCNPJ(cls, cnpjBusca):
        fornecedor = cls.query.filter_by(cnpj=cnpjBusca).first()
        if fornecedor:
            return fornecedor
        return None

    def save_fornecedor(self):
        banco.session.add(self)
        banco.session.commit()

    def update_fornecedor(self, razao_social, cnpj):
        self.razao_social = razao_social
        self.cnpj = cnpj

    def delete_fornecedor(self):
        banco.session.delete(self)
        banco.session.commit()
