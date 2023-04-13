from flask import Flask, render_template, redirect
from flask import request
from flask import url_for
from flask import flash
from flask import Blueprint, render_template
from flask_security import login_required, current_user
from flask_security.decorators import roles_required,roles_accepted
from dbConfig import get_connection
from datetime import datetime

platillos = Blueprint('platillos', __name__, url_prefix = '/catalogo')

@platillos.route('/productos', methods = ['GET'])
def productos():
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call show_products()')
            resulset = cursor.fetchall()
            print(resulset)
            return render_template('platillos.html', fecha_actual = fecha_actual, platillos = resulset)
    except Exception as exception:
        flash('No fue posible encontrar ningun producto' + str(exception))
    return render_template('platillos.html', fecha_actual = fecha_actual)