from .sql_alchemy import banco

class ProdutoModel(banco.Model):
    __tablename__ = 'PRODUTO'

    idproduto = banco.Column(banco.Integer, primary_key=True)
    nome_produto = banco.Column(banco.String(50))
    status_produto = banco.Column(banco.String(20))
    quantidade = banco.Column(banco.Integer)
    id_fornecedor = banco.Column(banco.Integer, banco.ForeignKey('FORNECEDOR.idfornecedor'))
    id_categoria = banco.Column(banco.Integer, banco.ForeignKey('CATEGORIA.idcategoria'))

    # fornecedor = banco.relationship('FornecedorModel', foreign_keys=id_fornecedor)
    # categoria = banco.relationship('CategoriaModel', foreign_keys=id_categoria)

    def __init__(self, idproduto, nome_produto, status_produto, quantidade, id_fornecedor, id_categoria):        
        self.idproduto = idproduto
        self.nome_produto = nome_produto
        self.status_produto = status_produto
        self.quantidade = quantidade
        self.id_fornecedor = id_fornecedor
        self.id_categoria = id_categoria

    def json(self):
        return {
            'idproduto':self.idproduto,
            'nome_produto':self.nome_produto,
            'status_produto':self.status_produto,
            'quantidade':self.quantidade,
            'id_fornecedor':self.id_fornecedor,
            'id_categoria':self.id_categoria            
        }

    @classmethod
    def find_produto(cls, idproduto):
        produto = cls.query.filter_by(idproduto=idproduto).first()
        if produto:
            return produto
        return None
    
    @classmethod
    def find_nome_produto(cls, nome_produto):
        produto = cls.query.filter_by(nome_produto=nome_produto).first()        
        if produto:
            return produto
        return None

    @classmethod
    def find_fornecedor_produto(cls, id_fornecedor):
        produto = cls.query.filter_by(id_fornecedor=id_fornecedor).first()
        if produto:
            return produto
        return None

    @classmethod
    def find_categoria_produto(cls, id_categoria):
        produto = cls.query.filter_by(id_categoria=id_categoria).first()
        if produto:
            return produto
        return None

    def save_produto(self):
        banco.session.add(self)
        banco.session.commit()

    def update_produto(self, nome_produto, status_produto, quantidade):
        self.nome_produto = nome_produto
        self.status_produto = status_produto
        self.quantidade = quantidade

    def delete_produto(self):
        banco.session.delete(self)
        banco.session.commit()

    def aumenta_quantidade(self, adicionais):
        print(self.quantidade)
        print(adicionais)
        self.quantidade = int(self.quantidade) + int(adicionais)
        print(self.quantidade)

    def diminui_quantidade(self, removidos):
        print(self.quantidade)
        print(removidos)
        self.quantidade = int(self.quantidade) - int(removidos)
        print(self.quantidade)
