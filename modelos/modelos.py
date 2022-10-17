import datetime
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


class ArchivoSubidoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ArchivoSubido
        include_relationships = True
        load_instance = True


class ArchivoTranformadoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ArchivoTranformado
        include_relationships = True
        load_instance = True


class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True
