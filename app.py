from app import create_app, db

app = create_app()

# Inicialização do banco de dados (opcional, se você estiver criando as tabelas no início)
with app.app_context():
    db.create_all()  # Cria todas as tabelas definidas nos modelos

if __name__ == '__main__':
    app.run(debug=True)