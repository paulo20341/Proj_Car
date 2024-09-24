from app import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    
    reservas = db.relationship('Reserva', backref='usuario', lazy=True)

class Veiculo(db.Model):
    __tablename__ = 'veiculos'
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    placa = db.Column(db.String(10), unique=True, nullable=False)
    disponivel = db.Column(db.Boolean, default=True)
    
    reservas = db.relationship('Reserva', backref='veiculo', lazy=True)

class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime, nullable=False)
    local_retirada = db.Column(db.String(255))  # Coluna que você mencionou
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)  # Tabela corrigida
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculos.id'), nullable=False)  # Tabela corrigida

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Usuario = db.Column(db.String(80), unique=True, nullable=False)
    Contraseña = db.Column(db.String(120), nullable=False)
    CPF = db.Column(db.String(11), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.Usuario}>'
