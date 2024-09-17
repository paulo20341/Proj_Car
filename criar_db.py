# criar_db.py
from app import create_app
from app import db

# Crie uma instância da aplicação
app = create_app()

# Execute o comando dentro do contexto da aplicação
with app.app_context():
    db.create_all()
    print("Banco de dados criado com sucesso!")
0