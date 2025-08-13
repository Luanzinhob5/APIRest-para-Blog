from flask import jsonify

def handle_not_found(e):
    return jsonify(error=str(e), message="Recurso não encontrado"), 404

def handle_bad_request(e):
    return jsonify(error=str(e), message="A requisição é inválida"), 400

def handle_internal_server_error(e):
    return jsonify(error="Erro Interno do Servidor", message="Ocorreu um problema inesperado."), 500