from flask import Blueprint
from flask_security import login_required, current_user
from flask import render_template, url_for, flash, redirect, request
from dbConfig import get_connection
import json

clientes = Blueprint('clientes', __name__,url_prefix='/clientes')

@clientes.route('/getAll')
@login_required
def getAll():
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_clientes()')
            resulset = cursor.fetchall()
            print(resulset)
            return render_template('/clientes/clientes.html', name = current_user.name, resulset=resulset, active = 'clientes')
        
    except Exception as ex:

        flash("No se encontro ningun registro en la BD: " + str(ex))
    
        return render_template('/clientes/clientes.html', name = current_user.name, active = 'clientes')

@clientes.route('/insertarCliente', methods=['GET','POST'])
@login_required
def insertar_cliente():

    if request.method == 'GET':
        return render_template('/clientes/insertarCliente.html', active = 'clientes', name = current_user.name)
    
    if request.method == 'POST':
        
        nombre = request.form['nombres']
        apellidos = request.form['apellidos']
        celular = request.form['celular']
        codigo_postal = request.form['codigo_postal']
        calle = request.form['calle']
        colonia = request.form['colonia']

        try:
            connection = get_connection()
            with connection.cursor () as cursor:
                cursor.execute('call sp_insertar_cliente(%s,%s,%s,%s,%s,%s)', (nombre, apellidos, celular, codigo_postal, calle, colonia))
                connection.commit()
                connection.close()
                flash("Registro insertado correctamente")
        except Exception as ex:

            flash("No se pude insertar el registro: " + str(ex))

        return redirect(url_for('clientes.getAll'))
    
@clientes.route('/obtenerCliente', methods=['GET','POST'])
@login_required
def obtener_cliente():
    
        if request.method == 'GET':

            id_cliente = request.args.get('id')

            try:
                connection = get_connection()
                with connection.cursor () as cursor:
                    cursor.execute('call sp_consultar_cliente_por_id(%s)', (id_cliente))
                    resulset = cursor.fetchall()
                    connection.commit()
                    connection.close()
                    return render_template('/clientes/actualizarCliente.html', resulset=resulset)
            except Exception as ex:
                        
                        flash("No se pude consultar el registro: " + str(ex))

            return redirect(url_for('clientes.getAll'))
        
@clientes.route('/actualizarCliente', methods=['POST'])
@login_required
def actualizar_cliente():
     
     if request.method == 'POST':
        
        id_cliente = request.form['id_cliente']
        nombres = request.form['nombresEdit']
        apellidos = request.form['apellidosEdit']
        celular = request.form['celularEdit']
        codigo_postal = request.form['codigo_postalEdit']
        calle = request.form['calleEdit']
        colonia = request.form['coloniaEdit']

        try:
            connection = get_connection()
            with connection.cursor () as cursor:
                cursor.execute('call sp_actualizar_cliente(%s,%s,%s,%s,%s,%s,%s)', (id_cliente, nombres, apellidos, celular, codigo_postal, calle, colonia))
                connection.commit()
                connection.close()
                flash("Registro actualizado correctamente")
                return redirect(url_for('clientes.getAll'))
        except Exception as ex:

            flash("No se pude actualizar el registro: " + str(ex))

        return redirect(url_for('clientes.getAll'))
     
@clientes.route('/eliminarCliente', methods=['GET'])
@login_required
def eliminar_cliente():
        
            if request.method == 'GET':
    
                id_cliente = request.args.get('id')
    
                try:
                    connection = get_connection()
                    with connection.cursor () as cursor:
                        cursor.execute('call sp_eliminar_cliente(%s)', (id_cliente))
                        connection.commit()
                        connection.close()
                        flash("Registro eliminado correctamente")
                except Exception as ex:
                            
                            flash("No se pude eliminar el registro: " + str(ex))
    
                return redirect(url_for('clientes.getAll'))