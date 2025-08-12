from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def criar_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    

    from .rotas_posts import posts_bp
    app.register_blueprint(posts_bp, url_prefix='/api')
    
    return app