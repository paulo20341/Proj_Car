from flask import Flask

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locadora_veiculos.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


if __name__ == '__main__':
    app.run(debug=True)
