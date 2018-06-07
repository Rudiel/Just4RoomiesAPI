from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker,mapper
from sqlalchemy import create_engine,Table,MetaData
from flask import json
from decimal import Decimal

app = Flask(__name__)

class Usuario(object):
    pass

engine = create_engine(
    'mysql+pymysql://NarumaSolutions:Naruma07?@justforroomies2.c3jidg9lddo4.us-east-2.rds.amazonaws.com/JustForRoomies')

metadata = MetaData(engine)

usuarios = Table('Usuario', metadata, autoload=True)
mapper(Usuario, usuarios)

Session = sessionmaker(bind=engine)
session = Session()


@app.route('/api/GetProfiles',methods=['GET'])
def getProfiles():
    res = session.query(Usuario).all()
    dataList= []
    for u in res:
        usuariosList ={
            'Nombre' : u.Nombre,
            'Apellido': u.Apellido,
            'IdImagen': u.Idimagen,
            'Nacionalidad': u.Nacionalidad,
            'Genero': u.Genero,
            'Edad': u.Edad,
            'IdFacebook': u.Idfacebook,
            'Email': u.Email,
            'Contrasenia': u.Contrasenia,
            'Descripcion': u.Descripcion,
            'Lugar': u.LugarDeseado
        }
        dataList.append(usuariosList)

    return jsonify(dataList)

class DecimalEncoder(json.JSONEncoder):
    def _iterencode(self, o, markers=None):
        if isinstance(o, Decimal):
            return (str(o) for o in [o])
        return super(DecimalEncoder, self)._iterencode(o, markers)

if __name__ == '__main__':
    app.run()
