from flask import Flask, render_template, redirect
from flask import request
from flask import url_for
from flask import flash
from flask import Blueprint, render_template
from flask_security import login_required, current_user
from flask_security.decorators import roles_required,roles_accepted
from dbConfig import get_connection
from datetime import datetime
from decimal import Decimal

ingrediente = Blueprint('ingrediente', __name__,url_prefix='/ingrediente')

@ingrediente.route('/getAll')
@login_required
@roles_required('admin')
def getAll():
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_ingredientes()')
            resulset = cursor.fetchall()
            return render_template('/ingrediente/ingrediente.html', name = current_user.name,fecha_actual=fecha_actual, resulset=resulset)
    except Exception as ex:
        flash("No se encontro ningun registro en la BD: " + str(ex))
    return render_template('/ingrediente/ingrediente.html', fecha_actual=fecha_actual,name = current_user.name)

@ingrediente.route('/insert')
@login_required
@roles_required('admin')
def insert():
    return render_template('/ingrediente/InsertarIngrediente.html')

@ingrediente.route('/insertIngrediente',methods=["GET","POST"])
@login_required
@roles_required('admin')
def insertIngrediente():
    if request.method == 'POST':
        ingrediente = request.form.get('ingrediente')
        unidad = request.form.get('unidad')
        stock = request.form.get('stock')
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_insertar_ingrediente(%s,%s,%s)',(ingrediente,unidad,Decimal(stock)))
            connection.commit()
            connection.close()
    except Exception as ex:
            flash("Ocurrio un error al registrar el nuevo ingrediente: " + str(ex))
            return redirect(url_for('ingrediente.insert'))
    return redirect(url_for('ingrediente.getAll'))

@ingrediente.route('/updateIngrediente', methods=['GET','POST'])
@login_required
@roles_required('admin')
def actualizar_ingrediente():
    if request.method == 'GET':
        id = request.args.get('id')
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call sp_buscar_ingrediente(%s)', (int(id)))
                resulset = cursor.fetchall()
                return render_template('/ingrediente/ActualizarIngrediente.html',  id = id,resulset = resulset)
        except Exception as ex:
                flash("No se encontro ningun registro en la BD: " + str(ex))
        
    if request.method == 'POST':
        id = request.form.get('id')
        ingrediente = request.form.get('ingrediente')
        unidad = request.form.get('unidad')
        stock = request.form.get('stock')
        usuario = current_user.id
        try:
            connection = get_connection()
            with connection.cursor () as cursor:
                cursor.execute('call sp_actualizar_ingrediente(%s,%s,%s,%s,%s)', (int(id),ingrediente,unidad,Decimal(stock),usuario))
                connection.commit()
                connection.close()

                
        except Exception as ex:
            flash("No se pude actualizar el registro: " + str(ex))
        return redirect(url_for('ingrediente.getAll'))
    return render_template('/ingrediente/ActualizarIngrediente.html')

@ingrediente.route('/deleteIngrediente', methods=['GET','POST'])
@login_required
@roles_required('admin')
def eliminar_ingrediente():
    if request.method == 'GET':
        id = request.args.get('id')
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call sp_buscar_ingrediente(%s)', (int(id)))
                resulset = cursor.fetchall()
                return render_template('/ingrediente/EliminarIngrediente.html',  id = id,resulset = resulset)
        except Exception as ex:
                flash("No se encontro ningun registro en la BD: " + str(ex))
        
    if request.method == 'POST':
        id = request.form.get('id')
        usuario = current_user.id
        try:
            connection = get_connection()
            with connection.cursor () as cursor:
                cursor.execute('call sp_delete_ingrediente(%s,%s)', (int(id),usuario))
                connection.commit()
                connection.close()              
        except Exception as ex:
            flash("No se pude actualizar el registro: " + str(ex))
        return redirect(url_for('ingrediente.getAll'))
    return render_template('/ingrediente/EliminarIngrediente.html')


