import datetime
from email.policy import default
from json import load
from pyexpat import model
from xml.etree.ElementInclude import include
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    tareas = db.relationship('Tarea', cascade='all, delete, delete-orphan')

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_archivo = db.Column(db.String(256)) 
    formato_entrada = db.Column(db.String(128))
    formato_salida = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    estado = db.Column(db.String(128), default="uploaded")
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    archivos = db.relationship('Archivo', cascade='all, delete, delete-orphan')

class Archivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_archivo = db.Column(db.String(256))
    ruta_archivo = db.Column(db.String(256))
    id_tarea = db.Column(db.Integer, db.ForeignKey('tarea.id'))

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True

class TareaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tarea
        include_relationships =False
        load_instance = True
        timeStamp = fields.String()

class ArchivoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Archivo
        include_relationships = True
        load_instance = True