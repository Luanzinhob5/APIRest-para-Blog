from flask import Blueprint, request, jsonify
from .models import Post
from . import db

posts_bp = Blueprint('posts', __name__)


# Rota de criação de um novo post
@posts_bp.route('/posts', methods=["POST"])
def criar_post():
    dados = request.get_json()

    if not dados or not 'titulo' in dados:
        return jsonify(response={"error": "O titulo e obrigatorio."}), 400

    novo_post = Post(
            titulo=dados['titulo'],
            descricao=dados.get("descricao", ''),
            conteudo=dados.get("conteudo", '')
        )
    try:
        db.session.add(novo_post)
        db.session.commit()
        return jsonify(novo_post.to_dict()), 201
    except Exception as e:
        return jsonify(response={"error": str(e)}), 500
        
    
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
def alterar_post_id(id):
    post = Post.query.get_or_404(id)
    data = request.get_json()

    post.titulo = data.get("titulo", post.titulo)
    post.conteudo = data.get("conteudo", post.conteudo)
    post.descricao = data.get("descricao", post.descricao)

    db.session.commit()

    return jsonify(post.to_dict())

@posts_bp.route('/posts/<int:id>', methods=['DELETE'])
def deletar_post_id(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return "", 204




