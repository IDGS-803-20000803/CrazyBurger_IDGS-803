from flask import Flask, render_template, redirect
from flask import request
from flask import url_for
from flask import flash
from flask import Blueprint, render_template
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from dbConfig import get_connection
from datetime import datetime

pedidos = Blueprint("pedidos", __name__, url_prefix="/pedido")


@pedidos.route("/historialPedidos")
@login_required
@roles_required("cliente")
def historial_pedidos():
    try:
        id_cliente = current_user.id
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("call sp_consultar_orden(%s)", (id_cliente,))
            pedidos = cursor.fetchall()
            return render_template(
                "shoping_car.html", pedidos=pedidos, name=current_user.name
            )
    except Exception as exception:
        flash("Ocurrio un error al consultar tus pedidos: " + str(exception), "error")
    return render_template("shoping_car.html")


@pedidos.route("/generarPedido", methods=["GET", "POST"])
@login_required
@roles_required("cliente")
def generar_pedido():
    if request.method == "GET":
        try:
            platillo_id = request.args.get("id")
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("call sp_buscar_producto_id(%s)", (platillo_id,))
                platillos = cursor.fetchall()
                return render_template("order_form.html", platillos=platillos)
        except Exception as exception:
            flash(
                "Ocurrio un error al consultar los productos de la BD: "
                + str(exception),
                "error",
            )

    if request.method == "POST":
        user_id = current_user.id
        fecha_pedido = datetime.now()
        cantidad = request.form.get("unidades")
        platillo_id = request.form.get("id")

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "call sp_insertar_orden(%s, %s, %s, %s)",
                    (fecha_pedido, user_id, cantidad, platillo_id),
                )
                connection.commit()
                connection.close()
                flash("Pedido generado correctamente")
        except Exception as ex:
            flash("No fue posible generar tu pedido" + str(ex))
        return redirect(url_for("pedidos.historial_pedidos"))
    return render_template("order_form.html")


@pedidos.route("/modificarPedido", methods=["POST"])
@login_required
@roles_required("cliente")
def modificar_pedido():
    try:
        id_pedido = request.form.get("id")
        cantidad = request.form.get("unidades")
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("call sp_actualiar_orden(%s,%s)", (id_pedido, cantidad))
            connection.commit()
            connection.close()
            flash("Pedido Actualizado correctamente")
    except Exception as exception:
        flash("Ocurrio un error al actualizar el pedido: " + str(exception), "error")
    return redirect(url_for("pedidos.historial_pedidos"))


@pedidos.route("/eliminarPedido", methods=["GET"])
@login_required
@roles_required("cliente")
def eliminar_pedido():
    try:
        id = request.args.get("id")
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("call sp_delete_orden(%s)", (id,))
            connection.commit()
            connection.close()
            flash("Pedido eliminado del carrito")
    except Exception as exception:
        flash("Ocurrio un error al eliminar el pedido: " + str(exception), "error")
    return redirect(url_for("pedidos.historial_pedidos"))


@pedidos.route("/perfilUsuario", methods=["GET", "POST"])
@login_required
@roles_required("cliente")
def perfil_usuario():
    if request.method == "GET":
        try:
            id = request.args.get("id")
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("call sp_actualizar_usuario(%s)", (id,))
                resulset = cursor.fetchall()
                return render_template("perfil_usuario.html", resulset=resulset)
        except Exception as exception:
            flash(
                "No fue posible encontrar la información del usuario: "
                + str(exception),
                "error",
            )

    if request.method == "POST":
        try:
            id = request.form.get("id")
            nombres = request.form.get("name")
            apellidos = request.form.get("lastname")
            celular = request.form.get("phone")
            calle = request.form.get("street")
            colonia = request.form.get("col")
            cp = request.form.get("cp")

            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "call sp_actualizar_cliente(%s, %s, %s, %s, %s, %s, %s)",
                    (id, nombres, apellidos, celular, cp, calle, colonia),
                )
                connection.commit()
                connection.close()
                flash("Perfil de usuario actualizado correctamente")
                return redirect(url_for("main.productos"))
        except Exception as exception:
            flash(
                "No fue posible actualizar el perfil de usuario" + str(exception),
                "error",
            )
    return render_template("perfil_usuario.html")
