from flask import Flask
from database import init_db
from flask_jwt_extended import JWTManager
from datetime import timedelta

import models.user
import models.livro
import models.emprestimo

from routes.users import users_bp
from routes.registros import registros_bp

def create_app():
    app = Flask(__name__)
    
    app.config["JWT_SECRET_KEY"] = "sua_chave_secreta_aqui_trocar" 
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1) 
    
    init_db(app) 
    
    jwt = JWTManager(app)
    
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(registros_bp, url_prefix='/registros')
    
    return app

if __name__ == '__main__':
    try:
        app = create_app()
        print("API Iniciada. Acessível em http://127.0.0.1:5000")
        app.run(debug=True)
    except Exception as e:
        print(f"Erro ao inicializar o app: {e}")