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

class Proveedor(db.Model):
    __tablename__ ='proveedor'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True, nullable=False)
    razon_social = db.Column(db.String(250), nullable=False, unique=True)
    rfc = db.Column(db.String(20), nullable=False, unique=True)
    alias = db.Column(db.String(240), nullable=False, unique=True)
    baja = db.Column(db.Boolean(), nullable=False)
    correo = db.Column(db.String(250), nullable=False)
    celular = db.Column(db.String(15), nullable=False)
    ciudad = db.Column(db.String(250), nullable=False)
    estado = db.Column(db.String(105), nullable=False)
    codigo_postal = db.Column(db.String(10), nullable=False)
    calle = db.Column(db.String(250), nullable=False)
    colonia = db.Column(db.String(250), nullable=False)
    fecha_creacion = db.Column(db.DateTime(), nullable=False)
    fecha_modificacion = db.Column(db.DateTime(), nullable=False)
    usuario_modificacion = db.Column(db.Integer, nullable=False)
    

class Empleados(db.Model):
    __tablename__ ='empleados'
    id = db.Column(db.Integer(), primary_key=True)
    nombres = db.Column(db.String(255))
    ape_paterno = db.Column(db.String(255))
    ape_materno = db.Column(db.String(255))
    foto_empleado = db.Column(db.String(255))
    rfc = db.Column(db.String(15))
    curp = db.Column(db.String(18))
    num_seguro_social = db.Column(db.String(45))
    celular = db.Column(db.String(10))
    alergias = db.Column(db.String(255))
    observaciones = db.Column(db.String(255))
    codigo_postal = db.Column(db.String(20))
    calle = db.Column(db.String(255))
    colonia = db.Column(db.String(255))
    baja = db.Column(db.Boolean())
    fecha_creacion = db.Column(db.DateTime())
    fecha_modificacion = db.Column(db.DateTime())
    usuario_modificacion = db.Column(db.Integer)
    puesto_id = db.Column(db.Integer, db.ForeignKey('puesto.id'))
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamento.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('empleados', lazy='dynamic'))
    puesto = db.relationship('Puesto', backref=db.backref('empleados', lazy='dynamic'))
    departamento = db.relationship('Departamento', backref=db.backref('empleados', lazy='dynamic'))

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

class Menu(db.Model):
    __tablename__='menu'
    id = db.Column(db.Integer(), primary_key=True)
    costo = db.Column(db.DECIMAL(10,3))
    baja = db.Column(db.Boolean())
    fecha_creacion = db.Column(db.DateTime())
    fecha_modificacion = db.Column(db.DateTime())
    usuario_modificacion = db.Column(db.Integer)
    receta_id = db.Column(db.Integer, db.ForeignKey('receta.id'))
    receta = db.relationship('Receta', backref='menu')
    

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
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    pedido = db.relationship('Pedido', backref = db.backref('detalle_pedidos', lazy = 'dynamic'))
    menu = db.relationship('Menu', backref = db.backref('detalle_pedidos', lazy = 'dynamic'))

class Inventario(db.Model):
    __tablename__='inventario'
    id = db.Column(db.Integer, primary_key = True)  
    cantidad_disponible = db.Column(db.DECIMAL(10,3))
    unidad_medida = db.Column(db.String(100))
    fecha_alta = db.Column(db.DateTime())
    fecha_vencimiento = db.Column(db.DateTime())
    fecha_modificacion = db.Column(db.DateTime())
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingrediente.id'))
    ingrediente = db.relationship('Ingrediente', backref='inventario')

class Tipo_salida(db.Model):
    __tablename__='tipo_salida'
    id = db.Column(db.Integer, primary_key = True)  
    tipo_salida = db.Column(db.String(250))

class Tipo_entrada(db.Model):
    __tablename__='tipo_entrada'
    id = db.Column(db.Integer, primary_key = True)  
    tipo_entrada = db.Column(db.String(250))

class Salida(db.Model):
    __tablename__='salida'
    id = db.Column(db.Integer, primary_key = True)  
    fecha_salida = db.Column(db.DateTime())
    cantidad = db.Column(db.DECIMAL(10,3))
    unidad_medida = db.Column(db.String(100))
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'))
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingrediente.id'))
    tipo_salida_id = db.Column(db.Integer, db.ForeignKey('tipo_salida.id'))
    ingrediente = db.relationship('Ingrediente', backref='salida')
    empleado = db.relationship('Empleados', backref='salida')
    tipo_salida = db.relationship('Tipo_salida', backref='salida')

class Entrada(db.Model):
    __tablename__='entrada'
    id = db.Column(db.Integer, primary_key = True)  
    fecha_entrada = db.Column(db.DateTime())
    fecha_vencimiento = db.Column(db.DateTime())
    cantidad = db.Column(db.DECIMAL(10,3))
    unidad_medida = db.Column(db.String(100))
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'))
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'))
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingrediente.id'))
    tipo_entrada_id = db.Column(db.Integer, db.ForeignKey('tipo_entrada.id'))
    ingrediente = db.relationship('Ingrediente', backref='entrada')
    empleado = db.relationship('Empleados', backref='entrada')
    tipo_entrada = db.relationship('Tipo_entrada', backref='entrada')
    proveedor = db.relationship('Proveedor', backref='entrada')