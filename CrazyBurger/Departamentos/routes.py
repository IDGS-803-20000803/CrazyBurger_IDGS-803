from flask import Flask, render_template, redirect
from flask import request
from flask import url_for
from flask import flash
from flask import Blueprint, render_template
from flask_security import login_required, current_user
from flask_security.decorators import roles_required,roles_accepted
from dbConfig import get_connection
from datetime import datetime

departamento = Blueprint('departamento', __name__,url_prefix='/departamento')

@departamento.route('/getAll')
@login_required
@roles_required('admin')
def getAll():
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_departamentos()')
            resulset = cursor.fetchall()
            return render_template('/departamento/Departamento.html', name = current_user.name,fecha_actual=fecha_actual, resulset=resulset)
    except Exception as ex:
        flash("No se encontro ningun registro en la BD: " + str(ex))
    return render_template('/departamento/Departamento.html', fecha_actual=fecha_actual,name = current_user.name)

@departamento.route('/insert')
@login_required
@roles_required('admin')
def insert():
    return render_template('/departamento/InsertarDepart.html')

@departamento.route('/insertDepartamento',methods=["GET","POST"])
@login_required
@roles_required('admin')
def insertDepartamento():
    if request.method == 'POST':
        departamento = request.form.get('departamento')
        descripcion = request.form.get('descripcion')

    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_insertar_depart(%s,%s)',(departamento,descripcion))
            connection.commit()
            connection.close()
    except Exception as ex:
            flash("Ocurrio un error al registrar el nuevo departamento: " + str(ex))
            return redirect(url_for('departamento.insert'))
    return redirect(url_for('departamento.getAll'))


@departamento.route('/updateDepart', methods=['GET','POST'])
@login_required
@roles_required('admin')
def actualizar_depart():
    if request.method == 'GET':
        id = request.args.get('id')
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call sp_buscar_depart(%s)', (int(id)))
                resulset = cursor.fetchall()
                return render_template('/departamento/ActualizarDepart.html',  id = id,resulset = resulset)
        except Exception as ex:
                flash("No se encontro ningun registro en la BD: " + str(ex))
        
    if request.method == 'POST':
        id = request.form.get('id')
        departamento = request.form.get('departamento')
        descripcion = request.form.get('descripcion')
        usuario = current_user.id
        try:
            connection = get_connection()
            with connection.cursor () as cursor:
                cursor.execute('call sp_actualizar_depart(%s,%s,%s,%s)', (int(id),departamento,descripcion,usuario))
                connection.commit()
                connection.close()
        except Exception as ex:
            flash("No se pude actualizar el registro: " + str(ex))
        return redirect(url_for('departamento.getAll'))
    return render_template('/departamento/ActualizarDepart.html')

@departamento.route('/deleteDepart', methods=['GET','POST'])
@login_required
@roles_required('admin')
def eliminar_depart():
    if request.method == 'GET':
        id = request.args.get('id')
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call sp_buscar_depart(%s)', (int(id)))
                resulset = cursor.fetchall()
                return render_template('/departamento/EliminarDepart.html',  id = id,resulset = resulset)
        except Exception as ex:
                flash("No se encontro ningun registro en la BD: " + str(ex))
        
    if request.method == 'POST':
        id = request.form.get('id')
        usuario = current_user.id
        try:
            connection = get_connection()
            with connection.cursor () as cursor:
                cursor.execute('call sp_delete_depart(%s,%s)', (int(id), usuario))
                connection.commit()
                connection.close()
        except Exception as ex:
            flash("No se pude eliminar el registro: " + str(ex))
        return redirect(url_for('departamento.getAll'))
    return render_template('/departamento/EliminarDepart.html')

