from flask import Blueprint, request, jsonify
from database import db
from models.livro import Livro
from models.user import Usuario
from models.emprestimo import Emprestimo
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta

PRAZO_DEVOLUCAO = 7 
VALOR_MULTA_DIARIA = 1.50

registros_bp = Blueprint('registros', __name__)

@registros_bp.route('/livros', methods=['POST'])
@jwt_required()
def create_livro():
    """C: Cria um novo livro no acervo."""
    data = request.get_json()
    titulo = data.get('titulo')
    autor = data.get('autor')

    if not titulo or not autor:
        return jsonify({"msg": "Título e autor são obrigatórios."}), 400

    new_livro = Livro(titulo=titulo, autor=autor, disponivel=True)
    
    db.session.add(new_livro)
    db.session.commit()
    
    return jsonify({
        "msg": "Livro cadastrado com sucesso.",
        "livro_id": new_livro.id,
        "titulo": new_livro.titulo
    }), 201

@registros_bp.route('/livros', methods=['GET'])
@jwt_required()
def get_livros():
    livros = Livro.query.all()
    
    results = [
        {
            "id": livro.id,
            "titulo": livro.titulo,
            "autor": livro.autor,
            "disponivel": livro.disponivel
        }
        for livro in livros
    ]
    return jsonify(results), 200

@registros_bp.route('/livros/<int:livro_id>', methods=['GET'])
@jwt_required()
def get_livro(livro_id):
    """R: Consulta um livro individualmente."""
    livro = Livro.query.get_or_404(livro_id)
    
    return jsonify({
        "id": livro.id,
        "titulo": livro.titulo,
        "autor": livro.autor,
        "disponivel": livro.disponivel
    }), 200

@registros_bp.route('/livros/<int:livro_id>', methods=['PUT'])
@jwt_required()
def update_livro(livro_id):
    livro = Livro.query.get_or_404(livro_id)
    data = request.get_json()
    
    if 'titulo' in data:
        livro.titulo = data['titulo']
    if 'autor' in data:
        livro.autor = data['autor']
    if 'disponivel' in data:
        livro.disponivel = data['disponivel']
        
    db.session.commit()
    return jsonify({"msg": "Livro atualizado com sucesso.", "id": livro.id}), 200

@registros_bp.route('/livros/<int:livro_id>', methods=['DELETE'])
@jwt_required()
def delete_livro(livro_id):
    livro = Livro.query.get_or_404(livro_id)
    
    if not livro.disponivel:
        return jsonify({"msg": "Não é possível remover. O livro está emprestado."}), 400
        
    db.session.delete(livro)
    db.session.commit()
    return jsonify({"msg": "Livro removido com sucesso."}), 200

@registros_bp.route('/emprestar', methods=['POST'])
@jwt_required()
def emprestar_livro():
    user_id = get_jwt_identity()
    data = request.get_json()
    livro_id = data.get('livro_id')

    usuario = Usuario.query.get(user_id)
    livro = Livro.query.get(livro_id)

    if not livro or not usuario:
        return jsonify({"msg": "Livro ou Usuário não encontrado."}), 404

    if not livro.disponivel:
        return jsonify({"msg": "Livro não está disponível para empréstimo."}), 400
        
    if usuario.multa_pendente > 0:
        return jsonify({"msg": f"Usuário possui multa pendente de R${usuario.multa_pendente:.2f}."}), 403

    new_emprestimo = Emprestimo(usuario_id=user_id, livro_id=livro_id, data_emprestimo=datetime.now())

    livro.disponivel = False
    
    db.session.add(new_emprestimo)
    db.session.commit()

    data_limite = new_emprestimo.data_emprestimo + timedelta(days=PRAZO_DEVOLUCAO)

    return jsonify({
        "msg": f"Livro '{livro.titulo}' emprestado com sucesso.",
        "prazo_devolucao": f"{PRAZO_DEVOLUCAO} dias",
        "data_limite": data_limite.strftime('%d/%m/%Y')
    }), 200


@registros_bp.route('/devolver', methods=['POST'])
@jwt_required()
def devolver_livro():
    user_id = get_jwt_identity()
    data = request.get_json()
    livro_id = data.get('livro_id')

    usuario = Usuario.query.get(user_id)
    livro = Livro.query.get(livro_id)
        
    emprestimo_ativo = Emprestimo.query.filter_by(
        usuario_id=user_id, 
        livro_id=livro_id
    ).first()

    if not emprestimo_ativo:
        return jsonify({"msg": "Este livro não foi emprestado por este usuário, ou já foi devolvido."}), 404

    data_emprestimo = emprestimo_ativo.data_emprestimo
    data_limite = data_emprestimo + timedelta(days=PRAZO_DEVOLUCAO)
    data_devolucao = datetime.now()
    
    multa = 0.0
    
    atraso = data_devolucao - data_limite
    dias_atraso = atraso.days if atraso.days > 0 else 0
    
    if dias_atraso > 0:
        multa = dias_atraso * VALOR_MULTA_DIARIA
        usuario.multa_pendente += multa
        
    db.session.delete(emprestimo_ativo)

    livro.disponivel = True
    
    db.session.commit()

    response = {
        "msg": f"Livro '{livro.titulo}' devolvido com sucesso.",
        "dias_atraso": dias_atraso
    }
    
    if multa > 0:
        response["multa_aplicada"] = f"R${multa:.2f}"
        response["msg"] += f"⚠️ Multa aplicada de R${multa:.2f}."
        
    return jsonify(response), 200

@registros_bp.route('/multa/consultar', methods=['GET'])
@jwt_required()
def consultar_multa():
    """Consulta o valor da multa pendente para o usuário autenticado."""
    user_id = get_jwt_identity()
    usuario = Usuario.query.get_or_404(user_id)
    
    return jsonify({
        "multa_pendente": f"R${usuario.multa_pendente:.2f}",
        "msg": "Esta é a multa consolidada por devoluções passadas. Empréstimos futuros só serão liberados após zerar o saldo."
    }), 200

@registros_bp.route('/multa/pagar', methods=['POST'])
@jwt_required()
def pagar_multa():
    """Permite ao usuário autenticado pagar uma parte ou o total da multa pendente."""
    user_id = get_jwt_identity()
    data = request.get_json()
    valor_pago_raw = data.get('valor_pago')

    if valor_pago_raw is None:
        return jsonify({"msg": "O valor_pago é obrigatório."}), 400

    try:
        valor_pago = float(valor_pago_raw)
    except ValueError:
        return jsonify({"msg": "Valor de pagamento inválido."}), 400

    if valor_pago <= 0:
        return jsonify({"msg": "O valor pago deve ser positivo."}), 400

    usuario = Usuario.query.get_or_404(user_id)
    
    if usuario.multa_pendente == 0:
        return jsonify({"msg": "Usuário não possui multa pendente para pagar."}), 200

    if valor_pago > usuario.multa_pendente:
        return jsonify({
            "msg": f"Valor pago excede a multa pendente de R${usuario.multa_pendente:.2f}.",
            "multa_pendente": f"R${usuario.multa_pendente:.2f}"
        }), 400
        
    usuario.multa_pendente -= valor_pago
    db.session.commit()
    
    return jsonify({
        "msg": f"Pagamento de R${valor_pago:.2f} processado.",
        "saldo_restante": f"R${usuario.multa_pendente:.2f}"
    }), 200