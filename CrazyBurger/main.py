from flask import Blueprint,render_template,redirect,url_for,request,flash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required,roles_accepted
from models import db
from datetime import datetime
from dbConfig import get_connection

main = Blueprint('main',__name__)


#Definimos la ruta para la pagina principal
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

#Definimos la ruta para la pagina de perfil de usuario
@main.route('/profile')
@login_required
@roles_accepted('admin','empleado')
def profile():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('call sp_total_ventas()')
        totalV = cursor.fetchall()
    
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('call sp_pedidos_terminados()')
        pedidos = cursor.fetchall()

    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    return render_template('informativo.html',pedidos=pedidos,totalV=totalV, name = current_user.name,fecha_actual=fecha_actual, active='profile')

#Definimos la ruta para la pagina de perfil de usuario
@main.route('/productos')
@login_required
@roles_accepted('cliente')
def productos():
    return redirect(url_for('platillos.getAll'))





