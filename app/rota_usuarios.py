from flask import Blueprint, request, jsonify
from .modelos import Usuario
from . import db

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route("/registro", methods=["POST"])
def registro():
    data = request.get_json()
