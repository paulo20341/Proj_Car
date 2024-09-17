# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuração do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locadora_veiculos.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar o banco de dados com o app
    db.init_app(app)

    # Importar os modelos para que o SQLAlchemy reconheça as tabelas
    from .models import Usuario, Veiculo, Reserva, Manutencao

    return app
