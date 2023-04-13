from flask_sqlalchemy import SQLAlchemy
#Importamos la clase UserMixin de  flask_login
from flask_security import UserMixin,RoleMixin
import datetime

db = SQLAlchemy()

# Define models
roles_users = db.Table('roles_users',
        db.Column('userId', db.Integer(), db.ForeignKey('user.id')),
        db.Column('roleId', db.Integer(), db.ForeignKey('role.id')))

class User(db.Model, UserMixin):
    
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
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

class Receta(db.Model):
    __tablename__ = 'receta'
    id = db.Column(db.Integer(), primary_key = True)
    nombre = db.Column(db.String(250))
    fecha_creacion = db.Column(db.DateTime())
    fecha_modificacion = db.Column(db.DateTime())
    usuario_modificacion = db.Column(db.Integer)
    baja = db.Column(db.Boolean())
    stock_minimo = db.Column(db.Integer)
    unidad_medida = db.Column(db.Integer)

class Platillo(db.Model):
    __tablename__ = 'platillo'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(250))
    descripcion = db.Column(db.String(250))
    baja = db.Column(db.Boolean())
    fecha_creacion = db.Column(db.DateTime())
    fecha_modificacion = db.Column(db.DateTime())
    usuario_modificacion = db.Column(db.Integer)
    costo = db.Column(db.Float)
    receta_id = db.Column(db.Integer, db.ForeignKey('receta.id'))
    receta = db.relationship('Receta', backref = db.backref('platillos', lazy = 'dynamic'))

class Pedido(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key = True)
    fecha_pedido = db.Column(db.DateTime())
    baja = db.Column(db.Boolean())
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    cliente = db.relationship('Cliente', backref = db.backref('pedidos', lazy = 'dynamic'))

class Detalle_Pedido(db.Model):
    __tablename__ = 'detalle_pedido'
    id = db.Column(db.Integer, primary_key = True)
    cantidad = db.Column(db.Integer)
    baja = db.Column(db.Boolean())
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'))
    platillo_id = db.Column(db.Integer, db.ForeignKey('platillo.id'))
    pedido = db.relationship('Pedido', backref = db.backref('detalle_pedidos', lazy = 'dynamic'))
    platillo = db.relationship('Platillo', backref = db.backref('detalle_platilllos', lazy = 'dynamic'))