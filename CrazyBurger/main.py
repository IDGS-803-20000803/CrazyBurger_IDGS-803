from flask import Blueprint,render_template,redirect,url_for,request,flash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from models import db
from datetime import datetime

main = Blueprint("main", __name__)


# Definimos la ruta para la pagina principal
@main.route("/")
def index():
    return render_template("index.html", active="index")

@main.route('/contact')
def contact():
    return render_template('contact.html', active='contact')

#Definimos la ruta para la pagina de perfil de usuario
@main.route('/profile')
@login_required
@roles_accepted('admin','empleado')
def profile():
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    return render_template('informativo.html', name = current_user.name,fecha_actual=fecha_actual, active='profile')

#Definimos la ruta para la pagina de perfil de usuario
@main.route('/productos')
@login_required
@roles_accepted('cliente')
def productos():
    return redirect(url_for('platillos.getAll'))





