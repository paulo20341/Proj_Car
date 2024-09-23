from flask import Blueprint, render_template, request, redirect, flash
from .models import Veiculo, Reserva  # Usando o ponto para referenciar o módulo dentro do pacote
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

        novo_veiculo = Veiculo(modelo=modelo, marca=marca, ano=ano, placa=placa)
        db.session.add(novo_veiculo)
        db.session.commit()
        flash('Veículo adicionado com sucesso!', 'success')
        return redirect('/veiculos')  # Redireciona para a lista de veículos
    
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
        return redirect('/veiculos')
    
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
