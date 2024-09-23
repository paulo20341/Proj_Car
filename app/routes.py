from flask import Blueprint, render_template, request, redirect, flash, session
from sqlalchemy.exc import IntegrityError
from .models import Veiculo, Reserva, Usuario  # Certifique-se de que Usuario esteja definido
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

bp = Blueprint('veiculos', __name__)

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

        # Verificar se a placa já existe
        if Veiculo.query.filter_by(placa=placa).first():
            flash('Erro: A placa já está registrada!', 'danger')
            return redirect('/veiculos/adicionar')

        novo_veiculo = Veiculo(modelo=modelo, marca=marca, ano=ano, placa=placa)

        try:
            db.session.add(novo_veiculo)
            db.session.commit()
            flash('Veículo adicionado com sucesso!', 'success')
            return redirect('/veiculos')
        except IntegrityError:
            db.session.rollback()  # Desfaz a transação em caso de erro
            flash('Erro: Não foi possível adicionar o veículo. Verifique os dados.', 'danger')
            return redirect('/veiculos/adicionar')

    return render_template('adicionar_veiculo.html')

@bp.route('/veiculos/editar/<int:id>', methods=['GET', 'POST'])
def editar_veiculo(id):
    veiculo = Veiculo.query.get_or_404(id)
    
    if request.method == 'POST':
        veiculo.modelo = request.form.get('modelo')
        veiculo.marca = request.form.get('marca')
        veiculo.ano = request.form.get('ano')
        veiculo.placa = request.form.get('placa')

        try:
            db.session.commit()
            flash('Veículo atualizado com sucesso!', 'success')
            return redirect('/veiculos')
        except IntegrityError:
            db.session.rollback()
            flash('Erro: A placa já está registrada!', 'danger')
            return redirect(f'/veiculos/editar/{id}')

    return render_template('editar_veiculo.html', veiculo=veiculo)

@bp.route('/veiculos/excluir/<int:id>', methods=['POST'])
def excluir_veiculo(id):
    veiculo = Veiculo.query.get_or_404(id)
    db.session.delete(veiculo)
    db.session.commit()
    flash('Veículo excluído com sucesso!', 'success')
    return redirect('/veiculos')

@bp.route('/reservar/<int:veiculo_id>', methods=['GET', 'POST'])
def reservar(veiculo_id):
    veiculo = Veiculo.query.get_or_404(veiculo_id)
    
    if request.method == 'POST':
        usuario_id = request.form.get('usuario_id')
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
        return redirect('/veiculos')
    
    return render_template('reservar.html', veiculo=veiculo)




@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        # Verificar se o e-mail já existe
        if Usuario.query.filter_by(email=email).first():
            flash('Erro: O e-mail já está registrado!', 'danger')
            return redirect('/login')

        # Criar novo usuário
        novo_usuario = Usuario(
            nome=nome,
            email=email,
            senha=generate_password_hash(senha)
        )

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Usuário registrado com sucesso! Você pode fazer login agora.', 'success')
            return redirect('/login')
        except IntegrityError:
            db.session.rollback()
            flash('Erro: Não foi possível registrar o usuário. Verifique os dados.', 'danger')
            return redirect('/login')

    usuarios = Usuario.query.all()  # Busca todos os usuários
    return render_template('login.html', usuario=usuarios)  # Passa a lista de usuários para o template
