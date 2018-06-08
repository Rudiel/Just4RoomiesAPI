from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,MetaData
from flask import json
from decimal import Decimal
from Model.User import Usuario
app = Flask(__name__)

#Cadena de conexion a la bd
engine = create_engine(
    'mysql+pymysql://NarumaSolutions:Naruma07?@justforroomies2.c3jidg9lddo4.us-east-2.rds.amazonaws.com/JustForRoomies')

metadata = MetaData(engine)

#Se crea una sesion con la conexion ya creada
Session = sessionmaker(bind=engine)
session = Session()


@app.route('/api/GetProfiles',methods=['GET'])
def getProfiles():
    #Se hace el query a la bd
    usuarios = session.query(Usuario).all()
    #Se crea una lista vacia
    dataList= []
    #Se itera en cada usuario de la lista de usuarios que regresa el query
    for usuario in usuarios:
        #Se crea un objeto por cada usuario
        UsuarioObj ={
            'Nombre' : usuario.Nombre,
            'Apellido': usuario.Apellido,
            'IdImagen': usuario.IdImagen,
            'Nacionalidad': usuario.Nacionalidad,
            'Genero': usuario.Genero,
            'Edad': usuario.Edad,
            'IdFacebook': usuario.IdFacebook,
            'Email': usuario.Email,
            'Contrasenia': usuario.Contrasenia,
            'Descripcion': usuario.Descripcion,
            'Lugar': usuario.LugarDeseado
        }
        #Se agrega el objeto a la lista
        dataList.append(UsuarioObj)
    #Regresa el listado de objetos cerados
    return jsonify(dataList)

class DecimalEncoder(json.JSONEncoder):
    def _iterencode(self, o, markers=None):
        if isinstance(o, Decimal):
            return (str(o) for o in [o])
        return super(DecimalEncoder, self)._iterencode(o, markers)

if __name__ == '__main__':
    app.run()
