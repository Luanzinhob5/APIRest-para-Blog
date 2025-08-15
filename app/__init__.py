from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from .config import Config
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
bcrypt = Bcrypt()

def criar_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)

    from . import errors
    app.register_error_handler(404, errors.handle_not_found)
    app.register_error_handler(400, errors.handle_bad_request)
    app.register_error_handler(500, errors.handle_internal_server_error)
    
    from .rotas_posts import posts_bp
    app.register_blueprint(posts_bp, url_prefix='/api')

    from .rota_usuarios import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return app