from . import db

#Tabela de Usuarios
class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(100), nullable=False)


#Tabela do Conteudo dos Blogs
class Post(db.Model):
    __tablename__ = 'post_do_blog'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    conteudo = db.Column(db.String(20000), nullable=False)

    #Converte o post para um dicionario
    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "conteudo": self.conteudo
        }
    
    def __repr__(self):
        return f"<Post {self.titulo}>"
