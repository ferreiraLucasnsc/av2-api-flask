from database import db

class Livro(db.Model):
    """Modelo que representa a tabela 'livros' no acervo."""
    __tablename__ = 'livros'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    disponivel = db.Column(db.Boolean, default=True)

    emprestimos = db.relationship('Emprestimo', backref='livro_emprestado', lazy='dynamic')

    def __repr__(self):
        return f'<Livro {self.titulo} (Disponível: {self.disponivel})>'