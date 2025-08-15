from flask import Blueprint, request, jsonify
from flask_restx import Api, Resource, fields
from pydantic import ValidationError
from sqlalchemy import select
from flask_jwt_extended import create_access_token

from .modelos import Usuario
from . import db
from .schemas import UsuarioSchema


auth_bp = Blueprint("auth", __name__)

api = Api(auth_bp,
          title="Autenticacao",
          version='1.0',
          description='Endpoints para registro e login de usuarios.')

ns = api.namespace('auth', description='Operacoes de Autenticacao')

usuario_input_modelo = api.model("UserInput", {
    "username": fields.String(required=True, description='Nome de usuario', min_length=3),
    "password": fields.String(required=True, description='Senha do usuario', min_length=6, type='password'),
})

token_modelo = api.model("Token", {
    "access_token": fields.String(readonly=True, description='Token de acesso JWT')
})

@ns.route('/registrar')
class Registro(Resource):

    @ns.doc('registrar_usuario')
    @ns.expect(usuario_input_modelo, validate=True)
    @ns.response(201, 'Usuario registrado com sucesso')
    @ns.response(409, 'Usuario ja existe')
    @ns.response(400, 'Verificacao falhou')
    def post(self):
        try:
            dados_usuario = UsuarioSchema.model_validate(api.payload)

        except ValidationError as e:
            return e.errors(), 400
        
        stmt = select(Usuario).where(Usuario.username == dados_usuario.username)
        if db.session.scalar(stmt) is not None:
            return {'message': 'Usuário já existe'}, 409
        
        novo_usuario = Usuario(username=dados_usuario.username)
        novo_usuario.set_password(dados_usuario.password)
        db.session.add(novo_usuario)
        db.session.commit()
        
        return {'message': 'Usuário registrado com sucesso'}, 201
    
@ns.route('/login')
class Login(Resource):

    @ns.doc('login_usuario')
    @ns.expect(usuario_input_modelo, validate=True)
    @ns.marshal_with(token_modelo, code=200)
    @ns.response(401, 'Credenciais inválidas')
    def post(self):
        """Autentica um usuário e retorna um token JWT."""
        try:
            dados_login = UsuarioSchema.model_validate(api.payload)
        except ValidationError as e:
            return e.errors(), 400
        
        stmt = select(Usuario).where(Usuario.username == dados_login.username)
        usuario = db.session.scalar(stmt)

        if usuario and usuario.check_password(dados_login.password):
            access_token = create_access_token(identity=str(usuario.id))
            return {'access_token': access_token} 
        
        return {'message': 'Credenciais inválidas'}, 401



