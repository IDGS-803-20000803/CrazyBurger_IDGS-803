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

inventario = Blueprint('inventario', __name__,url_prefix='/inventario')

@inventario.route('/getAll')
@login_required
@roles_accepted('admin','empleado')
def getAll():
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    usuario = current_user.id
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_inventario(%s,%s)', (usuario,fecha_actual))
            resulset = cursor.fetchall()
            connection.commit()
            connection.close()
            print(resulset)
            return render_template('/inventario/Inventario.html', name = current_user.name,fecha_actual=fecha_actual, resulset=resulset, active = 'inventario')
    except Exception as ex:
        flash("No se encontro ningun registro en la BD: " + str(ex))
    return render_template('/inventario/Inventario.html', fecha_actual=fecha_actual,name = current_user.name, active = 'inventario')

@inventario.route('/getEntrada')
@login_required
@roles_accepted('admin','empleado')
def getEntrada():
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_entradas()')
            resulset = cursor.fetchall()
            return render_template('/inventario/Entrada.html', name = current_user.name,fecha_actual=fecha_actual, resulset=resulset, active = 'inventario')
    except Exception as ex:
        flash("No se encontro ningun registro en la BD: " + str(ex))
    return render_template('/inventario/Entrada.html', fecha_actual=fecha_actual,name = current_user.name, active = 'inventario')

@inventario.route('/insertarEntrada', methods=['GET','POST'])
@login_required
@roles_accepted('admin','empleado')
def insertarEntrada():

    if request.method == 'GET':

        # Buscar los tipos de entrada
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_tipo_entrada()')
            tipoEntrada = cursor.fetchall()
        
        # Buscar los proveedores
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_proveedor()')
            proveedor = cursor.fetchall()
        
        # Buscar los ingredientes
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_ingredientes()')
            ingrediente = cursor.fetchall()

        return render_template('/inventario/insertarEntrada.html', name = current_user.name, tipoEntrada=tipoEntrada, proveedor=proveedor, ingrediente= ingrediente)
    if request.method == 'POST':
        
        vencimiento = request.form['vencimiento']
        ingrediente_id = request.form['ingrediente_id']
        cantidad = request.form['cantidad']
        unidad = request.form['unidad']
        tipo_entrada_id = request.form['tipo_entrada_id']
        proveedor_id = request.form['proveedor_id']
        usuario = current_user.id
        print(vencimiento)
        
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call sp_insertar_entrada(%s,%s,%s,%s,%s,%s,%s)',(vencimiento,ingrediente_id,cantidad,unidad,tipo_entrada_id,proveedor_id,usuario))
                connection.commit()
                flash("Entrada insertada correctamente")
                return redirect(url_for('inventario.getEntrada'))
        except Exception as ex:
            flash("Error al insertar la entrada: " + str(ex))
            return redirect(url_for('inventario.getEntrada'))
    
@inventario.route('/getSalida')
@login_required
@roles_accepted('admin','empleado')
def getSalida():
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_salidas()')
            resulset = cursor.fetchall()
            return render_template('/inventario/Salida.html', name = current_user.name,fecha_actual=fecha_actual, resulset=resulset, active = 'inventario')
    except Exception as ex:
        flash("No se encontro ningun registro en la BD: " + str(ex))
    return render_template('/inventario/Salida.html', fecha_actual=fecha_actual,name = current_user.name, active = 'inventario')


@inventario.route('/InventarioInfo', methods=['GET','POST'])
@login_required
@roles_accepted('admin','empleado')
def InventarioInfo():

    if request.method == 'GET':

        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        usuario = current_user.id
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call sp_consultar_inventory()')
                resulset = cursor.fetchall()
                return render_template('/inventario/InventarioInfo.html', name = current_user.name,fecha_actual=fecha_actual, resulset=resulset, active = 'inventario')
        except Exception as ex:
            flash("No se encontro ningun registro en la BD: " + str(ex))
        return render_template('/inventario/InventarioInfo.html', fecha_actual=fecha_actual,name = current_user.name, active = 'inventario')
    

@inventario.route('/insertSalida', methods=['GET','POST'])
@login_required
@roles_accepted('admin','empleado')
def insertSalida():
    if request.method == 'GET':
        id = request.args.get('id')
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call sp_consultar_tipo_salida()')
                tipoSalida = cursor.fetchall()

            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call sp_consultar_inventario_id(%s)', (id))
                resulset = cursor.fetchall()
                connection.commit()
                connection.close()

                return render_template('/inventario/InsertarSalida.html',  id = id,resulset = resulset,tipoSalida=tipoSalida)
        except Exception as ex:
                flash("No se encontro ningun registro en la BD: " + str(ex))
                return redirect(url_for('inventario.InventarioInfo'))
        
    if request.method == 'POST':
        id = request.form.get('id')
        cantidad = request.form.get('cantidad')
        tipo_salida_id = request.form.get('tipo_salida_id')
        usuario = current_user.id
        id_ingrediente= request.form.get('id_ingrediente')
        unidad = request.form.get('unidad')
        print(id)
        print(cantidad)
        print(tipo_salida_id)
        print(usuario)
        print(id_ingrediente)
        print(unidad)
        try:
            connection = get_connection()
            with connection.cursor () as cursor:
                cursor.execute('call sp_insertar_salida_invent(%s,%s,%s,%s,%s,%s)', (id,cantidad,tipo_salida_id,usuario, id_ingrediente, unidad))
                connection.commit()
                connection.close()
        except Exception as ex:
            flash("No se puede realizar el registro: " + str(ex))
        return redirect(url_for('inventario.InventarioInfo'))
    return redirect(url_for('inventario.InventarioInfo'))