import os
from flask import jsonify, request
from flask import send_from_directory
from flask import Response
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_restful import Resource

from modelos import db
from modelos import Usuario
from modelos import UsuarioSchema
from modelos import Tarea
from modelos import TareaSchema
from modelos import Archivo
from modelos import ArchivoSchema
from constans import UPLOAD_FOLDER

from werkzeug.utils import secure_filename

usuario_schema = UsuarioSchema()
tarea_schema = TareaSchema()
archivo_schema = ArchivoSchema()

INPUT_FILES_FOLDER = UPLOAD_FOLDER+"/"
OUTPUT_FILES_FOLDER = UPLOAD_FOLDER+"/"


class VistaRoot(Resource):
    def get(self):
        try:
            return {"MicroService": "cloud conversion tool is Ready v1"}
        except Exception as e:
            return {"satus": e}


class VistaHealth(Resource):

    def get(self):

        return {"satus": "ok"}


class VistaSignIn(Resource):

    def post(self):
        try:
            if request.json["password1"] == request.json["password2"]:
                nuevo_usuario = Usuario(
                    username=request.json["username"],
                    email=request.json["email"],
                    password=request.json["password1"],
                )

                db.session.add(nuevo_usuario)
                db.session.commit()
                token_de_acceso = create_access_token(identity=nuevo_usuario.id)
                return {"mensaje": "usuario creado exitosamente", "token": token_de_acceso, "id": nuevo_usuario.id}
            return {"mensaje": "las contrasenas no coinciden"}
        except Exception as e:
            print(e)
            return {"mensaje": f"falta {e}"}

    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.password1 = request.json.get("password", usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204


class VistaLogIn(Resource):
    def post(self):
        usuario = Usuario.query.filter(Usuario.email == request.json['email'],
                                       Usuario.password == request.json['password']).first()
        db.session.commit()
        if usuario is None:
            return {"mensaje": "El usuario no existe", "code": 404}
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"mansaje": "Inicio de sesion exitoso", "token": token_de_acceso}

class VistaTasks(Resource):
    
    @jwt_required()
    def get(self):
        if(not "user_id" in request.json):
            return Response("Bad Request", status=400)
        
        usuario = Usuario.query.get_or_404(request.json['user_id'])

        if(not "order" in request.json):
            order=0
        else:
            order=request.json['order']
        
        if(not "max" in request.json):
            if(order == 0):
                query = db.session.query(Tarea).filter_by(user_id=usuario.id).order_by(Tarea.id.asc()).all()
            else:
                query = db.session.query(Tarea).filter_by(user_id=usuario.id).order_by(Tarea.id.desc()).all()
        else:
            if(request.json['max']<=0):
                if(order == 0):
                    query = db.session.query(Tarea).filter_by(user_id=usuario.id).order_by(Tarea.id.asc()).all()
                else:
                   query = db.session.query(Tarea).filter_by(user_id=usuario.id).order_by(Tarea.id.desc()).all() 
            else:
                if(order == 0):
                    query = db.session.query(Tarea).filter_by(user_id=usuario.id).order_by(Tarea.id.asc()).limit(request.json['max']).all()
                else:
                    query = db.session.query(Tarea).filter_by(user_id=usuario.id).order_by(Tarea.id.desc()).limit(request.json['max']).all()
        return [tarea_schema.dump(tarea) for tarea in query]

    @jwt_required()
    def post(self):
        if not request.files["fileName"] or not request.values["newFormat"]:
            return Response("Bad Request", status=400)
        else:
            archivo_cargado = request.files["fileName"]
            nombre_archivo = secure_filename(archivo_cargado.filename)
            archivo_cargado.save(os.path.join(INPUT_FILES_FOLDER, nombre_archivo))
            nueva_tarea = Tarea(nombre_archivo=nombre_archivo.split(".")[0],\
                                 formato_entrada=nombre_archivo.split(".")[-1],\
                                 formato_salida=request.values["newFormat"],\
                                 user_id =get_jwt_identity())
            db.session.add(nueva_tarea)
            db.session.commit()
            nuevo_archivo = Archivo(nombre_archivo=nombre_archivo,\
                                    ruta_archivo=INPUT_FILES_FOLDER,\
                                    id_tarea=nueva_tarea.id,
                                    tiempo_proceso=''
                                    )
            db.session.add(nuevo_archivo)
            db.session.commit()
        return "Tarea creada exitosamente" 

class VistaTask(Resource):
    @jwt_required()
    def get(self, id_task):
        tarea = Tarea.query.get_or_404(id_task)
        
        return tarea_schema.dump(tarea)
    
    @jwt_required()
    def delete(self, id_task):
        tarea = Tarea.query.filter(Tarea.id == id_task, Tarea.estado == "disponible").first()
        if tarea is None:
            return {"mensaje": "Not Found", "code": 404}
        for archivo in tarea.archivos:
            try:
                os.remove(os.path.join(archivo.ruta_archivo, archivo.nombre_archivo))
            except OSError as e:
                return {"mensaje": e, "code": 404}
        db.session.delete(tarea)
        db.session.commit()
        return {"mensaje": "Archivos eliminados", "code": 204}
                  

    @jwt_required()
    def put(self, id_task):
        if not request.json["newFormat"]:
            return Response("Bad Request", status=400)
        else:
            tarea = Tarea.query.get_or_404(id_task)
            if tarea.estado == "processed":
                os.remove(os.path.join(INPUT_FILES_FOLDER, tarea.nombre_archivo))
            tarea.estado = "uploaded"
            tarea.formato_salida = request.json.get("newFormat", tarea.formato_salida)
            db.session.commit()
        return tarea_schema.dump(tarea)

class VistaArchivo(Resource):
    @jwt_required()
    def get(self,filename):        
        try:
            query = db.session.query(Archivo).filter_by(nombre_archivo=filename).all()
            if (len(query)==0):
                return Response("Not Found", status=404)
            print(query[0].ruta_archivo)
            print(query[0].nombre_archivo)
            return send_from_directory(query[0].ruta_archivo,query[0].nombre_archivo, as_attachment=True)
        except:
            return Response("Not Found", status=404)