from sqlalchemy import Column, Integer, String, Binary, Numeric, Float, Date, Boolean, ForeignKey,SmallInteger
from API.Model.base import Base

class Personalidad(Base):
    __tablename__ = 'Personalidad'

    IdPersonalidad = Column(Binary, primary_key=True)
    IdUsuario = Column(Binary, ForeignKey('Usuario.id'))
    Fumas = Column(SmallInteger)
    Mascotas = Column(SmallInteger)
    Estudias = Column(Integer)
    Activo = Column(SmallInteger)
    Fiestero = Column(SmallInteger)
    Cocinas = Column(SmallInteger)

    def __init__(self, IdPersonalidad=None, IdUsuario=None, Fumas=None, Mascotas=None,
                 Estudias=None, Activo=None, Fiestero=None, Cocinas=None):
        self.IdPersonalidad = IdPersonalidad
        self.IdUsuario = IdUsuario
        self.Fumas = Fumas
        self.Mascotas = Mascotas
        self.Estudias = Estudias
        self.Activo= Activo
        self.Fiestero = Fiestero
        self.Cocinas = Cocinas