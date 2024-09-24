from flask import Blueprint, render_template, request, redirect, flash, url_for, session
from .models import Veiculo, Reserva, User
from . import db

bp = Blueprint('veiculos', __name__)


@bp.route('/')
def index():
    return redirect('/menu')  # Redireciona para a página inicial que você deseja

@bp.route('/menu')
def menu():
    return render_template('base.html')

@bp.route('/veiculos')
def listar_veiculos():
    veiculos = Veiculo.query.all()
    return render_template('listar_veiculos.html', veiculos=veiculos)

@bp.route('/veiculos/adicionar', methods=['GET', 'POST'])
def adicionar_veiculo():
    if request.method == 'POST':
        modelo = request.form.get('modelo')
        marca = request.form.get('marca')
        ano = request.form.get('ano')
        placa = request.form.get('placa')

        novo_veiculo = Veiculo(modelo=modelo, marca=marca, ano=ano, placa=placa)
        db.session.add(novo_veiculo)
        db.session.commit()
        flash('Veículo adicionado com sucesso!', 'success')
        return redirect(url_for('veiculos.listar_veiculos'))
    
    return render_template('adicionar_veiculo.html')

@bp.route('/veiculos/editar/<int:id>', methods=['GET', 'POST'])
def editar_veiculo(id):
    veiculo = Veiculo.query.get_or_404(id)
    
    if request.method == 'POST':
        veiculo.modelo = request.form.get('modelo')
        veiculo.marca = request.form.get('marca')
        veiculo.ano = request.form.get('ano')
        veiculo.placa = request.form.get('placa')

        db.session.commit()
        flash('Veículo atualizado com sucesso!', 'success')
        return redirect(url_for('veiculos.listar_veiculos'))
    
    return render_template('editar_veiculo.html', veiculo=veiculo)

@bp.route('/veiculos/excluir/<int:id>', methods=['POST'])
def excluir_veiculo(id):
    veiculo = Veiculo.query.get_or_404(id)
    db.session.delete(veiculo)
    db.session.commit()
    flash('Veículo excluído com sucesso!', 'success')
    return redirect(url_for('veiculos.listar_veiculos'))

@bp.route('/reservar/<int:veiculo_id>', methods=['GET', 'POST'])
def reservar(veiculo_id):
    veiculo = Veiculo.query.get_or_404(veiculo_id)
    
    if request.method == 'POST':
        usuario_id = session.get('user_id')  # Captura o ID do usuário logado
        nova_reserva = Reserva(
            veiculo_id=veiculo.id,
            usuario_id=usuario_id,
            modelo=veiculo.modelo,
            marca=veiculo.marca,
            ano=veiculo.ano,
            placa=veiculo.placa
        )
        db.session.add(nova_reserva)
        db.session.commit()
        flash('Reserva feita com sucesso!', 'success')
        return redirect(url_for('veiculos.listar_veiculos'))
    
    return render_template('reservar.html', veiculo=veiculo)

@bp.route('/menu')
def inicial():
    return render_template('index.html')

@bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = request.form['user']
        sena = request.form['sena']
        cpf = request.form['cpf']

        existing_user = User.query.filter_by(Usuario=user).first()

        if existing_user:
            flash('Este usuário já existe. Por favor, escolha outro.', 'danger')
            return redirect(url_for('veiculos.register'))  # Corrija o nome da blueprint

        usuario = User(Usuario=user, Contraseña=sena, CPF=cpf)
        db.session.add(usuario)
        db.session.commit()

        flash('Usuário registrado com sucesso.', 'success')
        return redirect(url_for('veiculos.login'))  # Corrija o nome da blueprint para a rota de login

    return render_template('register.html')

@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        sena = request.form['sena']

        usuario = User.query.filter_by(Usuario=user).first()

        if usuario and usuario.Contraseña == sena:
            session['user_id'] = usuario.id
            session['username'] = usuario.Usuario

            flash('Login realizado com sucesso', 'success')
            return redirect(url_for('veiculos.inicial'))  # Corrija para redirecionar à rota inicial na blueprint correta
        else:
            flash('Nome de usuário ou senha incorretos', 'danger')

    return render_template('login.html')

@bp.route('/usuarios')
def listar_usuarios():
    usuarios = User.query.all()
    return render_template('listar_usuarios.html', usuarios=usuarios)

@bp.route('/usuarios/adicionar', methods=['GET', 'POST'])
def adicionar_usuario():
    if request.method == 'POST':
        user = request.form['user']
        sena = request.form['sena']
        cpf = request.form['cpf']

        existing_user = User.query.filter_by(Usuario=user).first()

        if existing_user:
            flash('Este usuário já existe. Por favor, escolha outro.', 'danger')
            return redirect('/usuarios/adicionar')  # Direciona diretamente para a rota

        usuario = User(Usuario=user, Contraseña=sena, CPF=cpf)
        db.session.add(usuario)
        db.session.commit()

        flash('Usuário registrado com sucesso.', 'success')
        return redirect('/usuarios')  # Direciona para a lista de usuários

    return render_template('adicionar_usuario.html')




