from . import db, bcrypt

#Tabela de Usuarios
class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


#Tabela do Conteudo dos Blogs
class Post(db.Model):
    __tablename__ = 'post_do_blog'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    conteudo = db.Column(db.String(20000), nullable=False)
    
    def __repr__(self):
        return f"<Post {self.titulo}>"
