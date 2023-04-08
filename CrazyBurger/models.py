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
    