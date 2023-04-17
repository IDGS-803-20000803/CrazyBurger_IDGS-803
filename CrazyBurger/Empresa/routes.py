from flask import Flask, render_template, redirect
from flask import request
from flask import url_for
from flask import flash
from flask import Blueprint, render_template
from flask_security import login_required, current_user
from flask_security.decorators import roles_required,roles_accepted
from dbConfig import get_connection
from datetime import datetime

empresa = Blueprint('empresa', __name__,url_prefix='/empresa')

@empresa.route('/getAll')
@login_required
@roles_required('admin')
def getAll():
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_empresa()')
            resulset = cursor.fetchall()
            return render_template('/empresa/Empresa.html', name = current_user.name,fecha_actual=fecha_actual, resulset=resulset, active = 'empresa')
    except Exception as ex:
        flash("No se encontro ningun registro en la BD: " + str(ex))
    return render_template('/empresa/Empresa.html', fecha_actual=fecha_actual,name = current_user.name, active = 'empresa')

@empresa.route('/updateEmpresa', methods=['GET','POST'])
@login_required
@roles_required('admin')
def actualizar_empresa():
    if request.method == 'GET':
        id = request.args.get('id')
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call sp_consultar_empresa()')
                resulset = cursor.fetchall()
                return render_template('/empresa/ActualizarEmpresa.html',  id = id,resulset = resulset)
        except Exception as ex:
                flash("No se encontro ningun registro en la BD: " + str(ex))
        
    if request.method == 'POST':
        id = request.form.get('id')
        razon = request.form.get('razon')
        correo = request.form.get('correo')
        direccion = request.form.get('direccion')
        rfc = request.form.get('rfc')
        usuario = current_user.id
        try:
            connection = get_connection()
            with connection.cursor () as cursor:
                cursor.execute('call sp_actualizar_empresa(%s,%s,%s,%s,%s,%s)', (int(id),razon,correo,direccion,rfc,usuario))
                connection.commit()
                connection.close()
        except Exception as ex:
            flash("No se pude actualizar el registro: " + str(ex))
        return redirect(url_for('empresa.getAll'))
    return render_template('/empresa/ActualizarEmpresa.html')







