from flask import Flask, render_template, redirect
from flask import request
from flask import url_for
from flask import flash
from flask import Blueprint, render_template
from flask_security import login_required, current_user
from flask_security.decorators import roles_required,roles_accepted
from dbConfig import get_connection
from datetime import datetime
from flask import jsonify

pedidos = Blueprint('pedidos', __name__, url_prefix = '/pedido')

@pedidos.route('/historialPedidos')
@login_required
@roles_required('cliente')
def historial_pedidos():
    try:
        id_cliente = current_user.id
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_pedido_cliente(%s)',(id_cliente,))
            pedidos = cursor.fetchall()
            return render_template('/pedido/shoping_car.html', pedidos = pedidos, name = current_user.name)
    except Exception as exception:
        flash("Ocurrio un error al consultar tus pedidos: " + str(exception), 'error')
    return render_template('/pedido/shoping_car.html')

@pedidos.route('/generarPedido', methods = ['GET', 'POST'])
@login_required
@roles_required('cliente')
def generar_pedido():
    if request.method == 'GET':
        try:
            platillo_id = request.args.get('id')
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call sp_buscar_menu_id(%s)',(platillo_id,))
                platillos = cursor.fetchall()
                return render_template('/pedido/order_form.html', platillos = platillos)
        except Exception as exception:
          flash("Ocurrio un error al consultar los productos de la BD: " + str(exception), 'error')

    if request.method == 'POST':
        user_id = current_user.id
        fecha_pedido = datetime.now()
        cantidad = request.form.get('unidades')
        platillo_id = request.form.get('id')
    
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call sp_insertar_pedido(%s, %s, %s, %s)',(fecha_pedido, user_id, cantidad, platillo_id))
                connection.commit()
                connection.close()
                flash('Pedido generado correctamente')
        except Exception as ex:
          flash('No fue posible generar tu pedido' + str(ex))
        return redirect(url_for('pedidos.historial_pedidos'))
    

@pedidos.route('/modificarPedido', methods = ['GET', 'POST'])
@login_required
@roles_required('cliente')
def modificar_pedido():
        try:
            id_pedido = request.form.get('id')
            cantidad = request.form.get('unidades')
            
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call sp_actualizar_pedido(%s,%s)', (id_pedido, cantidad))
                connection.commit()
                connection.close()
                flash('Pedido Actualizado correctamente')
        except Exception as exception:
            flash("Ocurrio un error al actualizar el pedido: " + str(exception), 'error')
        return redirect(url_for('pedidos.historial_pedidos'))

@pedidos.route('/eliminarPedido')
@login_required
@roles_required('cliente')
def eliminar_pedido():
    try:
        id = request.args.get('id')
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_eliminar_detalle(%s)', (id,))
            connection.commit()
            connection.close()
            flash('Pedido eliminado del carrito')
    except Exception as exception:
        flash("Ocurrio un error al eliminar el pedido: " + str(exception), 'error')
    return redirect(url_for('pedidos.historial_pedidos'))
