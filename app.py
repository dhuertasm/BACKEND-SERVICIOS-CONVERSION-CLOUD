from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api


from modelos import db

from vistas import VistaSignIn
from vistas import VistaLogIn
from vistas import VistaHealth
from vistas import VistaRoot
from vistas import VistaTasks
from vistas import VistaTask
from vistas import VistaArchivo

UPLOAD_FOLDER = './media'
ALLOWED_EXTENSIONS = {'txt', 'mp3', 'acc', 'ogg', 'wav', 'wma'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conversion.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['UPLOADED_FOLDER'] = UPLOAD_FOLDER

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaRoot, '/')

api.add_resource(VistaHealth, '/health')
api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaLogIn, '/login')
api.add_resource(VistaTasks, '/api/tasks')
api.add_resource(VistaTask, '/api/tasks/<int:id_task>')
api.add_resource(VistaArchivo, '/api/files/<filename>')

jwt = JWTManager(app)
