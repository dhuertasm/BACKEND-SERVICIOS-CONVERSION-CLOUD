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
    password1 = db.Column(db.String(50))
    password2 = db.Column(db.String(50))
    id_archivosubido = db.relationship('ArchivoSubido', cascade='all, delete, delete-orphan')


class ArchivoSubido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_archivo = db.Column(db.String(128))
    ruta_archivo = db.Column(db.String(128))
    formato_entrada = db.Column(db.String(128))
    formato_salida = db.Column(db.String(128))
    estado_proceso = db.Column(db.String(128))
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    id_archivotranformado = db.relationship('ArchivoTranformado', cascade='all, delete, delete-orphan')


class ArchivoTranformado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_archivo = db.Column(db.String(128))
    ruta_archivo = db.Column(db.String(128))
    formato_salida = db.Column(db.String(128))
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    id_archivosubido = db.Column(db.Integer, db.ForeignKey("archivo_subido.id"))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fileName = db.Column(db.String(256))
    newFormat = db.Column(db.String(128))
    timeStamp = db.Column(db.DateTime, default=datetime.datetime.now)
    status = db.Column(db.String(128), default="uploaded")
    outputFileName = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

class ArchivosSubidos(SQLAlchemyAutoSchema):
    class Meta:
        model = ArchivoSubido
        include_relationships = True
        load_instance = True


class ArchivosTranformados(SQLAlchemyAutoSchema):
    class Meta:
        model = ArchivoTranformado
        include_relationships = True
        load_instance = True


class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True

class TareaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tarea
        include_relationships =True
        load_instance = True
    timeStamp = fields.String()