from flask import Blueprint, request, jsonify
from models.user import Usuario
from database import db
from flask_jwt_extended import create_access_token
from datetime import timedelta

users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['POST'])
def register():
    """Rota para cadastrar um novo usuário."""
    data = request.get_json()
    
    if not data or not data.get('nome') or not data.get('email') or not data.get('password'):
        return jsonify({"msg": "Dados incompletos (nome, email, password) são obrigatórios."}), 400

    nome = data.get('nome')
    email = data.get('email')
    password = data.get('password')
    if Usuario.query.filter_by(email=email).first():
        return jsonify({"msg": "Usuário com este email já existe."}), 409

    new_user = Usuario(nome=nome, email=email)
    new_user.set_password(password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "Usuário cadastrado com sucesso!", "user_id": new_user.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Erro ao cadastrar usuário", "error": str(e)}), 500


@users_bp.route('/login', methods=['POST'])
def login():
    """Rota para autenticação e geração de JWT."""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"msg": "Email e senha são obrigatórios"}), 400

    email = data.get('email')
    password = data.get('password')
    
    user = Usuario.query.filter_by(email=email).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=30))
        
        return jsonify(
            {
                "msg": "Login realizado com sucesso",
                "user_id": user.id,
                "access_token": access_token
            }
        ), 200
    else:
        return jsonify({"msg": "Email ou senha inválidos"}), 401