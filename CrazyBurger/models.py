from flask_sqlalchemy import SQLAlchemy
#Importamos la clase UserMixin de  flask_login
from flask_security import UserMixin,RoleMixin
import datetime
from sqlalchemy import DECIMAL
db = SQLAlchemy()

# Define models
roles_users = db.Table('roles_users',
        db.Column('userId', db.Integer(), db.ForeignKey('user.id')),
        db.Column('roleId', db.Integer(), db.ForeignKey('role.id')))

class User(db.Model, UserMixin):
    
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    
class Role(RoleMixin, db.Model):
    
    __tablename__='role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))

class Cliente(db.Model):
    __tablename__ ='cliente'
    id = db.Column(db.Integer(), primary_key=True)
    nombres = db.Column(db.String(255))
    apellidos = db.Column(db.String(255))
    celular = db.Column(db.String(10))
    codigo_postal = db.Column(db.String(20))
    calle = db.Column(db.String(255))
    colonia = db.Column(db.String(255))
    fecha_creacion = db.Column(db.DateTime())
    fecha_modificacion = db.Column(db.DateTime())
    usuario_modificacion = db.Column(db.Integer)
    baja = db.Column(db.Boolean())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('clientes', lazy='dynamic'))

class Puesto(db.Model):
    __tablename__ ='puesto'
    id = db.Column(db.Integer(), primary_key=True)
    puesto = db.Column(db.String(255))
    descripcion = db.Column(db.String(255))
    baja = db.Column(db.Boolean())
    fecha_creacion = db.Column(db.DateTime())
    fecha_modificacion = db.Column(db.DateTime())
    usuario_modificacion = db.Column(db.Integer)

class Departamento(db.Model):
    __tablename__ ='departamento'
    id = db.Column(db.Integer(), primary_key=True)
    departamento = db.Column(db.String(255))
    descripcion = db.Column(db.String(255))
    baja = db.Column(db.Boolean())
    fecha_creacion = db.Column(db.DateTime())
    fecha_modificacion = db.Column(db.DateTime())
    usuario_modificacion = db.Column(db.Integer)

class Empresa(db.Model):
    __tablename__ ='empresa'
    id = db.Column(db.Integer(), primary_key=True)
    razon_social = db.Column(db.String(255))
    correo = db.Column(db.String(255))
    direccion = db.Column(db.String(255))
    rfc = db.Column(db.String(18))
    fecha_modificacion = db.Column(db.DateTime())
    usuario_modificacion = db.Column(db.Integer)

class Ingrediente(db.Model):
    __tablename__='ingrediente'
    id = db.Column(db.Integer(), primary_key=True)
    ingrediente = db.Column(db.String(255))
    unidad_medida = db.Column(db.String(100))
    stock_minimo = db.Column(db.DECIMAL(10,3))
    baja = db.Column(db.Boolean())
    fecha_creacion = db.Column(db.DateTime())
    fecha_modificacion = db.Column(db.DateTime())
    usuario_modificacion = db.Column(db.Integer)

class Receta(db.Model):
    __tablename__='receta'
    id = db.Column(db.Integer(), primary_key=True)
    receta = db.Column(db.String(255))
    descripcion = db.Column(db.String(255))
    tiempo_preparacion = db.Column(db.Integer())
    calorias = db.Column(db.String(100))
    foto_receta = db.Column(db.String(255))
    baja = db.Column(db.Boolean())
    fecha_creacion = db.Column(db.DateTime())
    fecha_modificacion = db.Column(db.DateTime())
    usuario_modificacion = db.Column(db.Integer)

class DetalleReceta(db.Model):
    __tablename__='detalle_receta'
    id = db.Column(db.Integer(), primary_key=True)
    cantidad = db.Column(db.String(255))
    unidad_medida = db.Column(db.String(255))
    baja = db.Column(db.Boolean())
    receta_id = db.Column(db.Integer, db.ForeignKey('receta.id'))
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingrediente.id'))
    receta = db.relationship('Receta', backref='detalles')
    ingrediente = db.relationship('Ingrediente', backref='detalles')