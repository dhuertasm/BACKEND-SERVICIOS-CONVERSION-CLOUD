from flask import request
from flask import send_from_directory
from flask import Response
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token
from flask_restful import Resource

from modelos import db
from modelos import Usuario
from modelos import UsuarioSchema
from modelos import Tarea
from modelos import TareaSchema

usuario_schema = UsuarioSchema()
tarea_schema = TareaSchema()

OUTPUT_FILES_FOLDER = "media/"

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
                    password1=request.json["password1"],
                    password2=request.json["password2"],
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
                                       Usuario.password1 == request.json['password1']).first()
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

class VistaTask(Resource):
    @jwt_required()
    def get(self, id_task):
        tarea = Tarea.query.get_or_404(id_task)
        return tarea_schema.dump(tarea)

class VistaArchivo(Resource):
    @jwt_required()
    def get(self,filename):

        try:
            return send_from_directory(OUTPUT_FILES_FOLDER,filename, as_attachment=True)
        except FileNotFoundError:
            return Response("Not Found", status=404)