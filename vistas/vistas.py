from flask import request
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from modelos import db
from modelos import Usuario
from modelos import UsuarioSchema

usuario_schema = UsuarioSchema()


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
        except Exception as e:
            print(e)
            return {"mensaje": f"falta {e}"}

    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("password1", usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204


class VistaLogIn(Resource):

    pass


