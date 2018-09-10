from flask import Flask, request, jsonify, make_response, json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
from API.Model.Usuario import Usuario
from API.Model.Habitacion import Habitacion
from API.Model.Amistad import Amistad
from API.Model.Personalidad import Personalidad
import uuid
from flask_httpauth import HTTPBasicAuth
from flask_api import status, response
from pyfcm import FCMNotification
import datetime

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

AUTH = {
    "User_J4R": "db108068-6e55-11e8-adc0-fa7ae01bbebc"
}


@auth.verify_password
def verify(username, password):
    if not username and password:
        return False
    return AUTH.get(username) == password


@app.route('/api/GetProfiles/Page', methods=['GET'])
@auth.login_required
def page():
    return get_paginated_list(Usuario, '/api/GetProfiles/Page', start=request.args.get('start', 1, int),
                              limit=request.args.get('limit', 10, int))


def get_paginated_list(cls, url, start, limit):
    session = Session()
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

    # dataList = []

    usuariosList = []

    # dataList.append(obj)
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

    # dataList.append(usuariosList)

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
    session = Session()

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
    session = Session()

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
    session = Session()

    req_data = request.get_json()

    FechaDisponibilidad = req_data['FechaDisponibilidad']
    Amueblado = req_data['Amueblado']
    Costo = req_data['Costo']
    Latitud = req_data['Latitud']
    Longitud = req_data['Longitud']
    IdUsuario = req_data['IdUsuario'].encode('utf-8')

    room = session.query(Habitacion).filter(Habitacion.IdUsuario == IdUsuario).first()

    if room is not None:
        # Editar habitacion
        room.Amueblado = Amueblado
        room.Longitud = Longitud
        room.Latitud = Latitud
        room.Costo = Costo
        room.FechaDisponibilidad = FechaDisponibilidad

        session.commit()

        content = {"message": "Habitacion editada correctamente",
                   "Code": 200}
        return make_response(jsonify(content), status.HTTP_200_OK)

    else:
        # Nueva habitacion
        id = str(uuid.uuid1())

        newRoom = Habitacion(id, IdUsuario, FechaDisponibilidad, Amueblado, Costo, Latitud, Longitud)

        session.add(newRoom)

        session.commit()

        content = {"message": "Habitacion creada correctamente",
                   "Code": 200}
        return make_response(jsonify(content), status.HTTP_200_OK)


@app.route('/api/LoginUsuario', methods=['POST'])
@auth.login_required
def LoginUsuario():
    session = Session()

    req_data = request.get_json()

    Contrasenia = req_data['Contrasenia']
    Email = req_data['Email']

    Comp = session.query(Usuario).filter(Usuario.Email == Email).first()

    if Comp is not None:

        if Comp.Contrasenia == Contrasenia:
            content = {"message": "Usuario Logueado Correctamente",
                       "Code": 200}
            return make_response(jsonify(content), status.HTTP_200_OK)

        else:
            content = {"message": "El Password es Incorrecto",
                       "Code": 400}
            return make_response(jsonify(content), status.HTTP_400_BAD_REQUEST)

    else:
        content = {"message": "El Usuario No Existe",
                   "Code": 400}
        return make_response(jsonify(content), status.HTTP_400_BAD_REQUEST)


@app.route('/api/LoginFace', methods=['POST'])
@auth.login_required
def LoginFace():
    session = Session()

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
    session = Session()

    req_data = request.get_json()

    Nombre = req_data['Nombre']
    Apellido = req_data['Apellido']
    Imagen = req_data['Imagen']
    Email = req_data['Email']
    Contrasenia = req_data['Contrasenia']

    if Nombre and Apellido and Imagen and Email and Contrasenia is not None:

        userAlready = session.query(Usuario).filter(Usuario.Email == Email).first()
        if userAlready is None:

            id = str(uuid.uuid1())
            usuario = Usuario(id, Nombre, Apellido, id, "", 0, 0, id, Email, Contrasenia, "", 0, 0, 0,
                              "")

            session.add(usuario)

            result = session.add(usuario)

            session.commit()

            print(result)

            content = {"UserID": id,
                       "message": "Usuario Creado con exito",
                       "Code": 200}
            return make_response(jsonify(content), status.HTTP_200_OK)

        else:
            content = {"message": "El Usuario ya existe",
                       "Code": 400}
            return make_response(jsonify(content), status.HTTP_400_BAD_REQUEST)
    else:
        content = {"message": "Algun campo esta vacio",
                   "Code": 400}
        return make_response(jsonify(content), status.HTTP_400_BAD_REQUEST)


@app.route('/api/CreatePersonality', methods=['POST'])
@auth.login_required
def createPersonality():
    session = Session()

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

        content = {"message": "Se guardo la informacion correctamente",
                   "Code": 200}
        return make_response(jsonify(content), status.HTTP_400_BAD_REQUEST)


    else:
        content = {"message": "El usuario no existe",
                   "Code": 400}
        return make_response(jsonify(content), status.HTTP_400_BAD_REQUEST)


@app.route('/api/EditProfile')
@auth.login_required
def editProfile():
    session = Session()
    req_data = request.get_json()

    # Terminar funcion de editar perfil


def bad_request(message):
    response = jsonify({'message': message})
    response.status_code = 400
    return response


@app.route('/api/sendNotification', methods=['GET'])
def sendNotification():
    push_service = FCMNotification(
        api_key="AAAAxOPDl_w:APA91bGCRzNWhu9DWBa9WICdaG2KVFGsZf_bDTWyPI6T7uiRqWFhI_B69P-Fgf0nE6eeccIl0cPfuPwaWcnHo5McLMHF4e1iQ8sCM69Fr7ksnAc6049Yt4MB3TNRmvX1oLc3giwuoN0YYnySvtfO96sqKSBEiVPp0g")

    # registration_id = "dUkj7m266mo:APA91bHC_x_a2SarndoHW4F7UL1GEGMUMsfIEYEZJ2RGwi-g8n8ZrAoyMvDb3SAan_Lrds7_VY86xO72TO6G2H20rOc3Uz32yVjo2S9HCSNIybDZk2_hYrdrwGdv7HIHKs2KG6TUymG4VZRcYzjvrbQFGTfbMvoywg"
    registration_id = "diDbllRXYv4:APA91bEcDKv3zUWPLQJag80wZaUS4zk-Mafm-5Amge3yRVVj_2A9kaQlTgYEC3rX5icihkoXPW4Ww_YiSOhqxMhI6Oak0FNy0F7-uo5gyEvUlEljr9OouwAbMIm9b7QVn7NpM08shl6jTDCWlsfK5hBYKA6EgviBDA"
    message_title = "Titulo"
    message_body = "Hola"

    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,
                                               message_body=message_body)

    if (result.get('success') == 1):
        return make_response("Push Enviada", status.HTTP_200_OK)
    else:
        return make_response("Push No enviada", status.HTTP_400_BAD_REQUEST)


@app.route('/api/RequestAmistad', methods=['POST'])
def RequestAmistad():
    session = Session()

    req_data = request.get_json()

    Emisor = req_data['Emisor'].encode('utf-8')
    Receptor = req_data['Receptor'].encode('utf-8')
    IdChat = req_data['IdChat'].encode('utf-8')

    Existe = session.query(Amistad).filter(Amistad.Receptor == Receptor and Amistad.Emisor == Emisor).first()
    if Existe is None:
        IdAmistad = str(uuid.uuid1())
        Hora = datetime.datetime.now().time()
        Fecha = datetime.datetime.now().date()
        newRelation = Amistad(IdAmistad, IdChat, Receptor, Emisor, Hora, Fecha, 1)

        session.add(newRelation)

        session.commit()

        content = {"message": "Se establecio una relacion",
                   "Code": 200}

        return make_response(jsonify(content), status.HTTP_200_OK)
    else:
        content = {"message": "Existe una relacion",
                   "Code": 200}

        return make_response(jsonify(content), status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route('/api/GetSolicitud', methods=['GET'])
@auth.login_required
def GetSolicitud():
    session = Session()

    Usuario = request.args.get('IdUsuario').encode('utf-8')

    Solicitudes = session.query(Amistad).all()

    # Se crea una lista vacia
    dataList = []
    # Se itera en cada usuario de la lista de usuarios que regresa el query
    for Solicitud in Solicitudes:

        if Usuario == Solicitud.Receptor.strip() and Solicitud.Estatus == 1:

            SolicitudObj = {}
            if Solicitud is not None:
                SolicitudObj = {
                    'id': str(Solicitud.id),
                    'IdChat': str(Solicitud.idChat),
                    'Emisor': str(Solicitud.Emisor),
                    'Receptor': str(Solicitud.Receptor),
                    'Fecha': str(Solicitud.Fecha),
                    'Hora': str(Solicitud.Hora),
                    'Estatus': Solicitud.Estatus
                }

            dataList.append(SolicitudObj)

    session.commit()

    # Regresa el listado de objetos cerados
    return jsonify(dataList)


@app.route('/api/GetChat', methods=['GET'])
@auth.login_required
def GetChat():
    session = Session()

    User = request.args.get('IdUsuario').encode('utf-8')

    Solicitudes = session.query(Amistad).all()

    # Se crea una lista vacia
    dataList = []
    # Se itera en cada usuario de la lista de usuarios que regresa el query
    for Solicitud in Solicitudes:

        if User == Solicitud.Receptor and Solicitud.Estatus == 2:

            SolicitudObj = {}
            if Solicitud is not None:
                SolicitudObj = {
                    'id': str(Solicitud.id),
                    'IdChat': str(Solicitud.idChat),
                    'Emisor': str(Solicitud.Emisor),
                    'Receptor': str(Solicitud.Receptor),
                    'Fecha': str(Solicitud.Fecha),
                    'Hora': str(Solicitud.Hora),
                    'Estatus': Solicitud.Estatus
                }
            dataList.append(SolicitudObj)

    session.commit()

    # Regresa el listado de objetos cerados
    return jsonify(dataList)


@app.route('/api/RechazarSolicitud', methods=['POST'])
@auth.login_required
def RechazarSolicitud():
    session = Session()
    req_data = request.get_json()

    IdSolicitud = req_data['IdSolicitud'].encode('utf-8')

    Solicitud = session.query(Amistad).filter(Amistad.id == IdSolicitud).first()

    if Solicitud is not None:
        Solicitud.Estatus = 3

    session.commit()

    content = {"message": "Se Rechazo la solicitud",
               "Code": 200}

    return make_response(jsonify(content), status.HTTP_200_OK)


@app.route('/api/AceptarSolicitud', methods=['POST'])
@auth.login_required
def Aceptarsolicitud():
    session = Session()
    req_data = request.get_json()

    IdSolicitud = req_data['IdSolicitud'].encode('utf-8')

    Solicitud = session.query(Amistad).filter(Amistad.id == IdSolicitud).first()

    if Solicitud is not None:
        Solicitud.Estatus = 2

    session.commit()

    content = {"message": "Se Acepto la solicitud",
               "Code": 200}

    return make_response(jsonify(content), status.HTTP_200_OK)
