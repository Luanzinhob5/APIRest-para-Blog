from flask import Blueprint, request, jsonify, abort
from flask_restx import Api, Resource, fields
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from sqlalchemy import select

from .modelos import Post
from . import db
from .schemas import PostCriarSchema, PostSchema, PostAtualizarSchema


posts_bp = Blueprint('posts', __name__)

api = Api(posts_bp,
          title='API de Blog',
          version='1.0',
          description='Uma API para gerenciar posts de um blog.')

ns = api.namespace('posts', description='Operacoes de Posts')

post_modelo = api.model('Post',{
    'id': fields.Integer(readonly=True, description='O identificador unico do post'),
    'titulo': fields.String(required=True, description= 'O titulo do post', min_length=3),
    'descricao': fields.String(required=True, description='A descricao do post'),
    'conteudo': fields.String(required=True, description='O conteudo do post'),

})

post_input_modelo = api.model('PostInput', {
    'titulo': fields.String(required=True, description='O titulo do post', min_length=3),
    'descricao': fields.String(required=True, description='A descricao do post'),
    'conteudo': fields.String(description='O conteudo do post') 
})

@ns.route('')
class ListaPosts(Resource):

    @ns.doc('Listar_posts')
    @ns.marshal_list_with(post_modelo)
    def get(self):
        pagina = request.args.get('pagina', 1, type=int)
        por_pagina = request.args.get('por_pagina', 10, type=int)

        stmt = select(Post).order_by(Post.id.desc())
        posts_paginados = db.paginate(stmt, page=pagina, per_page=por_pagina)

        return posts_paginados.items
    
    @ns.doc('criar_post')
    @jwt_required()
    @ns.expect(post_input_modelo, validate=True)
    @ns.marshal_list_with(post_modelo, code=201)
    def post(self):
        try:
            post_data = PostCriarSchema.model_validate(api.payload)
        except ValidationError as e:
            return e.errors(), 400
        
        novo_post = Post(**post_data.model_dump())
        db.session.add(novo_post)
        db.session.commit()
        return novo_post, 201
    
@ns.route("/<int:id>")
@ns.response(404, "Post nao encontrado")
@ns.param('id', 'O identificador do post')
class RecursoPost(Resource):

    @ns.doc('obter_post')
    @ns.marshal_with(post_modelo)
    def get(self, id):
        post = db.session.get(Post, id)
        if not post:
            abort(404, description=f"Post com id {id} nao encontrado.")
        return post
    
    @ns.doc('atualizar_post')
    @jwt_required()
    @ns.expect(post_input_modelo)
    @ns.marshal_with(post_modelo)
    def put(self, id):
        post = db.session.get(Post, id)
        if not post:
            abort(404, description=f"Post com id {id} nao encontrado.")

        try:
            dados_atualizados = PostAtualizarSchema.model_validate(api.payload)

        except ValidationError as e:
            return e.errors(), 400
        
        for key, value in dados_atualizados.model_dump(exclude_unset=True).items():
            setattr(post, key, value)

        db.session.commit()
        return post
    
    @ns.doc('deletar_post')
    @jwt_required()
    @ns.response(204, 'Post deletado com sucesso')
    def delete(self, id):
        post = db.session.get(Post, id)
        if not post:
            abort(404, description=f"Post com id {id} nao encontrado.")

        db.session.delete(post)
        db.session.commit()
        return "", 204

# Rota de criação de um novo post
# @posts_bp.route('/posts', methods=["POST"])
# @jwt_required()
# def criar_post():
#     try:
#         post_data = PostCriarSchema.model_validate(request.get_json())
#     except ValidationError as e:
#         return jsonify(e.errors()), 400
    
#     novo_post = Post(**post_data.model_dump())
#     db.session.add(novo_post)
#     db.session.commit()

#     return jsonify(PostSchema.model_validate(novo_post).model_dump()), 201
        
    
# # Rota para colher os dados de todos os posts
# @posts_bp.route('/posts', methods=["GET"])
# def pegar_posts():
#     pagina = request.args.get('pagina', 1, type=int)
#     por_pagina = request.args.get('por_pagina', 10, type=int)

#     todos_os_posts = select(Post).order_by(Post.id)
#     posts_paginados = db.paginate(todos_os_posts,page=pagina, per_page=por_pagina)
#     posts = posts_paginados.items

#     result = ([PostSchema.model_validate(post).model_dump() for post in posts])
#     return jsonify({
#         'posts': result,
#         'total_pages': posts_paginados.pages,
#         'current_page': posts_paginados.page,
#         'total_posts': posts_paginados.total
#     })


# # Rota de coleta de posts por id
# @posts_bp.route('/posts/<int:id>', methods=['GET'])
# def encontrar_post_id(id):
#     post = db.session.get(Post, id)
#     if not post:
#         abort(404, description=f"Post com id {id} não encontrado.")

#     if post:
#         return jsonify(post.to_dict()), 200
#     return jsonify(response={"error": "Post nao encontrado!"}), 204


# # Rota que muda os dados de um post
# @posts_bp.route('/posts/<int:id>', methods=['PUT'])
# @jwt_required()
# def alterar_post_id(id):
#     post = db.session.get(Post, id)
#     if not post:
#         abort(404, description=f"Post com id {id} não encontrado.")

#     data = request.get_json()

#     post.titulo = data.get("titulo", post.titulo)
#     post.conteudo = data.get("conteudo", post.conteudo)
#     post.descricao = data.get("descricao", post.descricao)

#     db.session.commit()

#     return jsonify(post.to_dict())

# @posts_bp.route('/posts/<int:id>', methods=['DELETE'])
# @jwt_required()
# def deletar_post_id(id):
#     post = db.session.get(Post, id)
#     if not post:
#         abort(404, description=f"Post com id {id} não encontrado.")

#     db.session.delete(post)
#     db.session.commit()
#     return "", 204




