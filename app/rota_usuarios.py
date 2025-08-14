from flask import request, jsonify, Blueprint
from .modelos import Usuario 
from . import db
from flask_jwt_extended import create_access_token
from sqlalchemy import select

auth_bp = Blueprint("usuarios", __name__)

@auth_bp.route("/registrar", methods=["POST"])
def registrar():
    data = request.get_json()
    if not data or not 'username' in data or not 'password' in data:
        return jsonify({'message': 'Usuario e senha sao obrigatorios'}), 400
    
    nome_usuario = select(Usuario).where(Usuario.username == data['username'])
    if db.session.scalar(nome_usuario) is not None:
        return jsonify({'message': 'Usuario ja existe'}), 409
    
    novo_usuario = Usuario(username=data['username'])
    novo_usuario.set_password(data['password'])
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({'message': 'Usuario registrado com sucesso'}), 201


@auth_bp.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    if not data or not 'username' in data or not 'password' in data:
        return jsonify({'message': 'Usuario e senha sao obrigatorios'}), 400
    
    nome_usuario = select(Usuario).where(Usuario.username == data['username'])
    usuario = db.session.scalar(nome_usuario)

    if usuario and usuario.check_password(data['password']):

        access_token = create_access_token(identity=str(usuario.id))
        return jsonify(access_token=access_token)
    
    return jsonify({'message': 'Credenciais invalidas'}), 401

