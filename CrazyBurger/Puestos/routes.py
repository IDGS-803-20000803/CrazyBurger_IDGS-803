
from flask import Flask, render_template, redirect
from flask import request
from flask import url_for
from flask import flash
from flask import Blueprint, render_template
from flask_security import login_required, current_user
from flask_security.decorators import roles_required,roles_accepted
from dbConfig import get_connection
from datetime import datetime

puestos = Blueprint('puestos', __name__,url_prefix='/puesto')

@puestos.route('/getAll')
@login_required
@roles_required('admin')
def getAll():
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_puestos()')
            resulset = cursor.fetchall()
            return render_template('puestos.html', name = current_user.name,fecha_actual=fecha_actual, resulset=resulset)
    except Exception as ex:
        flash("No se encontro ningun registro en la BD: " + str(ex))
    return render_template('puestos.html', fecha_actual=fecha_actual,name = current_user.name)

@puestos.route('/insert')
@login_required
@roles_required('admin')
def insert():
    return render_template('/puesto/InsertarPuesto.html')

@puestos.route('/insertPuesto',methods=["GET","POST"])
@login_required
@roles_required('admin')
def insertPuesto():
    if request.method == 'POST':
        puesto = request.form.get('puesto')
        descripcion = request.form.get('descripcion')

    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_insertar_puesto(%s,%s)',(puesto,descripcion))
            connection.commit()
            connection.close()
    except Exception as ex:
            flash("Ocurrio un error al registrar el nuevo puesto: " + str(ex))
            return redirect(url_for('puestos.insert'))
    return redirect(url_for('puestos.getAll'))

@puestos.route('/updatePuesto', methods=['GET','POST'])
def actualizar_puesto():
    if request.method == 'GET':
        id = request.args.get('id')
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call sp_buscar_puesto(%s)', (int(id)))
                resulset = cursor.fetchall()
                return render_template('/puesto/ActualizarPuesto.html',  id = id,resulset = resulset)
        except Exception as ex:
                flash("No se encontro ningun registro en la BD: " + str(ex))
        
    if request.method == 'POST':
        id = request.form.get('id')
        puesto = request.form.get('puesto')
        descripcion = request.form.get('descripcion')
        usuario = current_user.id
        try:
            connection = get_connection()
            with connection.cursor () as cursor:
                cursor.execute('call sp_actualizar_puesto(%s,%s,%s,%s)', (int(id),puesto,descripcion,usuario))
                connection.commit()
                connection.close()
        except Exception as ex:
            flash("No se pude actualizar el registro: " + str(ex))
        return redirect(url_for('puestos.getAll'))
    return render_template('/puesto/ActualizarPuesto.html')

@puestos.route('/deletePuesto', methods=['GET','POST'])
def eliminar_puesto():
    if request.method == 'GET':
        id = request.args.get('id')
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call sp_buscar_puesto(%s)', (int(id)))
                resulset = cursor.fetchall()
                return render_template('/puesto/EliminarPuesto.html',  id = id,resulset = resulset)
        except Exception as ex:
                flash("No se encontro ningun registro en la BD: " + str(ex))
        
    if request.method == 'POST':
        id = request.form.get('id')
        usuario = current_user.id
        try:
            connection = get_connection()
            with connection.cursor () as cursor:
                cursor.execute('call sp_delete_puesto(%s,%s)', (int(id), usuario))
                connection.commit()
                connection.close()
        except Exception as ex:
            flash("No se pude eliminar el registro: " + str(ex))
        return redirect(url_for('puestos.getAll'))
    return render_template('/puesto/EliminarPuesto.html')