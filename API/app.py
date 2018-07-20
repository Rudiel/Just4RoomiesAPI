from flask import Flask, request, jsonify, make_response
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
from API.Model.Usuario import Usuario
from API.Model.Habitacion import Habitacion
from API.Model.Personalidad import Personalidad
import uuid
from flask_httpauth import HTTPBasicAuth
from flask_api import status, response

app = Flask(__name__)

if __name__ == '__main__':
    app.run()

auth = HTTPBasicAuth()

# Cadena de conexion a la bd
engine = create_engine(
    'mysql+pymysql://NarumaSolutions:Naruma07?@justforroomies2.c3jidg9lddo4.us-east-2.rds.amazonaws.com/JustForRoomies')

metadata = MetaData(engine)

# Se crea una sesion con la conexion ya creada
Session = sessionmaker(bind=engine)

session = Session()

AUTH = {
    "User_J4R": "db108068-6e55-11e8-adc0-fa7ae01bbebc"
}


@auth.verify_password
def verify(username, password):
    if not username and password:
        return False
    return AUTH.get(username) == password


'''@app.route('/api/Login', methods=['POST'])
@auth.login_required
def login():
    req_data = request.get_json()

    user = req_data['Usuario']
    password = req_data['Password']

    usuario = session.query(Usuario).filter(Usuario.Email == user).first()

    if usuario is not None:
        if usuario.Contrasenia == password:
            content = {"message": "El usuario si existe"}
            return make_response(jsonify(content), status.HTTP_200_OK)
        else:
            content = {"message": "El password es invalido"}
            return make_response(jsonify(content), status.HTTP_406_NOT_ACCEPTABLE)
    else:
        content = {"message": "El usario no es correcto"}
        return make_response(jsonify(content), status.HTTP_400_BAD_REQUEST)'''


@app.route('/api/GetProfiles/Page',methods=['GET'])
@auth.login_required
def page():
    return get_paginated_list(Usuario, '/api/GetProfiles/Page', start=request.args.get('start',1,int), limit=request.args.get('limit',10,int))


def get_paginated_list(cls, url, start, limit):
    usuarios = session.query(cls).all()
    count = len(usuarios)

    if (count < start):
        return None

    objRoomie = {}

    obj = {}
    obj['start'] = start
    obj['limit'] = limit
    obj['count'] = count

    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)

    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)

    usuarios = usuarios[(start - 1):(start - 1 + limit)]

    #dataList = []

    usuariosList = []

    #dataList.append(obj)
    # Se itera en cada usuario de la lista de usuarios que regresa el query
    for usuario in usuarios:

        room = session.query(Habitacion).filter(Habitacion.IdUsuario == usuario.id).first()

        RoomObj = {}
        if room is not None:
            RoomObj = {
                'Id': room.IdHabitacion,
                'Amueblado': room.Amueblado,
                'Costo': room.Costo,
                'Latitud': room.Latitud,
                'Longitud': room.Longitud
            }
        personalidad = session.query(Personalidad).filter(Personalidad.IdUsuario == usuario.id).first()

        personObj = {}
        if personalidad is not None:
            personObj = {
                'Fumas': personalidad.Fumas,
                'Mascotas': personalidad.Mascotas,
                'Estudias': personalidad.Estudias,
                'Activo': personalidad.Activo,
                'Fiestero': personalidad.Fiestero,
                'Cocinas': personalidad.Cocinas
            }
        # Se crea un objeto por cada usuario
        UsuarioObj = {
            'Id': str(usuario.id),
            'Nombre': usuario.Nombre,
            'Apellido': usuario.Apellido,
            'IdImagen': usuario.IdImagen,
            'Nacionalidad': usuario.Nacionalidad,
            'Genero': usuario.Genero,
            'Edad': usuario.Edad,
            'IdFacebook': str(usuario.IdFacebook),
            'Email': usuario.Email,
            'Contrasenia': usuario.Contrasenia,
            'Descripcion': usuario.Descripcion,
            'Lugar': usuario.LugarDeseado,
            'Personalidad': personObj,
            'Room': RoomObj
        }

        # Se agrega el objeto a la lista
        usuariosList.append(UsuarioObj)

    #dataList.append(usuariosList)

    objRoomie = {
        'Pagination': obj,
        'Roomies': usuariosList
    }

    session.commit()

    # Regresa el listado de objetos cerados
    return jsonify(objRoomie)

@app.route('/api/GetProfiles', methods=['GET'])
@auth.login_required
def getProfiles():
    # Se hace el query a la bd
    usuarios = session.query(Usuario).all()

    # Se crea una lista vacia
    dataList = []
    # Se itera en cada usuario de la lista de usuarios que regresa el query
    for usuario in usuarios:

        room = session.query(Habitacion).filter(Habitacion.IdUsuario == usuario.id).first()

        RoomObj = {}
        if room is not None:
            RoomObj = {
                'Id': room.IdHabitacion,
                'Amueblado': room.Amueblado,
                'Costo': room.Costo,
                'Latitud': room.Latitud,
                'Longitud': room.Longitud
            }
        personalidad = session.query(Personalidad).filter(Personalidad.IdUsuario == usuario.id).first()

        personObj = {}
        if personalidad is not None:
            personObj = {
                'Fumas': personalidad.Fumas,
                'Mascotas': personalidad.Mascotas,
                'Estudias': personalidad.Estudias,
                'Activo': personalidad.Activo,
                'Fiestero': personalidad.Fiestero,
                'Cocinas': personalidad.Cocinas
            }
        # Se crea un objeto por cada usuario
        UsuarioObj = {
            'Id': str(usuario.id),
            'Nombre': usuario.Nombre,
            'Apellido': usuario.Apellido,
            'IdImagen': usuario.IdImagen,
            'Nacionalidad': usuario.Nacionalidad,
            'Genero': usuario.Genero,
            'Edad': usuario.Edad,
            'IdFacebook': str(usuario.IdFacebook),
            'Email': usuario.Email,
            'Contrasenia': usuario.Contrasenia,
            'Descripcion': usuario.Descripcion,
            'Lugar': usuario.LugarDeseado,
            'Personalidad': personObj,
            'Room': RoomObj
        }

        # Se agrega el objeto a la lista
        dataList.append(UsuarioObj)

        session.commit()

    # Regresa el listado de objetos cerados
    return jsonify(dataList)


@app.route('/api/SaveProfile', methods=['POST'])
@auth.login_required
def saveProfile():
    # Se obtienen los datos del request
    req_data = request.get_json()

    # Se asignan a constantes los datos especificos del request
    Nombre = req_data['Nombre']
    Apellido = req_data['Apellido']
    Nacionalidad = req_data['Nacionalidad']
    Email = req_data['Email']
    Genero = req_data['Genero']
    Edad = req_data['Edad']
    Descripcion = req_data['Descripcion']
    IdFacebook = req_data['IdFacebook']
    Presupuesto = req_data['Presupuesto']
    Latitud = req_data['Latitud']
    Longitud = req_data['Longitud']
    Lugar = req_data['Lugar']
    Contrasenia = req_data['Contrasenia']

    # Se crea un nuevo id
    id = str(uuid.uuid1())

    # Se crea un objeto usuario
    usuario = Usuario(id, Nombre, Apellido, "", Nacionalidad, Genero, Edad, id, Email, Contrasenia, Descripcion,
                      Presupuesto, Longitud, Latitud, Lugar)

    # Se guarda el usuario en la bd
    session.add(usuario)

    session.commit()

    # *Falta validar si la operacion se realizo con exito asi como los mensajes de error y authorization *
    return jsonify(id)


@app.route('/api/SaveRoom', methods=['POST'])
@auth.login_required
def saveRoom():
    req_data = request.get_json()

    FechaDisponibilidad = req_data['FechaDisponibilidad']
    Amueblado = req_data['Amueblado']
    Costo = req_data['Costo']
    Latitud = req_data['Latitud']
    Longitud = req_data['Longitud']
    IdUsuario = req_data['IdUsuario'].encode('utf-8')

    id = str(uuid.uuid1())

    room = Habitacion(id, IdUsuario, FechaDisponibilidad, Amueblado, Costo, Latitud, Longitud)

    session.add(room)

    session.commit()

    return jsonify(id)


@app.route('/api/LoginUsuario', methods=['POST'])
@auth.login_required
def LoginUsuario():
    req_data = request.get_json()

    Contrasenia = req_data['Contrasenia']
    Email = req_data['Email']

    Comp = session.query(Usuario).filter(Usuario.Email == Email).first()

    if Comp is not None:

        if Comp.Contrasenia == Contrasenia:
            content = {"message": "Usuario Logueado Correctamente",
                       "Code":200}
            return make_response(jsonify(content), status.HTTP_200_OK)

        else:
            content = {"message":"El Password es Incorrecto",
                       "Code":400}
            return make_response(jsonify(content),status.HTTP_400_BAD_REQUEST)

    else:
        content = {"message": "El Usuario No Existe",
                   "Code": 400}
        return make_response(jsonify(content), status.HTTP_400_BAD_REQUEST)


@app.route('/api/LoginFace', methods=['POST'])
@auth.login_required
def LoginFace():
    req_data = request.get_json()

    IdFacebook = req_data['IdFacebook']

    Comp = session.query(Usuario).filter(Usuario.IdFacebook == IdFacebook).first()

    if Comp is not None:

        room = session.query(Habitacion).filter(Habitacion.IdUsuario == Comp.id).first()
        RoomObj = {}
        if room is not None:
            RoomObj = {
                'Id': room.IdHabitacion,
                'Amueblado': room.Amueblado
            }
        personalidad = session.query(Personalidad).filter(Personalidad.IdUsuario == Comp.id).first()

        personObj = {}
        if personalidad is not None:
            personObj = {
                'Fumas': personalidad.Fumas,
                'Mascotas': personalidad.Mascotas,
                'Estudias': personalidad.Estudias,
                'Activo': personalidad.Activo,
                'Fiestero': personalidad.Fiestero,
                'Cocinas': personalidad.Cocinas
            }

        UsObj = {
            'Nombre': Comp.Nombre,
            'Apellido': Comp.Apellido,
            'IdImagen': Comp.IdImagen,
            'Nacionalidad': Comp.Nacionalidad,
            'Genero': Comp.Genero,
            'Edad': Comp.Edad,
            'IdFacebook': str(Comp.IdFacebook),
            'Email': Comp.Email,
            'Contrasenia': Comp.Contrasenia,
            'Descripcion': Comp.Descripcion,
            'Lugar': Comp.LugarDeseado,
            'Personalidad': personObj,
            'Room': RoomObj,
            'Personladidad': Personalidad
        }

    else:

        return "El usuario no existe"

    session.commit()

    return jsonify(UsObj)


@app.route('/api/CreateProfile', methods=['POST'])
@auth.login_required
def createUser():
    # TODO crear un usuario con el Nombre. Apellido, Correo electronico y contrasenia

    return None


@app.route('/api/CreatePersonality', methods=['POST'])
@auth.login_required
def createPersonality():
    req_data = request.get_json()

    IdUsuario = req_data['IdUsuario'].encode('utf-8')
    Nacionalidad = req_data['Nacionalidad']
    Idioma = req_data['Idioma']
    Edad = req_data['Edad']
    Longitud = req_data['Longitud']
    Latitud = req_data['Latitud']
    Fumas = req_data['Fumas']
    Mascotas = req_data['Mascotas']
    Activo = req_data['Activo']
    Fiestero = req_data['Fiestero']
    Estudias = req_data['Estudias']
    Cocinas = req_data['Cocinas']

    usuario = session.query(Usuario).filter(Usuario.id == IdUsuario).first()

    if usuario is not None:
        usuario.Nacionalidad = Nacionalidad
        usuario.Edad = Edad
        usuario.LatitudDeseada = Latitud
        usuario.LongitudDeseada = Longitud

        session.commit()

        id = str(uuid.uuid1())

        personalidad = Personalidad(id, usuario.id, Fumas, Mascotas, Estudias, Activo, Fiestero, Cocinas)

        session.add(personalidad)

    session.commit()

    return jsonify(IdUsuario)


def bad_request(message):
    response = jsonify({'message': message})
    response.status_code =400
    return response
