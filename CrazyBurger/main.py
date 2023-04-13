from flask import Blueprint, render_template
from flask_security import login_required, current_user
from flask_security.decorators import roles_required,roles_accepted
from models import db
from datetime import datetime

main = Blueprint('main',__name__)


#Definimos la ruta para la pagina principal
@main.route('/')
def index():
    return render_template('index.html')

#Definimos la ruta para la pagina de perfil de usuario
@main.route('/profile')
@login_required
@roles_required('admin')
def profile():
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    return render_template('informativo.html', name = current_user.name, fecha_actual = fecha_actual)

@main.route('/productos')
@login_required
@roles_required('cliente')
def productos():
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    return render_template('products.html', name = current_user.name,fecha_actual=fecha_actual)




