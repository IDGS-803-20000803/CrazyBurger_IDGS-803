from flask import Flask, render_template, redirect
from flask import request
from flask import url_for
from flask import flash
import uuid
import os
from flask import Blueprint, render_template
from flask_security import login_required, current_user
from flask_security.decorators import roles_required,roles_accepted
from dbConfig import get_connection
from datetime import datetime
from decimal import Decimal

receta = Blueprint('receta', __name__,url_prefix='/receta')

@receta.route('/getAll')
@login_required
@roles_required('admin')
def getAll():
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_receta()')
            resulset = cursor.fetchall()
            return render_template('/receta/Receta.html', name = current_user.name,fecha_actual=fecha_actual, resulset=resulset)
    except Exception as ex:
        flash("No se encontro ningun registro en la BD: " + str(ex))
    return render_template('/receta/Receta.html', fecha_actual=fecha_actual,name = current_user.name)

@receta.route('/insert')
@login_required
@roles_required('admin')
def insert():
    return render_template('/receta/InsertarReceta.html',name = current_user.name)

@receta.route('/detalle')
@login_required
@roles_required('admin')
def detalle():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('call sp_consultar_tipo_ing()')
        resulset = cursor.fetchall()
        cursor.execute('call sp_consultar_ultima_receta()')
        tabla = cursor.fetchall()
        return render_template('/receta/DetalleReceta.html',name = current_user.name, resulset=resulset, tabla=tabla)

@receta.route('/insertReceta',methods=["GET","POST"])
@login_required
@roles_required('admin')
def insertReceta():
    if request.method == 'POST':
        receta = request.form.get('receta')
        descripcion = request.form.get('descripcion')
        tiempo = request.form.get('tiempo')
        calorias = request.form.get('calorias')
     
    try:
        img = str(uuid.uuid4()) + '.png'
        imagen = request.files['imagen']
        ruta_imagen = os.path.abspath('..\\CrazyBurger\\static\\img')
        imagen.save(os.path.join(ruta_imagen, img))  
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_insertar_e_receta(%s,%s,%s,%s,%s)',(receta,descripcion,int(tiempo), calorias, img))
            connection.commit()
            connection.close()
            return redirect(url_for('receta.detalle'))

    except Exception as ex:
            flash("Ocurrio un error al registrar nuevo registro: " + str(ex))
            return redirect(url_for('receta.insert'))

@receta.route('/detalleIngrediente',methods=["GET","POST"])
@login_required
@roles_required('admin')
def detalleIngrediente():
    if request.method == 'POST':
        ingrediente = request.form.get('ingrediente')
        cantidad = request.form.get('cantidad')
        unidad = request.form.get('unidad')
    try:        
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_insertar_d_receta(%s,%s,%s)',(int(ingrediente),cantidad,unidad))
            connection.commit()
            connection.close()
            return redirect(url_for('receta.detalle'))
    except Exception as ex:
            flash("Ocurrio un error al registrar nuevo registro: " + str(ex))
            return redirect(url_for('receta.getAll'))
    


@receta.route('/updateReceta',methods=["GET","POST"])
@login_required
@roles_required('admin')
def updateReceta():
    if request.method == 'GET':
        id = request.args.get('id')
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call sp_buscar_receta_id(%s)', (int(id)))
                resulset = cursor.fetchall()
                return render_template('/receta/ActualizarReceta.html',  id = id,resulset = resulset)
        except Exception as ex:
                flash("No se encontro ningun registro en la BD: " + str(ex))

    if request.method == 'POST':
        id = request.form.get('id')
        receta = request.form.get('receta')
        descripcion = request.form.get('descripcion')
        tiempo = request.form.get('tiempo')
        calorias = request.form.get('calorias')
        usuario = current_user.id
    try:
        imagen = request.files['imagen']
        ruta_imagen = os.path.abspath('..\\CrazyBurger\\static\\img')       
        img = str(uuid.uuid4()) + '.png'
        imagen.save(os.path.join(ruta_imagen, img))  

        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_actualizar_e_receta(%s,%s,%s,%s,%s,%s,%s)',(int(id),receta,descripcion,int(tiempo), calorias, img, int(usuario)))
            connection.commit()
            connection.close()
            
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call sp_consultar_tipo_ing()')
                resulset = cursor.fetchall()
                cursor.execute('call sp_consultar_ultima_receta()')
                tabla = cursor.fetchall()
            
            return render_template('/receta/UpdateDetalle.html',  id = id,resulset = resulset,tabla=tabla)
    except Exception as ex:
            flash("Ocurrio un error al registrar nuevo registro: " + str(ex))
            return redirect(url_for('receta.getAll'))

@receta.route('/detalleUpdate')
@login_required
@roles_required('admin')
def detalleUpdate():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('call sp_consultar_tipo_ing()')
        resulset = cursor.fetchall()
        cursor.execute('call sp_consultar_ultima_receta()')
        tabla = cursor.fetchall()
        return render_template('/receta/DetalleReceta.html',name = current_user.name, resulset=resulset, tabla=tabla)
