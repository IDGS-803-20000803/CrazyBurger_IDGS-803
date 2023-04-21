from flask import Flask, render_template, redirect
from models import db, User, Role
from flask_login import LoginManager
from config import DevelopmentConfig
from flask_wtf.csrf import CSRFProtect
from flask_security  import Security, SQLAlchemyUserDatastore
from auth import auth
from main import main

userDataStore = SQLAlchemyUserDatastore(db, User, Role)

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

#Registramos  blueprints
app.register_blueprint(main)
app.register_blueprint(auth)

#Registramos los BluePrint de los modulos
from Puestos.routes import puestos
from Pedido.routes import pedidos
from Platillos.routes import platillos

app.register_blueprint(puestos)

from Departamentos.routes import departamento
app.register_blueprint(departamento)

from Empresa.routes import empresa
app.register_blueprint(empresa)

from Proveedor.routes import proveedor
app.register_blueprint(proveedor)

from Cliente.routes import clientes
app.register_blueprint(clientes)

from Empleados.routes import empleados
app.register_blueprint(empleados)

from Ingrediente.routes import ingrediente
app.register_blueprint(ingrediente)

from Recetas.routes import receta
app.register_blueprint(receta)
app.register_blueprint(pedidos)
app.register_blueprint(platillos)

from Compras.routes import compras
app.register_blueprint(compras)

#Definimos el LoginManger
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods = ['GET','POST'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    csrf.init_app(app)
    login_manager.init_app(app)
    security = Security(app, userDataStore)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port = 5000)