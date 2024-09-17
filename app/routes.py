from flask import Blueprint, render_template, request, redirect, url_for
from .models import Veiculo
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
        return redirect(url_for('veiculos.listar_veiculos'))
    return render_template('adicionar_veiculo.html')

@bp.route('/veiculos/editar/<int:id>', methods=['GET', 'POST'])
def editar_veiculo(id):
    veiculo = Veiculo.query.get(id)
    if request.method == 'POST':
        veiculo.modelo = request.form.get('modelo')
        veiculo.marca = request.form.get('marca')
        veiculo.ano = request.form.get('ano')
        veiculo.placa = request.form.get('placa')
        db.session.commit()
        return redirect(url_for('veiculos.listar_veiculos'))
    return render_template('editar_veiculo.html', veiculo=veiculo)

@bp.route('/veiculos/excluir/<int:id>')
def excluir_veiculo(id):
    veiculo = Veiculo.query.get(id)
    db.session.delete(veiculo)
    db.session.commit()
    return redirect(url_for('veiculos.listar_veiculos'))
