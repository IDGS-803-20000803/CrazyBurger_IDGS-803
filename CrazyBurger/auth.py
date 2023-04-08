from flask import Blueprint,render_template,redirect,url_for,request,flash
from werkzeug.security import generate_password_hash,check_password_hash
from flask_security import login_required
from flask_security.utils import login_user,logout_user, hash_password, encrypt_password
from models import db, User, Role
from flask_security import Security, SQLAlchemyUserDatastore
from dbConfig import get_connection



auth = Blueprint('auth', __name__, url_prefix='/security')

@auth.route("/login")
def login():
    return render_template('/security/login.html')

@auth.route("/login", methods=["POST"])
def login_post():
    email=request.form.get('email')
    password=request.form.get('password')
    remember= True if request.form.get('remember') else False
    
    #calculamos si existe un usuario ya registrado con ese email.
    user=User.query.filter_by(email=email).first()
    
    #Verificamos si el usuario existe y comprobamos el password
    if not user or not check_password_hash(user.password,password):
        flash('El usario y/o contrasena son incorrectos')
        return redirect(url_for('auth.login'))
    
    #Si llegamos aqui los datos son correctos y creamos una session para el usuario
    login_user(user,remember=remember)
    return redirect(url_for('main.profile'))
    

@auth.route("/register")
def register():
    return render_template('/security/register.html')

@auth.route("/register",methods=["POST"])
def register_post():
    #Datos para el registro del usuario
    email=request.form.get('email')
    name=request.form.get('name')
    password=request.form.get('password')
    apellidos=request.form.get('apellidos')
    celular = request.form.get('celular')
    codigoP = request.form.get('codigoP')
    calle = request.form.get('calle')
    colonia = request.form.get('colonia')
    password=generate_password_hash(password,method='sha256')
    #consultamos si existe un usuario ya registrado con ese email.
    user=User.query.filter_by(email=email).first()
    
    if user:
        flash('Ese correo ya esta en uso')
        return redirect(url_for('auth.register'))
    
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call sp_insertar_cliente(%s,%s,%s,%s,%s,%s,%s,%s)',(name,email,password,apellidos,celular,codigoP, calle,colonia))
            connection.commit()
            connection.close()
            flash("Registro guardado exitosamente")
    except Exception as ex:
            flash("Ocurrio un error al registrar el nuevo usuario: " + str(ex))
            return redirect(url_for('auth.register'))
    return redirect(url_for('auth.login'))
   

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
