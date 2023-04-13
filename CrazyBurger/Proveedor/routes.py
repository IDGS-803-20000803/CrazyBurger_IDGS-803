from flask import Blueprint
from flask_security import login_required, current_user
from flask import render_template, url_for, flash, redirect, request
from dbConfig import get_connection
import json

proveedor = Blueprint('proveedor', __name__,url_prefix='/proveedor')

@proveedor.route('/getAll')
@login_required
def getAll():
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_proveedor()')
            resulset = cursor.fetchall()
            print(resulset)
            return render_template('/proveedor/proveedor.html', name = current_user.name, resulset=resulset)
        
    except Exception as ex:

        flash("No se encontro ningun registro en la BD: " + str(ex))
    
        return render_template('/proveedor/proveedor.html', name = current_user.name)
    
@proveedor.route('/insertarProveedor', methods=['GET','POST'])
@login_required
def insertar_proveedor():

    if request.method == 'GET':
        return render_template('/proveedor/insertarProveedor.html')
    
    if request.method == 'POST':
        
        razon_social = request.form['razon_social']
        rfc = request.form['rfc']
        alias = request.form['alias']
        correo = request.form['correo']
        celular = request.form['celular']
        ciudad = request.form['ciudad']
        estado = request.form['estado']
        codigo_postal = request.form['codigo_postal']
        calle = request.form['calle']
        colonia = request.form['colonia']

        try:
            connection = get_connection()
            with connection.cursor () as cursor:
                cursor.execute('call sp_insertar_proveedor(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (razon_social, rfc, alias, correo, celular, ciudad, estado, codigo_postal, calle, colonia))
                connection.commit()
                connection.close()
                flash("Registro insertado correctamente")
        except Exception as ex:

            flash("No se pude insertar el registro: " + str(ex))

        return redirect(url_for('proveedor.getAll'))
    
    return render_template('/proveedor/insertarProveedor.html')

@proveedor.route('/verProveedor', methods=['GET','POST'])
@login_required
def ver_proveedor():
    
        if request.method == 'GET':

            id_proveedor = request.args.get('id')

            try:
                connection = get_connection()
                with connection.cursor () as cursor:
                    cursor.execute('call sp_consultar_proveedor_por_id(%s)', (id_proveedor))
                    resulset = cursor.fetchall()
                    connection.commit()
                    connection.close()
                    return render_template('/proveedor/actualizarProveedor.html', resulset=resulset)
            except Exception as ex:
                        
                        flash("No se pude consultar el registro: " + str(ex))

            return redirect(url_for('proveedor.getAll'))

@proveedor.route('/actualizarProveedor', methods=['POST'])
@login_required
def actualizar_proveedor():

    if request.method == 'POST':
        
        id_proveedor = request.form['id_proveedor']
        razon_social = request.form['razon_socialEdit']
        rfc = request.form['rfcEdit']
        alias = request.form['aliasEdit']
        correo = request.form['correoEdit']
        celular = request.form['celularEdit']
        ciudad = request.form['ciudadEdit']
        estado = request.form['estadoEdit']
        codigo_postal = request.form['codigo_postalEdit']
        calle = request.form['calleEdit']
        colonia = request.form['coloniaEdit']

        try:
            connection = get_connection()
            with connection.cursor () as cursor:
                cursor.execute('call sp_actualizar_proveedor(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (id_proveedor, razon_social, rfc, alias, correo, celular, ciudad, estado, codigo_postal, calle, colonia))
                connection.commit()
                connection.close()
                flash("Registro actualizado correctamente")
                return redirect(url_for('proveedor.getAll'))
        except Exception as ex:

            flash("No se pude actualizar el registro: " + str(ex))

        return redirect(url_for('proveedor.getAll'))
    
@proveedor.route('/eliminarProveedor', methods=['GET','POST'])
@login_required
def eliminar_proveedor():
        
            if request.method == 'GET':
    
                id_proveedor = request.args.get('id')
    
                try:
                    connection = get_connection()
                    with connection.cursor () as cursor:
                        cursor.execute('call sp_eliminar_proveedor(%s)', (id_proveedor))
                        connection.commit()
                        connection.close()
                        flash("Registro eliminado correctamente")
                        return redirect(url_for('proveedor.getAll'))
                except Exception as ex:
                            
                            flash("No se pude eliminar el registro: " + str(ex))
    
                return redirect(url_for('proveedor.getAll'))