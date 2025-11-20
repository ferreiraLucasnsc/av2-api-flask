from database import db
from datetime import datetime

class Emprestimo(db.Model):
    """Modelo que registra uma transação ativa de empréstimo (enquanto o livro não for devolvido)."""
    __tablename__ = 'emprestimos'
    
    id = db.Column(db.Integer, primary_key=True)
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    livro_id = db.Column(db.Integer, db.ForeignKey('livros.id'), nullable=False)
    
    data_emprestimo = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return f'<Emprestimo Usuario:{self.usuario_id} Livro:{self.livro_id} Data:{self.data_emprestimo.strftime("%Y-%m-%d")}>'