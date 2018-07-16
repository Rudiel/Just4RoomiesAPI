from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,MetaData
from flask import json
from decimal import Decimal
from API.Model.Usuario import Usuario
from API.Model.Habitacion import Habitacion
from API.Model.Personalidad import Personalidad
import uuid
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)

if __name__ == '__main__':
    app.run()

auth= HTTPBasicAuth()

#Cadena de conexion a la bd
engine = create_engine(
    'mysql+pymysql://NarumaSolutions:Naruma07?@justforroomies2.c3jidg9lddo4.us-east-2.rds.amazonaws.com/JustForRoomies')

metadata = MetaData(engine)

#Se crea una sesion con la conexion ya creada
Session = sessionmaker(bind=engine)

session = Session()

AUTH = {
    "User_J4R": "db108068-6e55-11e8-adc0-fa7ae01bbebc"
}

@auth.verify_password
def verify(username,password):
    if not username and password:
        return False
    return AUTH.get(username)== password

@app.route('/api/Login',methods=['POST'])
@auth.login_required
def login():
    req_data = request.get_json()

    Usuario = req_data['Usuario']
    Pass = req_data['Password']

    return None



@app.route('/api/GetProfiles',methods=['GET'])
@auth.login_required
def getProfiles():

    #Se hace el query a la bd
    usuarios = session.query(Usuario).all()
    #Se crea una lista vacia
    dataList= []
    #Se itera en cada usuario de la lista de usuarios que regresa el query
    for usuario in usuarios:

        room = session.query(Habitacion).filter(Habitacion.IdUsuario == usuario.id).first()

        RoomObj = {}
        if room is not None:
            RoomObj = {
                'Id': room.IdHabitacion,
                'Amueblado' : room.Amueblado
            }
        personalidad = session.query(Personalidad).filter(Personalidad.IdUsuario == usuario.id).first()

        personObj = {}
        if personalidad is not None:
            personObj = {
                 'Fumas' : personalidad.Fumas,
                 'Mascotas' : personalidad.Mascotas,
                 'Estudias' : personalidad.Estudias,
                 'Activo' : personalidad.Activo,
                 'Fiestero' : personalidad.Fiestero,
                 'Cocinas' : personalidad.Cocinas
            }
        #Se crea un objeto por cada usuario
        UsuarioObj ={
            #'Id': uuid.uuid5(uuid.NAMESPACE_DNS,usuario.id),
            'Nombre' : usuario.Nombre,
            'Apellido': usuario.Apellido,
            'IdImagen': usuario.IdImagen,
            'Nacionalidad': usuario.Nacionalidad,
            'Genero': usuario.Genero,
            'Edad': usuario.Edad,
            #'IdFacebook': uuid.uuid5(uuid.NAMESPACE_DNS,usuario.IdFacebook),
            'Email': usuario.Email,
            'Contrasenia': usuario.Contrasenia,
            'Descripcion': usuario.Descripcion,
            'Lugar': usuario.LugarDeseado,
            'Personalidad' : personObj,
            'Room': RoomObj
        }

        #Se agrega el objeto a la lista
        dataList.append(UsuarioObj)

        session.commit()

    #Regresa el listado de objetos cerados
    return jsonify(dataList)

@app.route('/api/SaveProfile', methods=['POST'])
@auth.login_required
def saveProfile():

        #Se obtienen los datos del request
        req_data = request.get_json()

        #Se asignan a constantes los datos especificos del request
        Nombre = req_data['Nombre']
        Apellido = req_data ['Apellido']
        Nacionalidad = req_data ['Nacionalidad']
        Email = req_data ['Email']
        Genero = req_data['Genero']
        Edad = req_data['Edad']
        Descripcion = req_data ['Descripcion']
        IdFacebook = req_data ['IdFacebook']
        Presupuesto = req_data['Presupuesto']
        Latitud = req_data ['Latitud']
        Longitud = req_data['Longitud']
        Lugar = req_data['Lugar']
        Contrasenia = req_data['Contrasenia']

        #Se crea un nuevo id
        id= str(uuid.uuid4())

        #Se crea un objeto usuario
        usuario = Usuario(id,Nombre,Apellido,"",Nacionalidad,Genero,Edad,id,Email,Contrasenia,Descripcion,Presupuesto,Longitud, Latitud,Lugar)

        #Se guarda el usuario en la bd
        session.add(usuario)

        session.commit()

        #*Falta validar si la operacion se realizo con exito asi como los mensajes de error y authorization *
        return  jsonify(id)


@app.route('/api/SaveRoom',methods=['POST'])
@auth.login_required
def saveRoom():

    req_data = request.get_json()


    FechaDisponibilidad = req_data['FechaDisponibilidad']
    Amueblado = req_data['Amueblado']
    Costo = req_data ['Costo']
    Latitud = req_data ['Latitud']
    Longitud = req_data['Longitud']
    IdUsuario = str(uuid.uuid5(uuid.NAMESPACE_DNS,req_data['IdUsuario'].encode('utf-8')))


    id= str(uuid.uuid4())

    room = Habitacion(id,IdUsuario , FechaDisponibilidad, Amueblado, Costo, Latitud, Longitud)

    session.add(room)

    session.commit()

    return jsonify(id)


@app.route('/api/savePerson',methods=['POST'])
@auth.login_required
def savePerson():

    req_data = request.get_json()

    Fumas  = req_data['Fumas']
    Mascotas = req_data['Mascotas']
    Estudias = req_data['Estudias']
    Activo = req_data['Activo']
    Fiestero = req_data['Fiestero']
    Cocinas = req_data['Cocinas']
    IdUsuario = str(uuid.uuid5(uuid.NAMESPACE_DNS,req_data['IdUsuario'].encode('utf-8')))


    id= str(uuid.uuid4())

    personalidad = Habitacion(id,IdUsuario , Fumas, Mascotas, Estudias, Activo, Fiestero, Cocinas)

    session.add(personalidad)

    session.commit()

    return jsonify(id)


@app.route('/api/LoginUsuario',methods=['POST'])
@auth.login_required
def LoginUsuario():
    req_data = request.get_json()

    Contrasenia = req_data['Contrasenia']
    Email = req_data['Email']

    Comp= session.query(Usuario).filter(Usuario.Email == Email).first()


    if Comp is not None:

      if Usuario.Contrasenia==Contrasenia:
           return "Usuario Correcto"
    else:

        return "Contraseña incorrecta"
    return "El usuario no existe"
    session.commit()

    return jsonify(id)

@app.route('/api/LoginFace',methods=['POST'])
@auth.login_required
def LoginFace():
    req_data = request.get_json()

    IdFacebook = req_data['IdFacebook']

    Comp= session.query(Usuario).filter(Usuario.IdFacebook == IdFacebook).first()


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
              # 'IdFacebook': uuid.uuid5(uuid.NAMESPACE_DNS,usuario.IdFacebook),
              'Email': Comp.Email,
              'Contrasenia': Comp.Contrasenia,
              'Descripcion': Comp.Descripcion,
              'Lugar': Comp.LugarDeseado,
              'Personalidad': personObj,
              'Room': RoomObj
            }

    else:


     return "El usuario no existe"


    session.commit()

    return jsonify(UsObj)
