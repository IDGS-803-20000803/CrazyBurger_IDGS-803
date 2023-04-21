from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_security.decorators import roles_required
from dbConfig import get_connection
from datetime import datetime

compras = Blueprint('compras', __name__, url_prefix='/compras')

@compras.route('/getAll')
@login_required
@roles_required('admin')
def getAll():

    try:
        
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_compras()')
            resulset = cursor.fetchall()

            lista = list(resulset)

            # Bucar proveedor
            for i in range(len(lista)):
                cursor.execute('call sp_consultar_proveedor_compra(%s)', (lista[i][9]))
                proveedor = cursor.fetchall()

                # Bucar empleado
                cursor.execute('call sp_consultar_empleado_compra(%s)', (lista[i][10]))
                empleado = cursor.fetchall()

                lista[i] = lista[i] + (proveedor[0][3],) + (empleado[0][1] +  ' ' + empleado[0][2] + ' ' + empleado[0][3] ,)

            resulset = tuple(lista)

            return render_template('/compras/compras.html', resulset=resulset, active = 'compras', name = current_user.name)
        
    except Exception as ex:
        
        print(ex)     
        
        return render_template('/compras/compras.html', active = 'compras', name = current_user.name)

@compras.route('/insertarCompra', methods=['GET','POST'])
@login_required
@roles_required('admin')
def insertarCompra():

    if request.method == 'GET':

        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute('call sp_consultar_proveedor()')
                proveedores = cursor.fetchall()

                return render_template('/compras/insertarCompra.html', proveedores=proveedores, active = 'compras', name = current_user.name)
            
        except Exception as ex:
                
                print(ex)     
            
                return render_template('/compras/insertarCompra.html', active = 'compras', name = current_user.name)


    if request.method == 'POST':

        tipo_conmpra = request.form['compra']

        other = request.form['otherCompra']
        nm = request.form['nombre']

        if tipo_conmpra == 'Other':
            nombre = other
        else:
            nombre = nm

        cantidad = request.form['cantidad']
        unidad_medida = request.form['unidadMedida']
        proveedor = request.form['sltProveedor']

        observaciones = request.form['observaciones']

        try:
            connection = get_connection()

            with connection.cursor () as cursor:
                cursor.execute('call sp_insertar_compra(%s, %s, %s, %s, %s, %s, %s)', (tipo_conmpra, nombre, cantidad, unidad_medida, current_user.id, proveedor, observaciones))
                connection.commit()
                connection.close()
                flash("Registro insertado correctamente")
                redirect(url_for('compras.getAll'))
        except Exception as ex:

            flash("No se pude insertar el registro: " + str(ex))

        return redirect(url_for('compras.getAll'))

@compras.route('/obtenerCompra', methods=['GET','POST'])
@login_required
@roles_required('admin')
def obtenerCompra():

    if request.method == 'GET':

        compra_id = request.args.get('id')

        connection = get_connection()
        with connection.cursor () as cursor:
            cursor.execute('call sp_consultar_compra_por_id(%s)', (compra_id))
            resulset = cursor.fetchall()

            cursor.execute('call sp_consultar_proveedor()')
            proveedores = cursor.fetchall()
    
        
        return render_template('/compras/actualizarCompra.html', resulset=resulset, active = 'compras', name = current_user.name, proveedores=proveedores)

@compras.route('/actualizarCompra', methods=['POST'])
@login_required
@roles_required('admin')
def actualizarCompra():

    compra_id = request.form['id']
    tipo_conmpra = request.form['compraEdit']

    other = request.form['otherCompraEdit']
    nm = request.form['nombreEdit']

    if tipo_conmpra == 'Other':
        nombre = other
    else:
        nombre = nm

    cantidad = request.form['cantidadEdit']
    unidad_medida = request.form['unidadMedidaEdit']
    proveedor = request.form['sltProveedorEdit']

    observaciones = request.form['observacionesEdit']

    try:

        connection = get_connection()
        with connection.cursor () as cursor:
            cursor.execute('call sp_actualizar_compra(%s, %s, %s, %s, %s, %s, %s, %s)', (compra_id, tipo_conmpra, nombre, cantidad, unidad_medida, current_user.id, proveedor, observaciones))
            connection.commit()
            connection.close()
            redirect(url_for('compras.getAll'))

    except Exception as ex:
            
        print(ex)

        return redirect(url_for('compras.getAll'))


    # # Retornar respuesta en formato JSON
    # response = {
    #     'status': 'success',
    # }

    # return response

@compras.route('/eliminarCompra', methods=['GET'])
@login_required
@roles_required('admin')
def eliminarCompra():

    compra_id = request.args.get('id')

    try:

        connection = get_connection()
        with connection.cursor () as cursor:
            cursor.execute('call sp_eliminar_compra(%s)', (compra_id))
            connection.commit()

            response = {
                'status': 'success',
            }

            return response

    except Exception as ex:
            
        print(ex)

        return redirect(url_for('compras.getAll'))