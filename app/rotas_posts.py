from flask import Blueprint, request, jsonify, abort
from .modelos import Post
from . import db
from .schemas import PostCriarSchema, PostSchema
from pydantic import ValidationError
from flask_jwt_extended import jwt_required
from sqlalchemy import select


posts_bp = Blueprint('posts', __name__)


# Rota de criação de um novo post
@posts_bp.route('/posts', methods=["POST"])
@jwt_required()
def criar_post():
    try:
        post_data = PostCriarSchema.model_validate(request.get_json())
    except ValidationError as e:
        return jsonify(e.errors()), 400
    
    novo_post = Post(**post_data.model_dump())
    db.session.add(novo_post)
    db.session.commit()

    return jsonify(PostSchema.model_validate(novo_post).model_dump()), 201
        
    
# Rota para colher os dados de todos os posts
@posts_bp.route('/posts', methods=["GET"])
def pegar_posts():
    pagina = request.args.get('pagina', 1, type=int)
    por_pagina = request.args.get('por_pagina', 10, type=int)

    todos_os_posts = select(Post).order_by(Post.id)
    posts_paginados = db.paginate(todos_os_posts,page=pagina, per_page=por_pagina)
    posts = posts_paginados.items

    result = ([PostSchema.model_validate(post).model_dump() for post in posts])
    return jsonify({
        'posts': result,
        'total_pages': posts_paginados.pages,
        'current_page': posts_paginados.page,
        'total_posts': posts_paginados.total
    })


# Rota de coleta de posts por id
@posts_bp.route('/posts/<int:id>', methods=['GET'])
def encontrar_post_id(id):
    post = db.session.get(Post, id)
    if not post:
        abort(404, description=f"Post com id {id} não encontrado.")

    if post:
        return jsonify(post.to_dict()), 200
    return jsonify(response={"error": "Post nao encontrado!"}), 204


# Rota que muda os dados de um post
@posts_bp.route('/posts/<int:id>', methods=['PUT'])
@jwt_required()
def alterar_post_id(id):
    post = db.session.get(Post, id)
    if not post:
        abort(404, description=f"Post com id {id} não encontrado.")

    data = request.get_json()

    post.titulo = data.get("titulo", post.titulo)
    post.conteudo = data.get("conteudo", post.conteudo)
    post.descricao = data.get("descricao", post.descricao)

    db.session.commit()

    return jsonify(post.to_dict())

@posts_bp.route('/posts/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_post_id(id):
    post = db.session.get(Post, id)
    if not post:
        abort(404, description=f"Post com id {id} não encontrado.")

    db.session.delete(post)
    db.session.commit()
    return "", 204




