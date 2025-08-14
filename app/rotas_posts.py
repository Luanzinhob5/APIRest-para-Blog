from flask import Blueprint, request, jsonify
from .modelos import Post
from . import db
from .schemas import PostCriarSchema
from pydantic import ValidationError
from flask_jwt_extended import jwt_required


posts_bp = Blueprint('posts', __name__)


# Rota de criação de um novo post
@posts_bp.route('/posts', methods=["POST"])
@jwt_required()
def criar_post():
    dados_json = request.get_json()

    try:
        dados_post = PostCriarSchema(**dados_json)
    except ValidationError as e:
        return jsonify(e.errors()), 400
    
    novo_post = Post(**dados_post.model_dump())
    db.session.add(novo_post)
    db.session.commit()

    return jsonify(novo_post.to_dict()), 201
        
    
# Rota para colher os dados de todos os posts
@posts_bp.route('/posts', methods=["GET"])
def pegar_posts():
    todos_posts = Post.query.all()
    result = ([post.to_dict() for post in todos_posts])
    return jsonify(result), 200


# Rota de coleta de posts por id
@posts_bp.route('/posts/<int:id>', methods=['GET'])
def encontrar_post_id(id):
    post = Post.query.get_or_404(id)
    if post:
        return jsonify(post.to_dict()), 200
    return jsonify(response={"error": "Post nao encontrado!"}), 204


# Rota que muda os dados de um post
@posts_bp.route('/posts/<int:id>', methods=['PUT'])
@jwt_required()
def alterar_post_id(id):
    post = Post.query.get_or_404(id)
    data = request.get_json()

    post.titulo = data.get("titulo", post.titulo)
    post.conteudo = data.get("conteudo", post.conteudo)
    post.descricao = data.get("descricao", post.descricao)

    db.session.commit()

    return jsonify(post.to_dict())

@posts_bp.route('/posts/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_post_id(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return "", 204




