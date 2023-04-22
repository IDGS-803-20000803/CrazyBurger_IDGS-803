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

menu = Blueprint('menu', __name__,url_prefix='/menu')

@menu.route('/getAll')
@login_required
@roles_required('admin')
def getAll():
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_menu()')
            resulset = cursor.fetchall()
            return render_template('/menu/Menu.html', name = current_user.name,fecha_actual=fecha_actual, resulset=resulset, active='menu')
    except Exception as ex:
        flash("No se encontro ningun registro en la BD: " + str(ex))
    return render_template('/menu/Menu.html', fecha_actual=fecha_actual,name = current_user.name, active='menu')

@menu.route('/insert')
@login_required
@roles_required('admin')
def insert():
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_receta()')
            resulset = cursor.fetchall()
            return render_template('/menu/InsertarMenu.html', name = current_user.name,resulset=resulset, active='menu')
    except Exception as ex:
        flash("No se encontro ningun registro en la BD: " + str(ex))
        return render_template('/menu/Menu.html',name = current_user.name, active='menu')

@menu.route('/insertarMenu',methods=["GET","POST"])
@login_required
@roles_required('admin')
def insertarMenu():
    if request.method == 'POST':
        receta = request.form.get('receta')
        costo = request.form.get('costo')
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_insertar_menu(%s,%s)',(int(receta),Decimal(costo)))
            connection.commit()
            connection.close()
    except Exception as ex:
            flash("Ocurrio un error al registrar el platillo: " + str(ex))
            return redirect(url_for('menu.insert'), name = current_user.name, active='menu')
    return redirect(url_for('menu.getAll'), name = current_user.name, active='menu')


@menu.route('/updateMenu', methods=['GET','POST'])
@login_required
@roles_required('admin')
def updateMenu():
    if request.method == 'GET':
        id = request.args.get('id')
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call sp_buscar_menu_id(%s)', (int(id)))
                resulset = cursor.fetchall()
                return render_template('/menu/ActualizarMenu.html',  id = id,resulset = resulset, active='menu', name = current_user.name)
        except Exception as ex:
                flash("No se encontro ningun registro en la BD: " + str(ex))
                return redirect(url_for('menu.getAll'), name = current_user.name, active='menu')
        
    if request.method == 'POST':
        id = request.form.get('id')
        costo = request.form.get('costo')
        usuario = current_user.id
        try:
            connection = get_connection()
            with connection.cursor () as cursor:
                cursor.execute('call sp_actualizar_menu(%s,%s,%s)', (int(id),Decimal(costo),usuario))
                connection.commit()
                connection.close()
                return redirect(url_for('menu.getAll'), name = current_user.name, active='menu')
        except Exception as ex:
            flash("No se pude actualizar el registro: " + str(ex))
            return redirect(url_for('menu.getAll'), name = current_user.name, active='menu')


@menu.route('/deleteMenu', methods=['GET','POST'])
@login_required
@roles_required('admin')
def deleteMenu():
    if request.method == 'GET':
        id = request.args.get('id')
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call sp_buscar_menu_id(%s)', (int(id)))
                resulset = cursor.fetchall()
                return render_template('/menu/EliminarMenu.html',  id = id,resulset = resulset, active='menu', name = current_user.name)
        except Exception as ex:
                flash("No se encontro ningun registro en la BD: " + str(ex))
                return redirect(url_for('menu.getAll'))
        
    if request.method == 'POST':
        id = request.form.get('id')
        usuario = current_user.id
        try:
            connection = get_connection()
            with connection.cursor () as cursor:
                cursor.execute('call sp_delete_menu(%s,%s)', (int(id), usuario))
                connection.commit()
                connection.close()
                return redirect(url_for('menu.getAll'), name = current_user.name, active='menu')
        except Exception as ex:
            flash("No se pude eliminar el registro: " + str(ex))
        return redirect(url_for('menu.getAll'), name = current_user.name, active='menu')
    