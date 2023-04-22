from flask import Flask, render_template, redirect, Response
from flask import request
from flask import url_for
from flask import flash
from flask import Blueprint, render_template
from flask_security import login_required, current_user
from flask_security.decorators import roles_accepted, roles_required
from dbConfig import get_connection
from datetime import datetime
from flask import make_response
from io import BytesIO
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A7
from reportlab.graphics.shapes import Image,Drawing
from reportlab.lib.utils import ImageReader
from reportlab.graphics import renderPDF


compras = Blueprint('compras',__name__,url_prefix='/compras')

@compras.route('/confirmarCompra')
@login_required
@roles_required('cliente')
def confirmarCompra():
    try:
        id_cliente = current_user.id
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_realizar_venta(%s)',(id_cliente))
            connection.commit()
            connection.close()
            flash('Compra realizada con exito')
            return redirect(url_for('pedidos.historial_pedidos'))
    except Exception as exception:
        flash("Ocurrio un error al consultar tus compras: " + str(exception), 'error')
    return redirect(url_for('pedidos.historial_pedidos'))



###################################################################################################

@compras.route('/comprasGuardadas')
@login_required
@roles_required('cliente')
def comprasGuardadas():
    try:
        user_id = current_user.id
        print(user_id)
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_venta(%s)',(user_id))
            detalle = cursor.fetchall()
            return render_template('/compras/historial_compras.html',detalle= detalle, name = current_user.name)
    except Exception as exception:
        flash('Ocurrio un error al consultar tus compras' + str(exception), 'error')

    return render_template('/compras/historial_compras.html')  


@compras.route('/comprasCamino')
@login_required
@roles_required('cliente')
def comprasCamino():
    try:
        user_id = current_user.id
        print(user_id)
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_venta_Camino(%s)',(user_id))
            detalle = cursor.fetchall()
            return render_template('/compras/historial_compras.html',detalle= detalle, name = current_user.name)
    except Exception as exception:
        flash('Ocurrio un error al consultar tus compras' + str(exception), 'error')
    return render_template('/compras/historial_compras.html')  

@compras.route('/comprasCompletadas')
@login_required
@roles_required('cliente')
def comprasCompletadas():
    try:
        user_id = current_user.id
        print(user_id)
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_venta_entregada(%s)',(user_id))
            detalle = cursor.fetchall()
            return render_template('/compras/historial_compras.html',detalle= detalle, name = current_user.name)
    except Exception as exception:
        flash('Ocurrio un error al consultar tus compras' + str(exception), 'error')
    return render_template('/compras/historial_compras.html')  


@compras.route('/totalcompras')
@login_required
@roles_accepted('admin','empleado')
def totalcompras():
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_ventas_general()',())
            venta = cursor.fetchall()
            return render_template('/compras/ventas.html',detalle= venta)
    except Exception as exception:
        flash('Ocurrio un error al consultar tus compras' + str(exception), 'error')

    return render_template('/compras/ventas.html')  


@compras.route('/enviarVenta', methods = ['GET'])
@login_required
@roles_accepted('admin','empleado')
def enviarVenta():
    try:
        id = request.args.get('id')
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_enviar_venta(%s)', (id,))
            connection.commit()
            connection.close()
            flash('La venta a sido enviada')
    except Exception as exception:
        flash("Ocurrio un error al eliminar el pedido: " + str(exception), 'error')
    return redirect(url_for('compras.totalcompras'))


@compras.route('/finalizarVenta', methods = ['GET'])
@login_required
@roles_accepted('admin','empleado')
def finalizarVenta():
    try:
        id = request.args.get('id')
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_venta_entregada(%s)', (id,))
            connection.commit()
            connection.close()
            flash('La venta a sido Entregada')
    except Exception as exception:
        flash("Ocurrio un error al eliminar el pedido: " + str(exception), 'error')
    return redirect(url_for('compras.totalcompras'))


@compras.route('/ticket', methods=['POST'])
@login_required
@roles_required('cliente')
def ticket():

    if request.method == 'POST':
        idPedido = request.form.get('id')
        Nombre_Producto = request.form.get('nombreProducto')
        fechaCompra = request.form.get('fechaCompra')
        precioProducto = request.form.get('PrecioProducto')
        cantidad=request.form.get('unidades')
        subtotal=request.form.get('subtotal')
        total=request.form.get('totalPagar')
    
        print(idPedido, Nombre_Producto, fechaCompra, precioProducto, cantidad, subtotal,  total)
    
        # Crear el objeto BytesIO para almacenar el PDF generado
        buffer = BytesIO()
    
        # Configurar el tamaño de la página y los márgenes
        width, height = A7
        margin = 5*mm
    
        # Crear el objeto canvas
        p = canvas.Canvas(buffer, pagesize=A7)
    
        # Agregar el logo del restaurante
    
        # Agregar el título del ticket
        p.setFont('Helvetica-Bold', 10)
        p.drawCentredString(width/2, height-30*mm, 'CRAZY BURGER')
    
        # Agregar la información del cliente
        p.setFont('Helvetica', 8)
        p.drawString(margin, height-45*mm, f'Id Compra:{idPedido}')
        p.drawString(margin, height-50*mm, f'Nombre Producto:{Nombre_Producto}')
        p.drawString(margin, height-55*mm, f'Fecha de Compra:{fechaCompra}')
    
        # Agregar la lista de productos
        p.setFont('Helvetica-Bold', 8)
        p.drawString(margin, height-65*mm, 'Productos')
        p.setFont('Helvetica', 8)
        y = height-70*mm
    
        # Agregar el total
        p.setFont('Helvetica-Bold', 8)
        p.drawString(margin, y-5*mm, 'Total')
        p.drawRightString(width-margin, y-5*mm, f':{total}')
    
        # Agregar el pie de página
        p.setFont('Helvetica', 6)
        p.drawString(margin, margin, 'Gracias por su Compra')
    
        # Guardar el PDF generado en el objeto BytesIO y cerrar el canvas
        p.showPage()
        p.save()
        buffer.seek(0)
        response = make_response(buffer.getvalue())
        response.headers.set('Content-Type', 'application/pdf')
        response.headers.set('Content-Disposition', 'attachment', filename='ticket.pdf')
        return response
    
    