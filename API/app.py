from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,MetaData
from flask import json
from decimal import Decimal
from Model.User import Usuario
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



@app.route('/api/GetProfiles',methods=['GET'])
@auth.login_required
def getProfiles():

    #Se hace el query a la bd
    usuarios = session.query(Usuario).all()
    #Se crea una lista vacia
    dataList= []
    #Se itera en cada usuario de la lista de usuarios que regresa el query
    for usuario in usuarios:
        #Se crea un objeto por cada usuario
        UsuarioObj ={
            'Id': uuid.uuid5(uuid.NAMESPACE_DNS,usuario.id),
            'Nombre' : usuario.Nombre,
            'Apellido': usuario.Apellido,
            'IdImagen': usuario.IdImagen,
            'Nacionalidad': usuario.Nacionalidad,
            'Genero': usuario.Genero,
            'Edad': usuario.Edad,
            'IdFacebook': uuid.uuid5(uuid.NAMESPACE_DNS,usuario.IdFacebook),
            'Email': usuario.Email,
            'Contrasenia': usuario.Contrasenia,
            'Descripcion': usuario.Descripcion,
            'Lugar': usuario.LugarDeseado
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


