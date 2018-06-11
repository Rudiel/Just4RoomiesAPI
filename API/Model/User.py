from sqlalchemy import Column, Integer, String, Binary, Numeric, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Usuario(Base):
    __tablename__ = 'Usuario'

    id = Column(Binary, primary_key=True)
    Nombre = Column(String)
    Apellido = Column(String)
    IdImagen = Column(String)
    Nacionalidad = Column(String)
    Genero = Column(Float)
    Edad = Column(Integer)
    IdFacebook = Column(Binary)
    Email = Column(String)
    Contrasenia = Column(String)
    Descripcion = Column(String)
    Presupuesto = Column(Numeric)
    LatitudDeseada = Column(Numeric)
    LongitudDeseada = Column(Numeric)
    LugarDeseado = Column(String)

    def __init__(self,Id, Nombre=None, Apellido=None, IdImagen=None, Nacionalidad=None, Genero=None, Edad=None,
                 IdFacebook=None,
                 Email=None, Contrasenia=None, Descripcion=None, Presupuesto=None, LongitudDeseada=None,
                 LatitudDeseada=None,
                 LugarDeseado=None):
        self.id = Id
        self.Nombre = Nombre
        self.Apellido = Apellido
        self.IdImagen = IdImagen
        self.Nacionalidad = Nacionalidad
        self.Genero = Genero
        self.Edad = Edad
        self.IdFacebook = IdFacebook
        self.Email = Email
        self.Contrasenia = Contrasenia
        self.Descripcion = Descripcion
        self.Presupuesto = Presupuesto
        self.LongitudDeseada = LongitudDeseada
        self.LatitudDeseada = LatitudDeseada
        self.LugarDeseado = LugarDeseado

