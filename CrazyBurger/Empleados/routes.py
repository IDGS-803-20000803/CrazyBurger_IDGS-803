from flask import Blueprint
from flask_security import login_required, current_user
from flask import render_template, url_for, flash, redirect, request
from dbConfig import get_connection
import json

empleados = Blueprint('empleados', __name__,url_prefix='/empleados')

@empleados.route('/getAll')
@login_required
def getAll():
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_empleados()')
            resulset = cursor.fetchall()
            print(resulset)
            return render_template('/empleados/empleados.html', name = current_user.name, resulset=resulset)
        
    except Exception as ex:

        flash("No se encontro ningun registro en la BD: " + str(ex))
    
        return render_template('/empleados/empleados.html', name = current_user.name)

@empleados.route('/insertarEmpleado', methods=['GET','POST'])
@login_required
def insertarEmpleado():

    if request.method == 'GET':

        # Buscar los puestos
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_puestos()')
            puestos = cursor.fetchall()
        
        # Buscar los departamentos
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_departamentos()')
            departamentos = cursor.fetchall()

        return render_template('/empleados/insertarEmpleado.html', name = current_user.name, puestos=puestos, departamentos=departamentos)
    
    if request.method == 'POST':

        nombres = request.form['nombres']
        ape_paterno = request.form['ape_paterno']
        ape_materno = request.form['ape_materno']
        foto_perfil = request.form['foto_perfil']
        rfc = request.form['rfc']
        curp = request.form['curp']
        num_seguro_social = request.form['num_seguro_social']
        celular = request.form['celular']
        alergias = request.form['alergias']
        observaciones = request.form['observaciones']
        codigo_postal = request.form['codigo_postal']
        calle = request.form['calle']
        colonia = request.form['colonia']
        puesto_id = request.form['puesto_id']
        departamento_id = request.form['departamento_id']
        usuario_id = request.form['usuario_id']

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call sp_insertar_empleado(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)',(nombres,ape_paterno,ape_materno,foto_perfil,rfc,curp,num_seguro_social,celular,alergias,observaciones,codigo_postal,calle,colonia,puesto_id,departamento_id, usuario_id))
                connection.commit()
                flash("Empleado insertado correctamente")
                return redirect(url_for('empleados.getAll'))
        except Exception as ex:
            flash("Error al insertar el empleado: " + str(ex))

            return redirect(url_for('empleados.getAll'))

@empleados.route('/obtenerEmpleado', methods=['GET'])
@login_required
def obtenerEmpleado():

    if request.method == 'GET':
        empleado_id = request.args.get('id')
        connection = get_connection()
        with connection.cursor () as cursor:
                cursor.execute('call sp_consultar_empleado_por_id(%s)', (empleado_id))
                empleado = cursor.fetchall()
                connection.commit()
                connection.close()

        # Buscar los puestos
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_puestos()')
            puestos = cursor.fetchall()

        # Buscar los departamentos
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_consultar_departamentos()')
            departamentos = cursor.fetchall()

        return render_template('/empleados/actualizarEmpleado.html', name = current_user.name, empleado=empleado, puestos=puestos, departamentos=departamentos)

@empleados.route('/actualizarEmpleado', methods=['POST'])
@login_required
def actualizarEmpleado():

    if request.method == 'POST':

        empleado_id = request.form['empleado_idEdit']
        nombres = request.form['nombresEdit']
        ape_paterno = request.form['ape_paternoEdit']
        ape_materno = request.form['ape_maternoEdit']
        foto_perfil = request.form['foto_perfilEdit']
        rfc = request.form['rfcEdit']
        curp = request.form['curpEdit']
        num_seguro_social = request.form['num_seguro_socialEdit']
        celular = request.form['celularEdit']
        alergias = request.form['alergiasEdit']
        observaciones = request.form['observacionesEdit']
        codigo_postal = request.form['codigo_postalEdit']
        calle = request.form['calleEdit']
        colonia = request.form['coloniaEdit']
        puesto_id = request.form['puesto_idEdit']
        departamento_id = request.form['departamento_idEdit']
        usuario_id = request.form['usuario_idEdit']

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call sp_actualizar_empleado(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)',(empleado_id, nombres,ape_paterno,ape_materno,foto_perfil,rfc,curp,num_seguro_social,celular,alergias,observaciones,codigo_postal,calle,colonia,puesto_id,departamento_id, usuario_id))
                connection.commit()
                connection.close()
                flash("Empleado actualizado correctamente")
                return redirect(url_for('empleados.getAll'))
            
        except Exception as ex:
            
            flash("Error al actualizar el empleado: " + str(ex))

            return redirect(url_for('empleados.getAll'))

@empleados.route('/eliminarEmpleado', methods=['GET'])
@login_required
def eliminarEmpleado():
    
        if request.method == 'GET':
            empleado_id = request.args.get('id')
            connection = get_connection()
            with connection.cursor () as cursor:
                    cursor.execute('call sp_eliminar_empleado(%s)', (empleado_id))
                    connection.commit()
                    connection.close()
                    flash("Empleado eliminado correctamente")
                    return redirect(url_for('empleados.getAll'))