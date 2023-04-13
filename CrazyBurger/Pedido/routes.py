from flask import Flask, render_template, redirect
from flask import request
from flask import url_for
from flask import flash
from flask import Blueprint, render_template
from flask_security import login_required, current_user
from flask_security.decorators import roles_required,roles_accepted
from dbConfig import get_connection
from datetime import datetime

pedidos = Blueprint('pedidos', __name__, url_prefix = '/pedido')

@pedidos.route('/historialPedidos')
def historial_pedidos():
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call show_order()')
            pedidos = cursor.fetchall()
            return render_template('shoping_car.html', pedidos = pedidos)
    except Exception as ex:
        flash('ERROR: No se encontro ningun platillo en la BD' + str(ex))
    return render_template('shoping_car.html')

@pedidos.route('generarPedido', methods = ['GET', 'POST'])
def generar_pedido():
    if request.method == 'GET':
        try:
            platillo_id = request.args.get('id')
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call show_product_id(%s)',(int(platillo_id)))
                platillos = cursor.fetchall()
                return render_template('order_form.html', platillos = platillos)
        except Exception as ex:
          flash('No se encontro el producto' + str(ex))

    if request.method == 'POST':
        user_id = current_user.id
        fecha_pedido = datetime.now()
        cantidad = request.form.get('unidades')
        platillo_id = request.form.get('id')

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call new_order(%s, %s, %s, %s)',(fecha_pedido, user_id, cantidad, platillo_id))
                connection.commit()
                connection.close()
                flash('Pedido generado correctamente')
        except Exception as ex:
          flash('No fue posible generar tu pedido' + str(ex))
        return redirect(url_for('pedidos.historial_pedidos'))
    return render_template('order_form.html')

@pedidos.route('/modificarPedido', methods = ['GET', 'POST'])
def modificar_pedido():
    try:
        pass
    except Exception as ex:
        flash('' + str(ex))
    return render_template('')

@pedidos.route('/eliminarPedido', methods = ['GET'])
def eliminar_pedido():
    try:
        id = request.args.get('id')
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call delete_order(%s)', (id))
            connection.commit()
            connection.close()
            flash('Pedido eliminado del carrito')
    except Exception as ex:
        flash('No fue posible eliminar el pedido del carrito' + str(ex), Warning)
    return redirect(url_for('pedidos.historial_pedidos'))